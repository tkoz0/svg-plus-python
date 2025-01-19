import math

# number (float or int)
num = float|int

# tuple vector
tvec = tuple[num,num]

class vec:
    ''' immutable 2d vector '''
    def __init__(self,x:'num|tvec|vec'=0.0,y:num=0.0):
        if isinstance(x,num):
            self.x = float(x)
            self.y = float(y)
        elif isinstance(x,vec):
            self.x = x.x
            self.y = x.y
        else:
            self.x,self.y = float(x[0]),float(x[1])
    def __repr__(self) -> str:
        return f'vec({repr(self.x)},{repr(self.y)})'
    def __str__(self) -> str:
        return f'({self.x},{self.y})'
    def __eq__(self,o) -> bool:
        return type(o) == type(self) and o.x == self.x and o.y == self.y
    def __ne__(self,o) -> bool:
        return not (self == o)
    def __hash__(self) -> int:
        return hash((self.x,self.y))
    def __bool__(self) -> bool:
        return abs(self.x) > 0.0 or abs(self.y) > 0.0
    def __add__(self,o:'vec|tvec') -> 'vec':
        if isinstance(o,tuple):
            return vec(self.x+o[0],self.y+o[1])
        else:
            return vec(self.x+o.x,self.y+o.y)
    def __sub__(self,o:'vec|tvec') -> 'vec':
        if isinstance(o,tuple):
            return vec(self.x-o[0],self.y-o[1])
        else:
            return vec(self.x-o.x,self.y-o.y)
    def __radd__(self,o:'vec|tvec') -> 'vec':
        return self + o
    def __rsub__(self,o:'vec|tvec') -> 'vec':
        return -(self - o)
    def __mul__(self,o:num) -> 'vec':
        return vec(self.x*o,self.y*o)
    def __rmul__(self,o:num) -> 'vec':
        return self * o
    def __truediv__(self,o:num) -> 'vec':
        return vec(self.x/o,self.y/o)
    def __matmul__(self,o:'vec|tvec') -> float:
        if isinstance(o,tuple):
            return self.x*o[0] + self.y*o[1]
        else:
            return self.x*o.x + self.y*o.y
    def __rmatmul__(self,o:'vec|tvec') -> float:
        return self @ o
    def __neg__(self) -> 'vec':
        return vec(-self.x,-self.y)
    def __pos__(self) -> 'vec':
        return self
    def __abs__(self) -> float:
        return math.hypot(self.x,self.y)
    def rad(self) -> float:
        return abs(self)
    def radsq(self) -> float:
        return self.x*self.x + self.y*self.y
    def thetar(self) -> float:
        return math.atan2(self.y,self.x)
    def thetad(self) -> float:
        return self.thetar()*180/math.pi
    def rotater(self,a=0.0) -> 'vec':
        return vec.polarr(abs(self),self.thetar()+a)
    def rotated(self,a=0.0) -> 'vec':
        return vec.polard(abs(self),self.thetad()+a)
    def normalize(self) -> 'vec':
        return self/abs(self)
    @staticmethod
    def rect(x:num=0.0,y:num=0.0) -> 'vec':
        '''
        rectangular coordinates, same as vec(x,y)
        '''
        return vec(x,y)
    @staticmethod
    def polarr(r:num=0.0,t:num=0.0) -> 'vec':
        '''
        polar coordinates with radians
        '''
        return vec(r*math.cos(t),r*math.sin(t))
    @staticmethod
    def polard(r:num=0.0,t:num=0.0) -> 'vec':
        '''
        polar coordinates with degrees
        '''
        return vec.polarr(r,t*math.pi/180)
    @staticmethod
    def convcomb(v1:'vec|tvec',v2:'vec|tvec',c:num) -> 'vec':
        '''
        convex combination
        '''
        if isinstance(v1,tuple):
            v1 = vec(v1)
        if isinstance(v2,tuple):
            v2 = vec(v2)
        return c*v1 + (1-c)*v2
    @staticmethod
    def midpoint(v1:'vec|tvec',v2:'vec|tvec') -> 'vec':
        '''
        midpoint/average of 2 vectors
        '''
        return vec.convcomb(v1,v2,0.5)
    @staticmethod
    def proj(a:'vec|tvec',b:'vec|tvec') -> 'vec':
        '''
        vector projection of a onto b
        '''
        if isinstance(a,tuple):
            a = vec(a)
        if isinstance(b,tuple):
            b = vec(b)
        return (a@b)*b/b.radsq()
    @staticmethod
    def angler(v1:'vec|tvec',v2:'vec|tvec') -> float:
        '''
        angle between 2 vectors (radians)
        '''
        if isinstance(v1,tuple):
            v1 = vec(v1)
        if isinstance(v2,tuple):
            v2 = vec(v2)
        return math.acos((v1@v2)/(abs(v1)*abs(v2)))
    @staticmethod
    def angled(v1:'vec|tvec',v2:'vec|tvec') -> float:
        '''
        angle between 2 vectors (degrees)
        '''
        return vec.angler(v1,v2)*180/math.pi

# "point vector/float"
pvf = vec|tvec|num

# "point none/float"
pnf = None|num

def parsevec1(a:pvf,b:pnf=None) -> vec:
    if isinstance(a,(vec,tuple)):
        return vec(a)
    elif isinstance(a,num) and isinstance(b,num):
        return vec(a,b)
    else:
        raise ValueError()

def parsevec2(a:pvf,b:pvf,c:pnf=None,d:pnf=None) -> tuple[vec,vec]:
    if isinstance(a,(vec,tuple)) and isinstance(b,(vec,tuple)):
        return vec(a),vec(b)
    elif isinstance(a,num) and isinstance(b,num) \
        and isinstance(c,num) and isinstance(d,num):
        return vec(a,b),vec(c,d)
    else:
        raise ValueError()

def parsevec3(a:pvf,b:pvf,c:pvf,d:pnf=None,e:pnf=None,f:pnf=None) -> tuple[vec,vec,vec]:
    if isinstance(a,(vec,tuple)) and isinstance(b,(vec,tuple)) and isinstance(c,(vec,tuple)):
        return vec(a),vec(b),vec(c)
    elif isinstance(a,num) and isinstance(b,num) and isinstance(c,num) \
        and isinstance(d,num) and isinstance(e,num) and isinstance(f,num):
        return vec(a,b),vec(c,d),vec(e,f)
    else:
        raise ValueError()

# TODO "vec3" class for 3d vector
