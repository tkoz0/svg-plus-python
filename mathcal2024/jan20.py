import sys
sys.path.insert(0,'..')
from svgpp import *
import math
from datetime import datetime
import copy

svgstrlist: list[str] = []

################################################################################

setwhitespace(4)
setprefix('jan20')

l = 5
r = l-0.5

svg = svgimage(vec(-l,-l),vec(l,l),250,250)
style = attrs(stroke='black',stroke_width=0.1,fill='none')

svg += circle(r,0,0,style)
svg += circle(0.1,0,0,style.fill('black'))

A = vec.polard(r,140)
B = vec.polard(r,0)
C = vec.polard(r,50)
D = vec.polard(r,170)

# estimate intersection point with bisection
s1,s2 = 0,1
while True:
    s3 = (s1+s2)/2
    E = vec.convcomb(A,B,s3)
    if math.isclose(0,vec.angler(D-C,E-C)):
        break
    if (E-C).thetar() < (D-C).thetar():
        s2 = s3
    else:
        s1 = s3

svg += line(A,E,attrs=style.stroke('red'))
svg += line(B,E,attrs=style.stroke('green'))
svg += line(C,E,attrs=style.stroke('purple'))
svg += line(D,E,attrs=style)

tstyle = attrs(font_size='0.05em',font_family='sans-serif')

svg += group([
    text('2x-10',-3,1,attrs(fill='black')),
    text('3x',1.5,0.5,attrs(fill='green')),
    text('2x-20',-2.5,3.5,attrs(fill='red')),
    text('2x',0.5,3.5,attrs(fill='purple'))
],tstyle)

svgstrlist.append(str(svg))

################################################################################

out = open('jan20.html','w')
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
