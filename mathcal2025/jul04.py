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

image = svgimage((0,0),(20,10),200,100)
style_line1 = attrs(stroke='black',stroke_width=0.25,fill='none')
style_font1 = attrs(fill='black',font_size='0.2em')

image += group([
    polyline([(19,1),(1,1),(1,9)]),
    rect(1,1,5,5),
    rect(5,1,10,6)
],style_line1)

SVG_STRS.append(str(image))

image = svgimage((0,0),(20,15),200,150)

image += group([
    line(1,1,19,1),
    rect(9,1,11,3),
    rect(6,1,9,4),
    rect(11,1,15,5),
    line(1,8,19,8),
    rect(10,8,12,10),
    rect(6,8,10,12),
    rect(10,10,13,13)
],style_line1)

SVG_STRS.append(str(image))

image = svgimage((0,0),(20,20),200,200)

image += group([
    rect(9,9,11,11),
    rect(11,11,14,8),
    rect(11,9,7,5),
    rect(9,9,4,14),
    rect(9,11,15,17)
],style_line1)

SVG_STRS.append(str(image))

image = svgimage((-2,-2),(35,35),370,370)

image += group([
    rect(0,0,18,18),
    rect(18,0,33,15),
    rect(18,15,25,22),
    rect(25,15,33,23),
    rect(0,18,14,32),
    rect(14,18,18,22),
    rect(14,22,24,32),
    rect(24,22,25,23),
    rect(24,23,33,32)
],style_line1)

image += group([
    text('18',7,11),
    text('15',24,9),
    text('7',21,20),
    text('8',28,20),
    text('14',5,26),
    text('4',15,21),
    text('10',17,28),
    text('9',28,29)
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
