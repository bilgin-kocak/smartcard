#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 15:31:42 2019

@author: ulkem
"""

import pandas as pd
shifts = pd.read_csv("Concated_Nov19_publicTransportation_withStartandEndTime.csv")
shifts["Start_Time"] = pd.to_datetime(shifts["Start_Time"])
shifts_grouped = shifts.groupby(["LID","SLID","VID","DID"])
lst = []
count = 0
for i,g in shifts_grouped:
    g_sorted = g.sort_values(by = ["Start_Time"])
    d = {}
    new_group = 1
    isFirst = 1
    for j,row in g_sorted.iterrows():
        if isFirst == 0 and new_group == 1 and len(d) ==6:
            lst.append(d)
            d = {}
        isFirst = 0
        new_group = 0
        if row["Status"] == "Start w/o passenger":
            if len(d) == 6:
                lst.append(d)
                d = {}
            d["LID"] = row["LID"]
            d["SLID"] = row["SLID"]
            d["VID"] = row["VID"]
            d["DID"] = row["DID"]
            d["Start_Time"] = row["Start_Time"]
        else:
            d["End_Time"] = row["End_Time"]
            if row["Status"] =="No pass":
                lst.append(d)
                d = {}

new_df = pd.DataFrame(lst)
new_df.to_csv("shifts_nov19.csv")