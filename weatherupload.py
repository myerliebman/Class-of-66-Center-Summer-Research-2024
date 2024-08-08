import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime



data = '/Users/myerliebman/Downloads/combined_output2023test_copy.xlsx'

df = pd.read_excel(data, sheet_name='Sheet1')

temp = df.iloc[:, 0].tolist()
temp2 = []
for num in temp:
    #remove units and add to new list
    newnum = num[:-3]
    floatnum = float(newnum)
    temp2.append(floatnum)
#print(temp2)

#########ACCOUNTS FOR MISSING DATA. MUST FIX
#temp2.append(40)
#temp2.append(40)
#temp2.append(40)
#temp2.append(40)
#temp2.append(40)





date = df.iloc[:, 1].tolist()
#unixdate = pd.to_datetime(date)
date2 = []
for date in date:
    newdate = int(date.timestamp())
    date2.append(newdate)
#print(date2)

date_and_time2 = [datetime.datetime.fromtimestamp(i).strftime('%Y-%m-%d %I:%M:%S %p') for i in date2]


#plt.plot(date_and_time2, temp2)
#plt.xticks(date_and_time2[::int(100)]) #sets number of ticks so that labels don't overlap
#plt.show()


