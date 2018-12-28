#! usr/bin/env python
import sys
import re
import csv
import os

def process(infile, hr, outfile1 = 'stops_summary.csv', outfile2  ='mode_summary.csv', outfile3 = 'company_summary.csv'):
	writer_rail = csv.writer(open(os.path.join(hr,outfile1), "wb"))
	writer_mode = csv.writer(open(os.path.join(hr,outfile2), "wb"))
	writer_company = csv.writer(open(os.path.join(hr,outfile3), "wb"))
	rail_headers = ['type','mode', 'line', 'node', 'seq', 'on', 'off', 'load', 'dir']
	mode_headers = ['type','mode', 'line', 'trips', 'miles', 'hrs', 'peak load', 'hw orig', 'hw revised', 'hw min']
	company_headers = ['type','Company', 'trips', 'miles', 'hrs', 'peak load']
	writer_rail.writerow(rail_headers)
	writer_mode.writerow(mode_headers)
	writer_company.writerow(company_headers)
	
	for line in open(infile):
		list = line[:-1].split(',')
		#print list
		type = list[0].split('_')
		if not list[2].isdigit() or type[2] =='VERSION': 
			continue
		if type[1] == 'Rail':
			row = []
			row2 = []
			trntype = type[0]
			mode = type[2]
			line = type[3]
			seq = type[4]
			node = type[5]
			row = [trntype, mode, line, node, seq]
			for item in list[1:]:
				row.append(item)
			if len(row) >  8:
				row2 = [row[0], row[1], row[2], row[3], row[4]]
				for item in row[8:]:
					row2.append(item)
				row = row[:8]
			if len(row) > 0:
				row.append('inbound')
				writer_rail.writerow(row)
			if len(row2) > 0:
				row2.append('outbound')
				writer_rail.writerow(row2)
		elif type[1] == 'Mode':
			if len(type) < 4:
				continue
			row = []
			trntype = type[0]
			mode = type[2]
			line = type[3]
			row = [trntype, mode, line]
			for item in list[2:]:
				row.append(item)
			writer_mode.writerow(row)
			
		elif type[1] == 'Company':
			row = []
			trntype = type[0]
			company = type[2]
			row = [trntype, company]
			for item in list[1:]:
				row.append(item)
			writer_company.writerow(row)
		
		
			