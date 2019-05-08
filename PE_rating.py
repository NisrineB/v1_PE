#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 16:30:36 2019

@author: nisrinebarkallah
"""

# Import des packages 
import pandas as pd 
import numpy as np 
import math
from sklearn.preprocessing import MinMaxScaler
from keras.models import Model
from keras.layers import Input
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers.merge import concatenate
import os
os.chdir

# Import des datasets 
rating = pd.read_excel("/Users/nisrinebarkallah/Dropbox/Grand Oral_project/Rating_pays.xlsx",error_bad_lines=False)
beta = pd.read_excel("/Users/nisrinebarkallah/Dropbox/Grand Oral_project/betas.xls")
comp_1 = pd.read_excel("/Users/nisrinebarkallah/Dropbox/Grand Oral_project/Export_1.xlsx")
comp_2 = pd.read_excel("/Users/nisrinebarkallah/Dropbox/Grand Oral_project/Export 02_05_2019 18_01 1.xlsx")
comp_3 = pd.read_excel("/Users/nisrinebarkallah/Dropbox/Grand Oral_project/Export 02_05_2019 18_03.xlsx")
comp_4 = pd.read_excel("/Users/nisrinebarkallah/Dropbox/Grand Oral_project/Export 02_05_2019 18_04.xlsx")
comp_5 = pd.read_excel("/Users/nisrinebarkallah/Dropbox/Grand Oral_project/Export 02_05_2019 18_05.xlsx")
comp_6 = pd.read_excel("/Users/nisrinebarkallah/Dropbox/Grand Oral_project/Export 02_05_2019 18_05 1.xlsx")
comp_7 = pd.read_excel("/Users/nisrinebarkallah/Dropbox/Grand Oral_project/Export 02_05_2019 18_07 (1).xlsx")
comp_8 = pd.read_excel("/Users/nisrinebarkallah/Dropbox/Grand Oral_project/Export 02_05_2019 18_07 1.xlsx")

# Création du dataset concaténé 
df = comp_1.append(comp_2)

# Preprocessing
c = df.isnull().sum(axis=0)

df = df.convert_objects(convert_numeric=True)
df.dtypes

df = df.drop(["Branch","Woco", "OwnData", "Listing status", "Code de consolidation"], 
             axis=1)

df = df[np.isfinite(df['Dernière année disp.'])]

for col in ['NACE Rev. 2 Code principal']:
    df[col] = df[col].astype('category')


# Drop observation >50% 

df["nul_value"] = df.isnull().sum(axis=1)
df = df[df.nul_value < 9]
df = df.drop(["nul_value"], axis=1)

# Dealing with missing values 
""""
d = {'Capitaux propres\nkUSD Année - 7':1,
     'Capitaux propres\nkUSD Année - 8':2,
     'Capitaux propres\nkUSD Année - 9':3}

df = df.rename(columns=d)

cols = [1,2,3]

df[cols] = df[cols].astype(float).apply(lambda x: x.interpolate(method='index'),
  axis=1).astype(int)
"""" 

# Dealing with missing value : grossier 

df.isnull().sum(axis=0)
colums = list(df.columns)

sales = df.iloc[:,7:17]
ebit = df.iloc[:,17:27]
net_income = df.iloc[:,27:37]
ROE = df.iloc[:,37:47]
ROIC = df.iloc[:,47:57]
ROA = df.iloc[:,57:67]
Eq = df.iloc[:,67:77]

"""
=> loop for interpolation 
sales.isnull().sum(axis=0)   
for i in sales.columns:
    sales[i]=sales[i].interpolate(method='linear',limit_direction='backward', 
         axis=1)
""" 
sales.fillna(sales.mean(), inplace=True)
ebit.fillna(ebit.mean(), inplace=True)
net_income.fillna(net_income.mean(), inplace=True)
ROE.fillna(ROE.mean(), inplace=True)
ROIC.fillna(ROIC.mean(), inplace=True)
ROA.fillna(ROA.mean(), inplace=True)
Eq.fillna(Eq.mean(), inplace=True)


data = pd.concat([df.iloc[:,0:7],sales,ebit, net_income, ROE, ROIC, ROA, Eq], 
                 axis=1 )


# Statistiques descriptives : étude du data set 
correlation_matrix = data.corr()
descr = data.describe()
ecart_interquartile= descr.loc["75%",:]- descr.loc["25%",:]

lim_inf = descr.loc['25%',:]-1.5*ecart_interquartile

lim_sup= descr.loc["75%",:]+1.5*ecart_interquartile

descr.loc["lim_inf", : ]=lim_inf
descr.loc["lim_sup", : ]=lim_sup

# Normalize dataset 

scaler = MinMaxScaler(feature_range=(0, 1))
data = scaler.fit_transform(data.iloc[:,7:77])

# Modèle : CNN




























