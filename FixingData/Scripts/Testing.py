import os
import json
import numpy as np
import pandas as pd

file_path = "C:/Users/19854/Desktop/School Files/Year 3, Semester 2/REU/FixingData/TestBed/SOILDATA/SM02/2018/01/01/30_PRNC.json"
date_arr = []
val_arr = []
with open(file_path) as f:
    data = json.load(f)
    l1 = list(data.values())
    np_arr = np.array(l1)
    transpose = np_arr.T
    transpose_list = transpose.tolist()
    for date, val in transpose_list:
        date_arr.append(date)
        val_arr.append(val)

print("The List is::\n\n", l1)
print("The dates are:\n", date_arr)
print("The values: \n", val_arr)


# Now test putting the data in order
file_path_1 = "C:/Users/19854/Desktop/School Files/Year 3, Semester 2/REU/FixingData/TestBed/SOILDATA/SM02/2018/"
month_folder = sorted(os.listdir(file_path_1))
# print(month_folder)
for months in month_folder:
    new_path = file_path_1 + months + '/'
    # print("New Path: ", new_path)
    if os.path.exists (new_path):
        # print(new_path)
        day_folders = sorted(os.listdir(new_path))

        for days in day_folders:
            day_path = new_path + days + '/'
            if os.path.exists(day_path):
                # print("Day Path: ", day_path)
                file = sorted(os.listdir(day_path))
                # I think it works how its supposed to, I'll stop here


##########################################################################
# Rewriting the loops to minimize the memory complexity with for each loops
kentucky_dayoftheyear = [0,1,2,3,4,5,6,6,6,6,6,6,6,6,67,7,7,77,7,7,7,7,7,7,7,7,7,7,4,567,65,65]
kentucky_hour =         [0,1,2,3,4,5,6,7,8,867,6,7,8,67,6,7,8,67,6,657,8,6,4545,6545,65,56,7,5,67,22,456,76]
kentucky_minute =       [0,1,2,3,4,5,5,6,7,78,6,56,67,7,6,6,7,6,65,7,56,5,7,78,7,76,8,76,673,6,7,5]

data_dayofyear =        [0,1,2,3,4,5,5,6,7,6,6,78,7,6,56,5,7,7,56,5,6,78,7,5,45,65,67,5,6,7,5,7]
data_hour =             [0,1,2,3,4,5,5,6,7,5,5,6,67,5,6,65,6,7,8,9,7,67,6,78,8,6,5,76,8,8,6,5]
data_minute =           [0,1,2,3,6,7,8,78,6,5,4,4,6,7,8,67,5,4,56,7,8,65,4,4,6,7,87,89,8,6,55,567]
data_list =             [0,1,2,3,4,5,5,6,7,67,5,8,7,56,5,6,8,86,56,7,6,5,6,8,6,88,678,68776,55,56,78,65]



dataToKentucky = [None] * len(kentucky_minute)

from datetime import datetime

start1 = datetime.now().time()

for kday in kentucky_dayoftheyear:
    for dday in data_dayofyear:
        if kday == dday:
            for khour in kentucky_hour:
                for dhour in data_hour:
                    if khour == dhour:
                        for kmin in kentucky_minute:
                            for dmin in data_minute:
                                if kmin == dmin:
                                    dataToKentucky[kentucky_minute.index(kmin)] = float(data_list[data_minute.index(dmin)])

end1 = datetime.now().time()

print("\n\n\nFirst time: \nStart: ", start1, "\nEnd: ", end1)
print("First arr: ", dataToKentucky)
# clear the array
dataToKentucky = [None] * len(kentucky_minute)


start2 = datetime.now().time()
for i in range(len(kentucky_dayoftheyear)):
    for j in range(len(data_list)):
        # temp = len(data_list) # can remove when done
        if (kentucky_dayoftheyear[i] == data_dayofyear[j]):
            if (kentucky_hour[i] == data_hour[j]):
                if (kentucky_minute[i] == data_minute[j]):
                    dataToKentucky[i] = float(data_list[j])
                    # data_list.pop(j) # to try and improve the time ### may need to remove
                    break # value to be added to the list has been found, break out of the loop searching through the data list


end2 = datetime.now().time()

print("Second time: \nStart: ", start2, "\nEnd: ", end2)
print("Second arr: ", dataToKentucky)

l1 = len(kentucky_dayoftheyear)
l2 = len(kentucky_hour)
l3 = len(kentucky_minute)
l4 = len(data_dayofyear)
l5 = len(data_hour)
l6 = len(data_minute)
l7 = len(data_list)
k_df = pd.DataFrame({"Day of the Year": kentucky_dayoftheyear,
                     "Hour": kentucky_hour,
                     "Minute": kentucky_minute})
