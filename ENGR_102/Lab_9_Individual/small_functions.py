# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   Lab_9 Individual
# Date:         15 10 2026
#

nums = [30, 125, 225, 1125, 2025, 3025, 4025, 5025, 6025, 7025, 8025, 9025, 2000]

from math import cos, asin, pi, sqrt

def parta(nums):
    nums.sort() # Sorting to get median
    median = 0
    if len(nums) % 2 == 0:
        median = (nums[int(len(nums)/2 + 0.5)] + nums[int(len(nums)/2 - 0.5)]) / 2
    else:
        median = nums[int(len(nums)/2 - 0.5)]
    return (nums[0], (median), nums[-1]) # could do min() and max() instead

def partb(time, dist):
    velocities = []
    for i in range(1, len(time)):
        velocities.append((dist[i] - dist[i-1]) / (time[i] - time[i-1])) # rise over run
    return velocities

def partc(nums):
    for i in range(len(nums)):
        for j in range(len(nums[1:])): # Somehow this works even though when i > 1, you check i twice
            if nums[i] + nums[j] == 2030:
                return nums[i] * nums[j]
    return False

def partd(num):
    numbers = [x for x in range(2, num + 1, 2)] # get even numbers
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if sum(numbers[j:i]) == num:
                return(numbers[j:i])
    return False

def parte(sphereR, holeR):
    h = 2 * sqrt(sphereR**2 - holeR**2) # Using 2 x (Area formula with a and h)
    return (pi * h**3) / 6

def partf(border, name, business, email):
    length = max(len(border) , len(name), len(business), len(email)) + 4
    
    output = []
    output.append(border * (length + 2)) # Use string multiplication instead of for loop
    output.append(border + name.center(length) + border) # found a new method (center) from python docs
    output.append(border + business.center(length) + border)
    output.append(border + email.center(length) + border)
    output.append(border * (length + 2))

    return "\n".join(output)

def partg(x, tolerance):
    total = 0
    n = 1
    while True:
        term = (2 / (2*n - 1)) * x**(2*n - 1) # Calculating each term
        if abs(term) < tolerance: 
            break
        total += term # Summation
        n += 1
    return total

print(partf("*", "Dr. Ritchey", "Texas A&M University", "snritchey@tamu.edu"))