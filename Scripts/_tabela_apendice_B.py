"""
O modelo B funcionaria bem se o Q calculado a partir da chuva fosse bom? (15/10/2026)

'Q bom' = escoamento direto MEDIDO distribuido no espaco pelo padrao do SCS-CN (como no desenho D).
Modelos (alvo: carga TOTAL SY_obs; c1,c2 em log; LOO aninhado):
  B   : c1*E(Q direto previsto SCS-CN) + c2*Qb_inicio*duracao_chuva*3600        [adotado antes]
  B_Q : c1*E(Q direto 'bom')            + c2*Qb_inicio*duracao_chuva*3600        [so o Q melhora]
  B_Q+base observada: c1*E(Q 'bom') + c2*soma(Bt)*3600                             [Q e base 'bons'; diagnostico]
  D   : c*E(Q 'bom') sem termo de base
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
SY = np.zeros(N); VD = np.zeros(N); BTV = np.zeros(N); RI = np.zeros(N); R = np.zeros(N); Qb0 = np.zeros(N); durR = np.zeros(N); Pv = []
for n in range(1, N + 1):
    r = ev.iloc[0 if n == 1 else n]; w = h.loc[r["Inicio"]:r["Fim"]]
    SY[n - 1] = r["SYY_t"]; VD[n - 1] = (w.Q - w.Bt).sum() * 3600; BTV[n - 1] = w.Bt.sum() * 3600
    RI[n - 1] = r["Intensidade_60min_mm/h"]; R[n - 1] = r["Chuva_evento_mm"]; Qb0[n - 1] = r["Qb_inicio"]
    durR[n - 1] = max(r["Tempo_precipitacao_p1_h"], r["Tempo_precipitacao_p2_h"])
    Pv.append(le(os.path.join(BASE, f"Evento {n}", f"ChuvaIDW{n}.tif"))[0][valido])


def esoma(i, lam, V=None):
    p = Pv[i]; Q = np.where(p <= lam * Sv, 0.0, (p - lam * Sv) ** 2 / (p + (1 - lam) * Sv))
    if V is not None:
        Q = np.minimum(V / (Q.sum() / 1000.0 * A) * Q, p)
    pr = Q / 1000.0 * A * (RI[i] / R[i]) / 3600.0
    return np.sum(COEF * np.maximum(Q * pr * A, 0.0) ** EXPO * KCLS)


ids = np.arange(N)
fit1 = lambda x, y: np.exp(np.mean(np.log(y) - np.log(x)))


def fit2(x1, x2, y):
    f = lambda p: np.log(np.clip(p[0] * x1 + p[1] * x2, 1e-9, None)) - np.log(y)
    best = None
    for s0 in ([y.mean() / x1.mean(), 0.0], [0.0, y.mean() / x2.mean()], [0.5 * y.mean() / x1.mean(), 0.5 * y.mean() / x2.mean()]):
        r = least_squares(f, s0, bounds=(0, np.inf), x_scale="jac")
        if best is None or r.cost < best.cost: best = r
    return best.x


nse = lambda o_, s_: 1 - np.sum((o_ - s_) ** 2) / np.sum((o_ - o_.mean()) ** 2)
nse_log = lambda o_, s_: 1 - np.sum((np.log(o_) - np.log(np.clip(s_, 1e-6, None))) ** 2) / np.sum((np.log(o_) - np.log(o_).mean()) ** 2)
ape = lambda o_, s_: 100 * np.abs(s_ - o_) / o_
f2 = lambda o_, s_: 100 * np.mean((s_ / o_ >= 0.5) & (s_ / o_ <= 2.0))


def roda(nome, x1, x2=None):
    if x2 is None:
        sim = fit1(x1, SY) * x1; loo = np.array([fit1(x1[ids != i], SY[ids != i]) * x1[i] for i in range(N)]); par = ""
    else:
        p = fit2(x1, x2, SY); sim = p[0] * x1 + p[1] * x2
        loo = np.zeros(N)
        for i in range(N):
            m = ids != i; pi = fit2(x1[m], x2[m], SY[m]); loo[i] = pi[0] * x1[i] + pi[1] * x2[i]
        par = f"parcela das encostas (mediana) = {np.median(100*p[0]*x1/sim):.0f}%"
    print(f"{nome:<62} {nse_log(SY, sim):7.3f} {nse_log(SY, loo):7.3f} {np.median(ape(SY, loo)):7.1f} {ape(SY, loo).mean():7.1f} {f2(SY, loo):6.0f} {spearmanr(SY, loo)[0]:8.3f} | {nse(SY, sim):7.3f} {nse(SY, loo):7.3f}  {par}")


base_chuva = Qb0 * durR * 3600.0
E_prev05 = pd.read_csv(os.path.join(DI, "comparacao_SY_previsao_vs_restrito.csv")).sort_values("evento").soma_E_unit_previsao_t.to_numpy(float)
E20 = np.array([esoma(i, 0.20) for i in range(N)]); E_bom = np.array([esoma(i, 0.20, VD[i]) for i in range(N)])
TRv = VD + BTV
V_ = np.array([float(ev.iloc[0 if n == 1 else n]["T_R_m3"]) for n in range(1, N + 1)]); QPm = np.array([float(ev.iloc[0 if n == 1 else n]["Q_pico"]) for n in range(1, N + 1)])
KLSC = 0.031 * 0.536 * 0.267


def nse_lin(y, s): return 1 - np.sum((y - s) ** 2) / np.sum((y - y.mean()) ** 2)


def avalia(nome, kind, xs):
    """kind: 'scale' | 'two' | 'power'. calibracao em LOG; devolve NSE linear in-sample, LOO e sem o evento 15 (c refeito)"""
    def pred(m, mask_pred=None):
        if kind == "scale":
            c = np.exp(np.mean(np.log(SY[m]) - np.log(xs[0][m]))); return lambda idx: c * xs[0][idx]
        if kind == "two":
            p = fit2(xs[0][m], xs[1][m], SY[m]); return lambda idx: p[0] * xs[0][idx] + p[1] * xs[1][idx]
        b, a = np.polyfit(np.log(xs[0][m]), np.log(SY[m] / KLSC), 1); return lambda idx: np.exp(a) * xs[0][idx] ** b * KLSC
    todos = np.ones(N, bool); sim = pred(todos)(ids)
    loo = np.array([pred(ids != i)(np.array([i]))[0] for i in range(N)])
    m15 = ids != 14; s15 = pred(m15)(ids[m15])
    print(f"| {nome} | {nse_lin(SY, sim):.2f} | {nse_lin(SY, loo):.2f} | {nse_lin(SY[m15], s15):.2f} |")


print("| Modelo | NSE (ajuste) | NSE (validacao cruzada) | NSE sem o evento 15 |")
avalia("SY = c · chuva do evento", "scale", [R])
avalia("SY = c · volume total medido", "scale", [V_])
avalia("Previsao pura anterior (lambda 0,05, sem base)", "scale", [E_prev05])
avalia("Modelo B, N1", "two", [E20, base_chuva])
avalia("Modelo B, N3", "two", [E_bom, base_chuva])
avalia("Modelo B, N4", "two", [E_bom, BTV])
avalia("IC refeita (concentrada)", "power", [V_ * QPm])
