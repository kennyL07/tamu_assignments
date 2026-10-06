# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   Lab 6
# Date:         DAY MONTH 2026
#
from math import floor
from math import sqrt

n = int(input("Enter a positive integer: ")) # Starting number of juggler seq
current_num = n # Store this as different variable since we will be operating on it
iterations = 0
juggler_seq = "" + str(n) # Start the string with the starting number

while (current_num != 1):
    if current_num % 2 == 0:
        current_num = floor(sqrt(current_num))
    elif current_num % 2 == 1:
        current_num = floor(current_num ** (3/2))
    juggler_seq = juggler_seq + ", " + str(current_num)
    iterations += 1

print(f"The Juggler sequence starting at {n} is:")
print(juggler_seq)
print(f"It took {iterations} iterations to reach 1")