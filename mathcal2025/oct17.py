import os
import sys
sys.path.insert(0,'..')
from svgpp import *
from math import acos, acosh, asin, asinh, atan, atan2, atanh, ceil, comb, \
    copysign, cos, cosh, degrees, dist, e, erf, erfc, exp, expm1, fabs, \
    factorial, floor, fmod, frexp, fsum, gamma, gcd, hypot, inf, isclose, \
    isfinite, isinf, isnan, isqrt, lcm, ldexp, lgamma, log, log10, log1p, \
    log2, modf, nan, nextafter, perm, pi, pow, prod, radians, remainder, \
    sin, sinh, sqrt, tan, tanh, tau, trunc, ulp
from datetime import datetime
from copy import deepcopy
SVG_STRS: list[str] = []
FILE_DATE = os.path.basename(__file__).replace('.py','')
setwhitespace(4)
setprefix(f'{FILE_DATE}_')

################################################################################
# edit here to create svg images and append strings to SVG_STRS

image = svgimage((0,0),(35,35),280,280)
style_line1 = attrs(stroke='black',stroke_width=0.35,fill='none')
style_font1 = attrs(fill='black',font_size='0.2em')

x1 = 10
x2 = sqrt(436)
y1 = 15
y2 = 6
O = vec((35-x1-x2)/2,(35-y1-y2)/2)
r = 2.5

G = [
    [O          ,O+(x1,0)    ,O+(x1+x2,0)],
    [O+(0,y1)   ,O+(x1,y1)   ,O+(x1+x2,y1)],
    [O+(0,y1+y2),O+(x1,y1+y2),O+(x1+x2,y1+y2)]
]

def arrow(A,B):
    u = (B-A).normalize()
    return line(A,B),polygon([B,B+u.rotated(165),B-0.75*u,B+u.rotated(-165)])

image += group([
    rect(G[0][0],G[2][2]),
    line(G[1][0],G[1][2]),
    line(G[0][1],G[2][1]),
    rect(G[0][0],G[0][0]+(r,r)),
    rect(G[1][0],G[1][0]+(r,-r)),
    rect(G[2][0],G[2][0]+(r,-r)),
    rect(G[2][1],G[2][1]+(r,-r)),
    rect(G[2][2],G[2][2]+(-r,-r)),
    line(G[2][0],G[1][1],attrs=attrs(stroke='red')),
    line(G[1][1],G[2][2],attrs=attrs(stroke='green')),
    line(G[0][0],G[1][1],attrs=attrs(stroke='#7cf')),
    line(G[1][1],G[0][2]),
    *arrow(O+(7,-2),vec.midpoint(G[0][0],G[1][1])),
    *arrow(O+(20,-2),vec.lerp(G[0][2],G[1][1],1/3)),
    *arrow(O+(8,23),vec.midpoint(G[2][0],G[1][1])),
    *arrow(O+(18,23),vec.midpoint(G[1][1],G[2][2])),
    line(O+(18,23.4),O+(24,23.4),attrs=attrs(stroke='green',stroke_width=0.2))
],style_line1)

image += group([
    text('x',O+(6,-3),attrs=attrs(fill='#7cf')),
    text('25',O+(18,-3)),
    text('10',O+(7,26),attrs=attrs(fill='red')),
    text('&radic;436',O+(16,26),attrs=attrs(fill='green'))
],style_font1)

SVG_STRS.append(str(image))

################################################################################
# write html file

out = open(f'{FILE_DATE}.html','w')
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

for s in SVG_STRS:
    out.write(f'<hr />\n{s}\n')

footer = f'''\
</body>
</html>
'''

out.write(footer)
out.close()
