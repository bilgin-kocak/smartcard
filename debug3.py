# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 14:26:15 2019

@author: ce-user
"""
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import sys
path = "C:/Users/kocak/OneDrive/Masaüstü/reag/"
sys.path.append(path)
import scutils
sc30_notGPS = pd.read_csv(path+"smart_card_30oct_notGPS_w_tripID.csv")
sc30_notGPS1 = scutils.resetIndex(sc30_notGPS)
#%%
dff = scutils.createSegmentBase(sc30_notGPS1)
#%%
#dff1 = scutils.getIndex(dff)
#%%
dff.to_csv(path+"only_sc_30oct.csv")
#%%
dff = pd.read_csv(path+"only_sc_30oct.csv")
dff2 = scutils.createMoveGroup(dff)
#%%
dff2 = scutils.getLocalDurak(dff2)
#%%
dff2 = scutils.getDirections(dff2)
sc_segments_w_tripID = scutils.getTripID(dff2)
#%%
sc_segments_w_tripID.to_csv(path + "smartcardOct30_segmentbased_w_tripID.csv")
#%%
shapefile = path+"ULID443_Guzargah_Durak/ULID443_Durak_split_v2.shp"
road = gpd.read_file(shapefile)

road.plot(color="red")

sc30_360 = sc30_notGPS[sc30_notGPS["ARAC_NO"]==360]
sc30_360 = sc30_360.sort_values(by=["TIMESTAMP"])
sc30_360["LocalID"] = 0
tempId = 1


#plt.scatter(sc30_360["BOYLAM"],sc30_360["ENLEM"], marker="d",c="yellow",edgecolors="darkblue")
for i,row in sc30_360.iterrows():
    if tempId >= 10:
        break
    sc30_360.loc[i,"LocalID"] = tempId
    plt.scatter(row["BOYLAM"],row["ENLEM"], marker="d",c="yellow",edgecolors="darkblue")
    plt.text(row["BOYLAM"],row["ENLEM"],str(tempId),fontsize=12)
    tempId = tempId + 1