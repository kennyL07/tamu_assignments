# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   Lab 4 Individual
# Date:         10 9 2026
#

numOfDays = int(input("Please enter a positive value for day: "))
if (numOfDays < 0):
    print("You entered an invalid number!")
    exit()
if (numOfDays < 11): # From 0-10
    print(f"The sum total number of gadgets produced on day {numOfDays} is {numOfDays * 10}")
elif (numOfDays < 51): #From 11-49
    sum = 100 + (numOfDays - 10) * (11 + (numOfDays)) // 2
    print(f"The sum total number of gadgets produced on day {numOfDays} is {int(sum)}")
else: # 50+
    days = min(100, numOfDays)
    sum = 1320 + 50 * (days-50)
    print(f"The sum total number of gadgets produced on day {numOfDays} is {int(sum)}")