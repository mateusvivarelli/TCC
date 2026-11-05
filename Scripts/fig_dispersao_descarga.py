"""
Figura 8 do TCC refeita em 05/11/2026 com o termo "descarga de sedimentos" (pedido do orientador).
Mesmos dados e mesmo desenho de Scripts/gerar_figuras_tcc.py (Figura 1, dispersao), sem dependencia de GDAL e com caminhos
relativos ao repositorio. Saida: TCC_Texto/figuras/fig_dispersao_descarga.png
Rodar da raiz do repositorio:  python Scripts/fig_dispersao_descarga.py
"""
import os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.ticker
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "Scripts"))
import _ic_original as ICO
DI = os.path.join(RAIZ, "Dados Iniciais"); FIG = os.path.join(RAIZ, "TCC_Texto", "figuras")
N = 17
AZUL, CINZA, VERM, LARANJA = "#1f5fa8", "#9a9a9a", "#c0392b", "#d98b1d"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
sd = pd.read_csv(os.path.join(DI, "comparacao_SY_lambda005_woodward.csv")).sort_values("evento")
ev = pd.read_excel(os.path.join(DI, "eventos_processados_manuais.xlsx"), sheet_name="Sheet1").iloc[:18]
R_ = [ev.iloc[0 if n == 1 else n] for n in range(1, N + 1)]
SY = np.array([float(r["SYY_t"]) for r in R_])
chuva = np.array([float(r["Chuva_evento_mm"]) for r in R_]); ids = np.arange(N); ch = np.zeros(N)
for i in range(N):
    m = ids != i
    ch[i] = np.exp(np.mean(np.log(SY[m]) - np.log(chuva[m]))) * chuva[i]
B = sd.SY_calc_LOO_t.to_numpy(); F = sd.SY_forc_LOO_t.to_numpy()
fig, ax = plt.subplots(2, 2, figsize=(10.5, 9.4), sharex=True, sharey=True); ax = ax.ravel()
lim = np.array([10, 30000])
for a_, (tit, obs, sim, cor) in zip(ax, (("Modelo simples com a chuva do evento\n(SY = c * chuva; só chuva)", SY, ch, CINZA),
                                         ("Modelo calculado: MUSLE espacializada,\nescoamento direto do SCS-CN (só chuva)", SY, B, AZUL),
                                         ("Modelo forçado: MUSLE espacializada,\nescoamento direto medido", SY, F, VERM),
                                         ("IC (concentrada), valores originais da IC:\nvolume e pico medidos, sem validação cruzada", ICO.Y_OBS, ICO.Y_SIM_CAL, LARANJA))):
    a_.fill_between(lim, lim / 2, lim * 2, color="#e8eef6")
    a_.plot(lim, lim, color="k", lw=0.8)
    a_.scatter(obs, sim, c=cor, s=34, zorder=3, edgecolor="white", linewidth=0.5)
    for i in range(N):
        a_.annotate(str(i + 1), (obs[i], sim[i]), fontsize=7, xytext=(3, 3), textcoords="offset points", color="#444")
    r = sim / obs; dentro = 100 * np.mean((r >= 0.5) & (r <= 2))
    a_.set_xscale("log"); a_.set_yscale("log"); a_.set_xlim(lim); a_.set_ylim(lim)
    ticks = [10, 100, 1000, 10000]
    for eixo in (a_.xaxis, a_.yaxis):
        eixo.set_major_locator(matplotlib.ticker.FixedLocator(ticks)); eixo.set_major_formatter(matplotlib.ticker.FixedFormatter([f"{t:,}".replace(",", ".") for t in ticks]))
        eixo.set_minor_locator(matplotlib.ticker.NullLocator())
    a_.set_title(tit, fontsize=10); a_.text(0.04, 0.93, f"dentro de fator 2: {dentro:.0f}%\nerro mediano: {np.median(100*np.abs(sim-obs)/obs):.0f}%", transform=a_.transAxes, va="top", fontsize=9)
    a_.set_xlabel("Descarga de sedimentos medida (t)")
    print(tit.split("\n")[0], "| fator 2", round(dentro), "| erro mediano", round(float(np.median(100*np.abs(sim-obs)/obs)), 1))
ax[0].set_ylabel("Descarga de sedimentos simulada,\nvalidação leave-one-out (t)")
ax[2].set_ylabel("Descarga de sedimentos simulada,\nvalidação leave-one-out (t)\n(IC: ajuste nos próprios 17 eventos)")
for a_ in ax[:2]:
    a_.set_xlabel("")
fig.suptitle("Descarga de sedimentos simulada x medida nos 17 eventos (números = evento)", fontsize=11)
fig.tight_layout(); out = os.path.join(FIG, "fig_dispersao_descarga.png"); fig.savefig(out, dpi=300); plt.close(fig); print(out)
