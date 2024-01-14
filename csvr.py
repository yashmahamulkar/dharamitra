import csv
import pandas as pd
 
# opening the CSV file
with open('clean.csv','r')as file:
   
  # reading the CSV file
  csvFile = csv.reader(file)
 
  # displaying the contents of the CSV file
  for lines in csvFile:
        print(lines)

