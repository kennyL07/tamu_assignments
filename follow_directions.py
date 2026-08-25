# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      519
# Assignment:   Lab 1
# Date:         25 8 2026
#

from math import cos
from math import radians

print("This shows the evaluation of (1-cos(x))/x^2 evaluated close to x=0")
print("My guess is indefinite")
for x in range(8):
    y = 1 / 10**x # moving the decimal over
    print( (1 - cos((y))) / y**2 )
print()
print("My guess was very off!")