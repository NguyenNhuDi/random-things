import sys
import os 
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f'{CURR_DIR}/../common')
from fraction import Fraction as F

class Vector:
    def __init__(self, * args):
        self.vec = list(args)

        for i, num in enumerate(self.vec):
            if not (isinstance(num, F) or isinstance(num, int)):
                raise ValueError(f'Vector must either be a fraction or an integer')
            
            if isinstance(num, int):
                self.vec[i] = F(num)

        self.s = len(self.vec)

    def __add__(self, other : "Vector") -> "Vector":
        if other.s != self.s:
            raise ValueError(f'The two vectors must be the same size!')
        
        return Vector(*[self.vec[i] + other.vec[i] for i in range(self.s)])
    
    def __sub__(self, other : "Vector") -> "Vector":
        if other.s != self.s:
            raise ValueError(f'The two vectors must be the same size!')
        
        return Vector(*[self.vec[i] - other.vec[i] for i in range(self.s)])
    
    def __mul__(self, other : "Vector") -> F:
        if other.s != self.s:
            raise ValueError(f'The two vectors must be the same size!')
        sum([self.vec[i] * other.vec[i] for i in range(self.s)])

    def __mul__(self, x : int) -> "Vector":
        return Vector(*[self.vec[i] * x for i in range(self.s)])
    
    def __truediv__(self, x : int) -> "Vector":
        return self.__mul__(F(1,x))
    
    def __iadd__(self, other : "Vector") -> "Vector":
        return self.__add__(other)
    
    def __isub__(self, other : "Vector") -> "Vector":
        return self.__sub__(other)
    
    def __imul__(self, other : "Vector") -> F:
        return self.__mul__(other)

    def __imul__(self, x : int) -> "Vector":
        return self.__mul__(x)
        
