# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 20:34:18 2019

@author: kocak
"""

import pandas as pd
import numpy as np
path = "C:/Users/kocak/OneDrive/Masaüstü/reag/"
# =============================================================================
# 
# df = pd.read_csv(path+"buffer_100.csv")    
# 
# for i, g_VID_DID in df.groupby(["VID","DID"]):
#     for j, group in g_VID_DID.groupby("USID"):
#         A = 5
# =============================================================================

segments_w_tripIDandP = pd.read_csv( path + "segment_directions_w_tripID&Passenger.csv")

segments_w_tripIDandP["ETA"] = segments_w_tripIDandP["L_TS"]
segments_w_tripIDandP["CumulativeRouteTraveled"] = 0
segments_w_tripIDandP["DeltaTime"] = 0.0
segments_w_tripIDandP["AvgV"] = 0.0
for i,group in segments_w_tripIDandP.groupby("ShiftID"):
    routeTravelled = 0.0
    for j,groupTrip in group.groupby("tripID"):
        routeTravelled = 0.0
        groupTrip = groupTrip.sort_values(by=["F_TS"]) 
        isDuplicated = groupTrip.duplicated(subset=['LOCAL_DIR'])  # Find not duplicated segments
        for index, row in groupTrip.iterrows():
            if isDuplicated[index] == False:
                routeTravelled += row["SegLength"]
            segments_w_tripIDandP.loc[index,"CumulativeRouteTraveled"] = routeTravelled
            groupTrip.loc[index,"CumulativeRouteTraveled"] = routeTravelled
            groupTrip.loc[index,"DeltaTime"] = pd.to_datetime(row["L_TS"]) - pd.to_datetime(row["F_TS"])
            segments_w_tripIDandP.loc[index,"DeltaTime"] = pd.to_datetime(row["L_TS"]) - pd.to_datetime(row["F_TS"])
            segments_w_tripIDandP.loc[index,"AvgV"] =  3.6*segments_w_tripIDandP.loc[index,"SegLength"]/pd.to_timedelta(segments_w_tripIDandP.loc[index,"DeltaTime"]).seconds
            groupTrip.loc[index,"AvgV"] = 3.6*segments_w_tripIDandP.loc[index,"SegLength"]/pd.to_timedelta(segments_w_tripIDandP.loc[index,"DeltaTime"]).seconds
            
a=segments_w_tripIDandP["AvgV"].max()