; Compares the difference in transit trip tables by mode across two scenarios. The script
; will also summarize trip differences by districts (e.g., transit markets) based on
; an taz_xref.csv file.

; Output files:
;  - agg_@yr@_@scen@_daily_trips_diff_by_mode.pactrips:            Transit trip difference table by major mode
;  - agg_@yr@_@scen@_daily_trips_diff_by_mode_summarized.pactrips: Transit trip difference matrix by major mode summarized to user-specified districts

; TAZ XREF CSV File Format (see example file: nsfv_taz_xref.csv)
;  - TAZ: CBM18 TAZ Number
:  - RSA: SCAG RSA Number
:  - CSA: SCAG CSA Number
:  - COUNTY: County Name (string)
:  - COUNTY_ID: County ID (number)
:  - DIST: District Name (string)
:  - DIST_ID: District ID (number)
:  - SUPDIST: Super District Name (string)
:  - SUPDIST_ID: Super District ID (number)


STUDY_AREA = 'NSFV'
COMP_PATH = '..\..\y2042 - NB'

scen = 'NB'
yr = 'y2042'

RUN PGM=MATRIX
  MATI[1] = "@COMP_PATH@\3ModCh\@yr@_@scen@_daily_by_mode.pactrips"
  MATI[2] = "..\3ModCh\@yr@_@scen@_daily_by_mode.pactrips"
  
  FILEO MATO = "agg_@yr@_@scen@_daily_trips_diff_by_mode.pactrips", MO=1-7,
    NAME=LOCAL,EXPRESS,RAPID,BRT,TRW,URAIL,CRAIL

  MW[1] = .01*MI.2.1 - .01*MI.1.1
  MW[2] = .01*MI.2.2 - .01*MI.1.2
  MW[3] = .01*MI.2.3 - .01*MI.1.3
  MW[4] = .01*MI.2.4 - .01*MI.1.4
  MW[5] = .01*MI.2.5 - .01*MI.1.5
  MW[6] = .01*MI.2.6 - .01*MI.1.6
  MW[7] = .01*MI.2.7 - .01*MI.1.7

ENDRUN


RUN PGM=MATRIX
  MATI[1] = "agg_@yr@_@scen@_daily_trips_diff_by_mode.pactrips"
  
  ZDATI = @STUDY_AREA@_taz_xref.CSV, Z=#1, RSA=#2, CSA=#3, COUNTY=#4, COUNTY_ID=#5, DIST=#6, DIST_ID=#7, SUPDIST=#8, SUPDIST_ID=#9
 
  FILEO MATO = "agg_@yr@_@scen@_daily_trips_diff_by_mode_summarized.pactrips", MO=1-7,
  NAME=LOCAL,EXPRESS,RAPID,BRT,TRW,URAIL,CRAIL

  MW[1] = MI.1.1
  MW[2] = MI.1.2
  MW[3] = MI.1.3
  MW[4] = MI.1.4
  MW[5] = MI.1.5
  MW[6] = MI.1.6
  MW[7] = MI.1.7
    
   RENUMBER ZONEO=ZI.1.SUPDIST_ID
ENDRUN