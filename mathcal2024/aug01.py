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

DATE = 'aug01'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(0,0),vec(100,100),300,300)
styleblack = attrs(stroke='black',stroke_width=0.5,fill='none')
fontstyle = attrs(fill='black',font_size='0.5em',font_style='italic')

A = vec(5,55)
C = vec(60,10)
B = vec(95,55)
P = vec(20,55)
M = vec.midpoint(A,B)
aCPB = vec.angler(C-P,B-P)
l = abs(C-P)*abs(B-M)/abs(B-P)
D = M + vec.polarr(l,-aCPB)
assert isclose(aCPB,vec.angler(D-M,B-M))

def makeparallelmark(X,Y):
    Z = vec.midpoint(X,Y)
    a = (Y-X).thetar()
    P1 = Z + vec.polarr(2,a+2.2)
    P2 = Z + vec.polarr(2,a-2.2)
    return polyline([P1,Z,P2])

svg += group([
    polygon([A,B,C]),
    polygon([P,D,B],attrs(fill='rgba(0,0,0,0.2)')),
    line(P,C),
    line(M,D),
    makeparallelmark(P,C),
    makeparallelmark(M,D)
] + [circle(2,X,attrs=attrs(fill='black')) for X in (A,C,B,P,M,D)]
,styleblack)

labels1: list[svgelem] = [text('APMB'[i],X+vec(-3,8),attrs=attrs()) for i,X in enumerate((A,P,M,B))]
labels2: list[svgelem] = [text('CD'[i],X+vec(2,-2)) for i,X in enumerate((C,D))]

svg += group(labels1+labels2+[
    text('AM',5,20,attrs(text_decoration='overline')),
    text('MB',25,20,attrs(text_decoration='overline')),
    text('=',18,20),
    text('Find the ratio of',15,75),
    text('the areas of PDB',15,85),
    text('and ACDP',15,95)
],fontstyle)

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
