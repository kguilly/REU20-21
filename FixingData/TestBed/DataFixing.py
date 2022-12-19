# Kaleb Guillot
# Last Edited: 5/22/2022
# This is a file to add columns of parameters to the Kentucky data. These columns are: PRES,
# DayOfTheYear, SM02, and ST02

# Outline of Code (2/8/22)
'''
- Separate the Pressure data into their respective years and output to new directory
- For each year passed by the arguments:
    - open the kentucky file as a dataframe
    - Add the day of the year
        - grab the day, month, and year columns and find day of the year
        - append to list
        - write list to dataframe
    - Expand the kentucky dataframe to include every day, hour, and five
      minute interval of the year
    - for the pressure, st02, and sm02 data
        - grab the data and put into a dataframe with the "DayOfTheYear", "Hour"
          and "Minute" columns
        - call the add_column function
            - change the data of hour and minute to match kentucky data
            - expand the parameter's dataframe to include every day, hour,
              and five minute interval of the year
            - find where the time of the kentucky and parameter df match
            - write the data to a list
            - append the list to the kentucky dataframe
    - Write the dataframe to a new csv file

'''

from audioop import avg
from genericpath import exists
import stat
import sys
from calendar import month
import csv
import os
from tkinter import N
from tkinter.messagebox import NO
from tkinter.tix import COLUMN
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
from pathlib import Path
import re
import json
import argparse


