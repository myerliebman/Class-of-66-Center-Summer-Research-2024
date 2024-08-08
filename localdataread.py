#Reads energy data from an eGauge meter (specified in URI) and writes to a csv file (specified in filename)


import csv
from egauge import webapi

from datetime import datetime

from tqdm import tqdm

from egauge.webapi.device import Capture, TriggerMode


URI = "http://eGauge22702.egaug.es"      # replace DEV with meter name
USR = "USER"                      # replace USER with user name
PWD = "PASS"                      # replace PASS with password

dev = webapi.device.Device(URI, webapi.JWTAuth(USR,PWD))

# Data Request Input Values
date_string_1 = "July 23, 2020 12:00 AM"
date_string_2 = "July 23, 2024 12:00 AM"
filename = 'weeklyenergycache.csv'

# Number of seconds in each interval
#interval_secs = 3600
#interval_secs = 86400
#interval_secs = 600
interval_secs = 604800

# Specifies which meter is being read from
register_numbers = [6]


# Formats dates
date_format = "%B %d, %Y %I:%M %p"
date_time_obj_1 = datetime.strptime(date_string_1, date_format)
date_time_obj_2 = datetime.strptime(date_string_2, date_format)
epoch_time_1 = date_time_obj_1.timestamp()
epoch_time_2 = date_time_obj_2.timestamp()


registers_string = ''
for reg in register_numbers:
    registers_string += str(reg)
    registers_string += '+'
registers_str = registers_string[:-1]

# Sets up progress bar tracking
total_intervals = 4
interval_size = int((epoch_time_2 - epoch_time_1) / total_intervals)

# Initializes tqdm (progress bar)
progress_bar = tqdm(total=total_intervals, desc="Fetching egauge energy data")

data_list = []

new_epoch_time1 = epoch_time_1
# Fetches data in intervals 
for _ in range(total_intervals):
    #print(f'/register?reg={registers_str}&rate&time={int(new_epoch_time1)}:{interval_secs}:{int(new_epoch_time1 + interval_size)}')
    data = dev.get(f'/register?reg={registers_str}&rate&time={int(new_epoch_time1)}:{interval_secs}:{int(new_epoch_time1 + interval_size)}')
    data_list.insert(0, data)
    new_epoch_time1 += interval_size
    progress_bar.update(1)

# Close progress bar
progress_bar.close()

# Allows for testing data output:
#data = dev.get('/register?reg=' + registers_str + '&rate&time=' + str(epoch_time_1) + ':' + interval_secs + ':' + str(epoch_time_2))
#print(data)



# Close progress bar
progress_bar.close()


# Process Data:

# Function to flatten the rows and convert to integers
def flatten_and_convert(rows):
    return [abs(int(row[0])) for row in rows]

# Extract and process data from ranges
all_differences = []
for data in data_list:
    for range_data in data['ranges']:
        values = flatten_and_convert(range_data['rows'])
        differences = [values[i+1] - values[i] for i in range(len(values)-1)]
        all_differences.extend(differences)


# Generate time intervals for differences
time_len = range(0, len(all_differences))
time_intervals = [int(epoch_time_1) + (int(interval_secs)*i) for i in time_len]
date_and_time2 = [datetime.fromtimestamp(i).strftime('%Y-%m-%d %I:%M:%S %p') for i in time_intervals]


# Converts energy values from Watt-Seconds (Joules)to kWh by dividing Ws by 3,600,000.
differences_kWh = [i * (-1/3600000) for i in all_differences] 
differences_kWh = differences_kWh[::-1]

#Function to write data to cache
def write_tuples_to_csv(time_intervals, differences_kWh):
    # Open the file in write mode
    with open(filename , mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write the tuples to the CSV file
        for i in range(len(differences_kWh)):
            writer.writerow([time_intervals[i], differences_kWh[i]])

write_tuples_to_csv(time_intervals, differences_kWh)