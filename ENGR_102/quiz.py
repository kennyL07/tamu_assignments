# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   Module 12 Quiz
# Date:         10 11 2026
#

import numpy as np
letters = "abcdefghijklmnopqrstuvwxyz"
message = "uzijaktocji"

file = open("module12quizF26.txt")
nums = file.readlines()

for i in range(len(nums)):
    nums[i] = nums[i].strip()

matrix = np.reshape(nums, (100, 100))
a = (sum([int(j) for j in matrix[73][0:5]]) / 5)
b = min([int(j) for j in matrix[7][0:5]])
c = max([int(j) for j in matrix[60][-5:]])
d = sum([int(j) for j in matrix[18][:3]])
e = min([int(j) for j in matrix[51][-3:]])
print(matrix)
# print(a,b,c,d,e)
shift = int(a - b + c - d + e) - 1
shifted = letters[shift:] + letters[:shift]

answer = ""
for m in range(len(message)):
    index = letters.index(message[m])
    answer += shifted[index]
print(answer)