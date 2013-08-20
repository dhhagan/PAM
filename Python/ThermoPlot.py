# ThermoPlot.py

# Plots the data from Thermoscientific gas analyzers
# Written by David H Hagan, August 20th, 2013

# Updates:
#   Format
#    Name:		Date:		Brief Overview:


# Import libraries needed
from numpy import *
from pylab import *
import glob, os, time, PAM

start = time.time()
print 'Analyzing Thermo Data...'

# Data for FILES
dir = "C:/Users/David/Documents/GitHub/PAM/Python/"

localtime = time.asctime(time.localtime(time.time()))

# Enter the date (probably just HHMMSS) you want to analyze or type LAST if you want to grab the most recent file
#date = 'LAST'	
date = '20130820 1120'
delim = '\t'

# Change to the correct directory
currentDir = os.getcwd()
if currentDir != dir:
    os.chdir(dir)

# Get all the files to analyze
files = PAM.getFile(date,'Gas')
fileName = files[0]

totalLines = 0
totalShortLines = 0


lineCount = 0
DATA, indexToName, lineNum, shortLines = PAM.analyzeFile(fileName,delim)	
totalLines += lineNum
totalShortLines += shortLines
header = DATA.keys()

print header
# Clean up the data and grab the columns we are interested in:
# For NOx: [Time, Data, NO, NOx]
Timestamp = DATA['Time Stamp Local']
NO = DATA['NO']
NO2 = DATA['NO2']
NOx = DATA['NOx']
values = {'NO':NO, 'NOx':NOx, 'NO2':NO2}
end = time.time()

#PAM.plotConc(values,Timestamp)

print 'Files being analyzed this run:\n'
for each in files:
    print '\t' + each

print 'No. lines read: ' + str(totalLines)
print 'No. short lines: ' + str(shortLines)

print 'Time Elapsed during run: ' + str(end - start) + ' s'
show()