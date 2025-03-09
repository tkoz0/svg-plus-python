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

image = svgimage((0,0),(5,6),200,240)
style_line1 = attrs(stroke='black',stroke_width=0.05,fill='none')
style_font1 = attrs(fill='black',font_size='0.02em')

y = 2.5
A = vec(0.5,y)
B = vec(1.5,y)
C = vec(2.5,y)
image += group([
    path(pathseq().M(C).A(A,1,1).Z(),attrs(fill='#7cf')),
    circle(2,2.5,y),
    circle(1,1.5,y),
    group([
        *(circle(0.05,P) for P in (A,B,C))
    ],attrs(fill='black'))
],style_line1)
image += group([
    text('Find the ratio of the larger',0.4,5.0),
    text('circle to the shaded region.',0.4,5.5)
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
