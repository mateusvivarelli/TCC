"""
MODELO ADOTADO (opcao B, 15/10/2026): MUSLE espacializada com DOIS COMPONENTES de sedimento.

    SY_evento = c1 * soma_pixels E_unit(Q_direto)   +   c2 * (Qb_inicio * duracao_da_CHUVA * 3600)
                 \\______ parte das encostas ______/        \\______ parte da vazao de base (bacia) ______/

  - Q_direto: escoamento direto do SCS-CN (CN-I, lambda = 0,20, fixado a priori), SEM lamina de base nos pixels.
  - E_unit = 11,8*(Q*pr*A)^0,56*K*C*LS,  pr = Q/1000*A*(RI/R)/3600   (Hao et al., 2022).
  - A base entra como UM termo da bacia (nao e espalhada pelos pixels): proporcional ao volume de referencia
    Qb_inicio*duracao*3600; a duracao usada e a da CHUVA (max dos dois postos), nao a da janela do hidrograma,
    para nao vazar informacao do resultado. c2 ja absorve o antigo kb.
  - c1 e c2 (>= 0) sao calibrados em LOG: minimos quadrados de ln(SY_obs) - ln(c1*E + c2*V).
  - Validacao leave-one-out ANINHADA: c1 e c2 refeitos sem o evento retido.
  - Metricas robustas ao evento 15: mediana do erro percentual (MedAPE), fracao de eventos em fator 2,
    Spearman, NSE em log; NSE linear so como apoio, com e sem o evento 15.

Variantes reportadas (nao adotadas como previsao): base OBSERVADA (limite superior/diagnostico) e duracao do
hidrograma (vazamento). Referencias sem MUSLE: SY = c*chuva e SY = c*T_R.

Saidas (sufixo _b2): Evento n/{Qdir,pr,E_unit,SY}{n}_b2.tif; Dados Iniciais/SY_medio_eventos_b2.tif;
Dados Iniciais/comparacao_SY_dois_componentes.csv. O mapa mostra SO a parte das encostas (escoamento direto).
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


ids = np.arange(N)
nse = lambda o_, s_: 1 - np.sum((o_ - s_) ** 2) / np.sum((o_ - o_.mean()) ** 2)
nse_log = lambda o_, s_: 1 - np.sum((np.log(o_) - np.log(np.clip(s_, 1e-6, None))) ** 2) / np.sum((np.log(o_) - np.log(o_).mean()) ** 2)
ape = lambda o_, s_: 100 * np.abs(s_ - o_) / o_
f2 = lambda o_, s_: 100 * np.mean((s_ / o_ >= 0.5) & (s_ / o_ <= 2.0))


def roda(nome, x1, x2=None):
    if x2 is None:
        c = fit1(x1, SY); sim = c * x1
        loo = np.array([fit1(x1[ids != i], SY[ids != i]) * x1[i] for i in range(N)]); par = (c,)
    else:
        p = fit2(x1, x2, SY); sim = p[0] * x1 + p[1] * x2; par = tuple(p)
        loo = np.zeros(N)
        for i in range(N):
            m = ids != i; pi = fit2(x1[m], x2[m], SY[m]); loo[i] = pi[0] * x1[i] + pi[1] * x2[i]
    m15 = ids != 14
    if x2 is None:
        s15 = fit1(x1[m15], SY[m15]) * x1[m15]
    else:
        p15 = fit2(x1[m15], x2[m15], SY[m15]); s15 = p15[0] * x1[m15] + p15[1] * x2[m15]
    return dict(nome=nome, par=par, sim=sim, loo=loo,
                linha=f"{nome:<58} {nse_log(SY, sim):7.3f} {nse_log(SY, loo):7.3f} {np.median(ape(SY, loo)):7.1f} {ape(SY, loo).mean():7.1f} {f2(SY, loo):6.0f} "
                      f"{spearmanr(SY, loo)[0]:8.3f} | {nse(SY, sim):7.3f} {nse(SY, loo):7.3f} {nse(SY[m15], s15):8.3f}")


print("=" * 128)
print("METRICAS (calibracao em log; LOO aninhado). MedAPE e MAPE em %; fator2 = % de eventos com 0,5 <= sim/obs <= 2")
print(f"{'modelo':<58} {'NSElog':>7} {'NSElog':>7} {'MedAPE':>7} {'MAPE':>7} {'fator2':>6} {'Spearman':>8} | {'NSE lin':>7} {'NSE lin':>7} {'NSE lin':>8}")
print(f"{'':<58} {'in':>7} {'LOO':>7} {'LOO':>7} {'LOO':>7} {'LOO':>6} {'LOO':>8} | {'in':>7} {'LOO':>7} {'sem ev15':>8}")
ref = [roda("REF  SY = c*chuva do evento", R), roda("REF  SY = c*T_R (volume total medido)", TR)]
vars_ = [
    roda("MUSLE so escoamento direto (lambda 0,20), sem base", E20),
    roda("B  2 componentes, base prevista (duracao da CHUVA)  [ADOTADO]", E20, X2["chuva"]),
    roda("B' 2 componentes, base prevista (duracao do HIDROGRAMA) [vaza]", E20, X2["hidrograma"]),
    roda("B* 2 componentes, base OBSERVADA (Bt) [diagnostico]", E20, X2["observada"]),
    roda("B  com lambda 0,05 (sensibilidade; base duracao da chuva)", E05, X2["chuva"]),
]
for m in ref + vars_:
    print(m["linha"])
mb = vars_[1]
c1, c2 = mb["par"]
print("=" * 128)
print(f"MODELO ADOTADO (B): c1 = {c1:.5f} (sedimento por unidade de E_unit das encostas) | c2 = {c2:.6f} t por m3 de volume de base de referencia")
print(f"  (c2 equivale a {c2*1.929:.6f} t por m3 de base prevista com o kb antigo de 1,93)")
sl = c1 * E20; bs = c2 * X2["chuva"]; tot = sl + bs
print(f"  parcela das encostas no SY total simulado: mediana {np.median(100*sl/tot):.0f}% (min {np.min(100*sl/tot):.0f}%, max {np.max(100*sl/tot):.0f}%); parcela da base: mediana {np.median(100*bs/tot):.0f}%")

# bootstrap de eventos
bl = []; bm = []; b2 = []
for _ in range(1500):
    ix = rng.integers(0, N, N)
    if np.ptp(SY[ix]) == 0: continue
    p = fit2(E20[ix], X2["chuva"][ix], SY[ix]); s_ = p[0] * E20[ix] + p[1] * X2["chuva"][ix]
    bl.append(nse_log(SY[ix], s_)); bm.append(np.median(ape(SY[ix], s_)))
    c0 = fit1(R[ix], SY[ix]); b2.append(np.median(ape(SY[ix], c0 * R[ix])))
print(f"bootstrap de eventos (in-sample, 1500): NSE-log mediana {np.median(bl):.2f} IC95% [{np.percentile(bl,2.5):.2f}; {np.percentile(bl,97.5):.2f}] | "
      f"MedAPE modelo B {np.median(bm):.0f}% [{np.percentile(bm,2.5):.0f}; {np.percentile(bm,97.5):.0f}] x chuva {np.median(b2):.0f}% [{np.percentile(b2,2.5):.0f}; {np.percentile(b2,97.5):.0f}]")
d = ape(SY, mb["loo"]) - ape(SY, ref[0]["loo"])
print(f"modelo B menos SY=c*chuva, por evento (erro % LOO): melhora em {np.sum(d<0)} de 17 eventos; diferenca mediana {np.median(d):+.1f} pontos; IC bootstrap da mediana "
      f"[{np.percentile([np.median(rng.choice(d, N)) for _ in range(3000)], 2.5):+.1f}; {np.percentile([np.median(rng.choice(d, N)) for _ in range(3000)], 97.5):+.1f}]")

# ----------------------------------------------------------- rasters + csv
tab = []
Eras = []
for n in range(1, N + 1):
    i = n - 1
    Qd = qdir(i); pr = Qd / 1000.0 * A * (RI[i] / R[i]) / 3600.0
    Ev = COEF * np.maximum(Qd * pr * A, 0.0) ** EXPO * KCLS; SYv = c1 * Ev
    pasta = os.path.join(BASE, f"Evento {n}")
    for nome, v in (("Qdir", Qd), ("pr", pr), ("E_unit", Ev), ("SY", SYv)):
        arr = np.full((ny, nx), np.nan); arr[valido] = v; salva(os.path.join(pasta, f"{nome}{n}_b2.tif"), arr, ds0)
    Eras.append(SYv)
    tab.append(dict(evento=n, SY_obs_t=SY[i], SY_encostas_t=sl[i], SY_base_t=bs[i], SY_total_sim_t=tot[i], erro_pct=100 * (tot[i] - SY[i]) / SY[i],
                    SY_total_LOO_t=mb["loo"][i], erro_LOO_pct=100 * (mb["loo"][i] - SY[i]) / SY[i], soma_E_unit_dir_t=E20[i], Qb_inicio=Qb0[i],
                    duracao_chuva_h=durR[i], volume_base_ref_m3=X2["chuva"][i], SY_chuva_ref_t=ref[0]["sim"][i], SY_vol_total_ref_t=ref[1]["sim"][i]))
    print(f"evento {n:>2}: obs {SY[i]:8.1f} t | encostas {sl[i]:8.1f} + base {bs[i]:8.1f} = {tot[i]:8.1f} t ({100*(tot[i]-SY[i])/SY[i]:+6.1f}%) | LOO {mb['loo'][i]:8.1f} ({100*(mb['loo'][i]-SY[i])/SY[i]:+6.1f}%)")
pd.DataFrame(tab).to_csv(os.path.join(DI, "comparacao_SY_dois_componentes.csv"), index=False, encoding="utf-8")
med = np.full((ny, nx), np.nan); med[valido] = np.mean(Eras, axis=0); salva(os.path.join(DI, "SY_medio_eventos_b2.tif"), med, ds0)
old, _ = le(os.path.join(DI, "SY_medio_eventos.tif"))
a = med[valido]; b_ = old[valido]; ok = np.isfinite(a) & np.isfinite(b_)
q1, q2 = np.nanpercentile(a[ok], 95), np.nanpercentile(b_[ok], 95)
print(f"mapa medio B x mapa anterior: r = {np.corrcoef(a[ok], b_[ok])[0,1]:.4f}; hot spots (top 5%) coincidentes: {100*np.sum((a[ok]>=q1)&(b_[ok]>=q2))/np.sum(a[ok]>=q1):.1f}%; "
      f"r com K*C*LS = {np.corrcoef(a[ok], KCLS[ok])[0,1]:.3f}; Spearman com K*C*LS = {spearmanr(a[ok], KCLS[ok])[0]:.3f}")
print("rasters *_b2.tif, SY_medio_eventos_b2.tif e comparacao_SY_dois_componentes.csv gravados")
