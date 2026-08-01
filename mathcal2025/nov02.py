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

image = svgimage((0,0),(25,30),250,300)
style_line1 = attrs(stroke='black',stroke_width=0.25,fill='none')
style_font1 = attrs(fill='black',font_size='0.2em')

C = vec(12.5,12.5)
r1 = 7
r2 = 11
v1 = vec.polard(r1,20)
v2 = v1.rotater(2)

# arrow stuff
A = C+(-2,-1)
B = C+(0.5,2)
u = (B-A).normalize()*0.5

image += group([
    path(pathseq().M(C).l(v2/2).a(-v2/2+v1/2,r1/2,r1/2),attrs(fill='#7cf')),
    path(pathseq().M(C).l(v1).a(-v1+v2,r1,r1,laflag=True).z()),
    path(pathseq().M(C+v1*r2/r1).A(C+v2*r2/r1,r2,r2,laflag=True)),
    path(pathseq().M(C+v2).A(C+v1,r1,r1),attrs(stroke='magenta')),
    path(pathseq().M(C+v2*r2/r1).A(C+v1*r2/r1,r2,r2),attrs(stroke='green')),
    line(C+v1,C+v1*r2/r1,attrs=attrs(stroke='red')),
    line(C+v2,C+v2*r2/r1,attrs=attrs(stroke='red')),
    line(A,B),
    polygon([B,B+u.rotated(-165),B-0.75*u,B+u.rotated(165)])
],style_line1)

image += group([
    text('a',C+(-6,8),attrs=attrs(fill='red')),
    text('b',C+(2,5.7),attrs=attrs(fill='magenta')),
    text('c',C+(5,12),attrs=attrs(fill='green')),
    text('2',C+(-6,16)),
    text('a',C+(-4,16),attrs=attrs(fill='red')),
    text('+',C+(-2,16)),
    text('b',C+(0,16),attrs=attrs(fill='magenta')),
    text('=',C+(2,16)),
    text('c',C+(4,16),attrs=attrs(fill='green')),
    text('x radians',C+(-5,-2),attrs=attrs(font_size='0.7em'))
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
