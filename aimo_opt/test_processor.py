from aimo_opt.optimize_aimo import AMCProcessor


def test_extract_final_answer_basic_code():
    """
    Test basic code block execution and answer extraction.
    """
    processor = AMCProcessor()

    response = '''
Here's the solution:
```python
x = 5 + 3
print(x)
```
'''
    assert processor.extract_final_answer(response) == "8"


def test_extract_final_answer_multiple_prints():
    """
    Test handling of multiple print statements in code block.
    """
    processor = AMCProcessor()

    response = '''
```python
print("intermediate")
print(42)
print("final:", 79)
```
'''
    assert processor.extract_final_answer(response) == "79"


def test_extract_final_answer_computation():
    """
    Test code block with mathematical computation.
    """
    processor = AMCProcessor()

    response = '''
```python
import math
result = math.factorial(4)
print(result)
```
'''
    assert processor.extract_final_answer(response) == "24"


def test_extract_final_answer_invalid_code():
    """
    Test handling of invalid Python code.
    """
    processor = AMCProcessor()

    response = '''
    ```python
    x = 1/0  # Division by zero error
    ```
    '''
    assert processor.extract_final_answer(response) == processor.INVALID_ANS


def test_extract_final_answer_non_numeric():
    """
    Test handling of non-numeric output.
    """
    processor = AMCProcessor()

    response = '''
```python
print("hello")
```
'''
    assert processor.extract_final_answer(response) == processor.INVALID_ANS


def test_extract_final_answer_boxed():
    """
    Test extraction of boxed LaTeX answers.
    """
    processor = AMCProcessor()

    response = r'\boxed{42}'
    assert processor.extract_final_answer(response) == "42"


def test_extract_final_answer_code_and_boxed():
    """
    Test precedence of code output over boxed answer.
    """
    processor = AMCProcessor()

    response = '''
```python
print(79)
```
Final answer: \boxed{42}
'''
    assert processor.extract_final_answer(response) == "79"


