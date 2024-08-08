**Class of 66' Center Summer Research 2024 Code:**

**Energy data code:**

localegaugetest.py - Tests connection to egauge meters

localdataread.py - Reads energy data from egauge meter and writes to a csv file

csvenergyupload.py - Reads energy data from a csv file for a specified date range


**Weather data code:**

weatherapihistorical.py - Reads energy data from WeatherLink and writes to a csv file

csvweatherupload.py - Reads energy data from a csv file for a specified date range


**General code:**

csvsort.py - Sorts a csv by timestamp

localtest.py - Graphs weather vs energy data

regressiontest.py - Runs a regression test on the graph from localtest 



**Instructions for use:**

Use localdataread.py and weatherapihistorical.py to get data and write to csv files. Use csvsort.py to sort the csv by timestamp.

Set date range to graph and filenames in csvenergyupload.py and csvweatherupload.py

Run localtest.py which calls csvenergyupload.py and csvweatherupload.py and graphs the data

Run regressiontest.py to call localtest.py and run a regression test on the data
