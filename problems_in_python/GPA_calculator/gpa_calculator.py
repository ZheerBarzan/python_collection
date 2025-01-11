
engilsh = float(input("Enter the marks of English: "))
maths = float(input("Enter the marks of Maths: "))
physics = float(input("Enter the marks of Physics: "))
chemistry = float(input("Enter the marks of Chemistry: "))
computer = float(input("Enter the marks of Computer: "))
biology = float(input("Enter the marks of Biology: "))


allLessons = [engilsh, maths, physics, chemistry, computer, biology]

def calculateAverage(allLessons):
    total = sum(allLessons)
    average = total / len(allLessons)
    return average

if __name__ == '__main__':
    average = calculateAverage(allLessons)
    print(f"The average marks is {average}")
    if average >= 90:
        print("Grade: A")
    elif average >= 80:
        print("Grade: B")
    elif average >= 70:
        print("Grade: C")
    elif average >= 60:
        print("Grade: D")
    elif average >= 50:
        print("Grade: E")
    else:
        print("Grade: F")
