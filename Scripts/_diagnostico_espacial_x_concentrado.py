"""Por que o MFM (espacializado) fica abaixo da IC (concentrada)? Escada de diferencas IC -> MFM, fator de
concentracao espacial, fracao do volume em pixels sem erosao e teste de forcar tambem o pico (27/10/2026)."""
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
COEF, EXPO, LAM, N = 11.8, 0.56, 0.20, 17
rng = np.random.default_rng(15102026)


def le(p):
    ds = gdal.Open(p); b = ds.GetRasterBand(1)
    a = b.ReadAsArray().astype(np.float64); nd = b.GetNoDataValue()
    ok = np.isfinite(a) & (a > -1e30)
    if nd is not None:
        ok &= a != nd
    return np.where(ok, a, np.nan), ds


def salva(caminho, arr, ref_ds, nodata=-9999.0):
    out = gdal.GetDriverByName("GTiff").Create(caminho, arr.shape[1], arr.shape[0], 1, gdal.GDT_Float32)
    out.SetGeoTransform(ref_ds.GetGeoTransform()); out.SetProjection(ref_ds.GetProjection())
    b = out.GetRasterBand(1); b.WriteArray(np.where(np.isfinite(arr), arr, nodata).astype(np.float32)); b.SetNoDataValue(nodata)
    b.FlushCache(); out = None


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

SY = np.zeros(N); TR = np.zeros(N); BTV = np.zeros(N); RI = np.zeros(N); R = np.zeros(N); Qb0 = np.zeros(N); durH = np.zeros(N); durR = np.zeros(N)
Pv = []
for n in range(1, N + 1):
    r = ev.iloc[0 if n == 1 else n]; w = h.loc[r["Inicio"]:r["Fim"]]
    SY[n - 1] = r["SYY_t"]; TR[n - 1] = r["T_R_m3"]; BTV[n - 1] = w.Bt.sum() * 3600
    RI[n - 1] = r["Intensidade_60min_mm/h"]; R[n - 1] = r["Chuva_evento_mm"]; Qb0[n - 1] = r["Qb_inicio"]
    durH[n - 1] = r["Duracao_horas"]; durR[n - 1] = max(r["Tempo_precipitacao_p1_h"], r["Tempo_precipitacao_p2_h"])
    Pv.append(le(os.path.join(BASE, f"Evento {n}", f"ChuvaIDW{n}.tif"))[0][valido])
VD = TR - BTV
print(f"duracao da chuva (h): min={durR.min():.0f} max={durR.max():.0f} | duracao da janela (h): min={durH.min():.0f} max={durH.max():.0f} | r(durR, durH)={np.corrcoef(durR, durH)[0,1]:.2f}")


def qdir(i, lam=LAM):
    p = Pv[i]
    return np.where(p <= lam * Sv, 0.0, (p - lam * Sv) ** 2 / (p + (1 - lam) * Sv))


def edir(i, lam=LAM):
    Q = qdir(i, lam); pr = Q / 1000.0 * A * (RI[i] / R[i]) / 3600.0
    return np.sum(COEF * np.maximum(Q * pr * A, 0.0) ** EXPO * KCLS)


E05 = np.array([edir(i, 0.05) for i in range(N)])
E20 = np.array([edir(i, 0.20) for i in range(N)])
X2 = {"chuva": Qb0 * durR * 3600.0, "hidrograma": Qb0 * durH * 3600.0, "observada": BTV}


def fit2(x1, x2, y):
    f = lambda p: np.log(np.clip(p[0] * x1 + p[1] * x2, 1e-9, None)) - np.log(y)
    best = None
    for s0 in ([y.mean() / x1.mean(), 0.0], [0.0, y.mean() / x2.mean()], [0.5 * y.mean() / x1.mean(), 0.5 * y.mean() / x2.mean()]):
        r = least_squares(f, s0, bounds=(0, np.inf), x_scale="jac")
        if best is None or r.cost < best.cost:
            best = r
    return best.x


def fit1(x, y):
    return np.exp(np.mean(np.log(y) - np.log(x)))


ids = np.arange(N)
QPm = np.array([float(ev.iloc[0 if n == 1 else n]["Q_pico"]) for n in range(1, N + 1)])
ape = lambda s_: 100 * np.abs(s_ - SY) / SY
f2 = lambda s_: 100 * np.mean((s_ / SY >= 0.5) & (s_ / SY <= 2.0))
nlog = lambda s_: 1 - np.sum((np.log(SY) - np.log(s_)) ** 2) / np.sum((np.log(SY) - np.log(SY).mean()) ** 2)
nlin = lambda s_: 1 - np.sum((SY - s_) ** 2) / np.sum((SY - SY.mean()) ** 2)

def loo_escala(x):
    return np.array([fit1(x[ids != i], SY[ids != i]) * x[i] for i in range(N)])

def loo_potencia(x):
    out = np.zeros(N)
    for i in range(N):
        m = ids != i; b, a = np.polyfit(np.log(x[m]), np.log(SY[m]), 1); out[i] = np.exp(a) * x[i] ** b
    return out

def esoma(i, lam, V):
    p = Pv[i]; Q = qdir(i, lam); Q = np.minimum(V / (Q.sum() / 1000.0 * A) * Q, p)
    pr = Q / 1000.0 * A * (RI[i] / R[i]) / 3600.0
    return np.sum(COEF * np.maximum(Q * pr * A, 0.0) ** EXPO * KCLS), Q

