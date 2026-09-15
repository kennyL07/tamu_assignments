# By submitting this assignment, I agree to the following:
# "Aggies do not lie, cheat, or steal, or tolerate those who do."
# "I have not given or received any unauthorized aid on this assignment."
#
# Names: Kennyson Le
# Adila Hansbhai
# Kingston Jackson
# Tevya Birnbaum
# Section: 519
# Assignment: Lab 3
# Date: 3 9 2026
#

num = float(input("Please enter the quantity to be converted: "))
print(f"{num:.2f} pounds force is equivalent to {num * 4.44822:.2f} newtons")
print(f"{num:.2f} meters is equivalent to {num * 3.28084:.2f} feet")
print(f"{num:.2f} atmospheres is equivalent to {num * 101.325:0.2f} kilopascals")
print(f"{num:.2f} watts is equivalent to {num * 3.412141633:.2f} BTU per hour")
print(f"{num:.2f} liters per second is equivalent to {num * 0.264172052 * 60:.2f} US gallons per minute") # Multiply by 60 again for seconds --> minutes
print(f"{num:.2f} degrees Celsius is equivalent to {(num * 1.8) + 32:.2f} degrees Fahrenheit")