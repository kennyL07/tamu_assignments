# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   Lab 4 Individual
# Date:         10 9 2026
#

from math import sqrt

A = float(input("Please enter the coefficient A: "))
B = float(input("Please enter the coefficient B: "))
C = float(input("Please enter the coefficient C: "))

if (A == 0) and (B == 0) and not (C == 0):
    print('You entered an invalid combination of coefficients!')
    exit()

if (A == 0):
    print("The root is x =", C * -1 / B)
    exit()

discriminant = B**2 - 4*A*C # need to check for imaginary numbers
if discriminant >= 0:
    numerator1 = (-1 * B + sqrt(discriminant))
    numerator2 = (-1 * B - sqrt(discriminant))
    denominator = 2 * A
    if (numerator1 == numerator2):
        print(f"The root is x = { numerator1 / denominator }")
    else:
        print(f"The roots are x = { numerator1 / denominator } and x = {numerator2 / denominator}")
else:
    imaginary = sqrt(abs(B**2 + (-4*A*C)))
    print(f"The roots are x = { -B / (2 * A) } + {imaginary / (2 * A)}i and x = { -B / (2 * A) } - {imaginary / (2 * A)}i")