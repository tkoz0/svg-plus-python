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

DATE = 'oct25'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(0,0),vec(30,40),240,320)
styleblack = attrs(stroke='black',stroke_width=0.3,fill='none')
fontstyle = attrs(fill='black',font_size='0.2em')

A = vec(3,33)
B = A+(6*sqrt(11),0)
C = B+(0,-30)
x = 25
y = 11
u = (C-A).normalize()
D = A+y*u

svg += group([
    polyline([A,B,C]),
    rect(B,B-(3,3)),
    polygon([A,B,D]),
    line(D,C,attrs=attrs(stroke='#5ac')),
    polyline([D-3*u,D-3*u+3*u.rotated(90),D+3*u.rotated(90)])
],styleblack)

svg += group([
    text('x',12,15),
    text('6&radic;11',10,38),
    text('30',25,25)
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
