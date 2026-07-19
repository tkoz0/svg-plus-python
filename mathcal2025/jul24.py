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

image = svgimage((-10,-10),(10,10),250,250)
style_line1 = attrs(stroke='black',stroke_width=0.25,fill='none')
style_font1 = attrs(fill='black',font_size='0.15em')

P = vec.polard(9,-90)
pv1 = vec.polard(5,36)
pv2 = vec.polard(5,60)

def angle1(P,t) -> path:
    u = -P.normalize()
    return path(pathseq().M(P+2*u.rotater(t)).A(P+2*u.rotater(-t),2,2)
        .M(P+u).l(2*u))
def angle2(P,t) -> path:
    u = -P.normalize()
    u1 = u.rotater(t/3)
    u2 = u.rotater(-t/3)
    return path(pathseq().M(P+3*u.rotater(t)).A(P+3*u.rotater(-t),3,3)
        .M(P+2*u1).l(2*u1).M(P+2*u2).l(2*u2))

image += group([
    circle(9,0,0),
    path(pathseq().M(P).L(P+pv1).A(P+pv2,5,5,sweep=True).L(P),attrs(fill='#7cf',stroke='#49c')),
    polygon([vec.polard(9,t) for t in (30,150,270)]),
    polygon([vec.polard(9,t) for t in (54,126,198,270,342)]),
    *(angle1(vec.polard(9,t),54*pi/180) for t in (54,126,198,342)),
    *(angle2(vec.polard(9,t),30*pi/180) for t in (30,150,270)),
    line(7,-8,3,-5.95),
    polygon([(2.9,-6.1),(3.05,-5.75),(2.7,-5.75)],attrs(fill='black'))
],style_line1)

image += text('x&deg;',7,-8,style_font1)

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
