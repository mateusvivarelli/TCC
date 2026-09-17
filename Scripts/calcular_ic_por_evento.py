"""
Recalcula o Indice de Conectividade (IC) POR EVENTO, usando
W_i = E_unit,i (o peso varia por evento, conforme Hao et al. 2022,
Eq. 6) - substitui a versao placeholder (W=1) de
calcular_indice_conectividade.py.

Para cada evento:
1. Reprojeta/realinha E_unit{n}.tif (grade 884x365) para a grade do
   MDE/flow accumulation (2722x1097).
2. Roda sagang:catchmentarea com VAL_INPUT=E_unit_evento para obter
   W_medio_montante (VAL_MEAN).
3. Calcula Ddn via propagacao vetorizada (mesma logica do script
   placeholder, agora com W variavel por celula).
4. Calcula IC_evento = log10(Dup/Ddn) e salva.
"""

import os
import time
import subprocess
import numpy as np
from osgeo import gdal

gdal.UseExceptions()

BASE = r"C:\TCC"
PASTA_QP = os.path.join(BASE, "Dados Iniciais", "qp_spatial")
QGIS_PROCESS = r"C:\Program Files\QGIS 3.44.14\bin\qgis_process-qgis-ltr.bat"
DEM_FILLED = os.path.join(PASTA_QP, "carvedDEM_corrigido_filled.tif")

OUTLET_X, OUTLET_Y = 318980.7663669552, 7432307.0820886735

# ============================================================
# 1. BASE FIXA: DEM, D8, declividade, area (flow accumulation)
# ============================================================

dem_ds = gdal.Open(DEM_FILLED)
gt = dem_ds.GetGeoTransform()
proj = dem_ds.GetProjection()
dem_band = dem_ds.GetRasterBand(1)
dem_nodata = dem_band.GetNoDataValue()
DEM = dem_band.ReadAsArray().astype(np.float64)
nrows, ncols = DEM.shape
VALIDO = (DEM != dem_nodata) & np.isfinite(DEM)

flowacc_ds = gdal.Open(os.path.join(PASTA_QP, "flowacc_corrigido.tif"))
flowacc_band = flowacc_ds.GetRasterBand(1)
flowacc_nodata = flowacc_band.GetNoDataValue()
A_M2 = flowacc_band.ReadAsArray().astype(np.float64)

slope_ds = gdal.Open(os.path.join(PASTA_QP, "slope_pct.tif"))
SLOPE_MM = slope_ds.GetRasterBand(1).ReadAsArray().astype(np.float64) / 100.0
SLOPE_MM = np.clip(SLOPE_MM, 0.001, None)

pixel_w = abs(gt[1])
pixel_h = abs(gt[5])

VIZINHOS = [
    (-1, -1, (pixel_w**2 + pixel_h**2) ** 0.5), (-1, 0, pixel_h), (-1, 1, (pixel_w**2 + pixel_h**2) ** 0.5),
    (0, -1, pixel_w),                                              (0, 1, pixel_w),
    (1, -1, (pixel_w**2 + pixel_h**2) ** 0.5),  (1, 0, pixel_h),  (1, 1, (pixel_w**2 + pixel_h**2) ** 0.5),
]

downstream_row = np.full((nrows, ncols), -1, dtype=np.int32)
downstream_col = np.full((nrows, ncols), -1, dtype=np.int32)
downstream_dist = np.zeros((nrows, ncols), dtype=np.float64)
melhor_declive = np.full((nrows, ncols), -np.inf, dtype=np.float64)

rows_idx, cols_idx = np.where(VALIDO)
elev_centro = DEM[rows_idx, cols_idx]

for dr, dc, dist in VIZINHOS:
    r_viz = rows_idx + dr
    c_viz = cols_idx + dc
    dentro = (r_viz >= 0) & (r_viz < nrows) & (c_viz >= 0) & (c_viz < ncols)
    elev_viz = np.full(len(rows_idx), np.nan)
    viz_valido = np.zeros(len(rows_idx), dtype=bool)
    idx_dentro = np.where(dentro)[0]
    rr = r_viz[idx_dentro]
    cc = c_viz[idx_dentro]
    viz_valido_local = VALIDO[rr, cc]
    elev_viz[idx_dentro[viz_valido_local]] = DEM[rr[viz_valido_local], cc[viz_valido_local]]
    viz_valido[idx_dentro[viz_valido_local]] = True
    declive = np.where(viz_valido, (elev_centro - elev_viz) / dist, -np.inf)
    melhor_declive_atual = melhor_declive[rows_idx, cols_idx]
    melhora = (declive > melhor_declive_atual) & viz_valido
    idx_melhora = np.where(melhora)[0]
    downstream_row[rows_idx[idx_melhora], cols_idx[idx_melhora]] = rows_idx[idx_melhora] + dr
    downstream_col[rows_idx[idx_melhora], cols_idx[idx_melhora]] = cols_idx[idx_melhora] + dc
    downstream_dist[rows_idx[idx_melhora], cols_idx[idx_melhora]] = dist
    melhor_declive[rows_idx[idx_melhora], cols_idx[idx_melhora]] = declive[idx_melhora]

col_exutorio = int((OUTLET_X - gt[0]) / gt[1])
row_exutorio = int((OUTLET_Y - gt[3]) / gt[5])
print(f"Base fixa pronta. Exutorio: linha={row_exutorio}, col={col_exutorio}")

tem_destino = VALIDO & (downstream_row >= 0) & (downstream_col >= 0)
idx_r, idx_c = np.where(tem_destino)
dest_r = downstream_row[idx_r, idx_c]
dest_c = downstream_col[idx_r, idx_c]


