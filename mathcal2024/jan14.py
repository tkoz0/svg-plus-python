import sys
sys.path.insert(0,'..')
from svgpp import *
import math
from datetime import datetime
import copy

svgstrlist: list[str] = []

################################################################################

setwhitespace(4)
setprefix('jan14')

svg = svgimage(vec(),vec(12,12),250,250)

A = vec(4,3)
B = A + vec(7,0).rotater(-0.3)
# angle A with law of cosines
thetaA = math.acos((14*14-7*7-9*9)/(-2*7*9))
C = A + vec.polarr(9,thetaA-0.3)
D = vec.midpoint(B,C)

black = attrs(stroke='black',stroke_width=0.1,fill='none')
svg += polygon([A,B,C],black)
u = (C-B).normalize().rotated(90)
svg += line(A,D,attrs=black)
svg += comment('tick marks for side bisection')
t1 = vec.midpoint(D,C)
t2 = vec.midpoint(D,B)
svg += line(t1-0.2*u,t1+0.2*u,attrs=black)
svg += line(t2-0.2*u,t2+0.2*u,attrs=black)
svg += comment('labels')
svg += group([
    text('x',7,7.5),
    text('4',4.25,6.25),
    text('7',6,2),
    text('9',2,7)
],attrs(font_size='0.1em',font_family='sans-serif'))

svgstrlist.append(str(svg))

################################################################################

out = open('jan14.html','w')
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
