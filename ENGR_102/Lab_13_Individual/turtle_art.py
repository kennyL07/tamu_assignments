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


def parta(turnAngle: float):
    
    """ Draw a star with a radius of 300
    
    Args: 
        turnAngle (float): The exterior angle of the points in degrees.
    """
    
    turns = 1
    while (turnAngle * turns) % 360 != 0:
        turns += 1
    turtle.dot(10 , "red")
    print("Iterations:", turns, "Angle", turnAngle)
    for i in range(turns):
        turtle.left(turnAngle)
        turtle.forward(300)

def partb(sequence: str):
    """ Follow a sequence of binary to create a path

    Args:
        sequence (str): Sequence of binary data.
    """
    
    turtle.dot(10, "red")
    for i in sequence:
        match i: # Bored.
            case "0":
                turtle.left(30)
                turtle.forward(30)
            case "1":
                turtle.left(-114)
                turtle.forward(30)

def partc(sequence: str, zeroAngle: float, oneAngle: float):
    """ 
    Follow a sequence of binary data consisting of 1's
    followed by (n - 1) zeros where n is the number of 1's preceeding

    Args:
        sequence (str): sequence of binary
        zeroAngle (float): angle to turn on zeros in degrees.
        oneAngle (float): angle to turn on ones in degrees.
    """
    
    turtle.dot(10, "red")
    for i in sequence:
        match i:
            case "0":
                turtle.left(zeroAngle)
                turtle.forward(10)
            case "1":
                turtle.left(oneAngle)
                turtle.forward(10)

def reset():
    """My reset function. 
    Pauses the program by asking for an input. 
    Resets the turtle playground.
    Then sets the speed.
    """
    
    input()
    turtle.reset()
    turtle.speed(0)



# main code
turtle.speed(0)
parta(160)
reset()

parta(141)
reset()

partb("01001")
reset()

partb("01001011")
reset()

seq1 = ""  # create a spiral sequence with 20 ones
for i in range(20):
    seq1 += "1" + "0" * i
print(seq1)
partc(seq1, 0, 90)
reset()
partc(seq1, 0, 30)
reset()

seq2 = ""  # create a spiral sequence with 50 ones
for i in range(50):
    seq2 += "1" + "0" * i
print(seq2)
partc(seq2, 0, 150)
reset()
partc(seq2, 5, 108)
reset()

turtle.done()   # only need once (at the end) so the window doesn't close