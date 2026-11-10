# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      519
# Assignment:   Lab Topic 2 (Individual)
# Date:         27 8 2026
#

z = 0
x = 1
z += x
print(z)

x = 1
y = 10
z = 0
x += 1
x += 1
y *= x
z += y
print(z)

x = 1
y = 10
z = 0
z += x
z += x # z = 2
y = 10
x = y
y *= x # y = 100
z += y
print(z)

x = 1
y = 10
z = 0
x = y
y *= x
y *= x
y *= x
y *= x
y *= x
y *= x
y *= x
y *= x
y *= x
y *= x
y *= x
y *= x
y *= x
y *= x
y *= x
z += y
print(z)

x = 1
y = 10
z = 0
x = y
y *= x
y *= x # y = 1000
x = 1
x += 1
y *= x
y *= x # 4000
z += y
z += y # z = 8000
y = 10
x = y
y *= x # 100
x = 1
x += 1
y *= x # 200
z += y
z += y
z += y
x += 1
x += 1
x += 1
z += x
y = 10
x += 1
x += 1
y *= x
z += y
print(z)