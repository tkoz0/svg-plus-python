import sys
sys.path.insert(0,'..')
from svgpp import *
import math
from datetime import datetime
import copy

svgstrlist: list[str] = []

################################################################################

setwhitespace(4)
setprefix('feb18')

svg = svgimage((0,10),(50,50),250,200)
style = attrs(stroke='black',stroke_width=0.5,fill='none')

C = vec(7,40)
B = vec(43,40)
c = math.acos((30*30 - 24*24 - 36*36)/(-2*24*36))
A = C + vec.polarr(24,-c)
D = vec.convcomb(A,B,0.6)
svg += line(C,B,attrs=style)
svg += polygon([A,D,C],style)
svg += line(D,B,attrs=style.stroke('#999'))
svg += text('x',35,32,attrs(font_size='0.3em',fill='#999'))
svg += group([
    text('24',8,30),
    text('36',20,45),
    text('A',A),
    text('B',B)
],attrs(font_size='0.3em'))
svg += path(pathseq().M(C.x+5,C.y).A(C+vec.polarr(5,-c),5,5)
            .M(C+vec.polarr(4,-c/4)).l(vec.polarr(2,-c/4))
            .M(C+vec.polarr(4,-3*c/4)).l(vec.polarr(2,-3*c/4)),style)
svg += text('AB',30,20,attrs(font_size='0.3em',style='text-decoration:overline;'))
svg += text('=30',37,20,attrs(font_size='0.3em'))

svgstrlist.append(str(svg))

svg += group([
    text('y',23,27),
    text('z',20,36),
    text('C',3,43),
    text('D',D)
],attrs(font_size='0.3em',fill='red'))

svgstrlist.append(str(svg))

################################################################################

out = open('feb18.html','w')
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
