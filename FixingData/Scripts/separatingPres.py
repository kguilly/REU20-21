''' Outline:
        - read
        - put data in dataframe
        - initialize arrays to store data
        - initialize count to store how many years the data has
        - loop thru 
            - read the file, append to array.
            - when you hit a new year, write the file out 
        - write out to multiple files'''

from re import X
import pandas as pd
import os


input_file_loc = "/home/kaleb/Files/FixingData/CSVs/BMBL_pressureData.csv"
output_file_loc_0 = "/home/kaleb/Files/FixingData/CSVs/PressureData/"



input_file = pd.read_csv(input_file_loc)

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
        utme[i+1]
    except:
        sameyear = False
        next_year = 0
    else:
        next_date_0 = (utme[i+1].split(' '))
        next_date_1 = (next_date_0[0].split('-'))
        next_year = next_date_1[0]    
   
    
    if(next_year!=year):
        sameyear = False

    # print("this year: ", year, "\nnext year: ", next_year, "\n")


    #if the next iteration does not equal the first station, write out the array and
    # clear it
    if(sameyear == False):
        output_file_loc =  output_file_loc_0 + stid[0] + year + "_pressureData.csv"
        with open(output_file_loc, 'w') as file:
    
            data = {"NET": (net_arr[i] for i in range (0, len(net_arr))), 
                    "STID" : (stid_arr[i] for i in range (0, len(net_arr))),
                    "UTME" : (utme_arr[i] for i in range(0,len(utme_arr))),
                    "PRES" : (pres_arr[i] for i in range(0,len(pres_arr)))}
            df = pd.DataFrame(data)
            print(df, '\n')
            #df.columns = ["NET", "STID","UTME","PRES"]
            df.to_csv(output_file_loc)

        net_arr = []
        stid_arr = []
        utme_arr = []
        pres_arr = []

    
