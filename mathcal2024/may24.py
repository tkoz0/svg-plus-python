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

DATE = 'may24'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(-20,-30),vec(20,20),200,300)
styleblack = attrs(stroke='black',stroke_width=0.2,fill='none')
fontstyle = attrs(fill='black',font_size='0.33em')

c1 = (0,0)
c2 = (10,-24)
svg += circle(18,c1,attrs=styleblack)
svg += circle(8,c2,attrs=styleblack)
svg += circle(0.25,c1,attrs=styleblack.fill('black'))
svg += circle(0.25,c2,attrs=styleblack.fill('black'))
svg += line(c1,c1+vec.polard(18,60),attrs=styleblack)
svg += line(c2,c2+vec.polard(8,-60),attrs=styleblack)
svg += line(18,0,18,-24,styleblack.stroke('#7cf'))
svg += text('8',8,-26,fontstyle)
svg += text('18',-3,10,fontstyle)
svg += text('x',15,-12,fontstyle.fill('#7cf'))

svg2 = deepcopy(svg)
svg2 += path(pathseq().M(18,-24).L(c2).L(c1).L(18,0),styleblack.stroke('red'))
svg2 += line(10,0,10,-24,styleblack.stroke('#7cf'))
svg2 += text('26',-1,-10,fontstyle.fill('red'))
svg2 += text('10',4,5,fontstyle.fill('red'))

svgstrlist.append(str(svg))
svgstrlist.append(str(svg2))

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
