#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 11:57:44 2019

@author: ulkem
"""

import pandas as pd
import numpy as np

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


sc = pd.read_csv("./10-ulasim_veri.csv",delimiter = ";")
segments = pd.read_csv("./segment_directions_w_tripID_.csv")
#segment = segments[segments["ShiftID"] == "443_211_224_2018-10-30 16:18:03_ 2018-10-30 19:00:37"]
sc['ENLEM'] = pd.to_numeric(sc['ENLEM'].astype(str).str.replace(',','.'))
sc['BOYLAM'] = pd.to_numeric(sc['BOYLAM'].astype(str).str.replace(',','.'))


# In[]
df_new = pd.DataFrame(columns = ["ULID","BILET_SERI_NO","POINT_LAT","POINT_LON","TS","DURAK1_LAT","DURAK1_LON","DURAK2_LAT","DURAK2_LON","MVGRP","SEGTID","ShiftID","DIRECTION","MOVED_DIR","R_DIR","tripID"])

for j,seg in segments.iterrows():
    vid = seg["ShiftID"].split("_")[1]
    lid = seg["ShiftID"].split("_")[0][:-1]
    slid = seg["ShiftID"].split("_")[0][-1]
    sc_filt = sc[(pd.to_datetime(sc["TIMESTAMP"]) >= pd.to_datetime(seg["F_TS"])) & (pd.to_datetime(sc["TIMESTAMP"]) <= pd.to_datetime(seg["L_TS"])) & (sc["ARAC_NO"] == int(vid)) & (sc["HAT_NO"] == int(lid)) & (sc["ALT_HAT_NO"] == int(slid))]
    for i,s in sc_filt.iterrows():
        dist = calculateDistance([s["ENLEM"],s["BOYLAM"]],[seg["DURAK1_LAT"],seg["DURAK1_LON"]])*1000
        dist2ls = calculateDistance([s["ENLEM"],s["BOYLAM"]],[seg["DURAK2_LAT"],seg["DURAK2_LON"]])*1000
        if dist > 50:
            status = "On Route"
        elif dist2ls < 50:
            status = "Next Stop"
        else:
            status = "Current Stop"
        if status == "On Route" or status == "Current Stop":
            df_new = df_new.append({'ULID': str(lid)+str(slid), 'BILET_SERI_NO': s["BILET_SERI_NO"], 'POINT_LAT': s['ENLEM'],"POINT_LON":s["BOYLAM"],"TS":s["TIMESTAMP"],"DURAK1_LAT":seg["DURAK1_LAT"],"DURAK1_LON":seg["DURAK1_LON"],"DURAK2_LAT":seg["DURAK2_LAT"],"DURAK2_LON":seg["DURAK2_LON"],"MVGRP":seg["MVGRP"],"SEGTID":seg["SEGTID"],"ShiftID":seg["ShiftID"],"DIRECTION":seg["DIRECTION"],"MOVED_DIR":seg["MOVED_DIR"],"R_DIR":seg["R_DIR"],"tripID":seg["tripID"],"dist2fs":dist,"Stop" : seg["MV_DIR_F"],"Status":status}, ignore_index=True)
        else:
            df_new = df_new.append({'ULID': str(lid)+str(slid), 'BILET_SERI_NO': s["BILET_SERI_NO"], 'POINT_LAT': s['ENLEM'],"POINT_LON":s["BOYLAM"],"TS":s["TIMESTAMP"],"DURAK1_LAT":seg["DURAK1_LAT"],"DURAK1_LON":seg["DURAK1_LON"],"DURAK2_LAT":seg["DURAK2_LAT"],"DURAK2_LON":seg["DURAK2_LON"],"MVGRP":seg["MVGRP"],"SEGTID":seg["SEGTID"],"ShiftID":seg["ShiftID"],"DIRECTION":seg["DIRECTION"],"MOVED_DIR":seg["MOVED_DIR"],"R_DIR":seg["R_DIR"],"tripID":seg["tripID"],"dist2fs":dist,"Stop" : seg["MV_DIR_L"],"Status":status}, ignore_index=True)






'''
sc_grouped = sc.groupby("BILET_SERI_NO")
for i,g in sc_grouped:
    
    sc_sorted = sc_grouped.sort_values("TIMESTAMP")
    for j,s in sc_sorted.iterrows():'''
    
# In[]
#df_new['POINT_LAT'] = pd.to_numeric(df_new['POINT_LAT'].astype(str).str.replace(',','.'))
#df_new['POINT_LON'] = pd.to_numeric(df_new['POINT_LON'].astype(str).str.replace(',','.'))
df_new.to_csv("./sc_w_tripID.csv")