"""
Gera os mapas finais de producao de sedimentos (SY) por pixel/evento.

Decisao de 17/09/2026: apos duas tentativas de corrigir a formulacao
FCI/DSC (Hao et al., 2022) nao superarem uma simples escala linear
constante de E_unit (ver Notas Claude/notas_musle_espacializada.md,
secao 7/9, e README.md), o usuario decidiu adotar esse baseline como
resultado final da Fase 2 - achado consistente com a literatura (ex.:
Baert et al., 2026, mostra tetos de precisao baixos para MUSLE
espacializada mesmo com dados observados perfeitos).

SY_sim,k = c * E_unit,k (regressao por minimos quadrados atraves da
origem, c calibrado contra os 17 valores de SY_obs = coluna SYY_t).

Gera:
- Evento {n}/SY{n}.tif: mapa de producao de sedimentos por pixel, por
  evento (toneladas/pixel).
- Dados Iniciais/SY_medio_eventos.tif: media dos 17 mapas - padrao
  espacial tipico de "hot spots" erosivos, independente do evento
  especifico (principal mapa de resultado do TCC).
"""

import os
import numpy as np
import pandas as pd
from osgeo import gdal

gdal.UseExceptions()

BASE = r"C:\TCC"
PASTA_DADOS = os.path.join(BASE, "Dados Iniciais")

df_eventos = pd.read_excel(
    os.path.join(PASTA_DADOS, "eventos_processados_manuais.xlsx"), sheet_name="Sheet1"
)


def ev_index(n):
    return 0 if n == 1 else n


SY_obs = np.array([df_eventos.iloc[ev_index(n)]["SYY_t"] for n in range(1, 18)], dtype=float)


def le_raster(caminho):
    ds = gdal.Open(caminho)
    band = ds.GetRasterBand(1)
    nodata = band.GetNoDataValue()
    arr = band.ReadAsArray().astype(np.float64)
    arr = np.where((arr != nodata) & np.isfinite(arr), arr, np.nan)
    gt = ds.GetGeoTransform()
    proj = ds.GetProjection()
    return arr, gt, proj, nodata


driver = gdal.GetDriverByName("GTiff")


def salva_raster(caminho, arr, gt, proj, nodata=-9999):
    nrows, ncols = arr.shape
    saida = np.where(np.isfinite(arr), arr, nodata).astype(np.float32)
    out = driver.Create(caminho, ncols, nrows, 1, gdal.GDT_Float32)
    out.SetGeoTransform(gt)
    out.SetProjection(proj)
    band_out = out.GetRasterBand(1)
    band_out.WriteArray(saida)
    band_out.SetNoDataValue(nodata)
    band_out.FlushCache()


# ============================================================
# 1. Calibra c (escala constante, minimos quadrados pela origem)
# ============================================================

Eunit_soma = np.empty(17)
Eunit_rasters = []
ref_gt = ref_proj = None

for n in range(1, 18):
    caminho = os.path.join(BASE, f"Evento {n}", f"E_unit{n}.tif")
    arr, gt, proj, nodata = le_raster(caminho)
    Eunit_rasters.append(arr)
    Eunit_soma[n - 1] = np.nansum(arr)
    if ref_gt is None:
        ref_gt, ref_proj = gt, proj

c_opt = np.sum(Eunit_soma * SY_obs) / np.sum(Eunit_soma**2)
SY_sim = c_opt * Eunit_soma
nse = 1 - np.sum((SY_obs - SY_sim) ** 2) / np.sum((SY_obs - np.mean(SY_obs)) ** 2)

print(f"c calibrado (SY_sim = c * E_unit, minimos quadrados pela origem): {c_opt:.6f}")
print(f"NSE do baseline: {nse:.4f}")
print(f"\n{'Evento':>7} | {'SY_obs(t)':>10} | {'SY_sim(t)':>10} | {'erro%':>8}")
for n in range(1, 18):
    erro = 100 * (SY_sim[n - 1] - SY_obs[n - 1]) / SY_obs[n - 1]
    print(f"{n:>7} | {SY_obs[n-1]:>10.2f} | {SY_sim[n-1]:>10.2f} | {erro:>7.1f}%")

# ============================================================
# 2. Salva SY{n}.tif por evento e o mapa medio (hot spots)
# ============================================================

soma_sy = None
conta_validos = None

for n in range(1, 18):
    sy_pixel = c_opt * Eunit_rasters[n - 1]
    caminho_saida = os.path.join(BASE, f"Evento {n}", f"SY{n}.tif")
    salva_raster(caminho_saida, sy_pixel, ref_gt, ref_proj)

    valido = np.isfinite(sy_pixel)
    if soma_sy is None:
        soma_sy = np.where(valido, sy_pixel, 0.0)
        conta_validos = valido.astype(np.float64)
    else:
        soma_sy += np.where(valido, sy_pixel, 0.0)
        conta_validos += valido.astype(np.float64)

sy_medio = np.where(conta_validos > 0, soma_sy / np.clip(conta_validos, 1, None), np.nan)
caminho_medio = os.path.join(PASTA_DADOS, "SY_medio_eventos.tif")
salva_raster(caminho_medio, sy_medio, ref_gt, ref_proj)

print(f"\nSY{{n}}.tif salvo para os 17 eventos.")
print(f"Mapa medio (hot spots): {caminho_medio}")
print(f"SY medio por pixel: min={np.nanmin(sy_medio):.6g} media={np.nanmean(sy_medio):.6g} "
      f"max={np.nanmax(sy_medio):.6g} t/evento")
print("\nConcluido.")
