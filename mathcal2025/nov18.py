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

image = svgimage((0,0),(15,20),225,300)
style_line1 = attrs(stroke='black',stroke_width=0.15,fill='none')
style_font1 = attrs(fill='black',font_size='0.07em')

def circle_intersect(P,Q,C,r):
    assert (P-C).mag() > r # P outside
    assert (Q-C).mag() < r # Q inside
    tmin = 0
    tmax = 1
    tmid = 0.5
    R = vec()
    while True:
        tmid = (tmin+tmax)/2
        if tmid == tmin or tmid == tmax: break
        R = vec.lerp(P,Q,tmid)
        if (R-C).mag() > r: tmin = tmid
        else: tmax = tmid
    assert abs((R-C).mag()-r) < 1e-12
    return R

O = vec(9,12)
l1 = vec.polard(1,-60)
l2 = vec.polard(1,-120)
ll = vec.polard(1,-75)
C3 = O+(0,-6)
C2 = O+(0,4)
C3T = C3+vec.polard(3,150)
C2T = C2+vec.polard(2,-30)
C3P = C3+(0,3)
C2P = C2+(0,-2)
A = circle_intersect(O-7*ll,O-5*ll,C2,2)
B = circle_intersect(O+2*ll,O+4*ll,C3,3)

def ticksat(P1,P2,*ts):
    u = (P1-P2).normalize().rotated(90)*0.4
    ret = []
    for t in ts:
        M = vec.lerp(P1,P2,t)
        ret.append(line(M-u,M+u))
    return ret

def arrow(P1,P2):
    u = (P2-P1).normalize()*0.3
    return (line(P1,P2),polygon([P2,P2+u.rotated(165),P2-0.75*u,P2+u.rotated(-165)]))

ar = 1.5
al1 = vec.polard(1,97.5)
al2 = vec.polard(1,112.5)

image += group([
    line(O+10*l1,O-8*l1),
    line(O+10*l2,O-8*l2),
    line(O+10*ll,O-8*ll),
    circle(3,C3),
    circle(2,C2),
    polyline([C3T,C3,C2,C2T]),
    group([
        *(circle(0.2,P) for P in (C2,C3,O,A,B,C2T,C3T,vec.midpoint(C3,O))),
        *arrow(vec(12,10),B+(0.6,0.3)),
        *arrow(vec(5,17),A+(-0.5,0))
    ],attrs(fill='black')),
    path(pathseq().M(O+vec.polard(ar,90)).A(O+vec.polard(ar,120),ar,ar,sweep=True)),
    group([
        *ticksat(C3,C3T,0.45,0.55),
        *ticksat(C3,vec.midpoint(C3,O),0.45,0.55),
        *ticksat(O,vec.midpoint(O,C3),0.75,0.85),
        line(O+al1*1.25,O+al1*1.75),
        line(O+al2*1.25,O+al2*1.75)
    ],attrs(stroke_width=0.1))
],style_line1)

image += group([
    text('A',4,17.5),
    text('B',12,10.5),
    text('O',O+(-1.5,0.5)),
    text('2',C2+(0.5,1)),
    text('3',C3+(-2,0)),
    text('Find',2,10),
    text('|OA||OB|',0.5,11.5)
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
