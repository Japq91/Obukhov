import cdsapi
import calendar
import sys
# === Validación de argumentos ===
if len(sys.argv) != 3:
    print("Usage: python era5_download.py <year> <month>")
    print("Example: python era5_download.py 2023 02")
    sys.exit(1)
year = sys.argv[1]
month = sys.argv[2].zfill(2)  # Asegura formato "02" si ingresan solo "2"
# === Cálculo de días del mes (considera año bisiesto automáticamente) ===
num_days = calendar.monthrange(int(year), int(month))[1]
days = [f"{day:02d}" for day in range(1, num_days + 1)]
#'''
# === CDS API Request ===
dataset = "reanalysis-era5-single-levels"
request = {
    "product_type": "reanalysis",
    "variable": [
        'instantaneous_eastward_turbulent_surface_stress',
        'instantaneous_moisture_flux',
        'instantaneous_northward_turbulent_surface_stress',
        'instantaneous_surface_sensible_heat_flux',
        'standard_deviation_of_filtered_subgrid_orography',
        'surface_pressure',
        '2m_dewpoint_temperature',
        '2m_temperature',
        #'forecast_surface_reughness',
        ],
    "year": year,
    "month": month,
    "day": days,
    "time": [f"{h:02d}:00" for h in range(24)],
    "data_format": "netcdf",
    "download_format": "unarchived",
    "area": [-20.64, -41.87, -22.64, -39.87]  # N, W, S, E
}
#'''
# === Nombre dinámico del archivo de salida ===
output_filename = f"datos/era5_{year}_{month}_inst.nc"
print(output_filename)
print(days)
# === Envío de la solicitud ===
client = cdsapi.Client()
client.retrieve(dataset, request, output_filename)
