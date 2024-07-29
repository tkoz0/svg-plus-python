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

DATE = 'jul28'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(-20,-20),vec(40,40),300,300)
styleblack = attrs(stroke='black',stroke_width=0.3,fill='none')
fontstyle = attrs(fill='black',font_size='0.5em')

y = 9
t = 1
z1 = (y+28,(y+21)/2)
z2 = ((y+35)/2,y+21)
xp1 = (y,0)
xp2 = (y+28,0)

svg += group([
    rect(0,0,7,7),
    rect(0,0,y,-y),
    rect(-y-7,-y,0,7),
    rect(-y-7,7,7,y+21),
    rect(7,0,y+28,y+21),
    line(y-t,-y/2,y+t,-y/2),
    line(y/2,-y-t,y/2,-y+t),
    line(-(y+7)/2-t/2,-y-t,-(y+7)/2-t/2,-y+t),
    line(-(y+7)/2+t/2,-y-t,-(y+7)/2+t/2,-y+t),
    line(-(y+7)-t,(7-y)/2+t/2,-(y+7)+t,(7-y)/2+t/2),
    line(-(y+7)-t,(7-y)/2-t/2,-(y+7)+t,(7-y)/2-t/2),
    line((-y-7)-t,(y+28)/2,(-y-7)+t,(y+28)/2),
    line((-y-7)-t,(y+28)/2-t,(-y-7)+t,(y+28)/2-t),
    line((-y-7)-t,(y+28)/2+t,(-y-7)+t,(y+28)/2+t),
    line(-y/2,y+21-t,-y/2,y+21+t),
    line(-y/2-t,y+21-t,-y/2-t,y+21+t),
    line(-y/2+t,y+21-t,-y/2+t,y+21+t),
    line(z1,z1+vec.polard(t+t/2,-45)),
    line(z1,z1+vec.polard(t+t/2,-135)),
    line(z2,z2+vec.polard(t+t/2,-45)),
    line(z2,z2+vec.polard(t+t/2,45)),
    line(10,-12,3,3),
    polygon([(3,3),(3,3)+vec.polard(t+t/2,-90),(3,3)+vec.polard(t+t/2,-40)],attrs(fill='black')),
    polyline([(y,-t-t/2),(y-t-t/2,-t-t/2),(y-t-t/2,0)]),
    polyline([(7,7-t-t/2),(7-t-t/2,7-t-t/2),(7-t-t/2,7)]),
    polyline([(0,7-t-t/2),(-t-t/2,7-t-t/2),(-t-t/2,7)]),
    polyline([(7,y+21-t-t/2),(7+t+t/2,y+21-t-t/2),(7+t+t/2,y+21)])
],styleblack)
svg += line(xp1,xp2,attrs=styleblack.stroke('aqua'))
svg += text('x',20,-1,fontstyle)
svg += text('Area=49',10,-12,fontstyle)

svgstrlist.append(str(svg))

f2 = fontstyle.fill('red').font_size('0.3em')
svg += group([
    text('7',0,5),
    text('y',0,-3),
    text('y+7',-11,7),
    text('y+14',-11,35),
    text('y+21',17,35)
],f2)

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
