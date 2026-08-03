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

image = svgimage((0,10),(60,50),300,200)
style_line1 = attrs(stroke='black',stroke_width=0.5,fill='none')
style_font1 = attrs(fill='black',font_size='0.5em')

a = 13*(sqrt(5+4*sqrt(2))-1)
A = vec(3,43)
h = sqrt(a*a-26*26)

def tick(A,B):
    M = vec.midpoint(A,B)
    u = (B-A).normalize().rotated(90)*2
    return line(M-u,M+u)

image += group([
    polyline([A+(0,-4),A+(4,-4),A+(4,0)]),
    polyline([A+(a,-4),A+(a+4,-4),A+(a+4,0)]),
    line(A+(a,0),A+(a+26,0),attrs=attrs(stroke='#7cf')),
    rect(A,A+(a,-a)),
    line(A+(0,-a),A+(a+26,0)),
    tick(A,A+(0,-a)),
    tick(A,A+(a,0)),
    tick(A+(0,-a),A+(a,-a)),
    tick(A+(a,-h),A+(a+26,0))
],style_line1)

image += group([
    text('x',A+(40,6))
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
