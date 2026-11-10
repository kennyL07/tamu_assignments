# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   Lab 6
# Date:         DAY MONTH 2026
#

int1 = int(input("Enter an integer: "))
int2 = int(input("Enter another integer: "))
sum = 0

for i in range(int1, int2 + 1): # needs to end at int2 + 1 since range is exclusive
    sum += i

print(f"The sum of all integers from {int1} to {int2} is", sum)