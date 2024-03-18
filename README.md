# svg-plus-python

## introduction

This library was created to allow combining code generating drawing with SVG.
SVG itself does not support embedding arbitrary code inside it, unless maybe
something could work with using JavaScript to generate the drawing when the web
page loads. The goal of this library is to provide a convenient and generic
interface for creating SVG drawings while being able to include code generation
along the SVG details. It is probably reasonably convenient for what it does
given the limitations of Python syntax and being quite generic.

Use of this library still requires a decent understanding of the SVG format.
There is plenty of documentation for it online such as the Mozilla developer
documentation. Below are some examples of using the library, which assume a
working knowledge of the SVG format basics. Afterward is some documentation.

Currently this library sort of assumes the user knows what they are doing.
There is room for improvement. If more people than myself are interested in
using it, there will probably be significant improvements made over time.

## example

<svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="-10 -5 20 10" width="500" height="250" style="background:white;">
    <line x1="-9" x2="-9" y1="-5" y2="5" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="-8" x2="-8" y1="-5" y2="5" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="-7" x2="-7" y1="-5" y2="5" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="-6" x2="-6" y1="-5" y2="5" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="-5" x2="-5" y1="-5" y2="5" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="-4" x2="-4" y1="-5" y2="5" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="-3" x2="-3" y1="-5" y2="5" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="-2" x2="-2" y1="-5" y2="5" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="-1" x2="-1" y1="-5" y2="5" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="1" x2="1" y1="-5" y2="5" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="2" x2="2" y1="-5" y2="5" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="3" x2="3" y1="-5" y2="5" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="4" x2="4" y1="-5" y2="5" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="5" x2="5" y1="-5" y2="5" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="6" x2="6" y1="-5" y2="5" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="7" x2="7" y1="-5" y2="5" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="8" x2="8" y1="-5" y2="5" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="9" x2="9" y1="-5" y2="5" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="-10" x2="10" y1="-5" y2="-5" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="-10" x2="10" y1="-4" y2="-4" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="-10" x2="10" y1="-3" y2="-3" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="-10" x2="10" y1="-2" y2="-2" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="-10" x2="10" y1="-1" y2="-1" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="-10" x2="10" y1="1" y2="1" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="-10" x2="10" y1="2" y2="2" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="-10" x2="10" y1="3" y2="3" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="-10" x2="10" y1="4" y2="4" stroke="lightgray" stroke-width="0.05" fill="none" />
    <line x1="-10" x2="10" y1="0" y2="0" stroke="black" stroke-width="0.05" fill="none" />
    <line x1="0" x2="0" y1="-5" y2="5" stroke="black" stroke-width="0.05" fill="none" />
    <path d="M -9 0 v 0.1 v -0.2 M -8 0 v 0.1 v -0.2 M -7 0 v 0.1 v -0.2 M -6 0 v 0.1 v -0.2 M -5 0 v 0.1 v -0.2 M -4 0 v 0.1 v -0.2 M -3 0 v 0.1 v -0.2 M -2 0 v 0.1 v -0.2 M -1 0 v 0.1 v -0.2 M 1 0 v 0.1 v -0.2 M 2 0 v 0.1 v -0.2 M 3 0 v 0.1 v -0.2 M 4 0 v 0.1 v -0.2 M 5 0 v 0.1 v -0.2 M 6 0 v 0.1 v -0.2 M 7 0 v 0.1 v -0.2 M 8 0 v 0.1 v -0.2 M 9 0 v 0.1 v -0.2 M 0 -4 h 0.1 h -0.2 M 0 -3 h 0.1 h -0.2 M 0 -2 h 0.1 h -0.2 M 0 -1 h 0.1 h -0.2 M 0 1 h 0.1 h -0.2 M 0 2 h 0.1 h -0.2 M 0 3 h 0.1 h -0.2 M 0 4 h 0.1 h -0.2" stroke="black" stroke-width="0.05" fill="none" />
    <path d="M -10 0.839 L -9 0.911 L -8 0.146 L -7 -0.754 L -6 -0.96 L -5 -0.284 L -4 0.654 L -3 0.99 L -2 0.416 L -1 -0.54 L 0 -1 L 1 -0.54 L 2 0.416 L 3 0.99 L 4 0.654 L 5 -0.284 L 6 -0.96 L 7 -0.754 L 8 0.146 L 9 0.911 L 10 0.839" stroke="red" stroke-width="0.05" fill="none" />
    <path d="M -10 3.839 Q -9.494 4.115 -9 3.911 Q -8.612 3.751 -8 3.146 Q -7.271 2.424 -7 2.246 Q -6.481 1.905 -6 2.04 Q -5.584 2.156 -5 2.716 Q -4.107 3.573 -4 3.654 Q -3.468 4.056 -3 3.99 Q -2.563 3.928 -2 3.416 Q -1.5 2.938 -1 2.46 Q -0.454 2 0 2 Q 0.454 2 1 2.46 Q 1.5 2.938 2 3.416 Q 2.563 3.928 3 3.99 Q 3.468 4.056 4 3.654 Q 4.107 3.573 5 2.716 Q 5.584 2.156 6 2.04 Q 6.481 1.905 7 2.246 Q 7.271 2.424 8 3.146 Q 8.612 3.751 9 3.911 Q 9.494 4.115 10 3.839" stroke="green" stroke-width="0.05" fill="none" />
    <text x="-5" y="-1" fill="red" font-size="0.05em" font-family="sans-serif">y=cos(x)</text>
    <text x="-5" y="2" fill="green" font-size="0.05em" font-family="sans-serif">y=cos(x)-3</text>
    <ellipse cx="-5" cy="-3" rx="4" ry="1" stroke="blue" stroke-width="0.05" fill="none" />
    <circle cx="3" cy="-3" r="1.5" stroke="orange" stroke-width="0.05" fill="rgba(255,255,0,0.4)" />
    <rect x="-1" y="-1" width="2" height="2" stroke="black" stroke-width="0.05" fill="#00FF00" transform="translate(7 -3) rotate(45)" />
