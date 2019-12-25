#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:21:03 2019

@author: ulkem
"""

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
#%%
# Get GPS and SHifts Data
shifts = pd.read_csv("C:/Users/kocak/OneDrive/Masaüstü/reag/shifts.csv")
sc = pd.read_csv("C:/Users/kocak/OneDrive/Masaüstü/reag/ekim.csv",delimiter=',')


# Change lat,lon columns to numeric type
sc['enlem'] = pd.to_numeric(sc['enlem'].astype(str).str.replace(',','.'))
sc['boylam'] = pd.to_numeric(sc['boylam'].astype(str).str.replace(',','.'))


# In[filter]

# Get 30-10-2018 
sc = sc[ (sc["enlem"] > 0) & (sc["boylam"] > 0) & (pd.to_datetime(sc["tarih_saat"]) > "2018-10-30 02:59:59") & (pd.to_datetime(sc["tarih_saat"]) < "2018-10-31 03:00:00") ]
#%%
# Get ULID 443
shifts = shifts[(shifts["LID"] == 44) & (shifts["SLID"] == 3)]

# In[Buffer]

# Get ULID 443
shifts = shifts[(shifts["LID"] == 44) & (shifts["SLID"] == 3)]

#Read selected file path
path = "C:/Users/kocak/OneDrive/Masaüstü/reag/ULID443_Guzargah_Durak/ULID443_Durak_split_v2.shp"
test = gpd.read_file(path)


# Sort shifts by Shift Start Time
shifts = shifts.sort_values(by = ["Start_Time"])

# Create a column that is from Point(lon,lat) format
sc = gpd.GeoDataFrame(sc,geometry=[Point(x, y) for x,y in zip(sc.boylam, sc.enlem)])

# Add 100m,50m,30m,10m line buffer to the line 
buffer_ = test.copy()
buffer_["geometry_100"] = ""
buffer_["geometry_50"] = ""
buffer_["geometry_30"] = ""
buffer_["geometry_10"] = ""
buffer_.geometry_100 = buffer_['geometry'].buffer(0.0009009009)
buffer_.geometry_50 = buffer_['geometry'].buffer(0.00045045045)
buffer_.geometry_30 = buffer_['geometry'].buffer(0.00022522522)
buffer_.geometry_10 = buffer_['geometry'].buffer(0.00009009009)


# Flag to see whether the segment is in 100m buffer of a segment
flag = 0


# list to be list of dictionaries (dictionaries will be converted to corresponding dataframe row)
lst = []

for j,s in shifts.iterrows():
    # Filter GPS data with the same VID and in between shift start and end time
    selected = sc[(pd.to_datetime(sc["tarih_saat"]) >= pd.to_datetime(s["Start_Time"])) & (pd.to_datetime(sc["tarih_saat"]) < pd.to_datetime(s["End_Time"])) & (sc["arac_no"] == s["VID"])]
    # Sort filtered GPS values by timestamp
    selected = selected.sort_values(by = ["tarih_saat"])
    # Add index column to sorted data 
    selected = selected.reset_index(drop = True)
    
    # For each filtered and indexed GPS data
    for k, c in selected.iterrows():
        # For each buffer geometry in the segment
        for i,b in buffer_.iterrows():
            # Initialize a dictionary
            d = {}
            d["INDEX"] = k 
            # If 100m buffer contains point's geometry  - (contains is a geopandas function)
            if (b.geometry_100).contains(c["geometry"]):
                flag = 1
                d["in_buffer_100"] = True
                d["VID"] = c["arac_no"]
                d["TIMESTAMP"] = c["tarih_saat"]
                d["DID"] = c["surucu_no"]
                d["POINT_LAT"] = c["enlem"]
                d["POINT_LON"] = c["boylam"]
                d["BUFFER1_LAT"] = b["Y1"]
                d["BUFFER1_LON"] = b["X1"]
                d["BUFFER2_LAT"] = b["Y2"]
                d["BUFFER2_LON"] = b["X2"]
                d["DURAK_SIRA_1"] = b["D_SIRA_1"]
                d["DURAK_SIRA_2"] = b["D_SIRA_2"]
                d["DURAK_NO_1"] = b["D_NO_1"]
                d["DURAK_NO_2"] = b["D_NO_2"]
                d["USID"] = b["USID"]
                d["SegLength"] = b["Sape_lengh"]
                

            else:
                d["in_buffer_100"] = False
                d["VID"] = c["arac_no"]
                d["TIMESTAMP"] = c["tarih_saat"]
                d["DID"] = c["surucu_no"]
                d["POINT_LAT"] = c["enlem"]
                d["POINT_LON"] = c["boylam"]
                d["BUFFER1_LAT"] = b["Y1"]
                d["BUFFER1_LON"] = b["X1"]
                d["BUFFER2_LAT"] = b["Y2"]
                d["BUFFER2_LON"] = b["X2"]
                d["DURAK_SIRA_1"] = b["D_SIRA_1"]
                d["DURAK_SIRA_2"] = b["D_SIRA_2"]
                d["DURAK_NO_1"] = b["D_NO_1"]
                d["DURAK_NO_2"] = b["D_NO_2"]
                d["USID"] = b["USID"]
                d["SegLength"] = b["Sape_lengh"]
                
                
            # If 50m buffer contains point's geometry  - (contains is a geopandas function)
            if (b.geometry_50).contains(c["geometry"]):
                d["in_buffer_50"] = True
                flag1 = 1
            else:
                d["in_buffer_50"] = False
                
                
            # If 30m buffer contains point's geometry  - (contains is a geopandas function)
            if (b.geometry_30).contains(c["geometry"]):
                d["in_buffer_30"] = True
            else:
                d["in_buffer_30"] = False      
                
                
            # If 10m buffer contains point's geometry
            if (b.geometry_10).contains(c["geometry"]):
                d["in_buffer_10"] = True
            else:
                d["in_buffer_10"] = False
            # If the point is in 100m buffer, append the point to the list
            if flag == 1:
                #print(d)
                flag = 0
                lst.append(d)
                #print(lst[-1])
# List of dictionaries to pandas dataframe
df = pd.DataFrame(lst)
#%%

df.to_csv("C:/Users/kocak/OneDrive/Masaüstü/reag/buffer_100.csv") 
writer = pd.ExcelWriter('C:/Users/kocak/OneDrive/Masaüstü/reag/Pandas-Example2.xlsx')
df.to_excel(writer,'Sheet1',index=False)
writer.save()

#%%
df = pd.read_csv("C:/Users/kocak/OneDrive/Masaüstü/reag/buffer_100.csv")    

# In[]
# Filtering operations for 50m and 30m buffer and create those files
df_50 = df[(df["in_buffer_10"] == True) | (df["in_buffer_30"] == True)| (df["in_buffer_50"])]
df_50.to_csv("C:/Users/kocak/OneDrive/Masaüstü/reag/buffer_50_segmented.csv")
df_30 = df[(df["in_buffer_10"] == True) | (df["in_buffer_30"] == True)]
df_30.to_csv("C:/Users/kocak/OneDrive/Masaüstü/reag/buffer_30_segmented.csv")

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
            # Initialize values again for the new group
            last_movement = 1
            rows.append(new_row)
            new_row = {}
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
                rows.append(new_row)
                # Initialize new movegroup of the group
                movement = movement + 1
                last_movement = movement
                flag = 0
                new_row = {}
                
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
    rows.append(new_row)



# In[]
# Since VID and DID is in ShiftID, VID and DID can be dropped     
rows_df = pd.DataFrame(rows).drop(columns = ["VID","DID"])
#%%
# Distances are converted from km to m
rows_df["FP2FS"] = rows_df["FP2FS"] * 1000
rows_df["LP2FS"] = rows_df["LP2FS"] * 1000
rows_df["FP2LS"] = rows_df["FP2LS"] * 1000
rows_df["LP2LS"] = rows_df["LP2LS"] * 1000


# Write to file
rows_df.to_csv("C:/Users/kocak/OneDrive/Masaüstü/reag/segments_and_distances_100m.csv")
#%%
rows_df = pd.read_csv("C:/Users/kocak/OneDrive/Masaüstü/reag/segments_and_distances_100m.csv")


# In[Direction]

# Initialize DIRECTION column
rows_df["DIRECTION"] = 0


for i,row in rows_df.iterrows():
    # Get VehicleID from ShiftID
    vid = int(row["ShiftID"].split("_")[1])
    
    # To decide on true direction
    if (row["FP2FS"] < row["FP2LS"] and row["LP2FS"] > row["LP2LS"]):
        rows_df.loc[i,"DIRECTION"] = 1
        
    
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
#%%

rows_df = pd.read_csv("C:/Users/kocak/OneDrive/Masaüstü/reag/segments_w_directions.csv")
# In[]


# Basic operations of DIRECTIONs
lst = []
rows_df["LOCAL_SEQ_DIR"] = ""
rows_df["MOVED_DIR"] = ""
rows_df["R_DIR"] = ""
rows_df["LOCAL_DIR"] = ""
rows_df["MV_DIR_F"] = ""
rows_df["MV_DIR_L"] = ""

for i, row in rows_df.iterrows():
    info_list = row["SEGTID"].split("_")
    rows_df.loc[i,"LOCAL_SEQ_DIR"] = str(info_list[1]) + "_" + str(info_list[2])
    rows_df.loc[i,"LOCAL_DIR"] = str(info_list[3]) + "_" + str(info_list[4])
    
    if row["DIRECTION"] == 1:
        info_list = row["SEGTID"].split("_")
        rows_df.loc[i,"MOVED_DIR"] = str(info_list[1]) + "_" + str(info_list[2])
        rows_df.loc[i,"R_DIR"] = info_list[3] + "_" + info_list[4]
        rows_df.loc[i,"MV_DIR_F"] = int(info_list[3])
        rows_df.loc[i,"MV_DIR_L"] = int(info_list[4])
        
        rows_df.loc[i,"FP_LP"] = str(row["F_IND"]) + "_" + str(row["L_IND"])
    else:
        info_list = row["SEGTID"].split("_")
        rows_df.loc[i,"MOVED_DIR"] = str(info_list[2]) + "_" + str(info_list[1])
        rows_df.loc[i,"R_DIR"] = info_list[4] + "_" + info_list[3]
        rows_df.loc[i,"MV_DIR_F"] = int(info_list[4])
        rows_df.loc[i,"MV_DIR_L"] = int(info_list[3])
        rows_df.loc[i,"FP_LP"] = str(row["F_IND"]) + "_" + str(row["L_IND"])

rows_df.to_csv("./segment_directions_last.csv")
#%%
rows_df.to_excel("./segment_directions_last.xlsx")

# In[]

# Filter right direction
rows_filtered = rows_df[rows_df["DIRECTION"] == 1]

# Group filtered values by SegmentID and ShiftID
rows_grouped = rows_filtered.groupby(["SEGTID","ShiftID"])
# Initialize new movegroups
rows_filtered["MVGRP"] = -1

# Edit movegroups
for i,g in rows_grouped:
    is_first = True
    move = 1
    for j,row in g.iterrows():
        if is_first:
            move = 1
            rows_filtered.loc[j,"MVGRP"] = move
            is_first = False
        else:
            rows_filtered.loc[j,"MVGRP"] = move
        move = move + 1


rows_filtered.to_csv("./segment_directions_last_filtered.csv")

#%%
import pandas as pd
import numpy as np

rows_filtered = pd.read_csv("C:/Users/kocak/OneDrive/Masaüstü/reag/segment_directions_last_filtered.csv") 
# In[ExtractTrip]


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
# In[]
rows_filtered.to_csv("./segment_directions_w_tripID_.csv")        
rows_filtered.to_excel("./segment_directions_w_tripID_.xlsx") 




