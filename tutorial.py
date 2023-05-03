import numpy as np
import sympy as sp

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
    

def factorial(n):
    """
    Computes the factorial of a non-negative integer n using recursion.
    """
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
    


# Define the polynomial coefficients
p = np.array([1, -5, 6])

# Find the roots using NumPy
roots_np = np.roots(p)

# Print the roots found by NumPy
print("Roots found by NumPy:", roots_np)

# Find the roots using SymPy
x = sp.symbols('x')
poly = sp.Poly(p, x)
roots_sp = poly.all_roots()

# Print the roots found by SymPy
print("Roots found by SymPy:", roots_sp)

