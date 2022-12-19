##########################
# Kaleb Guillot
# Last Edited: 2/18/2022
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

cache_file_loc_0 = "/home/kaleb/Files/MiMa_Software/Meto-Modelet-Suit/Modelet/cache/"
output_file_loc_0 = "/home/kaleb/Files/MiMa_Software/Meto-Modelet-Suit/Modelet/SortedOutput/"




stationList = []
scriptList = []
runList = []
parameterList = []
rmseList = []
mapeList = []
maeList = []

files = sorted(os.listdir(cache_file_loc_0))
for file in files:
    # print(file[-9:-1])
    if file[-9:-1] == 'error.tx': # the file is found
        
        

        with open((cache_file_loc_0 + file), 'r') as f:
            runNum = 1

            file_0 = file.split('_')
            station = file_0[0]

            findoutscript = file_0[1]
            # print(findoutscript)
            if findoutscript[0] == 'M':
                if findoutscript[0:4] == "MiMa":
                    script = findoutscript[0:4]
                    parameter = findoutscript[4:8]
                elif findoutscript[0:5] == "Micro":
                    script = findoutscript[0:5]
                    parameter = findoutscript[5:9]
            else:
                script = file_0[1]
                parameter = file_0[3]

            for line in f:
                # print(line)
                line_0 = line.split(' ')
                metric = line_0[0]

                # print(line_0)
                if line_0[0] != '\n':
                    line_1 = line_0[1].split(',')
                    value = line_1[0]

                    if metric == "RMSE":
                        rmseList.append(value)
                    elif metric == "MAE":
                        maeList.append(value)
                    elif metric == "MAPE":
                        mapeList.append(value)
                        
                        # append the rest of the stuff to their respective lists
                        stationList.append(station)
                        scriptList.append(script)
                        runList.append(runNum)
                        parameterList.append(parameter)
                        
                        runNum+=1
        f.close()



# Write the columns into the dataframe
# df = pd.DataFrame(data=[stationList, scriptList, runList, parameterList, rmseList, mapeList, maeList], columns=["Station", "Script", "Run Num", "Parameter", "RMSE", "MAPE", "MAE"])
dictionary = {"Station": stationList,
            "Run Num" : runList,
            "Script" : scriptList,
            "Parameter" : parameterList,
            "RMSE" : rmseList,
            "MAPE" : mapeList,
            "MAE" : maeList}
df = pd.DataFrame(dictionary)

# sort the columns by the station, then by the run Number
df.sort_values(by=["Station", "Parameter", "Run Num"], inplace=True)


# empty all the arrays, then copy the values over to the new lists (including empty lines)
stationList = []
runList = []
scriptList = []
parameterList = []
rmseList = []
mapeList = []
maeList = []

for i in range(1, len(df)):
    # if df.at[i, "Station"] != df.at[i-1, "Station"] and df.at[i-1, "Station"] != None:
    if df.at[i, "Run Num"] == 1: 
        # insert an empty row for every new script / station / parameter.
        rmseList.append(None)
        maeList.append(None)
        mapeList.append(None)
        stationList.append(None)
        scriptList.append(None)
        runList.append(None)
        parameterList.append(None)

        # another one to be safe
        rmseList.append(None)
        maeList.append(None)
        mapeList.append(None)
        stationList.append(None)
        scriptList.append(None)
        runList.append(None)
        parameterList.append(None)

   

    if i == 1:
        rmseList.append(df.at[0,"RMSE"])
        maeList.append(df.at[0,"MAE"])
        mapeList.append(df.at[0,"MAPE"])
        stationList.append(df.at[0,"Station"])
        scriptList.append(df.at[0,"Script"])
        runList.append(df.at[0,"Run Num"])
        parameterList.append(df.at[0,"Parameter"])

    rmseList.append(df.at[i,"RMSE"])
    maeList.append(df.at[i,"MAE"])
    mapeList.append(df.at[i,"MAPE"])
    stationList.append(df.at[i,"Station"])
    scriptList.append(df.at[i,"Script"])
    runList.append(df.at[i,"Run Num"])
    parameterList.append(df.at[i,"Parameter"])


dictionary1 = {"Station": stationList,
            "Script" : scriptList,
            "Run Num" : runList,
            "Parameter" : parameterList,
            "RMSE" : rmseList,
            "MAPE" : mapeList,
            "MAE" : maeList}
df1 = pd.DataFrame(dictionary1)
# df1.replace(None, np.nan, inplace=True)
# df1.replace(pd.NA, np.nan, inplace=True)


# Loop through the dataframe and for each station, script, and parameter, find the:
#   - Best run
#   - Mean value
#   - standard deviation = sqrt(1/N(sum(x(i)-(mu))^2))
totalRmse = []
totalMape = []
totalMae = []
n = 0 # the amount of values the lists have

## problem:
#       - saying that when we get back to the first run number of the script has problems, doesn't take into account
#       - situations where there's only one run. Going to have to replace all the null values with np.nan and then check for that
# - the else block will be an else if the iteration before that has a value and it has a station, meaning its not
# - a std dev or mean
# 

print(df1)
######### Current problem:: the output is not sorted, puts the values for the second mean and mse calculations 
# at the top instead of at the correct index. Work to get linux partition back working
firstRun = True
for i in range(0, len(df1)):
    
    if df1.at[i, "Run Num"] and type(df1.at[i, "RMSE"]) == str: # if there is a value present
        totalRmse.append(float(df1.at[i, "RMSE"]))
        totalMape.append(float(df1.at[i,"MAPE"]))
        totalMae.append(float(df1.at[i,"MAE"]))
        n+=1
        

    # a new script / station / parameter is being tested for. Reset the values and output the averages
    elif n != 0:
        print('hey big boy')
        # finding the mean value
        avgRmse = sum(totalRmse) / n
        avgMape = sum(totalMape) / n
        avgMae = sum(totalMae) / n

        # finding the standard deviation
        stdRmseArr = []
        stdMapeArr = []
        stdMaeArr = []
        for i in range(len(totalRmse)):
            stdRmseArr.append((totalRmse[i] - avgRmse)**2)
            stdMapeArr.append((totalMape[i] - avgMape)**2)
            stdMaeArr.append((totalMae[i] - avgMae)**2)
        stdRmse = (1/n * sum(stdRmseArr))**(1/2)
        stdMape = (1/n * sum(stdMapeArr))**(1/2)
        stdMae = (1/n * sum(stdMaeArr))**(1/2)


        #Insert mean into the dataframe
        df1.loc[i] = ["MEAN MSE", None , None , None, avgRmse, avgMape, avgMae]
        
        #insert std into the dataframe
        df1.loc[i+1] = ["STD DEV", None, None, None, stdRmse, stdMape, stdMae]
        df1.index = df1.index+2
        df1 = df1.sort_index()


        # clear out the values to get ready for the next iterations
        totalRmse = []
        totalMape = []
        totalMae = []
        n=0
        i+=1 # skip over the first iteration of the next loop

    #if i == len(df1): # if the end of the file is reached, concatenate the values


            
            



print(df1)
# export
# handle if the location does not exist
if not os.path.exists(output_file_loc_0):
    os.makedirs(output_file_loc_0)

today = date.today()
d1 = today.strftime("%m-%d-%Y")
output_file_loc_1 = output_file_loc_0 + "SortedOutput(" + str(d1) + ").csv"

df1.to_csv(output_file_loc_1, index=False)
print("The file was created")
