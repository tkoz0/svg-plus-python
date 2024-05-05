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

DATE = 'may05'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(-3,-3),vec(3,3),200,200)
styleblack = attrs(stroke='black',stroke_width=0.05,fill='none')

A = vec(-2.5,-2)
B = A + (5,0)
C = B + (0,4)
D = A + (3,4)
AB = vec.midpoint(A,B)
CD = vec.midpoint(C,D)
t1 = 0.5
t2 = 0.15
svg += group([
    polyline([A,B,C,D]),
    polyline([C-(0,t1),C-(t1,t1),C-(t1,0)]),
    polyline([AB-(t2,t2),AB,AB+(-t2,t2)]),
    polyline([CD-(t2,t2),CD,CD+(-t2,t2)])
],styleblack)
svg += line(A,D,attrs=styleblack.stroke('#7cf'))
svg += group([
    text('5',AB+(0,-t2)),
    text('2',CD+(-t2,-t2)),
    text('4',vec.midpoint(B,C)+(-0.5,0)),
    text('x',vec.midpoint(A,D),attrs=attrs(fill='#7cf'))
],attrs(font_size='0.05em'))

svgstrlist.append(str(svg))

E = A+(0,4)
svg += polyline([A,E,D],styleblack.stroke('red'))
svg += polyline([E+(0,-t1),E+(t1,-t1),E+(t1,0)],styleblack.stroke('red'))
svg += group([
    text('3',vec.midpoint(E,D)+(-t1,-t2)),
    text('4',vec.midpoint(A,E)+(t2,t2))
],attrs(font_size='0.05em',fill='red'))

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
