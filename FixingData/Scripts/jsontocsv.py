# Kaleb Guillot

# This is a script to convert json data 
# to a csv file

import json
import csv
import pandas as pd

# point to the files
input_file = "/home/kaleb/Files/FixingData/SOILDATA/SM02/2018/1D_BNGL_Avg.json"
output_file = "BNGL_soilData.csv"

with open(input_file) as input_:
    data = json.load(input_)

# Need to add a day of the year and year column so I can match 
# to the existing data

df = pd.DataFrame(data)
df.to_csv(output_file, header=['Date', "SM02"])



##################################################
# Testing phases
'''
#load the data into their respective variables
date_data = data['date']
val_data = data['val']

print(date_data)
print("\n\n####################################")
print(val_data)


####################################
# this doesn't work correctly

csv_writer = csv.writer(output_)
#counter variable used for writing 
# headers to the csv
count1 =0
count2 =00

for date in date_data:
    if count1==0:
        #write headers to the csv file
        #header = date.keys()
        csv_writer.writerow("Date")
        count1+=1
    
    #Writing data of csv file
    csv_writer.writerows(date)
for val in val_data:
    if count2==0:
        #header1 = val.keys()
        csv_writer.writerow("SM02")
        count2+=1

    csv_writer.writerows(val)

#####################################
#now write the value data to the csv

another_writer = csv.writer(output_)
if count2==0:
    another_writer("SM02")
    count2+=1
for i in range(0, len(val_data)):    
    another_writer.writerow(val_data[i])

df = open(output_file, 'w')
df.to_csv(output_file, header = ["Date", "SM02"])
'''

