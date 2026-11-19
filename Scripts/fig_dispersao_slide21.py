"""
Figura do slide 21 da defesa (modelo simples com a chuva x modelo calculado, MC), com os eixos x completos.
Mesmos dados e desenho de Scripts/fig_dispersao_descarga.py (branch claude/banca-04-11), so as duas figuras de cima,
em formato largo para o slide. Saida: TCC_Texto/figuras/slides/fig_dispersao_MC_slide21.png
Rodar da raiz do repositorio:  python Scripts/fig_dispersao_slide21.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.ticker
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DI = os.path.join(RAIZ, "Dados Iniciais"); FIG = os.path.join(RAIZ, "TCC_Texto", "figuras", "slides")
os.makedirs(FIG, exist_ok=True)
N = 17
AZUL, CINZA = "#1f5fa8", "#9a9a9a"
plt.rcParams.update({"font.family": ["Calibri", "DejaVu Sans"], "font.size": 12,
                     "axes.spines.top": False, "axes.spines.right": False})
sd = pd.read_csv(os.path.join(DI, "comparacao_SY_lambda005_woodward.csv")).sort_values("evento")
ev = pd.read_excel(os.path.join(DI, "eventos_processados_manuais.xlsx"), sheet_name="Sheet1").iloc[:18]
R_ = [ev.iloc[0 if n == 1 else n] for n in range(1, N + 1)]
SY = np.array([float(r["SYY_t"]) for r in R_])
chuva = np.array([float(r["Chuva_evento_mm"]) for r in R_]); ids = np.arange(N); ch = np.zeros(N)
for i in range(N):
    m = ids != i
    ch[i] = np.exp(np.mean(np.log(SY[m]) - np.log(chuva[m]))) * chuva[i]
B = sd.SY_calc_LOO_t.to_numpy()
fig, ax = plt.subplots(1, 2, figsize=(11.5, 5.3), sharex=True, sharey=True)
lim = np.array([10, 30000])
for a_, (tit, sim, cor) in zip(ax, (("Modelo simples com a chuva do evento\n(SY = c × chuva; só chuva)", ch, CINZA),
                                    ("Modelo calculado (MC): MUSLE espacializada,\nescoamento direto do SCS-CN (só chuva)", B, AZUL))):
    obs = SY
    a_.fill_between(lim, lim / 2, lim * 2, color="#e8eef6")
    a_.plot(lim, lim, color="k", lw=0.9)
    a_.scatter(obs, sim, c=cor, s=48, zorder=3, edgecolor="white", linewidth=0.6)
    for i in range(N):
        a_.annotate(str(i + 1), (obs[i], sim[i]), fontsize=9, xytext=(4, 4), textcoords="offset points", color="#444")
    r = sim / obs; dentro = 100 * np.mean((r >= 0.5) & (r <= 2)); med = float(np.median(100 * np.abs(sim - obs) / obs))
    a_.set_xscale("log"); a_.set_yscale("log"); a_.set_xlim(lim); a_.set_ylim(lim)
    ticks = [10, 100, 1000, 10000]
    for eixo in (a_.xaxis, a_.yaxis):
        eixo.set_major_locator(matplotlib.ticker.FixedLocator(ticks))
        eixo.set_major_formatter(matplotlib.ticker.FixedFormatter([f"{t:,}".replace(",", ".") for t in ticks]))
        eixo.set_minor_locator(matplotlib.ticker.NullLocator())
    a_.set_title(tit, fontsize=12)
    a_.text(0.04, 0.95, f"dentro de fator 2: {dentro:.0f}%\nerro mediano: {med:.0f}%", transform=a_.transAxes, va="top", fontsize=12)
    a_.set_xlabel("Descarga de sedimentos medida (t)")
    print(tit.split("\n")[0], "| fator 2", round(dentro), "| erro mediano", round(med, 1))
ax[0].set_ylabel("Descarga de sedimentos simulada,\nvalidação leave-one-out (t)")
fig.tight_layout(); out = os.path.join(FIG, "fig_dispersao_MC_slide21.png"); fig.savefig(out, dpi=200); plt.close(fig); print(out)
