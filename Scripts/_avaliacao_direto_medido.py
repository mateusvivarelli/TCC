"""
DESENHO FISICAMENTE MAIS COERENTE (15/10/2026): escoamento DIRETO medido nas encostas x sedimento do escoamento direto.

  Alvo A (coerente): SY_direto_obs = soma[(Q - Bt) * CSS * 3600 / 1e6]  (carga associada ao escoamento direto)
  Alvo B (carga total): SY_obs = soma[Q * CSS * 3600 / 1e6]
  Modelo: SCS-CN (CN-I, lambda 0,20) so da o PADRAO espacial; o total de cada evento e ancorado no escoamento
          direto MEDIDO (V_dir = T_R - soma(Bt)*3600): f = V_dir / V_calc; Q_obs = min(f*Q, P); pr, E_unit como Hao et al.
  Calibracao de c em log; metricas robustas (MedAPE, fator 2, NSE em log, Spearman) em LOO aninhado.
  Referencias: SY = c*V_dir (sem MUSLE), SY = c*chuva.
Atencao: assume que o sedimento do escoamento direto tem a mesma concentracao CSS da hora (aproximacao).
"""
import os
import sys

import numpy as np
import pandas as pd
from osgeo import gdal
from scipy.stats import spearmanr

gdal.UseExceptions()
sys.stdout.reconfigure(encoding="utf-8")
BASE = r"C:\TCC"; DI = os.path.join(BASE, "Dados Iniciais")
COEF, EXPO, N = 11.8, 0.56, 17


def le(p):
    ds = gdal.Open(p); b = ds.GetRasterBand(1)
    a = b.ReadAsArray().astype(np.float64); nd = b.GetNoDataValue()
    ok = np.isfinite(a) & (a > -1e30)
    if nd is not None:
        ok &= a != nd
    return np.where(ok, a, np.nan), ds


K, ds0 = le(os.path.join(DI, "K_raster.tif")); C, _ = le(os.path.join(DI, "C_raster.tif")); LS, _ = le(os.path.join(DI, "LS_moore.tif"))
gt = ds0.GetGeoTransform(); ny, nx = K.shape; A = abs(gt[1] * gt[5])
o = gdal.Warp("", gdal.Open(os.path.join(DI, "S - Seco.tif")), format="MEM", width=nx, height=ny,
              outputBounds=(gt[0], gt[3] + ny * gt[5], gt[0] + nx * gt[1], gt[3]), dstSRS=ds0.GetProjection(), resampleAlg=gdal.GRA_NearestNeighbour)
S = o.GetRasterBand(1).ReadAsArray().astype(np.float64); S = np.where(S > -1e30, S, np.nan)
valido = np.isfinite(S) & np.isfinite(K) & np.isfinite(C) & np.isfinite(LS)
KCLS = (K * C * LS)[valido]; Sv = S[valido]

ev = pd.read_excel(os.path.join(DI, "eventos_processados_manuais.xlsx"), sheet_name="Sheet1").iloc[:18]
h = pd.read_excel(os.path.join(DI, "Dados_finais_histereses_corrigido.xlsx"), sheet_name="Planilha1").iloc[:, :8]
h.columns = ["Data", "P1", "P2", "Ptot", "Q", "CSS", "Bt", "CSSBt"]; h["Data"] = pd.to_datetime(h["Data"]); h = h.set_index("Data")

SYt = np.zeros(N); SYd = np.zeros(N); VD = np.zeros(N); RI = np.zeros(N); R = np.zeros(N); Pv = []
for n in range(1, N + 1):
    r = ev.iloc[0 if n == 1 else n]; w = h.loc[r["Inicio"]:r["Fim"]]
    SYt[n - 1] = r["SYY_t"]; SYd[n - 1] = ((w.Q - w.Bt).clip(lower=0) * w.CSS).sum() * 3600 / 1e6
    VD[n - 1] = ((w.Q - w.Bt).sum()) * 3600; RI[n - 1] = r["Intensidade_60min_mm/h"]; R[n - 1] = r["Chuva_evento_mm"]
    Pv.append(le(os.path.join(BASE, f"Evento {n}", f"ChuvaIDW{n}.tif"))[0][valido])
