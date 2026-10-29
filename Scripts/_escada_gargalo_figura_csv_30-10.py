"""Refaz a figura da escada (Figura 9 da proposta de 30/10) só a partir de TCC_Texto/figuras/escada_gargalo.csv,
sem rasters, com os rótulos "escoamento" no lugar de "água" (comentário C30 do orientador) e sem rodapé de método.
Mesmo desenho de _escada_gargalo_chuva_escoamento.py; saída em TCC_Texto/figuras/escada_gargalo_30-10.png."""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

FIG = os.path.join("TCC_Texto", "figuras")
d = pd.read_csv(os.path.join(FIG, "escada_gargalo.csv"))
n1 = d[d.nivel.str.startswith("N1")].set_index("modelo")
n3 = d[d.nivel.str.startswith("N3")].set_index("modelo")
ic = n3.loc[[m for m in n3.index if m.startswith("IC")][0]]

fig, ax = plt.subplots(1, 2, figsize=(11, 4.6))
x = np.arange(2); wd = 0.36
cb, cs, ci = "#1f5fa8", "#b8b8b8", "#d98b1d"
for k, (key, tit) in enumerate((("MedAPE", "Erro percentual mediano (menor é melhor)"),
                                ("fator2", "Eventos dentro de fator 2 (maior é melhor)"))):
    a = ax[k]
    vb = [n1.loc["MUSLE espacializada", key], n3.loc["MUSLE espacializada", key]]
    r1 = a.bar(x - wd / 2, vb, wd, color=cb, label="MUSLE espacializada (MC e MFM)")
    r2 = a.bar(x[0] + wd / 2, n1.loc["simples (sem MUSLE)", key], wd, color=cs, label="Modelo simples: c * chuva do evento")
    r3 = a.bar(x[1] + wd / 2, ic[key], wd, color=ci, label="IC concentrada (valores originais)")
    for rr in list(r1) + list(r2) + list(r3):
        a.text(rr.get_x() + rr.get_width() / 2, rr.get_height() + 1, f"{rr.get_height():.0f}%", ha="center", fontsize=9)
    a.set_xticks(x)
    a.set_xticklabels(["Escoamento calculado\na partir da chuva", "Escoamento direto\nforçado ao medido"], fontsize=10)
    a.set_title(tit, fontsize=11)
    a.spines[["top", "right"]].set_visible(False)
    a.set_ylim(0, 112)
h_, l_ = ax[0].get_legend_handles_labels()
fig.legend(h_, l_, loc="lower center", ncol=3, frameon=False, fontsize=9, bbox_to_anchor=(0.5, 0.01))
fig.tight_layout(rect=(0, 0.08, 1, 0.98))
out = os.path.join(FIG, "escada_gargalo_30-10.png")
fig.savefig(out, dpi=150)
print("figura:", out)
