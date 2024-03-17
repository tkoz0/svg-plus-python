import sys
sys.path.insert(0,'..')
from svgpp import *
import math
from datetime import datetime
import copy

svgstrlist: list[str] = []

################################################################################

setwhitespace(4)
setprefix('jan11_')

svg = svgimage(vec(-0.5,-5),vec(3.5,0.5),200,275)

black = attrs(stroke='black',stroke_width=0.05,fill='none')

svg += comment('axes')
svg += path(pathseq().M(0,0).h(3.25).l(vec.polard(0.1,135))
            .l(vec.polard(-0.1,135)).l(vec.polard(0.1,-135))
            .M(0,0).v(-4.75).l(vec.polard(0.1,45))
            .l(vec.polard(-0.1,45)).l(vec.polard(0.1,135)),black)
svg += comment('tick marks')
p = pathseq()
n = group([],attrs(font_size='0.02em'))
for i in range(1,4):
    p = p.join(pathseq().M(i,0.1).v(-0.2))
    n += text(str(i),i-0.1,0.4)
for i in range(1,5):
    p = p.join(pathseq().M(0.1,-i).h(-0.2))
    n += text(str(i),-0.4,0.1-i)
n += text('0',-0.3,0.3)
svg += path(p,black)
svg += n

svg += path(pathseq().M(0,-3).l(3,-4/3).v(13/3),black.stroke('red'))
svg += circle(0.07,3,-13/3,black.stroke('red').fill('red'))
svg += text('(3,13/3)',2,-4.5,attrs(font_size='0.02em'))

svgstrlist.append(str(svg))

################################################################################

out = open('jan11.html','w')
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
