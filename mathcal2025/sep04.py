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

image = svgimage((0,0),(25,25),250,250)
style_line1 = attrs(stroke='black',stroke_width=0.2,fill='none')
style_font1 = attrs(fill='black',font_size='0.1em')

L1 = vec(3,24)
L2 = vec(24,10)
l = (L2-L1).normalize()
P1 = L1 + 8*l
P2 = P1 + 10*l
ll = l.rotated(-90)
C1 = P1 + 5*ll
C2 = P2 + 5*ll
S = vec.midpoint(P1,P2)
S1 = S - l
S2 = S + l

def tick(P,u):
    return line(P-0.25*u,P+0.25*u)

linegroup = group([
    line(L1,L2),
    circle(5,C1),
    circle(5,C2),
    group([
        circle(0.2,C1),
        circle(0.2,C2)
    ],attrs(fill='black')),
    polygon([S+l,S-l,S-l+2*ll,S+l+2*ll],attrs(fill='#7cf')),
    tick(S,ll),
    tick(S+l+ll,l),
    tick(S+2*ll,ll),
    tick(S-l+ll,l),
    line(P1,C1),
    line(P2,C2),
    polyline([P1+0.5*ll,P1+0.5*ll+0.5*l,P1+0.5*l]),
    polyline([P2+0.5*ll,P2+0.5*ll-0.5*l,P2-0.5*l]),
    polyline([S1+0.5*ll,S1+0.5*ll+0.5*l,S1+0.5*l]),
    polyline([S2+0.5*ll,S2+0.5*ll-0.5*l,S2-0.5*l]),
    line(S+ll,(18,20))
],style_line1)
image += linegroup

textgroup = group([
    text('5',C1+(1.5,1.5)),
    text('5',C2+(1.5,1.5)),
    text('x',18.5,21)
],style_font1)
image += textgroup

SVG_STRS.append(str(image))

linegroup += group([
    line(S+l+2*ll,C2),
    line(S+l+2*ll,P2+2*ll),
    polyline([P2+3*ll,P2+3*ll-l,P2+2*ll-l]),
    line(S+10*ll,S-5*ll,attrs=attrs(stroke_dasharray=[0.5]))
],attrs(stroke='red'))

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
