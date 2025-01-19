import random

def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)

user_input = input("Enter 'r' to roll the dice or 'q' to quit: ")
isPlaying = True

while isPlaying:
    if user_input == 'r':
        dice1, dice2 = roll_dice()
        print(f"Dice 1: {dice1}")
        print(f"Dice 2: {dice2}")
        user_input = input("Enter 'r' to roll the dice or 'q' to quit: ")
    elif user_input == 'q':
        isPlaying = False
    else:
        print("Invalid input")
        user_input = input("Enter 'r' to roll the dice or 'q' to quit: ")
