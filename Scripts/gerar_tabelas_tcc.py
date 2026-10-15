"""
TABELAS DO TCC com os dados de TODOS os eventos (15/10/2026). Grava arquivos Markdown em TCC_Texto/tabelas/:

  tab_eventos.md          caracteristicas dos 17 eventos (datas, duracao, chuva, intensidade, pico, vazao inicial)
  tab_volumes.md          volume total, vazao de base, escoamento direto medido x SCS-CN, sedimento medido
  tab_resultados.md       sedimento medido x simulado por modelo (validacao leave-one-out) e erros
  tab_qpico.md            vazao de pico medida x calculada pelo HU-SCS (Fase 1)
  tab_classes_uso.md      contribuicao por classe de uso (area x sedimento)
  tab_classes_solo.md     contribuicao por classe de solo
  tab_parametros.md       parametros fixos e calibrados dos modelos
"""
import os
import pickle
import sys

import numpy as np
import pandas as pd
from osgeo import gdal
from scipy.optimize import least_squares

gdal.UseExceptions()
sys.stdout.reconfigure(encoding="utf-8")
BASE = r"C:\TCC"; DI = os.path.join(BASE, "Dados Iniciais"); OUT = os.path.join(BASE, "TCC_Texto", "tabelas")
os.makedirs(OUT, exist_ok=True)
COEF, EXPO, N = 11.8, 0.56, 17
KLSC = 0.031 * 0.536 * 0.267


def le(p):
    ds = gdal.Open(p); b = ds.GetRasterBand(1)
    a = b.ReadAsArray().astype(np.float64); nd = b.GetNoDataValue()
    ok = np.isfinite(a) & (a > -1e30)
    if nd is not None:
        ok &= a != nd
    return np.where(ok, a, np.nan), ds


def br(v, d=1):
    return f"{v:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def md(cab, linhas, nome):
    t = "| " + " | ".join(cab) + " |\n|" + "|".join(["---"] * len(cab)) + "|\n" + "\n".join("| " + " | ".join(l) + " |" for l in linhas) + "\n"
    open(os.path.join(OUT, nome), "w", encoding="utf-8", newline="\n").write(t)


K, ds0 = le(os.path.join(DI, "K_raster.tif")); C, _ = le(os.path.join(DI, "C_raster.tif")); LS, _ = le(os.path.join(DI, "LS_raster.tif"))
gt = ds0.GetGeoTransform(); ny, nx = K.shape; A = abs(gt[1] * gt[5])
o = gdal.Warp("", gdal.Open(os.path.join(DI, "S - Seco.tif")), format="MEM", width=nx, height=ny,
              outputBounds=(gt[0], gt[3] + ny * gt[5], gt[0] + nx * gt[1], gt[3]), dstSRS=ds0.GetProjection(), resampleAlg=gdal.GRA_NearestNeighbour)
S = o.GetRasterBand(1).ReadAsArray().astype(np.float64); S = np.where(S > -1e30, S, np.nan)
valido = np.isfinite(S) & np.isfinite(K) & np.isfinite(C) & np.isfinite(LS)
KCLS = (K * C * LS)[valido]; Sv = S[valido]

ev = pd.read_excel(os.path.join(DI, "eventos_processados_manuais.xlsx"), sheet_name="Sheet1").iloc[:18]
EV = [ev.iloc[0 if n == 1 else n] for n in range(1, N + 1)]
h = pd.read_excel(os.path.join(DI, "Dados_finais_histereses_corrigido.xlsx"), sheet_name="Planilha1").iloc[:, :8]
h.columns = ["Data", "P1", "P2", "Ptot", "Q", "CSS", "Bt", "CSSBt"]; h["Data"] = pd.to_datetime(h["Data"]); h = h.set_index("Data")
SY = np.array([float(r["SYY_t"]) for r in EV]); TR = np.array([float(r["T_R_m3"]) for r in EV]); QPm = np.array([float(r["Q_pico"]) for r in EV])
RI = np.array([float(r["Intensidade_60min_mm/h"]) for r in EV]); R = np.array([float(r["Chuva_evento_mm"]) for r in EV]); Qb0 = np.array([float(r["Qb_inicio"]) for r in EV])
durR = np.array([max(r["Tempo_precipitacao_p1_h"], r["Tempo_precipitacao_p2_h"]) for r in EV]); dur = np.array([float(r["Duracao_horas"]) for r in EV])
BTV = np.array([h.loc[r["Inicio"]:r["Fim"]].Bt.sum() * 3600 for r in EV]); VD = TR - BTV
Pv = [le(os.path.join(BASE, f"Evento {n}", f"ChuvaIDW{n}.tif"))[0][valido] for n in range(1, N + 1)]
ids = np.arange(N)

# ---------------------------------------------------------------- escoamento SCS-CN e E_unit (calculado e forcado)
def qf(i, V=None, lam=0.20):
    p = Pv[i]; Q = np.where(p <= lam * Sv, 0.0, (p - lam * Sv) ** 2 / (p + (1 - lam) * Sv))
    if V is not None:
        Q = np.minimum(V / (Q.sum() / 1000.0 * A) * Q, p)
    return Q


