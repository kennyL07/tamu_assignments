# By submitting this assignment, I agree to the following:
# "Aggies do not lie, cheat, or steal, or tolerate those who do."
# "I have not given or received any unauthorized aid on this assignment."
#
# Names: Kennyson Le
# Adila Hansbhai
# Kingston Jackson
# Tevya Birnbaum
# Section: 567
# Assignment: Lab Topic 4 (team)
# Date: 10 SEPTEMBER 2026
#

cases = ["T", "t", "True"]
############ Part A ############ 
a = input("Enter True or False for a: ")
a = a in cases 
b = input("Enter True or False for b: ")
b = b in cases
c = input("Enter True or False for c: ")
c = c in cases

############ Part B ############ 
print("a and b and c:", bool(a and b and c))
print("a or b or c:", bool(a or b or c))

############ Part C ############ 
print("XOR:", bool(a or b) and not(a and b))
print("Odd number:", bool((a and not b and not c) or (b and not a and not c) or (c and not a and not b) or (a and b and c)))

############ Part D ############ 
