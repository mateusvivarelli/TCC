"""
MODELO ADOTADO (15/10/2026): MUSLE espacializada com 'escoamento direto + vazao de base prevista'.

Motivacao: T_R_m3 e a SOMA das vazoes horarias (inclui vazao de base, 34-55%), SY_obs e a carga
total (Q*CSS) e o SCS-CN calcula so escoamento direto (ver notas, secoes 15 e 16). O volume
escoado que alimenta a MUSLE passa a ser o volume TOTAL previsto:

    Q_pixel = Q_dir,k (SCS-CN, CN-I, lambda = 0,20 padrao)  +  q_base (mm, uniforme)
    q_base  = V_base / A_bacia * 1000
    V_base  = kb * Qb_inicio * Duracao_horas * 3600     (kb ajustado contra a soma de Bt)

depois, como antes: pr = Q/1000*A_pix*(RI/R)/3600 ; E_unit = 11,8*(Q*pr*A_pix)^0,56*K*C*P*LS ;
SY = c*E_unit, c por minimos quadrados pela origem nos 17 eventos.

lambda = 0,20 e fixado a priori (valor padrao do SCS), NAO escolhido pelo desempenho; a
sensibilidade a lambda e apenas reportada. A validacao leave-one-out e ANINHADA: para cada
evento retido refaz-se kb (sem ele) e c (sem ele, com E recalculado com esse kb).

Saidas (sufixo _vb): Evento n/Q{n}_vb.tif, pr{n}_vb.tif, E_unit{n}_vb.tif, SY{n}_vb.tif;
Dados Iniciais/SY_medio_eventos_vb.tif; Dados Iniciais/comparacao_SY_modelo_com_base.csv.
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
COEF, EXPO, LAM = 11.8, 0.56, 0.20
N = 17
rng = np.random.default_rng(20261015)


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
              outputBounds=(gt[0], gt[3] + ny * gt[5], gt[0] + nx * gt[1], gt[3]), dstSRS=ds0.GetProjection(),
              resampleAlg=gdal.GRA_NearestNeighbour)
S = o.GetRasterBand(1).ReadAsArray().astype(np.float64); S = np.where(S > -1e30, S, np.nan)
valido = np.isfinite(S) & np.isfinite(K) & np.isfinite(C) & np.isfinite(LS)
nval = int(valido.sum()); area_bacia = nval * A
KCLS = (K * C * LS)[valido]; Sv = S[valido]
print(f"grade {nx}x{ny}; pixels validos = {nval:,}; area da bacia (validos) = {area_bacia/1e6:.2f} km2; A_pix = {A:.2f} m2")

ev = pd.read_excel(os.path.join(DI, "eventos_processados_manuais.xlsx"), sheet_name="Sheet1").iloc[:18]
h = pd.read_excel(os.path.join(DI, "Dados_finais_histereses_corrigido.xlsx"), sheet_name="Planilha1").iloc[:, :8]
h.columns = ["Data", "P1", "P2", "Ptot", "Q", "CSS", "Bt", "CSSBt"]; h["Data"] = pd.to_datetime(h["Data"]); h = h.set_index("Data")

SY = np.zeros(N); TR = np.zeros(N); BTV = np.zeros(N); RI = np.zeros(N); R = np.zeros(N); Qb0 = np.zeros(N); dur = np.zeros(N)
Pv = []
for n in range(1, N + 1):
    r = ev.iloc[0 if n == 1 else n]; w = h.loc[r["Inicio"]:r["Fim"]]
    SY[n - 1] = r["SYY_t"]; TR[n - 1] = r["T_R_m3"]; BTV[n - 1] = w.Bt.sum() * 3600
    RI[n - 1] = r["Intensidade_60min_mm/h"]; R[n - 1] = r["Chuva_evento_mm"]; Qb0[n - 1] = r["Qb_inicio"]; dur[n - 1] = r["Duracao_horas"]
    Pv.append(le(os.path.join(BASE, f"Evento {n}", f"ChuvaIDW{n}.tif"))[0][valido])
VD = TR - BTV
xb = Qb0 * dur * 3600.0                      # (m3/s * h * 3600) = volume de referencia


def qdir(i, lam):
    p = Pv[i]
    return np.where(p <= lam * Sv, 0.0, (p - lam * Sv) ** 2 / (p + (1 - lam) * Sv))


def esoma(i, Qd, vb):
    Q = Qd + vb / area_bacia * 1000.0
    pr = Q / 1000.0 * A * (RI[i] / R[i]) / 3600.0
    return np.sum(COEF * np.maximum(Q * pr * A, 0.0) ** EXPO * KCLS)


def fit0(x, y):
    return np.sum(x * y) / np.sum(x * x)


def nse(o_, s_):
    return 1 - np.sum((o_ - s_) ** 2) / np.sum((o_ - o_.mean()) ** 2)


def wia(o_, s_):
    m = o_.mean()
    return 1 - np.sum((o_ - s_) ** 2) / np.sum((np.abs(s_ - m) + np.abs(o_ - m)) ** 2)


def nse_log(o_, s_):
    lo, ls = np.log(o_), np.log(s_)
    return 1 - np.sum((lo - ls) ** 2) / np.sum((lo - lo.mean()) ** 2)


def avalia_lambda(lam):
    """devolve dict com E (in-sample), SY sim, SY LOO aninhado, volumes"""
    Qd = [qdir(i, lam) for i in range(N)]
    kb = fit0(xb, BTV); vb = kb * xb
    E = np.array([esoma(i, Qd[i], vb[i]) for i in range(N)])
    c = fit0(E, SY); sim = c * E
    loo = np.zeros(N); kbl = np.zeros(N)
    for i in range(N):
        m = np.arange(N) != i
        kbi = fit0(xb[m], BTV[m]); kbl[i] = kbi
        Ei = np.array([esoma(j, Qd[j], kbi * xb[j]) for j in range(N)])
        loo[i] = fit0(Ei[m], SY[m]) * Ei[i]
    Vdir = np.array([Qd[i].sum() / 1000 * A for i in range(N)])
    Vtot = Vdir + kbl * xb  # base prevista sem o proprio evento (honesto)
    return dict(kb=kb, c=c, E=E, sim=sim, loo=loo, kbl=kbl, Vdir=Vdir, Vtot=Vtot, Qd=Qd, vb=vb)


# ------------------------------------------------------------------ sensibilidade a lambda
print("=" * 108)
print("SENSIBILIDADE A LAMBDA (lambda adotado = 0,20, fixado a priori; os demais so para reportar)")
print(f"{'lambda':>6} | {'volume TOTAL vs T_R: erro med / abs / NSE':>44} | {'SY: NSE in / LOO / abs LOO':>30}")
res = {}
for lam in (0.05, 0.10, 0.15, 0.20):
    d = avalia_lambda(lam); res[lam] = d
    e = 100 * (d["Vtot"] - TR) / TR
    print(f"{lam:6.2f} | {e.mean():+10.1f}% {np.abs(e).mean():8.1f}% {nse(TR, d['Vtot']):9.3f}        | "
          f"{nse(SY, d['sim']):7.3f} {nse(SY, d['loo']):7.3f} {np.mean(np.abs(100*(d['loo']-SY)/SY)):7.1f}%")
d = res[LAM]
kb, c, E, sim, loo = d["kb"], d["c"], d["E"], d["sim"], d["loo"]

print("=" * 108)
print(f"MODELO ADOTADO (lambda = {LAM:.2f}): kb = {kb:.3f} | c = {c:.6f}")
vb_nse = nse(BTV, d["kbl"] * xb)
print(f"vazao de base: prevista (kb sem o evento) x Bt observado: NSE = {vb_nse:.3f}; erro abs medio = {np.mean(np.abs(100*(d['kbl']*xb-BTV)/BTV)):.1f}%")
ev_t = 100 * (d["Vtot"] - TR) / TR
ev_d = 100 * (d["Vdir"] - VD) / VD
print(f"volume TOTAL previsto x T_R:        erro medio {ev_t.mean():+.1f}% | abs {np.abs(ev_t).mean():.1f}% | NSE {nse(TR, d['Vtot']):.3f}")
print(f"escoamento DIRETO (SCS-CN) x direto: erro medio {ev_d.mean():+.1f}% | abs {np.abs(ev_d).mean():.1f}% | NSE {nse(VD, d['Vdir']):.3f}  (so a parte SCS-CN)")
err = 100 * (sim - SY) / SY; errl = 100 * (loo - SY) / SY
print(f"SY (in-sample): NSE {nse(SY, sim):.3f} | WIA {wia(SY, sim):.3f} | PBIAS(sim-obs) {100*(sim.sum()-SY.sum())/SY.sum():+.1f}% | erro medio {err.mean():+.1f}% | abs {np.abs(err).mean():.1f}%")
print(f"SY (LOO aninhado): NSE {nse(SY, loo):.3f} | WIA {wia(SY, loo):.3f} | PBIAS {100*(loo.sum()-SY.sum())/SY.sum():+.1f}% | erro medio {errl.mean():+.1f}% | abs {np.abs(errl).mean():.1f}%")
print(f"SY: NSE em log (in-sample) {nse_log(SY, sim):.3f} (LOO {nse_log(SY, np.clip(loo, 1e-6, None)):.3f}) | Spearman(in) {spearmanr(SY, sim)[0]:.3f} (LOO {spearmanr(SY, loo)[0]:.3f})")

# sem o evento 15 (c refeito sem ele)
m15 = np.arange(N) != 14
c15 = fit0(E[m15], SY[m15]); print(f"SEM o evento 15 (c refeito = {c15:.5f}): NSE in-sample {nse(SY[m15], c15*E[m15]):.3f}")
loo15 = np.array([fit0(E[m15][np.arange(16) != k], SY[m15][np.arange(16) != k]) * E[m15][k] for k in range(16)])
print(f"                              NSE LOO (c apenas; kb fixo) {nse(SY[m15], loo15):.3f}")
# bootstrap dos eventos (c refeito em cada reamostragem)
bs = []
for _ in range(4000):
    ix = rng.integers(0, N, N)
    if np.ptp(SY[ix]) == 0: continue
    cb = fit0(E[ix], SY[ix]); bs.append(nse(SY[ix], cb * E[ix]))
print(f"bootstrap (4000 reamostragens de eventos, c refeito): NSE in-sample mediana {np.median(bs):.3f}, IC 95% [{np.percentile(bs,2.5):.2f}; {np.percentile(bs,97.5):.2f}]")

# benchmarks triviais (mesmos 17 eventos)
print("=" * 108)
print("BENCHMARKS SEM MUSLE (1 parametro c; LOO simples)")
for nome, xx in [("SY = c * T_R (volume total medido)", TR), ("SY = c * volume direto medido", VD), ("SY = c * Chuva_evento", R),
                 ("SY = c * (V_dir SCS + V_base prevista)", d["Vtot"])]:
    cc = fit0(xx, SY); s_ = cc * xx
    l_ = np.array([fit0(np.delete(xx, i), np.delete(SY, i)) * xx[i] for i in range(N)])
    print(f"  {nome:<44} NSE {nse(SY, s_):6.3f} | LOO {nse(SY, l_):6.3f} | abs LOO {np.mean(np.abs(100*(l_-SY)/SY)):5.1f}%")

# ------------------------------------------------------------------ rasters e tabela
print("=" * 108)
Eras = []
tab = []
for n in range(1, N + 1):
    i = n - 1
    Qt = d["Qd"][i] + d["vb"][i] / area_bacia * 1000.0
    pr = Qt / 1000.0 * A * (RI[i] / R[i]) / 3600.0
    Ev = COEF * np.maximum(Qt * pr * A, 0.0) ** EXPO * KCLS
    SYv = c * Ev
    pasta = os.path.join(BASE, f"Evento {n}")
    for nome, v in (("Q", Qt), ("pr", pr), ("E_unit", Ev), ("SY", SYv)):
        arr = np.full((ny, nx), np.nan); arr[valido] = v
        salva(os.path.join(pasta, f"{nome}{n}_vb.tif"), arr, ds0)
    Eras.append(SYv)
    tab.append(dict(evento=n, SY_obs_t=SY[i], SY_sim_t=sim[i], erro_pct=err[i], SY_loo_t=loo[i], erro_loo_pct=errl[i],
                    soma_E_unit_t=E[i], T_R_m3=TR[i], V_base_obs_m3=BTV[i], V_direto_obs_m3=VD[i],
                    Qb_inicio=Qb0[i], duracao_h=dur[i], V_base_prev_m3=d["vb"][i], V_dir_SCS_m3=d["Vdir"][i],
                    V_total_prev_loo_m3=d["Vtot"][i], erro_V_total_pct=ev_t[i]))
    print(f"evento {n:>2}: SY obs {SY[i]:8.1f} t | sim {sim[i]:8.1f} t ({err[i]:+6.1f}%) | LOO {loo[i]:8.1f} t ({errl[i]:+6.1f}%) | "
          f"V_total prev {d['Vtot'][i]:>11,.0f} vs {TR[i]:>11,.0f} m3 ({ev_t[i]:+6.1f}%)")
pd.DataFrame(tab).to_csv(os.path.join(DI, "comparacao_SY_modelo_com_base.csv"), index=False, encoding="utf-8")

med = np.full((ny, nx), np.nan); med[valido] = np.mean(Eras, axis=0)
salva(os.path.join(DI, "SY_medio_eventos_vb.tif"), med, ds0)
print("SY_medio_eventos_vb.tif e comparacao_SY_modelo_com_base.csv gravados")

# ------------------------------------------------------------------ mapa novo x mapa anterior
old, _ = le(os.path.join(DI, "SY_medio_eventos.tif"))
a = med[valido]; b = old[valido]; ok = np.isfinite(a) & np.isfinite(b)
print(f"mapa medio novo x anterior (previsao pura, lambda=0,05): r = {np.corrcoef(a[ok], b[ok])[0,1]:.4f}")
q95a, q95b = np.nanpercentile(a[ok], 95), np.nanpercentile(b[ok], 95)
print(f"coincidencia dos 5% superiores (hot spots): {100*np.sum((a[ok] >= q95a) & (b[ok] >= q95b))/np.sum(a[ok] >= q95a):.1f}%")
kcls = KCLS[ok]; print(f"r(mapa novo, K*C*LS) = {np.corrcoef(a[ok], kcls)[0,1]:.3f} | r(mapa anterior, K*C*LS) = {np.corrcoef(b[ok], kcls)[0,1]:.3f}")
