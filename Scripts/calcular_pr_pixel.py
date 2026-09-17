"""
Calcula pr_pixel (vazao de pico local, por pixel) para cada um dos 17
eventos, seguindo a formulacao de Hao et al. (2022):

    pr_pixel (m3/s) = [Q_pixel(mm)/1000 * Area_pixel(m2)] * (RI/R_evento) / 3600

Onde RI e a intensidade maxima de chuva do evento (mm/h) e R_evento e a
lamina total do evento (mm) - ambos escalares, iguais para todos os
pixels do mesmo evento. Usa RI = Intensidade_60min_mm/h e
R_evento = Chuva_evento_mm (colunas ja existentes na planilha de
eventos), para manter consistencia com o que ja foi usado nesta sessao.

Reaproveita o raster Q{n}_CN1.tif (CN-1, lambda=0.05, ja calibrado) de
cada pasta Evento {n}.
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

for numero_evento in range(1, 18):
    ev_index = 0 if numero_evento == 1 else numero_evento
    row = df_eventos.iloc[ev_index]

    RI = row["Intensidade_60min_mm/h"]
    R_evento = row["Chuva_evento_mm"]
    razao = RI / R_evento

    PASTA_EVENTO = os.path.join(BASE, f"Evento {numero_evento}")
    caminho_q = os.path.join(PASTA_EVENTO, f"Q{numero_evento}_CN1.tif")

    q_ds = gdal.Open(caminho_q)
    gt = q_ds.GetGeoTransform()
    proj = q_ds.GetProjection()
    band = q_ds.GetRasterBand(1)
    nodata = band.GetNoDataValue()
    Q = band.ReadAsArray().astype(np.float64)

    pixel_w = abs(gt[1])
    pixel_h = abs(gt[5])
    area_pixel_m2 = pixel_w * pixel_h

    valido = (Q != nodata) & np.isfinite(Q)

    pr = np.full(Q.shape, -9999, dtype=np.float32)
    pr_valido = (Q[valido] / 1000.0 * area_pixel_m2) * razao / 3600.0
    pr[valido] = pr_valido.astype(np.float32)

    caminho_saida = os.path.join(PASTA_EVENTO, f"pr{numero_evento}.tif")
    driver = gdal.GetDriverByName("GTiff")
    out = driver.Create(caminho_saida, q_ds.RasterXSize, q_ds.RasterYSize, 1, gdal.GDT_Float32)
    out.SetGeoTransform(gt)
    out.SetProjection(proj)
    band_out = out.GetRasterBand(1)
    band_out.WriteArray(pr)
    band_out.SetNoDataValue(-9999)
    band_out.FlushCache()
    out = None
    q_ds = None

    soma_pr = float(np.sum(pr_valido))
    max_pr = float(np.max(pr_valido)) if pr_valido.size else float("nan")

    print(f"Evento {numero_evento}: RI={RI:.2f} mm/h, R_evento={R_evento:.2f} mm, "
          f"razao={razao:.5f} /h -> pr salvo em {caminho_saida} "
          f"(soma={soma_pr:,.4f} m3/s, max_pixel={max_pr:.6f} m3/s)")

print("\nConcluido.")
