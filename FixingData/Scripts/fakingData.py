# fakingData

'''
This is a file to fill in missing values for a select station
'''

from os import stat
import pandas as pd


kentucky_data_loc = "/home/kaleb/Files/MiMa_Software/Meto-Modelet-Suit/data/Kentucky_Data/"
station = "QKSD"

# find each file
missingCsv = kentucky_data_loc + "2018/"+station+"_ALL_2018.csv"
newCSV = kentucky_data_loc + "2019/"+station+"_ALL_2019.csv"

# put each into a dataframe
missingCsv_file = pd.read_csv(missingCsv)
newCSV_file = pd.read_csv(newCSV)

# replace old
missingCsv_file['PRES'] = newCSV_file['PRES']

# write out to file
missingCsv_file.to_csv(missingCsv, index=False)

