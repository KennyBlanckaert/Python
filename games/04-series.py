import math

# These functions return generators
def squares():
    for i in range(1, 10):
        yield int(i**2)

def fibonacci():
    a,b = 1,1
    for i in range(1, 10):
        yield int(a)
        a,b = b, a+b

def pi_numbers():
    for item in str(math.pi):
        if (item != "."):
            yield int(item)

# User console
print("")
print("###################################")
print("Welcome!")
print("")
print("Which series do you want to train?")
print("-----------------------------------")
print("1. Squares of 1 to 10")
print("2. Fibonacci serie")
print("3. Numbers of pi")
print("")

success = False
while not success:
    try:
        number = int(input("> "))
    except:
        print("That's not a number? Try again.")
    else:
        if (1 <= number <= 3):
            success = True

# Set function
global function
if (number == 1):
    function = squares
elif (number == 2):
    function = fibonacci
else:
    # this is also a generator
    function = pi_numbers

# Start training
for number in function():
    global guess 
    success = False
    while not success:
        try:
            guess = int(input("Guess the number: "))
        except:
            print("That's not a number? Try again.")
        else:
            success = True

    if (guess == number):
        print("Indeed! That's correct.")
    else:
        print(f"Hmm, no! That's not right. The number was {number}")
    



