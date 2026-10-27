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
fit_lin = lambda x, y: np.sum(x * y) / np.sum(x * x)
ape = lambda s_: 100 * np.abs(s_ - SY) / SY
f2 = lambda s_: 100 * np.mean((s_ / SY >= 0.5) & (s_ / SY <= 2.0))
nlog = lambda s_: 1 - np.sum((np.log(SY) - np.log(np.clip(s_, 1e-9, None))) ** 2) / np.sum((np.log(SY) - np.log(SY).mean()) ** 2)
nlin = lambda o, s_: 1 - np.sum((o - s_) ** 2) / np.sum((o - o.mean()) ** 2)

def cn_para_S(arquivo):
    w = gdal.Warp("", gdal.Open(os.path.join(DI, arquivo)), format="MEM", width=nx, height=ny,
                  outputBounds=(gt[0], gt[3] + ny * gt[5], gt[0] + nx * gt[1], gt[3]), dstSRS=ds0.GetProjection(), resampleAlg=gdal.GRA_NearestNeighbour)
    cn = w.GetRasterBand(1).ReadAsArray().astype(np.float64)[valido]
    return 25.4 * (1000.0 / cn - 10.0), cn

S1 = Sv
S2, cn2 = cn_para_S("CN TCC.tif")
S3, cn3 = cn_para_S("CN TCC - Úmido.tif")

conv = lambda Sx: 1.33 * (Sx / 25.4) ** 1.15 * 25.4
AMC = ["II", "I", "I", "III", "I", "I", "I", "I", "I", "I", "I", "I", "I", "III", "I", "III", "I"]   # NEH-4, estacao de crescimento
SS = {"I": conv(S1), "II": conv(S2), "III": conv(S3)}

def campos(i, Sx, lam=0.05, V=None):
    p = Pv[i]; Q = np.where(p <= lam * Sx, 0.0, (p - lam * Sx) ** 2 / (p + (1 - lam) * Sx))
    vol = Q.sum() / 1000.0 * A
    if V is not None:
        Q = np.minimum(V / vol * Q, p)
    pr = Q / 1000.0 * A * (RI[i] / R[i]) / 3600.0
    return np.sum(COEF * np.maximum(Q * pr * A, 0.0) ** EXPO * KCLS), vol

print(f"{'cenario (lambda 0,05, S convertido)':<44} {'vol SCS/med':>11} {'vies':>6} {'NSE vol':>8} | {'MC MedAPE':>9} {'f2':>4} {'NSElog':>7} | {'MFM MedAPE':>10} {'f2':>4} {'NSElog':>7}")
for nome, esc in (("CN-I em todos os eventos", lambda i: SS["I"]), ("AMC de cada evento (regra NEH-4)", lambda i: SS[AMC[i]])):
    r = [campos(i, esc(i)) for i in range(N)]; Ec = np.array([a for a, _ in r]); Vc = np.array([b for _, b in r])
    Ef = np.array([campos(i, esc(i), V=VD[i])[0] for i in range(N)])
    mc = np.array([fit1(Ec[ids != i], SY[ids != i]) * Ec[i] for i in range(N)])
    mf = np.array([fit1(Ef[ids != i], SY[ids != i]) * Ef[i] for i in range(N)])
    print(f"{nome:<44} {np.median(Vc/VD):11.2f} {100*(Vc.sum()/VD.sum()-1):+5.0f}% {nlin(VD, Vc):8.2f} | {np.median(ape(mc)):9.1f} {f2(mc):4.0f} {nlog(mc):7.2f} | {np.median(ape(mf)):10.1f} {f2(mf):4.0f} {nlog(mf):7.2f}")
    if "cada" in nome:
        for i in (0, 3, 13, 15):
            print(f"   evento {i+1:>2} (AMC {AMC[i]:>3}): volume SCS/medido = {Vc[i]/VD[i]:.2f} | erro MC {100*(mc[i]-SY[i])/SY[i]:+.0f}%")
    else:
        for i in (0, 3, 13, 15):
            print(f"   evento {i+1:>2} (CN-I):     volume SCS/medido = {Vc[i]/VD[i]:.2f} | erro MC {100*(mc[i]-SY[i])/SY[i]:+.0f}%")
