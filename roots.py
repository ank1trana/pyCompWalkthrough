import numpy as np
import sympy as sp

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
