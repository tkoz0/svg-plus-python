import sys
sys.path.insert(0,'..')
from svgpp import *
import math
from datetime import datetime
import copy

svgstrlist: list[str] = []

################################################################################

DATE = 'apr10'
setwhitespace(4)
setprefix(f'{DATE}_')

svg = svgimage(vec(0.5,0.5),vec(3.5,3.5),250,250)

styleblack = attrs(stroke='black',fill='none',stroke_width=0.03)
styleblue = styleblack.stroke('#0cf')

rtangle = 0.3
ticklen = 0.15
a = 30
u = vec.polard(1,a)
uu = u.rotated(-90)
C = vec(2,2)
v = 0.5*u + (ticklen/2)*uu
A = C+uu
A += ((3-A.x)/u.x)*u
B = C+u
B += ((3-B.x)/uu.x)*uu

svg += group([
    path(pathseq().M(3,1).h(-2).v(2).h(2)),
    line(2,1,2,3),
    line(1,2,2,2),
    rect(1,3-rtangle,1+rtangle,3),
    path(pathseq().M(C).l(u).l(uu).l(-u).l(-uu)
         .M(C+u+(1-rtangle)*uu).l(-rtangle*u).l(rtangle*uu))
],styleblack)

svg += path(pathseq().M(1,3).v(-2).h(2).L(A).L(C+uu).L(C).L(C+u).L(B).L(3,3).h(-2),
            styleblue.fill('rgba(0,0,0,0.25)'))

svg += group([
    line(1-ticklen/2,1.5,1+ticklen/2,1.5),
    line(1-ticklen/2,2.5,1+ticklen/2,2.5),
    line(1.5,1-ticklen/2,1.5,1+ticklen/2),
    line(2.5,1-ticklen/2,2.5,1+ticklen/2),
    line(1.5,3-ticklen/2,1.5,3+ticklen/2),
    line(2.5,3-ticklen/2,2.5,3+ticklen/2),
    path(pathseq().M(C+v).l(-ticklen*uu).M(C+u+v.rotated(-90)).l(ticklen*u)
         .M(C+u+uu-v).l(ticklen*uu).M(C+v.rotated(-90)).l(ticklen*u))
],styleblack)

svg += text('1',2.25,1.9,attrs(font_size='0.025em'))

svgstrlist.append(str(svg))

svg2 = copy.deepcopy(svg)
stylered = styleblue.stroke('red')
svg2 += path(pathseq().M(3,1).h(-2).v(2).h(2).M(C+uu).l(-uu).l(u),stylered)
styleorange = styleblue.stroke('orange')
svg2 += group([
    polyline([C+u,((C+u).x,2),C]),
    polyline([C+uu,((C+uu).x,2),C]),
    line(C+uu,(3,(C+uu).y)),
    line(C+u,(3,(C+u).y))
],styleorange)
svg2 += group([
    polyline([C+uu,A,(3,(C+uu).y)]),
    polyline([C+u,B,(3,(C+u).y)])
],styleorange.stroke('blue'))
thetastyle = attrs(font_size='0.01em',fill='green')
svg2 += group([
    text('&theta;',2.05,1.65),
    text('&theta;',2.3,2.15),
    text('&theta;',2.4,1.5),
    text('&triangle;A',3.05,1.3),
    text('&triangle;B',3.05,2.4)
],thetastyle)
svg2 += path(pathseq().M(C.x,C.y-rtangle).A(C+rtangle*uu,rtangle,rtangle,sweep=True),
             styleorange.stroke('green'))
svg2 += text('a',3.05,1.15,thetastyle.fill('#0cf'))
svg2 += text('b',3.05,2.8,thetastyle.fill('#0cf'))

svgstrlist.append(str(svg2))

svg3 = svgimage(vec(0,0),vec(200,100),200,100)
styleorange = styleorange.stroke_width(2)
styleblue = styleorange.stroke('blue')
svg3 += line(10,30,90,30,styleorange)
svg3 += polyline([(10,30),(90,70),(90,30)],styleblue)
svg3 += line(130,75,170,75,styleorange)
svg3 += polyline([(130,75),(170,15),(170,75)],styleblue)
svg3 += text('1&ndash;sin(&theta;)',30,25)
svg3 += text('1&ndash;cos(&theta;)',125,90)
svg3 += text('&theta;',45,45)
svg3 += text('&theta;',160,45)
svg3 += text('h&#8321;',40,65)
svg3 += text('h&#8322;',135,40)
svg3 += text('c&#8321;',95,50)
svg3 += text('c&#8322;',175,55)

svgstrlist.append(str(svg3))

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
