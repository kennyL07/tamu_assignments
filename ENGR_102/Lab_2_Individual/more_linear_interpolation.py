# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      519
# Assignment:   Lab Topic 2 (Individual)
# Date:         27 8 2026
#

t0 = 12
pos = (8, 6, 7)
t1 = 85
pos2 = (-5,30,9)

slope = ((pos2[0] - pos[0]) / (t1-t0), 
        (pos2[1] - pos[1]) / (t1-t0), 
        (pos2[2] - pos[2]) / (t1-t0))
def interpolate(slope, pos, t0, tx) -> tuple: # Substitue input with t
    return (slope[0] * (tx-t0) + pos[0], slope[1] * (tx-t0) + pos[1], slope[2] * (tx-t0) + pos[2])

tx = 30.0
fpos = interpolate(slope, pos, t0, tx)
print("At time", tx, "seconds:")
print("x1 =", fpos[0], "m")
print("y1 =", fpos[1], "m")
print("z1 =", fpos[2], "m")
print("-----------------------")

tx = 37.5
fpos = interpolate(slope, pos, t0, tx)

print("At time", tx, "seconds:")
print("x2 =", fpos[0], "m")
print("y2 =", fpos[1], "m")
print("z2 =", fpos[2], "m")
print("-----------------------")

tx = 45.0
fpos = interpolate(slope, pos, t0, tx)



print("At time", tx, "seconds:")
print("x3 =", fpos[0], "m")
print("y3 =", fpos[1], "m")
print("z3 =", fpos[2], "m")
print("-----------------------")

tx = 52.5
fpos = interpolate(slope, pos, t0, tx)



print("At time", tx, "seconds:")
print("x4 =", fpos[0], "m")
print("y4 =", fpos[1], "m")
print("z4 =", fpos[2], "m")
print("-----------------------")

tx = 60.0
fpos = interpolate(slope, pos, t0, tx)



print("At time", tx, "seconds:")
print("x5 =", fpos[0], "m")
print("y5 =", fpos[1], "m")
print("z5 =", fpos[2], "m")
print("-----------------------")