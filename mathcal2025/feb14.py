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

image = svgimage((0,0),(3,3),250,250)
style_line1 = attrs(stroke='black',stroke_width=0.03,fill='none')
style_font1 = attrs(fill='black',font_size='0.02em')

def diagsquare(C,d):
    return polygon([C+(d,0),C+(0,d),C+(-d,0),C+(0,-d)])

C = vec(1.5,1.5)
D = C+vec.polard(1/sqrt(2),-45)
E = C+vec.polard(1/sqrt(2),-135)
X = C+(-1,0)
Y = C+(0,-1)
Z = C+(1,0)
image += group([
    diagsquare(C,1),
    diagsquare(C+(-0.8,0),0.2),
    diagsquare(C+(0.8,0),0.2),
    diagsquare(C+(0,-0.8),0.2),
    diagsquare(C+(0,0.8),0.2),
    group([
        path(pathseq().M(Z).A(Y,1/sqrt(2),1/sqrt(2)).Z()),
        path(pathseq().M(Y).A(X,1/sqrt(2),1/sqrt(2)).Z())
    ],attrs(fill='#7cf')),
    group([
        circle(0.05,D),
        circle(0.05,E)
    ],attrs(fill='black')),
    line(2.15,0.8,2.45,0.8),
    line(0.45,2.6,0.9,2.6),
    path(pathseq().M(0.2,2.6).h(0.07).l(0.07,0.3).l(0.07,-0.75).h(0.5))
],style_line1)
image += group([
    text('x',2.2,0.7),
    text('2',2.2,1.1),
    text('56',0.5,2.5),
    text('&pi;',0.6,2.85)
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
