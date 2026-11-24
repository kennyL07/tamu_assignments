# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   Lab-13-i
# Date:         24 11 2026
#

import turtle

def parta(turnAngle: float) -> int:
    # If the turn angle is less than 90, it is an interior angle
    if turnAngle <= 90:
        interiorAngle = turnAngle
    else:
        interiorAngle = abs(180 - turnAngle) * 2
    turns = 1
    while interiorAngle * turns % 360 != 0:
        turns += 1
    return int(turns)

def partb(sequence: str) -> None:
    turtle.dot(10, "red")
    for i in sequence:
        if i == "0":
            turtle.left(30)
            turtle.forward(30)
        if i == "1":
            turtle.left(-114)
            turtle.forward(30)
    turtle.done()
