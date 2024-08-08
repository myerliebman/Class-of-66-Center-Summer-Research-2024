# Reads weather data from a csv file (filename) for a specified date range. 
# Temperatures can be set to different intervals (daily highs, daily mins, daily averages, weekly averages) by uncommenting lines of code at the bottom of the file

import csv
from datetime import datetime

# Inputs:
date_string_1 = "January 1, 2023 12:00 AM"
date_string_2 = "January 1, 2024 12:00 AM"
filename = 'weathercache.csv'


date_format = "%B %d, %Y %I:%M %p"
date_time_obj_1 = datetime.strptime(date_string_1, date_format)
date_time_obj_2 = datetime.strptime(date_string_2, date_format)
epoch_time_1 = date_time_obj_1.timestamp()
epoch_time_2 = date_time_obj_2.timestamp()

times = []
temperatures = []
    
with open(filename, mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        #Each row has two columns: time and temperature
        if int(row[0]) < epoch_time_2 and int(row[0]) >= epoch_time_1 and (int(row[0]) % 3600 == 0):  #### %3600 Filters by hourly values
            time_value = int(row[0])
            #print(row[0])
            temperature_value = row[1] 
            times.append(time_value)
            temperatures.append(temperature_value)


daily_highs = []
daily_average = []
daily_mins = []
for day in range(int(len(temperatures)/24)):
    # Get the temperatures for the current day
    day_temps = temperatures[day * 24 : (day + 1) * 24]
    highest_temp = max(day_temps)
    min_temp = min(day_temps)
    average_temp = sum(float(temp) for temp in day_temps)/len(day_temps)
    # Append the highest temperature and average temperatures to lists
    daily_highs.append(highest_temp)
    daily_mins.append(min_temp)
    daily_average.append(average_temp)
    

weekly_averages = []
for week in range(int(len(daily_average)/7)):
    weekly_temps = daily_average[week * 7 : (week + 1) * 7]
    average_week_temp = sum(float(temp) for temp in weekly_temps)/len(weekly_temps)
    weekly_averages.append(average_week_temp)


# Temperatures are by default set to be temperatures in 1 hour intervals. The following lines can be uncommented to set temperatures to different intervals (daily highs, daily mins, daily averages, weekly averages):
#temperatures = daily_highs
temperatures = daily_average
#temperatures = weekly_averages
#temperatures = daily_mins
