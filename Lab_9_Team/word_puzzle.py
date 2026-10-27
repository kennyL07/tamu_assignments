# By submitting this assignment, I agree to the following:
# "Aggies do not lie, cheat, or steal, or tolerate those who do."
# "I have not given or received any unauthorized aid on this assignment."
#
# Names: Kennyson Le
# Adila Hansbhai
# Kingston Jackson
# Tevya Birnbaum
# Section: 567
# Assignment: Lab 9 Team
# Date: 20 10 2026
#



def get_valid_letters(puzzle):
    """
    Takes a string representing a puzzle and returns a string with 10 unique letters found in the puzzle.
    """
    unique_letters = "" # creating a blank string to add 10 unique letters to it
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in puzzle:
        if i not in unique_letters and i in letters: # checking if letter is already in string and checking if character in puzzle is actually a letter
            unique_letters += i       # adds letter to string if is not already in unique_string
        if len(unique_letters) == 10: # ends loop once unique_string is 10 letters long
            break
    return unique_letters

def is_valid_guess(unique_letters, guess):
    """
    Takes unique_string from the first function and compares it with a user guess called guess, returning a true value if the user's guess matches unique_string.
    """
    letters = []
    if len(guess) != 10:
        return False
    for i in guess:
        if not i in unique_letters:
            return False
        if i in letters:
            return False
        else:
            letters.append(i)
    return True

def check_user_guess(dividend, quotient, divisor, remainder) -> bool:
    return dividend == quotient * divisor + remainder

def make_number(word, key):
    dict = {}
    for num in range(len(key)): # TAKEOURSIM
        dict[key[num]] = num

    for letter in word:
        #convert word to numbers (loop through word and grab val thats a num from dict for each index then replace val in word for num (.replace))
        num = dict[letter]
        word = word.replace(letter, str(num))
        #return numbers
    return int(word) # "RUE" #TAKEOURSIM"

def make_numbers(puzzle_string, guess):
    parts = puzzle_string.split(" ")
    dividend = parts[2].split(",")[0]
    quotient = parts[0].split(",")[0]
    divisor = parts[0].split(",")[1]
    remainder = parts[-1].split(",")[-1]
    output = []
    for i in (dividend, quotient, divisor, remainder):
        output.append(make_number(i, guess))
    return (output[0], output[1], output[2], output[3]) # Dividend, Quotient, Divisor, Remainder

def print_puzzle(puzzle):
    """ Print puzzle as a long division problem. """
    puzzle = puzzle.split(",")
    for i in range(len(puzzle)):
        if i == 1:
            print(f"{len(puzzle[i].split('|')[1]) * '_': >16}")
        print(f"{puzzle[i]: >16}")
        if i > 1 and i % 2 == 0:
            print(f"{'-'*len(puzzle[i]): >16}")

def main():
    # The lines below demonstrate what the print_puzzle function outputs.
    
    # puzzle = "RUE,EAR | RUMORS,UEII  ,UKTR ,EAR ,KEOS,KAIK,USA"
    puzzle = input("Enter a word arithmetic puzzle: ")
    print()
    print_puzzle(puzzle)
    valid_letters = get_valid_letters(puzzle)
    print()
    user_input = input(f"Enter your guess, for example ABCDEFGHIJ: ")
    if not is_valid_guess(valid_letters, user_input):
        print("Your guess should contain exactly 10 unique letters used in the puzzle.")
        exit()
    dividend, quotient, divisor, remainder = make_numbers(puzzle, user_input)
    if check_user_guess(dividend, quotient, divisor, remainder):
        print("Good job!")
    else:
        print("Try again!")
        

if __name__ == "__main__":
    main()