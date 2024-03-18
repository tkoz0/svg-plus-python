# this is needed to make sure svgpp library is in the python path
import sys
sys.path.append('..')

from svgpp import *
import math
import numpy

svg = svgimage(vec(-10,-5),vec(10,5),500,250)

outline = attrs(stroke='black',stroke_width=0.05,fill='none')

# grid lines
for i in range(-9,10): # horizontal (i,-5) to (i,5)
    if i == 0: continue
    svg += line(i,-5,i,5,outline.stroke('lightgray'))
for i in range(-5,5): # vertical (-10,i) to (10,i)
    if i == 0: continue
    svg += line(vec(-10,i),vec(10,i),attrs=outline.stroke('lightgray'))

# coordinate axes
svg += line(-10,0,10,0,outline)
svg += line(vec(0,-5),vec(0,5),attrs=outline)

p = pathseq()

for i in range(-9,10): # x axis
    if i == 0: continue
    p = p.join(pathseq().M(i,0).v(0.1).v(-0.2))

for i in range(-4,5): # y axis
    if i == 0: continue
    p = p.join(pathseq().M(0,i).h(0.1).h(-0.2))

svg += path(p,outline)

# plot cos(x) starting from (-10,cos(-10))
f = lambda x : -math.cos(x)
v = vec(-10,f(-10))
p = pathseq().M(v)
x = -10
while x < 10: # increase x by 1, draw line to new point
    x += 1
    v2 = vec(x,f(x))
    p = p.L(v2)

svg += path(p,outline.stroke('red'))

# find the intersection of 2 lines
def intersection(x1,y1,m1,x2,y2,m2) -> vec:
    A = numpy.matrix([[m1,-1],[m2,-1]])
    b = numpy.array([m1*x1-y1,m2*x2-y2])
    x = numpy.linalg.solve(A,b)
    # if new x is not between x1 and x2, probably crossed inflection point
    if not (min(x1,x2) < x[0] < max(x1,x2)):
        return vec.midpoint(vec(x1,y1),vec(x2,y2))
    return vec(x[0],x[1])

fp = lambda x : math.sin(x)
v = vec(-10,f(-10)+3)
p = pathseq().M(v)
x = -10
while x < 10:
    x += 1
    v1 = intersection(v.x,v.y,fp(v.x),x,f(x)+3,fp(x))
    v = vec(x,f(x)+3)
    p = p.Q(v1,v)

svg += path(p,outline.stroke('green'))

text_style = attrs(font_size='0.05em',font_family='sans-serif')
svg += text('y=cos(x)',-5,-1,text_style.fill('red'))
svg += text('y=cos(x)-3',-5,2,text_style.fill('green'))

svg += ellipse(4,1,-5,-3,outline.stroke('blue'))
svg += circle(1.5,3,-3,outline.stroke('orange').fill('rgba(255,255,0,0.4)'))
svg += rect(-1,-1,1,1,attrs=outline.fill('#00FF00')
            .transforms([translate(7,-3),rotate(45)]))

out = open('graph1.html','w')
out.write(f'''\
<!DOCTYPE html>
<html>
<body>
<h1>svgpp example</h1>
{str(svg)}
</body>
</html>
''')
out.close()
