numbers = [22, 14, 42, 33, 25, 63, 21, 20, 10, 15]

# Find the minimum number in the list
def min(numbers):
    min = numbers[0]
    for number in numbers:
        if number < min:
            min = number
    return min

# Find the maximum number in the list
def max(numbers):
    max = numbers[0]
    for number in numbers:
        if number > max:
            max = number
    return max
# Find the average of the numbers in the list
def avg(numbers):
    average = numbers[0]
    for number in numbers[1:]:
        average += number
    return average / len(numbers)

print(f"Minimum: {min(numbers)}")
print(f"Maximum: {max(numbers)}")
print(f"Average: {avg(numbers)}")