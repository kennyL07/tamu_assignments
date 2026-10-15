# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   Lab 8 Individual
# Date:         15 10 2026
#

# a > @, b > 8, e > 3, o > 0, s > $, t > 7

leetdict = {
    "a": "@",
    "b" : "8",
    "e": "3",
    "o": "0",
    "s": "$",
    "t": "7"
}

def converToLeetspeak(text):
    output = ""
    for i in text:
        if i in leetdict:
            output += leetdict[i]
        else:
            output += i
    return output

someText = input("Enter some text: ")
print(f'In leet speak, "{someText}" is:')
print(converToLeetspeak(someText))

