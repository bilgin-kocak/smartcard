# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 09:52:42 2020

@author: kocak
"""

#sc30_sel_segment1 = scutils.getDirections(sc30_sel_segment1)

#%%
path = "C:/Users/kocak/OneDrive/Masaüstü/reag/"
sc30 = pd.read_csv(path+"sc30oct.csv")
total = 0
totalNan = 0
hatlar = [10,11,20,310,311,312,350,400,410,420,440,442,443,444,447,448,450,460]
hatlar = [443]
tot = []
nandata = []
for day in range(30):
    for i in hatlar:
        lid = str(i)[0:-1]
        slid = str(i)[-1]
        sc30_selected = pd.read_csv(path+"SmartCardResults/ULID"+lid+slid+"_"+str(day+1)+"oct.csv")
        tot.append(sc30_selected.shape[0])
        total +=  sc30_selected.shape[0]
        sc_sel = sc30_selected[sc30_selected['Stat']==0]
        nandata.append(sc_sel.shape[0])
        totalNan += sc_sel.shape[0] 
 #%%
fig, ax = plt.subplots()
rects1 = ax.bar(range(29), tot, label='Men')
rects2 = ax.bar(range(29), totalNan, label='Women')
