# By submitting this assignment, I agree to the following:
# "Aggies do not lie, cheat, or steal, or tolerate those who do."
# "I have not given or received any unauthorized aid on this assignment."
#
# Names: Kennyson Le
# Adila Hansbhai
# Kingston Jackson
# Tevya Birnbaum
# Section: 567
# Assignment: Lab 6
# Date: 24 9 2026
#

# store user inputs as "length" for the side length and "layers" for the number of layers in the pyramid
length = float(input("Enter the side length in meters: "))
layers = int(input("Enter the number of layers: "))

sum = 1

i = (layers * (layers + 1) * (layers * 2 + 1)) / 6 # Sum of n^2 
j = (layers - 1) * ((layers ) * ((layers * 2 - 1))) / 6
k = (layers * (layers + 1)) / 2

sum = (4 * length**2 * k) + length**2 * i + - length**2 * j 

print(f"You need {sum:.2f} m^2 of gold foil to cover the pyramid")