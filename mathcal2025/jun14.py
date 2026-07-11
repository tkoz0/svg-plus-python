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

image = svgimage((0,0),(30,36),250,300)
style_line1 = attrs(stroke='black',stroke_width=0.25,fill='none')
style_font1 = attrs(fill='black',font_size='0.15em')

m = 7
n = 6

C = vec(23,3)
B = C + (0,4*n)
A = B + vec.polard(3*m,220)

M = vec.midpoint(A,C)
P = vec.convcomb(A,B,1/3)
Q = vec.convcomb(B,C,1/4)

image += polygon([M,P,Q],style_line1.fill('#7cf'))

# for equal length marks
u = (C-A).normalize().rotated(90)
P1 = vec.midpoint(A,M)
P2 = vec.midpoint(M,C)

image += group([
    line(A,C),
    line(A,P,attrs=attrs(stroke='red')),
    line(P,B,attrs=attrs(stroke='green')),
    line(B,Q,attrs=attrs(stroke='magenta')),
    line(Q,C,attrs=attrs(stroke='darkorange')),
    line(P1-u,P1+u),
    line(P2-u,P2+u)
],style_line1)

labels = group([
    text('m',7,18,attrs(fill='red')),
    text('2m',14,24,attrs(fill='green')),
    text('n',24,24,attrs(fill='magenta')),
    text('3n',24,12,attrs(fill='darkorange')),
    text('x',15,16),
    text('A',4,14),
    text('B',24,29),
    text('C',24,4)
],style_font1)
image += labels

image += text('Area ABC is 48.',3,33,style_font1.font_size('0.2em'))

SVG_STRS.append(str(image))

# with the MPQ labeling
labels.append(text('M',13,7))
labels.append(text('P',11,21))
labels.append(text('Q',24,21))

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
