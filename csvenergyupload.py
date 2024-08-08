# Takes in an interval start date and end date (specified in date_string_1 and date_string_2) and a csv file (filename) and extracts energy data from that date range into a list of times and a list of energy used

import csv
from datetime import datetime

date_string_1 = "January 1, 2023 12:00 AM"
date_string_2 = "January 1, 2024 12:00 AM"
# Data location:
filename = 'dailyenergycache.csv'

date_format = "%B %d, %Y %I:%M %p"
date_time_obj_1 = datetime.strptime(date_string_1, date_format)
date_time_obj_2 = datetime.strptime(date_string_2, date_format)
epoch_time_1 = date_time_obj_1.timestamp()
epoch_time_2 = date_time_obj_2.timestamp()

times = []
energy = []
    

with open(filename, mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        #Each row has two columns: time and energy
        #print(row[0], epoch_time_1, epoch_time_2)
        if int(row[0]) < epoch_time_2 and int(row[0]) >= epoch_time_1:
            time_value = int(row[0])
            energy_value = float(row[1])
            times.append(time_value)
            energy.append(energy_value)

