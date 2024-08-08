# Reads energy data from WeatherLink API for a specifed date range and writes to a csv file (filename)

import json
import requests

from datetime import datetime
import csv
from tqdm import tqdm

BASE_URL = "https://api.weatherlink.com/v2/"

API_KEY = "<Insert API Key Here>"
API_SECRET = "<Insert API Secret Here>"

#Data Request Input Values
date_string_1 = "January 1, 2017 12:00 AM"
date_string_2 = "June 14, 2018 12:00 AM"
filename = 'weathercache.csv'


date_format = "%B %d, %Y %I:%M %p"
date_time_obj_1 = datetime.strptime(date_string_1, date_format)
date_time_obj_2 = datetime.strptime(date_string_2, date_format)
epoch_time_1 = int(date_time_obj_1.timestamp())
epoch_time_2 = int(date_time_obj_2.timestamp())

current_unix_time = str(int(datetime.now().timestamp()))


# https://weatherlink.github.io/v2-api/api-reference
endpoint = "historic"
# API Path Parameters
pathParameters = ['bb97a2e3-62c6-4ae6-aa6e-5e28d7e03b9e'
]

#creates list to store temperature and time data
time_temp_list = []

#Sets up progress bar
progress_bar = tqdm(total=(epoch_time_2 - epoch_time_1) // 86400, desc="Fetching weather data")

#Function to write data to csv file
def write_tuples_to_csv(tuple_list):
    with open(filename , mode='a', newline='') as file:
        writer = csv.writer(file)
        for key, value in tuple_list:
            writer.writerow([key, value])


while epoch_time_1 < epoch_time_2:
  
  # API Query String Parameters
  # Querys for max size allowed by the API (24 hours or 86400 seconds)
  queryParameters = [('start-timestamp', str(epoch_time_1)), ('end-timestamp', str(epoch_time_1 + 86400))
  ]
  # Create final API URL
  api_url = BASE_URL + endpoint 
  api_url += ''.join("/" + str(param) for param in pathParameters)[0:] 
  api_url += "?api-key=" + API_KEY 
  api_url += ''.join("&" + str(x) + "=" + str(y) for (x,y) in queryParameters)[0:]

  # Make call to API and pretty-print returned data
  api_results = requests.get(
    headers= {
      "X-Api-Secret": API_SECRET
    },
    url=api_url, 
    verify=True,
  )

  api_output = json.loads(api_results.text)

  data = api_output

  #Prints error messages if there are any
  if "message" in data:
    print(data["message"])
  
  #Extract ts (timestamp) and temp_out from each data point
  for sensor in data["sensors"]:
      for datapoint in sensor["data"]:
          ts = datapoint["ts"]
          temp_out = datapoint["temp_out"]
          time_temp_list.append((ts, temp_out))
  
  #Increments by the number of seconds in a day
  epoch_time_1 += 86400
  
  progress_bar.update(1)

progress_bar.close()



time_list = []
temp_list = []

#Deals with missing or null temperature valuse 
for i in range(int((epoch_time_2-epoch_time_1)/600)):   
  #Checks for null values and removes
  if time_temp_list[i][1] == None:  ##[1]
    print(f"None value detected at {datetime.fromtimestamp(time_temp_list[i][0]).strftime('%Y-%m-%d %I:%M:%S %p')} was removed")
    time_temp_list.pop(i)
  #Checks for missing values and adds
  if time_temp_list[i][1] == '':
     print(f"Missing value detected at {datetime.fromtimestamp(time_temp_list[i][0]).strftime('%Y-%m-%d %I:%M:%S %p')}")
     time_temp_list[i][1] == time_temp_list[i-1][1]


#Deals with missing timestamps
flag = False
while not flag:
  for i in range(len(time_temp_list)-1):
    if time_temp_list[i+1][0] - time_temp_list[i][0] > 600:
      print(f"Missing data detected at {datetime.fromtimestamp(time_temp_list[i][0]+600).strftime('%Y-%m-%d %I:%M:%S %p')}")
      #Adds a new time and temp value
      time_temp_list.insert(i+1, (time_temp_list[i][0]+600, (time_temp_list[i][1])))
      flag = False
    else:
      flag = flag or True

#Saves data
write_tuples_to_csv(time_temp_list)

for pair in time_temp_list:
  time_list.append(pair[0])
  temp_list.append(pair[1])

time_list2 = [datetime.fromtimestamp(i).strftime('%Y-%m-%d %I:%M:%S %p') for i in time_list]

#print(time_list2)
#print(temp_list)