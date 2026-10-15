"""
Pacote de auditoria do EVENTO 11 (04-08/jul/2019) - PARTE 1: dados.

Reconstroi, de forma independente (sem ler Q/pr/E/SY ja gerados), todas as
etapas do modelo para o evento 11 a partir dos insumos brutos, confere com os
rasters ja produzidos no projeto e grava em C:/TCC/Evento11_Auditoria:

    3_Rasters_QGIS/      GeoTIFFs do evento (insumos e resultados)
    2_Shapefiles_QGIS/   camadas vetoriais (mascara, estacoes, solo, uso, ...)
    dados_evento11.pkl   tudo que a PARTE 2 (planilhas) precisa

Roda com o Python do QGIS:
    "C:/Program Files/QGIS 4.2.1/bin/python-qgis.bat" gerar_pacote_evento11_dados.py
"""

import os
import pickle
import shutil
import sys

import numpy as np
import pandas as pd
import geopandas as gpd
from osgeo import gdal
from pyproj import Transformer

gdal.UseExceptions()
sys.stdout.reconfigure(encoding="utf-8")

BASE = r"C:\TCC"
DI = os.path.join(BASE, "Dados Iniciais")
EV = os.path.join(BASE, "Evento 11")
OUT = os.path.join(BASE, "Evento11_Auditoria")
RAS = os.path.join(OUT, "3_Rasters_QGIS")
SHP = os.path.join(OUT, "2_Shapefiles_QGIS")
for p in (OUT, RAS, SHP):
    os.makedirs(p, exist_ok=True)

N_EV = 11
LAMBDA = 0.05
P_CONST = 1.0
COEF = 11.8
EXPO = 0.56


def le(caminho, extra_nodata=False):
    ds = gdal.Open(caminho)
    b = ds.GetRasterBand(1)
    a = b.ReadAsArray().astype(np.float64)
    nd = b.GetNoDataValue()
    ok = np.isfinite(a)
    if nd is not None:
        ok &= a != nd
    if extra_nodata:
        ok &= (a > -1e30) & (a != 0)
    return np.where(ok, a, np.nan), ds


def grava(caminho, arr, ref_ds, nodata=-9999.0):
    drv = gdal.GetDriverByName("GTiff")
    out = drv.Create(caminho, arr.shape[1], arr.shape[0], 1, gdal.GDT_Float32)
    out.SetGeoTransform(ref_ds.GetGeoTransform())
    out.SetProjection(ref_ds.GetProjection())
    b = out.GetRasterBand(1)
    b.WriteArray(np.where(np.isfinite(arr), arr, nodata).astype(np.float32))
    b.SetNoDataValue(nodata)
    b.FlushCache()
    out = None


# ----------------------------------------------------------------------
# 1. Grade de referencia (a mesma do ChuvaIDW11.tif)
# ----------------------------------------------------------------------
P_qgis, ds_ref = le(os.path.join(EV, "ChuvaIDW11.tif"))
gt = ds_ref.GetGeoTransform()
ny, nx = P_qgis.shape
dx, dy = gt[1], -gt[5]
A_pix = dx * dy
cx = gt[0] + (np.arange(nx) + 0.5) * dx
cy = gt[3] - (np.arange(ny) + 0.5) * dy
X, Y = np.meshgrid(cx, cy)
print(f"grade {nx}x{ny}  dx={dx:.8f} dy={dy:.8f}  A_pixel={A_pix:.4f} m2")

# ----------------------------------------------------------------------
# 2. Evento e estacoes
# ----------------------------------------------------------------------
ev_df = pd.read_excel(os.path.join(DI, "eventos_processados_manuais.xlsx"), sheet_name="Sheet1").iloc[:18]
linha = ev_df.iloc[N_EV]
RI = float(linha["Intensidade_60min_mm/h"])
R_EV = float(linha["Chuva_evento_mm"])
V_MED = float(linha["T_R_m3"])
SY_OBS = float(linha["SYY_t"])

est = pd.read_csv(os.path.join(DI, "ESTPLUV", "ESTPLUV_11.csv"), sep=";")
tr = Transformer.from_crs(4326, 31983, always_xy=True)
est["x_utm"], est["y_utm"] = zip(*[tr.transform(lo, la) for lo, la in zip(est.lon, est.lat)])
print(est)

