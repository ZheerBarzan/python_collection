#gauss additon problems

def gauss_additon(n):
    return n*(n+1)//2


def main():
    n = int(input("Enter the number: "))
    result = gauss_additon(n)
    print(f"The sum of the first {n} natural numbers is {result}")
if __name__ == '__main__':
    main()