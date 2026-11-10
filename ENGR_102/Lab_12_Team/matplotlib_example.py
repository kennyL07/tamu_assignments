# By submitting this assignment, I agree to the following:
# "Aggies do not lie, cheat, or steal, or tolerate those who do."
# "I have not given or received any unauthorized aid on this assignment."
#
# Names: Kennyson Le
# Adila Hansbhai
# Kingston Jackson
# Tevya Birnbaum
# Section: 567
# Assignment: Lab 12 Team
# Date: 10 11 2026
#
# As a team, we have gone through all required sections of the
# tutorial, and each team member understands the material

import numpy as np
from matplotlib import pyplot as plt

# question 1
x = np.linspace(-2, 2, 100)  # Sample data.
f = 2
plt.figure(figsize=(5, 2.7), layout='constrained')
plt.plot(x, (1 / (4*f))* x**2, lw=f, color='red')
f = 6
plt.plot(x, (1 / (4*f))* x**2, lw=f, color='purple')
plt.xlabel('X Values')
plt.ylabel('Y Values')
plt.title('Parabola plots with varying focal lengths') # graph title

# question 2
x = np.linspace(-4, 4,100)
plt.figure(figsize=(2, 2))
plt.plot(x,(2*x**3 + 3*x**2 - 11*x - 6), marker = '*', color='orange') # each point will be a star for funsies
plt.xlabel('X Values')
plt.ylabel('Y Values')
plt.title('Plot of cubic polynomial') # graph title
plt.show()

# question 3
# graphing cos and sin
from math import pi, sin, cos

fig, axs = plt.subplots(2, 1, figsize=(5, 2.7), layout='constrained')
x = np.linspace(-2 * pi, 2 * pi)
y1 = [sin(i) for i in x ]
y2 = [cos(i) for i in x]

axs[0].plot(x, y1, color = "green")
axs[0].grid(True)
axs[0].set_title("Plot of sin(x)")
axs[1].plot(x, y2, color = "brown")
axs[1].set_title("Plot of cos(x)")
axs[1].grid(True)
plt.show()
