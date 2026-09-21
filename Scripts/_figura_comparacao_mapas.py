"""
Figura comparativa: mapa de producao de sedimentos na previsao pura
(Q do CN-SCS) x com o volume observado como restricao, mais a dispersao
SY_obs x SY_sim dos dois casos.

Escala de cor compartilhada entre os dois mapas (senao a comparacao visual
mente). Matiz unica, clara->escura, para magnitude; normalizacao log porque
a distribuicao de erosao e muito assimetrica.
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, LinearSegmentedColormap
from osgeo import gdal

gdal.UseExceptions()

BASE = r"C:\TCC"
PASTA_DADOS = os.path.join(BASE, "Dados Iniciais")
SAIDA = os.path.join(BASE, "Figuras")
os.makedirs(SAIDA, exist_ok=True)

SERIE_1 = "#2a78d6"   # azul  - previsao pura
SERIE_2 = "#eb6834"   # laranja - volume restrito
TEXTO = "#0b0b0b"
TEXTO_2 = "#52514e"
GRID = "#d8d7d2"

# matiz unica clara->escura para magnitude (sem arco-iris)
CMAP = LinearSegmentedColormap.from_list(
    "erosao", ["#fff3e8", "#fbc79a", "#f09048", "#d1621a", "#8f3c08", "#4a1e02"])


def le(caminho):
    ds = gdal.Open(caminho)
    b = ds.GetRasterBand(1)
    nd = b.GetNoDataValue()
    a = b.ReadAsArray().astype(np.float64)
    a = np.where((a != nd) & np.isfinite(a), a, np.nan)
    ds = None
    return a


prev = le(os.path.join(PASTA_DADOS, "SY_medio_eventos.tif"))
obs = le(os.path.join(PASTA_DADOS, "SY_medio_eventos_obs.tif"))

# recorta na extensao da bacia
m = np.isfinite(prev) | np.isfinite(obs)
linhas, colunas = np.where(m)
r0, r1 = linhas.min(), linhas.max() + 1
c0, c1 = colunas.min(), colunas.max() + 1
prev = prev[r0:r1, c0:c1]
obs = obs[r0:r1, c0:c1]

positivos = np.concatenate([prev[np.isfinite(prev) & (prev > 0)],
                            obs[np.isfinite(obs) & (obs > 0)]])
vmin = np.percentile(positivos, 2)
vmax = np.percentile(positivos, 99.8)
norm = LogNorm(vmin=max(vmin, 1e-6), vmax=vmax)

df = pd.read_csv(os.path.join(PASTA_DADOS, "comparacao_SY_previsao_vs_restrito.csv"))

plt.rcParams.update({"font.size": 12})
fig = plt.figure(figsize=(15.5, 7.6))
gs = fig.add_gridspec(2, 2, width_ratios=[1.45, 1], height_ratios=[1, 1],
                      hspace=0.28, wspace=0.16)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[:, 1])

for ax, dado, titulo, sub in (
    (ax1, prev, "Previsão pura (Q do modelo CN-SCS)", "NSE = 0,28 (val. cruzada) · erro abs. 46%"),
    (ax2, obs, "Volume observado como restrição", "NSE = 0,78 (val. cruzada) · erro abs. 28%"),
):
    ax.imshow(np.where(np.isfinite(dado), 1.0, np.nan), cmap="Greys", vmin=0, vmax=8)
    im = ax.imshow(np.where(dado > 0, dado, np.nan), cmap=CMAP, norm=norm)
    ax.set_title(titulo, fontsize=15, color=TEXTO, pad=7, loc="left")
    ax.text(0, -0.10, sub, transform=ax.transAxes, fontsize=12, color=TEXTO_2)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

cax = fig.add_axes([0.085, 0.045, 0.45, 0.022])
cb = fig.colorbar(im, cax=cax, orientation="horizontal")
cb.set_label("Produção de sedimentos por pixel (t/evento, média dos 17 eventos)",
             fontsize=12, color=TEXTO_2)
cb.ax.tick_params(labelsize=10.5, colors=TEXTO_2, length=3)
cb.outline.set_visible(False)

# dispersao
o = df["SY_obs_t"].to_numpy()
p = df["SY_previsao_t"].to_numpy()
r = df["SY_restrito_t"].to_numpy()
lim = max(o.max(), p.max(), r.max()) * 1.08

ax3.plot([0, lim], [0, lim], color=GRID, lw=1.5, zorder=1)
ax3.text(lim * 0.72, lim * 0.76, "1:1", fontsize=11, color=TEXTO_2, rotation=45)
ax3.scatter(o, p, s=85, color=SERIE_1, edgecolor="white", linewidth=1.4,
            zorder=3, label="Previsão pura")
ax3.scatter(o, r, s=85, color=SERIE_2, edgecolor="white", linewidth=1.4,
            zorder=4, label="Volume restrito")

ax3.set_xlim(0, lim)
ax3.set_ylim(0, lim)
ax3.set_aspect("equal")
ax3.set_xlabel("Sedimento medido no exutório (t)", fontsize=13, color=TEXTO_2)
ax3.set_ylabel("Sedimento simulado (t)", fontsize=13, color=TEXTO_2)
ax3.set_title("Desempenho por evento (n = 17)", fontsize=15, color=TEXTO, pad=7, loc="left")
ax3.grid(True, color=GRID, lw=0.7, alpha=0.7)
ax3.set_axisbelow(True)
for lado in ("top", "right"):
    ax3.spines[lado].set_visible(False)
for lado in ("left", "bottom"):
    ax3.spines[lado].set_color(GRID)
ax3.tick_params(labelsize=11, colors=TEXTO_2)
leg = ax3.legend(frameon=False, fontsize=12.5, loc="upper left")
for t in leg.get_texts():
    t.set_color(TEXTO)


caminho = os.path.join(SAIDA, "comparacao_previsao_vs_volume_restrito.png")
fig.savefig(caminho, dpi=170, bbox_inches="tight", facecolor="white")
print("salvo:", caminho)
