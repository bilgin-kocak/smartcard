# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 22:59:43 2019

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

ax = road.plot(color="red")

plt.scatter(road["X1"],road["Y1"],c="black")
plt.scatter(road.loc[13,"X2"],road.loc[13,"Y2"],c="black")
#
gps_selected = gps[(gps.index<=68)&(gps.index>=62)]
gps_selected.drop_duplicates(subset="geometry",inplace = True)

for i in range(62,69):
    plt.scatter(gps_selected.loc[i,"POINT_LON"],gps_selected.loc[i,"POINT_LAT"],c="yellow",edgecolor="darkblue",marker="d")
    plt.text(gps_selected.loc[i,"POINT_LON"],gps_selected.loc[i,"POINT_LAT"],i,fontsize=12,color="black") 