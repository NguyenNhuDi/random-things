def gcd(a : int, b : int):
    """
        Euclidean Algorithm states that:
        if a > b then gcd(a, b) = gcd(b, a mod(b))
    """

    if a == b:
        return a 
    
    elif a < b:
        a, b = b, a 
    
    return a if b == 0 else gcd(b, a % b)

if __name__ == '__main__':
    print(gcd(10, 2), gcd(3, 4))