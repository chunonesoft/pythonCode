import csv
import numpy as np

def readData(excelFile):
    list1 = []
    list2 = []
    a = np.array([4,512])
    with open('EMO_EEG_Data.csv','rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            list1.append(row[3])
            list2.append(row[2])
    list1.remove('F3')
    list2.remove('F7')
    print list1[0:511]
    print list2[0:511]
    a = [list1[0:511],list2[0:511]]
    print a
readData('1')