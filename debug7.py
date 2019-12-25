# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 10:21:05 2019

@author: kocak
"""
# Assign the stop ids to raw smart card data

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