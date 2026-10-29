"""Revisao 29/10, R2: bootstrap (4.000) e Wilcoxon pareado das diferencas de erro; sensibilidade sem ev 15 e sem ev 17;
erro contra tamanho do evento; alvo so do escoamento direto; numeros citados nas propostas 5 e 6."""
import numpy as np, pandas as pd
from scipy.stats import wilcoxon, spearmanr
S = "/tmp/claude-0/-home-user-TCC/f521a486-b85c-5056-a3b4-5f7d885f5fd6/scratchpad"
d = pd.read_csv(f"{S}/eventos_recalc.csv"); off = pd.read_csv("Dados Iniciais/comparacao_SY_lambda005_woodward.csv")
SY = d.SY.values; N = 17; ids = np.arange(N)
fit1 = lambda x, y: np.exp(np.mean(np.log(y) - np.log(x)))
ape = lambda o, s: 100*np.abs(s-o)/o
nse = lambda o, s: 1 - np.sum((o-s)**2)/np.sum((o-o.mean())**2)
def loo1(x, y, m):
    x, y = x[m], y[m]; k = np.arange(len(y)); return np.array([fit1(x[k != i], y[k != i])*x[i] for i in k])
def looic(y, m):
    Dq = (d.TR.values*d.Qp.values)[m]; y = y[m]; K = .031*.536*.267; k = np.arange(len(y)); out = []
    for i in k:
        b, a = np.polyfit(np.log(Dq[k != i]), np.log(y[k != i]/K), 1); out.append(np.exp(a)*Dq[i]**b*K)
    return np.array(out)
X = {"MC": off.soma_E_unit_calc_t.values, "MFM": off.soma_E_unit_forc_t.values, "chuva": d.R_planilha.values, "V_dir": d.VD.values, "T_R": d.TR.values}
def met(y, s): return np.median(ape(y, s)), 100*np.mean((s/y >= .5) & (s/y <= 2)), nse(np.log(y), np.log(s)), spearmanr(y, s)[0]
def todos(y, m):
    r = {k: loo1(v, y, m) for k, v in X.items()}; r["IC"] = looic(y, m); return r
print("== sensibilidade (LOO refeito no subconjunto): MedAPE / fator2 / NSElog / Spearman")
for rot, m in (("todos", ids >= 0), ("sem ev15", ids != 14), ("sem ev17", ids != 16), ("sem 15 e 17", (ids != 14) & (ids != 16))):
    r = todos(SY, m); print(rot, {k: tuple(np.round(met(SY[m], v), 2)) for k, v in r.items()})
r = todos(SY, ids >= 0)
rng = np.random.default_rng(29102026)
print("\n== diferencas pareadas do erro absoluto % (LOO): A - B (negativo = A melhor)")
for a, b in (("MC", "chuva"), ("MFM", "V_dir"), ("MFM", "IC"), ("MFM", "T_R"), ("V_dir", "IC")):
    dd = ape(SY, r[a]) - ape(SY, r[b]); bs = np.array([np.median(rng.choice(dd, N)) for _ in range(4000)])
    w = wilcoxon(ape(SY, r[a]), ape(SY, r[b]))
    print(f"{a} x {b}: mediana {np.median(dd):+.1f}; IC95% bootstrap [{np.percentile(bs,2.5):+.1f}; {np.percentile(bs,97.5):+.1f}]; A melhor em {np.sum(dd<0)}/17; Wilcoxon p = {w.pvalue:.3f}")
    # diferenca das medianas (o que o texto compara) por bootstrap
    bm = []
    for _ in range(4000):
        k = rng.integers(0, N, N); bm.append(np.median(ape(SY[k], r[a][k])) - np.median(ape(SY[k], r[b][k])))
    print(f"      diferenca das MedAPE {np.median(ape(SY, r[a]))-np.median(ape(SY, r[b])):+.1f}; IC95% [{np.percentile(bm,2.5):+.1f}; {np.percentile(bm,97.5):+.1f}]")
print("\n== evento a evento (erro LOO %, sinal)")
t = pd.DataFrame({k: np.round(100*(v-SY)/SY) for k, v in r.items()}); t.insert(0, "SY", SY.round()); t.index = ids+1; print(t.to_string())
for k, v in r.items():
    e = np.log(v/SY); print(f"{k}: Spearman(erro log, SY) {spearmanr(e, SY)[0]:+.2f}; (|erro|, SY) {spearmanr(np.abs(e), SY)[0]:+.2f}; (erro log, chuva) {spearmanr(e, d.R_planilha)[0]:+.2f}")
print("MC: superestima", np.sum(r["MC"] > SY), "subestima", np.sum(r["MC"] < SY), "razao min/max", (r["MC"]/SY).min().round(3), (r["MC"]/SY).max().round(3))
print("MFM fora do fator 2:", ids[(r["MFM"]/SY < .5) | (r["MFM"]/SY > 2)]+1, (r["MFM"]/SY)[16].round(3))
# concentracao por m3 de escoamento direto
cd = SY/d.VD.values*1e6; print("\nSY/V_dir mg/L min/max", cd.min().round(0), cd.max().round(0), "sem 17 max", np.sort(cd)[-2].round(0))
print("media ev1-6", cd[:6].mean().round(0), "ev14-17", cd[13:].mean().round(0), "ev1-11 (2018/19)", cd[:11].mean().round(0), "ev12-17 (2019/20)", cd[11:].mean().round(0))
e = 100*(r["MFM"]-SY)/SY; print("erro MFM ev1-6", e[:6].round(0), "ev14-17", e[13:].round(0))
print("Bt/T_R por evento min/max/total", (d.SBt/d.TR).min().round(3), (d.SBt/d.TR).max().round(3), (d.SBt.sum()/d.TR.sum()).round(3), "V_dir total", d.VD.sum()/1e6, "T_R total", d.TR.sum()/1e6, "V_SCS total", off.V_dir_SCS_m3.sum()/1e6)
print("coef. escoamento direto x chuva (Pearson)", np.corrcoef(d.VD/(d.R_planilha/1000*138.08e6), d.R_planilha)[0, 1].round(2))
# alvo so do escoamento direto (concentracao igual a da mistura a cada hora)
h = pd.read_excel("Dados Iniciais/Dados_finais_histereses_corrigido.xlsx").iloc[:, :8]; h.columns = ["Data", "P1", "P2", "Pt", "Q", "CSS", "Bt", "CB"]; h = h.set_index(pd.to_datetime(h.Data))
ev = pd.read_excel("Dados Iniciais/eventos_processados_manuais.xlsx").iloc[:18]; rows = [ev.iloc[0]] + [ev.iloc[n] for n in range(2, 18)]
SYd = np.array([((w.Q-w.Bt)*w.CSS).sum()*3600/1e6 for w in (h.loc[q["Inicio"]:q["Fim"]] for q in rows)])
print(f"\nalvo direto: soma {SYd.sum():.0f} t de {SY.sum():.0f} t ({100*SYd.sum()/SY.sum():.1f}%)")
for k in ("MC", "MFM", "chuva", "V_dir"):
    s = loo1(X[k], SYd, ids >= 0); print(f"  {k} com alvo direto: {tuple(np.round(met(SYd, s), 2))}")
s = looic(SYd, ids >= 0); print("  IC com alvo direto:", tuple(np.round(met(SYd, s), 2)))
