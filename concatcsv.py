#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 16:29:41 2019

@author: ulkem
"""

import pandas as pd

# In[]
nisan = pd.DataFrame(columns = ["sequence_id","packet_id","arac_no","tarih_saat","uydu_sayisi","enlem","boylam","heading","hiz","hat_no","surucu_no","insert_tarihi"])


for i in range(30,31):
    path = "/home/ulkem/Desktop/hediyeHoca/Nisan2019/navigation201904"
    if i<10:
        path = path + "0" + str(i) + ".csv"
    else:
        path = path + str(i) + ".csv"
    day = pd.read_csv(path,delimiter = ";",header = None)
    day.columns = ["sequence_id","packet_id","arac_no","tarih_saat","uydu_sayisi","enlem","boylam","heading","hiz","hat_no","surucu_no","insert_tarihi"] 
    nisan = nisan.append(day)


nisan.to_csv("/home/ulkem/Desktop/hediyeHoca/Nisan2019/nisan.csv",mode='a', header=False)