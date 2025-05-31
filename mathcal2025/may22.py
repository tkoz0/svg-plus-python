import os
import sys
sys.path.insert(0,'..')
from svgpp import *
from math import acos, acosh, asin, asinh, atan, atan2, atanh, ceil, comb, \
    copysign, cos, cosh, degrees, dist, e, erf, erfc, exp, expm1, fabs, \
    factorial, floor, fmod, frexp, fsum, gamma, gcd, hypot, inf, isclose, \
    isfinite, isinf, isnan, isqrt, lcm, ldexp, lgamma, log, log10, log1p, \
    log2, modf, nan, nextafter, perm, pi, pow, prod, radians, remainder, \
    sin, sinh, sqrt, tan, tanh, tau, trunc, ulp
from datetime import datetime
from copy import deepcopy
SVG_STRS: list[str] = []
FILE_DATE = os.path.basename(__file__).replace('.py','')
setwhitespace(4)
setprefix(f'{FILE_DATE}_')

################################################################################
# edit here to create svg images and append strings to SVG_STRS

image = svgimage((0,0),(20,20),200,200)
style_line1 = attrs(stroke='black',stroke_width=0.25,fill='none')
style_font1 = attrs(fill='black',font_size='0.1em')

image += group([
    polygon([(2,18),(18,18),(18,2)]),
    rect(8,16,10,18),
    rect(16,16,18,18),
    polygon([(10,10),(10,18),(18,2)],attrs(fill='#7cf')),
    line(5.5,17,5.5,19),
    line(6.5,17,6.5,19),
    line(13.5,17,13.5,19),
    line(14.5,17,14.5,19),
    line(9,13.5,11,13.5),
    line(9,14.5,11,14.5),
    line(14.6,12.6,16.8,12.6,attrs(stroke_width=0.1))
],style_line1)
image += text('2&radic;55',13,14,style_font1)

SVG_STRS.append(str(image))

################################################################################
# write html file

out = open(f'{FILE_DATE}.html','w')
header = f'''\
<!DOCTYPE html>
<html>
<head>
    <style type="text/css">
        body {{ background: black; }}
        svg {{ background: white; }}
    </style>
</head>
<body>
<p style="color:white;">{str(datetime.now())}</p>
'''
out.write(header)

for s in SVG_STRS:
    out.write(f'<hr />\n{s}\n')

footer = f'''\
</body>
</html>
'''

out.write(footer)
out.close()
