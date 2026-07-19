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

image = svgimage((0,0),(5,5),250,250)
style_line1 = attrs(stroke='black',stroke_width=0.05,fill='none')
style_font1 = attrs(fill='black',font_size='0.03em')

s = 3
A = vec(0.5,0.3)
C = A+(s,0)
B = A+(s,s)
D = C+vec.polard(3*sqrt(2),75)

r = 1.2
image += group([
    path(pathseq().M(C).l(0,r).A(C+(D-C).normalize()*r,r,r).M(C),
        attrs(stroke='#38b',fill='#7cf')),
    rect(A,B),
    line(B,D),
    group([
        line(A,B),
        line(C,D)
    ],attrs(stroke='red')),
    group([
        *(circle(0.1,P) for P in (A,B,C,D))
    ],attrs(fill='black')),
    line(4.2,1,3.6,1.3),
    polygon([(3.6,1.3),(3.655,1.235),(3.68,1.29)],attrs(fill='black')),
    line(0.45,3.8,1.6,3.8),
    line(2.4,3.8,3.6,3.8)
],style_line1)

image += group([
    text('A',0.05,0.5),
    text('B',3.6,3.2),
    text('C',3.65,0.5),
    text('D',4.6,4.9),
    text('x&deg;',4.3,1)
],style_font1)
image += text('AB = CD',0.5,4.5,attrs(font_size='0.05em'))

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
