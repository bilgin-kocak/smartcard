# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 21:00:55 2019

@author: kocak
"""
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

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
#%%
    
#string = "1541_1542_1543_1544_1545_1546_1547_1548_1549_1550_1551_1552"
string = "100_105"
def calculateNumbers(string):
    l = string.split("_")
    return len(l) 
def calculateDifference(string):
    l = string.split("_")
    return int(l[1]) - int(l[0])+1

for i,row in rows_df.iterrows():
    rows_df.loc[i,"#50mBuffer"] = calculateNumbers(row["In50mBuffer"][:-1])
    rows_df.loc[i,"#100mBuffer"] = int(row["L_IND"]) - int(row["F_IND"])+1