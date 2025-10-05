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

image = svgimage((0,0),(10,10),250,250)
style_line1 = attrs(stroke='black',stroke_width=0.1,fill='none')
style_font1 = attrs(fill='black',font_size='0.04em')

A = vec(2,1)
B = A+(3,3)
v1 = vec.polard(4,60)
v2 = v1.rotated(90)
image += group([
    rect(A,B),
    polygon([B,B+v1,B+v1+v2,B+v2]),
    polygon([B,B+v2,A+(0,3)],attrs(fill='#7cf')),
    line(A+(3,0),B+v1),
    line(vec.centroid(A+(3,0),B,B+v1),(7,2.5))
],style_line1)
image += group([
    text('Area = 3',6,2),
    text('Area = 9',A+(0.25,1.75)),
    text('Area = 16',B+(-2.25,3)),
    text('x',A+(0.5,3.75))
],style_font1)

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
