# Kaleb Guillot
# 1/18/2022
# This is a file to add columns of parameters to the Kentucky data. These columns are: PRES,
# DayOfTheYear, SM02, and ST02

'''     Outline of Code:
            - Open the files
            - Functions:
                - Separate the pressure data into individual years
                - Add day of the year column:
                    - grab the day, month, year columns
                    - combine to find day of the year
                    - add to array
                    - output array to file
                - Add the PRES column:
                    - grab the utme and pres columns in the pressure file
                    - find the corresponding day of the year for each utme line
                    - put the time and pressure data into a 2-d array
                    - Loop through the kentucky file
                        - for each line of the kentucky file, loop through the 2-d array of
                        pressure data
                            - if the year, day, and time of the kentucky file matches the
                            pressure data's, put the pressure data. Else, put "N/A". Add these
                            values to a list
                                (will the MiMa file read N/A?)
                    - Add the list to the kentucky file, header=PRES
                - Add the ST02 column
                - Add the PRES column
            - Function calls:
                - separate the pressure data
                - Loop for three years
                    - add the columns with their corresponding years as inputs '''
# Potential additions
#       - instead of calling all the arguments in the functions, just call self
#       - Add years to the end of the files, pass the years to the functions, and concatenate
#       the names like how it's done in other files
#           - Will need to do the same with output files
#       - make arguments for the user to enter specific dates and such
# This is a file to fix the Kentucky data that has not been previously sanitized. 
# The script takes a .csv Kentucky file and adds the columns: 
    # - DayOfTheYear
    # - PRES
    # - SM02
    # - ST02


from genericpath import exists
import sys
from calendar import month
import csv
import os
from tkinter import N
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
        self.kentucky_station_csv = "BMBL_Barbourville-3-E_Knox"
        self.kentucky_station_ID = "BMBL"

        # For these parameters, point at the folder that holds the years of data
        self.kentucky_file_loc_0 = "/home/kaleb/Files/FixingData/TestBed/KentuckyData/" #point at the folder containing the years
        self.st02_file_loc_0 = "/home/kaleb/Files/FixingData/TestBed/SOILDATA/ST02/"
        self.sm02_file_loc_0 = "/home/kaleb/Files/FixingData/TestBed/SOILDATA/SM02/"

        # Point at the exact file
        self.pres_file_loc_0 = "/home/kaleb/Files/FixingData/TestBed/BMBL_pressureData.csv"

        # Point at the folder you want to put it in
        self.kentucky_output_file_loc_0 = "home/kaleb/Files/FixingData/TestBed/KentuckyOutput/"
        self.pres_output_loc_0 = "/home/kaleb/Files/FixingData/TestBed/PressureOutput/"


    ##########################################################################
    # Function that separates the pressure data into individual years
    def sep_pres_data(self):

        input_file = pd.read_csv(self.pres_file_loc_0)

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

            # print("this year: ", year, "\nnext year: ", next_year, "\n")

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

        # print("Days::\n" ,days)
        # print("Months::\n", months)
        # print("Year::\n", year)

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
        # kentucky_file_loc, kentucky_station_csv, year, df, param):

        kentucky_dayoftheyear = kentucky_df["DayOfTheYear"]
        kentucky_hour = kentucky_df["Hour"]
        kentucky_minute = kentucky_df["Minute"]

        data_dayofyear = param_df["DayOfTheYear"]
        data_hour = param_df["Hour"]
        data_minute = param_df["Minute"]
        data_list = param_df[param]

        ## Problem with the parameter data. Hours and minutes are strings while the kentucky's are ints
        if isinstance(data_hour[1], str):
            data_hour = self.cleanse_data(data_hour)
        if isinstance(data_minute[1], str):
            data_minute = self.cleanse_data(data_minute)

        ### set cleanse_data to false after and then test the other lists

        dataToKentucky = [None] * len(kentucky_minute)
        for i in range(len(kentucky_dayoftheyear)):
            for j in range(len(data_list)):
                temp = len(data_list) # can remove when done
                if (kentucky_dayoftheyear[i] == data_dayofyear[j]):
                    if (kentucky_hour[i] == data_hour[j]):
                        if (kentucky_minute[i] == data_minute[j]):
                            dataToKentucky[i] = data_list[j]
                            data_list.pop(j) # to try and improve the time ### may need to remove
                            break

        kentucky_df.insert(2, param, dataToKentucky)

        # newkentuckyfile_loc = "/NewKentuckyFiles/"+year+'/New_'+kentucky_station_csv
        # kentucky_df.to_csv(newkentuckyfile_loc)

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
                # print(y)
                y = y[0] + y[1]
            # replace
            newArr.append(int(y))

        return newArr

    ###############################################################################
    # Add the pressure data (PRES column)
    def add_pres(self, year, kentucky_df):

        # (kentucky_station_ID, kentucky_station_csv, kentucky_file_loc_0, pressure_file_loc_0, year)

        pressure_file_loc = self.pres_output_loc_0 + str(year) + '/' + self.kentucky_station_ID + '_' + str(
            year) + "PRESdata.csv"
        pressure_file = pd.read_csv(pressure_file_loc)

        # Grab the pressure column and utme
        utme = pressure_file["UTME"]
        pres_data = pressure_file["PRES"]

        # print("UTME Data:: \n", utme)

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
        ############# troubleshooting purposes
        print("\n\n\nThe data type of the data is::\n ", type(pres_data_arr[6]))
        # df = pd.DataFrame([pres_dayoftheyear_arr, pres_hour_arr, pres_minute_arr, pres_data_arr], columns=["DayOfTheYear", "Hour", "Minute", "PRES"])
        df = pd.DataFrame({"DayOfTheYear": pres_dayoftheyear_arr,
                           "Hour": pres_hour_arr,
                           "Minute": pres_minute_arr,
                           "PRES": pres_data_arr})

        # add_column(self.kentucky_file_loc_0, self.kentucky_station_csv, year, df, "PRES")
        # self.add_column(self, "PRES", df, kentucky_df)
        self.add_column("PRES", df, kentucky_df)
        return None

    ##########################################################################
    # Add the ST02 column
    def add_st02(self, year, kentucky_df):
        # (kentucky_station_ID, kentucky_station_csv, kentucky_file_loc_0, st02_file_loc_0, year):

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
                            filename = "30_" + self.kentucky_station_ID + ".json"
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
            time_0 = date[1].split(':')

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

        # add_column(self.kentucky_file_loc_0, self.kentucky_station_csv, year, df, "ST02")
        # self.add_column(self, "ST02", df, kentucky_df)
        self.add_column("ST02", df, kentucky_df)

        return None

    ###########################################################################
    # Add the SM02
    def add_sm02(self, year, kentucky_df):
        # kentucky_station_ID, kentucky_station_csv, kentucky_file_loc_0, sm02_file_loc_0, year):

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
                            fileName = "30_" + self.kentucky_station_ID + ".json"
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
            time_0 = date[1].split(':')

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

        # self.add_column(kentucky_file_loc_0, kentucky_station_csv, year, df, "SM02")
        # add_column(kentucky_file_loc_0, kentucky_station_csv, year, df, "SM02")
        # self.add_column(self,"SM02", df, kentucky_df)

        self.add_column("SM02", df, kentucky_df)
        return None


