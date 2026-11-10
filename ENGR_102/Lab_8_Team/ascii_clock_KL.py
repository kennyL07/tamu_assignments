# By submitting this assignment, I agree to the following:
# "Aggies do not lie, cheat, or steal, or tolerate those who do."
# "I have not given or received any unauthorized aid on this assignment."
#
# Names: Kennyson Le
# Adila Hansbhai
# Kingston Jackson
# Tevya Birnbaum
# Section: 567
# Assignment: Lab 8 Team
# Date: 10 17 2026
#

#assumed variables from previous code
ascii_dict = {"a":["","",""],"1":["","",""]} # dictionary of lists of strings correlating to characters
time = "" # String of the user's time
isAM = False
is12 = False
preferredCharacter = ""

output = ["","","","",""] # Each row to print
for i in range(len(output)):
    for j in range(len(time)):
        if preferredCharacter:
            output[i] += ascii_dict [time[j]][i].replace("*", preferredCharacter) # this assumes that the item: colon exists
        else:
            output[i] += ascii_dict [time[j]][i].replace("*", time[j])
        output[i] += ascii_dict[" "][i]
    if is12:
        if isAM:
            output[i] += ascii_dict["a"][i]
        else:
            output[i] += ascii_dict["p"][i]
        output[i] += ascii_dict[" "][i] # [" ", " ", " ", " ", " "]
        output[i] += ascii_dict["m"][i]