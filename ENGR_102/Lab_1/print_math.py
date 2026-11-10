# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      519
# Assignment:   Lab 1
# Date:         25 8 2026
#

from math import sin
from math import log
from math import pi

#Reynold's Number
fluidVelocity = 9 # m/s
kinematicViscosity = 0.0015 # m^2/s
linearDimension = 0.875 #m

reynoldsNum = (fluidVelocity * linearDimension) / (kinematicViscosity)
print("Reynolds number is", reynoldsNum)

#Wavelength with Brag's law
crystalLayerDist = 0.030 #nm
scatterDeg = 35 

wavelength = 2 * crystalLayerDist * sin((scatterDeg * pi)/180) # Must convert to rads since math.sin() uses radians
print("Wavelength is", wavelength, "nm")

#Arps Equation
days = 10
initProductionRate = 100 # barrels/day
declineRate = 2 # decrease/day
hyperbolicConstant = 0.8

fProductionRate = initProductionRate / (1 + hyperbolicConstant * declineRate * days) ** (1 / hyperbolicConstant)
print("Production rate is", fProductionRate, "barrels/day")

#Tsiolkovsky rocket equation
initMass = 11000 # kg
fMass = 8300 # kg
exhaustVel = 2030 # m/s
dVelocity = exhaustVel * log(initMass / fMass)
print("Change of velocity is", dVelocity, "m/s")