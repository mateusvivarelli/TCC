"""
Recalcula o FCI (Functional Connectivity Index) por evento, seguindo a
Eq. (7) exata de Hao et al. (2022) - CORRIGE calcular_ic_por_evento.py,
que usava a media do E_unit completo como W-barra (Eq. 5 generica do
IC de Borselli), quando na verdade Hao et al. tem uma formula propria
para o numerador, especifica para a MUSLE:

    FCI_k = log10( [11,8 * (Q-barra * pr-barra)^0,56 * K-barra * C-barra
                    * P-barra * S-barra * sqrt(A)] / Ddn_k )

    Ddn_k = soma, ao longo do fluxo D8 ate o exutorio, de d_i/(W_i*S_i)
            (W_i = E_unit,i local - isso NAO muda, e o mesmo do IC
            generico, Eq. 6)

Diferencas-chave em relacao a versao anterior:
- Q-barra, pr-barra, K-barra, C-barra, S-barra sao medias SEPARADAS
  sobre a area de montante (nao a media do E_unit ja calculado/
  combinado).
- O fator LS NAO entra no numerador (so entra em E_unit, usado no
  denominador via W_i).
- K-barra, C-barra, S-barra sao fixos (nao mudam por evento) - so
  Q-barra e pr-barra precisam ser recalculados a cada evento.
"""

import os
import time
import subprocess
import numpy as np
from osgeo import gdal

gdal.UseExceptions()

BASE = r"C:\TCC"
PASTA_DADOS = os.path.join(BASE, "Dados Iniciais")
PASTA_QP = os.path.join(PASTA_DADOS, "qp_spatial")
QGIS_PROCESS = r"C:\Program Files\QGIS 3.44.14\bin\qgis_process-qgis-ltr.bat"
DEM_FILLED = os.path.join(PASTA_QP, "carvedDEM_corrigido_filled.tif")

OUTLET_X, OUTLET_Y = 318980.7663669552, 7432307.0820886735
P_CONST = 1.0

# ============================================================
# 1. BASE FIXA: DEM, D8, declividade, area (reaproveitados)
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

tem_destino = VALIDO & (downstream_row >= 0) & (downstream_col >= 0)
idx_r, idx_c = np.where(tem_destino)
dest_r = downstream_row[idx_r, idx_c]
dest_c = downstream_col[idx_r, idx_c]

print(f"Base fixa pronta. Exutorio: linha={row_exutorio}, col={col_exutorio}")


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
        f"--FLOW={PASTA_QP}\\_flowacc_tmp_fci.tif",
        f"--VAL_INPUT={val_input_path}",
        f"--VAL_MEAN={saida_path}",
        f"--ACCU_TARGET={DEM_FILLED}",
    ], capture_output=True, text=True)


def reprojeta_para_dem(caminho_origem, caminho_saida, nodata_saida=-9999):
    ds = gdal.Open(caminho_origem)
    gdal.Warp(
        caminho_saida, ds, format="GTiff",
        width=ncols, height=nrows,
        outputBounds=(gt[0], gt[3] + nrows * gt[5], gt[0] + ncols * gt[1], gt[3]),
        dstSRS=proj, resampleAlg=gdal.GRA_NearestNeighbour, dstNodata=nodata_saida,
    )
    return None


def le_raster(caminho):
    ds = gdal.Open(caminho)
    band = ds.GetRasterBand(1)
    nodata = band.GetNoDataValue()
    arr = band.ReadAsArray().astype(np.float64)
    arr = np.where((arr != nodata) & np.isfinite(arr), arr, np.nan)
    ds = None
    return arr


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
# 2. FATORES FIXOS (K-barra, C-barra, S-barra) - calculados 1 vez
# ============================================================

print("\nCalculando K-barra e C-barra (medias de montante, fixas)...")

caminho_k_dem = os.path.join(PASTA_QP, "_K_dem_tmp.tif")
reprojeta_para_dem(os.path.join(PASTA_DADOS, "K_raster.tif"), caminho_k_dem)
caminho_k_mean = os.path.join(PASTA_QP, "K_mean_upslope.tif")
roda_saga_val_mean(caminho_k_dem, caminho_k_mean)
K_BARRA = le_raster(caminho_k_mean)

caminho_c_dem = os.path.join(PASTA_QP, "_C_dem_tmp.tif")
reprojeta_para_dem(os.path.join(PASTA_DADOS, "C_raster.tif"), caminho_c_dem)
caminho_c_mean = os.path.join(PASTA_QP, "C_mean_upslope.tif")
roda_saga_val_mean(caminho_c_dem, caminho_c_mean)
C_BARRA = le_raster(caminho_c_mean)