def calcula_ddn(W):
    custo_local = downstream_dist / (np.clip(W, 1e-6, None) * SLOPE_MM)
    Ddn_2d = np.full((nrows, ncols), np.nan, dtype=np.float64)
    Ddn_2d[row_exutorio, col_exutorio] = 0.0
    pendentes = np.ones(len(idx_r), dtype=bool)
    for passo in range(nrows + ncols):
        if not pendentes.any():
            break
        ddn_destino = Ddn_2d[dest_r[pendentes], dest_c[pendentes]]
        prontos_local = np.isfinite(ddn_destino)
        if not prontos_local.any():
            continue
        idx_pend = np.where(pendentes)[0]
        idx_prontos = idx_pend[prontos_local]
        rr = idx_r[idx_prontos]
        cc = idx_c[idx_prontos]
        Ddn_2d[rr, cc] = custo_local[rr, cc] + ddn_destino[prontos_local]
        pendentes[idx_prontos] = False
    return Ddn_2d, pendentes.sum()


def roda_saga_val_mean(val_input_path, saida_path):
    subprocess.run([
        QGIS_PROCESS, "run", "sagang:catchmentarea",
        f"--ELEVATION={DEM_FILLED}",
        "--METHOD=4", "--FLOW_UNIT=1",
        f"--FLOW={PASTA_QP}\\_flowacc_tmp_ic.tif",
        f"--VAL_INPUT={val_input_path}",
        f"--VAL_MEAN={saida_path}",
        f"--ACCU_TARGET={DEM_FILLED}",
    ], capture_output=True, text=True)


driver = gdal.GetDriverByName("GTiff")


def salva_raster(caminho, arr, nodata=-9999):
    saida = np.where(np.isfinite(arr), arr, nodata).astype(np.float32)
    out = driver.Create(caminho, ncols, nrows, 1, gdal.GDT_Float32)
    out.SetGeoTransform(gt)
    out.SetProjection(proj)
    band_out = out.GetRasterBand(1)
    band_out.WriteArray(saida)
    band_out.SetNoDataValue(nodata)
    band_out.FlushCache()
    return None


# ============================================================
# 2. LOOP DOS 17 EVENTOS
# ============================================================

for numero_evento in range(1, 18):
    t0 = time.time()
    PASTA_EVENTO = os.path.join(BASE, f"Evento {numero_evento}")
    caminho_e_unit = os.path.join(PASTA_EVENTO, f"E_unit{numero_evento}.tif")

    # reprojeta E_unit (grade 884x365) para a grade do MDE (2722x1097)
    e_unit_ds = gdal.Open(caminho_e_unit)
    caminho_w = os.path.join(PASTA_EVENTO, f"_W_evento{numero_evento}_tmp.tif")
    gdal.Warp(
        caminho_w, e_unit_ds, format="GTiff",
        width=ncols, height=nrows,
        outputBounds=(gt[0], gt[3] + nrows * gt[5], gt[0] + ncols * gt[1], gt[3]),
        dstSRS=proj, resampleAlg=gdal.GRA_NearestNeighbour, dstNodata=-9999,
    )
    w_ds = gdal.Open(caminho_w)
    w_band = w_ds.GetRasterBand(1)
    w_nodata = w_band.GetNoDataValue()
    W_evento = w_band.ReadAsArray().astype(np.float64)
    W_evento = np.where((W_evento != w_nodata) & np.isfinite(W_evento) & (W_evento > 0), W_evento, 1e-6)
    w_ds = None

    # Dup: W medio e S medio a montante
    caminho_w_mean = os.path.join(PASTA_EVENTO, f"_Wmean_evento{numero_evento}_tmp.tif")
    roda_saga_val_mean(caminho_w, caminho_w_mean)
    wmean_ds = gdal.Open(caminho_w_mean)
    wmean_band = wmean_ds.GetRasterBand(1)
    wmean_nodata = wmean_band.GetNoDataValue()
    W_medio_montante = wmean_band.ReadAsArray().astype(np.float64)
    W_medio_montante = np.where((W_medio_montante != wmean_nodata) & np.isfinite(W_medio_montante),
                                 W_medio_montante, np.nan)
    wmean_ds = None

    slope_mean_ds = gdal.Open(os.path.join(PASTA_QP, "slope_mean_upslope_pct.tif"))
    S_medio_montante = slope_mean_ds.GetRasterBand(1).ReadAsArray().astype(np.float64) / 100.0
    S_medio_montante = np.clip(S_medio_montante, 0.001, None)
    slope_mean_ds = None

    Dup = W_medio_montante * S_medio_montante * np.sqrt(np.where(A_M2 > 0, A_M2, np.nan))

    Ddn_2d, n_pendentes = calcula_ddn(W_evento)

    IC = np.full((nrows, ncols), np.nan, dtype=np.float64)
    valido_ic = VALIDO & np.isfinite(Ddn_2d) & (Ddn_2d > 0) & np.isfinite(Dup) & (Dup > 0)
    IC[valido_ic] = np.log10(Dup[valido_ic] / Ddn_2d[valido_ic])

    caminho_ic = os.path.join(PASTA_EVENTO, f"IC{numero_evento}.tif")
    salva_raster(caminho_ic, IC)

    # limpeza dos temporarios
    for tmp in (caminho_w, caminho_w_mean):
        try:
            os.remove(tmp)
        except OSError:
            pass

    print(f"Evento {numero_evento}: IC salvo em {caminho_ic} "
          f"(validos={valido_ic.sum()}, pendentes={n_pendentes}, "
          f"IC_medio={np.nanmean(IC[valido_ic]):.3f}, {time.time()-t0:.1f}s)")

print("\nConcluido - IC calculado por evento.")