def test_extract_realistic_coded():
    """
    Test precedence of code output over boxed answer.
    """
    processor = AMCProcessor()

    response = '''
To solve this problem, we need to find the length of segment \( BE \) in a given triangle \( ABC \) with sides \( BC = 108 \), \( CA = 126 \), and \( AB = 39 \). Point \( X \) lies on segment \( AC \) such that \( BX \) bisects \( \angle CBA \), \( \omega \) is the circumcircle of triangle \( ABX \), and point \( Y \) is on \( \omega \) different from \( X \) such that \( CX = CY \). Line \( XY \) meets \( BC \) at \( E \). The length of \( BE \) is to be expressed as \( \frac{n}{m} \), where \( m \) and \( n \) are coprime positive integers, and we need to find \( m + n \).

### Approach

1. **Angle Bisector Theorem**: Since \( BX \) bisects \( \angle CBA \), we can use the angle bisector theorem to find the position of \( X \) on \( AC \).
2. **Circumcircle Properties**: \( \omega \) is the circumcircle of \( \triangle ABX \), and \( Y \) is a point on \( \omega \) such that \( CX = CY \). We need to find properties related to this circle and the given equal lengths.
3. **Intersection Point**: Line \( XY \) intersects \( BC \) at \( E \), and we need to find the length \( BE \).

### Solution Code

To solve this problem using Python and SymPy, we need to perform several geometric constructions and calculations. Here is the step-by-step code to find the length of \( BE \):

```python
import sympy as sp
# Define the given lengths
BC = 108
CA = 126
AB = 39
# Using the angle bisector theorem to find AX and CX
# BX bisects angle CBA, so AX/XC = AB/BC = 39/108 = 13/36
# Let AX = 13k and XC = 36k
# Since AX + XC = AC = 126, so 13k + 36k = 126 => 49k = 126 => k = 126/49 = 18/7
k = sp.Rational(18, 7)
AX = 13 * k
XC = 36 * k
# Now, CX = CY, and Y is on the circumcircle of ABX
# We need to find coordinates or use properties to find BE
# Let's place the triangle in a coordinate system
# Let's place point B at (0,0), C at (108,0), and find coordinates of A
# Using coordinates:
# Let B = (0,0), C = (108,0)
# Let A = (x,y), then distance AB = 39, AC = 126
x, y = sp.symbols('x y')
eq1 = sp.Eq(sp.sqrt(x**2 + y**2), AB)
eq2 = sp.Eq(sp.sqrt((x - 108)**2 + y**2), CA)
# Solve for x and y
sol = sp.solve((eq1, eq2), (x, y))
A = sol[1]  # Choose the positive y coordinate
# Now, find coordinates of X on AC such that AX/XC = 13/36
# Coordinates of X:
# X divides AC in the ratio 13:36
AX_ratio = 13
XC_ratio = 36
total_ratio = AX_ratio + XC_ratio
X_x = (AX_ratio * C[0] + XC_ratio * A[0]) / total_ratio
X_y = (AX_ratio * C[1] + XC_ratio * A[1]) / total_ratio
X = (X_x, X_y)
# Now, find the circumcircle of ABX
# Points A, B, X
# General equation of circle: x^2 + y^2 + dx + ey + f = 0
d, e, f = sp.symbols('d e f')
eqA = A[0]**2 + A[1]**2 + d*A[0] + e*A[1] + f
eqB = B[0]**2 + B[1]**2 + d*B[0] + e*B[1] + f
eqX = X_x**2 + X_y**2 + d*X_x + e*X_y + f
# Solve for d, e, f
sol_circle = sp.solve([eqA, eqB, eqX], (d, e, f))
circle_eq = sp.Eq(sp.Symbol('x')**2 + sp.Symbol('y')**2 + sol_circle[d]*sp.Symbol('x') + sol_circle[e]*sp.Symbol('y') + sol_circle[f], 0)
# Now, find point Y on the circle such that CX = CY
# CX is known, CY should be equal to CX
# Distance CY: sqrt((y - C_y)^2 + (x - C_x)^2) = CX
CX_length = sp.sqrt((X_x - C[0])**2 + (X_y - C[1])**2)
Y_x, Y_y = sp.symbols('Y_x Y_y')
distance_CY = sp.sqrt((Y_x - C[0])**2 + (Y_y - C[1])**2)
eq_CY = sp.Eq(distance_CY, CX_length)
# Y is on the circle: circle_eq
eq_circle = circle_eq.subs({'x': Y_x, 'y': Y_y})
# Solve for Y coordinates
sol_Y = sp.solve([eq_circle, eq_CY], (Y_x, Y_y))
# Choose the point different from X
Y = [pt for pt in sol_Y if pt != X][0]
# Now, find the intersection E of XY and BC
# Line XY: parametrize or find equation
# Points X and Y, find the line equation
# Parametrize line XY
t = sp.symbols('t')
E_x = X_x + t*(Y_x - X_x)
E_y = X_y + t*(Y_y - X_y)
# E lies on BC, which is the x-axis (y=0)
eq_E_y = sp.Eq(E_y, 0)
t_val = sp.solve(eq_E_y, t)[0]
E_x_val = E_x.subs(t, t_val)
E = (E_x_val, 0)
# Now, find BE: distance from B to E
BE = sp.sqrt((E_x_val - B[0])**2 + (E_y - B[1])**2)
BE_simplified = sp.simplify(BE)
BE_fraction = sp.Rational(BE_simplified).limit_denominator()
n, m = BE_fraction.as_numer_denom()
result = n + m
print(result)
```
'''
    assert processor.extract_final_answer(response) != processor.INVALID_ANS


