'''
This is the gateway script to the other python scripts in this 
folder. 
'''

import sys

import tasgn_report
import rpt2

if __name__ == '__main__':
    tod = sys.argv[1]
    if tod.upper() == 'AM':
        hrs = 3
    else:
        hrs = 6
    
    tasgn_report.process('RptTrn{}{}.OUT'.format(tod.upper(), hrs))
    rpt2.process('tasgn_report.csv','{}{}'.format(tod.lower(), hrs))

    #tasgn_report.process('RptTrn1hr.OUT')
    #rpt2.process('tasgn_report.csv','1hr')