"""
Calcula E_unit (erosao local por pixel) para cada um dos 17 eventos,
seguindo Hao et al. (2022), Eq. (1):

    E_unit = 11,8 * (Q * pr * Area_unit)^0,56 * K * C * P * LS

Q e pr em suas unidades locais (Q em mm, pr em m3/s, Area_unit em m2);
K, C, LS ja preparados como rasters (Dados Iniciais/K_raster.tif,
LS_raster.tif, C_raster.tif); P=1,0 constante (sem areas de preservacao
ativa na bacia, conforme a IC).
"""

import os
import numpy as np
from osgeo import gdal

gdal.UseExceptions()

BASE = r"C:\TCC"
PASTA_DADOS = os.path.join(BASE, "Dados Iniciais")

P_CONST = 1.0


def carrega(caminho):
    ds = gdal.Open(caminho)
    band = ds.GetRasterBand(1)
    nodata = band.GetNoDataValue()
    arr = band.ReadAsArray().astype(np.float64)
    gt = ds.GetGeoTransform()
    proj = ds.GetProjection()
    return arr, nodata, gt, proj, ds.RasterXSize, ds.RasterYSize


K, K_nodata, gt, proj, xsize, ysize = carrega(os.path.join(PASTA_DADOS, "K_raster.tif"))
LS, LS_nodata, _, _, _, _ = carrega(os.path.join(PASTA_DADOS, "LS_raster.tif"))
C, C_nodata, _, _, _, _ = carrega(os.path.join(PASTA_DADOS, "C_raster.tif"))

pixel_w = abs(gt[1])
pixel_h = abs(gt[5])
area_pixel_m2 = pixel_w * pixel_h

driver = gdal.GetDriverByName("GTiff")

resumo = []

for numero_evento in range(1, 18):
    PASTA_EVENTO = os.path.join(BASE, f"Evento {numero_evento}")

    Q, Q_nodata, _, _, _, _ = carrega(os.path.join(PASTA_EVENTO, f"Q{numero_evento}_CN1.tif"))
    pr, pr_nodata, _, _, _, _ = carrega(os.path.join(PASTA_EVENTO, f"pr{numero_evento}.tif"))

    valido = (
        (Q != Q_nodata) & np.isfinite(Q) &
        (pr != pr_nodata) & np.isfinite(pr) &
        (K != K_nodata) & np.isfinite(K) &
        (LS != LS_nodata) & np.isfinite(LS) &
        (C != C_nodata) & np.isfinite(C)
    )

    E_unit = np.full((ysize, xsize), -9999, dtype=np.float32)
    base = np.zeros((ysize, xsize), dtype=np.float64)
    base[valido] = np.maximum(Q[valido] * pr[valido] * area_pixel_m2, 0.0)

    e_valido = 11.8 * (base[valido] ** 0.56) * K[valido] * C[valido] * P_CONST * LS[valido]
    E_unit[valido] = e_valido.astype(np.float32)

    caminho_saida = os.path.join(PASTA_EVENTO, f"E_unit{numero_evento}.tif")
    out = driver.Create(caminho_saida, xsize, ysize, 1, gdal.GDT_Float32)
    out.SetGeoTransform(gt)
    out.SetProjection(proj)
    band_out = out.GetRasterBand(1)
    band_out.WriteArray(E_unit)
    band_out.SetNoDataValue(-9999)
    band_out.FlushCache()
    out = None

    soma_E = float(np.sum(e_valido))
    resumo.append((numero_evento, soma_E))
    print(f"Evento {numero_evento}: E_unit salvo em {caminho_saida} "
          f"(soma = {soma_E:,.2f} t, pixels validos = {valido.sum()})")

print("\n=== RESUMO ===")
print(f"{'Evento':>8} | {'Soma E_unit (t)':>18}")
for ev, soma in resumo:
    print(f"{ev:>8} | {soma:>18,.2f}")
