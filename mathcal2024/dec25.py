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

DATE = 'dec25'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(0,1),vec(30,13),300,120)
styleblack = attrs(stroke='black',stroke_width=0.1,fill='none')
fontstyle = attrs(fill='black',font_size='0.1em')

O = vec(3,10)
X = O+(24,0)
Y = O+(24,-7)
a = 5

svg += group([
    polygon([O,X,Y]),
    path(pathseq().M(O+(a,0)).A(O+a*(Y-O).normalize(),a,a))
],styleblack)

svg += group([
    text('&theta;',9,9.8),
    text('24',15,12),
    text('7',28,7),
    text('25',15,5)
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
