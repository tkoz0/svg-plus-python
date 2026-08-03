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

image = svgimage((0,0),(32,32),250,250)
style_line1 = attrs(stroke='black',stroke_width=0.25,fill='none')
style_font1 = attrs(fill='black',font_size='0.15em')

C = vec(16,22)
B = C+(6,0)
D = C+(0,-3)
A = C+(-6,-9)
s3u = A-C
s3v = s3u.rotated(-90)
s4u = B-A
s4v = s4u.rotated(-90)

def ticks(A,B,*ts) -> list[line]:
    result = []
    u = (A-B).rotated(90).normalize()*0.5
    for t in ts:
        M = vec.lerp(A,B,t)
        result.append(line(M-u,M+u))
    return result
def tick1(A,B): return ticks(A,B,0.5)
def tick2(A,B): return ticks(A,B,0.47,0.53)
def tick3(A,B): return ticks(A,B,0.45,0.5,0.55)
def tickarrow(A,B):
    M = vec.midpoint(A,B)
    u = (B-A).normalize()
    return polyline([M+u.rotated(135),M,M+u.rotated(-135)])

# helpers for diagonal right angle markers
L = A+s3v
R = B+s4v
Lu = -s3v.normalize()
Lv = Lu.rotated(90)
Ru = -s4v.normalize()
Rv = Ru.rotated(90)

image += group([
    # rect 6
    rect(C,C+(6,6)),
    *tick1(C,B),
    *tick1(C,C+(0,6)),
    *tick1(B,B+(0,6)),
    *tick1(C+(0,6),B+(0,6)),
    polyline([C+(6,5),C+(5,5),C+(5,6)]),
    # rect 9
    rect(D,D+(-9,9)),
    *tick2(D,D+(-9,0)),
    *tick2(D+(-9,0),D+(-9,9)),
    *tick2(D+(0,9),D+(-9,9)),
    polyline([D+(0,8),D+(-1,8),D+(-1,9)]),
    # rect 12
    polygon([C,A,A+s3v,C+s3v]),
    *tick3(A,A+s3v),
    *tick3(C,C+s3v),
    *tick3(A+s3v,C+s3v),
    polyline([L+Lv,L+Lu+Lv,L+Lu]),
    # rect 15
    polyline([A,B,B+s4v,A+s4v]),
    tickarrow(A,B),
    tickarrow(B,B+s4v),
    tickarrow(B+s4v,A+s4v),
    polyline([R+Rv,R+Ru+Rv,R+Ru]),
    group([
        line(A+s4v,A),
        tickarrow(A+s4v,A)
    ],attrs(stroke='#7cf')),
    # red points
    group([
        circle(0.5,P) for P in (A,B,C,D)
    ],attrs(fill='red',stroke='red'))
],style_line1)

image += group([
    text('x',A+(2,-6),attrs=attrs(fill='#7cf')),
    text('6',B+(1,4)),
    text('D is the centroid of &#9651;ABC',1,31),
    text('A',A+(-2.5,0)),
    text('B',B+(-1,-1.5)),
    text('C',C+(-2.5,0.5)),
    text('D',D+(0.5,2))
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
