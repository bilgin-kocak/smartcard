# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 19:32:03 2019

@author: kocak
"""
# In[]
import numpy as np

# To calculate distance between 2 points. Ex: calculateDistance([a["enlem"],a["boylam"]],[b["enlem"],b["boylam"]])
def calculateDistance(a,b):
    
    s_lat = a[0]
    s_lng = a[1]
    e_lat = b[0]
    e_lng = b[1]
    R = 6373.0
    
    s_lat = s_lat*np.pi/180.0                      
    s_lng = np.deg2rad(s_lng)     
    e_lat = np.deg2rad(e_lat)                       
    e_lng = np.deg2rad(e_lng)  
    
    d = np.sin((e_lat - s_lat)/2)**2 + np.cos(s_lat)*np.cos(e_lat) * np.sin((e_lng - s_lng)/2)**2
    return 2 * R * np.arcsin(np.sqrt(d)) 

# In[]
    
segments_w_tripID["#ofPassenger"] = 0
segments_w_tripID["Passengers@FS"] = 0
segments_w_tripID["Passengers@LS"] = 0
sc30["ShiftID"] = ""
sc30["tripID"] = 0
sc30["AssignedStopID"] = ""
sc30["Stat"] = 0      # 0 means on route, 1 means at stop
for shiftID, group in segments_w_tripID.groupby("ShiftID"):
    group = group.sort_values(by=["F_TS"])
    scForGroup = sc30[(sc30["ARAC_NO"]== int(shiftID[4:7]))]
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

#sc30.to_csv(path+"smart_card_30oct_w_tripID.csv")
#%%
oldShiftID = ""
for i,gr in segments_w_tripID.groupby("ShiftID"):
    if (i == oldShiftID):
        continue
    print(i)
    oldShiftID = i
    #%%
oldDID = 0
for i,gr in sc30.groupby("ARAC_NO"):
    if(i==oldDID):
        continue
    print(i)
    oldDID = i
    
#%%
