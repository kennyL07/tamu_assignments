# By submitting this assignment, I agree to the following:
# "Aggies do not lie, cheat, or steal, or tolerate those who do."
# "I have not given or received any unauthorized aid on this assignment."
#
# Names: Kennyson Le
# Aissata Sidibe
# David Troyer
# Kingston Jackson
# Carter Cutright
# Section: 519
# Assignment: Lab Topic 2 (Team) Part 2
# Date: 27 8 2026
#

from math import pi

t0 = 10 # minutes
dist0 = 2030 # kilometers

t1 = 55 # minutes
dist1 = 23030 # kilometers
speed = (dist1 - dist0) / (t1 - t0)
def interpolate(tx) -> float:
    return (speed * (tx-t0) + dist0)

print("Part 1:")
print("For t = 25 minutes, the position p =", interpolate(25), "kilometers")


print("Part 2:")
print("For t = 300 minutes, the position p =", interpolate(300) % (6745 * pi * 2), "kilometers")