def Esum(Q, i):
    pr = Q / 1000.0 * A * (RI[i] / R[i]) / 3600.0
    return np.sum(COEF * np.maximum(Q * pr * A, 0.0) ** EXPO * KCLS)


Vscs = np.array([qf(i).sum() / 1000.0 * A for i in range(N)])
Ecalc = np.array([Esum(qf(i), i) for i in range(N)])
Eforc = np.array([Esum(qf(i, VD[i]), i) for i in range(N)])
base_ch = Qb0 * durR * 3600.0


def fit2(x1, x2, y):
    f = lambda p: np.log(np.clip(p[0] * x1 + p[1] * x2, 1e-9, None)) - np.log(y)
    best = None
    for s0 in ([y.mean() / x1.mean(), 0.0], [0.0, y.mean() / x2.mean()], [0.5 * y.mean() / x1.mean(), 0.5 * y.mean() / x2.mean()]):
        r = least_squares(f, s0, bounds=(0, np.inf), x_scale="jac")
        if best is None or r.cost < best.cost: best = r
    return best.x


def loo2(x1, x2):
    out = np.zeros(N)
    for i in range(N):
        m = ids != i; p = fit2(x1[m], x2[m], SY[m]); out[i] = p[0] * x1[i] + p[1] * x2[i]
    return out


Bcalc = loo2(Ecalc, base_ch); Bforc = loo2(Eforc, BTV)
ch = np.array([np.exp(np.mean(np.log(SY[ids != i]) - np.log(R[ids != i]))) * R[i] for i in range(N)])
Dq = TR * QPm; ic = np.zeros(N)
for i in range(N):
    m = ids != i; b, a = np.polyfit(np.log(Dq[m]), np.log(SY[m] / KLSC), 1); ic[i] = np.exp(a) * Dq[i] ** b * KLSC
p_calc = fit2(Ecalc, base_ch, SY); p_forc = fit2(Eforc, BTV, SY); b_ic, a_ic = np.polyfit(np.log(Dq), np.log(SY / KLSC), 1)
print(f"modelo calculado c1={p_calc[0]:.5f} c2={p_calc[1]:.6f} | modelo forcado c1={p_forc[0]:.5f} c2={p_forc[1]:.6f} | IC alfa={np.exp(a_ic):.4f} beta={b_ic:.4f}")

# ================================================================= tabelas
dt = lambda x: pd.to_datetime(x).strftime("%d/%m/%y %Hh")
md(["Evento", "Início", "Fim", "Dur. (h)", "P DBT5 (mm)", "P Campo Limpo (mm)", "R (mm)", "RI (mm/h)", "Q pico (m³/s)", "Q inicial (m³/s)", "T chuva (h)"],
   [[str(n + 1), dt(EV[n]["Inicio"]), dt(EV[n]["Fim"]), br(dur[n], 0), br(EV[n]["chuva_p1_mm"]), br(EV[n]["chuva_p2_mm"]), br(R[n]), br(RI[n]), br(QPm[n]), br(Qb0[n], 2), br(durR[n], 0)] for n in range(N)]
   + [["**Média**", "", "", br(dur.mean(), 0), br(np.mean([r["chuva_p1_mm"] for r in EV])), br(np.mean([r["chuva_p2_mm"] for r in EV])), br(R.mean()), br(RI.mean()), br(QPm.mean()), br(Qb0.mean(), 2), br(durR.mean(), 0)]],
   "tab_eventos.md")

md(["Evento", "Volume total T_R (10³ m³)", "Vazão de base Σ Bt (10³ m³)", "Base (% do total)", "Direto medido (10³ m³)", "SCS-CN, λ = 0,20 (10³ m³)", "SCS-CN / medido", "Sedimento medido (t)"],
   [[str(n + 1), br(TR[n] / 1e3, 0), br(BTV[n] / 1e3, 0), br(100 * BTV[n] / TR[n], 0), br(VD[n] / 1e3, 0), br(Vscs[n] / 1e3, 0), br(Vscs[n] / VD[n], 2), br(SY[n], 0)] for n in range(N)]
   + [["**Total**", br(TR.sum() / 1e3, 0), br(BTV.sum() / 1e3, 0), br(100 * BTV.sum() / TR.sum(), 0), br(VD.sum() / 1e3, 0), br(Vscs.sum() / 1e3, 0), br(Vscs.sum() / VD.sum(), 2), br(SY.sum(), 0)]],
   "tab_volumes.md")

ape = lambda s_: 100 * np.abs(s_ - SY) / SY
f2 = lambda s_: 100 * np.mean((s_ / SY >= 0.5) & (s_ / SY <= 2.0))
linhas = []
for n in range(N):
    lin = [str(n + 1), br(SY[n], 0)]
    for s_ in (ch, Bcalc, Bforc, ic):
        lin += [br(s_[n], 0), f"{100*(s_[n]-SY[n])/SY[n]:+.0f}".replace("+", "+")]
    linhas.append(lin)
