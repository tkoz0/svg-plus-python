import sys
sys.path.insert(0,'..')
from svgpp import *
import math
from datetime import datetime
import copy

svgstrlist: list[str] = []

################################################################################

setwhitespace(4)
setprefix('jan15')

svg = svgimage(vec(),vec(25,25),250,250)

black = attrs(stroke='black',stroke_width=0.15,fill='none')

svg += line(1,24,24,24,black)
# angles
a = 48
b = 63
c = 102
d = 72
e = 54
x = 15
# points
A = vec(3,24)
B = vec(12,24)

l1 = 9*math.sin((b+e)*math.pi/180)/math.sin(x*math.pi/180)
l2 = 9*math.sin(a*math.pi/180)/math.sin(x*math.pi/180)
lines = pathseq().M(A).l(vec.polard(l1,-a)).l(-vec.polard(l2,-b))
C = A + vec.polard(l1,-a)
l1 = 9*math.sin(2*a*math.pi/180)/math.sin(30*math.pi/180)
l2 = 9*math.sin(e*math.pi/180)/math.sin(30*math.pi/180)
lines = lines.l(vec.polard(l1,-2*b)).l(vec.polard(l2,e+30))
D = B + vec.polard(l1,-2*b)
svg += comment('the 2 triangles')
svg += path(lines,black)

svg += comment('angle arcs')
arcs = pathseq().M(A+vec(2,0)).A(A+vec.polard(2,-2*a),2,2).M(A)
for t in [a/3,2*a/3,4*a/3,5*a/3]:
    u = vec.polard(1,-t)
    arcs = arcs.m(1.5*u).l(u).m(-2.5*u)
arcs = arcs.M(B+vec(2,0)).A(B+vec.polard(2,-2*b),2,2).M(B)
for t in [b/2,3*b/2]:
    u = vec.polard(1,-t)
    arcs = arcs.m(1.5*u).l(u).m(-2.5*u)
arcs = arcs.M(C+vec.polard(6,b+e)).A(C+vec.polard(6,180-a),6,6,sweep=True)
arcs = arcs.M(D+vec.polard(4,e)).A(D+vec.polard(4,e+30),4,4,sweep=True)
svg += path(arcs,black)

textformat = attrs(font_size='0.1em',font_family='sans-serif')

svg += comment('angle labels')
svg += group([
    line(18,3,21,5),
    line(5,8,2.5,12),
    line(7,12,4,23.5)
],black)
svg += group([
    text('x&deg;',17,3),
    text('30&deg;',5,8),
    text('48&deg;',7,12)
],textformat)

svgstrlist.append(str(svg))

svg += group([
    text('a',3,21),
    text('a',5.5,23),
    text('b',14.5,23),
    text('b',11,21.5),
    text('e',10,23.5),
    text('c',6.5,19),
    text('c',8.5,19),
    text('d',7.5,17.5),
    text('d',7.5,20.5)
],textformat.fill('red'))

svgstrlist.append(str(svg))

################################################################################

out = open('jan15.html','w')
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
