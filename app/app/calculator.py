"""
calculator module

"""


def add(a, b):
    """Returns the sum of a and b."""
    return a + b


def subtract(a, b):
    """Returns the difference of a and b."""
    return a - b


def multiply(a, b):
    """Returns the product of a and b."""
    return a * b    

def divide(a, b):
    """Returns the quotient of a and b. Raises ValueError if b is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b    

def power(base, exponent):
    """Returns base raised to the power of exponent."""
    return base ** exponent 

def modulus(a, b):
    """Returns the remainder of a divided by b."""
    if b == 0:
        raise ValueError("Cannot perform modulus with zero.")
    return a % b

def square_root(x):
    """Returns the square root of x. Raises ValueError if x is negative."""
    if x < 0:
        raise ValueError("Cannot compute square root of a negative number.")
    return x ** 0.5

def absolute_value(x):
    """Returns the absolute value of x."""
    return abs(x)

def factorial(n):
    """Returns the factorial of n. Raises ValueError if n is negative."""
    if n < 0:
        raise ValueError("Cannot compute factorial of a negative number.")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def logarithm(x, base=10):
    """Returns the logarithm of x to the specified base. Raises ValueError if x is non-positive."""
    if x <= 0:
        raise ValueError("Logarithm undefined for non-positive values.")
    import math
    return math.log(x, base)    

def sine(angle):
    """Returns the sine of the angle in radians."""
    import math
    return math.sin(angle)  

def cosine(angle):
    """Returns the cosine of the angle in radians."""
    import math
    return math.cos(angle)

def tangent(angle): 
    """Returns the tangent of the angle in radians."""
    import math
    return math.tan(angle)


def factorial_recursive(n):
    """Returns the factorial of n using recursion. Raises ValueError if n is negative."""
    if n < 0:
        raise ValueError("Cannot compute factorial of a negative number.")
    if n == 0 or n == 1:
        return 1
    return n * factorial_recursive(n - 1)

def gcd(a, b):
    """Returns the greatest common divisor of a and b. Raises ValueError if either a or b is zero."""
    if a == 0 or b == 0:
        raise ValueError("Cannot compute GCD with zero.")
    while b:
        a, b = b, a % b
    return abs(a)

def lcm(a, b):
    """Returns the least common multiple of a and b. Raises ValueError if either a or b is zero."""
    if a == 0 or b == 0:
        raise ValueError("Cannot compute LCM with zero.")
    return abs(a * b) // gcd(a, b)

def is_prime(n):
    """Returns True if n is a prime number, otherwise False. Raises ValueError if n is less than 2."""
    if n < 2:
        raise ValueError("Input must be greater than or equal to 2.")
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def fibonacci(n):
    """Returns the nth Fibonacci number. Raises ValueError if n is negative."""
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    if n == 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b    

def nth_prime(n):
    """Returns the nth prime number. Raises ValueError if n is less than 1."""
    if n < 1:
        raise ValueError("Input must be a positive integer.")
    count = 0
    num = 1
    while count < n:
        num += 1
        if is_prime(num):
            count += 1
    return num
