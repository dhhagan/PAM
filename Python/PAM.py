#PAM.py

import re
import glob, os, time
from numpy import *
from pylab import *

def analyzeFile(fileName,delim):
    cols = {}
    indexToName = {}
    lineNum = 0
    goodLines = 0
    shortLines = 0
    
    FILE = open(fileName,'r')
	
    for line in FILE:
        line = line.strip()
	
	if lineNum < 1:
	    lineNum += 1
	    continue	
	elif lineNum == 1:
	   headings = line.split(delim)
	   i = 0
	   for heading in headings:
	       heading = heading.strip()
	       cols[heading] = []
	       indexToName[i] = heading
	       i += 1
	   lineNum += 1
	   lineLength = len(cols)
	else:
	   data = line.split(delim)
	   if len(data) == lineLength:
	       goodLines += 1
	       i = 0
	       for point in data:
	           point = point.strip()
	           cols[indexToName[i]] += [point]
	           i += 1
	       lineNum += 1
	   else:
	       shortLines += 1
	       lineNum += 1
	       continue
    FILE.close
		
    return cols, indexToName, lineNum, shortLines

def numericalSort(value):
	numbers = re.compile(r'(\d+)')
	parts = numbers.split(value)
	parts[1::2] = map(int, parts[1::2])
	return parts
	
def popDate(fileName):
	run = fileName.split('.')[0]
	runNo = run.split('_')[-1]
	return runNo


def getFile(date,regex):#Works
        files = []
	files = sorted((glob.glob('*'+regex+'*')),key=numericalSort,reverse=True)
	if date.lower() == 'last':
		files = files[0]
	else:
	    files = [item for item in files if re.search(date,item)]

	return files

def plotConc(data,times):
        # This function plots data versus time 
	import datetime as dt
	from matplotlib import pyplot as plt
	from matplotlib.dates import date2num

	#time = [dt.datetime.strptime(time,"%m/%d/%Y %I:%M:%S %p") for time in times]
        time = [dt.datetime.strptime(time,"%m/%d/%y %H:%M") for time in times]
	x = date2num(time)
        legend_items = []
	
	fig = plt.figure('NO and NOx Readings for East St.Louis')
	graph = fig.add_subplot(111)
	for key,value in data.items():
                graph.plot_date(x,data[key],'-',xdate=True)
                legend_items.append(key)

	title('NO and NOx Concentrations', fontsize = 12)
	ylabel(r'$Concentration(ppm)$', fontsize = 12)
	xlabel(r"$Time \, Stamp$", fontsize = 12)
	legend(legend_items)
	grid(True)

	return 

def plotBankRelays(data,relays,times):
        # This function plots data versus time 
	import datetime as dt
	from matplotlib import pyplot as plt
	from matplotlib.dates import date2num
        
	time = [dt.datetime.strptime(time,"%m/%d/%Y %I:%M:%S %p") for time in times]
	x = date2num(time)
	#x1 = [date.strftime("%m-%d %H:%M:%S") for date in time]
        legend1 = []
        legend2 = []
        
	#plt.locator_params(axis='x', nbins=4)
	fig = plt.figure('VAPS Thermocouple Readings: Chart 2')
	ax1 = fig.add_subplot(111)
	ax2 = twinx()
	
	for key,value in data.items():
                ax1.plot_date(x,data[key],'-',xdate=True)
                legend1.append(key)
        for key,value in relays.items():
                ax2.plot_date(x,relays[key],'--',xdate=True)
                legend2.append(key)

	title('VAPS Temperatures: Chart 2', fontsize = 12)
	ax1.set_ylabel(r'$Temperature(^oC)$', fontsize = 12)
	ax2.set_ylabel(r'$Relay \, States$', fontsize = 12)
	ax1.set_xlabel(r"$Time \, Stamp$", fontsize = 12)
	#print [num2date(item) for item in ax1.get_xticks()]
	
	#ax1.set_xticks(x)
	
	#ax1.set_xticklabels([date.strftime("%m-%d %H:%M %p") for date in time])
        #ax1.legend(bbox_to_anchor=(0.,1.02,1.,.102),loc=3,ncol=2,mode="expand",borderaxespad=0.)
	ax1.legend(legend1,loc='upper right')
	ax2.legend(legend2,loc='lower right')
	#ax1.xaxis.set_major_formatter(FormatStrFormatter(date.strftime("%m-%d %H:%M:%S")))
	plt.subplots_adjust(bottom=0.15)
	grid(True)

	return


def goodFiles(files,goodHeaders,delim):   # Good
        irregFiles = 0
        goodFiles = []
        for file in files:
            lineNo = 0
            falseCount = 0
            FILE = open(file,'r')
            for line in FILE:
                line = line.strip()
                if lineNo == 5:
                    # Check all the headings to make sure the file is good
                    head = line.split(delim)
                    for item in head:
                        if item in goodHeaders:
                            continue
                        else:
                            falseCount += 1
                    if falseCount == 0:
                        goodFiles.append(file)
                    else:
                        irregFiles += 1
                    lineNo += 1
                            
                else:
                    lineNo += 1
                    continue
            FILE.close
        return goodFiles, irregFiles
