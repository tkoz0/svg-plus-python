import sys
sys.path.insert(0,'..')
from svgpp import *
import math
from datetime import datetime
import copy

svgstrlist: list[str] = []

################################################################################

setwhitespace(4)
setprefix('feb16')

svg = svgimage((-0.5,-0.5),(4.5,4.5),250,250)
style = attrs(stroke='black',stroke_width=0.05,fill='none')

svg += rect(0,0,4,4,attrs=style)
svg += line(0,1,4,0,style)
A = (4,0)+vec.polarr(16/math.sqrt(17),math.pi-math.atan(1/4))
svg += line(vec(),A,attrs=style)
svg += path(pathseq().M(A/2).l((A/2).rotated(-90)).l(A/2),style)
svg += line(0,0,0,1,style.stroke('red'))
svg += text('1',-0.4,0.6,attrs(font_size='0.03em',fill='red'))
svg += line((4,0),A,attrs=style.stroke('blue'))
svg += text('16/&Sqrt;(17)',1.2,1.2,attrs(font_size='0.03em',fill='blue'))

svgstrlist.append(str(svg))

################################################################################

out = open('feb16.html','w')
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
