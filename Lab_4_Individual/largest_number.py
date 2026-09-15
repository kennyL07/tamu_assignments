# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   Lab 4 Individual
# Date:         10 9 2026
#

num1 = float(input("Enter number 1: "))
num2 = float(input("Enter number 2: "))
num3 = float(input("Enter number 3: "))

largest = -1e99
if num1 > largest: # Why not just use the built in max()
    largest = num1
if num2 > largest:
    largest = num2
if num3 > largest:
    largest = num3

print("The largest number is", largest)