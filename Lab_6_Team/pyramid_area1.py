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

sum = 0
for i in range(1, layers + 1):
    sum += (i * length**2) * 4 # Side faces
    sum += i**2 * length**2 # Top face
    # sum -= length**2 * (i-1) # Num of squares on bottom squared * length of each square
    # print(sum)
for i in range(1, layers):
    sum -= length**2 * i**2
    
print(f"You need {sum:0.2f} m^2 of gold foil to cover the pyramid")