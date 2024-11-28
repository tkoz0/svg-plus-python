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

DATE = 'nov28'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(0,0),vec(20,20),300,300)
styleblack = attrs(stroke='black',stroke_width=0.1,fill='none')
fontstyle = attrs(fill='black',font_size='0.1em')

a0 = 20
P1 = vec(9,2)
P2 = P1 + vec.polard(8,a0)
P2a = P1 + vec.polard(3,a0)
P3 = P2 + vec.polard(3,a0-66)
P4 = P3 + vec.polard(-18,a0-66)
P2b = P2a + vec.polard(-15,a0-66)
P5 = vec.convcomb(P2a,P2b,0.7)
P6 = P5 + vec.polard(-13,a0-66-28)
u1 = vec.polard(1,a0)
u2 = vec.polard(1,a0-66)
u3 = (P6-P5).normalize()

svg += group([
    line(P1,P2),
    line(P3,P4),
    line(P2a,P2b),
    line(P5,P6),
    path(pathseq().M(P2a-2*u1).A(P2a-2*u2,2,2)),
    path(pathseq().M(P2-2*u1).A(P2+2*u2,2,2,sweep=True)),
    path(pathseq().M(P4+2*u2).A(P4+2*u3,2,2,sweep=True))
],styleblack)

svg += path(pathseq().M(P5).l(-3*u2).a(3*u2+3*u3,3,3).z(),
            styleblack.fill('#7cf'))
svg += path(pathseq().M(P5-3*u2).a(3*u2+3*u3,3,3),styleblack.stroke('blue'))

svg += group([
    text('66&deg;',7,4),
    text('114&deg;',15,2),
    text('152&deg;',8,18)
],fontstyle)

svg += text('x&deg;',6,10.5,fontstyle.fill('#7cf'))

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
