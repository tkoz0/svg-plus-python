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

DATE = 'nov09'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(0,0),vec(50,50),300,300)
styleblack = attrs(stroke='black',stroke_width=0.5,fill='none')
fontstyle = attrs(fill='black',font_size='0.5em')

A = vec(10,45)
u = vec(15,-15).normalize()
uu = u.rotated(-90)
B = A+40*u
C = B+9*uu
svg += group([
    polygon([A,B,C]),
    polyline([B-3*u,B-3*u+3*uu,B+3*uu])
],styleblack)
svg += line(B,C,attrs=styleblack.stroke('#7cf'))
svg += text('x',37,12,fontstyle.fill('#7cf'))
svg += group([
    text('41',10,25),
    text('40',25,40)
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
