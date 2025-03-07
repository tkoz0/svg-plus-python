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

image = svgimage((0,0),(10,15),200,300)
style_line1 = attrs(stroke='black',stroke_width=0.1,fill='none')
style_font1 = attrs(fill='black',font_size='0.05em')

A = vec(1,13)
B = A+(0,-3*sqrt(2))
C = A+(3*sqrt(6),0)
v = C-B
u = v.normalize()
E = B+v.rotated(-90)
u2 = v.rotated(90).normalize()
r = 3
image += group([
    polygon([A,B,C]),
    line(B,B+v),
    line(B,B+v.rotated(-90)),
    rect(A,A+(1,-1)),
    polygon([B,B+u,B+u+u.rotated(-90),B+u.rotated(-90)]),
    line(B+v,B+v.rotated(-90),attrs=attrs(stroke='#7cf')),
    path(pathseq().M(E+r*u2).A(E+r*u2.rotated(-45),r,r)),
    path(pathseq().M(C+(-r,0)).A(C+vec.polard(r,-150),r,r,sweep=True))
],style_line1)
image += group([
    text('3&radic;6',3,12.8),
    text('30&deg;',5.6,12.8),
    text('45&deg;',4.2,4),
    text('x',7,7)
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
