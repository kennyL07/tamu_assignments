# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   Lab 12
# Date:         12 11 2026
#

import numpy as np
import matplotlib.pyplot as plt

x = 0
y = 1
point = np.array([[x],[y]])
matrix = np.array([[1.02, 0.095],[-0.095, 1.02]])

xPoints = []
yPoints = []

for i in range(250):
    point = np.dot(matrix, point)
    xPoints.append(point[0][0])
    yPoints.append(point[1][0])
plt.plot(xPoints, yPoints, color="red")
plt.title("Swirl")
plt.xlabel("X Axis")
plt.ylabel("Y Axis")
plt.show()