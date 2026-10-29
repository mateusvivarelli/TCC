"""Cálculos pendentes das propostas de 30/10/2026 (rodar NO PC, com os rasters; NÃO TESTADO na nuvem, que não tem rasters).
Rodar da raiz do repositório com o Python do QGIS (GDAL), por exemplo:
    "C:\\Program Files\\QGIS 4.2.1\\bin\\python-qgis.bat" Scripts\\_analise_mapa_declividade_r2_30-10.py
Imprime:
  (1) R² do mapa de erosão média com K*LS*C (C31): em log e linear; R² com o termo de escoamento G; partição pela média
      dos ganhos de R² nas duas ordens (seção 3.4.9 da proposta). Para MC e MFM.
  (2) Contribuição por classe de declividade (Tabela 16) e cruzamento uso x solo x declividade nos 5% de pixels críticos.
  (3) Volume do MFM depois do limite Q <= P, contra o escoamento direto medido, por evento (seção 3.4.4).
  (4) Fração da erosão média nos pixels com CN-I < 35 (S0,20 > 471,7 mm), fora da faixa de Woodward et al. (2003).
Caminhos iguais aos de calcular_sy_lambda005_woodward.py, gerar_tabelas_tcc.py e _recalcular_ls_moore.py; conferir antes.
"""
import os
import pickle
import numpy as np
import pandas as pd
from osgeo import gdal

gdal.UseExceptions()
BASE = "."
DI = os.path.join(BASE, "Dados Iniciais")
N = 17


def le(p):
    ds = gdal.Open(p); b = ds.GetRasterBand(1)
    a = b.ReadAsArray().astype(np.float64); nd = b.GetNoDataValue()
    ok = np.isfinite(a) & (a > -1e30)
    if nd is not None:
        ok &= a != nd
    return np.where(ok, a, np.nan), ds


K, ds0 = le(os.path.join(DI, "K_raster.tif"))
C, _ = le(os.path.join(DI, "C_raster.tif"))
LS, _ = le(os.path.join(DI, "LS_moore.tif"))
gt = ds0.GetGeoTransform(); ny, nx = K.shape; A = abs(gt[1] * gt[5])


def warp(p, alg=gdal.GRA_NearestNeighbour):
    o = gdal.Warp("", gdal.Open(p), format="MEM", width=nx, height=ny,
                  outputBounds=(gt[0], gt[3] + ny * gt[5], gt[0] + nx * gt[1], gt[3]), dstSRS=ds0.GetProjection(), resampleAlg=alg)
    a = o.GetRasterBand(1).ReadAsArray().astype(np.float64)
    return np.where(a > -1e30, a, np.nan)


S20 = warp(os.path.join(DI, "S - Seco.tif"))
SLOPE = warp(os.path.join(DI, "qp_spatial", "slope_pct.tif"), gdal.GRA_Bilinear)  # mesma leitura do _recalcular_ls_moore.py
MC, _ = le(os.path.join(DI, "SY_medio_eventos_l05w.tif"))          # t por pixel, média dos 17 eventos
MF, _ = le(os.path.join(DI, "SY_medio_eventos_forcado_l05w.tif"))
KLSC = K * LS * C


def r2(y, x):
    return np.corrcoef(y, x)[0, 1] ** 2


print("=" * 100)
print("(1) R² do mapa de erosão média com K*LS*C (pixels com erosão > 0)")
for nome, M in (("MC", MC), ("MFM", MF)):
    ok = np.isfinite(M) & np.isfinite(KLSC) & (M > 0) & (KLSC > 0)
    ly, lk = np.log(M[ok]), np.log(KLSC[ok])
    lg = ly - lk                      # ln G_k + constante (G = termo de escoamento: chuva e CN)
    r_k, r_g = r2(ly, lk), r2(ly, lg)
    X = np.column_stack([np.ones(ok.sum()), lk, lg])
    res = ly - X @ np.linalg.lstsq(X, ly, rcond=None)[0]
    r_tot = 1 - res.var() / ly.var()  # deve dar 1 (decomposição exata)
    parte_k = 0.5 * (r_k + (r_tot - r_g)); parte_g = 0.5 * (r_g + (r_tot - r_k))
    print(f"{nome}: pixels {ok.sum()} | log: R2(KLSC) = {r_k:.3f}; R2(G) = {r_g:.3f}; R2 total = {r_tot:.3f} | "
          f"partição: fatores fixos {100*parte_k:.1f}%, escoamento {100*parte_g:.1f}% | "
          f"linear: R2(M, KLSC) = {r2(M[ok], KLSC[ok]):.3f} (Pearson {np.corrcoef(M[ok], KLSC[ok])[0,1]:.3f})")

