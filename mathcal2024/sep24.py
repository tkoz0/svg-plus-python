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

DATE = 'sep24'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(0,0),vec(10,15),200,300)
styleblack = attrs(stroke='black',stroke_width=0.1,fill='none')
fontstyle = attrs(fill='black',font_size='0.05em')

P1 = vec(4,12)
P2 = vec(7,7)
s1 = vec(1,-5).normalize()
s2 = vec(P2-P1).normalize()

svg += path(pathseq().M(P2).l(-3*s2).A(P2-3*s1,3,3).Z(),styleblack.stroke('#5af').fill('#7cf'))
svg += path(pathseq().M(P1).l(1.5*s1).A(P1-1.5*s2,1.5,1.5).Z(),styleblack)

def paralleltick(P,slope):
    slope = 0.4*slope.normalize()
    return polyline([P+slope.rotated(135),P,P+slope.rotated(-135)],styleblack)

svg += paralleltick(P1+3.8*s1,s1)
svg += paralleltick(P2-1.5*s1,s1)

svg += group([
    line(P1+15*s1,P1-15*s1),
    line(P2+15*s1,P2-15*s1),
    line(P1-15*s2,P1+15*s2)
],styleblack)

svg += text('x&deg;',5.4,10.6,fontstyle)
svg += text('156&deg;',1,11,fontstyle)

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
