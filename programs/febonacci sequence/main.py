

def feb(n):

    if n <=2:
        result = 1
    else:
        result = feb(n -1) + feb(n-2)

    return result


print(feb(7))
print(feb(50))