# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 20:03:11 2019

@author: Ulkem
"""


import pandas as pd

october = pd.read_csv('C:/Users/kocak/OneDrive/Masaüstü/reag/ekim.csv',delimiter=',')


# In[1]

#Filter 30th October

oct30 = october[(pd.to_datetime(october["tarih_saat"]) >= pd.to_datetime('2018-10-30 02:59:59')) & (pd.to_datetime(october["tarih_saat"]) < pd.to_datetime('2018-10-31 03:00:00')) & (october["enlem"] > 0) & (october["boylam"] > 0)]


#oct30.to_csv("30oct.csv")
#%%
import pandas as pd
oct30 = pd.read_csv("C:/Users/kocak/OneDrive/Masaüstü/reag/oct30.csv")
#%%
oct30_1 = oct30[(oct30["arac_no"]==248)&(oct30["hat_no"]==44)]
#%%

# In[10]
# Open file to write
f = open("C:/Users/kocak/OneDrive/Masaüstü/reag/Oct30_publicTransportation_withStartandEndTime.csv","w")
f.write("LID,VID,DRIVER_ID,Start_Time,End_Time,Event_Type\n")
# In[2]

#Group by vehicle ID
oct30_grouped = oct30.groupby('arac_no')
prev_lid = -1
prev_did = -1
prev_time = ""
event_type =""
count = 0

#For each vehicle ID
for index, group in oct30_grouped:
    
    is_first = 1
    
    #Flag to check if the row is the first row or not
    flag = 0
    
    #Sort values by timestamp
    group = group.sort_values(by = ['tarih_saat'])
    
    # For each line with that vehicle ID
    for index_,row in group.iterrows():
        # If it is first row of that group

        if (flag == 0):
            #Set previous values for the second line of the group
            prev_lid = row['hat_no']
            prev_did = row['surucu_no']
            start = row['tarih_saat']
            count = 1
            flag = 1
        else:
            end = prev_time
            #If everything is the same, then save previous row and continue
            if (prev_lid == row['hat_no'] and prev_did == row['surucu_no']):
                prev_time = row['tarih_saat']  
                count = count + 1
                continue
            
            elif count == 1:
                end = start
                toBeWritten = str(prev_lid) + "," + str(row['arac_no']) + "," + str(prev_did) + "," + str(start) + "," + str(end) +", " + "----\n"
                f.write(toBeWritten)
                flag = 0
            
            
            #If Line ID is changed
            elif (prev_lid != row['hat_no'] and prev_did == row['surucu_no'] and is_first == 0):
                # Now we should end the previous shift by previous timestamp 
                event_type = "LID changed\n"
                end = prev_time
                toBeWritten = str(prev_lid) + "," + str(row['arac_no']) + "," + str(prev_did) + "," + str(start) + "," + str(end) +", " + event_type
                f.write(toBeWritten)
                #Set the values of the next shift
                prev_lid = row["hat_no"]
                start = row["tarih_saat"]
                prev_did = row["surucu_no"]
                count = 1 
                flag = 0
                
            #If Driver ID is changed
            elif (prev_lid == row['hat_no'] and prev_did != row['surucu_no'] and is_first == 0):
                end = prev_time
                event_type = "DriverID changed\n"
                toBeWritten = str(prev_lid) + "," + str(row['arac_no']) + "," + str(prev_did) + "," + str(start) + "," + str(end) + ", " + event_type
                f.write(toBeWritten)
                #Set the values of the next shift
                prev_lid = row["hat_no"]
                start = row["tarih_saat"]
                prev_did = row["surucu_no"]
                count = 1
                flag = 0
            
            #If both of them changed
            elif (prev_lid != row['hat_no'] and prev_did != row['surucu_no'] and is_first == 0):
                event_type = "LID and DID changed\n"
                end = prev_time
                toBeWritten = str(prev_lid) + "," + str(row['arac_no']) + "," + str(prev_did) + "," + str(start) + "," + str(end) + ", " + event_type
                f.write(toBeWritten)
                #Set the values of the next shift
                prev_lid = row["hat_no"]
                start = row["tarih_saat"]
                prev_did = row["surucu_no"]  
                count = 1 
                flag = 0
                
            elif (is_first == 1):
                end = prev_time
                toBeWritten = str(prev_lid) + "," + str(row['arac_no']) + "," + str(prev_did) + "," + str(start) + "," + str(end) + ", " + "New Vehicle ID\n"
                #print(toBeWritten)
                is_first = 0
                f.write(toBeWritten)
                flag = 0
        
'''
# If data are not proper
elif end <= start:
    flag = 0
    continue
'''
# If it has only one row
# In[]
f.close()
# In[3]
                
#Smart Card
# Read October Smart Card Info
sc = pd.read_csv('C:/Users/kocak/OneDrive/Masaüstü/reag/10-ulasim_veri.csv',delimiter=';')
sc['ENLEM'] = pd.to_numeric(sc['ENLEM'].str.replace(',','.'))
sc['BOYLAM'] = pd.to_numeric(sc['BOYLAM'].str.replace(',','.'))

#Filter 30th October
sc30 = sc[(pd.to_datetime(sc["TIMESTAMP"]) >= pd.to_datetime('2018-10-30 02:59:59')) & (pd.to_datetime(sc["TIMESTAMP"]) < pd.to_datetime('2018-10-31 03:00:00')) & (sc["ENLEM"] > 0) & (sc["BOYLAM"] > 0)]

#Group by vehicle ID
sc30_grouped = sc30.groupby("ARAC_NO")


f = open("C:/Users/kocak/OneDrive/Masaüstü/reag/Oct30_publicTransportation_withStartandEndTime_sc.csv","w")
f.write("LID,VID,SLID,Start_Time,End_Time,Event_Type\n")
#%%
# Read October Smart Card Info
sc = pd.read_csv('C:/Users/kocak/OneDrive/Masaüstü/reag/sc_oct30.csv',delimiter=',')
sc['ENLEM'] = pd.to_numeric(sc['ENLEM'].str.replace(',','.'))
sc['BOYLAM'] = pd.to_numeric(sc['BOYLAM'].str.replace(',','.'))

#Filter 30th October
#sc30 = sc[(pd.to_datetime(sc["TIMESTAMP"]) >= pd.to_datetime('2018-11-19 02:59:59')) & (pd.to_datetime(sc["TIMESTAMP"]) < pd.to_datetime('2018-11-20 03:00:00')) & (sc["ENLEM"] > 0) & (sc["BOYLAM"] > 0)]

#Group by vehicle ID
sc30_grouped = sc30.groupby("ARAC_NO")


f = open("C:/Users/kocak/OneDrive/Masaüstü/reag/Oct30_publicTransportation_withStartandEndTime_sc.csv","w")
f.write("LID,VID,SLID,Start_Time,End_Time,Event_Type\n")
# In[2]


prev_lid = 0
prev_slid = 0
prev_time = ""
event_type =""
count = 0

#For each vehicle ID
for index, group in sc30_grouped:
    
    is_first = 1
    
    #Flag to check if the row is the first row or not
    flag = 0
    
    #Sort values by timestamp
    group = group.sort_values(by = ['TIMESTAMP'])
    
    # For each line with that vehicle ID
    for index_,row in group.iterrows():
        # If it is first row of that group
        if (flag == 0):
            #Set previous values for the second line of the group
            prev_lid = row['HAT_NO']
            prev_slid = row['ALT_HAT_NO']
            start = row['TIMESTAMP']
            count = 1
            flag = 1
        else:
            end = prev_time
            #If everything is the same, then save previous row and continue
            if (prev_lid == row['HAT_NO'] and prev_slid == row['ALT_HAT_NO']):
                prev_time = row['TIMESTAMP']    
                count = count + 1
                continue
            
            
            
            elif count == 1:
                end = start
                toBeWritten = str(prev_lid) + "," + str(row['ARAC_NO']) + "," + str(prev_slid) + "," + str(start) + "," + str(end) +", " + "----\n"
                f.write(toBeWritten)
                flag = 0
            
            
            
            #If Line ID is changed
            elif (prev_lid != row['HAT_NO'] and prev_slid == row['ALT_HAT_NO'] and is_first != 1):
                # Now we should end the previous shift by previous timestamp 
                event_type = "LID changed\n"
                end = prev_time
                toBeWritten = str(prev_lid) + "," + str(row['ARAC_NO']) + "," + str(prev_slid) + "," + str(start) + "," + str(end) +", " + event_type
                f.write(toBeWritten)
                #Set the values of the next shift
                prev_lid = row["HAT_NO"]
                start = row["TIMESTAMP"]
                prev_slid = row["ALT_HAT_NO"]
                count = 1
                
            #If Subline ID is changed
            elif (prev_lid == row['HAT_NO'] and prev_slid != row['ALT_HAT_NO'] and is_first != 1):
                end = prev_time
                event_type = "SLID changed\n"
                toBeWritten = str(prev_lid) + "," + str(row['ARAC_NO']) + "," + str(prev_slid) + "," + str(start) + "," + str(end) + ", " + event_type
                f.write(toBeWritten)
                #Set the values of the next shift
                prev_lid = row["HAT_NO"]
                start = row["TIMESTAMP"]
                prev_did = row["ALT_HAT_NO"]
                count = 1
            
            #If both of them changed
            elif (prev_lid != row['HAT_NO'] and prev_slid != row['ALT_HAT_NO'] and is_first != 1):
                event_type = "LID and SLID changed\n"
                end = prev_time
                toBeWritten = str(prev_lid) + "," + str(row['ARAC_NO']) + "," + str(prev_slid) + "," + str(start) + "," + str(end) + ", " + event_type
                f.write(toBeWritten)
                #Set the values of the next shift
                prev_lid = row["HAT_NO"]
                start = row["TIMESTAMP"]
                prev_did = row["ALT_HAT_NO"]
                count = 1
            elif (is_first == 1):
                end = prev_time
                toBeWritten = str(prev_lid) + "," + str(row['ARAC_NO']) + "," + str(prev_slid) + "," + str(start) + "," + str(end) + ", " + "New Vehicle ID\n"
                #print(toBeWritten)
                is_first = 0
                f.write(toBeWritten)
                flag = 0
f.close()