d_df = pd.DataFrame({"Day of the Year": data_dayofyear,
                     "Hour": data_hour,
                     "Minute": data_minute,
                     "Value": data_list})

#print("\n\nLast test", k_df["Day of the Year", "Hour", "Minute"].isin(d_df,["Day of the Year", "Hour", "Minute"]))

#k_df["New Column"] = np.where([k_df["Day of the Year"]==d_df["Day of the Year"], k_df["Hour"]==d_df["Hour"]], "truuuu", "nahhhhh")
new_df = pd.DataFrame()
new_df["MatchingDays"] = np.where(k_df["Day of the Year"]==d_df["Day of the Year"], 1, 0)
new_df["MatchingHours"] = np.where(k_df["Hour"] == d_df["Hour"], 1, 0)
new_df["MatchingMinues"] = np.where(k_df["Minute"] == d_df["Minute"], 1, 0)

#if all the columns in a row have matches, write the value to it
new_arr = []
for i in range(0,len(new_df)):
    if new_df.at[i,"MatchingDays"] == new_df.at[i,"MatchingHours"] == new_df.at[i,"MatchingMinues"] == 1:
        new_arr.append(data_list[i])
    else:
        new_arr.append(None)

new_df.insert(0, "does this work?", new_arr)


print(new_df)
print(len(new_df))

# new_arr = np.where(kentucky_dayoftheyear == data_dayofyear, "truuu", "nahhh")
# print(new_arr)

#########################################################################################################
# have to make a section of add_column that takes pandas dataframes of different sizes and matches their sizes,
# then sorts then by the dayoftheyear, then by the hour, then by the minute
'''
variables are::
kentucky_dayoftheyear = [0,1,2,3,4,5,6,6,6,6,6,6,6,6,67,7,7,77,7,7,7,7,7,7,7,7,7,7,4,567,65,65]
kentucky_hour =         [0,1,2,3,4,5,6,7,8,867,6,7,8,67,6,7,8,67,6,657,8,6,4545,6545,65,56,7,5,67,22,456,76]
kentucky_minute =       [0,1,2,3,4,5,5,6,7,78,6,56,67,7,6,6,7,6,65,7,56,5,7,78,7,76,8,76,673,6,7,5]

data_dayofyear =        [0,1,2,3,4,5,5,6,7,6,6,78,7,6,56,5,7,7,56,5,6,78,7,5,45,65,67,5,6,7,5,7]
data_hour =             [0,1,2,3,4,5,5,6,7,5,5,6,67,5,6,65,6,7,8,9,7,67,6,78,8,6,5,76,8,8,6,5]
data_minute =           [0,1,2,3,6,7,8,78,6,5,4,4,6,7,8,67,5,4,56,7,8,65,4,4,6,7,87,89,8,6,55,567]
data_list =             [0,1,2,3,4,5,5,6,7,67,5,8,7,56,5,6,8,86,56,7,6,5,6,8,6,88,678,68776,55,56,78,65]

k_df = pd.DataFrame({"Day of the Year": kentucky_dayoftheyear,
                     "Hour": kentucky_hour,
                     "Minute": kentucky_minute})
d_df = pd.DataFrame({"Day of the Year": data_dayofyear,
                     "Hour": data_hour,
                     "Minute": data_minute,
                     "Value": data_list})
'''

# First work on sorting them by the descending columns, then work on filling in missing data (will need to space them
# out by 5 minutes
print("\n\n\nFirst:\n", d_df)
d_df.sort_values(by=["Day of the Year", "Hour", "Minute"], inplace=True) #### this WORKS lego

print("\nSecond:\n",d_df)

'''
Now we have to work on filling in some missing values to match the kentucky data
- Method of "expandToMinutely"
      - make an empty list
      - for 24 hours
        - for 60 minutes of the hour
            - append the hour and minute to the list
    - put the list into a dataframe
    - use pd.merge(first_df, file_df, how='left', on=['Hour']) to do so
    - use .fillna(method = 'ffill', inplace=True)
'''
newList = []
for day in range(1,365):
    for hour in range(24):
        for minute in range(0,61,5): #5 minute spacing
            newList.append([day, hour, minute])
new_df_1 = pd.DataFrame(newList, columns=["Day of the Year","Hour", "Minute"])
new_df_2 = pd.merge(new_df_1, d_df, how='left', on=["Day of the Year"])
new_df_2.fillna(method='ffill',inplace=True)

print("\nThird:\n", new_df_2[110100:110200])