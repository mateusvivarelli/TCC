"""
TABELAS DO TCC com os dados de TODOS os eventos (15/10/2026; modelo so com escoamento direto desde 26/10/2026;
MODELO OFICIAL desde 28/10/2026: CN-I, lambda 0,05 com S convertido por Woodward et al. 2003, sem termo de base, c em log, LOO).
Grava arquivos Markdown em TCC_Texto/tabelas/:

  tab_eventos.md          caracteristicas dos 17 eventos (datas, duracao, chuva, intensidade, pico, vazao inicial)
  tab_volumes.md          volume total, vazao de base, escoamento direto medido x SCS-CN, sedimento medido
  tab_resultados.md       sedimento medido x simulado por modelo (validacao leave-one-out) e erros
  tab_qpico.md            vazao de pico medida x calculada pelo HU-SCS (Fase 1)
  tab_classes_uso.md      contribuicao por classe de uso (area x sedimento)
  tab_classes_solo.md     contribuicao por classe de solo
  tab_parametros.md       parametros fixos e calibrados dos modelos
  tab_mc_mfm_eventos.md   Tabela 10: medido, MC e MFM (ajuste e validacao cruzada) e razao SCS-CN/medido por evento
  tab_evento11_passo_a_passo.md  evento 11 do inicio ao fim (formato da Tabela 9)
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
LAM = 0.05   # modelo oficial: lambda 0,05 com S convertido (Woodward et al., 2003)
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


K, ds0 = le(os.path.join(DI, "K_raster.tif")); C, _ = le(os.path.join(DI, "C_raster.tif")); LS, _ = le(os.path.join(DI, "LS_moore.tif"))
gt = ds0.GetGeoTransform(); ny, nx = K.shape; A = abs(gt[1] * gt[5])
o = gdal.Warp("", gdal.Open(os.path.join(DI, "S - Seco.tif")), format="MEM", width=nx, height=ny,
              outputBounds=(gt[0], gt[3] + ny * gt[5], gt[0] + nx * gt[1], gt[3]), dstSRS=ds0.GetProjection(), resampleAlg=gdal.GRA_NearestNeighbour)
S = o.GetRasterBand(1).ReadAsArray().astype(np.float64); S = np.where(S > -1e30, S, np.nan)
valido = np.isfinite(S) & np.isfinite(K) & np.isfinite(C) & np.isfinite(LS)
KCLS = (K * C * LS)[valido]
S20 = S[valido]                                       # S do CN-I para lambda 0,20 (mm)
Sv = 25.4 * 1.33 * (S20 / 25.4) ** 1.15               # Woodward et al. (2003): S_0,05 (mm)

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
def qf(i, V=None, lam=LAM):
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


# modelo adotado em 26/10/2026: so escoamento direto, um coeficiente c em log (sem termo de vazao de base)
fit1 = lambda x, y: np.exp(np.mean(np.log(y) - np.log(x)))
loo1 = lambda x: np.array([fit1(x[ids != i], SY[ids != i]) * x[i] for i in range(N)])
Bcalc = loo1(Ecalc); Bforc = loo1(Eforc)
ch = np.array([np.exp(np.mean(np.log(SY[ids != i]) - np.log(R[ids != i]))) * R[i] for i in range(N)])
Dq = TR * QPm; ic = np.zeros(N)
for i in range(N):
    m = ids != i; b, a = np.polyfit(np.log(Dq[m]), np.log(SY[m] / KLSC), 1); ic[i] = np.exp(a) * Dq[i] ** b * KLSC
c_calc = fit1(Ecalc, SY); c_forc = fit1(Eforc, SY); b_ic, a_ic = np.polyfit(np.log(Dq), np.log(SY / KLSC), 1)
print(f"modelo calculado c={c_calc:.5f} | modelo forcado c={c_forc:.5f} | IC alfa={np.exp(a_ic):.4f} beta={b_ic:.4f}")

# ================================================================= tabelas
dt = lambda x: pd.to_datetime(x).strftime("%d/%m/%y %Hh")
md(["Evento", "Início", "Fim", "Dur. (h)", "P DBT5 (mm)", "P Campo Limpo (mm)", "R (mm)", "RI (mm/h)", "Q pico (m³/s)", "Q inicial (m³/s)", "T chuva (h)"],
   [[str(n + 1), dt(EV[n]["Inicio"]), dt(EV[n]["Fim"]), br(dur[n], 0), br(EV[n]["chuva_p1_mm"]), br(EV[n]["chuva_p2_mm"]), br(R[n]), br(RI[n]), br(QPm[n]), br(Qb0[n], 2), br(durR[n], 0)] for n in range(N)]
   + [["**Média**", "", "", br(dur.mean(), 0), br(np.mean([r["chuva_p1_mm"] for r in EV])), br(np.mean([r["chuva_p2_mm"] for r in EV])), br(R.mean()), br(RI.mean()), br(QPm.mean()), br(Qb0.mean(), 2), br(durR.mean(), 0)]],
   "tab_eventos.md")

md(["Evento", "Volume total T_R (10³ m³)", "Vazão de base Σ Bt (10³ m³)", "Base (% do total)", "Direto medido (10³ m³)", "SCS-CN, λ = 0,05 com S convertido (10³ m³)", "SCS-CN / medido", "Sedimento medido (t)"],
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
md(["Evento", "Medido (t)", "c*chuva (t)", "erro %", "Calculado (t)", "erro %", "Forçado (t)", "erro %", "IC (t)", "erro %"], linhas, "tab_resultados.md")

# ---- conferencia com o CSV do script oficial (calcular_sy_lambda005_woodward.py)
OFI = pd.read_csv(os.path.join(DI, "comparacao_SY_lambda005_woodward.csv")).sort_values("evento")
for rot, a_, b_ in (("MC LOO", Bcalc, OFI.SY_calc_LOO_t), ("MFM LOO", Bforc, OFI.SY_forc_LOO_t), ("soma E calc", Ecalc, OFI.soma_E_unit_calc_t),
                    ("soma E forc", Eforc, OFI.soma_E_unit_forc_t), ("V SCS", Vscs, OFI.V_dir_SCS_m3), ("c*chuva LOO", ch, OFI.SY_chuva_LOO_t), ("IC LOO", ic, OFI.SY_IC_LOO_t)):
    dif = np.max(np.abs(a_ / b_.to_numpy() - 1))
    print(f"conferencia {rot}: diferenca relativa maxima contra o CSV oficial = {dif:.2e}")
    assert dif < 1e-3, rot
assert abs(c_calc - 0.0344) < 5e-5 and abs(c_forc - 0.0222) < 5e-5, (c_calc, c_forc)

# ---- Tabela 10 por evento: medido, MC e MFM (ajuste e validacao cruzada), razao SCS-CN / medido
sg = lambda v: f"{v:+.0f}"
ajc = c_calc * Ecalc; ajf = c_forc * Eforc
md(["Evento", "Medido", "MC, ajuste", "Erro no ajuste (%)", "MC, validação cruzada", "Erro (%)", "MFM, ajuste", "Erro no ajuste (%)", "MFM, validação cruzada", "Erro (%)", "SCS-CN / medido (escoamento direto)"],
   [[str(n + 1), br(SY[n], 0), br(ajc[n], 0), sg(100 * (ajc[n] - SY[n]) / SY[n]), br(Bcalc[n], 0), sg(100 * (Bcalc[n] - SY[n]) / SY[n]),
     br(ajf[n], 0), sg(100 * (ajf[n] - SY[n]) / SY[n]), br(Bforc[n], 0), sg(100 * (Bforc[n] - SY[n]) / SY[n]), br(Vscs[n] / VD[n], 2)] for n in range(N)],
   "tab_mc_mfm_eventos.md")

qp = pd.read_csv(os.path.join(DI, "comparacao_qpico_convolucao_medido_vs_calculado.csv")).sort_values("evento")
md(["Evento", "Q pico medido (m³/s)", "Q pico calculado, HU-SCS (m³/s)", "Erro (%)"],
   [[str(int(r.evento)), br(r.Q_pico_medido_planilha), br(r.Qp_calc_convolucao), f"{r['erro_%']:+.0f}"] for _, r in qp.iterrows()]
   + [["**Média**", br(qp.Q_pico_medido_planilha.mean()), br(qp.Qp_calc_convolucao.mean()), f"{qp['erro_%'].mean():+.1f} (absoluto {qp['erro_%'].abs().mean():.1f})".replace(".", ",")]], "tab_qpico.md")

# ---- contribuicao por classe (mapas medios dos dois modelos)
with open(os.path.join(BASE, "Evento11_Auditoria", "dados_evento11.pkl"), "rb") as fh:
    D = pickle.load(fh)
iy, ix = D["iy"], D["ix"]
mc, _ = le(os.path.join(DI, "SY_medio_eventos_l05w.tif")); mf, _ = le(os.path.join(DI, "SY_medio_eventos_forcado_l05w.tif"))
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
    ["Número de curva", "CN-II da ANA convertido para CN-I", "ANA (2024); conversão de Chow, Maidment e Mays (1988)"],
    ["λ (razão de abstração inicial)", "0,05", "Woodward et al. (2003)"],
    ["Retenção S com λ = 0,05", "S0,05 = 25,4 * 1,33 * (S0,20 / 25,4)^1,15 (mm)", "Woodward et al. (2003), S0,20 do CN-I"],
    ["Peso do posto DBT5 / Campo Limpo na lâmina do evento", "0,307 / 0,693", "mínimos quadrados nos 17 eventos"],
    ["P (práticas conservacionistas)", "1,0", "sem práticas na bacia"],
    ["Modelo calculado: c (t por unidade de E_unit)", br(c_calc, 4), "calibrado em log, 17 eventos; só escoamento direto"],
    ["Modelo forçado: c (t por unidade de E_unit)", br(c_forc, 4), "calibrado em log, 17 eventos; escoamento direto medido"],
    ["IC refeita: α e β", f"{br(np.exp(a_ic), 3)} e {br(b_ic, 3)}", "regressão em log, K = 0,031, LS = 0,536, C = 0,267 (IC: 0,277 e 0,807)"]], "tab_parametros.md")

# ================================================================= evento 11 passo a passo (formato da Tabela 9 do Doc)
n11 = 10; e11 = EV[n11]
idx = -np.ones((ny, nx), dtype=int); idx[valido] = np.arange(valido.sum())
col = int((330180.0 - gt[0]) / gt[1]); lin_ = int((gt[3] - 7432860.0) / abs(gt[5])); j = idx[lin_, col]
assert j >= 0
_w = gdal.Warp("", gdal.Open(os.path.join(DI, "CN TCC.tif")), format="MEM", width=nx, height=ny,
               outputBounds=(gt[0], gt[3] + ny * gt[5], gt[0] + nx * gt[1], gt[3]), dstSRS=ds0.GetProjection(), resampleAlg=gdal.GRA_NearestNeighbour)
cn2_al = _w.GetRasterBand(1).ReadAsArray().astype(float)
cn2_pix = cn2_al[lin_, col]
cn1_pix = 4.2 * cn2_pix / (10 - 0.058 * cn2_pix)
S20_pix = 25.4 * (1000 / cn1_pix - 10); S05_pix = 25.4 * 1.33 * (S20_pix / 25.4) ** 1.15
assert abs(S05_pix - Sv[j]) < 0.5 and abs(S20_pix - S20[j]) < 0.5, (S05_pix, Sv[j], S20_pix, S20[j])
P11 = Pv[n11]; Pp = P11[j]; Q_all = qf(n11); Qp = Q_all[j]
pr_pix = Qp / 1000.0 * A * (RI[n11] / R[n11]) / 3600.0
Ke, Ce, LSe = K[lin_, col], C[lin_, col], LS[lin_, col]
Eun = COEF * (Qp * pr_pix * A) ** EXPO * Ke * Ce * LSe
uso_pix = [D["usoc"][k] for k in range(len(D["iy"])) if D["iy"][k] == lin_ and D["ix"][k] == col]
solo_pix = [D["solo"][k] for k in range(len(D["iy"])) if D["iy"][k] == lin_ and D["ix"][k] == col]
cn1_med = np.mean(25400.0 / (S20 + 254.0))
loo_c, loo_f = Bcalc[n11], Bforc[n11]
sem_esc = 100 * np.mean(Q_all <= 0)
e_sum = Ecalc[n11]
print(f"pixel exemplo: linha {lin_}, coluna {col}, uso {uso_pix}, solo {solo_pix}, P {Pp:.2f}, CN-II {cn2_pix:.1f}, CN-I {cn1_pix:.2f}, S20 {S20_pix:.1f}, S05 {S05_pix:.1f}, "
      f"Q {Qp:.2f}, pr {pr_pix:.3e}, K {Ke:.4f} C {Ce:.3f} LS {LSe:.3f}, E_unit {Eun:.4f}")
d2 = lambda v: br(v, 2)
f_ = lambda v, d=1: br(v, d)
lam_ = LAM * S05_pix
linhas11 = [
    ["Chuva medida", "DBT5 / Campo Limpo", f"{f_(e11['chuva_p1_mm'])} mm / {f_(e11['chuva_p2_mm'])} mm"],
    ["", "lâmina do evento R = 0,307 * P1 + 0,693 * P2", f"{f_(R[n11])} mm"],
    ["", "intensidade máxima RI; razão RI/R", f"{f_(RI[n11])} mm/h; {br(RI[n11] / R[n11], 3)} por hora"],
    ["Chuva do pixel (IDW)", "média nos pixels de cálculo (intervalo no raster)", f"{f_(P11.mean())} mm ({f_(P11.min())} a {f_(P11.max())} mm)"],
    ["Retenção", "CN-I médio; S0,20 médio; S0,05 médio (convertido)", f"{f_(cn1_med)}; {f_(S20.mean())} mm; {f_(Sv.mean())} mm"],
    ["Escoamento direto", "Q médio dos pixels; pixels sem escoamento", f"{f_(Q_all.mean())} mm; {f_(sem_esc, 0)}%"],
    ["", "volume calculado pelo SCS-CN / medido", f"{f_(Vscs[n11] / 1e3, 0)} mil m³ / {f_(VD[n11] / 1e3, 0)} mil m³ (razão {d2(Vscs[n11] / VD[n11])})"],
    ["Pixel de exemplo", "posição; uso; solo", f"E 330,18 km; N 7.432,86 km; {uso_pix[0].lower()}; {solo_pix[0]}"],
    ["", "chuva P; CN-II -> CN-I; S0,20 -> S0,05",
     f"{f_(Pp)} mm; {f_(cn2_pix)} -> {f_(cn1_pix)}; {f_(S20_pix)} mm -> {f_(S05_pix)} mm"],
    ["", "abstração inicial λS; escoamento Q",
     f"{f_(lam_)} mm; ({f_(Pp)} - {f_(lam_)})² / ({f_(Pp)} + 0,95 * {f_(S05_pix)}) = {d2(Qp)} mm"],
    ["", "vazão de pico local pr", f"{d2(Qp)}/1000 * 897,49 * {br(RI[n11] / R[n11], 3)} / 3600 = {br(pr_pix * 1e4, 2)} * 10^-4 m³/s"],
    ["", "K; C; LS", f"{br(Ke, 4)}; {br(Ce, 3)}; {br(LSe, 3)}"],
    ["", "índice de erosão E_unit",
     f"11,8 * ({d2(Qp)} * {br(pr_pix * 1e4, 2)} * 10^-4 * 897,49)^0,56 * {br(Ke, 4)} * {br(Ce, 3)} * {br(LSe, 3)} = {br(Eun, 3)}"],
    ["", "sedimento do pixel c * E_unit", f"{br(c_calc, 4)} * {br(Eun, 3)} = {br(c_calc * Eun, 4)} t ({br(1000 * c_calc * Eun, 1)} kg)"],
    ["Evento (MC)", "soma de E_unit sobre os pixels", br(e_sum, 0)],
    ["", "sedimento simulado SY = c * soma(E_unit) (ajuste)", f"{br(c_calc, 4)} * {br(e_sum, 0)} = {br(ajc[n11], 0)} t ({sg(100 * (ajc[n11] - SY[n11]) / SY[n11])}%)"],
    ["", "validação cruzada (c refeito sem o evento 11)", f"{br(loo_c, 0)} t ({sg(100 * (loo_c - SY[n11]) / SY[n11])}%)"],
    ["Evento (MFM)", "soma de E_unit com o escoamento forçado ao medido", br(Eforc[n11], 0)],
    ["", "sedimento simulado (ajuste, c = " + br(c_forc, 4) + "); validação cruzada", f"{br(ajf[n11], 0)} t ({sg(100 * (ajf[n11] - SY[n11]) / SY[n11])}%); {br(loo_f, 0)} t ({sg(100 * (loo_f - SY[n11]) / SY[n11])}%)"],
    ["Medido", "SY_obs = soma(Q * CSS)", f"{br(SY[n11], 0)} t"],
]
md(["Etapa", "Grandeza", "Valor"], linhas11, "tab_evento11_passo_a_passo.md")
print("tabelas ok:", sorted(os.listdir(OUT)))
