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

DATE = 'nov06'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(0,0),vec(20,20),300,300)
styleblack = attrs(stroke='black',stroke_width=0.1,fill='none')
fontstyle = attrs(fill='black',font_size='0.1em')

svg += group([
    line(1,10,19,10),
    polyline([(18,9),(19,10),(18,11)]),
    line(16,12,16,1),
    polyline([(15,2),(16,1),(17,2)]),
    line(1,12,19,4),
    group([
        circle(0.5,5.5,10),
        circle(0.5,14,6.25)
    ],attrs(fill='black'))
],styleblack)

svg += group([
    text('(-1,3)',10,5),
    text('-2',4,9),
    text('What is the',5,15),
    text('y-intercept?',5,17)
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
