"""
CN MELHOR? (15/10/2026) Calibra a conversao chuva -> escoamento direto do SCS-CN contra o escoamento direto MEDIDO.

Parametros calibrados: a (escala de S: S' = a*S, a<1 = mais escoamento) e lambda (Ia = lambda*S').
Objetivo: minimos quadrados do log do volume (erro relativo), uma vez por evento retido (LOO aninhado):
para cada evento i, (a, lambda) sao ajustados nos outros 16; depois o modelo B calculado e refeito com esses parametros
(c1 e c2 tambem sem o evento i). Reporta: (1) volume direto previsto; (2) sedimento (modelo B calculado).
"""
import os
import sys

import numpy as np
import pandas as pd
from osgeo import gdal
from scipy.optimize import least_squares
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


K, ds0 = le(os.path.join(DI, "K_raster.tif")); C, _ = le(os.path.join(DI, "C_raster.tif")); LS, _ = le(os.path.join(DI, "LS_raster.tif"))
gt = ds0.GetGeoTransform(); ny, nx = K.shape; A = abs(gt[1] * gt[5])
o = gdal.Warp("", gdal.Open(os.path.join(DI, "S - Seco.tif")), format="MEM", width=nx, height=ny,
              outputBounds=(gt[0], gt[3] + ny * gt[5], gt[0] + nx * gt[1], gt[3]), dstSRS=ds0.GetProjection(), resampleAlg=gdal.GRA_NearestNeighbour)
S = o.GetRasterBand(1).ReadAsArray().astype(np.float64); S = np.where(S > -1e30, S, np.nan)
valido = np.isfinite(S) & np.isfinite(K) & np.isfinite(C) & np.isfinite(LS)
KCLS = (K * C * LS)[valido]; Sv = S[valido]
ev = pd.read_excel(os.path.join(DI, "eventos_processados_manuais.xlsx"), sheet_name="Sheet1").iloc[:18]
h = pd.read_excel(os.path.join(DI, "Dados_finais_histereses_corrigido.xlsx"), sheet_name="Planilha1").iloc[:, :8]
h.columns = ["Data", "P1", "P2", "Ptot", "Q", "CSS", "Bt", "CSSBt"]; h["Data"] = pd.to_datetime(h["Data"]); h = h.set_index("Data")
SY = np.zeros(N); VD = np.zeros(N); RI = np.zeros(N); R = np.zeros(N); Qb0 = np.zeros(N); durR = np.zeros(N); Pv = []
for n in range(1, N + 1):
    r = ev.iloc[0 if n == 1 else n]; w = h.loc[r["Inicio"]:r["Fim"]]
    SY[n - 1] = r["SYY_t"]; VD[n - 1] = (w.Q - w.Bt).sum() * 3600; RI[n - 1] = r["Intensidade_60min_mm/h"]; R[n - 1] = r["Chuva_evento_mm"]
    Qb0[n - 1] = r["Qb_inicio"]; durR[n - 1] = max(r["Tempo_precipitacao_p1_h"], r["Tempo_precipitacao_p2_h"])
    Pv.append(le(os.path.join(BASE, f"Evento {n}", f"ChuvaIDW{n}.tif"))[0][valido])
ids = np.arange(N)


def qpix(i, a, lam):
    s = a * Sv; p = Pv[i]
    return np.where(p <= lam * s, 0.0, (p - lam * s) ** 2 / (p + (1 - lam) * s))


# tabela de volumes por (a, lambda)
AS = np.exp(np.linspace(np.log(0.05), np.log(2.0), 36)); LAMS = np.linspace(0.02, 0.40, 20)
Vtab = np.zeros((len(AS), len(LAMS), N))
for ia, a in enumerate(AS):
    for il, lam in enumerate(LAMS):
        for i in range(N):
            Vtab[ia, il, i] = qpix(i, a, lam).sum() / 1000.0 * A
print("tabela de volumes pronta")


def melhor(mask):
    err = (np.log(np.clip(Vtab[:, :, mask], 1.0, None)) - np.log(VD[mask])) ** 2
    tot = err.sum(axis=2); ia, il = np.unravel_index(np.argmin(tot), tot.shape); return AS[ia], LAMS[il]


a_all, l_all = melhor(np.ones(N, bool))
print(f"calibracao em todos os eventos: a = {a_all:.3f} (S' = a*S; CN equivalente mais alto) , lambda = {l_all:.2f}")
ape = lambda o_, s_: 100 * np.abs(s_ - o_) / o_
nse = lambda o_, s_: 1 - np.sum((o_ - s_) ** 2) / np.sum((o_ - o_.mean()) ** 2)
nlog = lambda y, s: 1 - np.sum((np.log(y) - np.log(np.clip(s, 1e-6, None))) ** 2) / np.sum((np.log(y) - np.log(y).mean()) ** 2)
f2 = lambda y, s: 100 * np.mean((s / y >= 0.5) & (s / y <= 2.0))

