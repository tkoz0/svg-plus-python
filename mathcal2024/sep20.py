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

DATE = 'sep20'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(0,0),vec(10,10),200,200)
styleblack = attrs(stroke='black',stroke_width=0.1,fill='none')
fontstyle = attrs(fill='black',font_size='0.05em')

P = vec(1,5)
ds = (3,3)
ds2 = (3,-3)
Q = P+ds
R = P+ds+ds2
S = P+ds2
T = R+vec(ds2).rotated(-30)
svg += polygon([P,Q,R,S],styleblack.fill('rgba(0,0,0,0.2)'))
svg += polygon([P,P+0.1*(Q-P),P+0.1*(R-P),P+0.1*(S-P)],styleblack)
svg += polygon([P,Q,R,T,S],styleblack.stroke('#7cf'))
def mpline(A:vec,B:vec,a:attrs):
    d = (A-B).normalize().rotated(90)
    m = vec.midpoint(A,B)
    return line(m-0.25*d,m+0.25*d,attrs=a)
svg += mpline(P,Q,styleblack.stroke('#7cf'))
svg += mpline(Q,R,styleblack.stroke('#7cf'))
svg += mpline(R,T,styleblack.stroke('#7cf'))
svg += mpline(T,S,styleblack.stroke('#7cf'))
svg += mpline(S,P,styleblack.stroke('#7cf'))
svg += mpline(S,R,styleblack)
svg += text('Area = 16',2.2,5.3,fontstyle)
svg += text('Find the perimeter.',1,9,fontstyle)

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