# ----------------------------------------------------------------------
# 3. IDW (potencia 2) recalculado e comparado ao raster do QGIS
# ----------------------------------------------------------------------
num = den = 0.0
for _, e in est.iterrows():
    d2 = (X - e.x_utm) ** 2 + (Y - e.y_utm) ** 2
    num = num + e.P / d2
    den = den + 1.0 / d2
P_idw = num / den
dif_idw = np.nanmax(np.abs(P_idw - P_qgis))
print(f"IDW: diferenca maxima entre Excel/Python e raster QGIS = {dif_idw:.2e} mm")

# ----------------------------------------------------------------------
# 4. CN (AMC II -> AMC I) -> S, alinhado a grade 884x365 (vizinho mais proximo)
# ----------------------------------------------------------------------
def alinha(caminho):
    s = gdal.Open(caminho)
    o = gdal.Warp(
        "", s, format="MEM", width=nx, height=ny,
        outputBounds=(gt[0], gt[3] + ny * gt[5], gt[0] + nx * dx, gt[3]),
        dstSRS=ds_ref.GetProjection(), resampleAlg=gdal.GRA_NearestNeighbour,
    )
    b = o.GetRasterBand(1)
    a = b.ReadAsArray().astype(np.float64)
    nd = b.GetNoDataValue()
    ok = np.isfinite(a) & (a > -1e30) & (a != 0)
    if nd is not None:
        ok &= a != nd
    return np.where(ok, a, np.nan)


CN2 = alinha(os.path.join(DI, "CN TCC.tif"))
CN1_arq = alinha(os.path.join(DI, "CN TCC - Seco.tif"))
S_arq = alinha(os.path.join(DI, "S - Seco.tif"))
CN1 = 4.2 * CN2 / (10 - 0.058 * CN2)
S = 25.4 * (1000 / CN1 - 10)
print(f"CN-I (formula) x arquivo: dif max = {np.nanmax(np.abs(CN1 - CN1_arq)):.2e}")
print(f"S (formula) x arquivo   : dif max = {np.nanmax(np.abs(S - S_arq)):.2e}")

# ----------------------------------------------------------------------
# 5. K, C, LS (valores dos rasters) e classes por ponto-em-poligono
# ----------------------------------------------------------------------
K, _ = le(os.path.join(DI, "K_raster.tif"))
C, _ = le(os.path.join(DI, "C_raster.tif"))
LS, _ = le(os.path.join(DI, "LS_raster.tif"))

Q_arq, _ = le(os.path.join(EV, "Q11_CN1.tif"))
mask_q = np.isfinite(Q_arq)
iy, ix = np.where(mask_q)
pts = gpd.GeoDataFrame({"lin": iy, "col": ix}, geometry=gpd.points_from_xy(X[iy, ix], Y[iy, ix]), crs=31983)

ped = gpd.read_file(os.path.join(BASE, "Pedologia Alto.shp"), encoding="utf-8")
uso = gpd.read_file(os.path.join(BASE, "Uso Solo Alto.shp"), encoding="utf-8")
j1 = gpd.sjoin(pts, ped[["Subordem", "Valor", "geometry"]], how="left", predicate="within")
j1 = j1[~j1.index.duplicated()]
j2 = gpd.sjoin(pts, uso[["CLASSE", "Valor", "geometry"]], how="left", predicate="within")
j2 = j2[~j2.index.duplicated()]
solo = j1["Subordem"].to_numpy(dtype=object)
usoc = j2["CLASSE"].to_numpy(dtype=object)
solo = np.array([s if isinstance(s, str) else "" for s in solo], dtype=object)
usoc = np.array([s if isinstance(s, str) else "" for s in usoc], dtype=object)
kpol = j1["Valor"].to_numpy(dtype=float)
cpol = j2["Valor"].to_numpy(dtype=float)
k_r = K[iy, ix]
c_r = C[iy, ix]
ok = np.isfinite(k_r)
print(f"K raster x poligono: {np.sum(np.isclose(k_r[ok], kpol[ok], atol=1e-6))}/{ok.sum()} pixels iguais")
ok = np.isfinite(c_r)
print(f"C raster x poligono: {np.sum(np.isclose(c_r[ok], cpol[ok], atol=1e-6))}/{ok.sum()} pixels iguais")

