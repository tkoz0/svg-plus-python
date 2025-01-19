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

DATE = 'dec24'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(0,0),vec(10,12),200,240)
styleblack = attrs(stroke='black',stroke_width=0.1,fill='none')
fontstyle = attrs(fill='black',font_size='0.05em')

l = 6
A = vec(2,1)
B = A+(l,0)
C = A+(l,l)
D = A+(0,l)

svg += group([
    polygon([A,B,C,D]),
    line(A,C),
    line(B,D),
],styleblack)

svg += group([
    *(circle(0.2,P) for P in (A,B,C,D))
],styleblack.fill('black'))

svg += group([
    text('x = number of',1,9),
    text('Hamiltonian paths',1,10),
    text('for this graph',1,11)
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
