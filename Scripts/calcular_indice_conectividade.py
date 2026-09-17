"""
Calcula o Indice de Conectividade (IC, Borselli et al. 2008; adaptado
por Hao et al. 2022, usando o exutorio da bacia como alvo em vez do
canal mais proximo):

    IC = log10( Dup / Ddn )
    Dup = W_medio_montante * S_medio_montante * sqrt(A)
    Ddn = soma, ao longo do caminho de fluxo D8 ate o exutorio, de
          d_i / (W_i * S_i)

Nesta primeira versao, o peso W e um placeholder uniforme (=1) - o
correto (W_i = E_unit,i, segundo Hao et al.) sera recalculado assim que
os rasters de K e C estiverem prontos (faltam os .dbf de
"Pedologia Alto.shp" e "Uso Solo Alto.shp").

Direcao de fluxo D8 calculada diretamente da elevacao (maior declive
entre os 8 vizinhos), em vez de decodificar a convencao do SAGA.
"""

import numpy as np
from osgeo import gdal

gdal.UseExceptions()

PASTA = r"C:\TCC\Dados Iniciais\qp_spatial"
OUTLET_X, OUTLET_Y = 318980.7663669552, 7432307.0820886735

# ============================================================
# 1. CARREGA DEM, FLOW ACCUMULATION E DECLIVIDADE
# ============================================================

dem_ds = gdal.Open(PASTA + r"\carvedDEM_corrigido_filled.tif")
gt = dem_ds.GetGeoTransform()
proj = dem_ds.GetProjection()
dem_band = dem_ds.GetRasterBand(1)
dem_nodata = dem_band.GetNoDataValue()
DEM = dem_band.ReadAsArray().astype(np.float64)
nrows, ncols = DEM.shape

flowacc_ds = gdal.Open(PASTA + r"\flowacc_corrigido.tif")
flowacc_band = flowacc_ds.GetRasterBand(1)
flowacc_nodata = flowacc_band.GetNoDataValue()
A_M2 = flowacc_band.ReadAsArray().astype(np.float64)

slope_ds = gdal.Open(PASTA + r"\slope_pct.tif")
slope_band = slope_ds.GetRasterBand(1)
SLOPE_MM = slope_band.ReadAsArray().astype(np.float64) / 100.0  # percent -> m/m
SLOPE_MM = np.clip(SLOPE_MM, 0.001, None)  # evita divisao por zero

slope_mean_ds = gdal.Open(PASTA + r"\slope_mean_upslope_pct.tif")
S_MEDIO_MONTANTE = slope_mean_ds.GetRasterBand(1).ReadAsArray().astype(np.float64) / 100.0
S_MEDIO_MONTANTE = np.clip(S_MEDIO_MONTANTE, 0.001, None)

VALIDO = (DEM != dem_nodata) & np.isfinite(DEM)
print(f"Pixels validos: {VALIDO.sum()}")

# ============================================================
# 2. DIRECAO DE FLUXO D8 (maior declive entre os 8 vizinhos)
# ============================================================

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

DEM_PAD = np.pad(DEM, 1, mode="constant", constant_values=np.nan)
VALIDO_PAD = np.pad(VALIDO, 1, mode="constant", constant_values=False)

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

n_sem_destino = int(np.sum(VALIDO & (downstream_row == -1)))
print(f"Pixels validos sem destino de fluxo (minimos locais/bordas): {n_sem_destino}")

print("Direcao de fluxo D8 calculada.")

# salva o D8 pra conferencia visual futura (opcional)
driver = gdal.GetDriverByName("GTiff")
out_dir = driver.Create(PASTA + r"\d8_flowto_row.tif", ncols, nrows, 1, gdal.GDT_Int32)
out_dir.SetGeoTransform(gt)
out_dir.SetProjection(proj)
out_dir.GetRasterBand(1).WriteArray(downstream_row)
out_dir.GetRasterBand(1).SetNoDataValue(-1)
out_dir = None

