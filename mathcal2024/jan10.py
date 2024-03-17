import sys
sys.path.insert(0,'..')
from svgpp import *
import math
from datetime import datetime
import copy

svgstrlist: list[str] = []

################################################################################

setwhitespace(4)
setprefix('jan10_')

svg = svgimage(vec(-0.25,-0.25),vec(1.25,1.25),250,250)

svg += cssstyles([
    cssclass('text','font-size: 0.01em; font-family: sans-serif;'),
    cssclass('textg','font-size: 0.007em; font-family: sans-serif; fill: green;'),
    cssclass('textb','font-size: 0.007em; font-family: sans-serif; fill: blue;')
])

normal = attrs(stroke='black',stroke_width=0.01,fill='none')
svg += rect(0,0,1,1,attrs=normal)
svg += rect(0,0,0.25,0.25,attrs=normal)

A = vec(0,0.75)
C = vec(1,0)
B = vec.convcomb(A,C,0.8)
D = vec(0,1)
E = vec(0.5,1)
F = vec(1,1)
svg += comment('mark the points')
for v in [A,B,C,D,E,F]:
    svg += circle(0.03,v)

svg += comment('the circle arc')
svg += path(pathseq().M(D).A(vec(0.5,0.5),0.5,0.5,sweep=True)
            .A(F,0.5,0.5,sweep=True),normal)

svg += comment('tick marks for equal side lengths')
svg += path(pathseq().M(0,0.5).h(0.025).h(-0.05)
            .M(1,0.5).h(0.025).h(-0.05)
            .M(0.5,0).v(0.025).v(-0.05),normal)

svg += comment('the line to solve for')
svg += line(A,C,attrs=normal)

svg += comment('text labels')
svg += group([
    text('8',0.45,-0.05),
    text('x',0.3,0.4)
],attrs(class_='text'))

svgstrlist.append(str(svg))

red = normal.stroke('red')
green = normal.stroke('green')
blue = normal.stroke('blue')

svg2 = copy.deepcopy(svg)
svg2 += comment('colored lines')
svg2 += path(pathseq().M(B).L(C).L(E),red)
svg2 += path(pathseq().M(B).L(E).L(F),blue)
svg2 += path(pathseq().M(B).L(A).L(E),green)
svg2 += comment('line segment labels')
svg2 += group([
    text('y',0.05,0.6),
    text('z',0.15,0.95)
],attrs(class_='textg'))
svg2 += group([
    text('4',0.35,0.8),
    text('4',0.75,0.95)
],attrs(class_='textb'))
svg2 += comment('right angles')
u = vec.polarr(0.1,-math.atan(0.75))
svg2 += path(pathseq().M(B+u).l(u.rotated(90)).l(-u)
             .M(F).m(0,-0.1).h(-0.1).v(0.1),red)

svgstrlist.append(str(svg2))

svg3 = copy.deepcopy(svg)
svg3 += comment('colored lines')
svg3 += path(pathseq().M(B).L(A).L(D).M(A).L(E),green)
svg3 += path(pathseq().M(B).L(E).L(D),blue)
svg3 += comment('line segment labels')
svg3 += group([
    text('y',0.05,0.65),
    text('y',-0.1,0.9),
    text('z',0.2,0.95)
],attrs(class_='textg'))
svg3 += comment('right angles')
u /= 2
svg3 += path(pathseq().M(B-u).l(u.rotated(90)).l(u)
             .M(D).m(0,-0.05).h(0.05).v(0.05),red)

svgstrlist.append(str(svg3))

################################################################################

out = open('jan10.html','w')
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
