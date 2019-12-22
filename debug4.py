# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 10:11:52 2019

@author: kocak
"""
# trip çıkar bir tane 129-130 to 1-2 var onu düzelt.
import pandas as pd

dff3 = dff2[dff2["Direction"]==1]
for i, group in dff3.groupby("ShiftID"):
    listIndexes = []
    group = group.sort_values(["F_TS","ST1"])
    for index1,row1 in group.iterrows():
        listIndexes.append(index1)
    firstRow = True
    for index,row in group.iterrows():
        if firstRow:
            tripID = 1
            group.loc[index,"TripID"] = tripID
            dff3.loc[index,"TripID"] = tripID
            fs = row["ST1"]
            firstRow = False
            continue
        if row["ST1"] < fs:
            listForSearch = listIndexes[listIndexes.index(index):]
            if group.loc[listForSearch[0],"F_IND"] == group.loc[listForSearch[1],"F_IND"] and \
            group.loc[listForSearch[0],"L_IND"] == group.loc[listForSearch[1],"L_IND"] and \
            group.loc[listForSearch[1],"ST1"] > fs:
                tripID +=0
                group.loc[index,"TripID"] = tripID + 1
                group.loc[listForSearch[1],"TripID"] = tripID
                dff3.loc[index,"TripID"] = tripID + 1
                dff3.loc[listForSearch[1],"TripID"] = tripID
                fs = row["ST1"]
                continue
            else:
                tripID +=1
        group.loc[index,"TripID"] = tripID
        dff3.loc[index,"TripID"] = tripID
        fs = row["ST1"]

sc_segments_w_tripID = dff3            
#%%
from shapely.geometry import Point
import geopandas as gpd
sc_segments_w_tripID["#ofPassengers"] = 0
sc_segments_w_tripID["#ofPassenger@FS"] = 0 
sc_segments_w_tripID["#ofPassenger@LS"] = 0 
sc_segments_w_tripID["#ofPassenger@Route"] = 0 
#sc30["ShiftID"] = ""
#sc30["tripID"] = 0
#sc30["AssignedStopID"] = ""
#sc30["Stat"] = 0      # 0 means on route, 1 means at stop
#gpsAracNo = []
sc_segments_FP = gpd.GeoDataFrame(index=sc_segments_w_tripID.index,crs={'init':'epsg:4326'},geometry=[Point(x, y) for x,y in zip(sc_segments_w_tripID.DURAK1_LON, sc_segments_w_tripID.DURAK1_LAT)])
sc_segments_LP = gpd.GeoDataFrame(index=sc_segments_w_tripID.index,geometry=[Point(x, y) for x,y in zip(sc_segments_w_tripID.DURAK2_LON, sc_segments_w_tripID.DURAK2_LAT)])
sc_segments_FP["geometry50_FP"] = sc_segments_FP["geometry"].buffer(0.00045045045)
sc_segments_FP["geometry100_FP"] = sc_segments_FP["geometry"].buffer(0.0009009009)
sc_segments_LP["geometry50_LP"] = sc_segments_LP["geometry"].buffer(0.00045045045)
sc_segments_LP["geometry100_LP"] = sc_segments_LP["geometry"].buffer(0.0009009009)
sc_segments50_FP = gpd.GeoDataFrame(index=sc_segments_FP.index,crs={'init':'epsg:4326'},geometry = sc_segments_FP["geometry50_FP"] )
sc_segments50_LP = gpd.GeoDataFrame(index=sc_segments_LP.index,crs={'init':'epsg:4326'},geometry = sc_segments_LP["geometry50_LP"] )
#%%
sc30_notGPS = gpd.GeoDataFrame(sc30_notGPS,geometry =[Point(x, y) for x,y in zip(sc30_notGPS.BOYLAM, sc30_notGPS.ENLEM)] )
sc30_notGPS["AssignedStopID"] = "null"
sc30_notGPS["Stat"] = 0
for shiftID, group in sc_segments_w_tripID.groupby("ShiftID"):
    group = group.sort_values(by=["F_TS"])
    scForGroup = sc30_notGPS[(sc30_notGPS["ARAC_NO"]== int(shiftID[4:7]))]
#    gpsAracNo.append(int(shiftID[4:7]))
    isFirstRow = True
    for i, row in group.iterrows():
        sc_between_segment = scForGroup[(pd.to_datetime(scForGroup["TIMESTAMP"]) >= pd.to_datetime(row["F_TS"])) & (pd.to_datetime(scForGroup["TIMESTAMP"]) <= pd.to_datetime(row["L_TS"]))]
        sc_segments_w_tripID.loc[i,"#ofPassenger"] = sc_between_segment.shape[0]
        splitedSegtID = row["SEGTID"].split("_")
        if isFirstRow:
            indexesForFS = []
            indexesForLS = []
            indexesForRoute = []
            for index, row_sc in sc_between_segment.iterrows():
                sc30_notGPS.loc[index,"ShiftID"] = row["ShiftID"]
                sc30_notGPS.loc[index,"tripID"] = row["TripID"]
                if sc_segments_FP.loc[i,"geometry50_FP"].contains(row_sc["geometry"]):
                    indexesForFS.append(index)
                    sc30_notGPS.loc[index,"AssignedStopID"] = splitedSegtID[3]
                    sc_between_segment.loc[index,"AssignedStopID"] = splitedSegtID[3]
                elif sc_segments_LP.loc[i,"geometry50_LP"].contains(row_sc["geometry"]):
                    indexesForLS.append(index)
                    sc30_notGPS.loc[index,"AssignedStopID"] = splitedSegtID[4]
                    sc_between_segment.loc[index,"AssignedStopID"] = splitedSegtID[4]
                else:
                    indexesForRoute.append(index)
                    distanceToFS = calculateDistance([row_sc["ENLEM"],row_sc["BOYLAM"]],[row["DURAK1_LAT"],row["DURAK1_LON"]])
                    distanceToLS = calculateDistance([row_sc["ENLEM"],row_sc["BOYLAM"]],[row["DURAK2_LAT"],row["DURAK2_LON"]])
                    distanceBetweenFS_LS = calculateDistance([row["DURAK1_LAT"],row["DURAK1_LON"]],[row["DURAK2_LAT"],row["DURAK2_LON"]])
                    if distanceToFS <= 100 and distanceToLS > distanceBetweenFS_LS:
                        sc30_notGPS.loc[index,"AssignedStopID"] = "en-route_b_"+str(int(splitedSegtID[3])-1)+"_"+splitedSegtID[3]
                        sc_between_segment.loc[index,"AssignedStopID"] = "en-route_b_"+str(int(splitedSegtID[3])-1)+"_"+splitedSegtID[3]
                    elif distanceToLS <= 100 and distanceToFS > distanceBetweenFS_LS:
                        sc30_notGPS.loc[index,"AssignedStopID"] = "en-route_a_"+splitedSegtID[4]+"_"+str(int(splitedSegtID[4])+1)
                        sc_between_segment.loc[index,"AssignedStopID"] = "en-route_a_"+splitedSegtID[4]+"_"+str(int(splitedSegtID[4])+1)
                    else:
                        sc30_notGPS.loc[index,"AssignedStopID"] = "en-route_"+splitedSegtID[3]+"_"+splitedSegtID[4]
                        sc_between_segment.loc[index,"AssignedStopID"] = "en-route_"+splitedSegtID[3]+"_"+splitedSegtID[4]
                        
            isFirstRow = False
            sc_segments_w_tripID.loc[i,"#ofPassenger@FS"] = len(indexesForFS)
            sc_segments_w_tripID.loc[i,"#ofPassenger@LS"] = len(indexesForLS)
            sc_segments_w_tripID.loc[i,"#ofPassenger@Route"] = len(indexesForRoute)
            prevIndex = i
            continue
        indexesForFS = []
        indexesForLS = []
        indexesForRoute = []
        for index, row_sc in sc_between_segment.iterrows():
            sc30_notGPS.loc[index,"ShiftID"] = row["ShiftID"]
            sc30_notGPS.loc[index,"tripID"] = row["TripID"]
            if sc_segments_FP.loc[i,"geometry50_FP"].contains(row_sc["geometry"]):
                indexesForFS.append(index)
                sc30_notGPS.loc[index,"AssignedStopID"] = splitedSegtID[3]
                sc_between_segment.loc[index,"AssignedStopID"] = splitedSegtID[3]
            elif sc_segments_LP.loc[i,"geometry50_LP"].contains(row_sc["geometry"]):
                indexesForLS.append(index)
                sc30_notGPS.loc[index,"AssignedStopID"] = splitedSegtID[4]
                sc_between_segment.loc[index,"AssignedStopID"] = splitedSegtID[4]
            else:
                indexesForRoute.append(index)
                distanceToFS = calculateDistance([row_sc["ENLEM"],row_sc["BOYLAM"]],[row["DURAK1_LAT"],row["DURAK1_LON"]])
                distanceToLS = calculateDistance([row_sc["ENLEM"],row_sc["BOYLAM"]],[row["DURAK2_LAT"],row["DURAK2_LON"]])
                distanceBetweenFS_LS = calculateDistance([row["DURAK1_LAT"],row["DURAK1_LON"]],[row["DURAK2_LAT"],row["DURAK2_LON"]])
                if distanceToFS <= 100 and distanceToLS > distanceBetweenFS_LS:
                    sc30_notGPS.loc[index,"AssignedStopID"] = "en-route_b_"+str(int(splitedSegtID[3])-1)+"_"+splitedSegtID[3]
                    sc_between_segment.loc[index,"AssignedStopID"] = "en-route_b_"+str(int(splitedSegtID[3])-1)+"_"+splitedSegtID[3]
                elif distanceToLS <= 100 and distanceToFS > distanceBetweenFS_LS:
                    sc30_notGPS.loc[index,"AssignedStopID"] = "en-route_a_"+splitedSegtID[4]+"_"+str(int(splitedSegtID[4])+1)
                    sc_between_segment.loc[index,"AssignedStopID"] = "en-route_a_"+splitedSegtID[4]+"_"+str(int(splitedSegtID[4])+1)
                else:
                    sc30_notGPS.loc[index,"AssignedStopID"] = "en-route_"+splitedSegtID[3]+"_"+splitedSegtID[4]
                    sc_between_segment.loc[index,"AssignedStopID"] = "en-route_"+splitedSegtID[3]+"_"+splitedSegtID[4]
        sc_segments_w_tripID.loc[i,"#ofPassenger@FS"] = len(indexesForFS)
        sc_segments_w_tripID.loc[i,"#ofPassenger@LS"] = len(indexesForLS)
        sc_segments_w_tripID.loc[i,"#ofPassenger@Route"] = len(indexesForRoute)
        prevIndex = i



# =============================================================================
# for i,group in dff2.groupby("ShiftID"):
#     group = group.sort_values(by=["ST1"])
#     historyF_IND = []
#     historyL_IND = []
#     historyIndex = []
#     directions = []
#     controls = []   #shows changes direction
#     controlIndex = []
#     listIndexes = []
#     for index,row in group.iterrows():
#         listIndexes.append(index)
#     isFirstRow = True
#     isUpdated = False
#     group["Direction"] = 0
#     for index,row in group.iterrows():
#         if isFirstRow:
#             historyF_IND.append(row["F_IND"])
#             historyL_IND.append(row["L_IND"])
#             historyIndex.append([index])
#             isFirstRow = False
#             group.loc[index,"Direction"] = 0
#             directions.append(0)
#             controls.append(0)
#             controlIndex.append(0)
#             continue
#         isUpdated = False
#         for j in range(len(historyF_IND)):
#             if historyF_IND[j] <= row["F_IND"] and historyL_IND[j] +1 >= row["F_IND"]:
#                 historyIndex[j].append(index)
#                 if historyF_IND[j] < row["F_IND"]:
#                     if directions[j] == -1:
#                         controls[j] =-1
#                         controlIndex[j] = index
#                     group.loc[index,"Direction"] = 1
#                     directions[j] = 1
#                 elif historyL_IND[j] < row["L_IND"]:
#                     group.loc[index,"Direction"] = 1
#                     if directions[j] == -1:
#                         controls[j] =-1
#                         controlIndex[j] = index
#                     directions[j] = 1
#                 historyF_IND[j] = row["F_IND"] 
#                 historyL_IND[j] = row["L_IND"]
#                 isUpdated = True
#             elif historyF_IND[j] -1 <= row["L_IND"] and historyL_IND[j]  >= row["L_IND"]:
#                 historyIndex[j].append(index)
#                 if historyL_IND[j] > row["L_IND"]:
#                     if directions[j] == 1:
#                         controls[j] = 1
#                         controlIndex[j] = index
#                     group.loc[index,"Direction"] = -1
#                     directions[j] = -1
#                 elif historyF_IND[j] > row["F_IND"]:
#                     if directions[j] == 1:
#                         controls[j] =1
#                         controlIndex[j] = index
#                     group.loc[index,"Direction"] = -1
#                     directions[j] = -1
#                 historyF_IND[j] = row["F_IND"] 
#                 historyL_IND[j] = row["L_IND"]
#                 isUpdated = True
#         if not isUpdated:
#             historyF_IND.append(row["F_IND"])
#             historyL_IND.append(row["L_IND"])
#             historyIndex.append([index])
#             directions.append(0)
#             controls.append(0)
#             controlIndex.append(0)
#             group.loc[index,"Direction"] = 0
#     
#     for ind in range(len(historyIndex)):
#         if controls[ind] == 0:
#             for jInd in historyIndex[ind]:
#                 group.loc[jInd,"Direction"] = directions[ind]
#         else:
#             firstIndex = historyIndex[ind].index(controlIndex[ind])
#             for jInd in historyIndex[ind][0:firstIndex]:
#                 group.loc[jInd,"Direction"] = controls[ind]
#             for jInd in historyIndex[ind][firstIndex:]:
#                 group.loc[jInd,"Direction"] = directions[ind]
#                
# =============================================================================
