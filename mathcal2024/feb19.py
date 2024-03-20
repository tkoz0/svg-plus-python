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
setprefix('feb19')

xmin = -10*math.pi
xmax = 10*math.pi
ymin = -1.5
ymax = 1.5
yst = 3 # y stertch

svg = svgimage((xmin,yst*ymin),(xmax,yst*ymax),800,math.ceil(yst*800*(ymax-ymin)/(xmax-xmin)))
style = attrs(stroke='black',stroke_width=0.05,fill='none')

def G(x,y) -> vec:
    return vec(x,-yst*y)

svg += line(xmin,0,xmax,0,style)
svg += line(0,yst*ymin,0,yst*ymax,style)
svg += line(G(xmin,-1),G(xmax,1),attrs=style.stroke('green'))
svg += line(-0.5,yst,0.5,yst,style.stroke_width(0.1))
svg += line(-0.5,-yst,0.5,-yst,style.stroke_width(0.1))
svg += line(xmin,yst,xmax,yst,style.stroke_dasharray([0.5]))
svg += line(xmin,-yst,xmax,-yst,style.stroke_dasharray([0.5]))

# find the intersection of 2 lines
def intersection(x1,y1,m1,x2,y2,m2) -> vec:
    A = numpy.matrix([[m1,-1],[m2,-1]])
    b = numpy.array([m1*x1-y1,m2*x2-y2])
    x = numpy.linalg.solve(A,b)
    # if new x is not between x1 and x2, probably crossed inflection point
    if not (min(x1,x2) < x[0] < max(x1,x2)):
        return vec.midpoint(vec(x1,y1),vec(x2,y2))
    return vec(x[0],x[1])

f = lambda x : math.sin(x)
fp = lambda x : math.cos(x)

x = xmin
p = pathseq().M(G(x,f(x)))
while x < xmax:
    x1,y1,m1 = x,f(x),fp(x)
    x += 0.5
    x2,y2,m2 = x,f(x),fp(x)
    v1 = intersection(x1,y1,m1,x2,y2,m2)
    p = p.Q(G(v1.x,v1.y),G(x,f(x)))

svg += path(p,style.stroke('red'))

svgstrlist.append(str(svg))

################################################################################

out = open('feb19.html','w')
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
