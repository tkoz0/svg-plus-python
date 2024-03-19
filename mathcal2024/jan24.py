import sys
sys.path.insert(0,'..')
from svgpp import *
import math
from datetime import datetime
import copy

svgstrlist: list[str] = []

################################################################################

setwhitespace(4)
setprefix('jan24')

svg = svgimage(vec(),vec(100,100),250,250)
style = attrs(stroke='black',stroke_width=0.5,fill='none')

A = vec(10,70)
B = vec(30,10)
C = vec(90,90)
Q = vec.midpoint(B,C)
AB = vec.midpoint(A,B)

svg += polygon([A,B,C],style)
svg += polyline([AB,Q,A],style)
svg += line(B,vec.midpoint(A,C),attrs=style)

def tick(a:vec,b:vec,n:int):
    m = vec.midpoint(a,b)
    llist = [i*3.0 for i in range(n)]
    llist = [z+abs(b-a)/4-sum(llist)/n for z in llist]
    u1 = (b-a).normalize()
    u2 = (b-a).normalize().rotated(90)
    p = pathseq()
    for z in llist:
        p = p.M(a+z*u1+2*u2).l(-4*u2)
        p = p.M(b-z*u1+2*u2).l(-4*u2)
    return p

svg += path(tick(A,B,3),style)
svg += path(tick(B,C,1),style)
svg += path(tick(A,C,2),style)

def findpr(a:vec,b:vec,v:vec):
    # find a+c*b in approx same direction as v with bisection
    c0,c1 = 0,1
    while (a+c1*b).thetad()+360 < v.thetad()+360:
        c1 *= 2
    while True:
        m = (c0+c1)/2
        if math.isclose((a+m*b).thetad()+360,v.thetad()+360):
            return m
        if (a+m*b).thetad()+360 < v.thetad()+360:
            c0 = m
        else:
            c1 = m

u = (vec.midpoint(A,C)-B).normalize()
P = B + findpr(B-AB,u,Q-AB)*u
R = B + findpr(B-A,u,Q-A)*u
svg += polygon([P,Q,R],style.fill('lightgray'))

svg += group([
    text('A',A.x-7,A.y),
    text('B',B),
    text('C',C),
    text('Q',Q),
    text('P',P.x-7,P.y-2),
    text('R',R.x-7,R.y)
],attrs(font_size='0.5em'))

svgstrlist.append(str(svg))

svg += group([
    text('D',28,35),
    text('E',40,40),
    text('F',25,55),
    text('G',45,53),
    text('H',35,70),
    text('J',55,70)
],attrs(font_size='0.5em',fill='red'))

svgstrlist.append(str(svg))

################################################################################

out = open('jan24.html','w')
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
