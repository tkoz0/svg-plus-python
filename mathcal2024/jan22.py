import sys
sys.path.insert(0,'..')
from svgpp import *
import math
from datetime import datetime
import copy

svgstrlist: list[str] = []

################################################################################

setwhitespace(4)
setprefix('jan22')

r = 16.5
x = 22

svg = svgimage(vec(-5,-5),vec(28*r/3+5,7*r+5),328,251)
style = attrs(stroke='black',stroke_width=1,fill='none')

svg += polygon([vec(0,7*r),vec(28*r/3,0),vec(28*r/3,7*r)],style)
svg += rect(16*r/3,3*r,28*r/3,7*r,attrs=style)
svg += rect(28*r/3-8,7*r-8,28*r/3,7*r,attrs=style)

# circle centers
Crt = vec(25*r/3,2*r)
Cr1 = vec(22*r/3,4*r)
Cr2 = vec(22*r/3,6*r)
C11a = vec(16*r/3+11,5*r)
C11b = vec(28*r/3-11,5*r)
Cx = vec(16*r/3-x,7*r-x)

svg += comment('top circle (r)')
svg += circle(r,Crt,attrs=style)
svg += comment('radius x circle')
svg += circle(x,Cx,attrs=style)
svg += comment('circles horizontal in square')
svg += circle(11,C11a,attrs=style)
svg += circle(11,C11b,attrs=style)
svg += comment('circles vertical in square')
svg += circle(r,Cr1,attrs=style)
svg += circle(r,Cr2,attrs=style)

svg += group([
    line(Crt,Crt+vec.polard(r,-30)),
    line(Cr1,Cr1+vec.polard(r,-20)),
    line(Cr2,Cr2+vec.polard(r,20)),
],style.stroke('lightgreen'))
svg += group([
    text('r',Crt+vec(0,-3)),
    text('r',Cr1+vec(0,-3)),
    text('r',Cr2+vec(0,-2))
],attrs(fill='lightgreen'))
svg += group([
    line(C11a,C11a+vec.polard(11,135)),
    line(C11b,C11b+vec.polard(11,45))
],style.stroke('red'))
svg += line(Cx,Cx+vec.polard(x,-45),attrs=style.stroke('#7bf'))
svg += text('x',Cx+vec(-5,-5),attrs=attrs(fill='#7bf'))

tickh = pathseq().m(-4,0).h(8)
tickv = pathseq().m(0,-4).v(8)
svg += path(pathseq().M(16*r/3,5*r).join(tickh).M(28*r/3,5*r).join(tickh)
            .M(22*r/3,3*r).join(tickv).M(22*r/3,7*r).join(tickv),style)

A = C11a + vec(-3,-3)
B = C11b + vec(-5,0)
C = vec(4*r,2.5*r)
svg += group([
    line(C,A),
    line(C,B),
    polygon([A,vec(A.x,A.y-2),vec(A.x-2,A.y)]),
    polygon([B,vec(B.x,B.y-2),vec(B.x-2,B.y)])
],style.stroke('red').fill('red'))
svg += text('11',C+vec(-10,-5),attrs=attrs(fill='red'))

svgstrlist.append(str(svg))

svg2 = svgimage(vec(-5,-5),vec(4*r+5,4*r+5),250,250)
style = style.stroke_width(0.5)
svg2 += group([
    rect(0,0,4*r,4*r),
    circle(11,11,2*r),
    circle(11,4*r-11,2*r),
    circle(r,2*r,r),
    circle(r,2*r,3*r),
    line(vec(-2,2*r),vec(2,2*r)),
    line(vec(4*r-2,2*r),vec(4*r+2,2*r)),
    line(vec(2*r,-2),vec(2*r,2)),
    line(vec(2*r,4*r-2),vec(2*r,4*r+2))
],style)
svg2 += line(0,2*r,11,2*r,style.stroke('red'))
svg2 += line(2*r,0,2*r,r,style.stroke('lightgreen'))
svg2 += polygon([vec(2*r,2*r),vec(2*r,r),vec(11,2*r)],style.stroke('blue'))
tstyle = attrs(font_size='0.3em')
svg2 += text('11',5,2*r-3,tstyle.fill('red'))
svg2 += text('r',2*r-5,10,tstyle.fill('lightgreen'))
svg2 += group([
    text('11+r',0,0,attrs(transforms=[translate(22,22),rotate(-math.atan(r/(2*r-11))*180/math.pi)])),
    text('2r-11',0,0,attrs(transforms=[translate(25,40),rotate(-20)])),
    text('r',2*r+3,r+12)
],tstyle.fill('blue'))

svgstrlist.append(str(svg2))

svg3 = svgimage(vec(-5,-5),vec(4*r+5,3*r+5),250,196)
Z = vec(3*r,2*r) + vec.polarr(r,-2*math.atan(2))
svg3 += polyline([Z,vec(0,3*r),vec(3*r,3*r)],style.stroke('blue'))
svg3 += polyline([Z,vec(4*r,0),vec(4*r,2*r)],style.stroke('red'))
svg3 += path(pathseq().M(4*r,2*r).v(r).h(-r),style)
svg3 += circle(r,3*r,2*r,style)
svg3 += group([
    line(3*r,2*r,4*r,2*r),
    line(3*r,2*r,3*r,3*r),
    line(r*vec(3,2),Z)
],style.stroke('lightgreen'))
svg3 += text('3r',r,2*r,tstyle.fill('blue'))
svg3 += text('3r',r,3*r-2,tstyle.fill('blue'))
svg3 += text('s',3*r,r-8,tstyle.fill('red'))
svg3 += text('s',4*r-3,r,tstyle.fill('red'))
svg3 += text('r',3*r+2,2*r-2,tstyle.fill('lightgreen'))

svgstrlist.append(str(svg3))

################################################################################

out = open('jan22.html','w')
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