# tabelas de classe -> fator
tab_K = ped.groupby("Subordem")["Valor"].agg(["first", "nunique"]).reset_index()
tab_C = uso.groupby("CLASSE")["Valor"].agg(["first", "nunique"]).reset_index()
assert (tab_K["nunique"] == 1).all() and (tab_C["nunique"] == 1).all()

# ----------------------------------------------------------------------
# 6. Cadeia completa recalculada
# ----------------------------------------------------------------------
Q = np.where(P_idw <= LAMBDA * S, 0.0, (P_idw - LAMBDA * S) ** 2 / (P_idw + (1 - LAMBDA) * S))
Q = np.where(np.isfinite(S), Q, np.nan)
pr = Q / 1000 * A_pix * (RI / R_EV) / 3600
valido = np.isfinite(Q) & np.isfinite(K) & np.isfinite(C) & np.isfinite(LS)
E = np.where(valido, COEF * np.maximum(Q * pr * A_pix, 0) ** EXPO * K * C * P_CONST * LS, np.nan)

V_calc_900 = np.nansum(Q) / 1000 * 900.0
V_calc_valid = np.nansum(np.where(valido, Q, 0)) / 1000 * A_pix
f = V_MED / V_calc_valid
Qo = np.where(valido, np.minimum(f * Q, P_idw), np.nan)
n_exc = int(np.sum(valido & (f * Q > P_idw)))
pro = Qo / 1000 * A_pix * (RI / R_EV) / 3600
Eo = np.where(valido, COEF * np.maximum(Qo * pro * A_pix, 0) ** EXPO * K * C * P_CONST * LS, np.nan)

# c de calibracao (17 eventos) - sai do CSV ja produzido
cmp_csv = pd.read_csv(os.path.join(DI, "comparacao_SY_previsao_vs_restrito.csv")).sort_values("evento")
SYobs17 = cmp_csv["SY_obs_t"].to_numpy(float)
E17 = cmp_csv["soma_E_unit_previsao_t"].to_numpy(float)
Eo17 = cmp_csv["soma_E_unit_restrito_t"].to_numpy(float)
c_pura = np.sum(E17 * SYobs17) / np.sum(E17 ** 2)
c_restr = np.sum(Eo17 * SYobs17) / np.sum(Eo17 ** 2)
SY = c_pura * E
SYo = c_restr * Eo
print(f"V_calc(900 m2, todos Q)={V_calc_900:,.1f} | V_calc(valido, A_pix)={V_calc_valid:,.1f} | f={f:.6f} | Q>P: {n_exc}")
print(f"sum E pura (recalculada)={np.nansum(E):.4f} | restrita={np.nansum(Eo):.4f}")
print(f"c_pura={c_pura:.6f} c_restr={c_restr:.6f}")
print(f"SY pura={np.nansum(SY):.3f} t | SY restrita={np.nansum(SYo):.3f} t | SY obs={SY_OBS:.3f} t")

# conferencia com rasters do projeto
for nome, mine in [("Q11_CN1", Q), ("pr11", pr), ("E_unit11", E), ("SY11", SY),
                   ("Q11_CN1_obs", Qo), ("pr11_obs", pro), ("E_unit11_obs", Eo), ("SY11_obs", SYo)]:
    arq, _ = le(os.path.join(EV, nome + ".tif"))
    both = np.isfinite(arq) & np.isfinite(mine)
    print(f"  {nome:<14} validos arq={np.isfinite(arq).sum():>7} meu={np.isfinite(mine).sum():>7}  "
          f"dif max={np.nanmax(np.abs(arq[both] - mine[both])):.2e}  soma arq={np.nansum(arq):.4f} meu={np.nansum(mine):.4f}")

# ----------------------------------------------------------------------
# 7. Rasters para o QGIS
# ----------------------------------------------------------------------
for nome in ["ChuvaIDW11", "Q11_CN1", "pr11", "E_unit11", "SY11",
             "Q11_CN1_obs", "pr11_obs", "E_unit11_obs", "SY11_obs"]:
    shutil.copy2(os.path.join(EV, nome + ".tif"), os.path.join(RAS, nome + ".tif"))
for nome in ["K_raster", "C_raster", "LS_raster"]:
    shutil.copy2(os.path.join(DI, nome + ".tif"), os.path.join(RAS, nome + ".tif"))
