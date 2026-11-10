# By submitting this assignment, I agree to the following:
# "Aggies do not lie, cheat, or steal, or tolerate those who do."
# "I have not given or received any unauthorized aid on this assignment."
#
# Names: Kennyson Le
# Adila Hansbhai
# Kingston Jackson
# Tevya Birnbaum
# Section: 567
# Assignment: Lab 3
# Date: 24 9 2026
#

from math import log

x = float(input("Enter a value for x: ")) # storing user input as 'x'
while x <= 0 or x > 2:
    x = float(input("Out of range! Try again: ")) # runs loop again if user inputs an invalid value
tolerance = float(input("Enter the tolerance: ")) # storing user input as "tolerance"

nlog = log(x)

sum = 0.0
i = 1
while (True):
    term = ((-1) ** (i - 1)) * ((x - 1) ** i) / i
    
    if abs(term) < tolerance:
        break
    sum += term
    i += 1

print(f"ln({x}) is approximately {sum}")
print(f"ln({x}) is exactly", nlog)
print(f"The difference is", abs((nlog - sum)))