# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   Lab 3 Individual
# Date:         3 9 2026
#
from math import pi
digits = int(input("Please enter the number of digits of precision for tau: "))
print(f"The value of tau to {digits} digits is: {2 * pi:.{digits}f}") # Tau = 2 * pi