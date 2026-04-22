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

image = svgimage((-11,-11),(11,11),250,250)
style_line1 = attrs(stroke='black',stroke_width=0.2,fill='none')
style_font1 = attrs(fill='black',font_size='0.1em')

A = vec.polard(10,-135)
B = vec.polard(10,-45)
C = vec.polard(10,90)

ar1,ar2 = 3,3.7

image += line(vec(),B,attrs=style_line1.stroke('#7cf'))

image += group([
    circle(10,0,0,style_line1),
    polygon([A,B,C]),
    group([
        circle(0.4,p) for p in [A,B,C,vec()]
    ],attrs(fill='black')),
    path(pathseq().M(A+(ar1,0)).A(A+vec.polard(ar1,67.5),ar1,ar1,sweep=True)
        .M(A+(ar2,0)).A(A+vec.polard(ar2,67.5),ar2,ar2,sweep=True)
        .M(B+(-ar1,0)).A(B+vec.polard(ar1,112.5),ar1,ar1)
        .M(B+(-ar2,0)).A(B+vec.polard(ar2,112.5),ar2,ar2)
        .M(C+vec.polard(ar2,-67.5)).A(C+vec.polard(ar2,-112.5),ar2,ar2)
    )
],style_line1)

image += group([
    text('45&deg;',-1,6),
    text('10&radic;2',-2,-8),
    text('__',0.6,-9.5),
    text('x',2.5,-1.5)
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
