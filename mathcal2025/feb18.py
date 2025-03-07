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

image = svgimage((0,0),(5,6.5),200,260)
style_line1 = attrs(stroke='black',stroke_width=0.05,fill='none')
style_font1 = attrs(fill='black',font_size='0.03em')

A = vec(4.4,6)
u1 = vec(-3,-2.2)
B = A+u1
C = A+u1.rotated(-36)
D = A+1.6*u1.rotated(36)
v1 = (B-A).normalize().rotated(90)
v2 = (C-A).normalize().rotated(90)
M1 = vec.midpoint(A,B)
M2 = vec.midpoint(A,C)
image += group([
    polygon([A,B,C]),
    polygon([A,B,D]),
    line(M1+0.2*v1,M1-0.2*v1),
    line(M2+0.2*v2,M2-0.2*v2)
],style_line1)
image += group([
    text('2x&deg;',3,5.9),
    text('2x&deg;',3.2,5.1),
    text('2y&deg;',1.3,4.7),
    text('y&deg;',2.35,1.5)
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
