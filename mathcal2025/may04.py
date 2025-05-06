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

image = svgimage((0,0),(10,15),200,300)
style_line1 = attrs(stroke='black',stroke_width=0.1,fill='none')
style_font1 = attrs(fill='black',font_size='0.075em')

p = vec(7,13)
a = sqrt(128)/3
h = 4/3

t1 = p+(0,-12)
t2 = p+vec.polarr(4,pi+asin(h/4))
t3 = p+(-6,0)
u = vec.polarr(0.75,asin(h/4))
v = u.rotated(-90)

image += group([
    polygon([p,t1,t2]),
    polygon([p,t2,t3],attrs(fill='#7cf')),
    polygon([t2,t2+v,t2+u+v,t2+u]),
    rect(p,p+(-0.75,-0.75))
],style_line1)

image += group([
    text('4',5,12),
    text('6',3,14.5),
    text('12',7.5,8)
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
