"""
CONFIGURACAO CANDIDATA (27/10/2026, ainda NAO adotada): MUSLE espacializada so com escoamento direto, com
lambda = 0,05 e a retencao convertida pela relacao de Woodward et al. (2003):
    S_0,05 = 1,33 * S_0,20 ^ 1,15   (S em polegadas)  ->  aqui em mm: 25,4 * 1,33 * (S/25,4) ^ 1,15
aplicada ao S do CN-I (AMC I, condicao representativa: 13 de 17 eventos pela regra de 5 dias do NEH-4).
Mesmo desenho do calcular_sy_so_direto.py (MC: Q do SCS-CN; MFM: Q reescalado ao escoamento direto medido;
SY = c * soma E_unit; c em log; LOO). Alvo: carga total.

Saidas (sufixo _l05w, nao sobrescreve o modelo adotado _sd): Evento n/{Qdir,pr,E_unit,SY}{n}_l05w.tif;
Dados Iniciais/SY_medio_eventos_l05w.tif, SY_medio_eventos_forcado_l05w.tif, comparacao_SY_lambda005_woodward.csv.
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



# ---------------------------------------------------------------- configuracao candidata (27/10/2026)
S_020 = Sv.copy()                                   # S do CN-I para lambda 0,20 (configuracao adotada)
Sv = 25.4 * 1.33 * (S_020 / 25.4) ** 1.15           # Woodward et al. (2003)
LAM = 0.05
E_ad = E20.copy()                                   # E do MC na configuracao adotada (lambda 0,20), para comparacao
E20 = np.array([edir(i, LAM) for i in range(N)])    # nome mantido: E do MC na configuracao candidata


ids = np.arange(N)
nse = lambda o_, s_: 1 - np.sum((o_ - s_) ** 2) / np.sum((o_ - o_.mean()) ** 2)
nse_log = lambda o_, s_: 1 - np.sum((np.log(o_) - np.log(np.clip(s_, 1e-6, None))) ** 2) / np.sum((np.log(o_) - np.log(o_).mean()) ** 2)
ape = lambda o_, s_: 100 * np.abs(s_ - o_) / o_
f2 = lambda o_, s_: 100 * np.mean((s_ / o_ >= 0.5) & (s_ / o_ <= 2.0))
fit_lin = lambda x, y: np.sum(x * y) / np.sum(x * x)
QPm = np.array([float(ev.iloc[0 if n == 1 else n]["Q_pico"]) for n in range(1, N + 1)])


def campos(i, lam=LAM, V=None):
    """Q, pr e E_unit por pixel; com V, o escoamento e reescalado para o volume direto V (m3) do evento."""
    p = Pv[i]; Q = qdir(i, lam)
    if V is not None:
        Q = np.minimum(V / (Q.sum() / 1000.0 * A) * Q, p)
    pr = Q / 1000.0 * A * (RI[i] / R[i]) / 3600.0
    return Q, pr, COEF * np.maximum(Q * pr * A, 0.0) ** EXPO * KCLS


Vscs = np.array([qdir(i, LAM).sum() / 1000.0 * A for i in range(N)])
Efor = np.array([campos(i, V=VD[i])[2].sum() for i in range(N)])
_Sc = Sv; Sv = S_020
Efor_ad = np.array([campos(i, 0.20, VD[i])[2].sum() for i in range(N)])
Sv = _Sc


def roda(nome, x, ajuste=fit1):
    c = ajuste(x, SY); sim = c * x
    loo = np.array([ajuste(x[ids != i], SY[ids != i]) * x[i] for i in range(N)])
    m15 = ids != 14; s15 = ajuste(x[m15], SY[m15]) * x[m15]
    return dict(nome=nome, c=c, sim=sim, loo=loo, nse=nse(SY, sim), nse_loo=nse(SY, loo), nse15=nse(SY[m15], s15),
                medape=np.median(ape(SY, loo)), fat2=f2(SY, loo), nlog=nse_log(SY, loo), sp=spearmanr(SY, loo)[0])


def roda_ic():
    Dq = TR * QPm; KLSC = 0.031 * 0.536 * 0.267

    def aj(m):
        b, a = np.polyfit(np.log(Dq[m]), np.log(SY[m] / KLSC), 1)
        return lambda j: np.exp(a) * Dq[j] ** b * KLSC
    sim = aj(np.ones(N, bool))(ids); loo = np.array([aj(ids != i)(i) for i in range(N)]); m15 = ids != 14
    return dict(nome="REF  IC concentrada (alfa, beta refeitos em log)", c=np.nan, sim=sim, loo=loo, nse=nse(SY, sim), nse_loo=nse(SY, loo),
                nse15=nse(SY[m15], aj(m15)(ids[m15])), medape=np.median(ape(SY, loo)), fat2=f2(SY, loo), nlog=nse_log(SY, loo), sp=spearmanr(SY, loo)[0])


M = [roda("CALCULADO  lambda 0,05, S convertido  [CANDIDATO]", E20),
     roda("FORCADO    lambda 0,05, S convertido  [CANDIDATO]", Efor),
     roda("adotado hoje: calculado, lambda 0,20", E_ad),
     roda("adotado hoje: forcado, lambda 0,20", Efor_ad),
     roda("REF  SY = c*chuva do evento", R),
     roda("REF  SY = c*volume direto medido", VD),
     roda("REF  SY = c*volume total medido (T_R)", TR),
     roda_ic()]
print("=" * 132)
print("ALVO: carga TOTAL medida | c em log | LOO (c refeito sem o evento) | MedAPE e fator 2 em %")
print(f"{'modelo':<62} {'c':>9} {'MedAPE':>7} {'fator2':>6} {'NSElog':>7} {'Spear':>6} | {'NSE in':>7} {'NSE LOO':>8} {'s/ev15':>7}")
for m in M:
    print(f"{m['nome']:<62} {m['c']:>9.4g} {m['medape']:>7.1f} {m['fat2']:>6.0f} {m['nlog']:>7.2f} {m['sp']:>6.2f} | {m['nse']:>7.2f} {m['nse_loo']:>8.2f} {m['nse15']:>7.2f}")
print("\nSENSIBILIDADE A CALIBRACAO: c por minimos quadrados LINEARES (NSE linear: in / LOO / sem ev15)")
for nome, x in (("calculado", E20), ("forcado", Efor), ("SY = c*chuva", R)):
    m = roda(nome, x, fit_lin)
    print(f"  {nome:<12} c = {m['c']:.4g} | NSE {m['nse']:.2f} / {m['nse_loo']:.2f} / {m['nse15']:.2f} | MedAPE {m['medape']:.1f}% | fator 2 {m['fat2']:.0f}%")

calc, forc, ch, vd, ic = M[0], M[1], M[4], M[5], M[7]
print(f"\nescoamento direto: SCS-CN / medido por evento: mediana {np.median(Vscs/VD):.2f} (min {np.min(Vscs/VD):.2f}, max {np.max(Vscs/VD):.2f}); "
      f"erro mediano do volume {np.median(100*np.abs(Vscs-VD)/VD):.0f}%; NSE do volume {nse(VD, Vscs):.2f}")
for a_, b_, rot in ((calc, ch, "calculado x SY=c*chuva"), (forc, vd, "forcado x SY=c*V_dir"), (forc, ic, "forcado x IC concentrada")):
    d = ape(SY, a_["loo"]) - ape(SY, b_["loo"]); bs = [np.median(rng.choice(d, N)) for _ in range(4000)]
    print(f"{rot:<26}: melhora em {np.sum(d < 0):>2} de 17 eventos; diferenca mediana do erro {np.median(d):+6.1f} pontos, IC95% [{np.percentile(bs,2.5):+.1f}; {np.percentile(bs,97.5):+.1f}]")

# ----------------------------------------------------------- rasters + csv
c_c, c_f = calc["c"], forc["c"]
print(f"\nCONFIGURACAO CANDIDATA: calculado c = {c_c:.6g} | forcado c = {c_f:.6g}  (t por unidade de E_unit)")
tab = []; Mc = []; Mf = []
for n in range(1, N + 1):
    i = n - 1
    Qd, pr, Ev = campos(i); pasta = os.path.join(BASE, f"Evento {n}")
    for nome, v in (("Qdir", Qd), ("pr", pr), ("E_unit", Ev), ("SY", c_c * Ev)):
        arr = np.full((ny, nx), np.nan); arr[valido] = v; salva(os.path.join(pasta, f"{nome}{n}_l05w.tif"), arr, ds0)
    Mc.append(c_c * Ev); Mf.append(c_f * campos(i, V=VD[i])[2])
    tab.append(dict(evento=n, SY_obs_t=SY[i], V_dir_medido_m3=VD[i], V_dir_SCS_m3=Vscs[i], V_base_Bt_m3=BTV[i],
                    soma_E_unit_calc_t=E20[i], SY_calc_t=calc["sim"][i], SY_calc_LOO_t=calc["loo"][i], erro_calc_LOO_pct=100 * (calc["loo"][i] - SY[i]) / SY[i],
                    soma_E_unit_forc_t=Efor[i], SY_forc_t=forc["sim"][i], SY_forc_LOO_t=forc["loo"][i], erro_forc_LOO_pct=100 * (forc["loo"][i] - SY[i]) / SY[i],
                    SY_chuva_LOO_t=ch["loo"][i], SY_Vdir_LOO_t=vd["loo"][i], SY_IC_LOO_t=ic["loo"][i]))
    print(f"evento {n:>2}: obs {SY[i]:7.0f} t | calculado LOO {calc['loo'][i]:7.0f} ({100*(calc['loo'][i]-SY[i])/SY[i]:+5.0f}%) | "
          f"forcado LOO {forc['loo'][i]:7.0f} ({100*(forc['loo'][i]-SY[i])/SY[i]:+5.0f}%) | SCS/medido {Vscs[i]/VD[i]:.2f}")
pd.DataFrame(tab).to_csv(os.path.join(DI, "comparacao_SY_lambda005_woodward.csv"), index=False, encoding="utf-8")
for nome, lst in (("SY_medio_eventos_l05w.tif", Mc), ("SY_medio_eventos_forcado_l05w.tif", Mf)):
    med = np.full((ny, nx), np.nan); med[valido] = np.mean(lst, axis=0); salva(os.path.join(DI, nome), med, ds0)
a = np.mean(Mc, axis=0); b = np.mean(Mf, axis=0)
q1, q2 = np.percentile(a, 95), np.percentile(b, 95)
print(f"mapa calculado x forcado: r = {np.corrcoef(a, b)[0,1]:.3f}; areas criticas (5%) coincidentes {100*np.sum((a>=q1)&(b>=q2))/np.sum(a>=q1):.1f}% | "
      f"r com K*C*LS: calculado {np.corrcoef(a, KCLS)[0,1]:.3f}, forcado {np.corrcoef(b, KCLS)[0,1]:.3f}")
for rot, arq, novo in (("calculado", "SY_medio_eventos_sd.tif", a), ("forcado", "SY_medio_eventos_forcado_sd.tif", b)):
    old, _ = le(os.path.join(DI, arq)); o_ = old[valido]; ok = np.isfinite(o_)
    qa, qo = np.percentile(novo[ok], 95), np.percentile(o_[ok], 95)
    print(f"mapa {rot}: candidato x adotado hoje r = {np.corrcoef(novo[ok], o_[ok])[0,1]:.3f}; areas criticas coincidentes "
          f"{100*np.sum((novo[ok]>=qa)&(o_[ok]>=qo))/np.sum(novo[ok]>=qa):.1f}%")
print("gravados: *_l05w.tif, SY_medio_eventos_l05w.tif, SY_medio_eventos_forcado_l05w.tif, comparacao_SY_lambda005_woodward.csv")