</svg>

As an example, we will make the SVG shown above, which has a plot of a few
functions and some shapes. First create an `svgimage` object with
$-10\leq x\leq10$ and $-5\leq y\leq5$, which will be the bounds for our graph.
To match the size 1:1, we will use image dimensions 500x250.

```py
from svgpp import *
import math
import numpy

svg = svgimage(vec(-10,-5),vec(10,5),500,250)
```

Next, define an attribute which represents the style for lines and curves. It
will have a stroke color of black, which can be adjusted later.

```py
outline = attrs(stroke='black',stroke_width=0.05,fill='none')
```

Now let's draw the coordinate grid. First we will add some grid lines in
light gray color, then the axes in black. Here, the example shows how the `line`
class can take the coordinates as 4 numbers or 2 vectors.

```py
# grid lines
for i in range(-9,10): # horizontal (i,-5) to (i,5)
    if i == 0: continue
    svg += line(i,-5,i,5,outline.stroke('lightgray'))
for i in range(-5,5): # vertical (-10,i) to (10,i)
    if i == 0: continue
    svg += line(vec(-10,i),vec(10,i),attrs=outline.stroke('lightgray'))

# coordinate axes
svg += line(-10,0,10,0,outline)
svg += line(vec(0,-5),vec(0,5),attrs=outline)
```

Next, let's make tick marks on the axes to show steps of size 1. Each tick mark
will be a small line of length 0.2. This time we will use a SVG path. Start with
the `pathseq` class which allows joining multiple SVG path drawing instructions
together. Then for each tick mark, move and draw the small line. Finally, add
a `path` to the SVG image made from the `pathseq` object and using our
attributes for black lines.

```py
p = pathseq()

for i in range(-9,10): # x axis
    if i == 0: continue
    p = p.join(pathseq().M(i,0).v(0.1).v(-0.2))

for i in range(-4,5): # y axis
    if i == 0: continue
    p = p.join(pathseq().M(0,i).h(0.1).h(-0.2))

svg += path(p,outline)
```

Now we will do something a little more complicated. We will plot $y=\cos(x)$
with a step size of 1 and linear interpolation. Then shifted 3 units down, we
will plot $y=\cos(x)-3$ with quadratic interpolation by using quadratic bezier
curves. Since SVG graphics inverts the direction of the $y$ axis from the usual
math standard, we will be plotting the negative of these functions for the SVG
coordinates. For the quadratic interpolation, a helper function `interpolate`
is created which is used to solve for the intersection of 2 lines tangent to the
curve.

```py
# plot cos(x) starting from (-10,cos(-10))
f = lambda x : -math.cos(x)
v = vec(-10,f(-10))
p = pathseq().M(v)
x = -10
while x < 10: # increase x by 1, draw line to new point
    x += 1
    v2 = vec(x,f(x))
    p = p.L(v2)

svg += path(p,outline.stroke('red'))

# find the intersection of 2 lines
def interpolate(x1,y1,m1,x2,y2,m2) -> vec:
    A = numpy.matrix([[m1,-1],[m2,-1]])
    b = numpy.array([m1*x1-y1,m2*x2-y2])
    x = numpy.linalg.solve(A,b)
    # if new x is not between x1 and x2, probably crossed inflection point
    if not (min(x1,x2) < x[0] < max(x1,x2)):
        return vec.midpoint(vec(x1,y1),vec(x2,y2))
    return vec(x[0],x[1])

fp = lambda x : math.sin(x)
v = vec(-10,f(-10)+3)
p = pathseq().M(v)
x = -10
while x < 10:
    x += 1
    v1 = interpolate(v.x,v.y,fp(v.x),x,f(x)+3,fp(x))
    v = vec(x,f(x)+3)
    p = p.Q(v1,v)

svg += path(p,outline.stroke('green'))
```

