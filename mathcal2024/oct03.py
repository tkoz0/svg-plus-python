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

DATE = 'oct03'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(0,0),vec(7,6),280,240)
styleblack = attrs(stroke='black',stroke_width=0.05,fill='none')
fontstyle = attrs(fill='black',font_size='0.03em')

theta = asin(2/sqrt(5))

P = vec(0.5,5.5)
PP = P+(3,-3)
v = vec.polarr(sqrt(5),pi/2-theta)

def squaretick(P:vec,v:vec,t:float,s:float,num:int):
    # this should be generalizable to regular polygons
    ret = []
    Pv1 = P+v
    Pv2 = P+sqrt(2)*v.rotated(-45)
    Pv3 = P+v.rotated(-90)
    for P1,P2 in ((P,Pv1),(Pv1,Pv2),(Pv2,Pv3),(Pv3,P)):
        u = s*(P2-P1).normalize()
        uu = t*(P2-P1).normalize().rotated(90)/2
        start = vec.midpoint(P1,P2) - u*(num-1)/2
        for i in range(num):
            m = start + i*u
            ret.append(line(m+uu,m-uu))
    return ret

svg += group([
    rect(P,PP),
    rect(P,P+(0.5,-0.5)),
    polygon([PP,PP+v,PP+sqrt(2)*v.rotated(-45),PP+v.rotated(-90)]),
    line(P+(3,0),PP+v),
    polygon([P+(0,-3),PP,PP+v.rotated(-90)],attrs(fill='#7cf')),
    *squaretick(P,vec(3,0),0.25,0,1),
    *squaretick(PP,v,0.25,0.125,2)
],styleblack)

svg += group([
    text('Area',1.5,4),
    text('= 9',1.5,4.5),
    text('Area',3.75,3.75),
    text('= 3',3.75,4.25),
    text('Area',4.5,2),
    text('= 5',4.5,2.5),
    text('x',3,2)
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