print(f"carga do escoamento direto / carga total por evento: min {np.min(SYd/SYt):.2f} max {np.max(SYd/SYt):.2f} mediana {np.median(SYd/SYt):.2f}")
print(f"escoamento direto (m3) por evento: min {VD.min():,.0f} max {VD.max():,.0f}")


def esoma(i, lam, V=None):
    p = Pv[i]
    Q = np.where(p <= lam * Sv, 0.0, (p - lam * Sv) ** 2 / (p + (1 - lam) * Sv))
    if V is not None:
        f = V / (Q.sum() / 1000.0 * A)
        Q = np.minimum(f * Q, p)
    pr = Q / 1000.0 * A * (RI[i] / R[i]) / 3600.0
    return np.sum(COEF * np.maximum(Q * pr * A, 0.0) ** EXPO * KCLS)


Edir = np.array([esoma(i, 0.20) for i in range(N)])
Eanc = np.array([esoma(i, 0.20, VD[i]) for i in range(N)])
Eanc05 = np.array([esoma(i, 0.05, VD[i]) for i in range(N)])
ids = np.arange(N)
fit1 = lambda x, y: np.exp(np.mean(np.log(y) - np.log(x)))
nse = lambda o_, s_: 1 - np.sum((o_ - s_) ** 2) / np.sum((o_ - o_.mean()) ** 2)
nse_log = lambda o_, s_: 1 - np.sum((np.log(o_) - np.log(np.clip(s_, 1e-6, None))) ** 2) / np.sum((np.log(o_) - np.log(o_).mean()) ** 2)
ape = lambda o_, s_: 100 * np.abs(s_ - o_) / o_
f2 = lambda o_, s_: 100 * np.mean((s_ / o_ >= 0.5) & (s_ / o_ <= 2.0))


def linha(nome, x, y):
    c = fit1(x, y); sim = c * x
    loo = np.array([fit1(x[ids != i], y[ids != i]) * x[i] for i in range(N)])
    m = ids != 14; s15 = fit1(x[m], y[m]) * x[m]
    return (f"{nome:<56} {nse_log(y, sim):7.3f} {nse_log(y, loo):7.3f} {np.median(ape(y, loo)):7.1f} {ape(y, loo).mean():7.1f} {f2(y, loo):6.0f} "
            f"{spearmanr(y, loo)[0]:8.3f} | {nse(y, sim):7.3f} {nse(y, loo):7.3f} {nse(y[m], s15):8.3f}")


for alvo, y in (("ALVO A (coerente): carga do escoamento direto", SYd), ("ALVO B: carga total (inclui a da vazao de base)", SYt)):
    print("=" * 130)
    print(alvo + " | calibracao em log, LOO aninhado")
    print(f"{'modelo':<56} {'NSElog':>7} {'NSElog':>7} {'MedAPE':>7} {'MAPE':>7} {'fator2':>6} {'Spearman':>8} | {'NSE lin':>7} {'NSE lin':>7} {'NSE lin':>8}")
    print(f"{'':<56} {'in':>7} {'LOO':>7} {'LOO':>7} {'LOO':>7} {'LOO':>6} {'LOO':>8} | {'in':>7} {'LOO':>7} {'sem ev15':>8}")
    print(linha("REF  SY = c*chuva do evento", R, y))
    print(linha("REF  SY = c*escoamento direto medido", VD, y))
    print(linha("MUSLE prevista: so escoamento direto SCS-CN (lambda 0,20)", Edir, y))
    print(linha("MUSLE ancorada no direto MEDIDO (lambda 0,20) [D]", Eanc, y))
    print(linha("MUSLE ancorada no direto MEDIDO (lambda 0,05)", Eanc05, y))
d = ape(SYd, np.array([fit1(Eanc[ids != i], SYd[ids != i]) * Eanc[i] for i in range(N)])) - ape(SYd, np.array([fit1(VD[ids != i], SYd[ids != i]) * VD[i] for i in range(N)]))
rng = np.random.default_rng(1)
bs = np.array([np.median(rng.choice(d, N)) for _ in range(4000)])
print("=" * 130)
print(f"MUSLE ancorada [D] menos SY=c*V_dir (erro % LOO, alvo A): melhora em {np.sum(d<0)} de 17 eventos; mediana {np.median(d):+.1f} pontos; IC95% da mediana [{np.percentile(bs,2.5):+.1f}; {np.percentile(bs,97.5):+.1f}]")
