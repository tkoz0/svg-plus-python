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

image = svgimage((0,0),(4.5,4.5),250,250)

style_line1 = attrs(stroke='black',stroke_width=0.05,fill='none')
style_line2 = attrs(stroke='red',stroke_width=0.02,fill='none')
style_font1 = attrs(fill='black',font_size='0.05em')
style_font2 = attrs(fill='black',font_size='0.015em')

global_tl = vec(0.2,-0.5)
def svgcoord(p) -> vec:
    p = vec(p)
    return global_tl+vec(p.x,5-p.y)

points = [(0.5,0.5),(2,1.5),(3,0.5),(3,2),(3.5,3),(2.5,3),(1.5,4),(1.5,2.5),(0.5,2)]
points = list(map(vec,points))
label_off = [(0.1,0.25),(-0.4,0.5),(0.1,0.3),(0.2,0.1),(0,-0.2),(0,-0.2),(-0.5,-0.2),(-1,-0.1),(-0.5,-0.2)]
label_off = list(map(vec,label_off))
assert len(points) == len(label_off)

image += polygon(list(map(svgcoord,points)),style_line1.fill('#7cf'))
image += text('x',global_tl+(1.75,3),attrs=style_font1)

for i in range(len(points)):
    image += circle(0.1,svgcoord(points[i]))
    px,py = points[i]
    image += text(f'({px},{py})',svgcoord(points[i])+label_off[i],attrs=style_font2)

SVG_STRS.append(str(image))

A = vec(0.5,4)
B = vec(3.5,4)
C = vec(3.5,0.5)
D = vec(0.5,0.5)

def putline(p:vec,q:vec):
    global image
    image += line(svgcoord(p),svgcoord(q),attrs=style_line2)

putline(A,B)
putline(B,C)
putline(C,D)
putline(points[-1],A)
putline(points[-2],points[-2]+(-1,0))
putline(points[-4],points[-4]+(0,1))
putline(points[3],points[3]+(0.5,0))
putline(points[1],points[1]+(0,-1))

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
