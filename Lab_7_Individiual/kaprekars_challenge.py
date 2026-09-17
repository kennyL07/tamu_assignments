# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   Lab 7
# Date:         DAY MONTH 2026
#

totalIterations = 0

for i in range(10000):
    result = int(i)
    iterations = 0
    if len(set(int(x) for x in str(result))) <= 1:
        continue
    while (result != 6174):
        number1 = [int(x) for x in str(result)]
        number2 = [int(x) for x in str(result)]
        while len(number1) != 4:
            number1.insert(0, 0)
        number1.sort(reverse=True)
        number2.sort(reverse=False)
        result = int("".join([str(x) for x in number1])) - int("".join([str(x) for x in number2]))
        iterations += 1
    print(iterations)
    totalIterations += iterations

print(f"Kaprekar's routine takes {totalIterations} total iterations for all four-digit numbers")