Next, let's add some text to label the 2 plotted functions.

```py
text_style = attrs(font_size='0.05em',font_family='sans-serif')
svg += text('y=cos(x)',-5,-1,text_style.fill('red'))
svg += text('y=cos(x)-3',-5,2,text_style.fill('green'))
```

Finally, we will add a few shapes in the top part of the graph. Some
transformations have been used for the rectangle.

```py
svg += ellipse(4,1,-5,-3,outline.stroke('blue'))
svg += circle(1.5,3,-3,outline.stroke('orange').fill('rgba(255,255,0,0.4)'))
svg += rect(-1,-1,1,1,attrs=outline.fill('#00FF00')
            .transforms([translate(7,-3),rotate(45)]))
```

Now we convert the SVG to a string and write a basic web page to a file.

```py
out = open('graph1.html','w')
out.write(f'''\
<!DOCTYPE html>
<html>
<body>
<h1>svgpp example</h1>
{str(svg)}
</body>
</html>
''')
out.close()
```

## functions for global settings

`setprecision(p)` sets the maximum number of digits after the decimal point to
use in numbers written. Default is 3

`setwhitespace(i)` sets the number of spaces for indentation, use -1 to disable.
Default is 4

`setprefix(s)` set a prefix string to use for CSS classes and IDs. Default is
empty string. This feature was made to help ensure unique names for things
because including multiple SVGs in a page can cause issues if names are
repeated. For example, on a math calendar page of mine, each SVG gets a prefix
of the date of the problem.

## vector class

This is a vector class. There is nothing very special about it. It is
initialized with `x` and `y` coordinates of type `float` and the usual vector
operations can be done with operators. Absolute value is the magnitude. Note
that angles go clockwise because the `y` axis points down in SVG, unlike the
usual coordinate plane.

There are the following member functions:

```
rad() - radius, or magnitude
radsq() - radius squared, or magnitude squared
thetar() - angle in radians
thetad() - angle in degrees
rotater(a) - vector result from rotation by a radians
rotated(a) - vector result from rotation by a degrees
normalize() - the unit vector with the same direction
```

And the following static functions:

```
rect(x,y) - vector from rectangular coordinates (same as constructor)
polarr(r,t) - vector from polar coordinates using radians
polard(r,t) - vector from polar coordinates using degrees
convcomb(u,v,c) - convex combination: c*u + (1-c)*v
midpoint(u,v) - average of 2 vectors, same as convcomb with c=0.5
proj(a,b) - projection of a onto b
angler(a,b) - angle between 2 vectors (in radians)
angled(a,b) - angle between 2 vectors (in degrees)
```

## constants

The classes `linecap` and `linejoin` contain constants for handling the
endpoints and connections between lines.

## transformations

SVG has transformations that can be applied to objects. All angles used are in
degrees. A list of these objects is passed to the `transforms` parameter in the
`attrs` class.

```
translate(x,y) or translate(v)
- translate(v) expects a vector
- translate(x,y) expects 2 numbers
rotate(angle)
skewx(angle)
skewy(angle)
scale(a) or scale(a,b)
- in scale(a), if a is vector, it specifies scaling in each dimension
- in scale(a), if a is number, use vec(a,a) for scaling
- scale(a,b) needs 2 numbers for scaling in each dimension
affine(a,b,c,d,e,f)
- expects 6 numbers, represents (x,y) -> (a*x+c*y+e,b*x+d*y+f)
```

## attributes

The class called `attrs` specifies some common attributes for XML tags that SVG
objects use for various styling information. They can be instantiated as
`attrs(attr1=value1,attr2=value2,...)` using Python keyword arguments.
Additionally, the chained member function calls add/modify paremeters by making
a copy (since the class is immutable). This allows creating a common object and
making changes to a small number of attributes where little differences are
needed. The expression `object.attr1(value1).attr2(value2)` would update
attribute 1 with value 1 and attribute 2 with value 2.

The attributes included are:

```
stroke - border color
stroke_width - border width
fill_opacity
stroke_opacity
stroke_linecap
stroke_linejoin
stroke_dasharray
transforms
class_ - css class name
id - css id name
font_size
font_family
```