class DataFixing():
    ##########################################################################
    def __init__(self):
        self.version = 1.0

        # For these parameters, point at the folder that holds the years of data. 
        self.kentucky_file_loc_0 = "/opt/Kentucky/"  # point at the folder containing the years
        self.st02_file_loc_0 = "/opt/Kentucky/SOILDATA/ST02/"
        self.sm02_file_loc_0 = "/opt/Kentucky/SOILDATA/SM02/"

        # Point at the folder holding the pressure file. Script thinks the name is <StationID>.csv
        self.pres_file_loc_0 = "/home/kaleb/Files/FixingData/TestBed/PressureInput/"

        # Point at the folder you want to put it in
        self.kentucky_output_file_loc_0 = "/home/kaleb/Files/FixingData/CSVs/(5_24)/"
        self.pres_output_loc_0 = "/home/kaleb/Files/FixingData/TestBed/PressureOutput/"

    ##########################################################################
    # Function that separates the pressure data into individual years
    def sep_pres_data(self, stationID):

        pres_file_loc_1 = self.pres_file_loc_0 + str(stationID) + ".csv"
        input_file = pd.read_csv(pres_file_loc_1)


        net = input_file['NET']
        stid = input_file["STID"]
        utme = input_file["UTME"]
        pres = input_file["PRES"]
        net.values.tolist()
        stid.values.tolist()
        utme.values.tolist()
        pres.values.tolist()

        net_arr = []
        stid_arr = []
        utme_arr = []
        pres_arr = []

        sameyear = True

        for i in range(0, len(net)):

            sameyear = True

            net_arr.append(net[i])
            stid_arr.append(stid[i])
            utme_arr.append(utme[i])
            pres_arr.append(pres[i])

            date_0 = (utme[i].split(' '))
            date_1 = (date_0[0].split('-'))
            year = date_1[0]

            try:
                utme[i + 1]
            except:
                sameyear = False
                next_year = 0
            else:
                next_date_0 = (utme[i + 1].split(' '))
                next_date_1 = (next_date_0[0].split('-'))
                next_year = next_date_1[0]

            if (next_year != year):
                sameyear = False

            # if the next iteration does not equal the first station, write out the array and
            # clear it
            if (sameyear == False):
                data = {"NET": (net_arr[i] for i in range(0, len(net_arr))),
                        "STID": (stid_arr[i] for i in range(0, len(net_arr))),
                        "UTME": (utme_arr[i] for i in range(0, len(utme_arr))),
                        "PRES": (pres_arr[i] for i in range(0, len(pres_arr)))}
                df = pd.DataFrame(data)

                pressure_output_loc_1 = self.pres_output_loc_0 + str(year) + '/'
                pressure_output_loc_2 = pressure_output_loc_1 + stid_arr[0] + '_' + str(year) + "PRESdata.csv"

                isExist = os.path.exists(pressure_output_loc_1)
                if (isExist == False):
                    os.makedirs(pressure_output_loc_1)
                df.to_csv(pressure_output_loc_2)

                # clear out the arrays to get ready for the next year
                net_arr = []
                stid_arr = []
                utme_arr = []
                pres_arr = []

        return None

    ##########################################################################
    # Function that adds a "DayOfTheYear" column to the Kentucky file
    def add_dayoftheyear(self, year, kentucky_df):

        # Read the file for the day, month, and year
        days = kentucky_df['Day']  ###### very sensitive to spaces
        months = kentucky_df["Month"]
        year = kentucky_df["Year"]

        # convert the dataframes to lists
        days.values.tolist()
        months.values.tolist()
        year.values.tolist()

        # loop through these lists and find the corresponding day of the
        # year for each date
        dayofyear = []
        for i in range(0, len(year)):
            y = int(year[i])
            m = int(months[i])
            d = int(days[i])
            kentucky_date = str(m) + '-' + str(d) + '-' + str(y)
            dayoftheyear = datetime.strptime(kentucky_date, '%m-%d-%Y').timetuple().tm_yday
            dayofyear.append(dayoftheyear)

        # Now add the column to the dataframe
        kentucky_df.insert(2, "DayOfTheYear", dayofyear)  # doesn't delete any columns
        return None

    ##########################################################################
    # Function to add columns
    def add_column(self, param, param_df, kentucky_df):

        data_hour = list(param_df["Hour"])
        data_minute = list(param_df["Minute"])
        data_list = list(param_df[param])

        ## Problem with the parameter data. Hours and minutes are strings while the kentucky's are ints
        if len(data_list) > 1:
            if isinstance(data_hour[1], str):
                param_df["Hour"] = self.cleanse_data(data_hour)
            if isinstance(data_minute[1], str):
                param_df["Minute"] = self.cleanse_data(data_minute)

        # Expand the parameter df to include every day, hour, and minute of the year
        param_df = self.expand_df(param_df)

        kentucky_df.insert(2, param, param_df[param])

        '''
        # temp_df = pd.DataFrame()
        # temp_df["MatchingDays"] = np.where(kentucky_df["DayOfTheYear"] == param_df["DayOfTheYear"], 1, 0)
        # temp_df["MatchingHours"] = np.where(kentucky_df["Hour"] == param_df["Hour"], 1, 0)
        # temp_df["MatchingMinutes"] = np.where(kentucky_df["Minute"] == param_df["Minute"], 1, 0)
        # temp_df.insert(0, "TheData", param_df[param])
        #
        # datatokentucky = []
        #
        # for i in range(0, len(temp_df)):
        #     if temp_df.at[i, "MatchingDays"] == temp_df.at[i, "MatchingHours"] == temp_df.at[i, "MatchingMinutes"] == 1:
        #         # append the value that corresponds to the correct index
        #         datatokentucky.append(temp_df.at[i, "TheData"])
        #     else:
        #         datatokentucky.append(None)
        # kentucky_df.insert(2, param, datatokentucky)

        
        dataToKentucky = [None] * len(kentucky_minute)
        for kday in kentucky_dayoftheyear:
            for dday in data_dayofyear:
                if kday == dday:
                    for khour in kentucky_hour:
                        for dhour in data_hour:
                            if khour == dhour:
                                for kmin in kentucky_minute:
                                    for dmin in data_minute:
                                        if kmin == dmin:
                                            dataToKentucky[kentucky_minute.index(kmin)] = ...
                                            data_list[data_minute.index(dmin)]
        '''

        return None

    ###############################################################################
    def cleanse_data(self, arr):
        newArr = []
        # Put the string into an array
        for x in arr:
            y = [char for char in x]
            # get rid of the first 0
            if (y[0] == '0'):
                y = y[1]
            else:
                y = y[0] + y[1]
            # replace
            newArr.append(int(y))

        return newArr

    ###############################################################################
    # Add the pressure data (PRES column)
    def add_pres(self, year, kentucky_df, stationId):

        pressure_file_loc = self.pres_output_loc_0 + str(year) + '/' + stationId + '_' + str(
            year) + "PRESdata.csv"
        pressure_file = pd.read_csv(pressure_file_loc)

        # Grab the pressure column and utme
        utme = pressure_file["UTME"]
        pres_data = pressure_file["PRES"]

        pres_dayoftheyear_arr = []
        pres_hour_arr = []
        pres_minute_arr = []
        pres_data_arr = []
        for i in range(0, len(utme)):
            # need to parse and compute the time and day of the year
            x = utme[i]
            y = x.split(' ')  # splits by the space in the middle
            utmeDate = y[0]
            utmeTime = y[1]

            # split the date by the hyphen, then separate into respective year, month, day..
            # then turn into the day of the year
            z = utmeDate.split('-')
            year_0 = z[0]
            month_0 = z[1]
            day_0 = z[2]
            pres_date = str(year_0) + '-' + str(month_0) + '-' + str(day_0)
            pres_dayoftheyear = datetime.strptime(pres_date, "%Y-%m-%d").timetuple().tm_yday

            # split the time by the colon, separate into hour, minute, second
            pres_time = utmeTime.split(":")
            pres_hour = pres_time[0]
            pres_minute = pres_time[1]
            # pres_second = pres_time[2]

            # Grab the pressure data
            pres = pres_data[i]

            # append the values to their arrays
            pres_dayoftheyear_arr.append(pres_dayoftheyear)
            pres_hour_arr.append(pres_hour)
            pres_minute_arr.append(pres_minute)
            pres_data_arr.append(pres)

        # concatenate the arrays into a multidimensional array
        df = pd.DataFrame({"DayOfTheYear": pres_dayoftheyear_arr,
                           "Hour": pres_hour_arr,
                           "Minute": pres_minute_arr,
                           "PRES": pres_data_arr})

        # some data is missing, fill null values 
        s = df["PRES"]
        total = 0
        count = 0
        s = s.replace(np.nan, pd.NA)

        for val in s:
            if val is not pd.NA:
                val = float(val)
                total += val
                count +=1
        if count > 0:
            avgVal = float(total / count)
        else:
            avgVal = 'N/A'

        s.fillna(method='ffill', inplace=True)
        s = s.fillna(avgVal)


        df["PRES"] = s

        self.add_column("PRES", df, kentucky_df)
        return None

    ##########################################################################
    # Add the ST02 column
    def add_st02(self, year, kentucky_df, stationID):

        date_arr = []
        val_arr = []
        st02_file_loc = self.st02_file_loc_0 + str(year) + '/'
        month_folder = sorted(os.listdir(st02_file_loc))

        for months in month_folder:
            month_path = self.st02_file_loc_0 + str(year) + '/'
            newPath = month_path + months + '/'

            if os.path.exists(newPath):
                day_folders = sorted(os.listdir(newPath))

                for days in day_folders:
                    day_path = newPath + days + '/'
                    if os.path.exists(day_path):
                        file = sorted(os.listdir(day_path))

                        for jsonFiles in file:
                            file_path = day_path + jsonFiles
                            filename = "30_" + stationID + ".json"
                            if jsonFiles == filename:

                                with open(file_path) as f:
                                    data = json.load(f)
                                    l1 = list(data.values())
                                    np_arr = np.array(l1)
                                    transpose = np_arr.T
                                    transpose_list = transpose.tolist()

                                    #######################################
                                    # May need to do this part another way
                                    for date, val in transpose_list:
                                        date_arr.append(date)
                                        val_arr.append(val)

        # The data from the json files is stored in the date arr and val arr
        # separate the date into the columns that need to be passed into the add column function
        # day of the year, hour, minute, and the value
        # take this from how I did it in the sep_pres_data function (May need to
        # eventually write a function to separate this on its own)
        # dates are formatted as: "yyyy-mm-dd hh:mm:ss"
        dayoftheyear_arr = []
        hour_arr = []
        minute_arr = []
        for date in date_arr:
            date_0 = (date.split(' '))
            # date_1 = date_0[0].split('-')
            time_0 = date_0[1].split(':')

            dayoftheyear = datetime.strptime(date_0[0], "%Y-%m-%d").timetuple().tm_yday
            dayoftheyear_arr.append(dayoftheyear)

            hour = time_0[0]
            minute = time_0[1]
            hour_arr.append(hour)
            minute_arr.append(minute)

        # df = pd.DataFrame([dayoftheyear_arr, hour_arr, minute_arr, val_arr], columns=["DayOfTheYear", "Hour", "Minute", "ST02"])
        df = pd.DataFrame({"DayOfTheYear": dayoftheyear_arr,
                           "Hour": hour_arr,
                           "Minute": minute_arr,
                           "ST02": val_arr})

        # self.add_column(self, "ST02", df, kentucky_df)
        self.add_column("ST02", df, kentucky_df)

        return None

    ###########################################################################
    # Add the SM02
    def add_sm02(self, year, kentucky_df, stationID):

        date_arr = []
        val_arr = []
        sm02_file_loc = self.sm02_file_loc_0 + str(year) + '/'
        month_folder = sorted(os.listdir(sm02_file_loc))

        for months in month_folder:
            month_path = self.sm02_file_loc_0 + str(year) + '/'
            newPath = month_path + months + '/'

            if os.path.exists(newPath):
                day_folders = sorted(os.listdir(newPath))

                for days in day_folders:
                    day_path = newPath + days + '/'

                    if os.path.exists(day_path):
                        file = sorted(os.listdir(day_path))

                        for jsonFiles in file:
                            file_path = day_path + jsonFiles
                            fileName = "30_" + stationID + ".json"
                            if jsonFiles == fileName:

                                with open(file_path) as f:
                                    # this part needs work:
                                    # load the data, put into an array, then transpose it
                                    data = json.load(f)
                                    l1 = list(data.values())
                                    np_arr = np.array(l1)
                                    transpose = np_arr.T
                                    transpose_list = transpose.tolist()

                                    for date, val in transpose_list:
                                        date_arr.append(date)
                                        val_arr.append(val)

        dayoftheyear_arr = []
        hour_arr = []
        minute_arr = []
        for date in date_arr:
            date_0 = (date.split(' '))
            # date_1 = date_0[0].split('-')
            time_0 = date_0[1].split(':')

            dayoftheyear = datetime.strptime(date_0[0], "%Y-%m-%d").timetuple().tm_yday
            dayoftheyear_arr.append(dayoftheyear)

            hour = time_0[0]
            minute = time_0[1]
            hour_arr.append(hour)
            minute_arr.append(minute)

        # df = pd.DataFrame([dayoftheyear_arr, hour_arr, minute_arr, val_arr], columns=["DayOfTheYear", "Hour", "Minute", "SM02"])
        df = pd.DataFrame({"DayOfTheYear": dayoftheyear_arr,
                           "Hour": hour_arr,
                           "Minute": minute_arr,
                           "SM02": val_arr})

        # self.add_column(self,"SM02", df, kentucky_df)

        self.add_column("SM02", df, kentucky_df)
        return None

    ##########################################################################
    # Df may not be of the right length to include every day, hour, and 5 minute time interval
    @staticmethod
    def expand_df(df):

        newList = []

        for day in range(1, 366):  # can't handle leap years yet
            for hour in range(24):
                for minute in range(0, 56, 5):
                    newList.append([day, hour, minute])
        temp_df = pd.DataFrame(newList, columns=["DayOfTheYear", "Hour", "Minute"])
        df = pd.merge(temp_df, df, how='left', on=["DayOfTheYear", "Hour", "Minute"])

        df.sort_values(by=["DayOfTheYear", "Hour", "Minute"], inplace=True)

        return df

    ############################################################################
    # The soil data is a little messed up, need to fix
    def fix_soil_data(self, df, soilParam):

        # First get the average of the soil parameter of the entire column        
        s = df[soilParam]
        total = 0
        count = 0

        for val in s:

            if val is not None and val is not np.nan: 
                val = float(val)
                total += val
                count += 1
        
        avgVal = total / count

        # forward fill 
        s = s.replace(np.nan, pd.NA)
        s.fillna(method='ffill', inplace=True)

        # # fill in all remaining values with the average value
        s = s.fillna(avgVal)
        
        df[soilParam] = s
    

