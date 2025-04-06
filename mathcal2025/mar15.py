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
style_line1 = attrs(stroke='black',stroke_width=0.2,fill='none')
style_font1 = attrs(fill='black',font_size='0.1em')

bl1 = vec(11,5)
bl2 = vec(1,12)
blv = vec(8,0)
bl1m = vec.midpoint(bl1,bl1+blv)
bl2m = vec.midpoint(bl2,bl2+blv)
xv = vec(0,15)

square = 3
triangle = 1.5

gs1 = bl1+blv+xv
gs2 = bl2+blv

cb1 = bl1+blv+(1,-triangle*sqrt(3)/2)
cb2 = bl2+blv+(1,-square)

def rt(P):
    return polygon([P,P+vec.polard(triangle,180),P+vec.polard(triangle,-120)])

image += group([
    group([
        rect(gs1,gs1+(-square,-square)),
        rect(gs2,gs2+(-square,-square))
    ],attrs(stroke='green')),
    group([
        rt(bl1+blv),
        rt(bl2+blv+xv)
    ],attrs(stroke='red')),
    group([
        line(bl1m,bl1m+xv),
        line(bl2m,bl2m+xv)
    ],attrs(stroke='blue')),
    line(bl1,bl1+blv),
    line(bl2,bl2+blv),
    path(pathseq().M(cb1).h(0.5).v(6).l(0.5,0.5).l(-0.5,0.5).v(6).h(-0.5)),
    path(pathseq().M(cb2).h(0.5).v(7.7).l(0.5,0.5).l(-0.5,0.5).v(7.7).h(-0.5))
],style_line1)

image += group([
    text('13',22,10.5),
    text('17',12,18),
    group([
        text('x',bl1+(2.5,5)),
        text('x',bl2+(2.5,5))
    ],attrs(fill='blue'))
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
