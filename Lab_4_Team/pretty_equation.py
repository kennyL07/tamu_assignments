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

import math
#user defines coefficients
coef_a = int(input("Please enter the coefficient A: "))
coef_b = int(input("Please enter the coefficient B: "))
coef_c = int(input("Please enter the coefficient C: "))

#make the equation pretty
if(coef_a == 1):
    pretty_a = "x^2" 
elif(coef_a > 0):
    pretty_a = str(coef_a)+"x^2"
elif(coef_a == 0):
    pretty_a = ""
elif(coef_a == -1):
    pretty_a = "- x^2"
elif(coef_a < 0):
    pretty_a = "- " + str(abs(coef_a))+"x^2"

if(coef_b == 1):
    if pretty_a:
        pretty_a += " + "
    pretty_b = "x" 
elif(coef_b > 0):
    if pretty_a:
        pretty_a += " + "
    pretty_b = str(coef_b)+"x"
elif(coef_b == 0):
    pretty_b = ""
elif(coef_b == -1):
    if pretty_a:
        pretty_a += " - "
    pretty_b = "x"
elif(coef_b < 0):
    pretty_b = str(abs(coef_b))+"x"
    if pretty_a:
        pretty_a +=  " - "
    else:
        pretty_b = " - " + pretty_b

if(coef_c > 0):
    pretty_c = " + " + str(coef_c)
elif(coef_c == 0):
    pretty_c = ""
elif(coef_c < 0):
    pretty_c = " - " + str(abs(coef_c))

print("The quadratic equation is " + pretty_a + pretty_b + pretty_c + " = 0")