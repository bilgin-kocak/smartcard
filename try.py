# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 23:00:15 2019

@author: kocak
"""

import pandas as pd

path = "C:/Users/kocak/OneDrive/Masaüstü/reag/"

rows_filtered = pd.read_csv(path+ "/segment_directions_w_tripID_.csv") 
rows_filtered["tripID"] = 0
# Group edited dataframe by ShiftID 
r_grouped = rows_filtered.groupby("ShiftID")

for i,g in r_grouped:
    last_stop = -1
    last_index = -99
    maxMoveDirF = g["MV_DIR_F"].max()
    minMoveDirL = g["MV_DIR_F"].min()
    tripID = 1
    lastSegtId = ""
    g_sorted = g.sort_values(by = ["F_TS"])
    for j,r in g_sorted.iterrows():
        stop = int((r["R_DIR"].split("_"))[0])
        segtId = r["SEGTID"]
        
        if int((r["R_DIR"].split("_"))[0]) == 72:
            a = 1
        
        if last_stop < stop:
                
            rows_filtered.loc[j,"tripID"] = tripID
            g.loc[j,"tripID"] = tripID
            g_sorted.loc[j,"tripID"] = tripID
            if stop - last_stop <= 5:  # Everything is normal
                rows_filtered.loc[j,"control"] = 100
                g.loc[j,"control"] = 100
                g_sorted.loc[j,"control"] = 100
            else: # There is a big jump (bus does not reach many duraks )
                rows_filtered.loc[j,"control"] = 150
                g.loc[j,"control"] = 150
                g_sorted.loc[j,"control"] = 150
        # More than one movegroup exits in segment 
        if last_stop == stop and lastSegtId == segtId:
            rows_filtered.loc[j,"tripID"] = tripID
            rows_filtered.loc[j,"control"] = 101
            g.loc[j,"tripID"] = tripID
            g.loc[j,"control"] = 101
            g_sorted.loc[j,"tripID"] = tripID
            g_sorted.loc[j,"control"] = 101
            
        
        if last_stop > stop:
            # We can say that this is not a big problem.(Same trip)
            if last_stop - stop <= 5:
                rows_filtered.loc[j,"tripID"] = tripID
                rows_filtered.loc[j,"control"] = 200
                g.loc[j,"tripID"] = tripID
                g.loc[j,"control"] = 200
                g_sorted.loc[j,"tripID"] = tripID
                g_sorted.loc[j,"control"] = 200
            else:
                # Trip changes
                tripID +=1 
                rows_filtered.loc[j,"tripID"] = tripID
                rows_filtered.loc[j,"control"] = 300
                g.loc[j,"tripID"] = tripID
                g.loc[j,"control"] = 300
                g_sorted.loc[j,"tripID"] = tripID
                g_sorted.loc[j,"control"] = 300
        
        last_row = r        
        last_stop = stop
        last_index = j
        lastSegtId = segtId
        
#%%
cols = ['SEGTID', 'F_TS','F_IND', 'L_IND','ShiftID', 'MVGRP','MV_DIR_F', 'MV_DIR_L', 'tripID', 'control']
df_selected = rows_filtered[cols]

rows_filtered.to_csv("C:/Users/kocak/OneDrive/Masaüstü/reag/segment_directions_w_tripID.csv")

rows_filtered.to_excel("C:/Users/kocak/OneDrive/Masaüstü/reag/segment_directions_w_tripID.xlsx")