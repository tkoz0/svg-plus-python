'''
SVGPP - SVG + Python
version 1
within version 1, try to maintain backward compatibility
'''

import copy
from .vec import *

PRECISION = 3
def setprecision(p=3):
    ''' maximum number of digits after decimal place '''
    global PRECISION
    PRECISION = p

def fstr(v:float):
    '''
    custom conversion to string representation
    '''
    s = str(round(v,PRECISION))
    return s[:-2] if s.endswith('.0') else s

WHITESPACE = 4
def setwhitespace(i=4):
    ''' number of spaces for indentation, -1 to disable whitespace '''
    global WHITESPACE
    WHITESPACE = i

PREFIX = ''
def setprefix(s=''):
    ''' prefix for class/id names '''
    global PREFIX
    PREFIX = s

class linecap:
    '''
    type of ending for line strokes
    butt = line drawn by flat brush
    square = line drawn by square brush
    round = line drawn by round brush
    '''
    butt = 'butt'
    square = 'square'
    round = 'round'

class linejoin:
    '''
    type of joining between line segments
    miter = square brush
    round = round brush
    bevel = angled transition
    '''
    miter = 'miter'
    round = 'round'
    bevel = 'bevel'

class transform:
    '''
    base class for transformation types
    '''

class translate(transform):
    def __init__(self,a:pvf,b:pnf=None):
        self.v = parsevec1(a,b)
    def __str__(self):
        return f'translate({fstr(self.v.x)} {fstr(self.v.y)})'

class rotate(transform):
    def __init__(self,a:num=0.0):
        self.a = float(a)
    def __str__(self):
        return f'rotate({fstr(self.a)})'

class skewx(transform):
    def __init__(self,a:num=0.0):
        self.a = float(a)
    def __str__(self):
        return f'skewX({fstr(self.a)})'

class skewy(transform):
    def __init__(self,a:num=0.0):
        self.a = float(a)
    def __str__(self):
        return f'skewY({fstr(self.a)})'

class scale(transform):
    def __init__(self,a:pvf,b:pnf=None):
        if isinstance(a,vec):
            self.v = a
        elif isinstance(a,tuple):
            self.v = vec(a)
        elif b is None:
            self.v = vec(a,a)
        else:
            self.v = vec(a,b)
    def __str__(self):
        if self.v.x == self.v.y:
            return f'scale({fstr(self.v.x)})'
        else:
            return f'scale({fstr(self.v.x)} {fstr(self.v.y)})'

class affine(transform):
    '''
    (x,y) -> (a*x+c*y+e,b*x+d*y+f)
    '''
    def __init__(self,a:num=1.0,b:num=0.0,c:num=0.0,d:num=1.0,e:num=0.0,f:num=0.0):
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        self.d = float(d)
        self.e = float(e)
        self.f = float(f)
    def __str__(self):
        return f'matrix({fstr(self.a)} {fstr(self.b)} {fstr(self.c)} {fstr(self.d)} {fstr(self.e)} {fstr(self.f)})'

