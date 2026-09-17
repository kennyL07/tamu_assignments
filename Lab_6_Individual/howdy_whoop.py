# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   Lab 6
# Date:         DAY MONTH 2026
#

interger1 = int(input("Enter an integer: "))
interger2 = int(input("Enter another integer: "))

for i in range(1, 101):
    if i % interger1 == 0:
        print("Howdy")
        continue
    if i % interger2 == 0:
        print("Whoop")
        continue
    print(i)