# ============================================================
# 3. Ddn: acumula d_i/(W_i*S_i) ao longo do fluxo D8 ate o exutorio
#    (propagacao vetorizada em "ondas", sem grafo/BFS em Python puro -
#    muito mais rapido que a versao anterior, que travava)
# ============================================================

import time

t0 = time.time()

W_PLACEHOLDER = np.ones((nrows, ncols), dtype=np.float64)

col_exutorio = int((OUTLET_X - gt[0]) / gt[1])
row_exutorio = int((OUTLET_Y - gt[3]) / gt[5])
print(f"\nPixel do exutorio: linha={row_exutorio}, col={col_exutorio}", flush=True)

custo_local = downstream_dist / (W_PLACEHOLDER * SLOPE_MM)

Ddn_2d = np.full((nrows, ncols), np.nan, dtype=np.float64)
Ddn_2d[row_exutorio, col_exutorio] = 0.0

# indices (linear) de destino de cada celula valida com destino definido
tem_destino = VALIDO & (downstream_row >= 0) & (downstream_col >= 0)
idx_r, idx_c = np.where(tem_destino)
dest_r = downstream_row[idx_r, idx_c]
dest_c = downstream_col[idx_r, idx_c]

pendentes = np.ones(len(idx_r), dtype=bool)
max_passos = nrows + ncols  # limite de seguranca

for passo in range(max_passos):
    if not pendentes.any():
        break
    ddn_destino = Ddn_2d[dest_r[pendentes], dest_c[pendentes]]
    prontos_local = np.isfinite(ddn_destino)
    if not prontos_local.any():
        # nenhuma celula pendente tem destino pronto ainda - continua
        continue
    idx_pend = np.where(pendentes)[0]
    idx_prontos = idx_pend[prontos_local]

    rr = idx_r[idx_prontos]
    cc = idx_c[idx_prontos]
    Ddn_2d[rr, cc] = custo_local[rr, cc] + ddn_destino[prontos_local]
    pendentes[idx_prontos] = False

    if passo % 50 == 0:
        print(f"  passo {passo}: {pendentes.sum()} pendentes, {time.time()-t0:.1f}s", flush=True)

print(f"Ddn calculado em {time.time()-t0:.1f}s. Pendentes restantes (nao alcancaram o exutorio): "
      f"{pendentes.sum()}", flush=True)

# ============================================================
# 4. Dup e IC final
# ============================================================

W_MEDIO_MONTANTE = np.ones((nrows, ncols), dtype=np.float64)  # placeholder

Dup = W_MEDIO_MONTANTE * S_MEDIO_MONTANTE * np.sqrt(np.where(A_M2 > 0, A_M2, np.nan))

IC = np.full((nrows, ncols), np.nan, dtype=np.float64)
valido_ic = VALIDO & np.isfinite(Ddn_2d) & (Ddn_2d > 0) & np.isfinite(Dup) & (Dup > 0)
IC[valido_ic] = np.log10(Dup[valido_ic] / Ddn_2d[valido_ic])

print(f"\nPixels com IC valido: {valido_ic.sum()} de {VALIDO.sum()}")
print(f"IC: min={np.nanmin(IC):.3f}, max={np.nanmax(IC):.3f}, media={np.nanmean(IC[valido_ic]):.3f}")

# ============================================================
# 5. SALVA OS RASTERS
# ============================================================

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

salva_raster(PASTA + r"\Ddn_placeholder.tif", Ddn_2d)
salva_raster(PASTA + r"\Dup_placeholder.tif", Dup)
salva_raster(PASTA + r"\IC_placeholder.tif", IC)

print("\nRasters salvos: Ddn_placeholder.tif, Dup_placeholder.tif, IC_placeholder.tif")
print("(placeholder = usa W=1 uniforme; recalcular quando K/C estiverem prontos)")
