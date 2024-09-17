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

DATE = 'sep09'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(0,0),vec(10,5),400,200)
styleblack = attrs(stroke='black',stroke_width=0.05,fill='none')
fontstyle = attrs(fill='red',font_size='0.05em')

svg += group([
    rect(1,1,9,4),
    line(1,1,4,4),
    rect(1,4,1.5,3.5),
    line(0.75,2.5,1.25,2.5),
    line(2.5,3.75,2.5,4.25),
    path([path.M(1+1.5*sqrt(2),1),path.A((2.5,2.5),1.5*sqrt(2),1.5*sqrt(2),0,True)],attrs(stroke='red'))
],styleblack)
svg += text('5x&deg;',3.25,2.25,fontstyle)

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
