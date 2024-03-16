import sys
sys.path.insert(0,'..')
from svgpp import *
import math
from datetime import datetime
import copy

svgstrlist: list[str] = []

################################################################################

setwhitespace(4)
setprefix('mar15_')

svg = svgimage(vec(-1,-6),vec(5,1),210,245)

vertices = [vec(0,0),vec(0,-3),vec(2,-4.5),vec(4,-3),vec(4,0)]
svg += polygon(vertices,attrs(stroke='black',stroke_width=0.05,fill='lightblue'))
for v in vertices:
    svg += circle(0.15,v,attrs=attrs(fill='black'))
axes = [
    path.M(vec(-0.5,0)),
    path.L(vec(4.5,0)),
    path.l(vec.polard(0.25,135)),
    path.l(vec.polard(-0.25,135)),
    path.l(vec.polard(0.25,-135)),
    path.M(vec(0,0.5)),
    path.L(vec(0,-5.5)),
    path.l(vec.polard(0.25,45)),
    path.l(vec.polard(-0.25,45)),
    path.l(vec.polard(0.25,135))
]
axisnums = group([text('0',vec(-0.5,0.5))],attrs(font_size='0.03em'))
for i in range(1,5):
    axes += [path.M(vec(i,0.1)),path.v(-0.2)]
    axisnums += text(str(i),vec(i-0.15,0.5))
for i in range(1,6):
    axes += [path.M(vec(0.1,-i)),path.h(-0.2)]
    axisnums += text(str(i),vec(-0.5,0.15-i))
svg += path(axes,attrs(stroke='black',stroke_width=0.05,fill='none'))
svg += axisnums
svg += text('x',1.5,-1.5,attrs(font_size='0.12em'))
svg += text('(2,4.5)',1,-5,attrs(font_size='0.05em'))

svgstrlist.append(str(svg))

################################################################################

out = open('mar15.html','w')
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
