# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 23:35:32 2019

@author: kocak
"""
dff2 = scutils.getDirections(dff2)
# Sadece artanları al daha sonra 2 tane olması gerekir history vairable ile değil geleceği araştır.
import pandas as pd
#dfff = pd.read_csv("C:/Users/kocak/OneDrive/Masaüstü/reag/Oct30_publicTransportation_withStartandEndTime.csv")
# =============================================================================
# for i,group in dff2.groupby("ShiftID"):
#     group = group.sort_values(by=["F_TS","ST1"])
#     group["Direction"] = 0
#     historyIndex = []
#     direction = 0
#     for index,row in group.iterrows():
#         if group.loc[index,"Direction"] != 0:
#             continue
#         listIndexes = []
#         for index1,row1 in group[group["Direction"]==0].iterrows():
#             listIndexes.append(index1)
#         listForSearch = listIndexes[listIndexes.index(index):]
#         f_IND = row["F_IND"]
#         l_IND = row["L_IND"]
#         control = 0
#         st1 = row["ST1"]
#         for j in listForSearch:
#             if f_IND <= group.loc[j,"F_IND"] and l_IND +1 >= group.loc[j,"F_IND"]:
#                 historyIndex.append(j)
#                 if f_IND < group.loc[j,"F_IND"]:
#                     #group.loc[index,"Direction"] = 1
#                     if st1 > group.loc[j,"ST1"]:
#                         control = -1
#                     direction = 1
#                 elif l_IND < group.loc[j,"L_IND"]:
#                     #group.loc[index,"Direction"] = 1
#                     if st1 > group.loc[j,"ST1"]:
#                         control = -1
#                     direction = 1
#                 f_IND = group.loc[j,"F_IND"]
#                 l_IND = group.loc[j,"L_IND"]
#                 st1 = group.loc[j,"ST1"]
#         if direction == 1 and control == 0:
#             group.loc[historyIndex,"Direction"] = 1
#             direction = 0
# =============================================================================


# Find direction of sc segment based data
 
for i,group in dff2.groupby("ShiftID"):
    group = group.sort_values(by=["ST1"])
    group["Direction"] = -1
    historyIndex = []
    direction = 0
    for index,row in group.iterrows():
        if group.loc[index,"Direction"] != -1:
            continue
        listIndexes = []
        for index1,row1 in group[group["Direction"]==-1].iterrows():
            listIndexes.append(index1)
        listForSearch = listIndexes[listIndexes.index(index):]
        F_IND = row["F_IND"]
        L_IND = row["L_IND"]
        st1 = row["ST1"]
        for j in listForSearch:
            if F_IND <= group.loc[j,"F_IND"] and L_IND +1 >= group.loc[j,"F_IND"]:
                historyIndex.append(j)
                if F_IND < group.loc[j,"F_IND"]:
                    #group.loc[index,"Direction"] = 1
                    direction = 1
                elif L_IND < group.loc[j,"L_IND"]:
                    #group.loc[index,"Direction"] = 1
                    direction = 1
                F_IND = group.loc[j,"F_IND"]
                L_IND = group.loc[j,"L_IND"]
                st1 = group.loc[j,"ST1"]
            elif L_IND >= group.loc[j,"L_IND"] and F_IND -1 <= group.loc[j,"L_IND"]:
                if direction != 1 : historyIndex = []
                break
        if direction == 1:
            group.loc[historyIndex,"Direction"] = 1
            historyIndex = []
            direction = 0        
            
            
# =============================================================================
# for i,group in dff2.groupby("ShiftID"):
#     group = group.sort_values(by=["ST1"])
#     group["Direction"] = -1
#     historyIndex = []
#     direction = 0
#     for index,row in group.iterrows():
#         if group.loc[index,"Direction"] != -1:
#             continue
#         listIndexes = []
#         for index1,row1 in group[group["Direction"]==-1].iterrows():
#             listIndexes.append(index1)
#         listForSearch = listIndexes[listIndexes.index(index):]
#         F_IND = row["F_IND"]
#         L_IND = row["L_IND"]
#         st1 = row["ST1"]
#         for j in listForSearch:
#             if F_IND <= group.loc[j,"F_IND"] and L_IND +1 >= group.loc[j,"F_IND"] and group.loc[j,"ST1"] - st1 <= 1:
#                 historyIndex.append(j)
#                 if F_IND < group.loc[j,"F_IND"]:
#                     #group.loc[index,"Direction"] = 1
#                     direction = 1
#                 elif L_IND < group.loc[j,"L_IND"]:
#                     #group.loc[index,"Direction"] = 1
#                     direction = 1
#                 F_IND = group.loc[j,"F_IND"]
#                 L_IND = group.loc[j,"L_IND"]
#                 st1 = group.loc[j,"ST1"]
#         if direction == 1:
#             group.loc[historyIndex,"Direction"] = 1
#             direction = 0        
# 
# =============================================================================

               