##########################################################################
## Configuring the main functionality of the codee
def main(self):
    parser = argparse.ArgumentParser(description="What years do you want to parse through?")
    parser.add_argument('--sy', default=2018, type=int, help="The year to start, formatted as: yyyy. Ex. 2018")
    parser.add_argument('--ey', default=2018, type=int, help="The end year, this year will be included")

    args = parser.parse_args()

    by = args.sy
    ey = args.ey

    year_range = ey - by

    f = DataFixing()

    # Below line is commented out to save time while troubleshooting
    # f.sep_pres_data()

    for i in range(0, year_range + 1):
        year = by + i

        # First load the data from the kentucky file into a pandas dataframe
        kentucky_df = pd.read_csv(f.kentucky_file_loc_0 + str(year) + '/' + f.kentucky_station_csv + '.csv')

        # Add the day of the year column to the kentucky files
        f.add_dayoftheyear(year, kentucky_df)
        print(kentucky_df.head())  # debugging purposes

        # add the pressure data
        f.add_pres(year, kentucky_df)
        print(kentucky_df.head())

        # add the st02 data
        f.add_st02(year, kentucky_df)
        print(kentucky_df.head())

        # add the sm02 data
        f.add_sm02(year, kentucky_df)
        print(kentucky_df.head())

        # Write the dataframe out to a csv
        kentucky_df.to_csv(f.kentucky_output_file_loc_0 + str(year) + '/New_' + f.kentucky_station_csv)

        print(year, "was successfully added")


if __name__ == "__main__":
    main(sys.argv[1:])

# python DataFixing2.py --sy=2018 --ey=2018