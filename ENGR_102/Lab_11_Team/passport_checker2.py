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
keys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "cid"]
validPassports = open("valid_passports2.txt", "w")

with open(filename, "r") as file:
    lines = file.readlines()
    lines.append("\n")
    
    for line in lines:
        if line.strip() == "":
            # byr – Birth year – four digits, between 1922 and 2010, inclusive
            # iyr – Issue year – four digits, between 2016 and 2026, inclusive
            # eyr – Expiration year – four digits, between 2026 and 2036, inclusive
            # hgt – Height – a number followed by either cm or in
            # If cm, the number must be between 150 and 193, inclusive
            # If in, the number must be between 59 and 76, inclusive
            # hcl – Hair color – a # followed by exactly 6 characters (0-9 or a-f)
            # ecl – Eye color – exactly one of the following: amb, blu, brn, gry, grn, hzl, oth
            # pid – Passport ID – not required
            # cid – Country ID – a three-digit number, NOT including leading zeroes
            
            data = fullPassportEntry.strip().split()
            keys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "cid"]
            valid = True
            
            for i in data:
                key, value = i.split(":")
                passDict[key] = value
            
            for key in keys:
                if key not in passDict:
                    valid = False

            if valid:
                if passDict["byr"]:
                    if not (1922 <= int(passDict["byr"]) <= 2010) or len(passDict["byr"]) != 4 or passDict["byr"].strip("0123456789") != "":
                        valid = False
                if passDict["iyr"]:
                    if not (2016 <= int(passDict["iyr"]) <= 2026) or len(passDict["iyr"]) != 4 or passDict["iyr"].strip("0123456789") != "":
                        valid = False
                if passDict["eyr"]:
                    if not (2026 <= int(passDict["eyr"]) <= 2036) or len(passDict["eyr"]) != 4 or passDict["eyr"].strip("0123456789") != "":
                        valid = False
                        
                if passDict["hgt"]:
                    height = passDict["hgt"][:-2]
                    if height == "" or height.strip("0123456789") != "": # Use strip instead of checking each individual character in a loop
                        valid = False
                    elif passDict["hgt"].endswith("cm"):
                        if not (150 <= int(height) <= 193):
                            valid = False
                    elif passDict["hgt"].endswith("in"):
                        if not (59 <= int(height) <= 76):
                            valid = False
                    else:
                        valid = False

                if passDict["hcl"]:
                    if not passDict["hcl"].startswith("#") or len(passDict["hcl"]) != 7 or passDict["hcl"][1:].strip("0123456789abcdef") != "":
                        # for i in passDict["hcl"][1:]:
                        #     if i not in "0123456789abcdef":
                        valid = False
                if passDict["ecl"]:
                    if passDict["ecl"] not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
                        valid = False
                if passDict["cid"]:
                    if len(passDict["cid"]) != 3 or passDict["cid"].strip("0123456789") != "" or passDict["cid"][0] == "0":
                        valid = False
            if valid:
                if count > 0:
                    validPassports.write("\n")      # new line only after the first one
                count += 1
                for i in rawPassportEntries:
                    validPassports.write(i.strip() + "\n")

            fullPassportEntry = ""
            rawPassportEntries = []
            passDict = {}
        else:
            fullPassportEntry += line.strip() + " "
            rawPassportEntries.append(line)

validPassports.close()
print(f"There are {count} valid passports")