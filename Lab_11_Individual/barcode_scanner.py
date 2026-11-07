# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   Lab 11 Individual
# Date:         6 11 2026
#

barcodeFile = input("Enter the name of the file:")
validCodesFile = 
totalValid = 0

with open(barcodeFile, "r") as codes:
    lines = codes.readlines()
    for code in lines:
        code = list(code.strip())
        group1 = code[:12:2]
        group2 = code[1:12:2]
        group1Nums = [int(a) for a in group1]
        group2Nums = [int(b) for b in group2]
        if 10 - int(str(sum(group2Nums) * 3 + sum(group1Nums))[-1]) == int(code[-1]):
            totalValid += 1
