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

DATE = 'dec16'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(0,0),vec(10,12.5),200,250)
styleblack = attrs(stroke='black',stroke_width=0.05,fill='none')
fontstyle = attrs(fill='black',font_size='0.05em')

gridgroup = group([
    line(1,1,1,9),
    line(1,1,9,1),
    line(9,1,9,9),
    line(1,9,9,9),
    line(1,2,9,2),
    line(8,1,8,9),
    line(2,1,2,9),
    line(1,8,9,8),
    rect(1,1,3,3),
    rect(9,1,7,3),
    rect(1,9,3,7),
    rect(9,9,7,7),
    *(line(x,1,x,2) for x in (4,5,6)),
    *(line(x,8,x,9) for x in (4,5,6)),
    *(line(1,y,2,y) for y in (4,5,6)),
    *(line(8,y,9,y) for y in (4,5,6))
],styleblack)

svg += gridgroup

svg += group([
    text('How many ways can',0.5,10),
    text('you tile the shape with',0.5,11),
    text('2 &times; 1 dominoes?',0.5,12)
],fontstyle)

svgstrlist.append(str(svg))

dstyle1 = styleblack.fill('red')
dstyle2 = styleblack.fill('orange')
svg2 = svgimage(vec(0,0),vec(10,10),200,200)
svg2 += gridgroup
svg3 = deepcopy(svg2)
svg4 = deepcopy(svg2)
svg3 += rect(2,1,4,2,attrs=dstyle1)
svg4 += rect(3,1,5,2,attrs=dstyle1)

svgstrlist.append(str(svg3))
svgstrlist.append(str(svg4))

svg5 = deepcopy(svg2)
svg5 += group([
    rect(3,1,5,2),
    rect(8,3,9,5),
    rect(7,8,5,9),
    rect(2,7,1,5)
],dstyle1)
svg5 += group([
    rect(5,1,7,2),
    rect(8,5,9,7),
    rect(5,8,3,9),
    rect(2,5,1,3)
],dstyle2)

svgstrlist.append(str(svg5))

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
