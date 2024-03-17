import sys
sys.path.insert(0,'..')
from svgpp import *
import math
from datetime import datetime
import copy

svgstrlist: list[str] = []

################################################################################

setwhitespace(4)
setprefix('jan01_')

svg = svgimage(vec(-2,-2),vec(17,17),250,250)
svg.append(cssstyles([
    cssclass('text','font-size: 0.1em; font-family: sans-serif;'),
    cssclass('text2','font-size: 0.07em; font-family: sans-serif;')
]))

svg += group([
    comment('top circle'),
    rect(vec(),vec(15,15)),
    comment('quarter circles'),
    path([
        path.M(vec(0,7.5)),
        path.A(vec(7.5,15),7.5,7.5,sweep=True),
        path.A(vec(15,7.5),7.5,7.5,sweep=True)
    ]),
    comment('inside top circle'),
    circle(5,vec(7.5,5)),
    circle(0.15,vec(7.5,5),attrs=attrs(fill='black')),
    line(vec(7.5,0),vec(7.5,5)),
    comment('inside middle circle'),
    circle(1,vec(7.5,11)),
    circle(0.15,vec(7.5,11),attrs=attrs(fill='black')),
    line(vec(7.5,11),vec(7.5,11)+vec.polarr(1,math.pi-math.atan(4/7.5)))
],attrs(stroke='black',stroke_width=0.1,fill='none',id='lines'))

svg += group([
    comment('text labels'),
    text('5',vec(8,3)),
    text('x',vec(5,12))
],attrs(class_='text'))

svgstrlist.append(str(svg))

svg2 = copy.deepcopy(svg)
svg3 = copy.deepcopy(svg)

red = attrs(stroke='red',stroke_width=0.1,fill='none')

def arrow(v:vec):
    ''' relative arrow from current point in path '''
    u = v.normalize()*0.5
    u1 = u.rotated(135)
    u2 = u.rotated(-135)
    return pathseq().l(v).l(u1).m(-u1).l(u2).m(-u2-v)

svg2 += comment('triangle 1 annotation')
svg2 += polygon([vec(15,15),vec(7.5,5),vec(7.5,15)],red)
svg2 += path([
    path.M(vec(15.5,0)),
    path.h(1),
    path.M(vec(15.5,15)),
    path.h(1),
    path.M(vec(0,15.5)),
    path.v(1),
    path.M(vec(15,15.5)),
    path.v(1)
],red)
svg2 += comment('arrows')
svg2 += path(
    pathseq().M(vec(16,6.5)).join(arrow(vec(0,-6))).m(vec(0,2)).join(arrow(vec(0,6)))
    .M(vec(6.5,16)).join(arrow(vec(-6,0))).m(vec(2,0)).join(arrow(vec(6,0))),red)
angle1 = math.atan(10/7.5) * 180/math.pi
svg2 += group([
    text('2r',vec(15.5,8)),
    text('2r',vec(7,16.5)),
    text('r',vec(10,14.5)),
    text('r+5',0,0,attrs(transforms=[translate(vec(11.5,9.5)),rotate(angle1)])),
    text('2r-5',0,0,attrs(transforms=[translate(vec(7,9)),rotate(-90)]))
],attrs(class_='text2').fill('red'))

svgstrlist.append(str(svg2))

svg3 += comment('triangle 2 annotation')
svg3 += polygon([vec(15,15),vec(7.5,5),vec(7.5,11)],red)
angle2 = math.atan(4/7.5) * 180/math.pi
svg3 += group([
    text('x+5',0,0,attrs(transforms=[translate(vec(7.25,9)),rotate(-90)])),
    text('x+15/2',0,0,attrs(transforms=[translate(vec(9,13)),rotate(angle2)])),
    text('25/2',0,0,attrs(transforms=[translate(vec(12,10.5)),rotate(angle1)]))
],attrs(class_='text2').fill('red'))

svgstrlist.append(str(svg3))

################################################################################

out = open('jan01.html','w')
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
