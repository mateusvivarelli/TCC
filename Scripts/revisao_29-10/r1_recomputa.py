"""Revisao independente 29/10: recomputa, a partir das planilhas de dados, R, TR, V_dir, SY_obs,
o filtro de Eckhardt e, a partir das somas de E_unit do CSV oficial, c, LOO e metricas."""
import numpy as np, pandas as pd
from scipy.stats import spearmanr
DI = "Dados Iniciais"; N = 17
ev = pd.read_excel(f"{DI}/eventos_processados_manuais.xlsx").iloc[:18]
h = pd.read_excel(f"{DI}/Dados_finais_histereses_corrigido.xlsx").iloc[:, :8]
h.columns = ["Data", "P1", "P2", "Ptot", "Q", "CSS", "Bt", "CSSBt"]; h["Data"] = pd.to_datetime(h["Data"]); h = h.set_index("Data")
rows = [ev.iloc[0]] + [ev.iloc[n] for n in range(2, 18)]
out = []
for n, r in enumerate(rows, 1):
    w = h.loc[r["Inicio"]:r["Fim"]]
    P1, P2 = float(r["chuva_p1_mm"]), float(r["chuva_p2_mm"])
    out.append(dict(ev=n, rotulo=r["Unnamed: 0"], P1=P1, P2=P2, R_planilha=r["Chuva_evento_mm"], R_pond=0.307*P1+0.693*P2,
                    P1_serie=w.P1.sum(), P2_serie=w.P2.sum(),
                    RI=r["Intensidade_60min_mm/h"], i60_1=r["i60_p1_mm/h"], i60_2=r["i60_p2_mm/h"],
                    TR_pl=r["T_R_m3"], TR=w.Q.sum()*3600, SBt=w.Bt.sum()*3600, nanQ=w.Q.isna().sum(), nanC=w.CSS.isna().sum(),
                    SY_pl=r["SYY_t"], SY=(w.Q*w.CSS).sum()*3600/1e6, Qp=float(r["Q_pico"]), Qmax_serie=w.Q.max(), nh=len(w)))
d = pd.DataFrame(out); d["VD"] = d.TR - d.SBt; d["RI_R"] = d.RI / d.R_planilha
pd.set_option("display.width", 250)
print(d.round(3).to_string())
off = pd.read_csv(f"{DI}/comparacao_SY_lambda005_woodward.csv")
print("max |SY recalc - CSV|:", np.max(np.abs(d.SY - off.SY_obs_t)), " max |VD - CSV|:", np.max(np.abs(d.VD - off.V_dir_medido_m3)),
      " max |SBt - CSV|:", np.max(np.abs(d.SBt - off.V_base_Bt_m3)))
print("max |R_pond - R_planilha|:", np.max(np.abs(d.R_pond - d.R_planilha)))
# pesos por MQ contra R_planilha
X = d[["P1", "P2"]].values; wls = np.linalg.lstsq(X, d.R_planilha.values, rcond=None)[0]; print("pesos MQ que reproduzem R_planilha:", wls, wls.sum())

SY = d.SY.values; ids = np.arange(N)
nse = lambda o, s: 1 - np.sum((o-s)**2)/np.sum((o-o.mean())**2)
nlog = lambda o, s: nse(np.log(o), np.log(s))
ape = lambda o, s: 100*np.abs(s-o)/o
f2 = lambda o, s: 100*np.mean((s/o >= .5) & (s/o <= 2))
fit1 = lambda x, y: np.exp(np.mean(np.log(y)-np.log(x)))
def roda(x):
    c = fit1(x, SY); loo = np.array([fit1(x[ids != i], SY[ids != i])*x[i] for i in ids])
    return dict(c=c, loo=loo, medape=np.median(ape(SY, loo)), f2=f2(SY, loo), nlog=nlog(SY, loo), sp=spearmanr(SY, loo)[0], nse_in=nse(SY, c*x), nse_loo=nse(SY, loo))
def ic():
    Dq = d.TR.values*d.Qp.values; K = .031*.536*.267
    def aj(m):
        b, a = np.polyfit(np.log(Dq[m]), np.log(SY[m]/K), 1); return a, b
    a, b = aj(ids >= 0); loo = np.array([np.exp(aj(ids != i)[0])*Dq[i]**aj(ids != i)[1]*K for i in ids])
    return dict(c=(np.exp(a), b), loo=loo, medape=np.median(ape(SY, loo)), f2=f2(SY, loo), nlog=nlog(SY, loo), sp=spearmanr(SY, loo)[0], nse_in=nse(SY, np.exp(a)*Dq**b*K), nse_loo=nse(SY, loo))
M = {"MC": roda(off.soma_E_unit_calc_t.values), "MFM": roda(off.soma_E_unit_forc_t.values), "c*chuva": roda(d.R_planilha.values),
     "c*V_dir": roda(d.VD.values), "c*T_R": roda(d.TR.values), "IC refeita": ic()}
for k, m in M.items():
    print(f"{k:<11} c={m['c']} MedAPE={m['medape']:.1f} f2={m['f2']:.0f} NSElog={m['nlog']:.2f} Spear={m['sp']:.2f} NSEin={m['nse_in']:.2f} NSEloo={m['nse_loo']:.2f}")
print("max |LOO MC - CSV|", np.max(np.abs(M['MC']['loo']-off.SY_calc_LOO_t)), "MFM", np.max(np.abs(M['MFM']['loo']-off.SY_forc_LOO_t)),
      "chuva", np.max(np.abs(M['c*chuva']['loo']-off.SY_chuva_LOO_t)), "Vdir", np.max(np.abs(M['c*V_dir']['loo']-off.SY_Vdir_LOO_t)), "IC", np.max(np.abs(M['IC refeita']['loo']-off.SY_IC_LOO_t)))
f = d.VD.values/off.V_dir_SCS_m3.values; print("fator f = V_dir/V_SCS:", np.round(f, 2), "eventos com f>1:", np.sum(f > 1))
Vs = off.V_dir_SCS_m3.values; print(f"volume SCS: vies {100*(Vs.sum()/d.VD.sum()-1):.1f}% erro mediano {np.median(ape(d.VD.values, Vs)):.1f}% NSE {nse(d.VD.values, Vs):.2f}")
print("variancia linear do ev15 (fracao de soma dos quadrados dos desvios):", ((SY[14]-SY.mean())**2/np.sum((SY-SY.mean())**2)))
# circularidade: SY = V * Cmedia
Cm = SY/d.TR.values
print("var ln SY", np.var(np.log(SY)), "var ln TR", np.var(np.log(d.TR)), "var ln Cmedia", np.var(np.log(Cm)), "corr(lnTR, lnCm)", np.corrcoef(np.log(d.TR), np.log(Cm))[0, 1])
print("corr ln SY x ln VD", np.corrcoef(np.log(SY), np.log(d.VD))[0, 1], " ln SY x ln E_MFM", np.corrcoef(np.log(SY), np.log(off.soma_E_unit_forc_t))[0, 1],
      " ln E_MFM x ln VD", np.corrcoef(np.log(off.soma_E_unit_forc_t), np.log(d.VD))[0, 1])
d.to_csv("/tmp/claude-0/-home-user-TCC/f521a486-b85c-5056-a3b4-5f7d885f5fd6/scratchpad/eventos_recalc.csv", index=False)
np.save("/tmp/claude-0/-home-user-TCC/f521a486-b85c-5056-a3b4-5f7d885f5fd6/scratchpad/loo.npy", {k: v["loo"] for k, v in M.items()}, allow_pickle=True)
