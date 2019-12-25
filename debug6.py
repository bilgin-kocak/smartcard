# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 10:21:05 2019

@author: kocak
"""
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import numpy as np

path = "C:/Users/kocak/OneDrive/Masaüstü/reag/"
shapefile = path+"ULID443_Guzargah_Durak/ULID443_Durak_split_v2.shp"
road = gpd.read_file(shapefile)

#%%
#october = pd.read_csv(path+'ekim.csv',delimiter=',')
#
#
##Filter 30th October
#
#oct30 = october[(pd.to_datetime(october["tarih_saat"]) >= pd.to_datetime('2018-10-30 02:59:59')) & (pd.to_datetime(october["tarih_saat"]) < pd.to_datetime('2018-10-31 03:00:00')) & (october["enlem"] > 0) & (october["boylam"] > 0)]
#oct30 = oct30[oct30["hat_no"]==44]
#oct30.to_csv(path+"oct30_gps.csv")
#%%
for i,row in road.iterrows():
    temp = row["USID"].split("_")
    road.loc[i,"USID"] = temp[0] +"_"+temp[3]+"_"+temp[4]+"_"+temp[1]+"_"+temp[2]
#df.to_csv(path+"buffer_100_updated.csv")
#%%
road.set_index("USID",inplace=True)
segments_w_tripID = pd.read_csv(path + "segment_directions_w_tripID&Passenger.csv")
df = pd.read_csv(path + "buffer_100.csv")
df = gpd.GeoDataFrame(df, geometry=[Point(x, y) for x,y in zip(df.POINT_LON, df.POINT_LAT)])
df.set_index("INDEX",inplace=True)
segments_w_tripID["N_F_IND"] = segments_w_tripID["F_IND"]
segments_w_tripID["N_L_IND"] = segments_w_tripID["L_IND"]
for shiftID, group in segments_w_tripID.groupby("ShiftID"):
    group = group.sort_values(by=["F_TS"])
    vehicleID = int(shiftID.split("_")[1])
    driverID = int(shiftID.split("_")[2])
    gps = df[(df["VID"]==vehicleID)&(df["DID"]==driverID)]
    isFirst = True
    for i,row in group.iterrows():
        if isFirst:
            isFirst = False
            prev_i = i
            continue
        segment1 = []
        segment2 = []
        if group.loc[prev_i,"L_IND"] >= row["F_IND"]:
            indexes = np.arange(row["F_IND"],group.loc[prev_i,"L_IND"]+1)
            for index in indexes:
                usid1 = group.loc[prev_i,"SEGTID"]
                usid2 = row["SEGTID"]
                gps_data = gps.loc[index]
                gps_data.drop_duplicates(subset="geometry",inplace = True)
                d1 = gps_data.geometry.distance(road.loc[usid1,"geometry"])
                d2 = gps_data.geometry.distance(road.loc[usid2,"geometry"])
                if d1.iloc[0] <= d2.iloc[0]:
                    segment1.append(index)
                else:
                    segment2.append(index)
            if len(indexes) == 0:
                prev_i = i
                continue
            if len(segment1) == 0:
                group.loc[prev_i,"N_L_IND"] = segment2[0]-1
            elif len(segment2) == 0:
                group.loc[i,"N_F_IND"] = segment1[-1] + 1
            else:
                group.loc[prev_i,"N_L_IND"] = segment1[-1]
                group.loc[i,"N_F_IND"] = segment2[0]
            prev_i = i
            
        
#    for ulid, groupGPS in gps.groupby("USID"):
#        tempDF = group[group["SEGTID"]==ulid]