# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 21:22:13 2019

@author: kocak
"""
import pandas as pd
import numpy as np

# In[Direction]

# Initialize DIRECTION column
rows_df["DIRECTION"] = 0


for i,row in rows_df.iterrows():
    # Get VehicleID from ShiftID
    vid = int(row["ShiftID"].split("_")[1])
    
    # To decide on true direction
    if (row["FP2FS"] < row["FP2LS"] and row["LP2FS"] > row["LP2LS"]):
        rows_df.loc[i,"DIRECTION"] = 1
        
    elif (row["FP2FS"] > row["LP2FS"] and row["LP2LS"] > row["FP2LS"]):
        rows_df.loc[i,"DIRECTION"] = -1
    
    # Attempt to fix U-turns
    elif float(row["FP2FS"]) < 100 and float(row["LP2FS"]) < 100 and float(row["FP2LS"]) > 100 and float(row["LP2LS"]) > 100:
        # Find GPS points of the movegroup
        pts_df = df[(pd.to_datetime(df["TIMESTAMP"]) >= pd.to_datetime(row["F_TS"])) & (pd.to_datetime(df["TIMESTAMP"]) <= pd.to_datetime(row["L_TS"])) & (vid == df["VID"])]
        
        # Find the point that has the min distance to the last stop
        for j, pt in pts_df.iterrows():
            pts_df.loc[j,"p2fs"] = calculateDistance([pt["BUFFER1_LAT"],pt["BUFFER1_LON"]],[pt["POINT_LAT"],pt["POINT_LON"]])
            pts_df.loc[j,"p2ls"] = calculateDistance([pt["BUFFER2_LAT"],pt["BUFFER2_LON"]],[pt["POINT_LAT"],pt["POINT_LON"]])
        minil2l = pts_df.loc[pts_df["p2ls"].idxmin()]
        # If first point to "min distance" point is the right direction, divide the points group 
        if (row["FP2FS"] < row["FP2LS"] and minil2l["p2fs"] > minil2l["p2ls"]):
            rows_df = rows_df.append({'DURAK1_LAT': row["DURAK1_LAT"], 'DURAK1_LON': row['DURAK1_LON'],"DURAK2_LAT": row["DURAK2_LAT"],"DURAK2_LON":row["DURAK2_LON"], "FP2FS":row["FP2FS"],"FP2LS":row["FP2LS"],"FP_LAT":row["FP_LAT"],"FP_LON":row["FP_LON"],"F_IND": row["F_IND"],"F_TS":row["F_TS"],"LP2FS":float(minil2l["p2ls"])*1000,"LP2LS":float(minil2l["p2ls"])*1000,"LP_LAT":minil2l["POINT_LAT"],"LP_LON":minil2l["POINT_LON"],"L_IND":minil2l["INDEX"], "L_TS":minil2l["TIMESTAMP"],"MVGRP":row["MVGRP"],"SEGTID":row["SEGTID"],"ShiftID":row["ShiftID"],"SegLength": row["SegLength"],"DIRECTION":1}, ignore_index=True)
            rows_df = rows_df.append({'DURAK1_LAT': row["DURAK1_LAT"], 'DURAK1_LON': row['DURAK1_LON'],"DURAK2_LAT": row["DURAK2_LAT"],"DURAK2_LON":row["DURAK2_LON"], "FP2FS":float(minil2l["p2fs"])*1000,"FP2LS":float(minil2l["p2ls"])*1000,"FP_LAT":minil2l["POINT_LAT"],"FP_LON":minil2l["POINT_LON"],"F_IND": minil2l["INDEX"],"F_TS":minil2l["TIMESTAMP"],"LP2FS":row["LP2FS"],"LP2LS":row["LP2LS"],"LP_LAT":row["LP_LAT"],"LP_LON":row["LP_LON"],"L_IND":row["L_IND"], "L_TS":row["L_TS"],"MVGRP":-1,"SEGTID":row["SEGTID"],"ShiftID":row["ShiftID"],"SegLength": row["SegLength"],"DIRECTION":-1}, ignore_index=True)
        else:
            rows_df.loc[i,"DIRECTION"] = -1
            
    # Attempt to fix U-turns (inverse direction) 
    elif float(row["FP2FS"]) > 100 and float(row["FP2LS"]) < 100 and float(row["LP2LS"]) < 100 and float(row["LP2FS"]) > 100:
        pts_df = df[(pd.to_datetime(df["TIMESTAMP"]) >= pd.to_datetime(row["F_TS"])) & (pd.to_datetime(df["TIMESTAMP"]) <= pd.to_datetime(row["L_TS"])) & (vid == df["VID"])]
        # Find point that has the min distance to the first stop
        for j, pt in pts_df.iterrows():
            pts_df.loc[j,"p2fs"] = calculateDistance([pt["BUFFER1_LAT"],pt["BUFFER1_LON"]],[pt["POINT_LAT"],pt["POINT_LON"]])
            pts_df.loc[j,"p2ls"] = calculateDistance([pt["BUFFER2_LAT"],pt["BUFFER2_LON"]],[pt["POINT_LAT"],pt["POINT_LON"]])
        minif2f = pts_df.loc[pts_df["p2fs"].idxmin()]
        
        # If it is the right direction, divide
        if (minif2f["p2fs"] < minif2f["p2ls"] and row["LP2FS"] > row["LP2LS"]):
            rows_df = rows_df.append({'DURAK1_LAT': row["DURAK1_LAT"], 'DURAK1_LON': row['DURAK1_LON'],"DURAK2_LAT": row["DURAK2_LAT"],"DURAK2_LON":row["DURAK2_LON"], "FP2FS":row["FP2FS"],"FP2LS":row["FP2LS"],"FP_LAT":row["FP_LAT"],"FP_LON":row["FP_LON"],"F_IND": row["F_IND"],"F_TS":row["F_TS"],"LP2FS":float(minif2f["p2fs"])*1000,"LP2LS":float(minif2f["p2ls"])*1000,"LP_LAT":minif2f["POINT_LAT"],"LP_LON":minif2f["POINT_LON"],"L_IND":minif2f["INDEX"], "L_TS":minif2f["TIMESTAMP"],"MVGRP":-1,"SEGTID":row["SEGTID"],"ShiftID":row["ShiftID"],"SegLength": row["SegLength"],"DIRECTION":-1}, ignore_index=True)
            rows_df = rows_df.append({'DURAK1_LAT': row["DURAK1_LAT"], 'DURAK1_LON': row['DURAK1_LON'],"DURAK2_LAT": row["DURAK2_LAT"],"DURAK2_LON":row["DURAK2_LON"], "FP2FS":float(minif2f["p2fs"])*1000,"FP2LS":float(minif2f["p2ls"]),"FP_LAT":minif2f["POINT_LAT"],"FP_LON":minif2f["POINT_LON"],"F_IND": minif2f["INDEX"],"F_TS":minif2f["TIMESTAMP"],"LP2FS":row["LP2FS"],"LP2LS":row["LP2LS"],"LP_LAT":row["LP_LAT"],"LP_LON":row["LP_LON"],"L_IND":row["L_IND"], "L_TS":row["L_TS"],"MVGRP":row["MVGRP"],"SEGTID":row["SEGTID"],"ShiftID":row["ShiftID"],"SegLength": row["SegLength"],"DIRECTION":1}, ignore_index=True)

        else:
            rows_df.loc[i,"DIRECTION"] = -1
    # If we cannot fix DIRECTION of the movegroup, we directly assign DIRECTION to -1
    else:
        rows_df.loc[i,"DIRECTION"] = -1

rows_df.to_csv("./segments_w_directions.csv")