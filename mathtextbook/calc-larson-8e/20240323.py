import sys
sys.path.insert(0,'../..')
from svgpp import *
import math
from datetime import datetime
import copy

svgstrlist: list[str] = []

################################################################################

svg = svgimage((-3,-2),(3,2),300,200)
style = attrs(stroke='black',stroke_width=0.02,fill='none')
axisstyle = style.stroke_width(0.05)

t = 0.1
svg += group([
    line((-3,0),(3,0)),
    line((0,-2),(0,2)),
    line((-2,-t),(-2,t)),
    line((-1,-t),(-1,t)),
    line((1,-t),(1,t)),
    line((2,-t),(2,t)),
    line((-t,-1),(t,-1)),
    line((-t,1),(t,1))
],axisstyle)

ystyle = style.stroke('red').stroke_dasharray([0.1])
svg += group([
    line((-3,1),(3,1)),
    line((-3,-1),(3,-1))
],ystyle)

lstyle = style.stroke('blue').stroke_dasharray([0.1])
svg += group([
    line((1,0),(2,-1)),
    line((-1,0),(-2,-1)),
    line((-1,0),(-2,1)),
    line((1,0),(2,1))
],lstyle)

svg += polygon([(1,0),(2,-1),(-2,-1),(-1,0),(-2,1),(2,1)],
               attrs().stroke('none').fill('lightgreen').fill_opacity(0.7))

svgstrlist.append(str(svg))

style = style.stroke_width(0.01)

r = 1
h = 0.4
svg = svgimage((-1.2*r,-1.2*r),(1.2*r,1.2*r),250,250)
a = math.asin(h/2)
svg += polygon([vec.polarr(r,aa) for aa in [a,-a,-math.pi/2,math.pi+a,math.pi-a]],style)
svg += line(vec.polarr(r,-a),vec.polarr(r,math.pi+a),attrs=style)
svg += circle(r,0,0,style)
svg += group([
    text('b',0,0.35*r),
    text('h',-0.95*r,0.1*r)
],attrs(fill='black',font_size='0.01em'))
A = vec.polarr(r,-a)
B = vec.polarr(r,math.pi+a)
C = vec(0,-1)
M1 = vec.midpoint(A,C)
M2 = vec.midpoint(B,C)
u1 = vec.polarr(r,-math.pi/4)
u2 = vec.polarr(r,-3*math.pi/4)
svg += line(M1+0.05*u1,M1-0.05*u1,attrs=style)
svg += line(M2+0.05*u2,M2-0.05*u2,attrs=style)

svgstrlist.append(str(svg))

r = 1
h = 3
s = (9*math.sqrt(2)-6)/7
t = 1-s/math.sqrt(2)
svg = svgimage((-1.2*r,-1.2*r),(1.2*r,1.2*r),250,250)
svg += circle(r,0,0,style)
svg += rect(-s/2,-s/2,s/2,s/2,attrs=style)

svgstrlist.append(str(svg))

svg = svgimage((0,0),(3.5,4.2),250,300)

C = vec(1.75,3.25)
P = vec(1.75,0.25)
R = vec(2.75,3.25)
L = vec(0.75,3.25)

svg += polygon([C,P,R],style)
svg += line(P,L,attrs=style)

Rb = C + (s/math.sqrt(2),0)
Lb = C - (s/math.sqrt(2),0)
Lb = C - (s/math.sqrt(2),0)
Rt = C + (s/math.sqrt(2),-s)
Lt = C + (-s/math.sqrt(2),-s)
svg += line(Rb,Rt,attrs=style)

E = C + (0,0.5)
F = C - (0,0.5)
svg += polygon([Rb,E,Lb,F],style)
svg += ellipse(1,0.6,C,attrs=style)

svg += group([
    text('3',1.6,1.5),
    text('s',2.3,2.6),
    text('t',2.55,3.4),
    text('s/&Sqrt;2',1.8,3.4),
    text('s',2.15,3.6)
],attrs(font_size='0.01em',fill='black'))

svgstrlist.append(str(svg))

svg = svgimage((-2,-2),(2,2),250,250)
style = style.stroke_width(0.02)
t = 0.1
svg += group([
    line(-2,0,2,0,style),
    line(0,-2,0,2,style),
    line(1,-t,1,t),
    line(-1,-t,-1,t),
    line(-t,1,t,1),
    line(-t,-1,t,-1)
],style)
h1u = lambda x : -0.5 + math.sqrt(0.25 + (x+1)**2)
h1b = lambda x : -0.5 - math.sqrt(0.25 + (x+1)**2)
d1 = lambda x : (x+1)/math.sqrt(0.25 + (x+1)**2)
h2u = lambda x : 0.5 + math.sqrt(0.25 + x**2)
h2b = lambda x : 0.5 - math.sqrt(0.25 + x**2)
d2 = lambda x : x/math.sqrt(0.25 + x**2)
svg += line(-2,1.5,1.5,-2,style.stroke_dasharray([0.1]))

# find the intersection of 2 lines
def intersection(x1,y1,m1,x2,y2,m2) -> vec:
    # A = [ [m1,-1] , [m2,-1] ], b = [ m1*x1 - y1, m2*x2 - y2]
    det = m2 - m1
    Ainv = [[-1/det,1/det],[-m2/det,m1/det]]
    b0,b1 = m1*x1-y1,m2*x2-y2
    v0 = Ainv[0][0]*b0 + Ainv[0][1]*b1
    v1 = Ainv[1][0]*b0 + Ainv[1][1]*b1
    v = vec(v0,v1)
    # if new x is not between x1 and x2, probably crossed inflection point
    if not (min(x1,x2) < v.x < max(x1,x2)):
        return vec.midpoint(vec(x1,y1),vec(x2,y2))
    return v

def G(v):
    return vec(v.x,-v.y)

x = -2.0
h1uvec = vec(x,h1u(x))
h1bvec = vec(x,h1b(x))
h2uvec = vec(x,h2u(x))
h2bvec = vec(x,h2b(x))
h1upath = pathseq().M(G(h1uvec))
h1bpath = pathseq().M(G(h1bvec))
h2upath = pathseq().M(G(h2uvec))
h2bpath = pathseq().M(G(h2bvec))
while x < 2.0:
    x += 0.5
    v1 = intersection(h1uvec.x,h1uvec.y,d1(h1uvec.x),x,h1u(x),d1(x))
    h1uvec = vec(x,h1u(x))
    h1upath = h1upath.Q(G(v1),G(h1uvec))
    v1 = intersection(h1bvec.x,h1bvec.y,-d1(h1bvec.x),x,h1b(x),-d1(x))
    h1bvec = vec(x,h1b(x))
    h1bpath = h1bpath.Q(G(v1),G(h1bvec))
    v1 = intersection(h2uvec.x,h2uvec.y,d2(h2uvec.x),x,h2u(x),d2(x))
    h2uvec = vec(x,h2u(x))
    h2upath = h2upath.Q(G(v1),G(h2uvec))
    v1 = intersection(h2bvec.x,h2bvec.y,-d2(h2bvec.x),x,h2b(x),-d2(x))
    h2bvec = vec(x,h2b(x))
    h2bpath = h2bpath.Q(G(v1),G(h2bvec))

svg += path(h1upath,style.stroke('red'))
svg += path(h1bpath,style.stroke('red'))
svg += path(h2upath,style.stroke('green'))
svg += path(h2bpath,style.stroke('green'))

svgstrlist.append(str(svg))

################################################################################

out = open('20240323.html','w')
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