class attrs:
    '''
    attribute information for svg drawings common to many elements
    stroke = border color
    fill = inner color
    fill_opacity =
    stroke_opacity =
    stroke_linecap = see linecap class
    stroke_linejoin = see linejoin class
    stroke_dasharray = list that will be repeated for (draw, nodraw, ...)
    transforms = list of transformations to apply
    class_ = class name(s) for css styles
    id = id for css styles
    font_size = font size
    font_family = font family
    font_style = can make font italic
    font_weight = can make font bold
    text_decoration = other font properties
    '''
    def __init__(self,stroke='',stroke_width:num=0.0,fill='',fill_opacity:num=-1.0,stroke_opacity:num=-1.0,
                 stroke_linecap='',stroke_linejoin='',stroke_dasharray:list[num]=[],
                 transforms:list[transform]=[],class_='',id='',font_size='',font_family='',
                 font_style='',font_weight='',text_decoration='',style=''):
        self._stroke = stroke
        self._stroke_width = float(stroke_width)
        self._fill = fill
        self._fill_opacity = float(fill_opacity)
        self._stroke_opacity = float(stroke_opacity)
        self._stroke_linecap = stroke_linecap
        self._stroke_linejoin = stroke_linejoin
        self._stroke_dasharray = stroke_dasharray[:]
        self._transforms = transforms[:]
        self._class_ = class_
        self._id = id
        self._font_size = font_size
        self._font_family = font_family
        self._font_style = font_style
        self._font_weight = font_weight
        self._text_decoration = text_decoration
        self._style = style
    def __str__(self):
        attrs = []
        if self._id != '':
            attrs.append(f'id="{PREFIX+self._id}"')
        if self._stroke != '':
            attrs.append(f'stroke="{self._stroke}"')
        if self._stroke_width > 0:
            attrs.append(f'stroke-width="{fstr(self._stroke_width)}"')
        if self._fill != '':
            attrs.append(f'fill="{self._fill}"')
        if self._fill_opacity >= 0:
            attrs.append(f'fill-opacity="{fstr(self._fill_opacity)}"')
        if self._stroke_opacity >= 0:
            attrs.append(f'stroke-opacity="{fstr(self._stroke_opacity)}"')
        if self._stroke_linecap != '':
            attrs.append(f'stroke-linecap="{self._stroke_linecap}"')
        if self._stroke_linejoin != '':
            attrs.append(f'stroke-linejoin="{self._stroke_linejoin}"')
        if len(self._stroke_dasharray) > 0:
            attrs.append(f"stroke-dasharray=\"{' '.join(map(str,self._stroke_dasharray))}\"")
        if len(self._transforms) > 0:
            attrs.append(f"transform=\"{' '.join(map(str,self._transforms))}\"")
        if self._font_size != '':
            attrs.append(f'font-size="{self._font_size}"')
        if self._font_family != '':
            attrs.append(f'font-family="{self._font_family}"')
        if self._font_style != '':
            attrs.append(f'font-style="{self._font_style}"')
        if self._font_weight != '':
            attrs.append(f'font-weight="{self._font_weight}"')
        if self._class_ != '':
            attrs.append(f'class="{PREFIX+self._class_}"')
        if self._text_decoration != '':
            attrs.append(f'text-decoration="{self._text_decoration}"')
        if self._style != '':
            attrs.append(f'style="{self._style}"')
        return ' '.join(attrs)
    def stroke(self,s:str):
        ret = copy.deepcopy(self); ret._stroke = s; return ret
    def stroke_width(self,f:num):
        ret = copy.deepcopy(self); ret._stroke_width = f; return ret
    def fill(self,s:str):
        ret = copy.deepcopy(self); ret._fill = s; return ret
    def fill_opacity(self,f:num):
        ret = copy.deepcopy(self); ret._fill_opacity = f; return ret
    def stroke_opacity(self,f:num):
        ret = copy.deepcopy(self); ret._stroke_opacity = f; return ret
    def stroke_linecap(self,s:str):
        ret = copy.deepcopy(self); ret._stroke_linecap = s; return ret
    def stroke_linejoin(self,s:str):
        ret = copy.deepcopy(self); ret._stroke_linejoin = s; return ret
    def stroke_dasharray(self,l:list[num]):
        ret = copy.deepcopy(self); ret._stroke_dasharray = l[:]; return ret
    def transforms(self,l:list[transform]):
        ret = copy.deepcopy(self); ret._transforms = l[:]; return ret
    def class_(self,s:str):
        ret = copy.deepcopy(self); ret._class_ = s; return ret
    def id(self,s:str):
        ret = copy.deepcopy(self); ret._id = s; return ret
    def font_size(self,s:str):
        ret = copy.deepcopy(self); ret._font_size = s; return ret
    def font_family(self,s:str):
        ret = copy.deepcopy(self); ret._font_family = s; return ret
    def font_style(self,s:str):
        ret = copy.deepcopy(self); ret._font_style = s; return ret
    def font_weight(self,s:str):
        ret = copy.deepcopy(self); ret._font_weight = s; return ret
    def style(self,s:str):
        ret = copy.deepcopy(self); ret._style = s; return ret
    def text_decoration(self,s:str):
        ret = copy.deepcopy(self); ret._text_decoration = s; return ret

class svgelem:
    '''
    base class for svg elements
    __str__ must return xml tag representation
    '''

