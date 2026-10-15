"""
DIAGNOSTICO (15/10/2026): o que muda se o volume 'medido' for o escoamento DIRETO
(T_R_m3 - soma(Bt)*3600) em vez do volume total (T_R_m3 = soma(Q)*3600)?

Refaz, para os 17 eventos: (1) erro de volume do SCS-CN (lambda=0,05) e lambda
que zera o vies; (2) variante de volume restrito com o volume direto; (3) modelos
triviais SY = c*V; (4) previsao pura com o lambda recalibrado; (5) alvo SY sem a
carga da vazao de base (opcional).

Roda com python-qgis.bat (precisa do Drive montado: rasters dos eventos).
"""
import os
import sys

import numpy as np
import pandas as pd
from osgeo import gdal

gdal.UseExceptions()
sys.stdout.reconfigure(encoding="utf-8")

BASE = r"C:\TCC"
DI = os.path.join(BASE, "Dados Iniciais")
EXPO, COEF = 0.56, 11.8


def le(p):
    ds = gdal.Open(p); b = ds.GetRasterBand(1)
    a = b.ReadAsArray().astype(np.float64); nd = b.GetNoDataValue()
    ok = np.isfinite(a) & (a > -1e30)
    if nd is not None:
        ok &= a != nd
    return np.where(ok, a, np.nan), ds


K, ds0 = le(os.path.join(DI, "K_raster.tif")); C, _ = le(os.path.join(DI, "C_raster.tif")); LS, _ = le(os.path.join(DI, "LS_raster.tif"))
gt = ds0.GetGeoTransform(); ny, nx = K.shape; A = abs(gt[1] * gt[5])
s_ds = gdal.Open(os.path.join(DI, "S - Seco.tif"))
o = gdal.Warp("", s_ds, format="MEM", width=nx, height=ny, outputBounds=(gt[0], gt[3] + ny * gt[5], gt[0] + nx * gt[1], gt[3]),
              dstSRS=ds0.GetProjection(), resampleAlg=gdal.GRA_NearestNeighbour)
S = o.GetRasterBand(1).ReadAsArray().astype(np.float64); S = np.where(S > -1e30, S, np.nan)

ev = pd.read_excel(os.path.join(DI, "eventos_processados_manuais.xlsx"), sheet_name="Sheet1").iloc[:18]
h = pd.read_excel(os.path.join(DI, "Dados_finais_histereses_corrigido.xlsx"), sheet_name="Planilha1").iloc[:, :8]
h.columns = ["Data", "P1", "P2", "Ptot", "Q", "CSS", "Bt", "CSSBt"]; h["Data"] = pd.to_datetime(h["Data"]); h = h.set_index("Data")

N = 17
SY = np.zeros(N); TR = np.zeros(N); VD = np.zeros(N); RI = np.zeros(N); R = np.zeros(N); SYnet = np.zeros(N)
P = []
for n in range(1, N + 1):
    r = ev.iloc[0 if n == 1 else n]; w = h.loc[r["Inicio"]:r["Fim"]]
    SY[n - 1] = r["SYY_t"]; TR[n - 1] = r["T_R_m3"]
    VD[n - 1] = ((w.Q - w.Bt).sum()) * 3600
    SYnet[n - 1] = ((w.Q - w.Bt) * w.CSS).sum() * 3600 / 1e6
    RI[n - 1] = r["Intensidade_60min_mm/h"]; R[n - 1] = r["Chuva_evento_mm"]
    P.append(le(os.path.join(BASE, f"Evento {n}", f"ChuvaIDW{n}.tif"))[0])

mask_q = np.isfinite(S)
valido = mask_q & np.isfinite(K) & np.isfinite(C) & np.isfinite(LS)


def qscs(Pn, lam):
    return np.where(Pn <= lam * S, 0.0, (Pn - lam * S) ** 2 / (Pn + (1 - lam) * S))


def metricas(x, alvo, nome, dados=None):
    c = np.sum(x * alvo) / np.sum(x ** 2); sim = c * x
    den = np.sum((alvo - alvo.mean()) ** 2)
    loo = np.array([np.sum(np.delete(x, i) * np.delete(alvo, i)) / np.sum(np.delete(x, i) ** 2) * x[i] for i in range(N)])
    err = 100 * (sim - alvo) / alvo
    print(f"  {nome:<44} c={c:<11.5g} NSE={1-np.sum((alvo-sim)**2)/den:6.3f}  LOO={1-np.sum((alvo-loo)**2)/den:6.3f}  "
          f"erro medio={err.mean():+6.1f}%  abs={np.abs(err).mean():5.1f}%")
    return c, sim