grava(os.path.join(RAS, "CN_II_alinhado.tif"), CN2, ds_ref)
grava(os.path.join(RAS, "CN_I_alinhado.tif"), CN1, ds_ref)
grava(os.path.join(RAS, "S_CN_I_alinhado.tif"), S, ds_ref)

# ----------------------------------------------------------------------
# 8. Shapefiles para o QGIS
# ----------------------------------------------------------------------
for stem in ["Máscara Jundiaí", "drenagem"]:
    for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg"]:
        orig = os.path.join(DI, stem + ext)
        if os.path.exists(orig):
            novo = {"Máscara Jundiaí": "Mascara_Bacia"}.get(stem, stem)
            shutil.copy2(orig, os.path.join(SHP, novo + ext))
for stem, novo in [("Pedologia Alto", "Pedologia_K"), ("Uso Solo Alto", "UsoSolo_C")]:
    for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg"]:
        orig = os.path.join(BASE, stem + ext)
        if os.path.exists(orig):
            shutil.copy2(orig, os.path.join(SHP, novo + ext))

w1 = None  # preenchido na PARTE 2 (planilha hidrologica) - aqui so a camada de estacoes
est_gdf = gpd.GeoDataFrame(
    {"id": est["id"], "lon": est["lon"], "lat": est["lat"], "P_mm": est["P"],
     "x_utm": est["x_utm"], "y_utm": est["y_utm"]},
    geometry=gpd.points_from_xy(est["x_utm"], est["y_utm"]), crs=31983,
)
est_gdf.to_file(os.path.join(SHP, "Estacoes_Chuva_Ev11.shp"), encoding="utf-8")

ids = np.arange(1, len(iy) + 1)
pix = gpd.GeoDataFrame(
    {
        "id": ids, "lin": iy, "col": ix,
        "P_mm": P_idw[iy, ix], "CN_II": CN2[iy, ix], "CN_I": CN1[iy, ix], "S_mm": S[iy, ix],
        "Solo": solo, "K": K[iy, ix], "Uso": usoc, "C": C[iy, ix], "LS": LS[iy, ix],
        "valido": valido[iy, ix].astype(int),
        "Q_mm": Q[iy, ix], "pr_m3s": pr[iy, ix], "E_t": E[iy, ix], "SY_t": SY[iy, ix],
        "Qobs_mm": Qo[iy, ix], "Eobs_t": Eo[iy, ix], "SYobs_t": SYo[iy, ix],
    },
    geometry=gpd.points_from_xy(X[iy, ix], Y[iy, ix]), crs=31983,
)
pix.to_file(os.path.join(SHP, "Pixels_Evento11.shp"), encoding="utf-8")
print(f"Pixels_Evento11.shp: {len(pix)} pontos")

# ----------------------------------------------------------------------
# 9. Pickle para a parte 2
# ----------------------------------------------------------------------
dados = dict(
    nx=nx, ny=ny, dx=dx, dy=dy, A_pix=A_pix, X0=gt[0], Y0=gt[3],
    est=est, RI=RI, R_EV=R_EV, V_MED=V_MED, SY_OBS=SY_OBS, linha=linha,
    iy=iy, ix=ix, P=P_idw[iy, ix], CN2=CN2[iy, ix], CN1=CN1[iy, ix], S=S[iy, ix],
    solo=solo, usoc=usoc, K=K[iy, ix], C=C[iy, ix], LS=LS[iy, ix],
    valido=valido[iy, ix], Q=Q[iy, ix], pr=pr[iy, ix], E=E[iy, ix], SY=SY[iy, ix],
    Qo=Qo[iy, ix], pro=pro[iy, ix], Eo=Eo[iy, ix], SYo=SYo[iy, ix],
    tab_K=tab_K, tab_C=tab_C, cmp_csv=cmp_csv, c_pura=c_pura, c_restr=c_restr,
    f=f, V_calc_900=V_calc_900, V_calc_valid=V_calc_valid, n_exc=n_exc,
    P_grid=P_idw, valido_grid=valido, Q_grid=Q, E_grid=E, SY_grid=SY, Qo_grid=Qo, Eo_grid=Eo, SYo_grid=SYo,
    S_grid=S, K_grid=K, C_grid=C, LS_grid=LS, pr_grid=pr,
)
with open(os.path.join(OUT, "dados_evento11.pkl"), "wb") as fh:
    pickle.dump(dados, fh)
print("OK")
