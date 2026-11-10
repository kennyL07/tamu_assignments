# By submitting this assignment, I agree to the following:
# "Aggies do not lie, cheat, or steal, or tolerate those who do."
# "I have not given or received any unauthorized aid on this assignment."
#
# Names: Kennyson Le
# Adila Hansbhai
# Kingston Jackson
# Tevya Birnbaum
# Section: 567
# Assignment: Lab 3
# Date: 3 9 2026
#

t0 = float(input("Enter time 1: "))
x0 = float(input("Enter the x position of the object at time 1: "))
y0 = float(input("Enter the y position of the object at time 1: "))
z0 = float(input("Enter the z position of the object at time 1: "))

t1 = float(input("Enter time 2: "))
x1 = float(input("Enter the x position of the object at time 2: "))
y1 = float(input("Enter the y position of the object at time 2: "))
z1 = float(input("Enter the z position of the object at time 2: "))
print()

pos0 = (x0, y0, z0) # Storing values as tuples
pos1 = (x1, y1, z1)

slope = ((pos1[0] - pos0[0]) / (t1-t0), 
        (pos1[1] - pos0[1]) / (t1-t0), 
        (pos1[2] - pos0[2]) / (t1-t0)) # Maybe using an array is better

def interpolate(slope, pos0, t0, tx) -> tuple:
    return (slope[0] * (tx-t0) + pos0[0], slope[1] * (tx-t0) + pos0[1], slope[2] * (tx-t0) + pos0[2])

for i in range(0, 5):
    tx = t0 + (t1 - t0) * i * .25
    point = interpolate(slope, pos0, t0, tx)
    print(f"At time {tx:.2f} seconds the object is at ({point[0]:.3f}, {point[1]:.3f}, {point[2]:.3f})", end="\n")  