## svg elements

### comment

`comment(text,multiline=False)`

Just an HTML comment `<!-- like this -->`. The multiline flag specifies whether
it should be formatted a little differently for multiple lines. This is only so
comments can be embedded in the SVG code, which I did when writing the SVG code
fully manually.

### group

`group(elems=[],attrs=attrs())`

Create an SVG group. This allows multiple SVG elements to share common
attributes. Includes `.append` member and `+=` operator to insert another
element.

### rect

`rect(<vec1,vec2 or x1,y1,x2,y2>,rx=0,ry=0,attrs=attrs())`

SVG rectangle. Specify coordinates as 2 vectors or 4 numbers. The `rx` and `ry`
describe the radius for rounded corners.

### circle

`circle(r,<vec or x,y>,attrs=attrs())`

SVG circle. `r` is the radius. The center is a vector or 2 numbers.

### ellipse

`ellipse(rx,ry,<vec or x,y>,attrs=attrs())`

SVG ellipse. `rx` and `ry` are the radii. The center is a vector or 2 numbers.

### line

`line(<v1,v2 or x1,y1,x2,y2>,attrs=attrs())`

SVG line. Specify endpoints as 2 vectors or 4 numbers.

### polyline

`polyline(points=[],attrs=attrs())`

SVG polyline. This is multiple connected line segments. The points are specified
as a list of vectors.

### polygon

`polygon(points=[],attrs=attrs())`

SVG polygon. The only difference from polyline is that a polygon automatically
connects the last point back to the first.

### text

`text(string,<vec or x,y>,attrs=attrs())`

SVG text. This takes a string for the text to display and a coordinate.

### path

`path(<list of pathelem or a single pathelem>,attrs=attrs())`

SVG path. This is a more generic element that draws with various instructions.
It supports moving to points, various lines, quadratic and cubic bezier curves,
and circular or elliptic arcs. It also includes a `.append` member and `+=`
operator to add more drawing instructions to the end of the path.

Within the path class are individual classes for the various instructions used
in path drawing. These are all named as single letters which match those in the
SVG documentation. Using this interface is almost the same as writing the SVG
path data, so you should be familiar with the documentation for SVG paths.

```
path.M(<v or x,y>) - move to (absolute)
path.m(<v or dx,dy>) - move to (relative)
path.L(<v or x,y>) - line to (absolute)
path.l(<v or dx,dy>) - line to (relative)
path.H(x) - horizontal line to (absolute)
path.h(dx) - horizontal line to (relative)
path.V(y) - vertical line to (absolute)
path.v(dy) - vertical line to (relative)
path.Z() or path.z() - close path
path.C(<v1,v2,v or x1,y1,x2,y2,x,y>)
- cubic bezier curve (absolute)
path.c(<v1,v2,v or dx1,dy1,dx2,dy2,dx,dy>)
- cubic bezier curve (relative)
path.S(<v2,v or x2,y2,x,y>)
- cubic bezier curve with implied control (absolute)
path.s(<v2,v or dx2,dy2,dx,dy>)
- cubic bezier curve with implied control (relative)
path.Q(<v1,v or x1,y1,x,y>)
- quadratic bezier curve (absolute)
path.q(<v1,v or dx1,dy1,dx,dy>)
- quadratic bezier curve (relative)
path.T(<v or x,y>)
- quadratic bezier curve with implied control (absolute)
path.t(<v or dx,dy>)
- quadratic bezier curve with implied control (relative)
path.A(v,rx,ry,rot=0.0,sweep=False,laflag=False)
- arc to v with radii rx,ry, rot in degrees, and 2 flags (absolute)
path.a(v,rx,ry,rot=0.0,sweep=False,laflag=False)
- arc to v with radii rx,ry, rot in degrees, and 2 flags (relative)
```

### pathseq

Path sequencer that uses chained . notation to construct paths. For example,
`pathseq().M(0,0).h(1).L(1,1).Z()`. It also has a `.join(pathelem)` function to
concatenate path data to it (makes a new object since pathseq is immutable).

### cssstyles

`cssstyles(<list of cssstyle objects>)`

This class specifies a list of CSS styles. The 2 types that can be in the list
are `cssid(id,s)` which is `#id { s }` in CSS code, and `cssclass(c,s)` which is
`.c { s }` in CSS code.

## svgimage

`svgimage(c1,c2,width,height)`

The SVG image class that stores all the objects representing an SVG image. The
vectors `c1` and `c2` specify the upper left and lower right corners of the
viewing box. The width and height are in pixels for the image size. This class
supports `.append` and `+=` for adding SVG elements. The desired SVG output is
created by converting one of these objects to a string.
