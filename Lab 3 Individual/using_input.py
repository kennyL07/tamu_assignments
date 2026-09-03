# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   Lab 1
# Date:         3 9 2026
#

from math import sin
from math import log
from math import pi

#Reynold's Number
print("This program calculates the Reynolds number given velocity, length, and viscosity")
fluidVelocity = float(input("Please enter the velocity (m/s): ")) # m/s
linearDimension = float(input("Please enter the length (m): ")) # m^2/s
kinematicViscosity = float(input("Please enter the viscosity (m^2/s): ")) #m

reynoldsNum = (fluidVelocity * linearDimension) / (kinematicViscosity)
print(f"Reynolds number is {reynoldsNum:.0f}", end="\n\n")

#Wavelength with Brag's law
print("This program calculates the wavelength given distance and angle")
crystalLayerDist = float(input("Please enter the distance (nm): ")) #nm
scatterDeg = float(input("Please enter the angle (degrees): "))

wavelength = 2 * crystalLayerDist * sin((scatterDeg * pi)/180) # Must convert to rads since math.sin() uses radians
print(f"Wavelength is {wavelength:.4f} nm", end="\n\n")

#Arps Equation
print("This program calculates the production rate given time, initial rate, and decline rate")
days = float(input("Please enter the time (days): "))
initProductionRate = float(input("Please enter the initial rate (barrels/day): ")) # barrels/day
declineRate = float(input("Please enter the decline rate (1/day): ")) # decrease/day
hyperbolicConstant = 0.8

fProductionRate = initProductionRate / (1 + hyperbolicConstant * declineRate * days) ** (1 / hyperbolicConstant)
print(f"Production rate is {fProductionRate:.2f} barrels/day", end="\n\n")

#Tsiolkovsky rocket equation
print("This program calculates the change of velocity given initial mass, final mass, and exhaust velocity")
initMass = float(input("Please enter the initial mass (kg): ")) # kg
fMass = float(input("Please enter the final mass (kg): ")) # kg
exhaustVel = float(input("Please enter the exhaust velocity (m/s): ")) # m/s
dVelocity = exhaustVel * log(initMass / fMass)
print(f"Change of velocity is {dVelocity:.1f} m/s")