# ---- (1) volume direto previsto, LOO
Vloo = np.zeros(N); par = []
for i in range(N):
    m = ids != i; a, lam = melhor(m); par.append((a, lam)); Vloo[i] = qpix(i, a, lam).sum() / 1000.0 * A
V020 = Vtab[np.argmin(np.abs(AS - 1.0)), np.argmin(np.abs(LAMS - 0.20)), :]
print("=" * 112)
print("(1) VOLUME DE ESCOAMENTO DIRETO PREVISTO x MEDIDO (LOO aninhado)")
print(f"  SCS-CN original (a=1, lambda 0,20): erro mediano {np.median(ape(VD, V020)):.0f}% | NSE {nse(VD, V020):.2f} | dentro de fator 2: {f2(VD, V020):.0f}% | Spearman {spearmanr(VD, V020)[0]:.2f}")
print(f"  SCS-CN calibrado (a e lambda)     : erro mediano {np.median(ape(VD, Vloo)):.0f}% | NSE {nse(VD, Vloo):.2f} | dentro de fator 2: {f2(VD, Vloo):.0f}% | Spearman {spearmanr(VD, Vloo)[0]:.2f}")
Xm = np.column_stack([np.ones(N), np.log(R)]); Vreg = np.zeros(N)
for i in range(N):
    m = ids != i; b = np.linalg.lstsq(Xm[m], np.log(VD[m]), rcond=None)[0]; Vreg[i] = np.exp(Xm[i] @ b)
print(f"  regressao log-log na chuva        : erro mediano {np.median(ape(VD, Vreg)):.0f}% | NSE {nse(VD, Vreg):.2f} | dentro de fator 2: {f2(VD, Vreg):.0f}% | Spearman {spearmanr(VD, Vreg)[0]:.2f}")
print(f"  parametros ajustados por evento retido: a de {min(p[0] for p in par):.2f} a {max(p[0] for p in par):.2f}; lambda de {min(p[1] for p in par):.2f} a {max(p[1] for p in par):.2f}")


# ---- (2) sedimento: modelo B calculado com o escoamento calibrado (aninhado)
def fit2(x1, x2, y):
    f = lambda p: np.log(np.clip(p[0] * x1 + p[1] * x2, 1e-9, None)) - np.log(y)
    best = None
    for s0 in ([y.mean() / x1.mean(), 0.0], [0.0, y.mean() / x2.mean()], [0.5 * y.mean() / x1.mean(), 0.5 * y.mean() / x2.mean()]):
        r = least_squares(f, s0, bounds=(0, np.inf), x_scale="jac")
        if best is None or r.cost < best.cost: best = r
    return best.x


def esoma(i, a, lam):
    Q = qpix(i, a, lam); pr = Q / 1000.0 * A * (RI[i] / R[i]) / 3600.0
    return np.sum(COEF * np.maximum(Q * pr * A, 0.0) ** EXPO * KCLS)


base = Qb0 * durR * 3600.0
loo = np.zeros(N); share = []
for i in range(N):
    a, lam = par[i]; E = np.array([esoma(j, a, lam) for j in range(N)]); m = ids != i
    p = fit2(E[m], base[m], SY[m]); loo[i] = p[0] * E[i] + p[1] * base[i]; share.append(100 * p[0] * E[i] / loo[i])
E20 = np.array([esoma(i, 1.0, 0.20) for i in range(N)]); loo20 = np.array([(lambda p: p[0] * E20[i] + p[1] * base[i])(fit2(E20[ids != i], base[ids != i], SY[ids != i])) for i in range(N)])
Ec = np.array([esoma(i, a_all, l_all) for i in range(N)]); pc = fit2(Ec, base, SY); simc = pc[0] * Ec + pc[1] * base
ch = np.array([np.exp(np.mean(np.log(SY[ids != i]) - np.log(R[ids != i]))) * R[i] for i in range(N)])
print("=" * 112)
print("(2) SEDIMENTO, MODELO B calculado (carga total; calibracao em log; LOO aninhado, inclusive a e lambda)")
print(f"{'modelo':<54} {'MedAPE':>7} {'fator2':>7} {'NSE-log':>8} {'Spearman':>8} | parcela das encostas (mediana)")
print(f"{'B com SCS-CN original (a=1, lambda 0,20)':<54} {np.median(ape(SY, loo20)):7.1f} {f2(SY, loo20):7.0f} {nlog(SY, loo20):8.3f} {spearmanr(SY, loo20)[0]:8.3f} | 10%")
print(f"{'B com SCS-CN calibrado (a e lambda)':<54} {np.median(ape(SY, loo)):7.1f} {f2(SY, loo):7.0f} {nlog(SY, loo):8.3f} {spearmanr(SY, loo)[0]:8.3f} | {np.median(share):.0f}%")
print(f"{'referencia: SY = c * chuva':<54} {np.median(ape(SY, ch)):7.1f} {f2(SY, ch):7.0f} {nlog(SY, ch):8.3f} {spearmanr(SY, ch)[0]:8.3f} |")
print("=" * 112)
