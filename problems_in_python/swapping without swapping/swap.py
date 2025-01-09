# using XOR operator to swap two numbers without using a temporary variable
from numpy.matlib import empty

a = 5
b = 10
print('a=',bin(a),' b=', bin(b)) # a=5  b=10 and in binary a=101 and b=1010
a = a^b
b = a^b
print('a=',bin(a),' b=', bin(b))
a = a^b
print('a=',bin(a),' b=', bin(b)) # a=1010 and b=101 in decimal a=10 and b=5



coffeeCup = "Coffee"
teaCup = "Tea"
print(f"Before swapping: [coffee cup contains: {coffeeCup} | tea cup contains: {teaCup}]")
emptyCup = coffeeCup
coffeeCup = teaCup
teaCup = emptyCup
print(f"After swapping: [coffee cup contains: {coffeeCup} | tea cup contains: {teaCup}]")