def squareRoot(n, precision=0.00001):
    if n < 0:
        return None  # Square root of a negative number is not defined in real numbers

    guess = n / 2.0  # Initial guess
    while abs(guess * guess - n) > precision:
        guess = 0.5 * (guess + n / guess)  # Newton's formula
    return guess

x = 16.0
y = 15.0
z = 25.0

print(squareRoot(x))  # Should print a value close to 4.0
print(squareRoot(y))  # Should print a value close to 3.87
print(squareRoot(z))  # Should print a value close to 5.0
print(squareRoot(-1))  # Should print None