# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   Lab 5
# Date:         9 16 2026
#

from math import log10

excessTemperature = float(input("Enter the excess temperature: "))
points = [(1.3, 1000), (5, 7000), (30, 1500000), (120, 25000), (1200, 1500000)]

def logLinearInterpolation(x: float) -> float:
    if x < points[0][0] or x > points[-1][0]: # Edge cases where value isn't within the range of points
        print("Surface heat flux is not available")
        return
    for i in range(len(points)):
        if x == points[i][0]: # Edge case for when the points are equal
            print(f"The surface heat flux is approximately {points[i][1]} W/m^2")
            return
        if points[i][0] < x < points[i + 1][0]:
            x0, y0 = points[i]
            x1, y1 = points[i + 1] # Don't need to be scared of a bounds error since we already checked those cases
            m = log10(y1 / y0) / log10(x1 / x0) # Solving for exponent m
            y = y0 * (x / x0) ** m
            print(f"The surface heat flux is approximately {round(y)} W/m^2")
            return

logLinearInterpolation(excessTemperature)

# Test cases
# logLinearInterpolation(-1)
# logLinearInterpolation(1.3)
# logLinearInterpolation(5)
# logLinearInterpolation(30)
# logLinearInterpolation(120)
# logLinearInterpolation(1000)
# logLinearInterpolation(1000000)
# logLinearInterpolation(2)
# logLinearInterpolation(14)
# logLinearInterpolation(99)
# logLinearInterpolation(600)
