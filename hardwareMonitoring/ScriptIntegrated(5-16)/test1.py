import tensorflow as tf
import os
import subprocess

# get the hardware and software memory stats, send them out to a csv file 
os.system("free -s 1 ; cpu.csv") 
os.system("nvidia-smi pmon ; gpu.csv")
# they run until I tell them to stop, how do I get them to run only for the duration of the file? 

gpus = tf.config.list_physical_devices('GPU')
print("Checking gpus: ", gpus)



cmd = 'cd .. ; cd .. ; ls'

os.system(cmd)
logical = tf.config.list_logical_devices('GPU')
physical = tf.config.list_physical_devices('GPU')
print("Logical:: ", logical, "\nPhysical: ", physical)