class comment(svgelem):
    '''
    xml/html comment
    '''
    def __init__(self,text='',multiline=False):
        self.text = text
        self.multiline = multiline
    def __str__(self):
        if WHITESPACE < 0:
            return ''
        if self.multiline:
            return f'<!--\n{self.text}\n-->'
        else:
            return f'<!-- {self.text} -->'

class group(svgelem):
    '''
    group svg elements to apply properties to many
    '''
    def __init__(self,elems:list[svgelem]=[],attrs=attrs()):
        self.elems = elems[:]
        self.attrs = attrs
    def __str__(self):
        attrs_ = str(self.attrs)
        inner = ''
        ws = lambda i : '' if WHITESPACE < 0 else '\n' + ' '*(i*WHITESPACE)
        ws2 = lambda i : '' if WHITESPACE < 0 else ' '*(i*WHITESPACE)
        for e in self.elems:
            inner += ws(0)
            inner += ws(0).join(ws2(1)+l for l in str(e).splitlines())
        inner += ws(0)
        return f'<g{" " if attrs_ != "" else ""}{attrs_}>{inner}</g>'
    def append(self,e:svgelem):
        self.elems.append(e)
    def __iadd__(self,e:svgelem):
        self.elems.append(e)
        return self

class rect(svgelem):
    '''
    svg rectangle
    v1 = top left corner
    v2 = bottom right corner
    rx,ry = radius for rounded corners
    '''
    def __init__(self,a:pvf,b:pvf,c:pnf=None,d:pnf=None,rx:num=0.0,ry:num=0.0,attrs=attrs()):
        t1,t2 = parsevec2(a,b,c,d)
        self.v1 = vec(min(t1.x,t2.x),min(t1.y,t2.y))
        self.v2 = vec(max(t1.x,t2.x),max(t1.y,t2.y))
        self.rx,self.ry = float(rx),float(ry)
        self.attrs = attrs
    def __str__(self):
        w = self.v2.x - self.v1.x
        h = self.v2.y - self.v1.y
        ret = f'<rect x="{fstr(self.v1.x)}" y="{fstr(self.v1.y)}" width="{fstr(w)}" height="{fstr(h)}"'
        if self.rx > 0: ret += f' rx="{fstr(self.rx)}"'
        if self.rx > 0: ret += f' ry="{fstr(self.ry)}"'
        attrs_ = str(self.attrs)
        if attrs_ != '':
            ret += ' ' + attrs_
        return ret + ' />'

class circle(svgelem):
    '''
    svg circle
    c = center
    r = radius
    '''
    def __init__(self,r:num,a:pvf,b:pnf=None,attrs=attrs()):
        self.c = parsevec1(a,b)
        self.r = float(r)
        self.attrs = attrs
    def __str__(self):
        ret = f'<circle cx="{fstr(self.c.x)}" cy="{fstr(self.c.y)}" r="{fstr(self.r)}"'
        attrs_ = str(self.attrs)
        if attrs_ != '':
            ret += ' ' + attrs_
        return ret + ' />'

class ellipse(svgelem):
    '''
    svg ellipse
    c = center
    r = radii
    '''
    def __init__(self,rx:num,ry:num,a:pvf,b:pnf=None,attrs=attrs()):
        self.c = parsevec1(a,b)
        self.rx,self.ry = float(rx),float(ry)
        self.attrs = attrs
    def __str__(self):
        ret = f'<ellipse cx="{fstr(self.c.x)}" cy="{fstr(self.c.y)}" rx="{fstr(self.rx)}" ry="{fstr(self.ry)}"'
        attrs_ = str(self.attrs)
        if attrs_ != '':
            ret += ' ' + attrs_
        return ret + ' />'

class line(svgelem):
    '''
    svg line
    v1 = first point
    v2 = second point
    '''
    def __init__(self,a:pvf,b:pvf,c:pnf=None,d:pnf=None,attrs=attrs()):
        self.v1,self.v2 = parsevec2(a,b,c,d)
        self.attrs = attrs
    def __str__(self):
        ret = f'<line x1="{fstr(self.v1.x)}" x2="{fstr(self.v2.x)}" y1="{fstr(self.v1.y)}" y2="{fstr(self.v2.y)}"'
        attrs_ = str(self.attrs)
        if attrs_ != '':
            ret += ' ' + attrs_
        return ret + ' />'

