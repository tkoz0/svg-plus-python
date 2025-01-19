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

DATE = 'dec27'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(0,0),vec(10,12),200,240)
styleblack = attrs(stroke='black',stroke_width=0.1,fill='none')
fontstyle = attrs(fill='black',font_size='0.05em')

r = 4/3
C = vec(5,5)

svg += circle(3*r,C,attrs=styleblack.stroke('#59a').fill('#7cf'))

Cs = [C+vec.polard(2*r,a) for a in range(0,360,60)]

svg += group([
    *(circle(r,P) for P in Cs)
],styleblack)

svg += group([
    *(text('Area',P+(-0.7*r,0)) for P in Cs),
    *(text('=3',P+(-0.4*r,0.6*r)) for P in Cs)
],fontstyle.font_size('0.05em'))

svg += group([
    text('Find the area of',1.5,10),
    text('the largest circle',1.5,11)
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
