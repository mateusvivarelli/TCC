"""
Dois graficos pedidos pelo orientador (05/11/2026), feitos so com dados do repositorio (sem rasters):
 - fig_soma_eunit_x_medido.png: soma de E_unit do evento x descarga de sedimentos medida, MC e MFM, com a reta SY = c * soma(E_unit)
 - fig_volume_concentracao.png: (a) descarga medida x volume total do evento; (b) variacao entre eventos do volume e da concentracao media
Rodar da raiz do repositorio:  python Scripts/fig_grupo_E.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.ticker as mt
import numpy as np, pandas as pd
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(RAIZ, "TCC_Texto", "figuras")
d = pd.read_csv(os.path.join(RAIZ, "Dados Iniciais", "comparacao_SY_lambda005_woodward.csv")).sort_values("evento")
ev = d.evento.values; O = d.SY_obs_t.values
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
br = lambda v: f"{v:,.0f}".replace(",", ".")
def eixo_log(eixo, ticks):
    eixo.set_major_locator(mt.FixedLocator(ticks)); eixo.set_major_formatter(mt.FixedFormatter([br(t) for t in ticks])); eixo.set_minor_locator(mt.NullLocator())

# ---------- Figura E1
fig, ax = plt.subplots(1, 2, figsize=(10.5, 4.6), sharey=True)
for a, (col, nome, cor) in zip(ax, (("soma_E_unit_calc_t", "MC: escoamento calculado pelo SCS-CN", "#1f5fa8"),
                                     ("soma_E_unit_forc_t", "MFM: escoamento direto forçado ao medido", "#c0392b"))):
    E = d[col].values; c = np.exp(np.mean(np.log(O / E)))
    x = np.array([1e3, 5e5])
    a.fill_between(x, c * x / 2, c * x * 2, color="#e8eef6", label="faixa de fator 2")
    a.plot(x, c * x, color="k", lw=0.9, label=f"SY = c * ΣE_unit (c = {c:.4f})".replace(".", ","))
    a.scatter(E, O, s=34, color=cor, edgecolor="white", linewidth=0.5, zorder=3)
    for e_, o_, n in zip(E, O, ev):
        a.annotate(str(n), (e_, o_), fontsize=7, xytext=(3, 3), textcoords="offset points", color="#444")
    a.set_xscale("log"); a.set_yscale("log"); a.set_xlim(x); a.set_ylim(100, 10000)
    eixo_log(a.xaxis, [1000, 10000, 100000]); eixo_log(a.yaxis, [100, 1000, 10000])
    a.set_title(nome, fontsize=10); a.set_xlabel("Soma de E_unit no evento (índice, sem unidade)")
    a.legend(loc="upper left", fontsize=8, frameon=False)
ax[0].set_ylabel("Descarga de sedimentos medida (t)")
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_soma_eunit_x_medido.png"), dpi=300); plt.close(fig)

# ---------- Figura E2
TR = d.V_dir_medido_m3.values + d.V_base_Bt_m3.values
C = O / TR * 1e6  # mg/L
lv, lo, lc = np.log(TR), np.log(O), np.log(C)
b, a0 = np.polyfit(lv, lo, 1); r2 = np.corrcoef(lv, lo)[0, 1] ** 2
fig, ax = plt.subplots(1, 2, figsize=(10.5, 4.6), gridspec_kw={"width_ratios": [1.25, 1]})
a = ax[0]
a.scatter(TR / 1e3, O, s=34, color="#4a4a4a", edgecolor="white", linewidth=0.5, zorder=3)
for t_, o_, n in zip(TR, O, ev):
    a.annotate(str(n), (t_ / 1e3, o_), fontsize=7, xytext=(3, 3), textcoords="offset points", color="#444")
xx = np.linspace(lv.min() - 0.1, lv.max() + 0.1, 50)
a.plot(np.exp(xx) / 1e3, np.exp(a0 + b * xx), color="k", lw=0.9, label=f"ajuste em log: R² = {r2:.2f}".replace(".", ","))
a.set_xscale("log"); a.set_yscale("log"); eixo_log(a.xaxis, [200, 500, 1000, 2000, 5000]); eixo_log(a.yaxis, [200, 500, 1000, 2000, 5000])
a.set_xlabel("Volume total escoado no evento (10³ m³)"); a.set_ylabel("Descarga de sedimentos medida (t)")
a.set_title("(a) Descarga de sedimentos e volume total", fontsize=10); a.legend(loc="upper left", fontsize=8, frameon=False)
a = ax[1]
rng = np.random.default_rng(3)
for k, (v, nome, cor) in enumerate(((TR / np.exp(lv.mean()), "Volume total", "#1f5fa8"), (C / np.exp(lc.mean()), "Concentração média\n(descarga / volume)", "#d98b1d"))):
    a.scatter(k + rng.uniform(-0.12, 0.12, len(v)), v, s=30, color=cor, edgecolor="white", linewidth=0.5, zorder=3)
    var = np.var(np.log(v)); a.text(k, 4.3, f"variância do log:\n{var:.2f}".replace(".", ","), ha="center", fontsize=9)
a.axhline(1, color="k", lw=0.6, ls="--")
a.set_yscale("log"); a.set_ylim(0.1, 7); eixo_log(a.yaxis, [0.2, 0.5, 1, 2])
a.yaxis.set_major_formatter(mt.FixedFormatter(["0,2", "0,5", "1", "2"]))
a.set_xticks([0, 1]); a.set_xticklabels(["Volume total", "Concentração média\n(descarga / volume)"]); a.set_xlim(-0.6, 1.6)
a.set_ylabel("Valor do evento / média geométrica dos 17 eventos")
a.set_title("(b) Variação entre os 17 eventos", fontsize=10)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_volume_concentracao.png"), dpi=300); plt.close(fig)
print("ok; R2", round(r2, 3), "var", round(np.var(lv), 2), round(np.var(lc), 2))
