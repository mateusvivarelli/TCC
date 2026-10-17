"""Figura 2x2: fator LS (antigo da IC x recalculado por Moore) e o mapa de
producao de sedimentos resultante de cada um. Escala de cor compartilhada
dentro de cada linha (senao a comparacao visual mente)."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, LinearSegmentedColormap
from osgeo import gdal

gdal.UseExceptions()
BASE = r"C:\TCC"
DI = os.path.join(BASE, "Dados Iniciais")
SAIDA = os.path.join(BASE, "Figuras")
os.makedirs(SAIDA, exist_ok=True)

TEXTO, TEXTO_2 = "#0b0b0b", "#52514e"
CMAP_LS = LinearSegmentedColormap.from_list(
    "ls", ["#eef4fb", "#b9d2ec", "#6fa5d6", "#3573b2", "#1b4473", "#0a2038"])
CMAP_SY = LinearSegmentedColormap.from_list(
    "sy", ["#fff3e8", "#fbc79a", "#f09048", "#d1621a", "#8f3c08", "#4a1e02"])


def le(c):
    ds = gdal.Open(c)
    b = ds.GetRasterBand(1)
    nd = b.GetNoDataValue()
    a = b.ReadAsArray().astype(np.float64)
    ds = None
    return np.where((a != nd) & np.isfinite(a), a, np.nan)


ls_velho = le(os.path.join(DI, "LS_raster.tif"))
ls_novo = le(os.path.join(DI, "LS_moore.tif"))
sy_velho = le(os.path.join(DI, "SY_medio_eventos_vb.tif"))
sy_novo = le(os.path.join(DI, "SY_medio_eventos_vbls.tif"))

m = np.isfinite(ls_velho) | np.isfinite(ls_novo)
lin, col = np.where(m)
r0, r1, c0, c1 = lin.min(), lin.max() + 1, col.min(), col.max() + 1
rec = lambda a: a[r0:r1, c0:c1]
ls_velho, ls_novo = rec(ls_velho), rec(ls_novo)
sy_velho, sy_novo = rec(sy_velho), rec(sy_novo)


def faixa(*arrs):
    v = np.concatenate([a[np.isfinite(a) & (a > 0)] for a in arrs])
    return LogNorm(vmin=max(np.percentile(v, 2), 1e-7), vmax=np.percentile(v, 99.8))


norm_ls = faixa(ls_velho, ls_novo)
norm_sy = faixa(sy_velho, sy_novo)

plt.rcParams.update({"font.size": 12})
fig, axes = plt.subplots(2, 2, figsize=(16.5, 8.4))

paineis = [
    (axes[0, 0], ls_velho, CMAP_LS, norm_ls, "Fator LS herdado da IC",
     "correlação com a declividade: 0,047"),
    (axes[0, 1], ls_novo, CMAP_LS, norm_ls, "Fator LS recalculado (Moore)",
     "correlação com a declividade: 0,943"),
    (axes[1, 0], sy_velho, CMAP_SY, norm_sy, "Produção de sedimentos — LS da IC", ""),
    (axes[1, 1], sy_novo, CMAP_SY, norm_sy, "Produção de sedimentos — LS recalculado",
     "56,9% dos hot spots coincidem com o mapa anterior"),
]
for ax, dado, cmap, norm, titulo, sub in paineis:
    ax.imshow(np.where(np.isfinite(dado), 1.0, np.nan), cmap="Greys", vmin=0, vmax=8)
    im = ax.imshow(np.where(dado > 0, dado, np.nan), cmap=cmap, norm=norm)
    ax.set_title(titulo, fontsize=14, color=TEXTO, pad=6, loc="left")
    if sub:
        ax.text(0, -0.07, sub, transform=ax.transAxes, fontsize=11, color=TEXTO_2)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax._im = im

for linha, rotulo in ((0, "Fator LS (adimensional)"),
                      (1, "Produção de sedimentos (t/pixel por evento)")):
    cax = fig.add_axes([0.25, 0.52 - linha * 0.485, 0.5, 0.016])
    cb = fig.colorbar(axes[linha, 1]._im, cax=cax, orientation="horizontal")
    cb.set_label(rotulo, fontsize=11, color=TEXTO_2)
    cb.ax.tick_params(labelsize=9.5, colors=TEXTO_2, length=3)
    cb.outline.set_visible(False)

plt.tight_layout(rect=[0, 0.05, 1, 1])
cam = os.path.join(SAIDA, "comparacao_LS_antigo_vs_moore.png")
fig.savefig(cam, dpi=165, bbox_inches="tight", facecolor="white")
print("salvo:", cam)
