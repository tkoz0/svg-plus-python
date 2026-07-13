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

image = svgimage((0,0),(15,15),250,250)
style_line1 = attrs(stroke='black',stroke_width=0.2,fill='none')
style_font1 = attrs(fill='black',font_size='0.1em')

C = vec(7.5,7.5)
P = C+vec.polarr(7,pi+acos(-1/7))

# arrow and helpers to draw triangle
A1 = vec(5,10.5)
A2 = vec(5.75,7)
u = (A2-A1).normalize().rotated(90) * 0.2

linegroup = group([
    circle(7,C),
    polygon([C+(7,0),C+(-7,0),P],attrs(fill='#7cf')),
    line(C+(-3,0),P),
    line(A1,A2),
    polygon([A2+u,A2-u,A2+(A2-A1).normalize()*0.6],attrs(fill='black'))
],style_line1)
image += linegroup

textgroup = group([
    text('Area = x&radic;3',3,12),
    text('4',2,9),
    text('10',8,9),
    text('8',6.5,5.5)
],style_font1)
image += textgroup

SVG_STRS.append(str(image))

# draw an extra radius and show an angle theta
linegroup.append(line(C,P,attrs=attrs(stroke='red')))
textgroup.append(text('&theta;',6,7,attrs(fill='red')))
textgroup.append(text('7',8.5,5.5,attrs(fill='red')))
r = 0.75
linegroup.append(path(pathseq().M(C+(-r,0)).A(C+(P-C).normalize()*r,r,r,sweep=True),attrs(stroke='red')))
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
