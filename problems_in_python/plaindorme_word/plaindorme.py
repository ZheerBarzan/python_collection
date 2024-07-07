def plaindorme( word):
    if len(word) == 0:
        return True
    elif word[0] != word[-1]:
        return False
    else:
        return plaindorme(word[1:-1])


print(plaindorme("racecar"))
print(plaindorme("hello"))
print(plaindorme("wow"))