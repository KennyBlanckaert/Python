import random as random

guesses = 0
last_difference = 0
random_number = random.randint(1, 100)
entered_number = int(input("Choose a number: "))

while (random_number != entered_number):
  	
	# Error message
	if (1 > entered_number > 100):
		print("OUT OF BOUNDS: guess a number between 1 and 100.")
		continue

	# Aid on first turn 
	if (guesses == 0):
		if ((random_number - 10) <= entered_number <= (random_number + 10)):
			print("WARM!")
		else:
			print("COLD")

	# Aid on other turns
	difference = abs(entered_number - random_number)
	if (guesses > 0):
		if (difference < last_difference):
			print("WARMER!")
		else:
			print("COLDER!")

	# recalculate last_difference
	last_difference = difference
	
	# Increment guesses
	guesses += 1

	# Next guess
	entered_number = int(input("Choose your next number: "))


print("Congratulations! You guessed the number.")
print(f"Required guesses: {guesses}")