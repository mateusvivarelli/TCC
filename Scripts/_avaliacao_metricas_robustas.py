"""
AVALIACAO COM METRICAS ROBUSTAS AO EVENTO DOMINANTE (15/10/2026)

Pedido do autor: nao deixar o evento 15 (49% da variancia linear do SY) comandar nem a
avaliacao nem a calibracao. Este script compara:

  calibracao de c:  (MQ) minimos quadrados lineares pela origem  [anterior]
                    (LOG) minimos quadrados em log: ln c = media(ln SY - ln E)  [erro relativo simetrico]
  avaliacao:        NSE linear; NSE em log; erro percentual absoluto medio e mediano (MAPE/MedAPE);
                    fracao de eventos com erro dentro de fator 2 (0,5 <= sim/obs <= 2);
                    vies geometrico; Spearman; participacao do maior evento na variancia

Todas as metricas "LOO" sao leave-one-out aninhadas (c, e no modelo de 2 componentes c1 e c2, refeitos
sem o evento retido). Para os modelos com kb (vazao de base prevista), kb e fixo em 1,929 aqui
(a diferenca de kb sem cada evento e pequena: 1,77-2,00; ver calcular_sy_com_base.py).
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
N = 17
rng = np.random.default_rng(15102026)
COEF, EXPO = 11.8, 0.56

# ----------------------------------------------------------- dados
nb = pd.read_csv(os.path.join(DI, "comparacao_SY_modelo_com_base.csv")).sort_values("evento")
cmp_ = pd.read_csv(os.path.join(DI, "comparacao_SY_previsao_vs_restrito.csv")).sort_values("evento")
ev = pd.read_excel(os.path.join(DI, "eventos_processados_manuais.xlsx"), sheet_name="Sheet1").iloc[:18]
idx = [0 if n == 1 else n for n in range(1, N + 1)]
SY = nb.SY_obs_t.to_numpy(float); TR = nb.T_R_m3.to_numpy(float); VD = nb.V_direto_obs_m3.to_numpy(float)
VBo = nb.V_base_obs_m3.to_numpy(float); VBp = nb.V_base_prev_m3.to_numpy(float); dur = nb.duracao_h.to_numpy(float)
R = np.array([ev.iloc[i]["Chuva_evento_mm"] for i in idx], float); RI = np.array([ev.iloc[i]["Intensidade_60min_mm/h"] for i in idx], float)
E_prev = cmp_.soma_E_unit_previsao_t.to_numpy(float); E_rest = cmp_.soma_E_unit_restrito_t.to_numpy(float); E_base = nb.soma_E_unit_t.to_numpy(float)


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


def e_direto(lam):
    """soma de E_unit com Q = escoamento direto (sem lamina de base) para os 17 eventos"""
    out = np.zeros(N)
    for n in range(1, N + 1):
        p = le(os.path.join(BASE, f"Evento {n}", f"ChuvaIDW{n}.tif"))[0][valido]
        Q = np.where(p <= lam * Sv, 0.0, (p - lam * Sv) ** 2 / (p + (1 - lam) * Sv))
        pr = Q / 1000.0 * A * (RI[n - 1] / R[n - 1]) / 3600.0
        out[n - 1] = np.sum(COEF * np.maximum(Q * pr * A, 0.0) ** EXPO * KCLS)
    return out


E_dir20 = e_direto(0.20); E_dir05 = e_direto(0.05)

# ----------------------------------------------------------- calibracao e metricas
def fit_scale(x, y, obj):
    if obj == "MQ":
        return np.sum(x * y) / np.sum(x * x)
    return np.exp(np.mean(np.log(y) - np.log(x)))


def fit_two(x1, x2, y, obj):
    """SY = c1*x1 + c2*x2 (c >= 0). MQ: minimos quadrados lineares; LOG: minimos quadrados em log"""
    if obj == "MQ":
        def f(p): return p[0] * x1 + p[1] * x2 - y
    else:
        def f(p): return np.log(np.clip(p[0] * x1 + p[1] * x2, 1e-9, None)) - np.log(y)
    best = None
    for s0 in ([y.mean() / x1.mean(), 0.0], [0.0, y.mean() / x2.mean()], [0.5 * y.mean() / x1.mean(), 0.5 * y.mean() / x2.mean()]):
        r = least_squares(f, s0, bounds=(0, np.inf))
        if best is None or r.cost < best.cost:
            best = r
    return best.x


def predict_models(model, obj):
    """devolve (sim in-sample, sim LOO aninhado)"""
    kind, xs = model
    ids = np.arange(N)
    if kind == "scale":
        x = xs[0]; c = fit_scale(x, SY, obj); sim = c * x
        loo = np.array([fit_scale(x[ids != i], SY[ids != i], obj) * x[i] for i in range(N)])
    else:
        x1, x2 = xs; p = fit_two(x1, x2, SY, obj); sim = p[0] * x1 + p[1] * x2
        loo = np.zeros(N)
        for i in range(N):
            m = ids != i; pi = fit_two(x1[m], x2[m], SY[m], obj); loo[i] = pi[0] * x1[i] + pi[1] * x2[i]
    return sim, loo


def nse(o_, s_): return 1 - np.sum((o_ - s_) ** 2) / np.sum((o_ - o_.mean()) ** 2)
def nse_log(o_, s_):
    lo, ls = np.log(o_), np.log(np.clip(s_, 1e-6, None)); return 1 - np.sum((lo - ls) ** 2) / np.sum((lo - lo.mean()) ** 2)
def ape(o_, s_): return 100 * np.abs(s_ - o_) / o_
def f2(o_, s_): r = s_ / o_; return 100 * np.mean((r >= 0.5) & (r <= 2.0))
def vies_geo(o_, s_): return 100 * (np.exp(np.mean(np.log(np.clip(s_, 1e-6, None) / o_))) - 1)


MODELOS = [
    ("SY = c·chuva do evento", ("scale", [R])),
    ("SY = c·volume total medido (T_R)", ("scale", [TR])),
    ("SY = c·escoamento direto medido", ("scale", [VD])),
    ("[vazado] SY = c·duração do evento", ("scale", [dur])),
    ("MUSLE esp.: previsão pura antiga (λ 0,05, sem base)", ("scale", [E_prev])),
    ("MUSLE esp.: direto λ 0,20, sem base", ("scale", [E_dir20])),
    ("MUSLE esp.: direto λ 0,20 + base uniforme [duração obs.]", ("scale", [E_base])),
    ("MUSLE esp.: 2 componentes (E_dir λ 0,20 + base obs.)", ("two", [E_dir20, VBo])),
    ("MUSLE esp.: 2 componentes (E_dir λ 0,05 + base obs.)", ("two", [E_dir05, VBo])),
    ("MUSLE esp.: 2 componentes (E_dir λ 0,20 + base prev. [dur. obs.])", ("two", [E_dir20, VBp])),
    ("MUSLE esp.: volume restrito ao total (usa T_R)", ("scale", [E_rest])),
]

print("=" * 132)
print("PARTICIPACAO DO MAIOR EVENTO NA VARIANCIA DO ALVO (denominador de cada NSE)")
for nome, y in (("linear (t)", SY), ("log (ln t)", np.log(SY))):
    d2 = (y - y.mean()) ** 2; o_ = np.argsort(-d2)
    print(f"  {nome:<11} maior evento = {o_[0]+1} ({100*d2[o_[0]]/d2.sum():.1f}%) | 3 maiores: " +
          ", ".join(f"ev{k+1} {100*d2[k]/d2.sum():.0f}%" for k in o_[:3]) + f" (soma {100*d2[o_[:3]].sum()/d2.sum():.0f}%)")
print("  ranking (Spearman) e erro percentual nao dependem de variancia: nenhum evento domina")

for obj, desc in (("LOG", "CALIBRACAO EM LOG (ln c = media(ln SY - ln E)); 2 componentes: minimos quadrados em log"),
                  ("MQ", "CALIBRACAO ANTERIOR (minimos quadrados lineares)")):
    print("=" * 132)
    print(desc)
    print(f"{'modelo':<66} {'NSE-log':>8} {'NSE-log':>8} {'MAPE':>7} {'MedAPE':>7} {'fator2':>7} {'vies':>7} {'Spearman':>8} | {'NSE lin':>7} {'NSE lin':>7}")
    print(f"{'':<66} {'in':>8} {'LOO':>8} {'LOO%':>7} {'LOO%':>7} {'LOO%':>7} {'geo%':>7} {'LOO':>8} | {'in':>7} {'LOO':>7}")
    for nome, mod in MODELOS:
        sim, loo = predict_models(mod, obj)
        print(f"{nome:<66} {nse_log(SY, sim):8.3f} {nse_log(SY, loo):8.3f} {ape(SY, loo).mean():7.1f} {np.median(ape(SY, loo)):7.1f} "
              f"{f2(SY, loo):7.0f} {vies_geo(SY, loo):+7.1f} {spearmanr(SY, loo)[0]:8.3f} | {nse(SY, sim):7.3f} {nse(SY, loo):7.3f}")

# ----------------------------------------------------------- incerteza (bootstrap de eventos) para modelos-chave
print("=" * 132)
print("BOOTSTRAP de eventos (2000 reamostragens; c refeito em log; metrica in-sample) - IC 95%")
chaves = [m for m in MODELOS if m[0] in ("SY = c·chuva do evento", "SY = c·volume total medido (T_R)", "MUSLE esp.: previsão pura antiga (λ 0,05, sem base)",
                                        "MUSLE esp.: direto λ 0,20, sem base", "MUSLE esp.: 2 componentes (E_dir λ 0,20 + base obs.)")]
for nome, (kind, xs) in chaves:
    if kind != "scale":
        continue
    x = xs[0]; res_l = []; res_m = []
    for _ in range(2000):
        ix = rng.integers(0, N, N)
        if np.ptp(SY[ix]) == 0: continue
        c = fit_scale(x[ix], SY[ix], "LOG"); s_ = c * x[ix]
        res_l.append(nse_log(SY[ix], s_)); res_m.append(np.median(ape(SY[ix], s_)))
    print(f"  {nome:<62} NSE-log in: mediana {np.median(res_l):6.3f} IC [{np.percentile(res_l,2.5):6.2f}; {np.percentile(res_l,97.5):5.2f}] | MedAPE: {np.median(res_m):5.1f}% IC [{np.percentile(res_m,2.5):4.1f}; {np.percentile(res_m,97.5):4.1f}]")
print("=" * 132)