class polyline(svgelem):
    '''
    svg polyline
    points = list of points to connect
    '''
    def __init__(self,points:list[vec]|list[tvec]|list[vec|tvec]=[],attrs=attrs()):
        self.points = [vec(v) for v in points]
        self.attrs = attrs
    def __str__(self):
        ret = f"<polyline points=\"{' '.join(f'{fstr(p.x)} {fstr(p.y)}' for p in self.points)}\""
        attrs_ = str(self.attrs)
        if attrs_ != '':
            ret += ' ' + attrs_
        return ret + ' />'

class polygon(svgelem):
    '''
    svg polygon
    points = list of points to connect
    '''
    def __init__(self,points:list[vec]|list[tvec]|list[vec|tvec]=[],attrs=attrs()):
        self.points = [vec(v) for v in points]
        self.attrs = attrs
    def __str__(self):
        ret = f"<polygon points=\"{' '.join(f'{fstr(p.x)} {fstr(p.y)}' for p in self.points)}\""
        attrs_ = str(self.attrs)
        if attrs_ != '':
            ret += ' ' + attrs_
        return ret + ' />'

class text(svgelem):
    '''
    svg text
    '''
    def __init__(self,text:str,a:pvf,b:pnf=None,attrs=attrs()):
        self.text = text
        self.pos = parsevec1(a,b)
        self.attrs = attrs
    def __str__(self):
        ret = f'<text x="{fstr(self.pos.x)}" y="{fstr(self.pos.y)}"'
        attrs_ = str(self.attrs)
        if attrs_ != '':
            ret += ' ' + attrs_
        return ret + f'>{self.text}</text>'

class pathelem:
    '''
    base class for svg path instructions
    '''

