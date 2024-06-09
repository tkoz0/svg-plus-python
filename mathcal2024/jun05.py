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

DATE = 'jun05'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(0,0),vec(5,5),250,250)
styleblack = attrs(stroke='black',stroke_width=0.025,fill='none')
fontstyle = attrs(fill='black',font_size='0.025em')

A = vec(4.25,4)
svg += group([
    line(0.25,4,4.75,4),
    path(pathseq().M(A).v(-1).h(-1).v(1).M(A+(0,-1)).v(-2/3).h(-2/3)
         .M(A+(-1/6,-2)).h(-1/3).v(1/3)
         .M(A+(-2.5,0)).v(-0.5).h(-0.5)),
    path(pathseq().M(A+(-1.5,0)).l(1,-2).l(-2,-1).l(-1,2).l(2,1),attrs().fill('#9cf'))
],styleblack)

svg += text('Everything is a square',0.7,4.6,fontstyle)
svg += text('x',2.2,2.6,fontstyle)

svg += line(A+(-1/6,-2),A+(-1/6,-5/3),attrs=styleblack.stroke('red'))
svg += line(A+(-2/3,-5/3),A+(-2/3,-1),attrs=styleblack.stroke('green'))
svg += line(A+(-3,-1/2),A+(-3,0),attrs=styleblack.stroke('purple'))

def arrow(X,Y,s) -> tuple[line,polygon]:
    v1 = vec(Y)-vec(X)
    v2 = 0.1*v1.normalize().rotated(150)
    v3 = 0.1*v1.normalize().rotated(-150)
    return line(X,Y,attrs=s),polygon([Y,Y+v2,Y+v3],s)

svg += text('1',3.3,3.7,fontstyle)
l,p = arrow((4.5,2.7),(3.7,2.7),styleblack.stroke('green').fill('green'))
svg += l; svg += p; svg += text('&#8532;',4.55,2.8,fontstyle.fill('green'))
l,p = arrow((4.4,1.5),(4.15,2.1),styleblack.stroke('red').fill('red'))
svg += l; svg += p; svg += text('&#8531;',4.4,1.5,fontstyle.fill('red'))
l,p = arrow((0.7,3.8),(1.2,3.8),styleblack.stroke('purple').fill('purple'))
svg += l; svg += p; svg += text('&#189;',0.35,3.9,fontstyle.fill('purple'))

svgstrlist.append(str(svg))

svg += group([
    polygon([A+(-2/3,-5/3),A+(-1,-1),A+(-2/3,-1)],styleblack.stroke('orange')),
    polygon([A+(-1/2,-2),A+(-3/2,0),A+(-1/2,0)],styleblack.stroke('orange')),
    rect(A+(-2/3,-1),A+(-2/3,-1)+(-0.1,-0.1)),
    rect(A+(-1/2,0),A+(-1/2,0)+(-0.1,-0.1))
],styleblack.stroke('orange'))

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
