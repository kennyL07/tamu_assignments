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
data_avg = [[] for a in range(12)]
data_max = [[] for a in range(12)]
data_min = [[] for a in range(12)]
data_percip = [[] for a in range(12)]

for data in lines:
    data = data.strip().split(",")
    month, day, year = data[0].split("/")
    avg = float(data[7]) if data[7] else np.nan
    maximum = float(data[8]) if data[8] else np.nan
    minimum = float(data[9]) if data[9] else np.nan
    percipitation = float(data[5]) if data[5] else np.nan
    if not avg == np.nan: data_avg[int(month) - 1].append(avg)
    if not maximum == np.nan: data_max[int(month) - 1].append(maximum)
    if not minimum == np.nan: data_min[int(month) - 1].append(minimum)
    if not percipitation == np.nan: data_percip[int(month) - 1].append(percipitation)        
        

mean_temp = [sum(i)/len(i) for i in data_avg]
mean_percip = [sum(i)/9 for i in data_percip]
maxs = [max(i) for i in data_max]
mins = [min(i) for i in data_min]

fig, ax1 = plt.subplots()

day = np.arange(len(days[0]))

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
# print(mean_percip)
plt.bar(np.arange(1,13), mean_temp)
plt.plot(np.arange(1,13), maxs)
plt.plot(np.arange(1,13), mins)
plt.plot(np.arange(1,13), mean_percip)
plt.title("Temperature and Percipitation by Month")
plt.xlabel("Month")
plt.ylabel("Average Temperature (F) \n Montly Percipitation (in)")
plt.show()