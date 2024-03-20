import sys
sys.path.insert(0,'..')
from svgpp import *
import math
from datetime import datetime
import copy

svgstrlist: list[str] = []

################################################################################

setwhitespace(4)
setprefix('mar12')

svg = svgimage((0,0),(100,100),250,250)
style = attrs(stroke='black',stroke_width=1,fill='none')

u = vec(30,0)
uu = u.rotated(-60)
ud = u.rotated(60)
def s(u:vec):
    return pathseq().l(u).m(-u+0.5*u+0.1*u.rotated(-90)).l(0.2*u.rotated(90)).m(0.5*u+0.1*u.rotated(-90))

svg += path(pathseq().M(5,90).join(s(uu)).join(s(uu)).join(s(uu))
            .join(s(ud)).join(s(ud)).join(s(ud))
            .join(s(-u)).join(s(-u)).join(s(-u)).M((5,90)+u)
            .join(s(uu)).join(s(uu)).join(s(-u))
            .join(s(ud)).join(s(ud)).join(s(uu))
            .join(s(-u)).join(s(-u)).join(s(ud)),style)

svgstrlist.append(str(svg))

################################################################################

out = open('mar12.html','w')
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