linhas.append(["**Erro mediano (%)**", ""] + sum([[ "", br(np.median(ape(s_)), 0)] for s_ in (ch, Bcalc, Bforc, ic)], []))
linhas.append(["**Dentro de fator 2 (%)**", ""] + sum([["", br(f2(s_), 0)] for s_ in (ch, Bcalc, Bforc, ic)], []))
md(["Evento", "Medido (t)", "c·chuva (t)", "erro %", "Calculado (t)", "erro %", "Forçado (t)", "erro %", "IC (t)", "erro %"], linhas, "tab_resultados.md")

qp = pd.read_csv(os.path.join(DI, "comparacao_qpico_convolucao_medido_vs_calculado.csv")).sort_values("evento")
md(["Evento", "Q pico medido (m³/s)", "Q pico calculado, HU-SCS (m³/s)", "Erro (%)"],
   [[str(int(r.evento)), br(r.Q_pico_medido_planilha), br(r.Qp_calc_convolucao), f"{r['erro_%']:+.0f}"] for _, r in qp.iterrows()]
   + [["**Média**", br(qp.Q_pico_medido_planilha.mean()), br(qp.Qp_calc_convolucao.mean()), f"{qp['erro_%'].mean():+.1f} (absoluto {qp['erro_%'].abs().mean():.1f})".replace(".", ",")]], "tab_qpico.md")

# ---- contribuicao por classe (mapas medios dos dois modelos)
with open(os.path.join(BASE, "Evento11_Auditoria", "dados_evento11.pkl"), "rb") as fh:
    D = pickle.load(fh)
iy, ix = D["iy"], D["ix"]
mc, _ = le(os.path.join(DI, "SY_medio_eventos_b2.tif")); mf, _ = le(os.path.join(DI, "SY_medio_eventos_forcado.tif"))
sc, sf = mc[iy, ix], mf[iy, ix]; ok = np.isfinite(sc) & np.isfinite(sf)
for campo, nome, arq in (("usoc", "uso", "tab_classes_uso.md"), ("solo", "solo", "tab_classes_solo.md")):
    cls = np.array(D[campo], dtype=object)[ok]; a_ = sc[ok]; b_ = sf[ok]; linhas = []
    for cl in sorted(set(cls), key=lambda c: -np.sum(cls == c)):
        m = cls == cl
        if cl == "":
            continue
        linhas.append([cl, br(100 * m.mean(), 1), br(100 * a_[m].sum() / a_.sum(), 1), br(1000 * a_[m].mean(), 2), br(100 * b_[m].sum() / b_.sum(), 1), br(1000 * b_[m].mean(), 2),
                       br(100 * a_[m].sum() / a_.sum() / (100 * m.mean()) * 100, 0)])
    md([f"Classe de {nome}", "Área (%)", "Sedimento, modelo calculado (%)", "kg/pixel, calculado", "Sedimento, modelo forçado (%)", "kg/pixel, forçado", "Contribuição / área, calculado (%)"], linhas, arq)

tK, tC = D["tab_K"], D["tab_C"]
solo_v = np.array(D["solo"], dtype=object)[ok]; uso_v = np.array(D["usoc"], dtype=object)[ok]
lin = [[f"Solo: {r.Subordem}", br(float(r["first"]), 4), br(100 * np.mean(solo_v == r.Subordem), 1)] for _, r in tK.sort_values("first", ascending=False).iterrows()]
lin += [[f"Uso: {r.CLASSE}", br(float(r["first"]), 3), br(100 * np.mean(uso_v == r.CLASSE), 1)] for _, r in tC.sort_values("first", ascending=False).iterrows()]
md(["Classe", "Fator (K para solo; C para uso)", "Pixels de cálculo (%)"], lin, "tab_fatores_classes.md")
md(["Parâmetro", "Valor", "Origem"],
   [["Coeficiente de Williams (11,8) e expoente (0,56)", "11,8 e 0,56", "Williams (1975), mantidos"],
    ["λ (razão de abstração inicial)", "0,20", "valor padrão do SCS-CN (CN tabelado)"],
    ["Peso do posto DBT5 / Campo Limpo na lâmina do evento", "0,307 / 0,693", "mínimos quadrados nos 17 eventos"],
    ["P (práticas conservacionistas)", "1,0", "sem práticas na bacia"],
    ["Modelo calculado: c₁ (t por unidade de E_unit)", br(p_calc[0], 4), "calibrado em log, 17 eventos"],
    ["Modelo calculado: c₂ (t por m³ de volume de base de referência)", br(p_calc[1], 5), "calibrado em log, 17 eventos"],
    ["Modelo forçado: c₁", br(p_forc[0], 4), "calibrado em log, 17 eventos"],
    ["Modelo forçado: c₂ (t por m³ de vazão de base medida)", br(p_forc[1], 5), "calibrado em log, 17 eventos"],
    ["IC refeita: α e β", f"{br(np.exp(a_ic), 3)} e {br(b_ic, 3)}", "regressão em log, K = 0,031, LS = 0,536, C = 0,267 (IC: 0,277 e 0,807)"]], "tab_parametros.md")
print("tabelas ok:", sorted(os.listdir(OUT)))
