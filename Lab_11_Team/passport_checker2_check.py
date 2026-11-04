# By submitting this assignment, I agree to the following:
# "Aggies do not lie, cheat, or steal, or tolerate those who do."
# "I have not given or received any unauthorized aid on this assignment."
#
# Names: Kennyson Le
# Adila Hansbhai
# Kingston Jackson
# Tevya Birnbaum
# Section: 567
# Assignment: Lab 11 Team
# Date: 03 11 2026
#

filename = input("Enter the name of the file: ")
count = 0
fullPassportEntry = ""
rawPassportEntries = []
passDict = {}
keys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "cid"]  # pid is optional
yearRanges = {"byr": (1922, 2010), "iyr": (2016, 2026), "eyr": (2026, 2036)}
eyeColors = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
validPassports = open("valid_passports2.txt", "w")

with open(filename, "r") as file:
    lines = file.readlines()
lines.append("\n")   # extra blank line so the LAST passport goes through the loop too

for line in lines:
    if line.strip() == "":
        data = fullPassportEntry.split()
        valid = True
        for item in data:
            parts = item.split(":", 1)
            if len(parts) == 2:
                passDict[parts[0]] = parts[1]

        # 1) every required field must exist
        for key in keys:
            if key not in passDict:
                valid = False

        # 2) only look at the values once we know they all exist
        if valid:
            # byr, iyr, eyr: exactly four digits, inside the range
            for key in yearRanges:
                value = passDict[key]
                if len(value) != 4 or value.strip("0123456789") != "":
                    valid = False
                elif not (yearRanges[key][0] <= int(value) <= yearRanges[key][1]):
                    valid = False

            # hgt: digits followed by cm or in (anything else is invalid)
            hgt = passDict["hgt"]
            number = hgt[:-2]
            if number == "" or number.strip("0123456789") != "":
                valid = False
            elif hgt.endswith("cm"):
                if not (150 <= int(number) <= 193):
                    valid = False
            elif hgt.endswith("in"):
                if not (59 <= int(number) <= 76):
                    valid = False
            else:
                valid = False

            # hcl: '#' then exactly 6 characters from 0-9 / a-f
            hcl = passDict["hcl"]
            if len(hcl) != 7 or hcl[0] != "#" or hcl[1:].strip("0123456789abcdef") != "":
                valid = False

            # ecl: one of the allowed colors
            if passDict["ecl"] not in eyeColors:
                valid = False

            # cid: three digits, no leading zero
            cid = passDict["cid"]
            if len(cid) != 3 or cid.strip("0123456789") != "" or cid[0] == "0":
                valid = False

        if valid:
            if count > 0:
                validPassports.write("\n")      # blank line BETWEEN passports only
            count += 1
            for i in rawPassportEntries:
                validPassports.write(i.rstrip("\r\n") + "\n")

        fullPassportEntry = ""
        rawPassportEntries = []
        passDict = {}
    else:
        fullPassportEntry += line.strip() + " "
        rawPassportEntries.append(line)

validPassports.close()
# output number of valid passports
print(f"There are {count} valid passports")