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

image = svgimage((0,0),(20,20),250,250)
style_line1 = attrs(stroke='black',stroke_width=0.25,fill='none')
style_font1 = attrs(fill='black',font_size='0.1em')

r = 5*sqrt(6)-5*sqrt(2)
u = vec.polard(1,-45)
v = vec.polard(1,45)
s = r*(2+sqrt(3))
x = 20
L = vec((20-(s*u+r*v).x)/2,20-(20-(r*v+s*u).x)/2-r*v.x)
T = L+s*u
B = L+r*v
R = T+r*v
Cr = L+(1+sqrt(3))*r*u
Cx = B+r*u

linegroup = group([
    group([
        line(T-r*u,T),
        line(vec.midpoint(T-r*u,T)+v,vec.midpoint(T-r*u,T)-v)
    ],attrs(stroke='red')),
    path(pathseq().M(B+2*r*u).A(B,r,r)),
    path(pathseq().M(L+sqrt(3)*r*u).A(T,r,r)),
    line(L,R,attrs=attrs(stroke='#7cf')),
    polyline([T-r*u,L,B,R,T]),
    line(vec.midpoint(B,B+r*u)+v,vec.midpoint(B,B+r*u)-v),
    group([
        *(circle(0.3,P) for P in (L,T,B,R,Cr,Cx))
    ],attrs(fill='black'))
],style_line1)
image += linegroup

image += group([
    text('5&radic;6 - 5&radic;2',L+(5,-13),attrs=attrs(fill='red')),
    text('x',L+(6,-1),attrs=attrs(fill='#7cf',font_size='1.5em'))
],style_font1)

SVG_STRS.append(str(image))

linegroup += group([
    polygon([T-r*u,B+r*u,B+r*u*(1+sqrt(3))]),
    polyline([R-r*u-u,R-r*u-u-v,R-r*u-v])
],attrs(stroke='green'))

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
