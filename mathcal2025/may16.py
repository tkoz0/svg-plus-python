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

image = svgimage((-10,-15),(10,5),250,250)
style_line1 = attrs(stroke='black',stroke_width=0.1,fill='none')
style_font1 = attrs(fill='black',font_size='0.075em')

u1 = vec(2,-2)
u2 = vec(2,6)
image += group([
    line(-9,0,9,0),
    line(0,-14,0,4),
    line(5,0.5,5,-0.5),
    line(-5,0.5,-5,-0.5),
    line(-0.5,-5,0.5,-5),
    line(-0.5,-10,0.5,-10),
    group([
        *(circle(0.25,p) for p in [(4,0),(-4,0),(2,-6),(0,-4),(0,-12)])
    ],attrs(fill='black')),
    line((0,-12)-0.25*u2,(0,-12)+2.5*u2),
    line((0,-4)-3*u1,(0,-4)+2.5*u1)
],style_line1)
image += group([
    text('(0,a)',-3,-4),
    text('(0,b)',-3,-12),
    text('(2,6)',3,-6),
    text('(-4,0)',-6,-1),
    text('(4,0)',4,-1),
    text('Find a + b',-6,3.5)
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