##########################################################################
# Configuring the main functionality of the code
def main(self):
    # parser = argparse.ArgumentParser(description="What years do you want to parse through?")
    # parser.add_argument('--sy', default=2018, type=int, help="The year to start, formatted as: yyyy. Ex. 2018")
    # parser.add_argument('--ey', default=2018, type=int, help="The end year, this year will be included")

    # args = parser.parse_args()

    f = DataFixing()

    # Which station would you like to test for:
    stationID = input("Enter the 4 letter acronym of the station to test for: ")

    # Date ranges
    dateRange = input("Enter the year range of data to fix (yyyy - yyyy): ")
    separated = dateRange.split('-')
    by = int(separated[0])
    ey = int(separated[1])

    year_range = ey - by

    sep_pres = input("Would you like to separate the pressure data into yearly files [y/n]? ")
    if sep_pres == 'y' or sep_pres == 'Y':
        f.sep_pres_data(stationID)
    else:
        print("The pressure data was not separated\n")

    for i in range(0, year_range + 1):
        year = by + i

        # First load the data from the kentucky file into a pandas dataframe
        files = sorted(os.listdir(f.kentucky_file_loc_0 + str(year) + '/'))
        
        for file in files:
            if file[0:3] == stationID[0:3]:
                kentucky_df = pd.read_csv(f.kentucky_file_loc_0 + str(year) + '/' + file)
        
        # Add the day of the year column to the kentucky files
        f.add_dayoftheyear(year, kentucky_df)
        # print(kentucky_df.head())  # debugging purposes

        # Fix the length of the kentucky data
        kentucky_df_2 = f.expand_df(kentucky_df)

        # add the pressure data
        f.add_pres(year, kentucky_df_2, stationID)
        # print(kentucky_df.head())

        # add the st02 data
        f.add_st02(year, kentucky_df_2, stationID)
        # print(kentucky_df.head())

        # add the sm02 data
        f.add_sm02(year, kentucky_df_2, stationID)
        # print(kentucky_df.head())

        # Compress the data
        compress = input("Would you like to strip the beginning of the year from the file [y/n]? ")
        if compress == 'y' or compress == 'Y':
            kentucky_df_3 = kentucky_df_2.loc[kentucky_df_2["Month"] >= 7]
            print(kentucky_df_3.head())
        else:
            print("The beginning of the year was kept in the file.\n")


        # Expand the soil data to five minute spacing
        fill_in_soilData = input("Would you like to fill in the missing values of soil data [y/n]? ")
        if fill_in_soilData == 'y' or fill_in_soilData == 'Y':
            f.fix_soil_data(kentucky_df_3, "ST02")
            f.fix_soil_data(kentucky_df_3, "SM02")
        else:
            print("The missing data was kept in the file.\n")

        print(kentucky_df_3.head())

        # Write the dataframe out to a csv
        newPath = f.kentucky_output_file_loc_0 + str(year) + '/'
        if not os.path.exists(newPath):
            os.makedirs(newPath)
        kentucky_df_3.to_csv(newPath + stationID + "_ALL_" + str(year) + ".csv", index=False)

        print(year, "was successfully added")


if __name__ == "__main__":
    main(sys.argv[1:])
