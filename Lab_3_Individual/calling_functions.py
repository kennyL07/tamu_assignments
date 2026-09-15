# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   THE ASSIGNMENT NUMBER (e.g. Lab 1b-2)
# Date:         DAY MONTH 2026
#

from math import sqrt

def printresult(shape, side, area):
    '''Print the result of the calculation'''
    print(f'A {shape} with side {side:.2f} has area {area:.3f}')

sideLength = float(input("Please enter the side length: "))
printresult("triangle", sideLength, sideLength**2 * sqrt(3) / 4) # Inline calculations
printresult("square", sideLength, sideLength**2)
printresult("pentagon", sideLength, (0.25 * sqrt(5 * (5 + 2 * sqrt(5))) * sideLength ** 2)) # sqrt of  5 + 2 * sqrt of 5
printresult("hexagon", sideLength, 3 * sqrt(3) / 2 * sideLength**2)
printresult("dodecagon", sideLength, 3 * (2 + sqrt(3)) * sideLength**2)