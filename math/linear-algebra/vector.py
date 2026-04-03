import sys
import os 
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f'{CURR_DIR}/../common')
from fraction import Fraction as F
from typing import List

class Vector:
    def __init__(self, * args):
        self.vec = list(args)

        for i, num in enumerate(self.vec):
            if not (isinstance(num, F) or isinstance(num, int)):
                raise ValueError(f'Vector must either be a fraction or an integer')
            
            if isinstance(num, int):
                self.vec[i] = F(num)

        self.s = len(self.vec)

    def __str__(self) -> str:
        out = f'{{'

        for i in range(self.s):
            if i < self.s - 1:
                out += f'{self.vec[i]}, '
            else:
                out += f'{self.vec[i]}'
        out += f'}}'
        return out

    def __add__(self, other : "Vector") -> "Vector":
        if other.s != self.s:
            raise ValueError(f'The two vectors must be the same size!')
        
        return Vector(*[self.vec[i] + other.vec[i] for i in range(self.s)])
    
    def __sub__(self, other : "Vector") -> "Vector":
        if other.s != self.s:
            raise ValueError(f'The two vectors must be the same size!')
        
        return Vector(*[self.vec[i] - other.vec[i] for i in range(self.s)])
    
    def __mul__(self, other):
        if isinstance(other, Vector):
            if other.s != self.s:
                raise ValueError(f'The two vectors must be the same size!')
            
            return sum([self.vec[i] * other.vec[i] for i in range(self.s)], start=F(0))
        else:
            return Vector(*[self.vec[i] * other for i in range(self.s)])

    def __truediv__(self, x):
        if isinstance(x, int):
            return self.__mul__(F(1,x))
        else:
            return self.__mul__(F(x.denom, x.numer))
    
    def __iadd__(self, other : "Vector") -> "Vector":
        return self.__add__(other)
    
    def __isub__(self, other : "Vector") -> "Vector":
        return self.__sub__(other)
    
    def __imul__(self, other):
        return self.__mul__(other)

    def __itruediv__(self, x) -> "Vector":
        return self.__truediv__(x)
    
"""
Project u onto v
"""
def proj(u : Vector, v : Vector):
    numer = u * v 
    denom = v * v 

    s = numer / denom

    return v * s

def normalize(u : Vector) -> Vector:
    magnitude = u * u 
    return u / magnitude.sqrt()


"""
returns an orthonormal version
"""
def gram_schmidt(basis : List[Vector]):
    out = []
    for b in basis:
        new = b
        for o in out:
            new -= proj(b, o)
        out.append(new)

    return list(map(normalize, out))


if __name__ == '__main__':

    v = Vector(2, -10, -2, -2)
    
    a = Vector(-5, 4, 4, 1)
    b = Vector(-2, 4, 3, -38)
    b -= proj(b, a)

    v = (proj(v, a) + proj(v, b))
    print(v)
