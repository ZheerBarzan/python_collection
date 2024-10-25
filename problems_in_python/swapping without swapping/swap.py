# using XOR operator to swap two numbers without using a temporary variable
a = 0b1010
b = 0b0011
print('a=',bin(a),' b=', bin(b)) # 0b1010 0b0011
a = a^b
b = a^b
print('a=',bin(a),' b=', bin(b)) # 0b1010 0b0011
a = a^b
print('a=',bin(a),' b=', bin(b)) # 0b1010 0b0011
