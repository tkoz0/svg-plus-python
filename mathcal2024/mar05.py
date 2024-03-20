import sys
sys.path.insert(0,'..')
from svgpp import *
import math
from datetime import datetime
import copy
import numpy

svgstrlist: list[str] = []

################################################################################

setwhitespace(4)
setprefix('mar05')

svg = svgimage((0,0),(15,12),250,200)
style = attrs(stroke='black',stroke_width=0.1,fill='none')

A = vec(1,8)
B = vec(14,8)
C = vec(7.5,1.5)
svg += polygon([A,B,C],style)
r = math.sqrt(5)
F = vec(9,8)
D = vec(4,8)
E = vec(9,3)

ar = 1.5
svg += comment('angle markings')
svg += path(pathseq().M(A.x+ar,A.y).A(A+vec.polard(ar,-45),ar,ar).M(A+vec.polard(ar-0.5,-22.5)).l(vec.polard(1,-22.5))
            .M(B+vec.polard(ar,-135)).A((B.x-ar,B.y),ar,ar).M(B-vec.polard(ar-0.5,22.5)).l(-vec.polard(1,22.5))
            .M(C+(0.5,0.5)).l(-0.5,0.5).l(-0.5,-0.5),style)

a1 = math.pi/2-math.atan(2)
z = vec.polarr(r,-a1)
zp = z.rotated(-90)
svg += comment('squares')
svg += path(pathseq().M(F).l(z).l(2*zp).l(-3*z).l(-zp).l(2*z).l(-zp).m(zp).l(z).m(-z).l(zp).m(-zp-z).l(zp),style)
svg += polygon([F+zp,F+zp+z,F+zp+z+zp,F+zp+zp],style.fill('#7bf'))
svg += comment('square side markings')
svg += path(pathseq().M(F+0.5*z-0.1*zp).l(0.2*zp).m(0.8*zp).l(0.2*zp).m(0.8*zp).l(0.2*zp)
            .m(-z).l(-0.2*zp).m(-0.8*zp).l(-0.2*zp).m(-z).l(0.2*zp).m(0.8*zp).l(0.2*zp)
            .M(F+0.5*zp-0.1*z).l(0.2*z).m(0.8*z).l(0.2*z).m(zp)
            .l(-0.2*z).m(-0.8*z).l(-0.2*z).m(-0.8*z).l(-0.2*z).m(-0.8*z).l(-0.2*z),style)

svg += text('x',8.1,5,attrs(font_size='0.1em'))
svg += path(pathseq().M(A+(0.5,0.5)).l(0.5,0.5).h(11).l(0.5,-0.5).M(7.5,9).v(0.5),style)
svg += text('13',6.5,11,attrs(font_size='0.1em'))

svgstrlist.append(str(svg))

svg += line(D,E,attrs=style.stroke('green'))
svg += line(E,F,attrs=style.stroke('red'))
svg += group([
    text('A',A.x-0.75,A.y+0.5),
    text('B',B.x+0.25,B.y+0.5),
    text('C',C.x-0.25,C.y-0.25),
    text('D',D.x-0.25,D.y+0.75),
    text('E',E+(0.25,-0.25)),
    text('F',F+(-0.25,0.75))
],attrs(font_size='0.05em'))

svgstrlist.append(str(svg))

svg2 = svgimage((0,0),(8,6.4),250,200)
Z1 = vec(1,3.5)
Z2 = Z1 + vec.polarr(3*r,-a1)
Z3 = Z1 + vec.polarr(r,math.pi/2-a1)
svg2 += polygon([Z1,Z2,Z3],style)
h = 3/math.sqrt(2)
u = (Z2-Z3).normalize().rotated(90)*h
svg2 += line(Z1,Z1+u,attrs=style.stroke('red'))
svg2 += line(Z1+u,Z2,attrs=style.stroke('green'))
svg2 += group([
    text('3r',2.3,2.3),
    text('r',1,5),
    text('h',1.8,4.2),
    text('r&Sqrt;(10)',4.5,4)
],attrs(font_size='0.05em',font_family='sans-serif'))

svgstrlist.append(str(svg2))

################################################################################

out = open('mar05.html','w')
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
