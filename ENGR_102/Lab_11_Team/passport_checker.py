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

validPassports = open("valid_passports.txt", "w")

totalPassports = 0

with open(filename, "r") as file:
    for line in file:
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
            
            # Do logic here
            data = fullPassportEntry.strip().split()
            keys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "cid"]
            passDict = {}
            valid = True
            for item in data:
                key, value = item.split(":")
                passDict[key] = value
            for i in keys:
                if i not in passDict:
                    valid = False
                    break
            if valid:
                count += 1
                for i in rawPassportEntries:
                    validPassports.write(i)
                validPassports.write("\n")
            fullPassportEntry = ""
            rawPassportEntries = []
        else:
            fullPassportEntry += line.strip() + " "
            rawPassportEntries.append(line)
            totalPassports += 1

data = fullPassportEntry.strip().split()
keys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "cid"]
passDict = {}
valid = True
for item in data:
    key, value = item.split(":")
    passDict[key] = value
for i in keys:
    if i not in passDict:
        valid = False
        break
if valid:
    count += 1
    for i in rawPassportEntries:
        validPassports.write(i)
    validPassports.write("\n")

validPassports.close()
# output number of valid passports
print(f"There are {count} valid passports")
