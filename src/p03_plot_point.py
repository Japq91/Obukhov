#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import os
from glob import glob as gb

ri='/home/jonathan/PB_tareas/Tarea2/test2/datos'

for yea in range(1990,2024):
    for month in range(12):
        mon='%02d'%(month+1)
        file='%s/era5_%s_%s_inst.nc'%(ri,yea,mon)
        if not os.path.exists(file): continue        
        file1='../out_nc/Lu_%s_%s_.nc'%(yea,mon)
        if not os.path.exists(file1): 
            print(yea,mon)  
            os.system('python p01_obukhov_calculate.py %s'%file)
        file2='../out_csv/neutral_%s%s.csv'%(yea,mon)
        if not os.path.exists(file2): os.system('python p02_save_events.py %s'%file1)        

# ### count
def plot1(dataframe):
    fig=plt.figure(figsize=(6,3))
    plt.pcolormesh(dataframe,cmap='turbo')
    plt.colorbar(label='[%]')
    plt.ylabel('months')
    plt.xlabel('hours')
    return fig

def p01_merge(files):
    for i,file in enumerate(files):
        df=pd.read_csv(file,index_col='year_month')
        if i==0: df1=df.copy()
        else: df1=pd.concat([df1,df],axis=0)
    df1.index=pd.to_datetime(df1.index)    
    return df1

def p02_porcentaje(df1):
    # Agrupar por número de mes (1 a 12) y calcular el promedio
    df_sum = df1.groupby(df1.index.month).sum()
    df_sum.index.name = 'month'
    df_dias = (df1*0+1).mul(df1.index.days_in_month, axis=0)
    df_dias.index=pd.to_datetime(df_dias.index)
    df_nsum = df_dias.groupby(df_dias.index.month).sum()
    df_nsum.index.name = 'month'
    df0=100*df_sum/df_nsum
    return df0

## save
tipo='stable' #'neutral','stable','unstable'
files=sorted(gb('../out_csv/%s_*'%(tipo)))
dfi=p01_merge(files)
stable=p02_porcentaje(dfi)
fig=plot1(stable)
plt.title(tipo.capitalize())
fig.savefig('../out_fig/%s_35years.png'%tipo, dpi=200, bbox_inches='tight')

tipo='neutral' #'neutral','stable','unstable'
files=sorted(gb('../out_csv/%s_*'%(tipo)))
dfi=p01_merge(files)
neutral=p02_porcentaje(dfi)
fig=plot1(neutral)
plt.title(tipo.capitalize())
fig.savefig('../out_fig/%s_35years.png'%tipo, dpi=200, bbox_inches='tight')

tipo='unstable' #'neutral','stable','unstable'
files=sorted(gb('../out_csv/%s_*'%(tipo)))
dfi=p01_merge(files)
unstable=p02_porcentaje(dfi)
fig=plot1(unstable)
plt.title(tipo.capitalize())
fig.savefig('../out_fig/%s_35years.png'%tipo, dpi=200, bbox_inches='tight')


fig=plot1(stable+unstable+neutral)
plt.title('Suma')
fig.savefig('../out_fig/suma_35years.png', dpi=200, bbox_inches='tight')

