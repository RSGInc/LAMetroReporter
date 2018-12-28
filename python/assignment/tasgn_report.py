#! usr/bin/env python
"""
tasgn_report.py

Pull out summary statistics from a transit assignment report file 
for further processing.

Original Author: Andrew Stryker <stryker@pbworld.com>
Modified By: Hannah Carson <hannah.carson@rsginc.com>
"""

import sys
import re
import csv




def process(infile, outfile = 'tasgn_report.csv'):
    """
    """

    writer = csv.writer(open(outfile, "wb"))

    report = None
    begin = re.compile(r'^\s*INPUT FILE = TRLDATA')
    end = re.compile(r'^\s*$TOTAL')
    good = re.compile(r'^\s*\D*\d+')
    station = re.compile(r'^\s*P A S S E N G E R')
    route = re.compile(r'^\s*MODE  LINE')
    company = re.compile(r'^\s*COMPANY')


    for line in open(infile):
        line = line[:-1]    # eliminate the newline character
         
        # find REPORT of BUS, BRT, URB, COM and BLEND
        if begin.match(line):
           fields = line.split()
           report = fields[-1]
           if re.search('trnall', report):
               report = 'trn'
           elif re.search('BrT', report):
               report = 'BrT'
           elif re.search('UrR', report):
               report = 'UrR'
           elif re.search('CmR', report):
               report = 'CmR'    
           else:
               report = 'CUB'
           print report
            
        if station.match(line):
           rail = line.split()
           report = report[0:3] + '_' + 'Rail' + '_' + rail[-6] + '_' + rail[-1]
           print report
        elif route.match(line):
             report = report[0:3] + '_' + 'Mode' 
             print report
        elif company.match(line):
             report = report[0:3] + '_' + 'Company'
             print report
               
        #if end.match(line):
            #report = None


        if report is None or not good.match(line):
           continue
        

        fields = line.split()
        col = len(fields)
        result = list()
        result1=list()
        
        if re.search('Rail', report): 
			if col == 8 or col == 5: 
				key = report + '_' + fields[0] +'_' + fields[1]               
				result = [key]
				for x in fields[2:]:
					result.append(x)
			elif col == 16:
				key1 = report + '_' + fields[0] + '_' + fields[1]
				result = [key1]
				for x in fields[2:8]:
					result.append(x)                  
				key2 = report + '_' + fields[8] + '_' + fields[9]
				result1 = [key2]
				for x in fields[10:16]:
					result1.append(x)
			elif col == 10:
				key3 = report + '_' + fields[0] + '_' + fields[1]
				result = [key3]
				for x in fields[2:5]:
					result.append(x)                  
				key4 = report + '_' + fields[5] + '_' + fields[6]
				result1 = [key4]
				for x in fields[7:10]:
					result1.append(x) 				
		
		
        elif re.search('Company', report):
			key = report + '_' + fields[0]                
			result = [key]
			for x in fields[1:]:
				result.append(x)
        
        elif re.search('Mode', report):
			if  not fields[0].startswith('\d'): continue
			if len(fields) == 5:
				key = report + '_' + fields[0]
				result = [key]
				for x in fields[1:]:
					result.append(x)
			else:
				key = report + '_' + fields[0] + '_' + fields[1]          
				result = [key]
				for x in fields[1:]:
					result.append(x)
        if len(result) > 0:
			#print(result)
			if result[1][0].isdigit():
				writer.writerow(result)
        if len(result1) > 0: 
			if result1[1][0].isdigit():
				writer.writerow(result1)


if __name__ == "__main__":

    print sys.argv

    process(sys.argv[1])