def vol_stats(Vc, alvo):
    e = 100 * (Vc - alvo) / alvo
    nse = 1 - np.sum((alvo - Vc) ** 2) / np.sum((alvo - alvo.mean()) ** 2)
    return e.mean(), np.abs(e).mean(), nse


# ---------------------------------------------------------------- 1. volume x lambda
print("=" * 100)
print("1. VOLUME DO SCS-CN (CN-I) x alvo; Q valido (900 m2, igual ao CSV do projeto)")
print(f"   soma por evento: T_R total = {TR.sum():,.0f} m3 | escoamento direto = {VD.sum():,.0f} m3 ({100*VD.sum()/TR.sum():.1f}% do total)")
lams = np.round(np.arange(0.02, 0.41, 0.02), 2)
tab = []
for lam in lams:
    Vc = np.array([np.nansum(qscs(P[i], lam)[mask_q]) / 1000 * 900 for i in range(N)])
    tab.append((lam, Vc, vol_stats(Vc, TR), vol_stats(Vc, VD)))
print(f"   {'lambda':>6} | {'vs TOTAL: err med / abs / NSE':>32} | {'vs DIRETO: err med / abs / NSE':>32}")
for lam, Vc, a, b in tab:
    marca = " <- adotado" if abs(lam - 0.05) < 1e-9 else ""
    print(f"   {lam:6.2f} | {a[0]:+9.1f}% {a[1]:7.1f}% {a[2]:8.3f} | {b[0]:+9.1f}% {b[1]:7.1f}% {b[2]:8.3f}{marca}")
lam_zero = min(tab, key=lambda t: abs(t[3][0]))[0]
lam_nse = max(tab, key=lambda t: t[3][2])[0]
lam_abs = min(tab, key=lambda t: t[3][1])[0]
print(f"   lambda com vies ~0 contra o direto: {lam_zero:.2f} | melhor NSE do volume: {lam_nse:.2f} | menor erro absoluto: {lam_abs:.2f}")

# ---------------------------------------------------------------- 2. volume restrito
print("=" * 100)
print("2. VOLUME RESTRITO (Q reescalado por evento; lambda=0,05 como antes) - alvo SY_obs (carga total, SYY_t)")


def restrito(V):
    Es = np.zeros(N); fs = np.zeros(N); exc = 0
    for i in range(N):
        Q = qscs(P[i], 0.05); Vc = np.nansum(np.where(valido, Q, 0)) / 1000 * A
        f = V[i] / Vc; fs[i] = f
        Qo = np.where(valido, np.minimum(f * Q, P[i]), np.nan)
        pr = Qo / 1000 * A * (RI[i] / R[i]) / 3600
        E = np.where(valido, COEF * np.maximum(Qo * pr * A, 0) ** EXPO * K * C * LS, np.nan)
        Es[i] = np.nansum(E)
    return Es, fs


Es_tot, f_tot = restrito(TR)
Es_dir, f_dir = restrito(VD)
print(f"   fator f (total):  min={f_tot.min():.2f} max={f_tot.max():.2f} mediana={np.median(f_tot):.2f}")
print(f"   fator f (direto): min={f_dir.min():.2f} max={f_dir.max():.2f} mediana={np.median(f_dir):.2f}")
metricas(Es_tot, SY, "restrito ao volume TOTAL (T_R)  [atual]")
metricas(Es_dir, SY, "restrito ao volume DIRETO")
metricas(Es_dir, SYnet, "restrito ao DIRETO, alvo SY sem vazao de base")

# ---------------------------------------------------------------- 3. triviais
print("=" * 100)
print("3. MODELOS TRIVIAIS (sem MUSLE) - alvo SY_obs")
metricas(TR, SY, "SY = c * T_R (total)")
metricas(VD, SY, "SY = c * volume direto")
metricas(VD, SYnet, "SY = c * volume direto, alvo SY sem base")
metricas(R, SY, "SY = c * Chuva_evento")

# ---------------------------------------------------------------- 4. previsao pura x lambda
print("=" * 100)
print("4. PREVISAO PURA (Q do SCS-CN, sem usar volume medido) com varios lambda - alvo SY_obs")


def previsao(lam):
    Es = np.zeros(N)
    for i in range(N):
        Q = qscs(P[i], lam)
        pr = Q / 1000 * A * (RI[i] / R[i]) / 3600
        E = np.where(valido, COEF * np.maximum(Q * pr * A, 0) ** EXPO * K * C * LS, np.nan)
        Es[i] = np.nansum(E)
    return Es


for lam in sorted({0.05, 0.10, 0.18, 0.20, lam_zero, lam_nse}):
    metricas(previsao(lam), SY, f"previsao pura, lambda={lam:.2f}")
print("=" * 100)
