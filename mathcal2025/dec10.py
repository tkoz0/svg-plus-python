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
style_font1 = attrs(fill='black',font_size='0.2em')

L = vec(3,26)
R = L+(20,0)
M = vec.midpoint(L,R)
T = vec(15,3)
u = vec(1,-7).normalize()

def linedist(P1,P2,L1,L2):
    L = vec.midpoint(L1,L2)
    n = (L2-L1).normalize().rotated(90)
    m = vec.proj((L-P1),n).mag()
    if vec.angler(n,L-P1) > pi/2:
        n = -n
    assert vec.angler(n,L-P1) < pi/2
    mp = m*tan(vec.angler(n,P2-P1))
    return sqrt(m*m+mp*mp)
def lineto(P1,P2,L1,L2):
    return P1+(P2-P1).normalize()*linedist(P1,P2,L1,L2)
def perplineto(P,L1,L2):
    L = vec.midpoint(L1,L2)
    n = (L2-L1).normalize().rotated(90)
    m = vec.proj((L-P),n).mag()
    if vec.angler(n,L-P) > pi/2:
        n = -n
    assert vec.angler(n,L-P) < pi/2
    return P+m*n

# guess a position for the middle of the line
# this is close enough for visual representation
B = M+7.4*u
v = u.rotated(90)
print(linedist(B,B+v,L,T),linedist(B,B-v,R,T))
BR = lineto(B,B+v,R,T)
BL = lineto(B,B-v,L,T)
BRM = vec.midpoint(BR,B)
BLM = vec.midpoint(BL,B)
tv = u*0.5
ra1u = (L-T).normalize()*1.5
ra1v = ra1u.rotated(-90)
ra2u = (R-T).normalize()*1.5
ra2v = ra2u.rotated(90)

linegroup = group([
    polyline([R,T,L,M]),
    line(M,R,attrs=attrs(stroke='#7cf')),
    line(M-5*u,M+25*u),
    line(BR,BL),
    line(L,perplineto(L,R,T)),
    line(R,perplineto(R,L,T)),
    line(BRM-tv,BRM+tv), # tick
    line(BLM-tv,BLM+tv), # tick
    polyline([B-1.5*v,B-1.5*u-1.5*v,B-1.5*u]), # middle right angle
    polyline([BL+ra1u,BL+ra1u+ra1v,BL+ra1v]), # left right angle
    polyline([BR+ra2u,BR+ra2u+ra2v,BR+ra2v]), # right right angle
    group([
        *(circle(0.4,P) for P in (L,R,M,B))
    ],attrs(fill='black'))
    #path(pathseq().M(R).A(L,10,10))
],style_line1)
image += linegroup

image += group([
    text('10',L+(3,3)),
    text('x',L+(14,3))
],style_font1)

# seems like something is a little jank and calculations are off
# but it should be close enough for a reasonable visualization I guess

SVG_STRS.append(str(image))

linegroup.append(group([
    path(pathseq().M(R).A(L,10,10)),
    polyline([BL,M,BR])
],attrs(stroke='red')))

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
