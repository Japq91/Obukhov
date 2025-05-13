#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script calculates the number of events for stable or unstable conditions according to the Obukhov length (Linv).
Requires: xarray, numpy, pandas
Usage: python p02_save_events.py input.nc
"""
import sys
import numpy as np
import xarray as xr
import pandas as pd
#
LAT_PONTO = -21.6389#-0.25
LON_PONTO = -40.8693#+0.25
#
ifile=sys.argv[1]
year=ifile.split('_')[-3] #solo funciona para la nomenclatura dada
mon=ifile.split('_')[-2] # ""
# funciones
# Clasificar en categorías
def classify_linv(value):
    if value < -0.01: return 'unstable'
    elif value > 0.01: return 'stable'
    else: return 'neutral'
# codigo
d0=xr.open_dataset(ifile)
d1=d0['Linv'].sel(latitude=LAT_PONTO,longitude=LON_PONTO,method='nearest')
df=d1.to_dataframe().reset_index().copy()
#
all_hours = pd.Index(np.arange(0, 24), name='hour')
all_months = df['valid_time'].dt.to_period('M').astype(str).unique()
all_index = pd.MultiIndex.from_product([all_months, all_hours], names=['year_month', 'hour'])
#
df['category'] = df['Linv'].apply(classify_linv)
df['hour'] = df['valid_time'].dt.hour
df['year_month'] = df['valid_time'].dt.to_period('M').astype(str)
# Contar eventos por hora y categoría
summary = {}
for cat in ['unstable', 'stable', 'neutral']:
    s = (
        df[df['category'] == cat]
        .groupby(['year_month', 'hour'])
        .size()
        .reindex(all_index, fill_value=0)
        .unstack()
    )
    summary[cat] = s
# DataFrames individuales
summary['unstable'].to_csv('../out_csv/unstable_%s%s.csv'%(year,mon),index=True)
summary['stable'].to_csv('../out_csv/stable_%s%s.csv'%(year,mon),index=True)
summary['neutral'].to_csv('../out_csv/neutral_%s%s.csv'%(year,mon),index=True)
#print('done!')

