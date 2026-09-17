# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   Lab 7
# Date:         DAY MONTH 2026
#

n = input("Enter a four-digit integer: ")

result = int(n)
steps = "" + n
iterations = 0
while (result != 6174):
    number1 = [int(x) for x in str(result)]
    number2 = [int(x) for x in str(result)]
    iterations += 1
    while len(number1) != 4:
        number1.insert(0, 0)
    number1.sort(reverse=True)
    number2.sort(reverse=False)
    result = int("".join([str(x) for x in number1])) - int("".join([str(x) for x in number2]))
    steps = steps + " > " + str(result)
    iterations += 1
print(steps)
print(f"{n} reaches 6174 via Kaprekar's routine in {iterations} iterations")