def test_extract_realistic_code_2():
    """
    Test precedence of code output over boxed answer.
    """
    processor = AMCProcessor()

    response = '''
To tackle this problem, we need to find all integers \( m \) between 2 and 40 for which there exist \( m \) distinct positive integers \( a_1, a_2, \dots, a_m \) such that the sum of these integers is equal to the sum of their pairwise greatest common divisors plus one. In other words, we need to satisfy the equation:
\[
a_1 + a_2 + \dots + a_m = G(a_1, a_2, \dots, a_m) + 1
\]
where \( G(a_1, a_2, \dots, a_m) \) is the sum of the pairwise greatest common divisors of the \( a_i \)'s.
### Approach
1. **Understanding the Problem:**
   - We need to find sets of \( m \) distinct positive integers where the sum of the elements equals the sum of all pairwise GCDs plus one.
   - This seems quite restrictive, so we might need to look for patterns or specific properties of the numbers involved.
2. **Simplifying the Problem:**
   - For small \( m \), we can try to find such sets manually or through code.
   - We need to compute the sum of pairwise GCDs, which for \( m \) numbers is \( \sum_{1 \leq i < j \leq m} \gcd(a_i, a_j) \).
3. **Key Observations:**
   - If all \( a_i \) are equal, but they need to be distinct.
   - Perhaps considering numbers where some are multiples of others could simplify GCD calculations.
4. **Plan:**
   - Write a function to compute the sum of pairwise GCDs.
   - Iterate over possible sets of \( m \) distinct positive integers and check if they satisfy the condition.
   - Due to the combinatorial explosion, we need an efficient way to generate and test these sets.
### Solution Code
To solve this problem, we will write a Python script that iterates through possible values of \( m \) from 2 to 40 and checks for the existence of \( m \) distinct positive integers whose sum equals the sum of their pairwise GCDs plus one.
```python
import math
from itertools import combinations
def sum_pairwise_gcds(nums):
    n = len(nums)
    total = 0
    for i in range(n):
        for j in range(i + 1, n):
            total += math.gcd(nums[i], nums[j])
    return total
def is_artificial(m):
    # We need to find m distinct positive integers a1, a2, ..., am such that
    # a1 + a2 + ... + am = sum of pairwise gcds + 1
    # To make it manageable, we'll try small ranges for ai
    
    # Let's try ai in the range 1 to 100
    for combo in combinations(range(1, 101), m):
        s = sum(combo)
        gcd_sum = sum_pairwise_gcds(combo)
        if s == gcd_sum + 1:
            return True
    return False
artificial_ms = []
for m in range(2, 41):
    if is_artificial(m):
        artificial_ms.append(m)
print(sum(artificial_ms))
```
### Explanation
1. **sum_pairwise_gcds Function:**
   - Computes the sum of the greatest common divisors (GCDs) of all pairs in a given list of numbers.
2. **is_artificial Function:**
   - Checks if there exists a set of \( m \) distinct positive integers within the range 1 to 100 that satisfy the condition \( a1 + a2 + ... + am = G(a1, a2, ..., am) + 1 \).
   - Uses combinations from itertools to generate all possible combinations of \( m \) distinct numbers from 1 to 100 and checks the condition for each combination.
3. **Main Loop:**
   - Iterates over \( m \) from 2 to 40 and uses the `is_artificial` function to check if \( m \) is artificial.
   - Collects all artificial \( m \) values and computes their sum.
This approach ensures that we systematically check for the condition across the specified range of \( m \) and possible sets of integers, leveraging combinatorial generation and GCD computations.
'''
    assert processor.extract_final_answer(response) != processor.INVALID_ANS


def test_extract_final_answer_invalid_format():
    """
    Test handling of invalid answer formats.
    """
    processor = AMCProcessor()

    response = "The answer is 42"
    assert processor.extract_final_answer(response) == processor.INVALID_ANS


def test_extract_final_answer_empty():
    """
    Test handling of empty or None input.
    """
    processor = AMCProcessor()

    assert processor.extract_final_answer("") == processor.INVALID_ANS
    assert processor.extract_final_answer(None) == processor.INVALID_ANS
