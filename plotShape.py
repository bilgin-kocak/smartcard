# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 22:05:48 2019

@author: kocak
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import numpy as np
#%%
path = "C:/Users/kocak/OneDrive/Masaüstü/reag/"
pathShape = "C:/Users/kocak/OneDrive/Masaüstü/reag/ULID443_Guzargah_Durak/ULID443_Durak_split_v2.shp"
road = gpd.read_file(pathShape)
#sc30 = pd.read_csv("smart_card_30oct_w_tripID.csv")
road=road.sort_values(by=["D_SIRA_1"])

buffer_100 = road.copy()
buffer_100.geometry = road['geometry'].buffer(0.0009009009)

buffer_50 = gpd.GeoDataFrame(road,geometry = [Point(x, y) for x,y in zip(road.X1, road.Y1)])
buffer_50.geometry = buffer_50["geometry"].buffer(0.00045045045)

ax = buffer_100.plot(color = "cyan")
road.plot(color="red", ax = ax)
buffer_50.plot(color="pink",ax = ax)

plt.scatter(road["X1"],road["Y1"],c="black")
plt.scatter(road.loc[13,"X2"],road.loc[13,"Y2"],c="black")
#
#plt.scatter(sc30["BOYLAM"],sc30["ENLEM"],c="yellow",edgecolor="darkblue",marker="d")
plt.scatter(sc30_notGPS["BOYLAM"],sc30_notGPS["ENLEM"],c="yellow",edgecolor="darkblue",marker="d")
#for i,row in road.iterrows():
#    plt.text(row["X1"],row["Y1"],row["D_SIRA_1"],fontsize=12,color="black")

for i,row in sc30_notGPS.iterrows():
    plt.text(row["BOYLAM"],row["ENLEM"],row["AssignedStopID"],fontsize=12,color="black")    

#sc30NotInBuffer = sc30[(sc30["Stat"]==0)&(sc30["ARAC_NO"]==248)]
#plt.scatter(sc30NotInBuffer["BOYLAM"],sc30NotInBuffer["ENLEM"],c="yellow",edgecolor="darkblue",marker="d")

#plt.scatter(oct30_1["boylam"],oct30_1["enlem"],c="yellow",edgecolor="darkblue",marker="d")

#for i,row in sc30NotInBuffer.iterrows():
#    plt.text(row["BOYLAM"],row["ENLEM"],row["TIMESTAMP"],fontsize=12,color="black")
#%%
#sc_segments_FP.loc[i].plot()
ax=sc_segments50_FP.loc[[i]].plot(color="red")
sc_segments50_LP.loc[[i]].plot(ax=ax)
plt.scatter(row_sc["BOYLAM"],row_sc["ENLEM"],c="yellow",edgecolor="darkblue",marker="d")
#%%
path = "C:/Users/kocak/OneDrive/Masaüstü/reag/"
sc30 = pd.read_csv(path+"sc30oct.csv")
hatlar = [10,11,20,310,311,312,350,400,410,420,440,442,443,444,447,448,450,460]
hatlar = [443]
for day in range(23):
    day = 29
    for i in hatlar:
        lid = str(i)[0:-1]
        slid = str(i)[-1]
        pathShape = path+"Hatlar/ULID"+lid+slid+".shp"
        road = gpd.read_file(pathShape)
        road.rename(columns={'D_NO_12':'D_NO_2','Shape_leng':'Sape_lengh'}, inplace=True)
        road["USID"] = "ULID"+lid+slid+"_"+road["D_SIRA_1"].map(str)+"_"+road["D_SIRA_2"].map(str)+"_"+road["D_NO_1"].map(str)+"_"+road["D_NO_2"].map(str)
        road["X1"] = pd.to_numeric(road["X1"])
        road["X2"] = pd.to_numeric(road["X2"])
        road["Y1"] = pd.to_numeric(road["Y1"])
        road["Y2"] = pd.to_numeric(road["Y2"])
        #sc30 = pd.read_csv("smart_card_30oct_w_tripID.csv")
        road=road.sort_values(by=["D_SIRA_1"])
        buffer_100 = road.copy()
        buffer_100.geometry = road['geometry'].buffer(0.0009009009)
        buffer_50 = gpd.GeoDataFrame(road,geometry = [Point(x, y) for x,y in zip(road.X1, road.Y1)])
        buffer_50.geometry = buffer_50["geometry"].buffer(0.00045045045)
        ax = buffer_100.plot(color = "cyan")
        road.plot(color="red", ax = ax)
        buffer_50.plot(color="pink",ax = ax)
        sc30_selected = pd.read_csv(path+"SmartCardResults/ULID"+lid+slid+"_"+str(day+1)+"oct.csv")
        sc_sel = sc30_selected[sc30_selected['Stat']==0]
#        plt.scatter(sc_sel["BOYLAM"],sc_sel["ENLEM"],c="yellow",edgecolor="darkblue",marker="d")
#        for i,row in sc_sel.iterrows():
#            plt.text(row["BOYLAM"],row["ENLEM"],row["ARAC_NO"],fontsize=12,color="black")
        plt.scatter(sc30_selected["BOYLAM"],sc30_selected["ENLEM"],c="yellow",edgecolor="darkblue",marker="d")
        for i,row in sc30_selected.iterrows():
            plt.text(row["BOYLAM"],row["ENLEM"],row["AssignedStopID"],fontsize=12,color="black")    
#%%

pathShape = path+"Hatlar/ULID410.shp"
road = gpd.read_file(pathShape)
#%%
road=road.sort_values(by=["D_SIRA_1"])
buffer_100 = road.copy()
buffer_100.geometry = road['geometry'].buffer(0.0009009009)
buffer_50 = gpd.GeoDataFrame(road,geometry = [Point(x, y) for x,y in zip(road.X1, road.Y1)])
buffer_50.geometry = buffer_50["geometry"].buffer(0.00045045045)
ax = buffer_100.plot(color = "cyan")
road.plot(color="red", ax = ax)
buffer_50.plot(color="pink",ax = ax)

sc30_selected = pd.read_csv(path+"SmartCardResults/ULID10.csv")
sc_sel = sc30_selected[sc30_selected['Stat']==0]
#        plt.scatter(sc_sel["BOYLAM"],sc_sel["ENLEM"],c="yellow",edgecolor="darkblue",marker="d")
#        for i,row in sc_sel.iterrows():
#            plt.text(row["BOYLAM"],row["ENLEM"],row["ARAC_NO"],fontsize=12,color="black")
plt.scatter(sc30_selected["BOYLAM"],sc30_selected["ENLEM"],c="yellow",edgecolor="darkblue",marker="d")
    for i,row in sc30_selected.iterrows():
        plt.text(row["BOYLAM"],row["ENLEM"],row["AssignedStopID"],fontsize=12,color="black")    
        