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

image = svgimage((0,0),(25,30),250,300)
style_line1 = attrs(stroke='black',stroke_width=0.25,fill='none')
style_font1 = attrs(fill='black',font_size='0.15em')

A = vec(3,18)
C = vec(23,18)
D = vec(7,11)
E = vec(17,11)
B = vec(11,4)

def tick1(P,Q):
    M = vec.midpoint(P,Q)
    u = (P-Q).normalize().rotated(90)
    return line(M-u,M+u)
def tick2(P,Q):
    M1 = vec.lerp(P,Q,0.45)
    M2 = vec.lerp(P,Q,0.55)
    u = (P-Q).normalize().rotated(90)
    return (line(M1-u,M1+u),line(M2-u,M2+u))

image += group([
    polygon([A,B,C]),
    line(D,E),
    tick1(A,D),
    tick1(D,B),
    *tick2(B,E),
    *tick2(E,C)
],style_line1)

image += group([
    text('A',A+(-2,-0.5)),
    text('B',B+(0.5,-0.5)),
    text('C',C),
    text('D',D+(-2,-0.5)),
    text('E',E+(0.5,-0.5)),
    text('Find the ratio',3,22),
    text('of the areas of',3,25),
    text('&#9651;ABC and &#9651;DBE',3,28)
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
