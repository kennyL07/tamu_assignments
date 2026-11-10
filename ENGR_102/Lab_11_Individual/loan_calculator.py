# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   Lab 11 Individual
# Date:         6 11 2026
#

fileName = input("Enter the output filename: ")
principal = float(input("Enter the principal amount: "))
termLength = int(input("Enter the term length (months): "))
annualRate = float(input("Enter the annual interest rate: "))

loanFile = open(fileName, "w")

totalInterest = 0
balance = principal
monthlyPayment = (principal * annualRate / 12) / ( 1 - (1 / (1 + annualRate / 12)**termLength))


loanFile.write("Month,Total Accrued Interest,Loan Balance" + "\n")
loanFile.write(f"0,$0.00,${balance:0.2f}" + "\n") # First line

for i in range(1, termLength + 1):
    totalInterest += balance * annualRate / 12
    balance += balance * annualRate / 12
    balance -= monthlyPayment
    loanFile.write(f"{i},${totalInterest:0.2f},${balance:0.2f}" + "\n")
loanFile.close()