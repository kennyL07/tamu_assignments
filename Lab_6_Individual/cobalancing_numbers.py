# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   Lab 6
# Date:         DAY MONTH 2026
#

cobalancing_num = int(input("Enter a value for n: "))

leftSide = sum(range(cobalancing_num+1)) # Sum of all values from 0 - n (Basically 1 - n)

r = 0
rightSide = 0
while(rightSide < leftSide): # Stops when right side >= leftSide
    r += 1 # Start with the value directly after n
    rightSide += cobalancing_num + r

if (rightSide != leftSide):
    print(f"{cobalancing_num} is not a co-balancing number")
else:
    print(f"{cobalancing_num} is a co-balancing number with r={r}")