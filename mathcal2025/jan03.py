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
style_font1 = attrs(fill='black',font_size='0.07em')

C = vec(5,8)

def angle(a):
    P = C+vec.polard(4,a)
    return path(pathseq().M(P+vec.polard(1,a-120)).A(P+vec.polard(1,a+120),1,1))

def tick1(P,Q):
    M = vec.midpoint(P,Q)
    a = (P-Q).thetad()+90
    u = vec.polard(0.2,a)
    return [line(P,Q),line(M+u,M-u)]

def tick2(P,Q):
    M1 = vec.convcomb(P,Q,0.45)
    M2 = vec.convcomb(P,Q,0.55)
    a = (P-Q).thetad()+90
    u = vec.polard(0.2,a)
    return [line(P,Q),line(M1+u,M1-u),line(M2+u,M2-u)]

pts = [C+vec.polard(4,60*a) for a in range(6)]
pp0 = vec.midpoint(pts[-1],pts[-2])
pp1 = pp0+(0,-2*sqrt(3))
pp2 = vec.midpoint(pp0,pp1)

gl1 = group([
    polygon([pts[-2],pp1,pts[-1],pp2],attrs(fill='#7cf')),
    polygon(pts),
    *(line(C+vec.polard(2.75,60*a),C+vec.polard(3.25,60*a)) for a in range(6)),
    *(angle(60*a) for a in range(6)),
    polygon([pts[-1],pts[-2],pp1]),
    *tick1(pts[-1],pp2),
    *tick1(pts[-2],pp2),
    *tick2(pp0,pp2),
    *tick2(pp1,pp2),
    line(7,2,5.7,3)
],style_line1)

gl2 = group([
    *(circle(0.2,C+vec.polard(4,60*a)) for a in range(6)),
    circle(0.2,pp0),
    circle(0.2,pp1),
    circle(0.2,pp2)
],style_line1.fill('black'))

image += text('x',7.2,2.5,style_font1)
image += text('2&radic;2&radic;3',3.2,13,style_font1)
image += text('4',5.3,12.3,style_font1.font_size('0.03em'))

image += gl1
image += gl2
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
