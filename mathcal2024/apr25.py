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

DATE = 'apr25'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(0,0),vec(25,25),300,300)
styleblack = attrs(stroke='black',stroke_width=0.2,fill='none')

s1 = 5.
s2 = 5*sqrt(3)
s3 = 5*(1+sqrt(3))
s3edge = vec.polard(s3,-30)
s3u = vec.polard(1,-30)
tick = 0.5

P = vec(8,22)
def vtick(seq:pathseq,points:list[vec|tvec]):
    for point in points:
        seq = seq.M(point).v(tick).v(-2*tick)
    return seq
def htick(seq:pathseq,points:list[vec|tvec]):
    for point in points:
        seq = seq.M(point).h(tick).h(-2*tick)
    return seq
def dtick1(seq:pathseq,points:list[vec|tvec]):
    for point in points:
        seq = seq.M(point).l(s3u.rotated(90)*tick).l(s3u.rotated(-90)*2*tick)
    return seq
def dtick2(seq:pathseq,points:list[vec|tvec]):
    for point in points:
        seq = seq.M(point).l(s3u*tick).l(-s3u*2*tick)
    return seq

P1 = P+s3edge.rotated(-90)+s3edge/2
P2 = P+s3edge.rotated(-90)/2

svg += group([
    path(pathseq().M(P).l(s3edge).l(s3edge.rotated(-90)).l(-s3edge).Z()),
    rect(P,P+(s1,-s1),attrs=attrs(fill='rgba(0,127,255,0.25)')),
    rect(P+(s1,-s1),P+2*vec(s1,-s1)),
    rect(P+(s1,-2*s1),P+(s1,-2*s1)+(s2,-s2),attrs=attrs(fill='rgba(127,127,127,0.25)')),
    path(pathseq().M(P+s3edge.rotated(-90)+2*s3u).l(2*s3u.rotated(90)).l(-2*s3u)),
    path(pathseq().M(P+(s1+s2,-2*s1-s2)+(0,1.5)).h(-1.5).v(-1.5)),
    path(pathseq().M(P+(s1,-s1)+(0,-1.5)).h(-1.5).v(1.5)),
    path(htick(pathseq(),[
        P+(0,-s1/2),
        P+(s1,-1.5*s1),
        P+(2*s1,-1.5*s1),
        P+(s1,-2*s1-s2/2),
        P+(s1,-2*s1-s2/2+tick),
        P+(s1+s2,-2*s1-s2/2),
        P+(s1+s2,-2*s1-s2/2+tick)
    ])),
    path(vtick(pathseq(),[
        P+(s1/2,0),
        P+(s1/2,-s1),
        P+(s1+s2/2,-2*s1-s2),
        P+(s1+s2/2+tick,-2*s1-s2)
    ])),
    path(dtick1(pathseq(),[P1,P1-tick*s3u,P1-tick*2*s3u])),
    path(dtick2(pathseq(),[P2,P2+tick*s3u.rotated(90),P2+tick*2*s3u.rotated(90)]))
],styleblack)

svg += group([
    text('x',P+(2,-2),attrs=attrs(font_size='0.15em')),
    text('Area=75',P+(7,-1),attrs=attrs(font_size='0.15em')),
    path(pathseq().M(21,19).L(18,9),styleblack),
    polygon([(18.2,9),(17.8,9.2),(17.8,8.5)],styleblack.fill('black'))
])

svgstrlist.append(str(svg))

svg2 = deepcopy(svg)

svg2 += polygon([P,P+(s1,0),P+(s1,-2*s1-s2)],styleblack.stroke('red'))
svg2 += polygon([P,P+(2*s1,-2*s1),P+s3edge],styleblack.stroke('green'))
svg2 += text('t',4,8,attrs(font_size='0.1em',fill='red'))
svg2 += text('r',10,23.5,attrs(font_size='0.1em',fill='red'))

svgstrlist.append(str(svg2))

svg3 = deepcopy(svg)

a = (15+5*sqrt(3))/2
b = (5+5*sqrt(3))/2
svg3 += rect(P+(-b,0),P+s3edge+(0,-a),attrs=styleblack.stroke('orange'))
svg3 += text('b',1.5,6.5,attrs(fill='orange',font_size='0.1em'))
svg3 += text('a',5,5,attrs(fill='orange',font_size='0.1em'))
svg3 += polygon([P+(s1,-2*s1),P+(2*s1,-2*s1),P+(s1,-2*s1-s2)],styleblack.fill('rgba(255,255,0,0.5)'))
svg3 += polygon([P+s3edge.rotated(-90),P+(s1,-a),P+(s1,-s1)],styleblack.stroke('red'))

svgstrlist.append(str(svg3))

svg4 = deepcopy(svg)

svg4 += polygon([P,P+(s1,0),P+(s1,-2*s1-s2)],styleblack.stroke('green'))
svg4 += polygon([P+(s1,-2*s1-s2),P+(2*s1,-2*s1),P+(s1,-2*s1)],styleblack.stroke('red'))
svg4 += text('&alpha;',13.5,7,attrs(font_size='0.1em',fill='red'))
svg4 += text('&beta;',11.8,9,attrs(font_size='0.1em',fill='green'))

svgstrlist.append(str(svg4))

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
