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

DATE = 'jun28'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(0,0),vec(8,10),280,350)
styleblack = attrs(stroke='black',stroke_width=0.06,fill='none')
fontstyle = attrs(fill='black',font_size='0.03em')

x = sqrt(5)
y = 3
s = y-x
ox,oy = 1,1
sx1 = (ox,oy+x+y),(ox+x,oy+x+x+y)
sx2 = (ox+x+s,oy+y),(ox+x+y,oy+y+x)
sy1 = (ox+x+y-x,oy),(ox+y+y,oy+y)
sy2 = (ox+x,ox+x+y),(ox+x+y,oy+x+y+y)
svg += group([
    rect(sx1[0],sx1[1]),
    rect(sx2[0],sx2[1]),
    rect(sy1[0],sy1[1]),
    rect(sy2[0],sy2[1])
],styleblack)
svg += polygon([(ox+x,oy+x+x+y),(ox+y+y,oy),(ox+x+y,oy+x+y)],styleblack.fill('rgba(0,0,0,0.2)'))

p = pathseq()
t = 0.25

def tick1(p:pathseq,v1,v2,sides=''):
    x1,x2 = v1[0],v2[0]
    y1,y2 = v1[1],v2[1]
    xm,ym = (x1+x2)/2,(y1+y2)/2
    if 'l' in sides:
        p = p.M(v1[0]-t,ym).h(2*t)
    if 'r' in sides:
        p = p.M(v2[0]-t,ym).h(2*t)
    if 't' in sides:
        p = p.M(xm,v1[1]-t).v(2*t)
    if 'b' in sides:
        p = p.M(xm,v2[1]-t).v(2*t)
    return p

def tick2(p:pathseq,v1,v2,sides=''):
    x1,x2 = v1[0],v2[0]
    y1,y2 = v1[1],v2[1]
    xm,ym = (x1+x2)/2,(y1+y2)/2
    if 'l' in sides:
        p = p.M(v1[0]-t,ym-t/2).h(2*t).M(v1[0]-t,ym+t/2).h(2*t)
    if 'r' in sides:
        p = p.M(v2[0]-t,ym-t/2).h(2*t).M(v2[0]-t,ym+t/2).h(2*t)
    if 't' in sides:
        p = p.M(xm-t/2,v1[1]-t).v(2*t).M(xm+t/2,v1[1]-t).v(2*t)
    if 'b' in sides:
        p = p.M(xm-t/2,v2[1]-t).v(2*t).M(xm+t/2,v2[1]-t).v(2*t)
    return p

def topra(p:pathseq,v):
    v = vec(v)
    return p.M(v+(2*t,0)).v(2*t).h(-2*t)

p = tick1(p,sy1[0],sy1[1],'lrt')
p = tick1(p,sy2[0],sy2[1],'rb')
p = tick2(p,sx1[0],sx1[1],'ltb')
p = tick2(p,sx2[0],sx2[1],'lr')
p = topra(p,sx1[0])
p = topra(p,sx2[0])
p = topra(p,sy1[0])
p = topra(p,sy2[0])
svg += path(p,styleblack)

svg += group([
    text('x = sum of',1,2),
    text('areas of the',1,2.5),
    text('squares',1,3),
    text('Area = 7',1,9.5)
],fontstyle)

def arrow(X,Y,s) -> tuple[line,polygon]:
    v1 = vec(Y)-vec(X)
    v2 = 0.1*v1.normalize().rotated(150)
    v3 = 0.1*v1.normalize().rotated(-150)
    return line(X,Y,attrs=s),polygon([Y,Y+v2,Y+v3],s)

a1,a2 = arrow((2.5,9),(4.5,7),styleblack)
svg += a1
svg += a2

svgstrlist.append(str(svg))

svg += group([
    polygon([sx1[1],(ox+y+x,oy+x+y+x),sx2[1]]),
    polygon([sx2[1],(ox+y+y,oy),(ox+y+y,oy+x+y)]),
    rect(sx2[1],(ox+y+y,oy+y+x+x))
],styleblack.stroke('orange').fill('rgba(255,127,0,0.2)'))

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
