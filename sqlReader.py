# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 22:06:06 2019

@author: kocak
"""
import pandas as pd
f = open("C:/Users/kocak/OneDrive/Masaüstü/reag/oct24.csv","w")
f.write((("`SEQUENCE_ID`, `PACKET_ID`, `ARAC_NO`, `TARIH_SAAT`, `UYDU_SAYISI`, `ENLEM`, `BOYLAM`, `HEADING`, `HIZ`, `HAT_NO`, `SURUCU_NO`, `INSERT_TARIHI`\n").replace("`","").replace(" ","")).lower())
fh = open('gps_oct24.sql')
for line in fh:
    
    if line.startswith("(",1,6):
        string = (line[2:len(line)-3]).replace("'","")
        f.write(string+"\n")
    #line.startswith()
    
f.close()
fh.close()

oct24 = pd.read_csv("C:/Users/kocak/OneDrive/Masaüstü/reag/oct24.csv")