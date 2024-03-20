import sys
sys.path.insert(0,'..')
from svgpp import *
import math
from datetime import datetime
import copy

svgstrlist: list[str] = []

################################################################################

setwhitespace(4)
setprefix('feb15')

svg = svgimage((-10,-10),(10,10),250,250)
style = attrs(stroke='black',stroke_width=0.1,fill='none')

svg += circle(9,0,0,style)
svg += polygon([(-9,0),vec(),vec.polard(9,60)],style)
svg += path(pathseq().M(vec.polard(2,60)).A((-2,0),2,2,sweep=True),style)

svg += group([
    text('5&Sqrt;(3)',-6,-1),
    text('2&pi;/3',3,0),
    text('x',-4,5)
],attrs(font_size='0.1em',font_family='sans-serif'))

svg += line(3,0,-1,1,style)
svg += polygon([(-1,1),(-0.8,0.7),(-0.7,1.2)],style.fill('black'))

svgstrlist.append(str(svg))

################################################################################

out = open('feb15.html','w')
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
