# Inputs data by running csvenergyupload and csvweatherupload and graphs the data using matplotlib

import matplotlib.pyplot as plt

from datetime import datetime

import numpy as np
from matplotlib.ticker import FuncFormatter


from csvweatherupload import temperatures as temp_list, times as time_list2
from csvenergyupload import energy as differences_kWh, times

#date_and_time2 = [datetime.fromtimestamp(i).strftime('%Y-%m-%d %I:%M:%S %p') for i in times]
date_and_time2 = [datetime.fromtimestamp(i).strftime('%m-%d-%Y') for i in times]

print("Length of differences_kWH (energy): ", len(differences_kWh))
print("Length of temp_list (weather): ", len(temp_list))

#Time interval between recordings in hours
time_interval = 24

kW_list = [i/time_interval for i in differences_kWh]


temp_list = [float(i) for i in temp_list]

# Sets up graphing
plt.rc('figure', figsize=(11, 7))
fig, ax1 = plt.subplots()

def format_energy(y, pos):
    return f'{y:.1f} kW'

def format_temperature(y, pos):
    return f'{y:.0f} °F'

# Plot energy on first axis
ax1.plot(date_and_time2, kW_list, label = 'Energy', linewidth=1)
ax1.yaxis.set_major_formatter(FuncFormatter(format_energy))
ax1.set_ylabel('Energy', color='blue')

#Creates a second axis
ax2 = ax1.twinx()

# Plot temperature on second axis
ax2.plot(date_and_time2, temp_list, label = 'Temp', linewidth=1, color='orange')
ax2.yaxis.set_major_formatter(FuncFormatter(format_temperature))
ax2.set_ylabel('Temperature', color='orange')


#tick_positions = [162,526,890,1254] #Use for graphing 4 years
tick_positions = [0, 59, 119, 180, 241, 302, 363]
ax1.set_xticks(tick_positions)
ax2.yaxis.grid(False)

ax1.set_xlabel('Date')

# Sets y-axis ticks for temperature
y_min, y_max = ax2.get_ylim()
y_ticks_temp = np.linspace(y_min, y_max, 5)
ax2.set_yticks(y_ticks_temp)

# Sets y-axis ticks for energy
y_min, y_max = plt.ylim()
y_ticks_energy = np.linspace(y_min, y_max, 5)
plt.yticks(y_ticks_energy)


# Graphs data
plt.xlabel('Time Interval')
plt.ylabel('Temperature')
ax1.set_label('Energy')
plt.title('Daily High Temperature vs Heat Pump Energy Used: 2023')
plt.grid(True)
plt.show()


#print(differences_kWh)
#print(temp_list)

