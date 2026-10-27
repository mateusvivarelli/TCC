"""
ESCADA DA INFORMACAO HIDROLOGICA (15/10/2026; refeita em 26/10/2026 SEM termo de vazao de base) - onde esta o gargalo.

Degraus (de menos para mais informacao hidrologica), alvo = carga TOTAL de sedimentos, c em log, LOO, lambda 0,20.
Modelo adotado desde 26/10/2026: so escoamento direto, um coeficiente (SY = c * soma E_unit).
  N1  so chuva                                   : MUSLE (SCS-CN previsto)          x  SY = c*chuva
  N2  volume direto PREVISTO por regressao(chuva): MUSLE (volume previsto, padrao SCS-CN) x SY = c*V_prev
  N3  volume direto MEDIDO (modelo forcado)       : MUSLE (volume medido, padrao SCS-CN)  x SY = c*V_dir
Cada degrau compara a MUSLE espacializada com a regra de um coeficiente que usa o MESMO insumo (sem MUSLE, sem mapa).
Saidas: figuras/escada_gargalo.png e figuras/escada_gargalo.csv
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from osgeo import gdal
from scipy.optimize import least_squares
from scipy.stats import spearmanr

gdal.UseExceptions()
sys.stdout.reconfigure(encoding="utf-8")
BASE = r"C:\TCC"; DI = os.path.join(BASE, "Dados Iniciais"); FIG = os.path.join(BASE, "TCC_Texto", "figuras")
os.makedirs(FIG, exist_ok=True)
COEF, EXPO, N, LAM = 11.8, 0.56, 17, 0.20
rng = np.random.default_rng(15102026)


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
SY = np.zeros(N); VD = np.zeros(N); BTV = np.zeros(N); RI = np.zeros(N); R = np.zeros(N); Qb0 = np.zeros(N); durR = np.zeros(N); Pv = []
for n in range(1, N + 1):
    r = ev.iloc[0 if n == 1 else n]; w = h.loc[r["Inicio"]:r["Fim"]]
    SY[n - 1] = r["SYY_t"]; VD[n - 1] = (w.Q - w.Bt).sum() * 3600; BTV[n - 1] = w.Bt.sum() * 3600
    RI[n - 1] = r["Intensidade_60min_mm/h"]; R[n - 1] = r["Chuva_evento_mm"]; Qb0[n - 1] = r["Qb_inicio"]
    durR[n - 1] = max(r["Tempo_precipitacao_p1_h"], r["Tempo_precipitacao_p2_h"])
    Pv.append(le(os.path.join(BASE, f"Evento {n}", f"ChuvaIDW{n}.tif"))[0][valido])
ids = np.arange(N)
base_ch = Qb0 * durR * 3600.0


def esoma(i, lam, V=None):
    p = Pv[i]; Q = np.where(p <= lam * Sv, 0.0, (p - lam * Sv) ** 2 / (p + (1 - lam) * Sv))
    if V is not None:
        Q = np.minimum(V / (Q.sum() / 1000.0 * A) * Q, p)
    pr = Q / 1000.0 * A * (RI[i] / R[i]) / 3600.0
    return np.sum(COEF * np.maximum(Q * pr * A, 0.0) ** EXPO * KCLS)


def fit2(x1, x2, y):
    f = lambda p: np.log(np.clip(p[0] * x1 + p[1] * x2, 1e-9, None)) - np.log(y)
    best = None
    for s0 in ([y.mean() / x1.mean(), 0.0], [0.0, y.mean() / x2.mean()], [0.5 * y.mean() / x1.mean(), 0.5 * y.mean() / x2.mean()]):
        r = least_squares(f, s0, bounds=(0, np.inf), x_scale="jac")
        if best is None or r.cost < best.cost: best = r
    return best.x


fit1 = lambda x, y: np.exp(np.mean(np.log(y) - np.log(x)))


def loo1(x):
    return np.array([fit1(x[ids != i], SY[ids != i]) * x[i] for i in range(N)])


def loo2(x1, x2):
    out = np.zeros(N)
    for i in range(N):
        m = ids != i; p = fit2(x1[m], x2[m], SY[m]); out[i] = p[0] * x1[i] + p[1] * x2[i]
    return out


# volume direto previsto por regressao em log (LOO)
Xm = np.column_stack([np.ones(N), np.log(R)]); ly = np.log(VD); Vp = np.zeros(N)
for i in range(N):
    m = ids != i; b = np.linalg.lstsq(Xm[m], ly[m], rcond=None)[0]; Vp[i] = np.exp(Xm[i] @ b)

E1 = np.array([esoma(i, LAM) for i in range(N)])
E2 = np.array([esoma(i, LAM, Vp[i]) for i in range(N)])
E3 = np.array([esoma(i, LAM, VD[i]) for i in range(N)])
ape = lambda s_: 100 * np.abs(s_ - SY) / SY
f2 = lambda s_: 100 * np.mean((s_ / SY >= 0.5) & (s_ / SY <= 2.0))
nlog = lambda s_: 1 - np.sum((np.log(SY) - np.log(np.clip(s_, 1e-6, None))) ** 2) / np.sum((np.log(SY) - np.log(SY).mean()) ** 2)

def loo1_n2():
    """N2 totalmente aninhado: em cada rodada a regressao do volume na chuva e refeita SEM o evento retido."""
    outB = np.zeros(N); outS = np.zeros(N)
    for i in range(N):
        m = ids != i
        bcoef = np.linalg.lstsq(Xm[m], ly[m], rcond=None)[0]; Vp_i = np.exp(Xm @ bcoef)
        E_i = np.array([esoma(j, LAM, Vp_i[j]) for j in range(N)])
        outB[i] = fit1(E_i[m], SY[m]) * E_i[i]; outS[i] = fit1(Vp_i[m], SY[m]) * Vp_i[i]
    return outB, outS


_N2B, _N2S = loo1_n2()
NIV = [
    ("N1: so chuva\n(modelo calculado)", loo1(E1), loo1(R)),
    ("N2: volume direto previsto\n(regressao na chuva)", _N2B, _N2S),
    ("N3: volume direto medido\n(modelo forcado)", loo1(E3), loo1(VD)),
]
ref = np.array([np.exp(np.mean(np.log(SY[ids != i]) - np.log(R[ids != i]))) * R[i] for i in range(N)])
print("=" * 118)
print("ESCADA (alvo carga total, c em log, LOO, lambda 0,20, sem termo de base)")
print(f"{'nivel':<44} {'modelo':<26} {'MedAPE':>7} {'fator2':>7} {'NSE-log':>8} {'Spearman':>8} | melhora de B vs simples: n eventos / mediana (IC95%)")
rows = []
for nome, b, s in NIV:
    d = ape(b) - ape(s); bs = np.array([np.median(rng.choice(d, N)) for _ in range(4000)])
    for tag, v in (("MUSLE espacializada", b), ("simples (sem MUSLE)", s)):
        extra = f"{np.sum(d<0):>2}/17  {np.median(d):+6.1f} [{np.percentile(bs,2.5):+.1f}; {np.percentile(bs,97.5):+.1f}]" if tag.startswith("MUSLE") else ""
        print(f"{nome.replace(chr(10),' '):<44} {tag:<26} {np.median(ape(v)):7.1f} {f2(v):7.0f} {nlog(v):8.3f} {spearmanr(SY, v)[0]:8.3f} | {extra}")
        rows.append(dict(nivel=nome.replace("\n", " "), modelo=tag, MedAPE=np.median(ape(v)), fator2=f2(v), NSE_log=nlog(v), Spearman=spearmanr(SY, v)[0]))
print(f"{'referencia: SY = c * chuva':<44} {'':<26} {np.median(ape(ref)):7.1f} {f2(ref):7.0f} {nlog(ref):8.3f} {spearmanr(SY, ref)[0]:8.3f}")
pd.DataFrame(rows).to_csv(os.path.join(FIG, "escada_gargalo.csv"), index=False, encoding="utf-8")

# ---- figura
NIV_FIG = [NIV[0], NIV[2]]   # figura do texto: so os dois modelos (N1 = calculado da chuva; N4 = forcado ao medido)
fig, ax = plt.subplots(1, 2, figsize=(11, 4.8))
x = np.arange(len(NIV_FIG)); wd = 0.36
cb, cs = "#1f5fa8", "#b8b8b8"
for k, (key, tit, fmt) in enumerate((("MedAPE", "Erro percentual mediano (menor é melhor)", "{:.0f}%"), ("fator2", "Eventos dentro de fator 2 (maior é melhor)", "{:.0f}%"))):
    a = ax[k]
    vb = [np.median(ape(b)) if key == "MedAPE" else f2(b) for _, b, _ in NIV_FIG]
    vs = [np.median(ape(s)) if key == "MedAPE" else f2(s) for _, _, s in NIV_FIG]
    r1 = a.bar(x - wd / 2, vb, wd, color=cb, label="MUSLE espacializada (só escoamento direto)")
    r2 = a.bar(x + wd / 2, vs, wd, color=cs, label="Regra simples com o mesmo insumo (c · chuva ou c · volume direto)")
    for rr in list(r1) + list(r2):
        a.text(rr.get_x() + rr.get_width() / 2, rr.get_height() + 1, fmt.format(rr.get_height()), ha="center", fontsize=9)
    a.axhline(np.median(ape(ref)) if key == "MedAPE" else f2(ref), color="#c0392b", ls="--", lw=1.2, label="Referência: SY = c · chuva")
    a.set_xticks(x); a.set_xticklabels(["Água calculada\nda chuva (previsão)", "Água forçada\nao medido"], fontsize=10)
    a.set_title(tit, fontsize=11)
    a.spines[["top", "right"]].set_visible(False)
    a.set_ylim(0, 112)
h_, l_ = ax[0].get_legend_handles_labels()
fig.legend(h_, l_, loc="lower center", ncol=3, frameon=False, fontsize=9, bbox_to_anchor=(0.5, 0.045))
fig.suptitle("Quanto melhor a estimativa da água, melhor o sedimento: o gargalo é transformar chuva em escoamento", fontsize=12)
fig.text(0.5, 0.005, "Calculada da chuva: escoamento direto pelo SCS-CN. Forçada ao medido: escoamento direto medido (volume total menos a vazão de base). Sem termo de vazão de base.\n"
         "Validação leave-one-out, calibração em log (um coeficiente), 17 eventos, λ = 0,20, carga total de sedimentos.", ha="center", fontsize=7.5)
fig.tight_layout(rect=(0, 0.11, 1, 0.95))
fig.savefig(os.path.join(FIG, "escada_gargalo.png"), dpi=150)
print("figura:", os.path.join(FIG, "escada_gargalo.png"))
