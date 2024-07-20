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

DATE = 'jul20'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(0,0),vec(12,10),300,250)
styleblack = attrs(stroke='black',stroke_width=0.1,fill='none')
fontstyle = attrs(fill='black',font_size='0.05em')

C = vec(5.5,5)

svg += path(pathseq().M(C).L(C+vec.polard(2,-180)).A(C+vec.polard(2,-200),2,2).Z(),
            attrs(stroke='none',stroke_width=0.2,fill='#7af'))
svg += path(pathseq().M(C+vec.polard(2,-180)).A(C+vec.polard(2,-200),2,2),
            attrs(stroke='blue',stroke_width=0.1,fill='none'))

svg += group([
    line(C,C+vec.polard(6,0)),
    line(C,C+vec.polard(4,-110)),
    line(C,C+vec.polard(5,-180)),
    line(C,C+vec.polard(5,-200)),
    line(C,C+vec.polard(5,-290)),
    polyline([C+vec.polard(1,-200),C+vec.polard(sqrt(2),-245),C+vec.polard(1,-290)])
],styleblack)

svg += group([
    text('(3y+20)&deg;',C+(0.5,-0.5)),
    text('(2y+10)&deg;',C+(1,1)),
    text('x&deg;',C+(-4,1))
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
