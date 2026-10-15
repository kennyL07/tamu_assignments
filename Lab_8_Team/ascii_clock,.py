#assumed variables from previous code
characters = {"a":["","",""],"1":["","",""]} # dictionary of lists of strings correlating to characters
time = "" # String of the user's time
isAM = False 
is12 = False
preferredCharacter = ""

output = ["","","","",""] # Each row to print
for i in range(len(output)):
    for j in range(len(time)):
        if preferredCharacter:
            output[i] += characters[time[j]][i].replace("*", preferredCharacter) # this assumes that the item: colon exists
        else: 
            output[i] += characters[time[j]][i].replace("*", time[j])
        output[i] += characters[" "][i]
    if is12:
        if isAM:
            output[i] += characters["a"][i]
        else:
            output[i] += characters["p"][i]
        output[i] += characters[" "][i] # [" ", " ", " ", " ", " "]
        output[i] += characters["m"][i]