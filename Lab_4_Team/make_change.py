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
payment = float(input("How much did you pay? "))
cost = float(input("How much did it cost? "))
change = payment - cost
print(f"You received ${change:.2f} in change. That is...")

# Coins
penny = .01
nickel = .05
dime = .10
quarter = .25

if not (change // quarter == 0):
    if (change // quarter > 1):
        print(f"{int(change // quarter)} quarters")
    else: 
        print(f"{int(change // quarter)} quarter")
    change %= quarter
    change = round(change, 2)

if not (change // dime == 0):
    if (change // dime > 1):
        print(f"{int(change // dime)} dimes")
    else: 
        print(f"{int(change // dime)} dime")
    change %= dime
    change = round(change, 2)

if not (change // nickel == 0):
    if (change // nickel > 1):
        print(f"{int(change // nickel)} nickels")
    else: 
        print(f"{int(change // nickel)} nickel")
    change %= nickel
    change = round(change, 2)
if not (change == 0):
    if round(change * 100) == 1:
        print(f"{round(change * 100)} penny")
    else:
        print(f"{round(change * 100)} pennies")
    