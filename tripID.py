# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 18:35:51 2019

@author: kocak
"""

import pandas as pd
import numpy as np
path = "C:/Users/kocak/OneDrive/Masaüstü/reag/"

segments_w_tripID = pd.read_csv(path + "segment_directions_w_tripID.csv")
#%%
#Smart Card
# Read October Smart Card Info
sc = pd.read_csv(path+'10-ulasim_veri.csv',delimiter=';')
sc['ENLEM'] = pd.to_numeric(sc['ENLEM'].str.replace(',','.'))
sc['BOYLAM'] = pd.to_numeric(sc['BOYLAM'].str.replace(',','.'))

#Filter 30th October
sc30 = sc[(pd.to_datetime(sc["TIMESTAMP"]) >= pd.to_datetime('2018-10-30 02:59:59')) & (pd.to_datetime(sc["TIMESTAMP"]) < pd.to_datetime('2018-10-31 03:00:00')) & (sc["ENLEM"] > 0) & (sc["BOYLAM"] > 0)]
sc30.to_csv(path + "smart_card_30oct.csv")
#%%
# Read the 30oct smartcard data
sc30 = pd.read_csv(path + "smart_card_30oct.csv")
#%%
tempStringLID = segments_w_tripID.loc[1,"SEGTID"][4:6]  # e.g 44
tempStringSLID = segments_w_tripID.loc[1,"SEGTID"][6:7]  # e.g 3
sc30 = sc30[(sc30["HAT_NO"] == int(tempStringLID)) & (sc30["ALT_HAT_NO"] == int(tempStringSLID)) ]

#%%

segments_w_tripID["#ofPassenger"] = 0
segments_w_tripID["Passengers@FS"] = 0
segments_w_tripID["Passengers@LS"] = 0
sc30["ShiftID"] = ""
sc30["tripID"] = 0
sc30["AssignedStopID"] = ""
sc30["Stat"] = 0      # 0 means on route, 1 means at stop
gpsAracNo = []
for shiftID, group in segments_w_tripID.groupby("ShiftID"):
    group = group.sort_values(by=["F_TS"])
    scForGroup = sc30[(sc30["ARAC_NO"]== int(shiftID[4:7]))]
    gpsAracNo.append(int(shiftID[4:7]))
    isFirstRow = True
    for i, row in group.iterrows():
        if isFirstRow:
            sc_between_segment = scForGroup[(pd.to_datetime(scForGroup["TIMESTAMP"]) >= pd.to_datetime(row["F_TS"])) & (pd.to_datetime(scForGroup["TIMESTAMP"]) <= pd.to_datetime(row["L_TS"]))]
            segments_w_tripID.loc[i,"#ofPassenger"] = sc_between_segment.shape[0]
            for index, row_sc in sc_between_segment.iterrows():
            # smart card distance to first stop and last stop
                d_to_FS = calculateDistance(np.array([row["DURAK1_LAT"],row["DURAK1_LON"]]),np.array([row_sc["ENLEM"],row_sc["BOYLAM"]]))
                d_to_LS = calculateDistance(np.array([row["DURAK2_LAT"],row["DURAK2_LON"]]),np.array([row_sc["ENLEM"],row_sc["BOYLAM"]]))
                sc30.loc[index,"ShiftID"] = row["ShiftID"]
                sc30.loc[index,"tripID"] = row["tripID"]
                if d_to_FS >= d_to_LS:
                    segments_w_tripID.loc[i,"Passengers@LS"] += 1 
                    sc30.loc[index,"AssignedStopID"] = row["MOVED_DIR"].split("_")[1]
                    sc30.loc[index,"Stat"] = 1 
                else:
                    segments_w_tripID.loc[i,"Passengers@FS"] += 1  
                    sc30.loc[index,"AssignedStopID"] = row["MOVED_DIR"].split("_")[0]
                    sc30.loc[index,"Stat"] = 1 
            isFirstRow = False
            prevIndex = i
            
            continue
        sc_between_segment = scForGroup[(pd.to_datetime(scForGroup["TIMESTAMP"]) >= pd.to_datetime(group.loc[prevIndex,"L_TS"])) & (pd.to_datetime(scForGroup["TIMESTAMP"]) <= pd.to_datetime(row["L_TS"]))]
        segments_w_tripID.loc[i,"#ofPassenger"] = sc_between_segment.shape[0]
        for index, row_sc in sc_between_segment.iterrows():
            # smart card distance to first stop and last stop
            d_to_FS = calculateDistance(np.array([row["DURAK1_LAT"],row["DURAK1_LON"]]),np.array([row_sc["ENLEM"],row_sc["BOYLAM"]]))
            d_to_LS = calculateDistance(np.array([row["DURAK2_LAT"],row["DURAK2_LON"]]),np.array([row_sc["ENLEM"],row_sc["BOYLAM"]]))
            sc30.loc[index,"ShiftID"] = row["ShiftID"]
            sc30.loc[index,"tripID"] = row["tripID"]
            if d_to_FS >= d_to_LS:
                segments_w_tripID.loc[i,"Passengers@LS"] += 1 
                sc30.loc[index,"AssignedStopID"] = row["MOVED_DIR"].split("_")[1]
                sc30.loc[index,"Stat"] = 1 
            else:
                segments_w_tripID.loc[i,"Passengers@FS"] += 1 
                sc30.loc[index,"AssignedStopID"] = row["MOVED_DIR"].split("_")[0]
                sc30.loc[index,"Stat"] = 1 
        prevIndex = i

#%%
segments_w_tripID.to_csv(path + "segment_directions_w_tripID&Passenger.csv")
sc30.to_csv(path+"smart_card_30oct_w_tripID.csv")
#%%
# Filter the smartcard data that has not gps data
sc30_notGPS = sc30.copy()
for aracNo in gpsAracNo:
    sc30_notGPS = sc30_notGPS[sc30_notGPS["ARAC_NO"]!=aracNo]
    

for i,group in sc30_notGPS.groupby("ARAC_NO"):
    for index,row in group.iterrows():
        sc30_notGPS.loc[index,"ShiftID"] = str(row["HAT_NO"]) + str(row["ALT_HAT_NO"]) + "_" + str(i)
        sc30.loc[index,"ShiftID"] = str(row["HAT_NO"]) + str(row["ALT_HAT_NO"]) +"_"+str(i)
#%%
sc30_notGPS.to_csv(path+"smart_card_30oct_notGPS_w_tripID.csv")
#%%
for shiftID, group in segments_w_tripID.groupby("ShiftID"):
    group = group.sort_values(by=["F_TS"])
#%%
segments_w_tripID = pd.read_csv(path+ "segment_directions_w_tripID&Passenger.csv")
