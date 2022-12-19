## Make the process easier by putting everying into functions::

# Outline
'''
| Station | Script | Run Num | Parameter | RMSE | MAPE | MAE |

- Also include lines at the end of each paramter for each station for:
    - Confidence Value = (mean) +/- () * ((std dev) / (sqrt(sample size)))
    - Standard Deviation
    - Mean Values
'''


# import statements
import os
import sys
from datetime import date
import numpy as np
import pandas as pd
import scipy.stats as st   # documentation:: https://www.statology.org/confidence-intervals-python/
import statistics

class SortingModeletOutput2:

    def __init__(self):

        self.cache_loc_0 = "/home/kaleb/Files/MiMa_Software/Meto-Modelet-Suit/Modelet/cache/"
        self.output_folder_loc_0 = "/home/kaleb/Files/FixingData/SortingOutput/SortedOutput/"

    ###########################################################################
    def grabData(self, cache_file_loc_0):

        # initialize empty lists to temporarily hold values
        stationList = []
        scriptList = []
        runList = []
        parameterList = []
        rmseList = []
        mapeList = []
        maeList = []
        # value to pass through functions that indicates the number of files
        numOfFiles = 0

        files = sorted(os.listdir(cache_file_loc_0))
        for file in files:
            if file[-9:-1] == 'error.tx':  # the file is found
                numOfFiles+=1 # add the files to the number of files
                with open((cache_file_loc_0 + file), 'r') as f:
                    runNum = 1

                    file_0 = file.split('_')
                    station = file_0[0]
                    findoutscript = file_0[1]
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
                        line_0 = line.split(' ')
                        metric = line_0[0]

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

                                runNum += 1
                f.close()

        # Write the columns into the dataframe
        # df = pd.DataFrame(data=[stationList, scriptList, runList, parameterList, rmseList, mapeList, maeList], columns=["Station", "Script", "Run Num", "Parameter", "RMSE", "MAPE", "MAE"])
        dictionary = {"Station": stationList,
                      "Run Num": runList,
                      "Script": scriptList,
                      "Parameter": parameterList,
                      "RMSE": rmseList,
                      "MAPE": mapeList,
                      "MAE": maeList}
        df = pd.DataFrame(dictionary)

        # sort the columns of the dataframe
        df.sort_values(by=["Station", "Parameter", "Run Num"], inplace=True)
        return df, numOfFiles

    ###########################################################################
    # pass a dataframe, return a dataframe with empty spaces every time there's a new station / script / parameter
    def putSpaces(self, df):

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


            if i == 1:
                rmseList.append(df.at[0, "RMSE"])
                maeList.append(df.at[0, "MAE"])
                mapeList.append(df.at[0, "MAPE"])
                stationList.append(df.at[0, "Station"])
                scriptList.append(df.at[0, "Script"])
                runList.append(df.at[0, "Run Num"])
                parameterList.append(df.at[0, "Parameter"])

            rmseList.append(df.at[i, "RMSE"])
            maeList.append(df.at[i, "MAE"])
            mapeList.append(df.at[i, "MAPE"])
            stationList.append(df.at[i, "Station"])
            scriptList.append(df.at[i, "Script"])
            runList.append(df.at[i, "Run Num"])
            parameterList.append(df.at[i, "Parameter"])

        dictionary1 = {"Station": stationList,
                       "Script": scriptList,
                       "Run Num": runList,
                       "Parameter": parameterList,
                       "RMSE": rmseList,
                       "MAPE": mapeList,
                       "MAE": maeList}
        df1 = pd.DataFrame(dictionary1)
        return df1


    ###########################################################################
    def findMetrics(self, df1, numOfFiles):
        # print(numOfFiles)
        
        # metric array to hold the calculated metrics for each file
        '''
                        RMSE          |     Mape     |    Mae
        STD   | [file1, file2, file3]
        Mean  | [file1, file2, file3]
        Conf. |

        and so on
        call to the df would look like:
        df.at[metric, mse val][file number]]
        '''
        # metric array = [[[Number of files] Number of MSE values] Number of calculated metrics]
        # currently there's three MSE and three metrics (if we're including the confidence)
        metric_array = [[["                    " for x in range(3)] for y in range(3)] for z in range(numOfFiles)]
        # new_arr = np.arr(metric_array)
        metric_array = np.array(metric_array)
        print(metric_array.shape) # the shape of numpy arrays are opposite to that of python's
    
        # print(np_arr)
        # print(pd.DataFrame(metric_array))# np.nans are instances of floats but the if(val): returns false for np.nans

        totalRmse = []
        totalMape = []
        totalMae = []
        n = 0  # the amount of values the lists have
        currentFileNum = 0 # variable to keep in order to know which level of the array to append the values to

        ## This loop works.. Don't change (except for the part of inserting into the dataframe)
        firstRun = True
        for i in range(0, len(df1)):

            if df1.at[i, "Run Num"] and type(df1.at[i, "RMSE"]) == str:  # if there is a value present. I hope they're all strings because I made the df in earlier function
                totalRmse.append(float(df1.at[i, "RMSE"]))
                totalMape.append(float(df1.at[i, "MAPE"]))
                totalMae.append(float(df1.at[i, "MAE"]))
                n += 1


            # a new script / station / parameter is being tested for. Reset the values and output the averages
            elif n != 0:
                # finding the mean value
                avgRmse = sum(totalRmse) / n
                avgMape = sum(totalMape) / n
                avgMae = sum(totalMae) / n

                # finding the standard deviation
                stdRmse = statistics.pstdev(totalRmse)
                stdMape = statistics.pstdev(totalMape)
                stdMae = statistics.pstdev(totalMae)

                # print(type(stdRmse))

                #######################################
                # Finding a 95% confidence interval of a single run for each mse.
                rmseConf = st.norm.interval(0.95, loc=avgRmse, scale=stdRmse)
                mapeConf = st.norm.interval(0.95, loc=avgMape, scale=stdMape)
                maeConf = st.norm.interval(0.95, loc=avgMae, scale=stdMae)

                # round the values so they'll fit nicely into the array
                # first convert the tuple to a list
                rmseConf = list(rmseConf)
                mapeConf = list(mapeConf)
                maeConf = list(maeConf)

                # round each element of the list
                rmseConf[0] = round(rmseConf[0], 6)
                rmseConf[1] = round(rmseConf[1], 6)
                mapeConf[0] = round(mapeConf[0], 6)
                mapeConf[1] = round(mapeConf[1], 6)
                maeConf[0] = round(maeConf[0], 6)
                maeConf[1] = round(maeConf[1], 6)

                # # convert the list to a string to put into the array
                # rmseConf = str(rmseConf[0]) + ', ' + str(rmseConf[1])
                # mapeConf = str(mapeConf[0]) + ', ' + str(mapeConf[1])
                # maeConf = str(maeConf[0]) + ', ' + str(maeConf[1])

                # print(i)
                # print(currentFileNum)

                # insert the values into the metric_Arr
                metric_array[currentFileNum][0][0] = str(stdRmse) #insert std into rmse
                metric_array[currentFileNum][0][1] = str(stdMape) # insert std into mape
                metric_array[currentFileNum][0][2] = str(stdMae) # insert std into mae
                metric_array[currentFileNum][1][0] = str(avgRmse) # mean of rmse
                metric_array[currentFileNum][1][1] = str(avgMape)# mean of mape
                metric_array[currentFileNum][1][2] = str(avgMae) # mean of mae
                metric_array[currentFileNum][2][0] = str(rmseConf)# confidence of rmse
                metric_array[currentFileNum][2][1] = str(mapeConf)# confidence of mape
                metric_array[currentFileNum][2][2] = str(maeConf)# confidence of mae

                # clear out the values to get ready for the next iterations
                totalRmse = []
                totalMape = []
                totalMae = []
                n = 0
                currentFileNum+=1 # onto the next file

            if i >= len(df1) - 1: # the values at the end of the df weren't getting put into the arr
                # finding the mean value
                print("we came in here\n\n\n\n\n\n\n\n\n\n\n\n\n")
                avgRmse = sum(totalRmse) / n
                avgMape = sum(totalMape) / n
                avgMae = sum(totalMae) / n

                # finding the standard deviation
                stdRmse = statistics.pstdev(totalRmse)
                stdMape = statistics.pstdev(totalMape)
                stdMae = statistics.pstdev(totalMae)

                # print(type(stdRmse))

                #######################################
                # Finding a 95% confidence interval of a single run for each mse.
                rmseConf = st.norm.interval(0.95, loc=avgRmse, scale=stdRmse)
                mapeConf = st.norm.interval(0.95, loc=avgMape, scale=stdMape)
                maeConf = st.norm.interval(0.95, loc=avgMae, scale=stdMae)

                # round the values so they'll fit nicely into the array
                # first convert the tuple to a list
                rmseConf = list(rmseConf)
                mapeConf = list(mapeConf)
                maeConf = list(maeConf)

                # round each element of the list
                rmseConf[0] = round(rmseConf[0], 6)
                rmseConf[1] = round(rmseConf[1], 6)
                mapeConf[0] = round(mapeConf[0], 6)
                mapeConf[1] = round(mapeConf[1], 6)
                maeConf[0] = round(maeConf[0], 6)
                maeConf[1] = round(maeConf[1], 6)

                # # convert the list to a string to put into the array
                # rmseConf = str(rmseConf[0]) + ', ' + str(rmseConf[1])
                # mapeConf = str(mapeConf[0]) + ', ' + str(mapeConf[1])
                # maeConf = str(maeConf[0]) + ', ' + str(maeConf[1])

                # print(i)
                # print(currentFileNum)

                # insert the values into the metric_Arr
                metric_array[currentFileNum][0][0] = str(stdRmse) #insert std into rmse
                metric_array[currentFileNum][0][1] = str(stdMape) # insert std into mape
                metric_array[currentFileNum][0][2] = str(stdMae) # insert std into mae
                metric_array[currentFileNum][1][0] = str(avgRmse) # mean of rmse
                metric_array[currentFileNum][1][1] = str(avgMape)# mean of mape
                metric_array[currentFileNum][1][2] = str(avgMae) # mean of mae
                metric_array[currentFileNum][2][0] = str(rmseConf)# confidence of rmse
                metric_array[currentFileNum][2][1] = str(mapeConf)# confidence of mape
                metric_array[currentFileNum][2][2] = str(maeConf)# confidence of mae

                # clear out the values to get ready for the next iterations
                totalRmse = []
                totalMape = []
                totalMae = []
                n = 0
                currentFileNum+=1 # onto the next file

        return metric_array


    ##########################################################################
    def insertMetrics(self, df, metric_array):
        # initialize lists and other iterative variable to put all the info into a new dataframe

        fileNum = 0
        stationList = []
        scriptList = []
        runNumList = []
        parameterList = []
        rmseList = []
        mapeList = []
        maeList = []
        for i in range(len(df)):


            if float(df.at[i, "Run Num"]) > -100000: # it is not an empty value, insert what's already in the df
                stationList.append(df.at[i, "Station"])
                scriptList.append(df.at[i,"Script"])
                runNumList.append(df.at[i,"Run Num"])
                parameterList.append(df.at[i,"Parameter"])
                rmseList.append(df.at[i,"RMSE"])
                mapeList.append(df.at[i,"MAPE"])
                maeList.append(df.at[i, "MAE"])

            else: # the value is empty, put the metric calculations and the right row names in the "Station" List
                # append the Mean
                stationList.append("Mean")
                scriptList.append(None)
                runNumList.append(None)
                parameterList.append(None)
                rmseList.append(metric_array[fileNum][1][0])
                mapeList.append(metric_array[fileNum][1][1])
                maeList.append(metric_array[fileNum][1][2])

                # append the standard deviation
                stationList.append("STD Dev")
                scriptList.append(None)
                runNumList.append(None)
                parameterList.append(None)
                rmseList.append(metric_array[fileNum][0][0])
                mapeList.append(metric_array[fileNum][0][1])
                maeList.append(metric_array[fileNum][0][2])

                # append the confidence interval
                stationList.append("Confidence")
                scriptList.append(None)
                runNumList.append(None)
                parameterList.append(None)
                rmseList.append(metric_array[fileNum][2][0])
                mapeList.append(metric_array[fileNum][2][1])
                maeList.append(metric_array[fileNum][2][2])


                # append an empty row
                stationList.append(None)
                scriptList.append(None)
                runNumList.append(None)
                parameterList.append(None)
                rmseList.append(None)
                mapeList.append(None)
                maeList.append(None)

                # iterate the file number
                fileNum +=1

            if i == len(df)-1: # if the end of the dataframe is reached, append the values to the arrays
                # append the Mean
                stationList.append("Mean")
                scriptList.append(None)
                runNumList.append(None)
                parameterList.append(None)
                rmseList.append(metric_array[fileNum][1][0])
                mapeList.append(metric_array[fileNum][1][1])
                maeList.append(metric_array[fileNum][1][2])


                # append the standard deviation
                stationList.append("STD Dev")
                scriptList.append(None)
                runNumList.append(None)
                parameterList.append(None)
                rmseList.append(metric_array[fileNum][0][0])
                mapeList.append(metric_array[fileNum][0][1])
                maeList.append(metric_array[fileNum][0][2])

                # append the confidence interval
                stationList.append("Confidence")
                scriptList.append(None)
                runNumList.append(None)
                parameterList.append(None)
                rmseList.append(metric_array[fileNum][2][0])
                mapeList.append(metric_array[fileNum][2][1])
                maeList.append(metric_array[fileNum][2][2])

                # append an empty row
                stationList.append(None)
                scriptList.append(None)
                runNumList.append(None)
                parameterList.append(None)
                rmseList.append(None)
                mapeList.append(None)
                maeList.append(None)


        # put the values into a new df
        dictionary = {"Station" : stationList,
                      "Script" : scriptList,
                      "Run Num" : runNumList,
                      "Parameter" : parameterList,
                      "RMSE" : rmseList,
                      "MAPE" : mapeList,
                      "MAE" : mapeList}
        df1 = pd.DataFrame(dictionary)
        return df1


def main(self):

    # import the class
    s = SortingModeletOutput2()

    # First grab the data and put it into the dataframe
    df, numOfFiles = s.grabData(s.cache_loc_0)

    # Next put some empty spaces when there's a new script / station / whatever
    df = s.putSpaces(df)

    # next we gonna find the metrics
    metric_array = s.findMetrics(df,numOfFiles)

    # next we gonna insert the metrics into a the df by making yet another df
    df = s.insertMetrics(df, metric_array)
    
    # adjust the aligning of the data, align all the numbers to the right and text to the left
    # df.set_table_styles([dict(selector='th', props=[('text-align', 'left')])])
    
    print(df.head())


    # write the df out to a csv
    if not os.path.exists(s.output_folder_loc_0):
        os.makedirs(s.output_folder_loc_0)

    today = date.today()
    d1 = today.strftime("%m-%d-%Y")
    output_file_loc_1 = s.output_folder_loc_0 + "SortedOutput(" + str(d1) + ").csv"

    df.to_csv(output_file_loc_1, index=False)
    print("The file was created")



if __name__ == "__main__":
    main(sys.argv[1:])