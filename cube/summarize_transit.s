; This script takes the outputs from the 8 CBM18 Mode Choice models and
; summarizes transit trips by time of day and major transit mode (i.e., local,
; express, rapid, brt, transitway, urban rail, and commuter rail).

; The outputs of this script are as follows:
;  - {}_pk_by_mode.pactrips:     Peak period transit trips by major mode
;  - {}_op_by_mode.pactrips:     Off-peak period transit trips by major mode
;  - {}_daily_by_mode.pactrips:  Daily transit trips by major mode
;  - {}_pk_transit.pactrips:     Peak period transit trips (no mode breakdown)
;  - {}_op_transit.pactrips:     Off-peak period transit trips (no mode breakdown)
;  - {}_daily_transit.pactrips:  Daily transit trips (no mode breakdown)

; This script is intended to be run from a folder at the same level as 3ModCh
; in the CBM18 model setup. As an example, the scripts could be run from a 
; folder called 9Reports.

sce = 'NB'
yr = 'y2042'

RUN PGM=MATRIX
  MATI[1] = "..\3ModCh\@yr@_@sce@_pk_hbo_bu1.pactrips"
  MATI[2] = "..\3ModCh\@yr@_@sce@_pk_hbu_bu1.pactrips"
  MATI[3] = "..\3ModCh\@yr@_@sce@_pk_hbw_bu1.pactrips"
  MATI[4] = "..\3ModCh\@yr@_@sce@_pk_nhb_bu1.pactrips"
  
  FILEO MATO = "..\3ModCh\@yr@_@sce@_pk_by_mode.pactrips", MO=1-7,
    NAME=LOCAL, EXPRESS, RAPID, BRT, TRW, URAIL, CRAIL
  
  MW[1] = MI.1.1 + MI.1.2 + MI.1.20 +
          MI.2.1 + MI.2.2 + MI.2.20 +
          MI.3.1 + MI.3.2 + MI.3.20 + 
          MI.4.1 + MI.4.2 + MI.4.20
  
  MW[2] = MI.1.3 + MI.1.4 + MI.1.22 +
          MI.2.3 + MI.2.4 + MI.2.22 +
          MI.3.3 + MI.3.4 + MI.3.22 + 
          MI.4.3 + MI.4.4 + MI.4.22
  
  MW[3] = MI.1.15 + MI.1.16 + MI.1.21 +
          MI.2.15 + MI.2.16 + MI.2.21 +
          MI.3.15 + MI.3.16 + MI.3.21 +
          MI.4.15 + MI.4.16 + MI.4.21 
  
  MW[4] = MI.1.17 + MI.1.18 + MI.1.19 + MI.1.24 + MI.1.29 +
          MI.2.17 + MI.2.18 + MI.2.19 + MI.2.24 + MI.2.29 +
          MI.3.17 + MI.3.18 + MI.3.19 + MI.3.24 + MI.3.29 +
          MI.4.17 + MI.4.18 + MI.4.19 + MI.4.24 + MI.4.29 
  
  MW[5] = MI.1.13 + MI.1.14 + MI.1.23 +
          MI.2.13 + MI.2.14 + MI.2.23 +
          MI.3.13 + MI.3.14 + MI.3.23 +
          MI.4.13 + MI.4.14 + MI.4.23
  
  MW[6] = MI.1.9 + MI.1.10 + MI.1.11 + MI.1.12 + MI.1.28 +
          MI.2.9 + MI.2.10 + MI.2.11 + MI.2.12 + MI.2.28 +
          MI.3.9 + MI.3.10 + MI.3.11 + MI.3.12 + MI.3.28 +
          MI.4.9 + MI.4.10 + MI.4.11 + MI.4.12 + MI.4.28
  
  MW[7] = MI.1.5 + MI.1.6 + MI.1.7 + MI.1.8 + MI.1.27 + 
          MI.2.5 + MI.2.6 + MI.2.7 + MI.2.8 + MI.2.27 +
          MI.3.5 + MI.3.6 + MI.3.7 + MI.3.8 + MI.3.27 +
          MI.4.5 + MI.4.6 + MI.4.7 + MI.4.8 + MI.4.27
  
ENDRUN

