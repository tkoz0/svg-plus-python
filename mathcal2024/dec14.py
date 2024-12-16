import sys
sys.path.insert(0,'..')
from svgpp import *
from math import *
#from math import acos, acosh, asin, asinh, atan, atan2, atanh, ceil, comb, \
#    copysign, cos, cosh, degrees, dist, e, erf, erfc, exp, expm1, fabs, \
#    factorial, floor, fmod, frexp, fsum, gamma, gcd, hypot, inf, isclose, \
#    isfinite, isinf, isnan, isqrt, lcm, ldexp, lgamma, log, log10, log1p, \
#    log2, modf, nan, nextafter, perm, pi, pow, prod, radians, remainder, \
#    sin, sinh, sqrt, tan, tanh, tau, trunc, ulp
from datetime import datetime
from copy import deepcopy

svgstrlist: list[str] = []

################################################################################

DATE = 'dec14'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(0,0),vec(10,10),200,200)
styleblack = attrs(stroke='black',stroke_width=0.05,fill='none')
fontstyle = attrs(fill='black',font_size='0.05em')

def cvec(a,b):
    return vec(a+1,9-b)

def cvect(a,b):
    return (cvec(a,b).x,cvec(a,b).y)

def cstr(P):
    return f'({int(P.x-1)},{int(9-P.y)})'

A = cvec(1,1)
B = cvec(3,5)
C = cvec(5,6)
D = cvec(7,2)
E = cvec(6,8)
F = cvec(2,7)

svg += polygon([A,B,C,D,E,F],styleblack.fill('#7cf'))
svg += group([
    *(circle(0.2,P) for P in (A,B,C,D,E,F))
],styleblack.fill('black'))
svg += text('x',4.3,3,fontstyle.font_size('0.1em'))

svg2 = deepcopy(svg)

svg += group([
    *(text(cstr(P),P.x-1,P.y+1) for P in (A,B,C,D)),
    text(cstr(E),E.x+0.5,E.y+0.5),
    text(cstr(F),F.x-2,F.y+0.5)
],fontstyle)

svg2 += group([
    *(text(L+cstr(P),P.x-1,P.y+1) for P,L in ((A,'A'),(B,'B'),(C,'C'),(D,'D'))),
    text('E'+cstr(E),E.x+0.5,E.y+0.5),
    text('F'+cstr(F),F.x-2.5,F.y+0.5)
],fontstyle)

svgstrlist.append(str(svg))
svgstrlist.append(str(svg2))

svg += group([
    *(line(cvec(i,-1),cvec(i,9)) for i in range(-1,10)),
    *(line(cvec(-1,i),cvec(9,i)) for i in range(-1,10))
],styleblack.stroke_width(0.02))
svg += group([
    *(circle(0.15,*P) for P in (cvect(2,3),cvect(6,4),cvect(2,5),cvect(4,6),
                               cvect(4,7),cvect(3,6),cvect(3,7),cvect(5,7),
                               cvect(6,5),cvect(6,6),cvect(6,7),cvect(2,4),cvect(2,6)))
],styleblack.fill('red'))

svgstrlist.append(str(svg))

################################################################################

out = open(f'{DATE}.html','w')
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

for svgstr in svgstrlist:
    out.write(f'<hr />\n{svgstr}\n')

footer = f'''\
</body>
</html>
'''

out.write(footer)
out.close()
