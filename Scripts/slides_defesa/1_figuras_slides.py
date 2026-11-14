"""Figuras para os slides 11 a 28 da defesa (14/11/2026).
Recortes das figuras do TCC (um painel por slide, maior) e o hidrograma do evento 11.
Saida: TCC_Texto/figuras/slides/"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FIG = os.path.join(BASE, "TCC_Texto", "figuras"); OUT = os.path.join(FIG, "slides")
os.makedirs(OUT, exist_ok=True)


def recorta(arq, caixa, nome):
    im = Image.open(os.path.join(FIG, arq)); w, h = im.size
    x0, y0, x1, y1 = [int(round(v * (w if i % 2 == 0 else h))) for i, v in enumerate(caixa)]
    im.crop((x0, y0, x1, y1)).save(os.path.join(OUT, nome)); print(nome, x1 - x0, y1 - y0)


# evento 11, um painel por slide (fracoes da largura e da altura da figura original)
recorta("mapas/mapa_08a_evento11_chuva_retencao_escoamento.png", (0, 0.058, 1, 0.362), "ev11_chuva.png")
recorta("mapas/mapa_08a_evento11_chuva_retencao_escoamento.png", (0, 0.370, 1, 0.674), "ev11_retencao.png")
recorta("mapas/mapa_08a_evento11_chuva_retencao_escoamento.png", (0, 0.683, 1, 0.988), "ev11_escoamento.png")
recorta("mapas/mapa_08b_evento11_erosao_sedimento.png", (0, 0.058, 0.875, 0.372), "ev11_eunit_sem_escala.png")
recorta("mapas/mapa_08b_evento11_erosao_sedimento.png", (0, 0.382, 1, 0.698), "ev11_sedimento.png")
# dispersao: linha de cima (simples com chuva e MC) e linha de baixo (MFM e concentrado)
recorta("fig_dispersao_descarga.png", (0, 0.045, 1, 0.495), "dispersao_simples_e_MC.png")
recorta("fig_dispersao_descarga.png", (0, 0.495, 1, 1), "dispersao_MFM_e_concentrado.png")
# mapa medio e areas criticas do MC (coluna da esquerda)
recorta("mapas/mapa_07_sedimento_medio.png", (0, 0.11, 0.50, 0.93), "mapa_medio_e_criticas_MC.png")

# hidrograma, chuva e concentracao do evento 11
d = pd.read_excel(os.path.join(BASE, "Dados Iniciais", "Dados_finais_histereses_corrigido.xlsx"))
d = d.rename(columns={d.columns[1]: "P_DBT5", d.columns[2]: "P_CL", d.columns[4]: "Q", d.columns[5]: "CSS", d.columns[6]: "Bt"})
ini, fim = pd.Timestamp("2019-07-04 12:00"), pd.Timestamp("2019-07-08 07:00")
j = d[(d.Data >= ini - pd.Timedelta(hours=12)) & (d.Data <= fim + pd.Timedelta(hours=12))].copy()
e = j[(j.Data >= ini) & (j.Data <= fim)]
plt.rcParams.update({"font.size": 13, "font.family": "DejaVu Sans"})
fig, (a1, a2) = plt.subplots(2, 1, figsize=(12, 6.4), sharex=True, gridspec_kw={"height_ratios": [1, 2.2]})
a1.bar(j.Data - pd.Timedelta(minutes=15), j.P_DBT5, width=0.02, color="#7FA7D9", label="DBT5 (leste)")
a1.bar(j.Data + pd.Timedelta(minutes=15), j.P_CL, width=0.02, color="#1F4E8C", label="Campo Limpo (oeste)")
a1.invert_yaxis(); a1.set_ylabel("Chuva\n(mm/h)"); a1.legend(frameon=False, loc="lower right", fontsize=11)
a2.fill_between(e.Data, e.Bt, e.Q, color="#9CC3E6", label="escoamento direto")
a2.plot(j.Data, j.Q, color="#1F4E8C", lw=2, label="vazão")
a2.plot(j.Data, j.Bt, color="#555555", lw=1.5, ls="--", label="vazão de base")
a2.set_ylabel("Vazão (m³/s)"); a2.set_ylim(0, None)
b = a2.twinx(); b.plot(j.Data, j.CSS, color="#D98B1F", lw=2, label="CSS"); b.set_ylabel("CSS (mg/L)", color="#B06A0A"); b.set_ylim(0, None)
for ax in (a1, a2):
    ax.axvline(ini, color="k", lw=0.8, ls=":"); ax.axvline(fim, color="k", lw=0.8, ls=":")
    ax.spines[["top", "right"]].set_visible(False)
b.spines[["top"]].set_visible(False)
h1, l1 = a2.get_legend_handles_labels(); h2, l2 = b.get_legend_handles_labels()
a2.legend(h1 + h2, l1 + l2, frameon=False, loc="upper right", fontsize=11)
a2.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d/%m"))
fig.tight_layout(); fig.savefig(os.path.join(OUT, "ev11_hidrograma.png"), dpi=200); plt.close(fig)
print("hidrograma ok; Q pico", e.Q.max(), "CSS pico", e.CSS.max(), "chuva", e.P_DBT5.sum(), e.P_CL.sum())
