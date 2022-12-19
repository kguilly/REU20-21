# This is a file to test the parts of python's syntax that I have forgotten

from cgi import test
import datetime
from importlib.metadata import files
import json
import pandas as pd
import numpy as np
month = 2
day = 3
year = 2020
date = str(month) + '-'+str(day)+'-'+str(year)

dayofyear = datetime.datetime.strptime(date, '%m-%d-%Y').timetuple().tm_yday

print(dayofyear)

##########################################################################

#import numpy as np

preshua = [1,2,3,4,5,6]
day = [7,8,9,10,11]
bofum = [preshua, day]

# bofum_transposed = [[row[i] for row in bofum] for i in range(len(bofum[0]))]
# bofum_transposed = [preshua]; [day]

print("\n\n\nTesting array functionality::\n",bofum)
# print("\n\nThe Transposed array::", bofum_transposed)
print("\n\n\n")                                #   row,col
print("This should print out 5 then 10::\n", bofum[0][4], "\n", bofum[1][3])
'''
arr = np.array([preshua, day], np.int32)
print(arr.shape)
print(arr.dtype)'''

##########################################################################
arr = [i for i in range(0,10)]
another_arr = [0] * 10
print("\n\n\n", arr, "\n\n", another_arr)


##########################################################################
print("\n\n\n##########################\nTesting OS usefulness")

import os



# print(month_folders)
# for months in month_folder:
#     newPath = file_path+months+'/'
#     day_folders = sorted(os.listdir(newPath))
#     for days in day_folders:
#         filepath = newPath + days + '/'
#         print("\nDays::", days)
#         print("\nFile Path",filepath)
df = pd.DataFrame(columns=['Date', "Value"])
date_arr = []
val_arr = []
file_path = "/home/kaleb/Files/FixingData/SOILDATA/ST02/2018/"
month_folder = sorted(os.listdir(file_path))

for months in month_folder:
    file_path = "/home/kaleb/Files/FixingData/SOILDATA/ST02/2018/"
    newPath = file_path + months + '/'
    if os.path.exists(newPath):
        day_folders = sorted(os.listdir(newPath))
        print("Months::",months)

        for days in day_folders:
            day_path = newPath + days + '/'
            if os.path.exists(day_path):
                idk = sorted(os.listdir(day_path))
                # print(idk)    
                # for f in day_path:
                #     jsonFilePath = day_path + f
                #     print(jsonFilePath)
                #     if (jsonFilePath==day_path+"30_ZION.json"):
                #         print(jsonFilePath)
                for jsonFiles in idk:
                    file_path = day_path + jsonFiles
                    if jsonFiles == '30_BMTN.json':
                        # print(jsonFiles)
                        print(file_path)
                        with open(file_path) as f:
                            data =(json.load(f))
                            l1 = list(data.values())
                            np_arr = np.array(l1)
                            transpose = np_arr.T
                            transpose_list = transpose.tolist()
                            # print(transpose_list)

                            for date, val in transpose_list:
                                date_arr.append(date)
                                val_arr.append(val)

                            # print(l1)
                            # for date in l1[:][0]:
                            #     date_arr.append(date)
                            # for val in l1[:][1]:
                            #     val_arr.append(val)
                            # print(date_arr)
                            # df2 = pd.DataFrame([date_arr, val_arr], columns=["Date", "Values"])
                            # print(df2)
                            # df["Date"].append(df2["Date"])
                            # df["Values"].append(df2["Values"])
                            # Need to figure out how to get rid of the column headers for
                            # all the iterations, then add my own singular header at the end when ready
                            # blah = json.loads(data)
                            #######################
                            # print(data)
                            # date_arr.append(data[1:]['date'])
                            # arr = zip(data[0], data[1])
                            # print(arr)
                            # df.append(data, ignore_index=True)
                        # split the data up into individual columns to be added to our dataframe
                        # could use two separate arrays


# Make the arrays into a dataframe, transpose them first
# np_date_arr = np.array(date_arr)
# transpose1 = np_date_arr.T
# t_date_arr = transpose1.tolist()

# np_val_arr = np.array(val_arr)
# transpose2 = np_val_arr.T
# t_val_arr = transpose2.tolist()
# df = pd.DataFrame([t_date_arr, t_val_arr], columns=["Date", "Values"])
# print(df.head)

# print(l1)
# print("Date Array::\n",date_arr)
# print("\n\nValues Array::\n", val_arr)


# print(df)
# df = pd.DataFrame(data, columns=["Date", "SM02"])
# print(df)
# a = 10
# b = 11
# testingggg = a > b ? a : b

# print("\nTesting::\n",testingggg)

# for folder in month_folders:
#     if(folder== ("0"+str(i for i in range(1,10)) or (i for i in range(11,13)))):
#         day_folders = os.listdir(folder)
#         print(day_folders)
#         for day in day_folders:
#             print(day)
#             if(day == "0"+str(i for i in range(0,32))):
#                 files = os.listdir(day)
#                 print("\nDay::\n",day)
#                 print("\nFiles::\n",files)


#                 if(files=="30_ZION.json"):
#                     print("found one")


# for root,dirs,files in os.walk(file_path):
  #  print(dirs)


#########################################################################$
print("\n\n\n\n\n\n\nTESTING searching through the folders::")
file_path = "/home/kaleb/Files/FixingData/SOILDATA/ST02/2018/"
month_folder = sorted(os.listdir(file_path))

for months in month_folder:
    newPath = file_path + months + '/'
    if os.path.exists(newPath):
        day_folders = sorted(os.listdir(newPath))
        print("Months::",months)
