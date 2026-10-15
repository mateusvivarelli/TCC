"""
DIAGNOSTICO (15/10/2026): previsao pura 'escoamento direto (SCS-CN) + vazao de base'.

Q_pixel = Q_direto,k (SCS-CN, lambda dado) + q_base (mm, uniforme na bacia)
q_base = V_base / area * 1000;  V_base = kb * Qb_inicio * duracao * 3600
kb e ajustado SEM o evento avaliado (leave-one-out), com Qb_inicio e duracao da planilha.
Depois pr, E_unit, c e as metricas de SY (c tambem leave-one-out).
"""
import os
import sys

import numpy as np
import pandas as pd
from osgeo import gdal

gdal.UseExceptions()
sys.stdout.reconfigure(encoding="utf-8")
BASE = r"C:\TCC"; DI = os.path.join(BASE, "Dados Iniciais")
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
o = gdal.Warp("", gdal.Open(os.path.join(DI, "S - Seco.tif")), format="MEM", width=nx, height=ny,
              outputBounds=(gt[0], gt[3] + ny * gt[5], gt[0] + nx * gt[1], gt[3]), dstSRS=ds0.GetProjection(),
              resampleAlg=gdal.GRA_NearestNeighbour)
S = o.GetRasterBand(1).ReadAsArray().astype(np.float64); S = np.where(S > -1e30, S, np.nan)
mq = np.isfinite(S); valido = mq & np.isfinite(K) & np.isfinite(C) & np.isfinite(LS)
area_bacia = valido.sum() * A

ev = pd.read_excel(os.path.join(DI, "eventos_processados_manuais.xlsx"), sheet_name="Sheet1").iloc[:18]
h = pd.read_excel(os.path.join(DI, "Dados_finais_histereses_corrigido.xlsx"), sheet_name="Planilha1").iloc[:, :8]
h.columns = ["Data", "P1", "P2", "Ptot", "Q", "CSS", "Bt", "CSSBt"]; h["Data"] = pd.to_datetime(h["Data"]); h = h.set_index("Data")

N = 17
SY = np.zeros(N); TR = np.zeros(N); BT = np.zeros(N); RI = np.zeros(N); R = np.zeros(N); Qb0 = np.zeros(N); dur = np.zeros(N); P = []
for n in range(1, N + 1):
    r = ev.iloc[0 if n == 1 else n]; w = h.loc[r["Inicio"]:r["Fim"]]
    SY[n - 1] = r["SYY_t"]; TR[n - 1] = r["T_R_m3"]; BT[n - 1] = w.Bt.sum() * 3600
    RI[n - 1] = r["Intensidade_60min_mm/h"]; R[n - 1] = r["Chuva_evento_mm"]; Qb0[n - 1] = r["Qb_inicio"]; dur[n - 1] = r["Duracao_horas"]
    P.append(le(os.path.join(BASE, f"Evento {n}", f"ChuvaIDW{n}.tif"))[0])

x = Qb0 * dur * 3600
den = np.sum((SY - SY.mean()) ** 2)
nse = lambda o_, s_: 1 - np.sum((o_ - s_) ** 2) / np.sum((o_ - o_.mean()) ** 2)

kb_loo = np.array([np.sum(np.delete(x, i) * np.delete(BT, i)) / np.sum(np.delete(x, i) ** 2) for i in range(N)])
print(f"kb (todos os eventos) = {np.sum(x*BT)/np.sum(x**2):.2f} | kb sem cada evento: min={kb_loo.min():.2f} max={kb_loo.max():.2f}")
Vb_loo = kb_loo * x
print(f"vazao de base prevista (LOO) x observada (soma Bt): NSE={nse(BT, Vb_loo):.3f}  erro abs={np.mean(np.abs(100*(Vb_loo-BT)/BT)):.1f}%")
print(f"   (observacao: a duracao usada e a da janela do evento na planilha; ver ressalva no texto)")
print("=" * 100)
print(f"{'lambda':>6} | {'VOLUME TOTAL: erro medio / abs / NSE':>40} | {'SY (previsao pura): NSE in / LOO / erro abs LOO':>50}")
for lam in (0.05, 0.10, 0.15, 0.20):
    Es = np.zeros(N); Vtot = np.zeros(N)
    for i in range(N):
        Qd = np.where(P[i] <= lam * S, 0.0, (P[i] - lam * S) ** 2 / (P[i] + (1 - lam) * S))
        qb = Vb_loo[i] / area_bacia * 1000.0
        Q = Qd + qb
        Vtot[i] = np.nansum(np.where(mq, Q, 0)) / 1000 * 900
        pr = Q / 1000 * A * (RI[i] / R[i]) / 3600
        E = np.where(valido, COEF * np.maximum(Q * pr * A, 0) ** EXPO * K * C * LS, np.nan)
        Es[i] = np.nansum(E)
    c = np.sum(Es * SY) / np.sum(Es ** 2); sim = c * Es
    loo = np.array([np.sum(np.delete(Es, i) * np.delete(SY, i)) / np.sum(np.delete(Es, i) ** 2) * Es[i] for i in range(N)])
    ev_ = 100 * (Vtot - TR) / TR
    print(f"{lam:6.2f} | {ev_.mean():+9.1f}% {np.abs(ev_).mean():8.1f}% {nse(TR, Vtot):8.3f}         | "
          f"{1-np.sum((SY-sim)**2)/den:8.3f} {1-np.sum((SY-loo)**2)/den:8.3f} {np.mean(np.abs(100*(loo-SY)/SY)):8.1f}%")
print("=" * 100)
print("referencia (como esta hoje): previsao pura lambda=0,05 sem base: NSE in 0,371 / LOO 0,282 / erro abs LOO 46,1%")
