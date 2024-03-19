import sys
sys.path.insert(0,'..')
from svgpp import *
import math
from datetime import datetime
import copy

svgstrlist: list[str] = []

################################################################################

setwhitespace(4)
setprefix('jan18')

s = 5.85
t = 0.2

svg = svgimage(vec(-0.5,-1.5),vec(s+0.5,s+1),205,250)

black = attrs(stroke='black',stroke_width=0.05,fill='none')

svg += rect(0,0,s,s,attrs=black)
E = vec(s/2,s)
h = math.sqrt(3*3 - (s/2)**2)
B = vec(0,s)
A = vec(0,s-h)
D = vec(s/2+2*h,s)
C = vec(s/2+2*h,0)
F = C + A - E # last corner of rectangle
ar = math.atan(h/(s/2))
ad = ar*180/math.pi

svg += comment('shaded rectangle')
svg += path(pathseq().M(A).L(F).L(C).L(E).Z(),black.fill('rgba(0,0,255,0.3)'))
svg += comment('outer square tick marks')
svg += path(pathseq().M(s/4,s).v(t).v(-2*t).M(3*s/4,s).v(t).v(-2*t)
            .M(s,s/2).l(vec.polard(t,45)).l(vec.polard(-t,45)).l(vec.polard(t,135))
            .M(s/2,0).l(vec.polard(t,-45)).l(vec.polard(-t,-45)).l(vec.polard(t,45))
            .M(0,s/2).l(vec.polard(t,-45)).l(vec.polard(-t,-45)).l(vec.polard(t,-135)),black)

tick2 = pathseq().m(vec.polard(0.8,ad)+vec.polard(t,ad+90)).l(vec.polard(2*t,ad-90)) \
    .m(vec.polard(t,ad+90)+vec.polard(0.2,ad)+vec.polard(t,ad+90)).l(vec.polard(2*t,ad-90))
tick3 = pathseq().m(vec.polard(2.8,ad-90)+vec.polard(t,ad)).l(vec.polard(-2*t,ad)) \
    .m(vec.polard(t,ad)+vec.polard(0.2,ad-90)+vec.polard(t,ad)).l(vec.polard(-2*t,ad)) \
    .m(vec.polard(t,ad)+vec.polard(0.2,ad-90)+vec.polard(t,ad)).l(vec.polard(-2*t,ad))
svg += comment('shaded rectangle tick marks')
svg += path(pathseq().M(A).join(tick2).M(F).join(tick2).M(A).join(tick3).M(E).join(tick3),black)

svg += comment('right angles')
svg += path(pathseq().M(A+vec.polard(2*t,ad)).l(vec.polard(2*t,ad-90)).l(vec.polard(2*t,ad-180))
            .M(s,s-2*t).h(-2*t).v(2*t),black)

svg += comment('text labels')
svg += group([
    text('x',s/2-1,s/2),
    text('3',s/2,-0.5)
],attrs(font_size='0.07em'))

svgstrlist.append(str(svg))

svg += comment('triangles and right angles')
svg += polygon([A,B,E],black.stroke('lightgreen'))
svg += polygon([C,D,E],black.stroke('red'))
svg += path(pathseq().M(0,s-1.5*t).h(1.5*t).v(1.5*t),black.stroke('lightgreen'))
svg += path(pathseq().M(D+vec(-1.5*t,0)).v(-1.5*t).h(1.5*t),black.stroke('red'))

svg += comment('labeled points')
svg += group([
    text('A',A+vec(-2*t,0)),
    text('B',B+vec(-2*t,2*t)),
    text('C',C+vec(-t,-t)),
    text('D',D+vec(-t,2*t)),
    text('E',E+vec(-t,2*t))
],attrs(font_size='0.03em'))

svgstrlist.append(str(svg))

################################################################################

out = open('jan18.html','w')
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
