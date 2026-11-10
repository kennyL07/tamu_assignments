# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   Lab 11 Individual
# Date:         6 11 2026
#

weatherData = open("WeatherDataCLL.csv", "r")
data = weatherData.readlines()

temps = []
dates = {}
# {"dewPoint", "avgPressure", "avgWetBulb", "avgDailyWind", 
# "percipitation", "avgHumidity", "avgTemp", "maxTemp", "minTemp"}

for entry in data[1:]:
    entry = entry.strip().split(",")
    dates[entry[0]] = entry[1:]
    if entry[-1]:
        temps.append(float(entry[-1]))
    if entry[-2]:
        temps.append(float(entry[-2]))
weatherData.close()
print(f"10-year maximum temperature: {int(max(temps))} F")
print(f"10-year minimum temperature: {int(min(temps))} F" + "\n")

month = input("Please enter a month: ")
year = input("Please enter a year: ")

monthDict = {"January": 1,"February": 2,"March": 3,"April": 4,"May": 5,"June": 6,"July": 7,"August": 8,"September": 9,"October": 10,"November": 11,"December": 12,}
# {"dewPoint", "avgPressure", "avgWetBulb", "avgDailyWind", 
# "percipitation", "avgHumidity", "avgTemp"}
count = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[]}
for i in range(1,32):
    if f"{monthDict[month]}/{i}/{year}" in dates:
        day = dates[f"{monthDict[month]}/{i}/{year}"]
        for i in range(7):
            if day[i]:
                count[i].append(float(day[i]))
daysWithPercipitation = 0
for j in count[4]: # Counting precentage of days with rain not avgPercipitation
    if j > 0:
        daysWithPercipitation += 1
print()
print("For", month, year + ":")
print(f"Mean average daily pressure: {sum(count[1]) / len(count[1]):0.2f} in Hg")
print(f"Mean average daily temperature: {sum(count[6]) / len(count[6]):0.1f} F")
print(f"Mean average daily wet bulb temperature: {sum(count[2]) / len(count[2]):0.1f} F")
print(f"Mean average daily dew point: {sum(count[0]) / len(count[0]):0.1f} F")
print(f"Mean average daily relative humidity: {sum(count[5]) / len(count[5]):0.1f}%")
print(f"Mean average daily wind speed: {sum(count[3]) / len(count[3]):0.2f} mph")
print(f"Percentage of days with precipitation: {(daysWithPercipitation / len(count[4]) * 100):0.1f}%")