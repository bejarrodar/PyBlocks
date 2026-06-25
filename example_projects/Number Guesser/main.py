# Guess the Number Game  # __pyblocks_id__:b0
import random  # __pyblocks_id__:b1
number = random.randint(1, 10)  # __pyblocks_id__:b2
guess = int(input("Guess a number 1-10: "))  # __pyblocks_id__:4b02d29f
if guess == number:  # __pyblocks_id__:b4
    print("You got it!")  # __pyblocks_id__:b4c0
else:  # __pyblocks_id__:b5
    print("Wrong! It was " + str(number))  # __pyblocks_id__:b5c0