# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le
# Section:      567
# Assignment:   Lab 7 Individual
# Date:         DAY MONTH 2026
#

nums = input("Enter numbers: ")  # What if they use a different delimiter?
nums = [int(x) for x in nums.split()]
total = 0
for i in nums:
    total += i

leftSum = 0
for i in range(len(nums)):
    leftSum += nums[i]
    rightSum = total - leftSum

    if leftSum == rightSum:
        leftSub = nums[:i+1]
        rightSub = nums[i+1:]

        print(f"Left: {leftSub}")
        print(f"Right: {rightSub}")
        print(f"Both sum to {leftSum}")
        exit()
print("Cannot split evenly")
