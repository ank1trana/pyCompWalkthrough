print('hi')
print('hi'+'1231231'+str(99999))
def a_method():
    print('well here we are in a method')
print('\n\t all done, now out')

def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)