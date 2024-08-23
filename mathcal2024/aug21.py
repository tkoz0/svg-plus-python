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

DATE = 'aug21'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(-3,-3),vec(63,73),261,300)
styleblack = attrs(stroke='black',stroke_width=0.5,fill='none')
fontstyle = attrs(fill='black',font_size='0.5em',font_style='italic')

svg += polygon([(30,0),(60,20),(30,70),(0,20)],styleblack.fill('rgba(127,191,255,0.5)'))

svg += group([
    circle(0.5,x,y)  for x in range(0,70,10) for y in range(0,80,10)
],styleblack.fill('black'))

svg += text('Area = x',15,27,fontstyle)

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
