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
style_font1 = attrs(fill='black',font_size='0.12em')

xs = [2.5+4*i for i in range(6)]
ys = [5+4*i for i in range(3)]
xmin,xmax = min(xs),max(xs)
ymin,ymax = min(ys),max(ys)

image += group([
    *(line(x,ymin,x,ymax) for x in xs),
    *(line(xmin,y,xmax,y) for y in ys),
    group([circle(0.2,x,y) for x in xs for y in ys],attrs(fill='black'))
],style_line1)

image += group([
    text('A',2,15),
    text('Z',22,4),
    text('Find the number of paths',1,19),
    text('from A to Z that only go',1,21),
    text('up or to the right',1,23)
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
