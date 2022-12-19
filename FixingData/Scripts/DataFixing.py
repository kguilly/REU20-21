#Kaleb Guillot
#1/16/2022

#This is a file to integrate the soil and pressure parameters of the 
#Kentucky Mesonet weather dataset into the existing dataset. 

import csv
import os
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
from pathlib import Path
import re

#point at the kentucky mesonet data
kentucky_file = "/home/kaleb/Files/FixingData/testing.csv" #test file for now
file = pd.read_csv(kentucky_file)
#point at the data files to be added to the mesonet data
soilData = ""
pressureData = ""

#loop that adds diferent values to the cells
for i in range (1, int(file.columns)):
    #how do you find the column number of a column
    file.iat[i, 1] = i+100
    file.iat[i, 2] = i+400

#add 'DayOfTheYear'
file['DayOfTheYear'] = 0

# Use this function and the line after to add the day of the year
# to the data
def dayoftheyear(x):
    if x!=0:
        
        # Traverse the dataframe,
        # return the value that you want to put in 
        # each row of the array
        month = (file[x, "Month"])
        day = (file[x, "Day"])
        year = (file[x, "Year"])

        date = str(month) + '-'+str(day)+'-'+str(year)
        print(date)
        #dayofyear = datetime.datetime.strptime(date, '%m-%d-%Y').timetuple().tm_yday
        #dayofyear = datetime.strptime(date, '%m-%d-%Y').timetuple().tm_yday
        dayofyear = 1
        return dayofyear
    return 0
#file["DayOfTheYear"] = file["DayOfTheYear"].apply(dayoftheyear)




#add 'ST02' (soil temperature at 2 meters)
file['ST02'] = 1
#add 'SM02' (soil moisture at 2 meters)
file['SM02'] = 2


file.to_csv("testing.csv", index=False)
