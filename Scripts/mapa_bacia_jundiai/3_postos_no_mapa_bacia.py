"""Acrescenta os dois postos pluviometricos ao mapa da bacia (mapa_bacia_jundiai.png), sem refazer o mapa.
A imagem e georreferenciada pelos tracos dos eixos: x de 270 a 350 km e y de 7410 a 7450 km (UTM 23S).
Saida: TCC_Texto/figuras/mapas/mapa_bacia_jundiai_postos.png"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from pyproj import Transformer

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(BASE, "TCC_Texto", "figuras", "mapas", "mapa_bacia_jundiai.png")
DST = os.path.join(BASE, "TCC_Texto", "figuras", "mapas", "mapa_bacia_jundiai_postos.png")
im = np.array(Image.open(SRC).convert("RGB")); H, W = im.shape[:2]
d = im.mean(axis=2) < 100
# tracos dos eixos (abaixo do eixo x e a esquerda do eixo y)
xt = [c for c in range(W) if d[1101:1106, c].all()]; yt = [r for r in range(H) if d[r, 109:114].all()]
xt = [np.mean(g) for g in np.split(np.array(xt), np.where(np.diff(xt) > 2)[0] + 1)]
yt = [np.mean(g) for g in np.split(np.array(yt), np.where(np.diff(yt) > 2)[0] + 1)]
assert len(xt) == 9 and len(yt) == 5, (xt, yt)
ax_x = np.polyfit(np.arange(270, 351, 10), xt, 1); ax_y = np.polyfit(np.arange(7450, 7409, -10), yt, 1)
px = lambda e, n: (np.polyval(ax_x, e / 1000), np.polyval(ax_y, n / 1000))

tr = Transformer.from_crs(4326, 31983, always_xy=True)
postos = {"DBT5": tr.transform(-46.4809, -23.2646), "Campo Limpo Paulista": tr.transform(-46.760284, -23.208778)}

dpi = 170
fig = plt.figure(figsize=(W / dpi, H / dpi), dpi=dpi); ax = fig.add_axes([0, 0, 1, 1]); ax.imshow(im); ax.axis("off")
halo = [pe.withStroke(linewidth=3, foreground="white")]
for nome, (e, n) in postos.items():
    x, y = px(e, n)
    ax.plot(x, y, "o", ms=17, mfc="none", mec="#0B3C8C", mew=3, zorder=5)
    if nome == "DBT5":
        ax.plot(x, y, "o", ms=6, color="#0B3C8C", zorder=6)
        ax.text(x + 16, y - 24, "Posto DBT5", ha="right", va="bottom", fontsize=9, fontweight="bold", color="#0B3C8C", path_effects=halo)
    else:
        ax.text(x + 30, y + 52, "Posto Campo Limpo", ha="center", va="top", fontsize=9, fontweight="bold", color="#0B3C8C", path_effects=halo)
# entrada de legenda, logo acima da legenda do mapa
lx, ly = 1745, 856
ax.add_patch(plt.Rectangle((lx, ly - 18), 508, 36, fc="white", ec="#cccccc", lw=0.8, zorder=7))
ax.plot(lx + 26, ly, "o", ms=9, mfc="none", mec="#0B3C8C", mew=2.5, zorder=8)
ax.text(lx + 52, ly, "Posto pluviométrico (registro horário)", va="center", fontsize=8, zorder=8)
ax.set_xlim(0, W); ax.set_ylim(H, 0)
fig.savefig(DST, dpi=dpi); plt.close(fig)
print("ok", DST, {k: tuple(round(float(v)) for v in px(*c)) for k, c in postos.items()})