class path(svgelem):
    '''
    svg path
    '''
    def __init__(self,d:list[pathelem]|pathelem=[],attrs=attrs()):
        self.d = d[:] if isinstance(d,list) else [d]
        self.attrs = attrs
    def __str__(self):
        ret = f"<path d=\"{' '.join(map(str,self.d))}\""
        attrs_ = str(self.attrs)
        if attrs_ != '':
            ret += ' ' + attrs_
        return ret + ' />'
    def append(self,e:'pathelem'):
        self.d.append(e)
    def __iadd__(self,e:'pathelem'):
        self.d.append(e)
        return self

    class M(pathelem):
        '''
        move to (absolute)
        '''
        def __init__(self,a:pvf,b:pnf=None):
            self.v = parsevec1(a,b)
        def __str__(self):
            return f'M {fstr(self.v.x)} {fstr(self.v.y)}'

    class m(pathelem):
        '''
        move to (relative)
        '''
        def __init__(self,a:pvf,b:pnf=None):
            self.v = parsevec1(a,b)
        def __str__(self):
            return f'm {fstr(self.v.x)} {fstr(self.v.y)}'

    class L(pathelem):
        '''
        line to (absolute)
        '''
        def __init__(self,a:pvf,b:pnf=None):
            self.v = parsevec1(a,b)
        def __str__(self):
            return f'L {fstr(self.v.x)} {fstr(self.v.y)}'

    class l(pathelem):
        '''
        line to (relative)
        '''
        def __init__(self,a:pvf,b:pnf=None):
            self.v = parsevec1(a,b)
        def __str__(self):
            return f'l {fstr(self.v.x)} {fstr(self.v.y)}'

    class H(pathelem):
        '''
        horizontal line to (absolute)
        '''
        def __init__(self,x:num=0.0):
            self.x = float(x)
        def __str__(self):
            return f'H {fstr(self.x)}'

    class h(pathelem):
        '''
        horizontal line to (relative)
        '''
        def __init__(self,dx:num=0.0):
            self.dx = float(dx)
        def __str__(self):
            return f'h {fstr(self.dx)}'

    class V(pathelem):
        '''
        vertical line to (absolute)
        '''
        def __init__(self,y:num=0.0):
            self.y = float(y)
        def __str__(self):
            return f'V {fstr(self.y)}'

    class v(pathelem):
        '''
        vertical line to (relative)
        '''
        def __init__(self,dy:num=0.0):
            self.dy = float(dy)
        def __str__(self):
            return f'v {fstr(self.dy)}'

    class Z(pathelem):
        '''
        close path
        '''
        def __init__(self):
            pass
        def __str__(self):
            return 'Z'

    class z(pathelem):
        '''
        close path
        '''
        def __init__(self):
            pass
        def __str__(self):
            return 'z'

    class C(pathelem):
        '''
        cubic bezier curve (absolute)
        v1 = control 1
        v2 = control 2
        v = end
        '''
        def __init__(self,a:pvf,b:pvf,c:pvf,d:pnf=None,e:pnf=None,f:pnf=None):
            self.v1,self.v2,self.v = parsevec3(a,b,c,d,e,f)
        def __str__(self):
            return f'C {fstr(self.v1.x)} {fstr(self.v1.y)} {fstr(self.v2.x)} {fstr(self.v2.y)} {fstr(self.v.x)} {fstr(self.v.y)}'

    class c(pathelem):
        '''
        cubic bezier curve (relative)
        v1 = control 1
        v2 = control 2
        v = end
        '''
        def __init__(self,a:pvf,b:pvf,c:pvf,d:pnf=None,e:pnf=None,f:pnf=None):
            self.v1,self.v2,self.v = parsevec3(a,b,c,d,e,f)
        def __str__(self):
            return f'c {fstr(self.v1.x)} {fstr(self.v1.y)} {fstr(self.v2.x)} {fstr(self.v2.y)} {fstr(self.v.x)} {fstr(self.v.y)}'

    class S(pathelem):
        '''
        cubic bezier curve with implied control (absolute)
        - implied control is reflection of previous control
          if previous command is S or C, otherwise cursor position
        v2 = control 2
        v = end
        '''
        def __init__(self,a:pvf,b:pvf,c:pnf=None,d:pnf=None):
            self.v2,self.v = parsevec2(a,b,c,d)
        def __str__(self):
            return f'S {fstr(self.v2.x)} {fstr(self.v2.y)} {fstr(self.v.x)} {fstr(self.v.y)}'

    class s(pathelem):
        '''
        cubic bezier curve with implied control (relative)
        - implied control is reflection of previous control
          if previous command is s or c, otherwise cursor position
        v2 = control 2
        v = end
        '''
        def __init__(self,a:pvf,b:pvf,c:pnf=None,d:pnf=None):
            self.v2,self.v = parsevec2(a,b,c,d)
        def __str__(self):
            return f'S {fstr(self.v2.x)} {fstr(self.v2.y)} {fstr(self.v.x)} {fstr(self.v.y)}'

    class Q(pathelem):
        '''
        quadratic bezier curve (absolute)
        v1 = control
        v = end
        '''
        def __init__(self,a:pvf,b:pvf,c:pnf=None,d:pnf=None):
            self.v1,self.v = parsevec2(a,b,c,d)
        def __str__(self):
            return f'Q {fstr(self.v1.x)} {fstr(self.v1.y)} {fstr(self.v.x)} {fstr(self.v.y)}'

    class q(pathelem):
        '''
        quadratic bezier curve (relative)
        v1 = control
        v = end
        '''
        def __init__(self,a:pvf,b:pvf,c:pnf=None,d:pnf=None):
            self.v1,self.v = parsevec2(a,b,c,d)
        def __str__(self):
            return f'q {fstr(self.v1.x)} {fstr(self.v1.y)} {fstr(self.v.x)} {fstr(self.v.y)}'

    class T(pathelem):
        '''
        quadratic bezier curve with implied control (absolute)
        - implied control is reflection of previous control
          if previous command is Q or T, otherwise cursor position
        v = end
        '''
        def __init__(self,a:pvf,b:pnf=None):
            self.v = parsevec1(a,b)
        def __str__(self):
            return f'T {fstr(self.v.x)} {fstr(self.v.y)}'

    class t(pathelem):
        '''
        quadratic bezier curve with implied control (relative)
        - implied control is reflection of previous control
          if previous command is q or t, otherwise cursor position
        v = end
        '''
        def __init__(self,a:pvf,b:pnf=None):
            self.v = parsevec1(a,b)
        def __str__(self):
            return f't {fstr(self.v.x)} {fstr(self.v.y)}'

    class A(pathelem):
        '''
        arc (absolute)
        rx,ry = radii
        rot = rotation (degrees)
        laflag = large arc flag (>180 degrees arc)
        sweep = sweep flag (use ellipse on counterclockwise side)
        v = endpoint
        '''
        def __init__(self,v:vec|tvec,rx:num,ry:num,rot:num=0.0,sweep=False,laflag=False):
            self.rx,self.ry = float(rx),float(ry)
            self.rot = float(rot)
            self.laflag = laflag
            self.sweep = sweep
            self.v = vec(v)
        def __str__(self):
            return f'A {fstr(self.rx)} {fstr(self.ry)} {fstr(self.rot)} {int(self.laflag)} {int(self.sweep)} {fstr(self.v.x)} {fstr(self.v.y)}'

    class a(pathelem):
        '''
        arc (relative)
        r = radii
        rot = rotation (degrees)
        laflag = large arc flag (>180 degrees arc)
        sweep = sweep flag (use ellipse on counterclockwise side)
        v = endpoint
        '''
        def __init__(self,v:vec|tvec,rx:num,ry:num,rot:num=0.0,sweep=False,laflag=False):
            self.rx,self.ry = float(rx),float(ry)
            self.rot = float(rot)
            self.laflag = laflag
            self.sweep = sweep
            self.v = vec(v)
        def __str__(self):
            return f'a {fstr(self.rx)} {fstr(self.ry)} {fstr(self.rot)} {int(self.laflag)} {int(self.sweep)} {fstr(self.v.x)} {fstr(self.v.y)}'

