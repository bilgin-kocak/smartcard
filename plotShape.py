# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 22:05:48 2019

@author: kocak
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
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