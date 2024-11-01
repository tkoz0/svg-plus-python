import sys
sys.path.insert(0,'..')
from svgpp import *
from math import *
#from math import acos, acosh, asin, asinh, atan, atan2, atanh, ceil, comb, \
#    copysign, cos, cosh, degrees, dist, e, erf, erfc, exp, expm1, fabs, \
#    factorial, floor, fmod, frexp, fsum, gamma, gcd, hypot, inf, isclose, \
#    isfinite, isinf, isnan, isqrt, lcm, ldexp, lgamma, log, log10, log1p, \
#    log2, modf, nan, nextafter, perm, pi, pow, prod, radians, remainder, \
#    sin, sinh, sqrt, tan, tanh, tau, trunc, ulp
from datetime import datetime
from copy import deepcopy

svgstrlist: list[str] = []

################################################################################

DATE = 'oct31'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(0,0),vec(20,20),300,300)
styleblack = attrs(stroke='black',stroke_width=0.1,fill='none')
fontstyle = attrs(fill='black',font_size='0.1em')

A = vec(3,7)
B = vec(9,1)
C = vec(15,8)
D = vec(18,19)

def make_arc(P,v1,v2,r):
    v1 = v1.normalize()
    v2 = v2.normalize()
    return path(pathseq().M(P).L(P+r*v1).A(P+r*v2,r,r).Z())

def make_arrow(P,Q):
    P,Q = vec(P),vec(Q)
    u = (Q-P).normalize() * 0.5
    return [line(P,Q),polygon([Q,Q+u.rotated(150),Q+u.rotated(-150)],attrs(fill='black'))]

xarc = make_arc(D,C-D,A-D,6)
xarc.attrs = attrs(stroke='#38a',fill='#7cf')
svg += group([
    make_arc(A,D-A,B-A,4),
    make_arc(B,A-B,C-B,4),
    make_arc(C,B-C,D-C,4),
    xarc,
    polygon([A,B,C,D]),
    *make_arrow((3,9),(5,7)),
    *make_arrow((12,2),(9,3)),
    *make_arrow((17,8),(14,10)),
    *make_arrow((5,16),(16,16))
],styleblack)

svg += group([
    text('94&deg;',2,11),
    text('72&deg;',12,2.5),
    text('163&deg;',16,8),
    text('x&deg;',3,16.5)
],fontstyle)

svgstrlist.append(str(svg))

################################################################################

out = open(f'{DATE}.html','w')
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

for svgstr in svgstrlist:
    out.write(f'<hr />\n{svgstr}\n')

footer = f'''\
</body>
</html>
'''

out.write(footer)
out.close()
