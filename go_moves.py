# By submitting this assignment, I agree to the following:
# "Aggies do not lie, cheat, or steal, or tolerate those who do."
# "I have not given or received any unauthorized aid on this assignment."
#
# Names: Kennyson Le
# Adila Hansbhai
# Kingston Jackson
# Tevya Birnbaum
# Section: 567
# Assignment: Lab 3
# Date: 1 10 2026
#

# First make the matrix (list of lists) for the blank starting board 
board = []
for i in range(9):
    row = []
    for j in range(9):
        row.append(".")
    board.append(row)

def printBoard():
    for i in range(len(board)):
        for j in range(len(board)):
            print(board[i][j], end='')
        print()

# Use a variable to keep track of white/black turns
turn = 0
userInput = ''
x = ''
y = ''
piece = ''
# While input isn’t stop:
# Compare variable to determine turn
# Ask user to place a stone on the board (black first)
# Check if board coordinate is valid
# Check if board is empty / contains “.’
# Replace cell with stone type
# Flip turns

while (turn != 80 and x != 'stop' or y != 'stop'):
    if turn % 2 == 0:
        print('Black:')
    else:
        print('White:')
    x = int(input("Enter the X coordinate from 1-9:"))
    y = int(input("Enter the Y coordinate from 1-9:"))
    if turn % 2 == 0:
        piece = chr(9679) 
    else: 
        piece = chr(9675)  # displays filled circle: ●  player 1 ;  displays empty circle: ○ player 2
    if board[x][y] != '.':
        print("Please Enter a valid coordinate")
        continue
    board[x][y] = piece
    printBoard()



# Print “game over” once the board is completely full
print("Game over!")