E20, Q20 = zip(*[esoma(i, 0.20, VD[i]) for i in range(N)]); E20 = np.array(E20)
E05, Q05 = zip(*[esoma(i, 0.05, VD[i]) for i in range(N)]); E05 = np.array(E05)
qp_proxy = VD * (RI / R) / 3600.0
passos = [
    ("1 IC: alfa*(T_R*qp_medido)^beta, beta livre", loo_potencia(TR * QPm)),
    ("2 expoente fixo 0,56: c*(T_R*qp_medido)^0,56", loo_escala((TR * QPm) ** 0.56)),
    ("3 volume direto: c*(V_dir*qp_medido)^0,56", loo_escala((VD * QPm) ** 0.56)),
    ("4 pico estimado da chuva: c*(V_dir*V_dir*RI/R)^0,56", loo_escala((VD * qp_proxy) ** 0.56)),
    ("5 espacial, padrao lambda 0,05 (agua medida)", loo_escala(E05)),
    ("6 espacial, padrao lambda 0,20 = MFM adotado", loo_escala(E20)),
]
print(f"{'passo':<56} {'MedAPE':>7} {'fator2':>6} {'NSElog':>7} {'NSElin':>7}")
for nome, s_ in passos:
    print(f"{nome:<56} {np.median(ape(s_)):7.1f} {f2(s_):6.0f} {nlog(s_):7.2f} {nlin(s_):7.2f}")

# fator de concentracao espacial: quanto a soma de Q^1,12 difere da agua espalhada por igual
def conc(Qs):
    return np.array([np.sum(np.clip(q, 0, None) ** 1.12) / (q.size * np.mean(q) ** 1.12) for q in Qs])
F20, F05 = conc(Q20), conc(Q05)
print(f"\nfator de concentracao (sum Q^1,12 / agua uniforme): lambda 0,20: {F20.min():.2f} a {F20.max():.2f} (razao max/min {F20.max()/F20.min():.1f}x) | "
      f"lambda 0,05: {F05.min():.2f} a {F05.max():.2f} ({F05.max()/F05.min():.1f}x)")
frac0 = np.array([np.mean(q <= 1e-9) for q in Q20])
print("pixels sem escoamento (lambda 0,20) por evento:", " ".join(f"{100*v:.0f}%" for v in frac0))
print("fator lambda 0,20 por evento:               ", " ".join(f"{v:.1f}" for v in F20))
e4 = np.log(passos[3][1] / SY); e6 = np.log(passos[5][1] / SY)
print(f"correlacao entre log(F20) e o erro que a espacializacao acrescenta (log MFM - log passo 4): {np.corrcoef(np.log(F20), e6 - e4)[0,1]:.2f}")
print(f"correlacao entre chuva do evento e log(F20): {np.corrcoef(R, np.log(F20))[0,1]:.2f}")
Cv = C[valido]; Kv = K[valido]
zero = (Cv == 0) | (Kv == 0)
print(f"\npixels com erosao impossivel (C = 0 ou K = 0: urbano/agua): {100*zero.mean():.1f}% da bacia")
for lam, Qs in (("0,20", Q20), ("0,05", Q05)):
    fr = np.array([q[zero].sum() / q.sum() for q in Qs])
    print(f"lambda {lam}: % do volume medido que cai em pixels sem erosao, por evento: " + " ".join(f"{100*v:.0f}" for v in fr))
mfm = passos[5][1]
print("erro MFM (LOO) por evento:                                    " + " ".join(f"{100*(m-o)/o:+.0f}" for m, o in zip(mfm, SY)))
print("chuva do evento (mm):                                         " + " ".join(f"{v:.0f}" for v in R))
fr20 = np.array([q[zero].sum() / q.sum() for q in Q20])
print(f"correlacao: % do volume em pixels sem erosao x log(MFM/medido) = {np.corrcoef(fr20, np.log(mfm/SY))[0,1]:.2f}")

# ---- forcar tambem o pico: pr_k = Q_k*A/1000 * (qp_med/V_dir)  =>  sum_k pr_k = qp_med
qp_dir = np.zeros(N); qp_tot = np.zeros(N)
for n in range(1, N + 1):
    r = ev.iloc[0 if n == 1 else n]; w = h.loc[r["Inicio"]:r["Fim"]]
    qp_dir[n - 1] = (w.Q - w.Bt).max(); qp_tot[n - 1] = w.Q.max()
fator_chuva = (RI / R) / 3600.0
print(f"\npico direto medido / pico total medido: {np.median(qp_dir/qp_tot):.2f} (mediana)")
print(f"razao pico/volume: medida (direto) x estimada pela chuva, por evento: " + " ".join(f"{(q/v)/fc:.2f}" for q, v, fc in zip(qp_dir, VD, fator_chuva)))
print(f"\n{'variante (agua medida em tudo)':<58} {'MedAPE':>7} {'fator2':>6} {'NSElog':>7} {'NSElin':>7}")
for lam, E in (("0,20", E20), ("0,05", E05)):
    for nome, qp in (("pico do escoamento direto medido", qp_dir), ("pico total medido", qp_tot)):
        Eq = E * ((qp / VD) / fator_chuva) ** EXPO
        s_ = loo_escala(Eq)
        print(f"{'MFM lambda ' + lam + ', volume e ' + nome:<58} {np.median(ape(s_)):7.1f} {f2(s_):6.0f} {nlog(s_):7.2f} {nlin(s_):7.2f}")
    s_ = loo_escala(E); print(f"{'MFM lambda ' + lam + ', so o volume (pico da chuva)':<58} {np.median(ape(s_)):7.1f} {f2(s_):6.0f} {nlog(s_):7.2f} {nlin(s_):7.2f}")
