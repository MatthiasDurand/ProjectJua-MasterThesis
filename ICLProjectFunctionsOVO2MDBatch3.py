#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 07:38:52 2020

@author: MatthiasDurand
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import time
import datetime
from datetime import datetime
import calendar
import os
from glob import glob

#All the functions are explained in the file Juan Process Functions Explanations MDV1
def Timestamp_as_Index(df):
    df = pd.DataFrame(data=df)
    return(df.set_index(pd.to_datetime(df['Timestamp']))) 
def Hourly_Mean(df):
    df = (df.set_index(pd.to_datetime(df['Timestamp'])))
    return(df.resample('1H').mean())
def Number_of_Hours(df):
    return(df.count()['Supply Voltage'])
def Number_of_Months(df):
    return(df.resample('1m').mean().count()['Supply Voltage'])
def Percentage_Missing_Data(df):
    return((100*(len(df) - df.count())/len(df)))
def Monthly_Missing_Data(df):
    number_of_data = (df.resample('1m').count()['Supply Voltage'])
    for i in range (len(number_of_data)):
        number_of_data[i] =  100 - 100*number_of_data[i]/(calendar.monthrange(number_of_data.index[i].year,number_of_data.index[i].month)[1]*24)
    return(number_of_data)
def Weekly_Profile(df):#Creation of an hourly mean of the dataset, with all the data available
    return(df.groupby(df.index.weekday).mean())
def Daily_Profile(df):#Creation of an hourly mean of the dataset, with all the data available
    return(df.groupby(df.index.hour).mean())
def Total_Power_Consumption(df):  #SUM(i*V) and not SUM(I)*SUM(V) #CORRECTION ON THE FORMULAS:
    return((df['Supply Voltage']*df['Supply Current']).sum())
def Total_Power_Production(df):
    return((df['Panel Voltage']*df['Panel Current']).sum())
def Total_Power_Utilization(df):
    return(100*Total_Power_Consumption(df)/Total_Power_Production(df))
def Daily_Power_Utilization(df):
    Daily_df = df.resample('1d').mean()
    return(100*(Daily_df['Supply Voltage']*Daily_df['Supply Current'])/(Daily_df['Panel Voltage']*Daily_df['Panel Current']))
def Weekly_Power_Utilization(df):
    Daily_df = df.resample('1w').mean()
    return(100*(Daily_df['Supply Voltage']*Daily_df['Supply Current'])/(Daily_df['Panel Voltage']*Daily_df['Panel Current']))
def Daily_Mean(df):
    return(df.resample('1d').mean())
def Weekly_Mean(df):
    return(df.resample('1w').mean())
def Monthly_Mean(df):
    return(df.resample('1m').mean())
def Timescale_Reduction(df):
    Mdf = Monthly_Missing_Data(df)
    Code_Mdf = Mdf.index.map(lambda x: 100*x.year + x.month)
    df_Clean = df
    for i in range (len(Mdf)):
        if Mdf[i] > 95:
            df_Clean = df_Clean[df_Clean.index.map(lambda x: 100*x.year + x.month) != Code_Mdf[i]]
    return (df_Clean)
def Daily_Mean_Power(df): #The unit will be Wh/day / Correction sum(u*i) != sum(u)*sum(i) done
    return((Daily_Profile(df)['Supply Voltage']*Daily_Profile(df)['Supply Current']).sum(),(Daily_Profile(df)['Panel Voltage']*Daily_Profile(df)['Panel Current']).sum())


def plot_power_production(df):
    plt.xlabel("Date")
    plt.ylabel("Power Production")
    plt.plot(df['Panel Voltage']*df['Panel Current'])   
def plot_power_consumption(df):
    plt.xlabel("Date")
    plt.ylabel("Power Consumption")
    plt.plot(df['Supply Voltage']*df['Supply Current'])
def plot_power_production_and_consumption(df):
    plt.subplot(2, 1, 1)
    plt.xlabel("Date")
    plt.ylabel("Power Consumption")
    plt.plot(df['Supply Voltage']*df['Supply Current'])
    plt.subplot(2, 1, 2)
    plt.xlabel("Date")
    plt.ylabel("Power Production")
    plt.plot(df['Panel Voltage']*df['Panel Current'])
    
