# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 19:48:44 2019

@author: kocak
"""
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import sys
path = "C:/Users/kocak/OneDrive/Masaüstü/reag/"
sys.path.append(path)
import scutils
#%%
#Smart Card
# Read October Smart Card Info
sc = pd.read_csv(path+'10-ulasim_veri.csv',delimiter=';')
sc['ENLEM'] = pd.to_numeric(sc['ENLEM'].str.replace(',','.'))
sc['BOYLAM'] = pd.to_numeric(sc['BOYLAM'].str.replace(',','.'))

#Filter 30th October
sc30 = sc[(pd.to_datetime(sc["TIMESTAMP"]) >= pd.to_datetime('2018-10-30 02:59:59')) & (pd.to_datetime(sc["TIMESTAMP"]) < pd.to_datetime('2018-10-31 03:00:00')) & (sc["ENLEM"] > 0) & (sc["BOYLAM"] > 0)]
#%%
sc30.to_csv(path+"sc30oct.csv")
#%%
sc30 = pd.read_csv(path+"sc30oct.csv")
hatlar = [10,11,20,310,311,312,350,400,410,420,440,442,443,444,447,448,450,460]
hatlar = [447]
for i in hatlar:
    lid = str(i)[0:-1]
    slid = str(i)[-1]
    pathShape = path+"Hatlar/ULID"+lid+slid+".shp"
    road = gpd.read_file(pathShape)
    road.rename(columns={'D_NO_12':'D_NO_2','Shape_leng':'Sape_lengh'}, inplace=True)
    road["USID"] = "ULID"+road["ULID"].map(str)+"_"+road["D_SIRA_1"].map(str)+"_"+road["D_SIRA_2"].map(str)+"_"+road["D_NO_1"].map(str)+"_"+road["D_NO_2"].map(str)
    road["X1"] = pd.to_numeric(road["X1"])
    road["X2"] = pd.to_numeric(road["X2"])
    road["Y1"] = pd.to_numeric(road["Y1"])
    road["Y2"] = pd.to_numeric(road["Y2"])
    
    sc30_selected = sc30[(sc30["HAT_NO"]==int(lid))&(sc30["ALT_HAT_NO"]==int(slid))]
    sc30_selected["ShiftID"] = sc30_selected["HAT_NO"].map(str)+sc30_selected["ALT_HAT_NO"].map(str)+"_"+sc30_selected["ARAC_NO"].map(str)
    
    
    scutils.resetIndex(sc30_selected)
    
    sc30_sel_segment = scutils.createSegmentBase(sc30_selected,road)
    
    sc30_sel_segment1 = scutils.createMoveGroup(sc30_sel_segment)
    
    scutils.getLocalDurak(sc30_sel_segment1)
    
    sc30_sel_segment1 = scutils.getDirections(sc30_sel_segment1)
    sc_segments_w_tripID = scutils.getTripID(sc30_sel_segment1)
    
    sc_selected_result = scutils.assignScData(sc_segments_w_tripID,sc30_selected)
    
    
    sc_selected_result.to_csv(path+"SmartCardResults/ULID"+lid+slid+".csv")

#%%
    sc_selected_result.to_excel(path+"SmartCardResults/ULID"+lid+slid+".xlsx")