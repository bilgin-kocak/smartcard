# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 14:22:35 2019

@author: Ulkem
"""

import pandas as pd

# Read smart card and gps shifts

gps_shifts = pd.read_csv("C:/Users/kocak/OneDrive/Masaüstü/reag/Oct24_publicTransportation_withStartandEndTime.csv")
sc_shifts = pd.read_csv("C:/Users/kocak/OneDrive/Masaüstü/reag/Oct24_publicTransportation_withStartandEndTime_sc.csv")
#%%
gps_shi = gps_shifts[(gps_shifts["VID"]==248)& (gps_shifts["DRIVER_ID"]==269)&(gps_shifts["LID"]==44)]
#%%
sc_shi = sc_shifts[(sc_shifts["LID"]==44)&(sc_shifts["VID"]==248)]
# In[1]
gps_shifts = gps_shifts.sort_values(by = ["VID","Start_Time"])
sc_shifts = sc_shifts.sort_values(by = ["VID","Start_Time"])

f = open("C:/Users/kocak/OneDrive/Masaüstü/reag/NewConcated_Oct24_publicTransportation_withStartandEndTime.csv","w")
f.write("LID,SLID,VID,DID,Start_Time,End_Time,Status\n")
is_first = 1
endstr = ""
endstr1 = ""
printed = 0
printed1 = 0
isin = 0
for i,gps in gps_shifts.iterrows():
    
    if (is_first == 0 and isin == 1):
        f.write(endstr)
    isin = 0
    flag = 0
    end = ""
    is_first = 0
    # If it is not a datum which has one row or from tram
    if gps["LID"] != 10 and gps["Event_Type"] != " ----":
        sc = sc_shifts[(sc_shifts["VID"] == gps["VID"]) & (sc_shifts["LID"] == gps["LID"])  & (sc_shifts["Event_Type"] != " ----")]
        # If there are corresponding SC shifts with that GPS Shift properties
        if len(sc) > 0:
            for index,s in sc.iterrows():
                # Labeling stage
                if (pd.to_datetime(s["Start_Time"]) >= pd.to_datetime(gps["Start_Time"]) and pd.to_datetime(gps["End_Time"]) >= pd.to_datetime(s["End_Time"]) ):
                    isin = 1
                    if flag == 0:
                        toBePrinted1 = str(gps["LID"]) + "," + str(s["SLID"]) + "," + str(s["VID"]) + "," + str(gps["DRIVER_ID"]) + "," + str(gps["Start_Time"]) + "," + str(s["Start_Time"]) + ",Start w/o passenger\n" + str(gps["LID"]) + "," + str(s["SLID"]) + "," + str(s["VID"]) + "," + str(gps["DRIVER_ID"]) + "," + str(s["Start_Time"]) + "," + str(s["End_Time"]) + ",With passenger\n"
                        f.write(toBePrinted1)
                        flag = 1
                        end = s["End_Time"]
                        endstr = str(gps["LID"]) + "," + str(s["SLID"]) + "," + str(s["VID"]) + "," + str(gps["DRIVER_ID"]) +  "," + str(s["End_Time"]) + "," + str(gps["End_Time"]) + ",No pass\n"
                        printed = 0
                    elif flag == 1:
                        toBePrinted3 = str(gps["LID"]) + "," + str(s["SLID"]) + "," + str(s["VID"]) + "," + str(gps["DRIVER_ID"]) + "," +  str(end) + "," + str(s["Start_Time"]) + ",Start w/o passenger\n" + str(gps["LID"]) + "," + str(s["SLID"]) + "," + str(s["VID"]) + "," + str(gps["DRIVER_ID"]) + "," + str(s["Start_Time"]) + "," + str(s["End_Time"]) + ",With passenger\n"
                        f.write(toBePrinted3)
                        end = s["End_Time"]
                        printed1 = 0
                        endstr = str(gps["LID"]) + "," + str(s["SLID"]) + "," + str(s["VID"]) + "," + str(gps["DRIVER_ID"]) +  "," + str(s["End_Time"]) + "," + str(gps["End_Time"]) + ",No pass\n"
f.close()

#%%
dfsa = pd.read_csv("C:/Users/kocak/OneDrive/Masaüstü/reag/NewConcated_Oct24_publicTransportation_withStartandEndTime.csv")
#%%
writer = pd.ExcelWriter('C:/Users/kocak/OneDrive/Masaüstü/reag/.xlsx')
df.to_excel(writer,'Sheet1',index=False)
writer.save()
#%%
gps1 = pd.read_csv(path+"Oct24_publicTransportation_withStartandEndTime.csv")
sc = pd.read_csv(path+"Oct24_publicTransportation_withStartandEndTime_sc.csv")
sc12 = sc[sc["LID"]==47]
gps12 = gps[gps["LID"]==47]
dfsa1 = dfsa[dfsa["LID"]==47]
