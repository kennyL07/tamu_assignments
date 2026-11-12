# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   Lab 12
# Date:         12 11 2026
#

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as date
file = open("WeatherDataCLL.csv")

days = [[] for a in range(10)]
# 0 Date,
# 1 Average Dew Point (F),
# 2 Average Pressure (in Hg),
# 3 Average Wet Bulb Temperature (F),
# 4 Average Daily Wind Speed (mph),
# 5 Precipitation (in),
# 6 Average Relative Humidity (%),
# 7 Average Temperature (F),
# 8 Maximum Temperature (F),
# 9 Minimum Temperature (F)

lines = file.readlines()[1:]
for data in lines:
    data = data.strip().split(",")
    days[0].append(data[0])
    for i in range(1, len(data)):
        if not data[i]:
            days[i].append(np.nan)
        else:
            days[i].append(float(data[i]))

day = np.arange(len(days[0]))

fig, ax1 = plt.subplots()

line1 = ax1.plot(day, days[3], label='Avg Wet Bulb Temp', color='red')
ax1.set_xlabel('date')
ax1.set_ylabel('Average Wet Bulb Temperature (F)')
ax1.set_ylim(10, 83)
ax1.set_yticks(np.arange(0, 110, 5))
ax2 = ax1.twinx()
line2 = ax2.plot(day, days[2], label='Average Pressure', color='blue')
ax2.set_ylabel('Average Pressure (in Hg)')
ax2.set_ylim(29, 31)
ax2.set_yticks(np.arange(29, 31, 0.1))

plt.title('Average Wet Bulb Temperature and Average Pressure')
lines_all = line1 + line2

plt.show()

fig2, y = plt.subplots()

# counts, bins = np.histogram(days[4])
y.hist(days[4],"auto",color="green")
y.set_yticks(np.arange(0,400,50))
y.set_xlabel("Average Daily Wind Speed (mph)")
y.set_ylabel("Number of Days")
y.set_xticks(np.arange(0,25,5))
y.set_title("Histogram of Average Wind Speed")
plt.show()

plt.scatter(days[1], days[6]).set_color("black")
plt.ylabel("Average Relative Humidity (%)")
plt.xlabel("Average Dew Point (F)")
plt.title('Average Relative Humidty vs Average Dew Point')
plt.show()