#Exportation of the data from the file Sarah sent to me:
PATH = '/Users/MatthiasDurand/Desktop/Imperial College/Master Thesis Project/Exported Data/OVO2 DATA BATCH 3'
def Exportation(PATH):
    EXT = '*.csv'
    Files_Names = []
    for dossier, sous_dossiers, fichiers in os.walk(PATH):
        PATH1 = dossier
        all_csv_files = [file for path, subdir, files in os.walk(PATH1)for file in glob(os.path.join(path, EXT))]
        Files_Names.append(all_csv_files)
    #Files_Names gives the name of every files in every sub_folders

    n = len(Files_Names[0])
    RESULT_All = []
    for i in range (n):
        fichier = Files_Names[0][i]
        dataset = pd.read_csv(fichier)
        RESULT_All.append([dataset])
    #How to remove the colums that are in an different format that I don't understand: 
    #The names of the columns are compared to 'compare2' and 'compare3' which are two kinds of shape
    #Compare2 can be modified and used while compare3 have to be removed
    
    compare2 = ['id', 'device', 'imei', 'supply_voltage', 'supply_current','battery_voltage', 'panel_voltage', 'panel_current', 'temp_room','temp_battery', 'time_stamp']
    compare3 = ['No.', 'IMEI', 'Inverter Voltage', 'Inverter Current','Battery Voltage', 'Panel Voltage', 'Panel Current', 'Timestamp']
    List_to_Remove = []
    List_to_Modify = []
    for i in range (len(RESULT_All)):
        for j in range (len(RESULT_All[i])):
            if (len(RESULT_All[i][j].columns)==8):
                if ((RESULT_All[i][j].columns == compare3).all()):
                    List_to_Remove.append((i,j))
            if (len(RESULT_All[i][j].columns)==11):
                if ((RESULT_All[i][j].columns == compare2).all()):
                    List_to_Modify.append((i,j))
        
    for k in range (len(List_to_Modify)):
        (i,j) = List_to_Modify[k]  #[len(List_to_Remove) - k - 1]
        RESULT_All[i][j] = RESULT_All[i][j].rename(columns = {'supply_voltage' : 'Supply Voltage', 'supply_current':'Supply Current',
           'battery_voltage':'Battery Voltage', 'panel_voltage':'Panel Voltage', 'panel_current':'Panel Current', 'temp_room':'Room Temperature',
           'temp_battery':'Battery Temperature', 'time_stamp':'Timestamp'})
        RESULT_All[i][j].drop(['id', 'device', 'imei'], axis = 1, inplace = True)
    for k in range (len(List_to_Remove)):
        (i,j) = List_to_Remove[len(List_to_Remove) - k - 1]
        del RESULT_All[i][j]
    #This little code allows to delete all the non-numeric parameters in the input data! 
    for j in range (len(RESULT_All)):
        for i in range (len(RESULT_All[j])):
            
            df=RESULT_All[j][i]
            L=[]
            for c in df.columns[0:7]:
                L.append(pd.to_numeric(df[c],errors='coerce',downcast=None))
            #L.append(df['Timestamp'])
            l=np.array(L)
            l=l.transpose()
            RESULT_All[j][i]=pd.DataFrame(data=l, columns=df.columns[0:7],dtype=float)
            RESULT_All[j][i]['Timestamp'] = df['Timestamp']

    RESULT_Concat = []
    for i in range (len(RESULT_All)):
        df = RESULT_All[i][0]
        df = Timestamp_as_Index(df)
        df= Hourly_Mean(df)
        RESULT_Concat.append(df)
        RESULT_All[i][0] = df
    #    L = []
    #    for j in range (len(RESULT_All[i])):
    #        RESULT_All[i][j] = Timestamp_as_Index(RESULT_All[i][j])
    #        RESULT_All[i][j] = Hourly_Mean(RESULT_All[i][j])
    #        L.append(RESULT_All[i][j])
    #    RESULT_Concat.append(pd.concat(L))
    #RESULT_Concat = RESULT_All
    
    NAMING = []
    for dossier, sous_dossiers, fichiers in os.walk(PATH):
        NAMING.append(fichiers)
    NAMING = NAMING[0]
    NAMING = NAMING[1:len(NAMING)]
    #NAMING = NAMING[1:len(NAMING)] useful only for Batch 1, for unknown reasons
    for i in range (len(NAMING)):
        NAMING[i] = NAMING[i][0:len(NAMING[i])-4]
    
    return(RESULT_All,RESULT_Concat,NAMING)


RESULT_All,RESULT_Concat,NAMING = Exportation(PATH)


