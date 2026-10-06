# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le
# Section:      567
# Assignment:   Lab 7 Individiual
# Date:         6 10 2026
#

name = input("What is your name? ")

vowels = "aeiouyAEIOUY" # Y is considered a vowel
new_name = name
if name[0] in vowels:
    new_name = name[0].lower() + name[1:]
else:
    i = 0
    while(not (new_name[0] in vowels)):
        i += 1
        new_name = name[i:]

print(f"{name}, {name}, Bo-B{new_name}")
print(f"Banana-Fana Fo-F{new_name}")
print(f"Me Mi Mo-M{new_name}")
print(f"{name}!")
