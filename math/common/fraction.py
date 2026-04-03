from util import gcd

class Fraction:
    def __init__(self, numer, denom = 1):
        
        if denom == 0:
            raise ZeroDivisionError

        g = gcd(numer, denom)
        
        self.numer = numer // g
        self.denom = denom // g

    def __str__(self):
        return f'{self.numer} / {self.denom}'

    def __lt__(self, other : "Fraction") -> bool:
        a = self.numer * other.denom
        b = other.numer * self.denom
        return a < b 

    def __le__(self, other : "Fraction") -> bool:
        a = self.numer * other.denom
        b = other.numer * self.denom
        return a <= b 
    
    def __neg__(self) -> "Fraction":
        return Fraction(-self.numer, -self.denom)
    
    def __gt__(self, other : "Fraction") -> bool:
        return not self.__le__(other)

    def __ge__(self, other : "Fraction") -> bool:
        return not self.__lt__(other)
    
    def __eq__(self, other : "Fraction") -> bool:
        return other.numer == self.numer and other.denom == self.denom
    
    def __ne__(self, value : "Fraction") -> bool:
        return not self.__eq__(value)
    
    def __add__(self, other : "Fraction") -> "Fraction":
        a_num = self.numer * other.denom
        b_num = other.numer * self.denom

        denom = self.denom * other.denom
        numer = a_num + b_num

        return Fraction(numer=numer, denom=denom)
    
    def __sub__(self, other : "Fraction") -> "Fraction":
        a_num = self.numer * other.denom
        b_num = other.numer * self.denom

        denom = self.denom * other.denom
        numer = a_num - b_num

        return Fraction(numer=numer, denom=denom)
    
    def __mul__(self, other : "Fraction"):
        return Fraction(numer=(self.numer * other.numer), denom=(self.denom * other.denom))
    
    def __truediv__(self, other : "Fraction") -> "Fraction":
        flip = Fraction(numer=other.denom, denom=other.numer)
        return self.__mul__(flip)
    
    def __iadd__(self, other : "Fraction") -> "Fraction":
        return self.__add__(other)
    
    def __isub__(self, other : "Fraction") -> "Fraction":
        return self.__sub__(other)

    def __imul__(self, other : "Fraction") -> "Fraction":
        return self.__mul__(other)
    
    def __itruediv__(self, other : "Fraction") -> "Fraction":
        return self.__truediv__(other)
    

    
if __name__ == '__main__':
    a = Fraction(1, 2)
    b = Fraction(1, 4)

    c = a + b 
    d = a - b
    e = a * b 
    f = a / b 

    print(a)
    print(b)
    print(c)
    print(d)
    print(e)
    print(f)
    
