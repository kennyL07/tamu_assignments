# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   Lab 8 Team
# Date:         15 10 2026
#

# Get User inputs
time = input("Enter the time: ")
# Split User inputs into hours, minutes
time_hour = int(time.split(':')[0])
time_minute = int(time.split(':')[1])
# Determine 12 or 24.
is12 = input("Choose the clock type (12 or 24): ") == "12"
isAm = not(is12 and time_hour >= 12)
    # If 12, determine AM or PM
if time_hour < 1 and time_hour > 24 and time_minute > 60 and time_minute < 0:
    print("Not eligiable")
if is12:
    if time_hour > 12:
        time_hour = time_hour-12
    if time_hour == 0:
        time_hour = 12
# Get preferred character and check eligibility
preferredCharacter = input("Enter your preferred character: ")
while(preferredCharacter and not preferredCharacter in "abcdeghkmnopqrsuvwxyz@$&*="): 
    preferredCharacter = input("Character not permitted! Try again: ") # have the user try again if their input is not in the list of valid characters
print()

#Ascii dictionary with every character as a 5 height ascii character
ascii_dict = {
    '0': [
        "***",
        "* *",
        "* *",
        "* *",
        "***"
    ],
    '1': [
        " * ",
        "** ",
        " * ",
        " * ",
        "***"
    ],
    '2': [
        "***",
        "  *",
        "***",
        "*  ",
        "***"
    ],
    '3': [
        "***",
        "  *",
        "***",
        "  *",
        "***"
    ],
    '4': [
        "* *",
        "* *",
        "***",
        "  *",
        "  *"
    ],
    '5': [
        "***",
        "*  ",
        "***",
        "  *",
        "***"
    ],
    '6': [
        "***",
        "*  ",
        "***",
        "* *",
        "***"
    ],
    '7': [
        "***",
        "  *",
        "  *",
        "  *",
        "  *"
    ],
    '8': [
        "***",
        "* *",
        "***",
        "* *",
        "***"
    ],
    '9': [
        "***",
        "* *",
        "***",
        "  *",
        "***"
    ],
    ':': [
        " ",
        ":",
        " ",
        ":",
        " "
    ],
    'A': [
        " A ",
        "A A",
        "AAA",
        "A A",
        "A A"
    ],
    'P': [
        "PPP",
        "P P",
        "PPP",
        "P  ",
        "P  "
    ],
    'M': [
        "M   M",
        "MM MM",
        "M M M",
        "M   M",
        "M   M"
    ],
    'whitespace': [
        " ",
        " ",
        " ",
        " ",
        " "
    ]
}

if preferredCharacter:
    for i in ascii_dict:
        ascii_dict[i] = [x.replace("*",preferredCharacter) for x in ascii_dict[i]] # If prefered character exists change dictionary entries to use prefered character
else:
    for i in range(10):
        ascii_dict[str(i)] = [x.replace("*",str(i)) for x in ascii_dict[str(i)]] # else replace dictionary with numbers for entry


# All ascii items have a height of 5
prin1 = ""
prin2 = ""
prin3 = ""
prin4 = ""
prin5 = ""

for k in str(time_hour):
    prin1 += ascii_dict[k][0]
    prin1 += " "
    prin2 += ascii_dict[k][1]
    prin2 += " "
    prin3 += ascii_dict[k][2]
    prin3 += " "
    prin4 += ascii_dict[k][3]
    prin4 += " "
    prin5 += ascii_dict[k][4]
    prin5 += " "

prin1 += "  "
prin2 += ": "
prin3 += "  "
prin4 += ": "
prin5 += "  "

if time_minute < 10:
    time_minute = "0" + str(time_minute)
else:
    time_minute = str(time_minute)
prin1 += ascii_dict[time_minute[0]][0]
prin2 += ascii_dict[time_minute[0]][1]
prin3 += ascii_dict[time_minute[0]][2]
prin4 += ascii_dict[time_minute[0]][3]
prin5 += ascii_dict[time_minute[0]][4]
prin1 += " "
prin2 += " "
prin3 += " "
prin4 += " "
prin5 += " "
prin1 += ascii_dict[time_minute[1]][0]
prin2 += ascii_dict[time_minute[1]][1]
prin3 += ascii_dict[time_minute[1]][2]
prin4 += ascii_dict[time_minute[1]][3]
prin5 += ascii_dict[time_minute[1]][4]

if is12:
    prin1 += " " # Spacing only exists for 12 hour format
    prin2 += " "
    prin3 += " "
    prin4 += " "
    prin5 += " "
    if isAm:
        prin1 += ascii_dict["A"][0]
        prin1 += " "
        prin2 += ascii_dict["A"][1]
        prin2 += " "
        prin3 += ascii_dict["A"][2]
        prin3 += " "
        prin4 += ascii_dict["A"][3]
        prin4 += " "
        prin5 += ascii_dict["A"][4]
        prin5 += " "
    else:
        prin1 += ascii_dict["P"][0]
        prin1 += " "
        prin2 += ascii_dict["P"][1]
        prin2 += " "
        prin3 += ascii_dict["P"][2]
        prin3 += " "
        prin4 += ascii_dict["P"][3]
        prin4 += " "
        prin5 += ascii_dict["P"][4]
        prin5 += " "

    prin1 += ascii_dict["M"][0]
    prin2 += ascii_dict["M"][1]
    prin3 += ascii_dict["M"][2]
    prin4 += ascii_dict["M"][3]
    prin5 += ascii_dict["M"][4]

# Finally print all rows
print(prin1)
print(prin2)
print(prin3)
print(prin4)
print(prin5)