S_BARRA = le_raster(os.path.join(PASTA_QP, "slope_mean_upslope_pct.tif")) / 100.0
S_BARRA = np.where(np.isfinite(S_BARRA), np.clip(S_BARRA, 0.001, None), np.nan)

print(f"K-barra: media={np.nanmean(K_BARRA):.4f} | C-barra: media={np.nanmean(C_BARRA):.4f} | "
      f"S-barra: media={np.nanmean(S_BARRA):.4f}")

for tmp in (caminho_k_dem, caminho_c_dem):
    try:
        os.remove(tmp)
    except OSError:
        pass

# ============================================================
# 3. LOOP DOS 17 EVENTOS: Q-barra, pr-barra, Dup, Ddn, FCI
# ============================================================

resumo = []

for numero_evento in range(1, 18):
    t0 = time.time()
    PASTA_EVENTO = os.path.join(BASE, f"Evento {numero_evento}")

    # Q-barra (media de montante de Q)
    caminho_q_dem = os.path.join(PASTA_QP, f"_Q_dem_tmp{numero_evento}.tif")
    reprojeta_para_dem(os.path.join(PASTA_EVENTO, f"Q{numero_evento}_CN1.tif"), caminho_q_dem)
    caminho_q_mean = os.path.join(PASTA_QP, f"_Q_mean_tmp{numero_evento}.tif")
    roda_saga_val_mean(caminho_q_dem, caminho_q_mean)
    Q_BARRA = le_raster(caminho_q_mean)

    # pr-barra (media de montante de pr)
    caminho_pr_dem = os.path.join(PASTA_QP, f"_pr_dem_tmp{numero_evento}.tif")
    reprojeta_para_dem(os.path.join(PASTA_EVENTO, f"pr{numero_evento}.tif"), caminho_pr_dem)
    caminho_pr_mean = os.path.join(PASTA_QP, f"_pr_mean_tmp{numero_evento}.tif")
    roda_saga_val_mean(caminho_pr_dem, caminho_pr_mean)
    PR_BARRA = le_raster(caminho_pr_mean)

    # Dup (Eq. 7): 11,8*(Q-barra*pr-barra)^0,56 * K-barra * C-barra * P-barra * S-barra * sqrt(A)
    base = np.clip(Q_BARRA * PR_BARRA, 0, None)
    Dup = 11.8 * (base ** 0.56) * K_BARRA * C_BARRA * P_CONST * S_BARRA * np.sqrt(np.where(A_M2 > 0, A_M2, np.nan))

    # Ddn: usa E_unit local (W_i) - reaproveita o raster ja reprojetado
    caminho_e_unit = os.path.join(PASTA_EVENTO, f"E_unit{numero_evento}.tif")
    caminho_w_dem = os.path.join(PASTA_QP, f"_W_dem_tmp{numero_evento}.tif")
    reprojeta_para_dem(caminho_e_unit, caminho_w_dem)
    W_evento = le_raster(caminho_w_dem)
    W_evento = np.where(np.isfinite(W_evento) & (W_evento > 0), W_evento, 1e-6)

    Ddn_2d, n_pendentes = calcula_ddn(W_evento)

    FCI = np.full((nrows, ncols), np.nan, dtype=np.float64)
    valido_fci = VALIDO & np.isfinite(Ddn_2d) & (Ddn_2d > 0) & np.isfinite(Dup) & (Dup > 0)
    FCI[valido_fci] = np.log10(Dup[valido_fci] / Ddn_2d[valido_fci])

    caminho_fci = os.path.join(PASTA_EVENTO, f"FCI{numero_evento}.tif")
    salva_raster(caminho_fci, FCI)

    resumo.append((numero_evento, valido_fci.sum(), np.nanmean(FCI[valido_fci]),
                   np.nanmin(FCI[valido_fci]), np.nanmax(FCI[valido_fci])))

    for tmp in (caminho_q_dem, caminho_q_mean, caminho_pr_dem, caminho_pr_mean, caminho_w_dem):
        try:
            os.remove(tmp)
        except OSError:
            pass

    print(f"Evento {numero_evento}: FCI salvo em {caminho_fci} "
          f"(validos={valido_fci.sum()}, FCI_medio={np.nanmean(FCI[valido_fci]):.3f}, "
          f"{time.time()-t0:.1f}s)")

print("\n=== RESUMO ===")
print(f"{'Evento':>7} | {'validos':>8} | {'FCI_medio':>10} | {'FCI_min':>9} | {'FCI_max':>9}")
for ev, n, media, minimo, maximo in resumo:
    print(f"{ev:>7} | {n:>8} | {media:>10.3f} | {minimo:>9.3f} | {maximo:>9.3f}")

print("\nConcluido - FCI (Eq. 7 exata) calculado por evento.")