print("=" * 100)
print("(2) Contribuição por classe de declividade (Tabela 16)")
cls = [(0, 3), (3, 8), (8, 20), (20, 45), (45, 75), (75, 1e9)]
okm = np.isfinite(MC) & np.isfinite(MF) & np.isfinite(SLOPE)
print(f"pixels com erosão e declividade: {okm.sum()} (conferir contra 153.855)")
lin = []
for a, b in cls:
    m = okm & (SLOPE >= a) & (SLOPE < b)
    lin.append((f"{a} a {b if b < 1e8 else 'mais'}", 100 * m.sum() / okm.sum(), 100 * MC[m].sum() / MC[okm].sum(), 100 * MF[m].sum() / MF[okm].sum()))
print(pd.DataFrame(lin, columns=["Declividade (%)", "Área (%)", "Erosão MC (%)", "Erosão MFM (%)"]).round(1).to_string(index=False))

# cruzamento nos pixels críticos (5% maiores do MC), com as classes de uso e solo do pacote do evento 11
with open(os.path.join(BASE, "Evento11_Auditoria", "dados_evento11.pkl"), "rb") as fh:
    D = pickle.load(fh)
iy, ix = np.asarray(D["iy"]), np.asarray(D["ix"])
uso = np.array(D["usoc"], dtype=object); solo = np.array(D["solo"], dtype=object)
mc_v, sl_v = MC[iy, ix], SLOPE[iy, ix]
okv = np.isfinite(mc_v) & np.isfinite(sl_v)
lim = np.nanpercentile(mc_v[okv], 95)
crit = okv & (mc_v >= lim)
dc = pd.cut(sl_v, [0, 3, 8, 20, 45, 75, 1e9], right=False, labels=["0-3", "3-8", "8-20", "20-45", "45-75", ">75"])
t = pd.DataFrame({"uso": uso[crit], "solo": solo[crit], "decl": np.asarray(dc)[crit]})
print(f"\npixels críticos (MC, >= percentil 95 = {lim*1000:.1f} kg): {crit.sum()}")
print((t.value_counts(normalize=True) * 100).round(1).head(10).to_string())

print("=" * 100)
print("(3) MFM: volume depois do limite Q <= P contra o escoamento direto medido")
S05 = 25.4 * 1.33 * (S20 / 25.4) ** 1.15
valido = np.isfinite(S20) & np.isfinite(K) & np.isfinite(C) & np.isfinite(LS)
ev = pd.read_excel(os.path.join(DI, "eventos_processados_manuais.xlsx"), sheet_name="Sheet1").iloc[:18]
h = pd.read_excel(os.path.join(DI, "Dados_finais_histereses_corrigido.xlsx"), sheet_name="Planilha1").iloc[:, :8]
h.columns = ["Data", "P1", "P2", "Ptot", "Q", "CSS", "Bt", "CSSBt"]; h["Data"] = pd.to_datetime(h["Data"]); h = h.set_index("Data")
lin = []
for n in range(1, N + 1):
    r = ev.iloc[0 if n == 1 else n]; w = h.loc[r["Inicio"]:r["Fim"]]
    vd = r["T_R_m3"] - w.Bt.sum() * 3600
    p = le(os.path.join(BASE, f"Evento {n}", f"ChuvaIDW{n}.tif"))[0][valido]; s = S05[valido]
    q = np.where(p <= 0.05 * s, 0.0, (p - 0.05 * s) ** 2 / (p + 0.95 * s))
    vs = q.sum() / 1000 * A; f = vd / vs
    qf = np.minimum(f * q, p); vf = qf.sum() / 1000 * A
    lin.append((n, vd / 1e3, vs / 1e3, f, vf / 1e3, 100 * (vf / vd - 1), 100 * np.mean(f * q > p)))
print(pd.DataFrame(lin, columns=["Evento", "Vdir medido (10³ m³)", "V_SCS (10³ m³)", "f", "V_MFM após limite (10³ m³)",
                                 "Diferença (%)", "Pixels limitados (%)"]).round(2).to_string(index=False))

print("=" * 100)
print("(4) Pixels com CN-I < 35 (S0,20 > 471,7 mm)")
fora = valido & (S20 > 471.7)
okc = np.isfinite(MC)
print(f"pixels: {fora.sum()} ({100*fora.sum()/valido.sum():.1f}% dos pixels de cálculo); "
      f"erosão média MC nesses pixels: {100*np.nansum(MC[fora & okc])/np.nansum(MC[okc]):.1f}% do total; "
      f"MFM: {100*np.nansum(MF[fora & np.isfinite(MF)])/np.nansum(MF[np.isfinite(MF)]):.1f}%")
