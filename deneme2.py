# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 23:41:29 2019

@author: kocak
"""
import pandas as pd

rows_filtered = pd.read_csv("./segment_directions_last_filtered.csv")

flag = 0
# Group edited dataframe by ShiftID 
r_grouped = rows_filtered.groupby("ShiftID")


for i,g in r_grouped:
    last_stop = -1
    last_index = -99
    tripID = 1
    g_sorted = g.sort_values(by = ["F_TS"])
    for j,r in g_sorted.iterrows():
        stop = int((r["R_DIR"].split("_"))[0])

                
        if last_stop < stop:
                
            rows_filtered.loc[j,"tripID"] = tripID
            rows_filtered.loc[j,"control"] = 1
            if stop-last_stop > 1:
                rows_filtered.loc[j,"tripID"] = tripID
                rows_filtered.loc[j,"control"] = -1
        
        else:
            flag = 1
            stopDist = r["SegLength"]
            # If the distance between fp and fs and between lp and ls, it should be checked.
            if 100 <  float(r["FP2FS"]) or 100 < float(r["LP2LS"]):
                print(float(r["FP2FS"]))
                rows_filtered.loc[j,"tripID"] = tripID
                rows_filtered.loc[j,"control"] = -1
            else:
                tripID = tripID + 1
                rows_filtered.loc[j,"tripID"] = tripID
                rows_filtered.loc[j,"control"] = 1
        
        last_to_last_row = last_row
        last_to_last_index = last_index
        last_row = r        
        last_stop = stop
        last_index = j