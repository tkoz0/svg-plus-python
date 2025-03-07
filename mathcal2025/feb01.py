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

image = svgimage((-1,-5),(3,1),200,300)
style_line1 = attrs(stroke='black',stroke_width=0.02,fill='none')
style_font1 = attrs(fill='black',font_size='0.2em')

def Pt(x,y) -> vec:
    return vec(x,-y)

# axes
xlo = Pt(-1,0)
xhi = Pt(3,0)
ylo = Pt(0,-1)
yhi = Pt(0,5)

image += group([
    group([
        line(xlo,xhi),
        line(ylo,yhi)
    ],attrs(stroke_width=0.05)),
    group([
        *(line(Pt(-1,y),Pt(3,y)) for y in range(1,5)),
        *(line(Pt(x,-1),Pt(x,5)) for x in range(1,3)),
    ],attrs(stroke_width=0.02,stroke_dasharray=[0.1,0.1]))
],attrs(stroke='black',fill='none'))

image += group([
    path(pathseq().M(Pt(0,0)).Q(Pt(1/2,0),Pt(1,1)).Z()),
    path(pathseq().M(Pt(1,1)).Q(Pt(3/2,2),Pt(2,4)).L(Pt(2,2)).Z())
],attrs(stroke='none',stroke_width=0.05,fill='rgba(255,0,0,0.333)'))

image += group([
    line(Pt(-1,-1),Pt(3,3)),
    path(pathseq().M(Pt(-1,1)).Q(Pt(1,-3),Pt(3,9)))
    #path(pathseq().M(Pt(-1,1)).Q(Pt(-1/2,0),Pt(0,0)).Q(Pt(1/2,0),Pt(1,1))
    #     .Q(Pt(3/2,2),Pt(2,4)).Q(Pt(5/2,6),Pt(3,9)))
],attrs(stroke='red',stroke_width=0.05,fill='none'))

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
