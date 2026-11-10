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
# Date: 5 11 2026
#

# part i
# As a team, we have gone through all required sections of the 
# tutorial, and each team member understands the material

from numpy import arange, reshape, transpose, sqrt
A = arange(12).reshape(3, 4)
B = arange(8).reshape(4, 2)
C = arange(6).reshape(2, 3)

# part ii
print(A, "\n")
print(B, "\n")
print(C, "\n")

# part iii
D = A @ B @ C
print(D, "\n")

# part iv
D = transpose(D)
print("D^T =", D, "\n")

# part v
e = (sqrt(D))/2
print("E =", e, "\n")