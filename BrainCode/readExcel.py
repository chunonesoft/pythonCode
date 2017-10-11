#coding=utf-8
import csv
import codecs

def readExcel():
     with open('EEG.csv') as csvfile:
         reader = csv.reader(csvfile)
         rows = [row for row in reader]
         return rows
readExcel()
