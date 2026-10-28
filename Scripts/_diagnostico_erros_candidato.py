"""De onde vem o erro do modelo candidato (CN-I, lambda 0,05, S convertido): agua x sedimento por unidade de agua (27/10/2026)."""
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



# ===================== DE ONDE VEM O ERRO DO CANDIDATO (27/10/2026) =====================
from scipy.stats import spearmanr
cd = pd.read_csv(os.path.join(DI, "comparacao_SY_lambda005_woodward.csv")).sort_values("evento")
obs = cd.SY_obs_t.to_numpy(); mc = cd.SY_calc_LOO_t.to_numpy(); mf = cd.SY_forc_LOO_t.to_numpy(); vdl = cd.SY_Vdir_LOO_t.to_numpy()
rv = cd.V_dir_SCS_m3.to_numpy() / cd.V_dir_medido_m3.to_numpy()
emc, emf, evd = np.log(mc / obs), np.log(mf / obs), np.log(vdl / obs)

print("=== 1. MODELO CALCULADO: o erro e a agua? ===")
print(f"r entre log(erro do MC) e log(volume SCS / medido): {np.corrcoef(emc, np.log(rv))[0,1]:.2f}")
b = np.polyfit(np.log(rv), emc, 1)
print(f"inclinacao: log(erro MC) = {b[0]:.2f} * log(volume SCS/medido) + {b[1]:.2f}   (1,12 seria so a agua, pela potencia de Q)")
res = emc - np.polyval(b, np.log(rv))
print(f"variancia do log(erro MC): {emc.var():.3f}; explicada pela agua: {100*(1-res.var()/emc.var()):.0f}%")

print("\n=== 2. MODELO FORCADO: o que sobra com a agua certa ===")
print(f"r entre erro do MFM e erro de SY = c*V_dir (mesma agua, sem MUSLE): {np.corrcoef(emf, evd)[0,1]:.2f}")
print(f"variancia do log(erro): MFM {emf.var():.3f} | c*V_dir {evd.var():.3f} | diferenca MFM - c*V_dir {np.var(emf-evd):.3f}")

# concentracao media de sedimento do escoamento direto: o que a agua sozinha nao explica
conc = obs / cd.V_dir_medido_m3.to_numpy() * 1e6   # g/m3 = mg/L equivalente (t / m3 * 1e6)
datas, durR_, RI_, R_, Qb_, Qpd, P5 = [], [], [], [], [], [], []
for n in range(1, N + 1):
    r = ev.iloc[0 if n == 1 else n]; t0 = pd.to_datetime(r["Inicio"]); w = h.loc[r["Inicio"]:r["Fim"]]
    ant = h.loc[t0 - pd.Timedelta(hours=120): t0 - pd.Timedelta(hours=1)]
    datas.append(t0); P5.append(float((0.307 * ant.P1.fillna(0) + 0.693 * ant.P2.fillna(0)).sum()))
    Qpd.append(float((w.Q - w.Bt).max()))
datas = pd.to_datetime(pd.Series(datas))
dias_desde_anterior = np.r_[np.nan, np.diff(datas.values).astype("timedelta64[h]").astype(float) / 24.0]
chuva_ant30 = []
for n, t0 in enumerate(datas):
    ant = h.loc[t0 - pd.Timedelta(days=30): t0 - pd.Timedelta(hours=1)]
    chuva_ant30.append(float((0.307 * ant.P1.fillna(0) + 0.693 * ant.P2.fillna(0)).sum()))
mes = np.array([d.month for d in datas]); estacao = np.array([((m - 10) % 12) for m in mes])   # meses desde outubro
dfx = pd.DataFrame(dict(conc=conc, erro_MFM=emf, erro_cVdir=evd, R=RI * 0 + R, RI=RI, RI_R=RI / R, P5=P5, chuva_30d=chuva_ant30,
                        Qb_inicio=Qb0, dur_chuva=durR, pico_dir=Qpd, pico_sobre_vol=np.array(Qpd) / VD, dias_desde_anterior=dias_desde_anterior,
                        meses_desde_out=estacao))
print("\nconcentracao media de sedimento no escoamento direto, por evento (mg/L):", " ".join(f"{c:.0f}" for c in conc))
print("\nSpearman com: log(concentracao) | erro do MFM | erro de c*V_dir")
for col in ("R", "RI", "RI_R", "P5", "chuva_30d", "Qb_inicio", "dur_chuva", "pico_dir", "pico_sobre_vol", "dias_desde_anterior", "meses_desde_out"):
    m = np.isfinite(dfx[col].to_numpy())
    a1 = spearmanr(np.log(dfx.conc[m]), dfx[col][m])[0]; a2 = spearmanr(dfx.erro_MFM[m], dfx[col][m])[0]; a3 = spearmanr(dfx.erro_cVdir[m], dfx[col][m])[0]
    print(f"  {col:<22} {a1:+.2f} | {a2:+.2f} | {a3:+.2f}")
print("\nerros por evento (%), MFM | c*V_dir:")
for i in range(N):
    print(f"  ev {i+1:>2} ({datas[i].strftime('%d/%m/%y')}): MFM {100*(mf[i]/obs[i]-1):+5.0f} | c*V_dir {100*(vdl[i]/obs[i]-1):+5.0f} | conc {conc[i]:5.0f} mg/L | dias desde o anterior {dias_desde_anterior[i]:5.1f}")
