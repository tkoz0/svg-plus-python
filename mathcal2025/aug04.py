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

image = svgimage((0,0),(30,15),300,150)
style_line1 = attrs(stroke='black',stroke_width=0.25,fill='none')
style_font1 = attrs(fill='black',font_size='0.1em')

A = vec(3,2.5)
B = A+(0,10)
C = A+(24,0)
O = A+(4,4)
u = vec.polarr(1,atan(24/10))

image += group([
    polygon([A,B,C]),
    circle(4,O),
    line(O,O+(-4,0)),
    line(O,O+(0,-4)),
    line(O,O+4*u),
    line(O,B),
    line(O,C)
],style_line1)

image += group([
    text('r',1.5,5),
    text('s',1.5,10),
    text('s',6,13),
    text('10',0.5,7),
    text('24',13,2),
    text('26',13,11)
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
