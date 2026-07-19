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

image = svgimage((0,0),(8,10),250,300)
style_line1 = attrs(stroke='black',stroke_width=0.1,fill='none')
style_font1 = attrs(fill='black',font_size='0.05em')

u = vec.polard(4,45)
v = u.rotated(90)

C = vec(4,3)

def tick(A,B):
    u = (B-A).rotated(90).normalize()*0.5
    M = vec.midpoint(A,B)
    return line(M-u,M+u)
def ang(P,u):
    u = vec(u).normalize()*0.5
    v = u.rotated(-90)
    return path(pathseq().M(P-v).l(u).l(v))

image += group([
    group([
        rect(C+(-2,-2),C+(2,2)),
        polygon([C,C+u,C+u+v,C+v])
    ],attrs(fill='#7cf')),
    rect(C+(-2,-2),C+(2,2)),
    polygon([C,C+u,C+u+v,C+v]),
    tick(C+(-2,-2),C+(2,-2)),
    tick(C+(2,-2),C+(2,2)),
    tick(C+(2,2),C+(-2,2)),
    tick(C+(-2,2),C+(-2,-2)),
    tick(C,C+u),
    tick(C+u,C+u+v),
    tick(C+u+v,C+v),
    tick(C+v,C),
    ang(C+(-2,-2),(1,0)),
    ang(C+(2,-2),(0,1)),
    ang(C+(-2,2),(0,-1)),
    ang(C+u,(-1,1)),
    ang(C+u+v,(-1,-1)),
    ang(C+v,(1,-1))
],style_line1)

image += group([
    text('4',0.8,3.2),
    text('Area = x',2.4,2.5)
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
