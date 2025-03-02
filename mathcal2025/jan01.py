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

image = svgimage((0,0),(2,2),250,250)
style_line1 = attrs(stroke='black',stroke_width=0.02,fill='none')
style_font1 = attrs(fill='black',font_size='0.01em')

gl1 = group(attrs=style_line1)

s = sqrt(3)-1
x = 1
y = 2/sqrt(3)-1
z = 1-1/sqrt(3)
A = vec(0.6,0.3)
gl1 += rect(A,A+(s,s))
gl1 += path(pathseq().M(A+(-z,0)+vec.polard(x,60)).l(vec.polard(x+y,-60))
            .l(vec.polard(x,60)).h(-z))
gl1 += line(A,A+(-z,0))
gl1 += line(A+(-z,0),A+(-z,0)+vec.polard(x,60),attrs=attrs(stroke='#7cf'))
image += text('The square has',0.2,1.5,style_font1)
image += text('side length &radic;3 - 1',0.2,1.75,style_font1)
#image += line(1.15,1.62,1.28,1.62,style_line1.stroke_width(0.01))
image += text('x',0.3,1,style_font1.fill('#7cf'))

gl2 = group(attrs=style_line1.stroke_width(0.01))

def tick(P,a):
    global gl2
    u = vec.polard(0.04,a)
    gl2 += line(P-u,P+u)

tick(A+(s-y/2,0),90)
tick(A+(s-y,0)+vec.polard(y/2,-60),30)

def angle(P,a1,a2):
    global gl2
    gl2 += path(pathseq().M(P+vec.polard(0.1,a1))
                  .A(P+vec.polard(0.1,a2),0.1,0.1))
    tick(P+vec.polard(0.1,(a1+a2)/2),(a1+a2)/2)

angle(A+(-z,0)+vec.polard(x,60),-60,-120)
angle(A+(s-y,0),-180,-240)
angle(A+(-z,0),60,0)

image += gl1
image += gl2
SVG_STRS.append(str(image))

gl1 += polygon([A,A+(-z,0),A+(-z,0)+vec.polard(x-y,60)],attrs(stroke='orange'))
gl1 += rect(A,A+(-y,y),attrs=attrs(stroke='orange'))
SVG_STRS.append(str(image))

image += text('y',0.5,1.2,style_font1)
image += text('z',0.35,0.25,style_font1)
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
