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

image = svgimage((0,0),(8,9),240,280)
style_line1 = attrs(stroke='black',stroke_width=0.05,fill='none')
style_font1 = attrs(fill='black',font_size='0.05em')

s = 8/pow(27,1/4)
print(s)

C = vec(4,4)
Hs = [C+vec.polard(s,60*i) for i in range(6)] # big hexagon vertices
T1 = [Hs[0],Hs[1],C] # lower right blue triangle
Ls = [(C,Hs[i]) for i in range(2,6)] # big hexagon inner lines
T2 = [vec.midpoint(*Hs[-2:]),*(vec.midpoint(C,H) for H in Hs[-2:])] # upper blue triangle
T3p = [vec.midpoint(*Hs[2:4]),Hs[3],vec.midpoint(C,Hs[3])] # triangle around left blue
T3 = [vec.midpoint(T3p[i],T3p[(i+1)%3]) for i in range(3)] # small left blue triangle
T4 = [C,*Hs[-2:]] # one of 6 triangles in the big hexagon, with 2 tick marks

def tick1(A,B) -> line:
    u = (B-A).normalize().rotated(90)*0.2
    m = vec.midpoint(A,B)
    return line(m-u,m+u)
def tick2(A,B) -> tuple[line,line]:
    u = (B-A).normalize().rotated(90)*0.2
    m1 = vec.lerp(A,B,0.45)
    m2 = vec.lerp(A,B,0.55)
    return (line(m1-u,m1+u),line(m2-u,m2+u))
def tick3(A,B) -> tuple[line,line,line]:
    u = (B-A).normalize().rotated(90)*0.2
    m1 = vec.lerp(A,B,0.45)
    m2 = vec.lerp(A,B,0.5)
    m3 = vec.lerp(A,B,0.55)
    return (line(m1-u,m1+u),line(m2-u,m2+u),line(m3-u,m3+u))
def half1(A,B) -> tuple[vec,vec]:
    return (A,vec.midpoint(A,B))
def half2(A,B) -> tuple[vec,vec]:
    return (vec.midpoint(A,B),B)

image += group([
    polygon(Hs),
    *(line(*item) for item in Ls),
    polygon(T1,attrs(fill='#7cf')),
    polygon(T2,attrs(fill='#7cf')),
    polygon(T3p),
    polygon(T3,attrs(fill='#7cf')),
    *(tick1(T3[i],T3[(i+1)%3]) for i in range(3)),
    *(tick1(*half1(T3p[i],T3p[(i+1)%3])) for i in range(3)),
    *(tick1(*half2(T3p[i],T3p[(i+1)%3])) for i in range(3)),
    *tick2(*half1(*Hs[2:4])),
    *tick2(*half1(C,Hs[3])),
    *sum((tick2(*half1(T4[i],T4[(i+1)%3])) for i in range(3)),()),
    *sum((tick2(*half2(T4[i],T4[(i+1)%3])) for i in range(3)),()),
    *sum((tick2(T2[i],T2[(i+1)%3]) for i in range(3)),()),
    *tick3(Hs[3],Hs[4]),
    *tick3(Hs[-1],Hs[0]),
    *tick3(Hs[0],Hs[1]),
    *tick3(Hs[1],Hs[2]),
    *tick3(C,Hs[0]),
    *tick3(C,Hs[1]),
    *tick3(C,Hs[2]),
    line(6.75,1.1,7.75,1.1), # for fraction
    line(7,1.25,7.75,1.25) # for fraction
],style_line1)

image += text('8',7,1,style_font1)
image += text('&radic;27',6.8,1.65,style_font1.font_size('0.03em'))
image += text('4',6.8,1.4,style_font1.font_size('0.02em'))
image += text('Find the area',1.5,8.5,style_font1)

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
