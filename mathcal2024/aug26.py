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

DATE = 'aug26'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(-2,-2),vec(2,2),250,250)
styleblack = attrs(stroke='black',stroke_width=0.05,fill='none')
fontstyle = attrs(fill='black',font_size='0.5em')

angles1 = [0,60,120,180,240,300]
angles2 = [30,90,150,210,270,330]
hvertices = [vec.polard(1,a) for a in angles1]
hexpoly = polygon(hvertices,attrs=attrs(stroke='red'))

triangles:list[svgelem] = [polygon([(0,0),hvertices[i],hvertices[(i+1)%6]]) for i in range(6)]
triangles += [polygon([vec.polard(sqrt(3),angles2[i]),hvertices[i],hvertices[(i+1)%6]]) for i in range(6)]

svg += group(triangles+[hexpoly],styleblack)

svgstrlist.append(str(svg))

svg = svgimage(vec(-2,-2),vec(2,2),250,250)

innertriangles:list[svgelem] = [polygon(hvertices[::2]),polygon(hvertices[1::2])]
svg += group(innertriangles+[hexpoly],styleblack)

svgstrlist.append(str(svg))

svg = svgimage(vec(-2,-2),vec(2,2),250,250)

outertriangles:list[svgelem] = [polygon([hvertices[i],hvertices[(i+2)%6],vec.polard(2,angles1[(i+1)%6])]) for i in range(6)]
svg += group(outertriangles+[hexpoly,polygon([hvertices[0],hvertices[2],vec.polard(2,angles1[1])],attrs(stroke='green'))],styleblack)

svgstrlist.append(str(svg))

svg = svgimage(vec(-2,-2),vec(2,2),250,250)

triangles:list[svgelem] = [polygon([hvertices[i],hvertices[(i+3)%6],vec.polard(sqrt(3),angles2[(i+1)%6])]) for i in range(6)]
svg += group(triangles+[hexpoly,polygon([hvertices[0],hvertices[3],vec.polard(sqrt(3),angles2[1])],attrs(stroke='green'))],styleblack)

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
