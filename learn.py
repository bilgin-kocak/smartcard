# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 21:03:50 2019

@author: kocak
"""
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# In[]+++
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

string1= "2843_2844_2845_2846_2847_2848_2849_2850_2851_"
string2 = "2851"
def addString(string1,string2):
    if string1[-len(string2)-1:-1] != string2:
        string1 += string2 + "_"
    
    return string1

#addString(string1, string2)

# In[]

# Group points in 100m buffer by SegmentID, VehicleID and DriverID
df_grouped = df.groupby(["USID","VID","DID"])

#List of dictionaries
rows = []

# To see it is the first row of the whole dataframe
first_row = True

# Will be append to the rows list
new_row = {}

# To see whether there is a row to be inserted
flag = 0
# sums for 50m buffer and 
sum50 = 0
sumAll = 0
in50mBuffer = ""
# Initialize first movegroup number
last_movement = 1
movement = 1
for i,g in df_grouped:
    # Sort current group by index
    g_sorted = g.sort_values(by = ["INDEX"])
    # Initialize prev_index to add previous index
    prev_index = -99
    
    # To see if it is the first member of the group
    new_group = True
    movement = 1
    
    
    # Travel through the sorted group
    for j, row in g_sorted.iterrows():
        if row["INDEX"] - prev_index < 2:
            if row["in_buffer_50"]:
                #in50mBuffer += str(row["INDEX"])+"_"
                in50mBuffer = addString(in50mBuffer, str(row["INDEX"]))
        
        if first_row == True:
            #in50mBuffer += str(row["INDEX"])+"_"
            in50mBuffer = addString(in50mBuffer, str(row["INDEX"]))
        # If it is the first row of the group but not of the dataframe (to insert the last element of the previous group)
        if new_group == True and first_row == False and flag == 1:
            #Add values of last row of the group
            new_row["L_IND"] = last_row["INDEX"]
            new_row["LP2FS"] = calculateDistance([last_row["POINT_LAT"],last_row["POINT_LON"]],[last_row["BUFFER1_LAT"],last_row["BUFFER1_LON"]])
            new_row["LP2LS"] = calculateDistance([last_row["POINT_LAT"],last_row["POINT_LON"]],[last_row["BUFFER2_LAT"],last_row["BUFFER2_LON"]])
            new_row["L_TS"] = last_row["TIMESTAMP"]
            new_row["LP_LAT"] = last_row["POINT_LAT"]
            new_row["LP_LON"] = last_row["POINT_LON"]
            new_row["SegLength"] = last_row["SegLength"]
            # Find the shift which point belongs to 
            start = shifts[(pd.to_datetime(shifts["Start_Time"]) <= pd.to_datetime(new_row["F_TS"])) & (pd.to_datetime(shifts["End_Time"]) >= pd.to_datetime(new_row["L_TS"])) & (shifts["VID"] == new_row["VID"])]["Start_Time"]
            end = shifts[(pd.to_datetime(shifts["Start_Time"]) <= pd.to_datetime(new_row["F_TS"])) & (pd.to_datetime(shifts["End_Time"]) >= pd.to_datetime(new_row["L_TS"])) & (shifts["VID"] == new_row["VID"])]["End_Time"]
            # Add ShiftID
            segid = "443_" + str(new_row["VID"]) + "_" + str(new_row["DID"]) + "_" + str(start.item()) + "_" +str(end.item()) 
            new_row["ShiftID"] = segid
            # Add movegroup information
            new_row["MVGRP"] = last_movement
            if last_row["in_buffer_50"]:
                in50mBuffer = addString(in50mBuffer, str(last_row["INDEX"]))
                #in50mBuffer += str(last_row["INDEX"])+"_"
            new_row["In50mBuffer"] = in50mBuffer
            # Initialize values again for the new group
            last_movement = 1
            rows.append(new_row)
            new_row = {}
            in50mBuffer = ""
            if row["in_buffer_50"]:
                in50mBuffer = addString(in50mBuffer, str(row["INDEX"]))
                #in50mBuffer += str(row["INDEX"])+"_"
            usid_list = row["USID"].split("_")
            # Rearrange segmentID
            usid = usid_list[0] + "_" + usid_list[3] + "_" + usid_list[4] + "_" + usid_list[1] + "_" + usid_list[2]
            new_row["SEGTID"] = usid
            new_row["F_TS"] = row["TIMESTAMP"]
            new_row["VID"] = row["VID"]
            new_row["DID"] = row["DID"]
            new_row["DURAK1_LAT"] = row["BUFFER1_LAT"]
            new_row["DURAK1_LON"] = row["BUFFER1_LON"]
            new_row["DURAK2_LAT"] = row["BUFFER2_LAT"]
            new_row["DURAK2_LON"] = row["BUFFER2_LON"]
            new_row["FP_LAT"] = row["POINT_LAT"]
            new_row["FP_LON"] = row["POINT_LON"]
            new_row["FP2FS"] = calculateDistance([row["POINT_LAT"],row["POINT_LON"]],[row["BUFFER1_LAT"],row["BUFFER1_LON"]])
            new_row["FP2LS"] = calculateDistance([row["POINT_LAT"],row["POINT_LON"]],[row["BUFFER2_LAT"],row["BUFFER2_LON"]])
            new_row["F_IND"] = row["INDEX"]
            
            # There are some values to be inserted
            flag = 1
            # We are not at the first value of the group anymore
            new_group = False
            
        # If there is a jump between previous index and current index, previous index is the last index of the movegroup    
        elif row["INDEX"] - prev_index > 2:
            # Since prev_index = -99 for the first row,1 - (-99) = 100 > 2 (however, there is nothing to be inserted), then we should check whether there is a need to divide movegroups
            # If it is not the first row and there is a row to be inserted 
            if first_row == False and flag == 1:

                # Append dictionary of the previous movegroup
                new_row["L_IND"] = last_row["INDEX"]
                new_row["LP2FS"] = calculateDistance([last_row["POINT_LAT"],last_row["POINT_LON"]],[last_row["BUFFER1_LAT"],last_row["BUFFER1_LON"]])
                new_row["LP2LS"] = calculateDistance([last_row["POINT_LAT"],last_row["POINT_LON"]],[last_row["BUFFER2_LAT"],last_row["BUFFER2_LON"]])
                new_row["L_TS"] = last_row["TIMESTAMP"]
                new_row["LP_LAT"] = last_row["POINT_LAT"]
                new_row["LP_LON"] = last_row["POINT_LON"]
                new_row["SegLength"] = last_row["SegLength"]
                # Find shift of the First and Last point of the movegroup
                start = shifts[(pd.to_datetime(shifts["Start_Time"]) <= pd.to_datetime(new_row["F_TS"])) & (pd.to_datetime(shifts["End_Time"]) >= pd.to_datetime(new_row["L_TS"])) & (shifts["VID"] == new_row["VID"])]["Start_Time"]
                end = shifts[(pd.to_datetime(shifts["Start_Time"]) <= pd.to_datetime(new_row["F_TS"])) & (pd.to_datetime(shifts["End_Time"]) >= pd.to_datetime(new_row["L_TS"])) & (shifts["VID"] == new_row["VID"])]["End_Time"]
                segid = "443_" + str(new_row["VID"]) + "_" + str(new_row["DID"]) + "_" + str(start.item()) + "_" +str(end.item()) 
                #segid = "443_" + str(new_row["VID"]) + "_" + str(new_row["DID"]) + "_" + str(new_row["FIRST_TS"] + "_" +str(new_row["LAST_TS"])) 
                new_row["ShiftID"] = segid
                new_row["MVGRP"] = movement
                if last_row["in_buffer_50"]:
                    in50mBuffer = addString(in50mBuffer, str(last_row["INDEX"]))
                    #in50mBuffer += str(last_row["INDEX"])+"_"
                new_row["In50mBuffer"] = in50mBuffer
                rows.append(new_row)
                # Initialize new movegroup of the group
                movement = movement + 1
                last_movement = movement
                flag = 0
                new_row = {}
                in50mBuffer = ""
                if row["in_buffer_50"]:
                    in50mBuffer = addString(in50mBuffer, str(row["INDEX"]))
                    #in50mBuffer += str(row["INDEX"])+"_"
                
            # Edit SegmentID of the current group
            usid_list = row["USID"].split("_")
            usid = usid_list[0] + "_" + usid_list[3] + "_" + usid_list[4] + "_" + usid_list[1] + "_" + usid_list[2]
            new_row["SEGTID"] = usid
            
            new_row["F_TS"] = row["TIMESTAMP"]
            new_row["VID"] = row["VID"]
            new_row["DID"] = row["DID"]
            new_row["FP_LAT"] = row["POINT_LAT"]
            new_row["FP_LON"] = row["POINT_LON"]
            new_row["DURAK1_LAT"] = row["BUFFER1_LAT"]
            new_row["DURAK1_LON"] = row["BUFFER1_LON"]
            new_row["DURAK2_LAT"] = row["BUFFER2_LAT"]
            new_row["DURAK2_LON"] = row["BUFFER2_LON"]
            new_row["FP2FS"] = calculateDistance([row["POINT_LAT"],row["POINT_LON"]],[row["BUFFER1_LAT"],row["BUFFER1_LON"]])
            new_row["FP2LS"] = calculateDistance([row["POINT_LAT"],row["POINT_LON"]],[row["BUFFER2_LAT"],row["BUFFER2_LON"]])
            new_row["F_IND"] = row["INDEX"]
            # Now, there is something to append, then flag = 1
            flag = 1
            
        # Keep information about the previous row
        prev_index = row["INDEX"]
        last_row = row
        first_row = False
        new_group = False
# If there is any value to be inserted, it should be inserted. 
if flag == 1:
    new_row["L_IND"] = last_row["INDEX"]
    new_row["LP2FS"] = calculateDistance([last_row["POINT_LAT"],last_row["POINT_LON"]],[last_row["BUFFER1_LAT"],last_row["BUFFER1_LON"]])
    new_row["LP2LS"] = calculateDistance([last_row["POINT_LAT"],last_row["POINT_LON"]],[last_row["BUFFER2_LAT"],last_row["BUFFER2_LON"]])
    new_row["L_TS"] = last_row["TIMESTAMP"]
    new_row["SegLength"] = last_row["SegLength"]
    start = shifts[(pd.to_datetime(shifts["Start_Time"]) <= pd.to_datetime(new_row["F_TS"])) & (pd.to_datetime(shifts["End_Time"]) >= pd.to_datetime(new_row["L_TS"])) & (shifts["VID"] == new_row["VID"])]["Start_Time"]
    end = shifts[(pd.to_datetime(shifts["Start_Time"]) <= pd.to_datetime(new_row["F_TS"])) & (pd.to_datetime(shifts["End_Time"]) >= pd.to_datetime(new_row["L_TS"])) & (shifts["VID"] == new_row["VID"])]["End_Time"]
    segid = "443_" + str(new_row["VID"]) + "_" + str(new_row["DID"]) + "_" + str(start.item()) + "_" +str(end.item())
    #segid = "443_" + str(new_row["VID"]) + "_" + str(new_row["DID"]) + "_" + str(new_row["FIRST_TS"]) + "_" +str(new_row["LAST_TS"])
    new_row["ShiftID"] = segid
    new_row["MVGRP"] = last_movement
    if last_row["in_buffer_50"]:
        in50mBuffer = addString(in50mBuffer, str(last_row["INDEX"]))
    new_row["In50mBuffer"] = in50mBuffer
    rows.append(new_row)
#%%
    rows_df = pd.DataFrame(rows).drop(columns = ["VID","DID"]);
    writer = pd.ExcelWriter('C:/Users/kocak/OneDrive/Masaüstü/reag/segment_with_inbuffer50m.xlsx')
    rows_df.to_excel(writer,'Sheet1',index=False)
    writer.save()