class pathseq(pathelem):
    '''
    path sequencer using . notation (function calls) to append instructions
    instances are immmutable
    '''
    def __init__(self,path_:list[pathelem]=[]):
        self.path = path_
    def __str__(self):
        return ' '.join(map(str,self.path))
    def join(self,o:pathelem):
        ''' concatenate path with more instructions '''
        if type(o) == type(self):
            return pathseq(self.path+o.path)
        else:
            return pathseq(self.path+[o])
    def M(self,a:pvf,b:pnf=None):
        ''' move to (absolute) '''
        return pathseq(self.path+[path.M(a,b)])
    def m(self,a:pvf,b:pnf=None):
        ''' move to (relative) '''
        return pathseq(self.path+[path.m(a,b)])
    def L(self,a:pvf,b:pnf=None):
        ''' line to (absolute) '''
        return pathseq(self.path+[path.L(a,b)])
    def l(self,a:pvf,b:pnf=None):
        ''' line to (relative) '''
        return pathseq(self.path+[path.l(a,b)])
    def H(self,x:num):
        ''' horizontal line to (absolute) '''
        return pathseq(self.path+[path.H(x)])
    def h(self,dx:num):
        ''' horizontal line to (relative) '''
        return pathseq(self.path+[path.h(dx)])
    def V(self,y:num):
        ''' vertical line to (absolute) '''
        return pathseq(self.path+[path.V(y)])
    def v(self,dy:num):
        ''' vertical line to (relative) '''
        return pathseq(self.path+[path.v(dy)])
    def Z(self):
        ''' close path '''
        return pathseq(self.path+[path.Z()])
    def z(self):
        ''' close path '''
        return pathseq(self.path+[path.z()])
    def C(self,a:pvf,b:pvf,c:pvf,d:pnf=None,e:pnf=None,f:pnf=None):
        ''' cubic bezier curve (absolute) '''
        return pathseq(self.path+[path.C(a,b,c,d,e,f)])
    def c(self,a:pvf,b:pvf,c:pvf,d:pnf=None,e:pnf=None,f:pnf=None):
        ''' cubic bezier curve (relative) '''
        return pathseq(self.path+[path.c(a,b,c,d,e,f)])
    def S(self,a:pvf,b:pvf,c:pnf=None,d:pnf=None):
        ''' cubic bezier curve with implied control (absolute) '''
        return pathseq(self.path+[path.S(a,b,c,d)])
    def s(self,a:pvf,b:pvf,c:pnf=None,d:pnf=None):
        ''' cubic bezier curve with implied control (relative) '''
        return pathseq(self.path+[path.s(a,b,c,d)])
    def Q(self,a:pvf,b:pvf,c:pnf=None,d:pnf=None):
        ''' quadratic bezier curve (absolute) '''
        return pathseq(self.path+[path.Q(a,b,c,d)])
    def q(self,a:pvf,b:pvf,c:pnf=None,d:pnf=None):
        ''' quadratic bezier curve (relative) '''
        return pathseq(self.path+[path.q(a,b,c,d)])
    def T(self,a:pvf,b:pnf=None):
        ''' quadratic bezier curve with implied control (absolute) '''
        return pathseq(self.path+[path.T(a,b)])
    def t(self,a:pvf,b:pnf=None):
        ''' quadratic bezier curve with implied control (relative) '''
        return pathseq(self.path+[path.t(a,b)])
    def A(self,v:vec|tvec,rx:num,ry:num,rot:num=0.0,sweep=False,laflag=False):
        ''' arc (absolute) '''
        return pathseq(self.path+[path.A(v,rx,ry,rot,sweep,laflag)])
    def a(self,v:vec|tvec,rx:num,ry:num,rot:num=0.0,sweep=False,laflag=False):
        ''' arc (relative) '''
        return pathseq(self.path+[path.a(v,rx,ry,rot,sweep,laflag)])

