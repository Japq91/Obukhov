# Obukhov
Explicación de cómo calcular la longitud de Obukhov (L) utilizando datos del reanálisis ERA5 del ECMWF
```markdown
# Cálculo de la Longitud de Obukhov (L) con datos ERA5

Este documento explica cómo calcular la longitud de Obukhov (L) utilizando datos del reanálisis ERA5 del ECMWF.

## Fórmula de la Longitud de Obukhov

La longitud de Obukhov se calcula como:

```
L = - (u_*³ × T₀) / (κ × g × w'θ'₀)
```

**Donde:**
- `u_*`: Velocidad de fricción [m/s]
- `T₀`: Temperatura superficial del aire [K]
- `κ ≈ 0.4`: Constante de von Kármán
- `g ≈ 9.81 m/s²`: Aceleración gravitacional
- `w'θ'₀`: Flujo de calor sensible en superficie [K·m/s]

## Variables requeridas y disponibilidad en ERA5

| Variable | Disponible en ERA5 | Alternativas/Conversión |
|----------|-------------------|-------------------------|
| `u_*` (velocidad de fricción) | ❌ No | `u_* = κ × u₁₀ / ln(10/z₀)` |
| `T₀` (temperatura superficial) | ❌ No | Usar `2m_temperature` como aproximación |
| `w'θ'₀` (flujo de calor) | ✅ Sí (`surface_sensible_heat_flux`) | Convertir: `[K·m/s] = [W/m²] / (ρ × cₚ)`<br>Donde `ρ ≈ 1.225 kg/m³`, `cₚ ≈ 1005 J/(kg·K)` |
| `z₀` (rugosidad) | ✅ Sí (`surface_roughness`) | - |

## Ejemplo de implementación en Python

```python
import numpy as np

# Datos de entrada (ejemplo ERA5)
u10 = 5.0                # Viento a 10m [m/s] (magnitud)
t2m = 288.0              # Temperatura a 2m [K]
heat_flux = 50.0         # Flujo calor sensible [W/m²]
z0 = 0.01                # Rugosidad superficial [m]

# Constantes físicas
KAPPA = 0.4              # Constante de von Kármán
G = 9.81                 # Gravedad [m/s²]
RHO = 1.225              # Densidad aire [kg/m³]
CP = 1005                # Calor específico [J/(kg·K)]

# 1. Calcular velocidad de fricción (u_*)
u_star = KAPPA * u10 / np.log(10/z0)

# 2. Convertir flujo de calor a [K·m/s]
w_prime_theta = heat_flux / (RHO * CP)

# 3. Calcular longitud de Obukhov (L)
L = - (u_star**3 * t2m) / (KAPPA * G * w_prime_theta)

print(f"Longitud de Obukhov calculada: {L:.1f} m")
```

## Limitaciones importantes

⚠️ **Consideraciones al usar esta aproximación:**
1. La estimación de `u_*` asume condiciones atmosféricas neutras
2. El flujo de calor en ERA5 es valor instantáneo (ideal usar promedios temporales)
3. `2m_temperature` no equivale exactamente a temperatura superficial (`T₀`)
4. Para mayor precisión, el IFS calcula estos parámetros de forma acoplada e iterativa

## Recursos adicionales

- [Documentación técnica IFS Cy49r1](https://www.ecmwf.int/en/elibrary/112024-ifs-documentation-cy49r1-part-iv-physical-processes)
- [Conjuntos de datos ERA5](https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era5)
- [ERA5-Land (incluye más variables de superficie)](https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era5-land)

> **Nota:** Para investigación avanzada, considere solicitar acceso a los parámetros de turbulencia directos mediante el Servicio de Soporte del ECMWF.
``` 