RUN PGM=MATRIX
  MATI[1] = "..\3ModCh\@yr@_@sce@_op_hbo_bu1.pactrips"
  MATI[2] = "..\3ModCh\@yr@_@sce@_op_hbu_bu1.pactrips"
  MATI[3] = "..\3ModCh\@yr@_@sce@_op_hbw_bu1.pactrips"
  MATI[4] = "..\3ModCh\@yr@_@sce@_op_nhb_bu1.pactrips"
  
  FILEO MATO = "..\3ModCh\@yr@_@sce@_op_by_mode.pactrips", MO=1-7,
    NAME=LOCAL, EXPRESS, RAPID, BRT, TRW, URAIL, CRAIL
  
  MW[1] = MI.1.1 + MI.1.2 + MI.1.20 +
          MI.2.1 + MI.2.2 + MI.2.20 +
          MI.3.1 + MI.3.2 + MI.3.20 + 
          MI.4.1 + MI.4.2 + MI.4.20
  
  MW[2] = MI.1.3 + MI.1.4 + MI.1.22 +
          MI.2.3 + MI.2.4 + MI.2.22 +
          MI.3.3 + MI.3.4 + MI.3.22 + 
          MI.4.3 + MI.4.4 + MI.4.22
  
  MW[3] = MI.1.15 + MI.1.16 + MI.1.21 +
          MI.2.15 + MI.2.16 + MI.2.21 +
          MI.3.15 + MI.3.16 + MI.3.21 +
          MI.4.15 + MI.4.16 + MI.4.21 
  
  MW[4] = MI.1.17 + MI.1.18 + MI.1.19 + MI.1.24 + MI.1.29+
          MI.2.17 + MI.2.18 + MI.2.19 + MI.2.24 + MI.2.29+
          MI.3.17 + MI.3.18 + MI.3.19 + MI.3.24 + MI.3.29+
          MI.4.17 + MI.4.18 + MI.4.19 + MI.4.24 + MI.4.29
  
  MW[5] = MI.1.13 + MI.1.14 + MI.1.23 +
          MI.2.13 + MI.2.14 + MI.2.23 +
          MI.3.13 + MI.3.14 + MI.3.23 +
          MI.4.13 + MI.4.14 + MI.4.23
  
  MW[6] = MI.1.9 + MI.1.10 + MI.1.11 + MI.1.12 + MI.1.28 +
          MI.2.9 + MI.2.10 + MI.2.11 + MI.2.12 + MI.2.28 +
          MI.3.9 + MI.3.10 + MI.3.11 + MI.3.12 + MI.3.28 +
          MI.4.9 + MI.4.10 + MI.4.11 + MI.4.12 + MI.4.28
  
  MW[7] = MI.1.5 + MI.1.6 + MI.1.7 + MI.1.8 + MI.1.27 + 
          MI.2.5 + MI.2.6 + MI.2.7 + MI.2.8 + MI.2.27 +
          MI.3.5 + MI.3.6 + MI.3.7 + MI.3.8 + MI.3.27 +
          MI.4.5 + MI.4.6 + MI.4.7 + MI.4.8 + MI.4.27
  
ENDRUN

RUN PGM=MATRIX
  MATI[1] = "..\3ModCh\@yr@_@sce@_pk_by_mode.pactrips"
  MATI[2] = "..\3ModCh\@yr@_@sce@_op_by_mode.pactrips"
  
  FILEO MATO = "..\3ModCh\@yr@_@sce@_daily_by_mode.pactrips", MO=1-7,
    NAME=LOCAL, EXPRESS, RAPID, BRT, TRW, URAIL, CRAIL
    
  MW[1] = MI.1.1 + MI.2.1
  MW[2] = MI.1.2 + MI.2.2
  MW[3] = MI.1.3 + MI.2.3
  MW[4] = MI.1.4 + MI.2.4
  MW[5] = MI.1.5 + MI.2.5
  MW[6] = MI.1.6 + MI.2.6
  MW[7] = MI.1.7 + MI.2.7
 
ENDRUN


RUN PGM=MATRIX
  MATI[1] = "..\3ModCh\@yr@_@sce@_pk_by_mode.pactrips"
  
  FILEO MATO = "..\3ModCh\@yr@_@sce@_pk_transit.pactrips", MO=1,
    NAME=TotTransit
  
  MW[1] = MI.1.1 + MI.1.2 + MI.1.3 +
          MI.1.4 + MI.1.5 + MI.1.6 +
          MI.1.7
ENDRUN

RUN PGM=MATRIX
  MATI[1] = "..\3ModCh\@yr@_@sce@_op_by_mode.pactrips"
  
  FILEO MATO = "..\3ModCh\@yr@_@sce@_op_transit.pactrips", MO=1,
    NAME=TotTransit
  
  MW[1] = MI.1.1 + MI.1.2 + MI.1.3 +
          MI.1.4 + MI.1.5 + MI.1.6 +
          MI.1.7
ENDRUN

RUN PGM=MATRIX
  MATI[1] = "..\3ModCh\@yr@_@sce@_op_transit.pactrips"
  MATI[2] = "..\3ModCh\@yr@_@sce@_pk_transit.pactrips"
  
  FILEO MATO = "..\3ModCh\@yr@_@sce@_daily_transit.pactrips", , MO=1,
    NAME=TotTransit
    
  MW[1] = MI.1.1 + MI.2.1  
ENDRUN