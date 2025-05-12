#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to calculate Obukhov length (Linv) from NetCDF data.
Requires: xarray, numpy
Usage: python obukhov_calculate.py input.nc
"""
import sys
import numpy as np
import xarray as xr
#
ifile=sys.argv[1]
year=ifile.split('_')[-3] #solo funciona para la nomenclatura dada
mon=ifile.split('_')[-2] # ""
# funciones
def qswat(t, p):
    """
    Calculates the specific humidity of saturation (respect to water).
    Args:
        t (np.ndarray): Temperature (K).
        p (np.ndarray): Presión (Pa).
    Returns:
        np.ndarray: qswt: Saturation specific humidity  (kg/kg).
    """
    rkbol = 1.380658e-23
    rnavo = 6.0221367e+23
    r = rnavo * rkbol
    rmd = 28.9644
    rmv = 18.0153
    rd = 1000 * r / rmd  # Dry air constant
    rv = 1000 * r / rmv  # Water vapor constant
    restt = 611.21
    r2es = restt * rd / rv
    r3les = 17.502
    r4les = 32.19
    retv = rv / rd - 1  # Correction for virtual temperature
    rtt = 273.16        # Melting point (0°C)
    foeew = r2es * np.exp((r3les * (t - rtt)) / (t - r4les))
    qs = foeew / p
    zcor = 1 / (1 - retv * qs)
    qswt = qs * zcor
    return qswt
def calculate_obukhov_length(input_nc):
    """
    Calculates the inverse Obukhov length (Linv) and saves the return a dataset.
    Args:
        input_nc (str): Ruta al archivo NetCDF de entrada.
    """
    # Abrir el dataset de entrada
    ds = xr.open_dataset(input_nc)
    # Constantes físicas
    rd = 287.06      # Constante del gas para aire seco (J/kg/K)
    retv = 0.6078    # Factor de corrección de temperatura virtual
    cp = 1004.7      # Calor específico del aire a presión constante (J/kg/K)
    vk = 0.4         # Constante de Von Kármán
    g = 9.81         # Aceleración gravitatoria (m/s²)
    Linvrange = 100. # Rango máximo/minimo para Linv
    # Calcular humedad específica (qs) y temperatura virtual (tv)
    q2 = qswat(ds['d2m'], ds['sp'])  # d2m = Temperatura de rocío a 2m
    tv2 = ds['t2m'] * (1 + retv * q2)  # t2m = Temperatura a 2m
    # Calcular densidad del aire (rho) y velocidad de fricción (ust)
    rho = ds['sp'] / (rd * tv2)  # sp = Presión superficial (Pa)
    tau = np.sqrt(ds['iews']**2 + ds['inss']**2)  # Estrés turbulento
    ust = np.maximum(np.sqrt(tau / rho), 0.001)   # Velocidad de fricción
    # Calcular flujos turbulentos
    wt = -ds['ishf'] / (rho * cp)  # Flujo de calor sensible
    wq = -ds['ie'] / rho            # Flujo de humedad
    wtv = wt + retv * ds['t2m'] * wq  # Flujo de calor virtual
    # Calcular longitud inversa de Obukhov (Linv)
    tvst = -wtv / ust
    Linv = vk * g * tvst / (tv2 * ust**2)
    Linv = np.clip(Linv, -Linvrange, Linvrange)  # Limitar valores extremos
    print(f"Linv - Max: {Linv.max().values:.3e}, Min: {Linv.min().values:.3e}, Mean: {np.abs(Linv).mean().values:.3e}")
    return Linv,ust
# codigo
Ld,u_star=calculate_obukhov_length(ifile)
Ld2=Ld.to_dataset(name='Linv')
u_star2=u_star.to_dataset(name='u_s')
u_star2["u_s"].attrs = {
    "units": "m/s^2",
    "long_name": "Friction velocity",
    "description": "Calculated from Turb. surface stress and Air density",
}
Ld2["Linv"].attrs = {
    "units": "m^-1",
    "long_name": "Inverse Obukhov length",
    "description": "Calculated from t2m, d2m, sp, ie, ishf, iews, inss",
}
xr.merge([Ld2,u_star2]).to_netcdf('../out_nc/Lu_%s_%s_.nc'%(year,mon))
#print('done!')
