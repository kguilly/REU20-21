##########################
# Kaleb Guillot
# Last Edited: 4/9/2022
# This is a file to sort the metric output of the files in the Meto-Modelet-Suit
# Want to produce a table that looks like::
'''
| Station | Script | Run Num | Parameter | RMSE | MAPE | MAE |

- Also include lines at the end of each paramter for each station for:
    - Best run
    - Standard Deviation
    - Mean Values
'''
import os
from datetime import date

import numpy as np
import pandas as pd


# Point at the cache folder in the Meto-Modelet-Suit
cache_file_loc_0 = "/home/kaleb/Files/MiMa_Software/Meto-Modelet-Suit/Modelet/cache/"
# Name and locate a desired output folder
output_file_loc_0 = "/home/kaleb/Files/MiMa_Software/Meto-Modelet-Suit/Modelet/SortedOutput/"



# Initialize main lists to hold the values that will be placed in the dataframe
stationList = []
scriptList = []
runList = []
parameterList = []
rmseList = []
mapeList = []
maeList = []

files = sorted(os.listdir(cache_file_loc_0))

for file in files:

    if file[-9:-1] == 'error.tx': # find the appropriate file

        # initialize some temp arrays to store this file's data
        # all lists should be lists of strings to have the interval for standard deviation
        stationListTemp = []
        scriptListTemp = []
        runListTemp = []
        parameterListTemp = []
        rmseListTemp = []
        mapeListTemp = []
        maeListTemp = []

        # grab some info from the file name
        file_0 = file.split('_')
        station = file_0[0]
        findScript = file_0[1]

        if findScript[0] == 'M':
            if findScript[0:4] == "MiMa":
                script = findScript[0:4]
                parameter = findScript[4:8]
            elif findScript[0:5] == "Micro":
                script = findScript[0:5]
                parameter = findScript[5:9]
        else:
            script = file_0[1]
            parameter = file_0[3]

        # open the file, perform calculations, then add to the main lists
        with open((cache_file_loc_0 + file), 'r') as f:
            runNum = 1 # var for the runnum column

            for line in f:
                line_0 = line.split(' ')
                metric = line_0[0]

                if metric != '\n':
                    line_1 = line_0[1].split(',')
                    value = line_1[0]

                    if metric == "RMSE":
                        rmseListTemp.append(str(value))
                    elif metric == "MAE":
                        maeListTemp.append(str(value))
                    elif metric == "MAPE":
                        mapeListTemp.append(str(value))
                        
                    # append the rest of the stuff to their respective lists
                    stationListTemp.append(station)
                    scriptListTemp.append(script)
                    runListTemp.append(str(runNum))
                    parameterListTemp.append(parameter)

                    runNum+=1

        f.close()

        # send temp lists to other functions for calculations to be performed 
            # make sure the list is at least a single element long before doing so
        # then add an empty space at the end of the temp list
        # append the temp list to the original list
        # write the lists to a dataframe
            # then out to a csv
            
        if runNum >= 2: # condition for list length


                    