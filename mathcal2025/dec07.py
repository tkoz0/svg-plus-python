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

image = svgimage((0,0),(20,25),200,250)
style_line1 = attrs(stroke='black',stroke_width=0.25,fill='none')
style_font1 = attrs(fill='black',font_size='0.15em')

s = 5+3*sqrt(2)
x = 7
A = vec(10-s,5)
B = A+(2*s,0)
C = B+(0,2*s)
D = A+(0,2*s)
r = 2
O = C+(-x,-x)
P = O+vec.polard(x,-135)

def tick1(A,B):
    u = (B-A).normalize().rotated(90)*1
    M = vec.midpoint(A,B)
    return line(M-u,M+u)
def tick2(A,B):
    u = (B-A).normalize().rotated(90)*1
    M1 = vec.lerp(A,B,0.46)
    M2 = vec.lerp(A,B,0.54)
    return (line(M1-u,M1+u),line(M2-u,M2+u))

image += group([
    rect(A,C),
    line(O,P,attrs=attrs(stroke='#7cf')),
    group([
        line(vec.midpoint(A,B),B,attrs=attrs(stroke='red')),
        *tick2(vec.midpoint(A,B),B)
    ],attrs(stroke='red')),
    *tick2(A,vec.midpoint(A,B)),
    tick1(B,C),
    tick1(C,D),
    rect(A,A+(r,r)),
    rect(C,C-(r,r)),
    rect(B,B+(-r,r)),
    rect(D,D+(r,-r)),
    circle(x,O),
    path(pathseq().M(vec.midpoint(A,D)).A(vec.midpoint(A,B),s,s)),
    group([
        *(circle(0.5,P) for P in (A,vec.midpoint(A,B),O,P))
    ],attrs(fill='black'))
],style_line1)

image += text('5+3&radic;2',A+(10,-2),attrs=style_font1.fill('red'))
image += text('x',A+(10,9),attrs=style_font1)

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