class cssstyle:
    ''' base class '''

class cssid(cssstyle):
    def __init__(self,id:str,s:str):
        self.id = id
        self.s = s
    def __str__(self):
        return f'#{PREFIX + self.id} {{ {self.s} }}'

class cssclass(cssstyle):
    def __init__(self,c:str,s:str):
        self.c = c
        self.s = s
    def __str__(self):
        return f'.{PREFIX + self.c} {{ {self.s} }}'

class cssstyles(svgelem):
    '''
    css styles for embedding in svg
    '''
    def __init__(self,css:list[cssstyle]=[]):
        self.css = css
    def __str__(self):
        ws = lambda i : '' if WHITESPACE < 0 else '\n' + ' '*(i*WHITESPACE)
        #ws2 = lambda i : '' if WHITESPACE < 0 else ' '*(i*WHITESPACE)
        ret = '<style>'
        for css in self.css:
            ret += ws(1) + str(css)
        return ret + '\n</style>'

class gradstop:
    def __init__(self,class_:str,offset:float,color:str,opacity:float):
        self.class_ = class_
        self.offset = offset
        self.color = color
        self.opacity = opacity

class lingrad:
    def __init__(self,id:str,stops:list[gradstop],a:pvf,b:pvf,c:pnf=None,d:pnf=None):
        self.id = id
        self.stops = stops[:]
        self.v1,self.v2 = parsevec2(a,b,c,d)

class radgrad:
    def __init__(self,id:str,stops:list[gradstop],r:num,a:pvf,b:pvf,c:pnf=None,d:pnf=None):
        self.id = id
        self.stops = stops[:]
        self.r = r
        self.c,self.f = parsevec2(a,b,c,d)

class svgimage:
    xmlns = 'http://www.w3.org/2000/svg'
    version = '1.1'
    def __init__(self,c1:vec|tvec,c2:vec|tvec,width:int,height:int):
        self.vb1 = vec(c1)
        self.vb2 = vec(c2)
        self.width = width
        self.height = height
        self.elems: list[svgelem] = []
    def append(self,e:svgelem):
        self.elems.append(e)
    def __iadd__(self,e:svgelem):
        self.elems.append(e)
        return self
    def __str__(self):
        vbw = self.vb2.x - self.vb1.x
        vbh = self.vb2.y - self.vb1.y
        ret = f'<svg version="{svgimage.version}" xmlns="{svgimage.xmlns}"'\
            f' viewBox="{fstr(self.vb1.x)} {fstr(self.vb1.y)} {fstr(vbw)} {fstr(vbh)}"'
        if self.width >= 0 and self.height >= 0:
            ret += f' width="{self.width}" height="{self.height}"'
        ret += '>'
        ws = lambda i : '' if WHITESPACE < 0 else '\n' + ' '*(i*WHITESPACE)
        ws2 = lambda i : '' if WHITESPACE < 0 else ' '*(i*WHITESPACE)
        for e in self.elems:
            ret += ws(0)
            ret += ws(0).join(ws2(1)+l for l in str(e).splitlines())
        return ret + ws(0) + '</svg>'

if __name__ == '__main__':
    pass
