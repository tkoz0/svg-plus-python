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

image = svgimage((0,0),(25,25),250,250)
style_line1 = attrs(stroke='black',stroke_width=0.25,fill='none')
style_font1 = attrs(fill='black',font_size='0.1em')

B = vec(2,8)
h = vec(18,0)
v = vec(3,8)
T = B+h+(0,-5)

image += group([
    polygon([B,B+h,B+h+v,B+v],attrs(stroke='none',fill='#7cf')),
    polyline([B,B+v,B+v+h]),
    group([
        polyline([B,B+h,B+h+v]),
        line(B+h,T)
    ],attrs(stroke_dasharray=[0.7])),
    line(T,B),
    line(T,B+v),
    line(T,B+v+h)
],style_line1)

image += group([
    text('1',B+h+(-1.5,-1.5)),
    text('4',B+h+(1.5,-1)),
    text('7',B+(11,-0.5)),
    text('8',B+(8,-3)),
    text('Area = x',B+(10,5)),
    text('All edges of rectangular',B+(0,12)),
    text('pyramid have integer length',B+(0,14))
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
