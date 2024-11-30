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

DATE = 'nov30'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(-10,-10),vec(10,10),300,300)
styleblack = attrs(stroke='black',stroke_width=0.1,fill='none')
fontstyle = attrs(fill='black',font_size='0.15em')

r = 8
ri = r*sqrt(3)/2
s = 6
A = vec.polard(r,90)
svg += group([
    polygon([vec.polard(r,30+60*z) for z in range(6)]),
    *(line(vec.polard(ri-0.5,z),vec.polard(ri+0.5,z)) for z in range(0,360,60)),
    path(pathseq().M(A).l(0,-s).A(A+vec.polard(s,-120),s,s).Z(),attrs(fill='#7cf',stroke='#5ac')),
    polyline([vec.polard(r,z) for z in [210,90,-90]])
],styleblack)

svg += text('x&deg;',-3,1,fontstyle)

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
