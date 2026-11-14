import os, json, sys
import numpy as np, geopandas as gpd, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe
from shapely.geometry import LineString, Point
from shapely.ops import unary_union
sys.stdout.reconfigure(encoding='utf-8')
D = r"C:\Users\user\AppData\Local\Temp\claude\60ed5afc26073541\6f697bf5-4a56-4dbc-a537-266e661ffede\scratchpad\mapa_bacia"
OUT = r"C:\TCC\TCC_Texto\figuras\mapas"
RES = 150.0
g = json.load(open(D + r"\geo.json")); gt = g["gt"]; ny, nx = g["ny"], g["nx"]
nxt = np.load(D + r"\nxt.npy"); acc = np.load(D + r"\acc.npy"); areakm2 = acc * RES * RES / 1e6
def xy(c): i, j = divmod(int(c), nx); return gt[0] + (j + 0.5) * gt[1], gt[3] + (i + 0.5) * gt[5]
# ---- bacia total
b = gpd.read_file(D + r"\bacia_jundiai_total.gpkg"); b = b[b["v"] == 1]
bacia = unary_union(b.geometry).buffer(200).buffer(-200).simplify(60)
upper = gpd.read_file(r"C:\TCC\Dados Iniciais\Máscara Jundiaí.shp").to_crs(31983).geometry.unary_union
dren = gpd.read_file(r"C:\TCC\Dados Iniciais\drenagem.shp").to_crs(31983)
bacia = bacia.union(upper).buffer(150).buffer(-150).simplify(60)
print("bacia total km2", bacia.area / 1e6, "parte alta km2", upper.area / 1e6, "parte alta dentro da bacia (%)", 100 * upper.intersection(bacia).area / upper.area)
# ---- municipios
nomes = {m["id"]: m["nome"] for m in json.load(open(D + r"\r2.txt", encoding="utf-8"))}
mun = gpd.read_file(D + r"\mun_sp.geojson").set_crs(4326).to_crs(31983)
mun["cod"] = mun["codarea"].astype(int); mun["nome"] = mun["cod"].map(nomes)
mun["a_total"] = mun.geometry.area / 1e6
mun["ov_bacia"] = mun.geometry.intersection(bacia).area / 1e6
mun["ov_alta"] = mun.geometry.intersection(upper).area / 1e6
comp = mun[mun["ov_bacia"] > 3.0].copy().sort_values("ov_bacia", ascending=False)
comp["pct_munic"] = 100 * comp["ov_bacia"] / comp["a_total"]
print(comp[["nome", "a_total", "ov_bacia", "pct_munic", "ov_alta"]].round(1).to_string(index=False))
alta = comp[comp["ov_alta"] > 0.5]
print("municipios da parte alta:", alta[["nome", "ov_alta"]].round(1).to_string(index=False))
comp.drop(columns="geometry").to_csv(D + r"\municipios_bacia.csv", index=False, encoding="utf-8-sig")
# ---- rios (celulas com area >= limiar), apenas dentro da bacia
inb = np.zeros(ny * nx, bool)
from shapely import vectorized
ii, jj = np.mgrid[0:ny, 0:nx]
X = gt[0] + (jj + 0.5) * gt[1]; Y = gt[3] + (ii + 0.5) * gt[5]
inside = vectorized.contains(bacia.buffer(300), X.ravel(), Y.ravel())
LIM = 6.0
segs = []; lw = []
for c in np.where((areakm2 >= LIM) & inside)[0]:
    n = nxt[c]
    if n < 0: continue
    segs.append([xy(c), xy(n)]); lw.append(0.35 + 0.55 * np.log10(areakm2[c] / LIM))
# curso principal: da foz para montante pelo maior acumulado
inside0 = vectorized.contains(bacia.buffer(-150), X.ravel(), Y.ravel())
foz = int(np.argmax(np.where(inside0 & (areakm2 < 3000), areakm2, 0)))
up = {}
for c in np.where(inside & (nxt >= 0))[0]: up.setdefault(nxt[c], []).append(c)
path = [foz]
while path[-1] in up:
    path.append(max(up[path[-1]], key=lambda k: areakm2[k]))
main = LineString([xy(c) for c in path])
print("foz area km2", areakm2[foz], "comprimento do curso principal (km, DEM)", main.length / 1000)
# Tiete (celulas muito grandes, fora da bacia)
big = np.where(areakm2 >= 4000)[0]
bigsegs = [[xy(c), xy(nxt[c])] for c in big if nxt[c] >= 0]
# ---- figura
fig, ax = plt.subplots(figsize=(13.5, 7.9))
munall = mun[mun.geometry.intersects(bacia.buffer(15000))]
munall.boundary.plot(ax=ax, color="#9AA3B2", lw=0.5, zorder=2)
comp.plot(ax=ax, color="#F5F3EE", zorder=1)
gpd.GeoSeries([bacia], crs=31983).plot(ax=ax, color="#CFE0F2", ec="#1F5FA8", lw=1.6, zorder=3, alpha=0.95)
comp.boundary.plot(ax=ax, color="#7B8597", lw=0.7, ls="--", zorder=4)
ax.add_collection(LineCollection(bigsegs, colors="#1B4E8C", linewidths=2.4, zorder=5))
ax.add_collection(LineCollection(segs, colors="#2B7BBA", linewidths=lw, zorder=6))
ax.plot(*main.xy, color="#08306B", lw=2.4, zorder=7)
gpd.GeoSeries([upper], crs=31983).plot(ax=ax, color="#F2C46B", ec="#A8620F", lw=1.8, alpha=0.75, zorder=8)
dren[dren["NORIOCOMP"] != "Rio Jundiaí"].plot(ax=ax, color="#2B7BBA", lw=0.35, zorder=9)
dren[dren["NORIOCOMP"] == "Rio Jundiaí"].plot(ax=ax, color="#08306B", lw=2.2, zorder=10)
ex, ey = 319870.0, 7432300.0
cl = gpd.GeoSeries([Point(*__import__("pyproj").Transformer.from_crs(4326, 31983, always_xy=True).transform(-46.760284, -23.208778))], crs=31983)
cl.plot(ax=ax, marker="^", color="#d7191c", edgecolor="k", markersize=70, zorder=11)
# rotulos de municipios
for _, r in comp.iterrows():
    gg = r.geometry.intersection(bacia)
    if r["nome"] == "Campo Limpo Paulista": gg = gg.difference(upper)
    elif r["ov_alta"] > 0.5: gg = r.geometry.intersection(upper)
    p = gg.representative_point()
    off = 2300 if r["nome"] == "Campo Limpo Paulista" else 0
    ax.text(p.x, p.y + off, r["nome"], ha="center", va="center", fontsize=8, color="#14213D", zorder=12, fontweight="bold" if r["ov_alta"] > 0.5 else "normal",
            path_effects=[pe.withStroke(linewidth=2.2, foreground="white", alpha=0.85)])
mx, my = main.interpolate(0.55, normalized=True).x, main.interpolate(0.55, normalized=True).y
ax.text(mx, my + 1500, "Rio Jundiaí", fontsize=9, style="italic", color="#08306B", zorder=12, rotation=0, path_effects=[pe.withStroke(linewidth=2.5, foreground="white")])
ax.text(262200, 7436800, "Rio Tietê", fontsize=9, style="italic", color="#1B4E8C", zorder=12, path_effects=[pe.withStroke(linewidth=2.5, foreground="white")])
xmin, ymin, xmax, ymax = bacia.buffer(4000).bounds
ymin = ymin - 7000; xmax = xmax + 1500
ax.set_xlim(xmin, xmax); ax.set_ylim(ymin, ymax); ax.set_aspect("equal")
from matplotlib.ticker import FuncFormatter, MultipleLocator
ax.xaxis.set_major_locator(MultipleLocator(10000)); ax.yaxis.set_major_locator(MultipleLocator(10000))
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v/1000:.0f}")); ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v/1000:.0f}"))
ax.tick_params(labelsize=8); ax.set_xlabel("E (km, UTM 23S)", fontsize=8); ax.set_ylabel("N (km)", fontsize=8); ax.grid(True, color="#d0d0d0", lw=0.4, ls=":")
# escala e norte
L = 10000; sx, sy = xmin + 0.04 * (xmax - xmin), ymin + 0.07 * (ymax - ymin)
for k, c in enumerate(("k", "w")): ax.add_patch(mpatches.Rectangle((sx + k * L / 2, sy), L / 2, 600, fc=c, ec="k", lw=0.8, zorder=20))
for dx, t in ((0, "0"), (L / 2, "5"), (L, "10 km")): ax.text(sx + dx, sy + 1100, t, ha="center", fontsize=8, zorder=20)
nxp, nyp = xmax - 0.05 * (xmax - xmin), ymax - 0.18 * (ymax - ymin)
ax.annotate("", xy=(nxp, nyp + 0.12 * (ymax - ymin)), xytext=(nxp, nyp), arrowprops=dict(arrowstyle="-|>", color="k", lw=1.4, mutation_scale=12), zorder=20)
ax.text(nxp, nyp + 0.135 * (ymax - ymin), "N", ha="center", fontsize=10, fontweight="bold", zorder=20)
leg = [mpatches.Patch(fc="#CFE0F2", ec="#1F5FA8", lw=1.5, label=f"Bacia do rio Jundiaí ({bacia.area/1e6:,.0f} km²)".replace(",", ".")),
       mpatches.Patch(fc="#F2C46B", ec="#A8620F", lw=1.5, label=f"Parte alta estudada ({upper.area/1e6:.1f} km²)".replace(".", ",", 1) if False else f"Parte alta estudada ({upper.area/1e6:.1f} km²)".replace(".", ",")),
       Line2D([0], [0], color="#08306B", lw=2.4, label="Rio Jundiaí (curso principal)"), Line2D([0], [0], color="#2B7BBA", lw=1.2, label="Afluentes e rede de drenagem"),
       Line2D([0], [0], color="#7B8597", lw=0.9, ls="--", label="Limite municipal (IBGE)"),
       Line2D([0], [0], marker="^", color="w", markerfacecolor="#d7191c", markeredgecolor="k", markersize=9, label="Exutório da parte alta (Campo Limpo Paulista)")]
ax.legend(handles=leg, loc="lower right", fontsize=8, framealpha=0.95, title="Legenda", title_fontsize=9, bbox_to_anchor=(1.0, 0.0))
ax.set_title("Bacia do rio Jundiaí e a parte alta estudada, com municípios e rios", fontsize=11)
fig.text(0.01, 0.0, "Fontes: limites municipais do IBGE; bacia delimitada a partir de modelo digital de elevação (AWS Terrain Tiles, base SRTM); rede de drenagem da parte alta do projeto. Rios em ordem de grandeza (DEM de 150 m).", fontsize=7)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(OUT, "mapa_bacia_jundiai.png"), dpi=170, bbox_inches="tight", pad_inches=0.12); plt.close(fig)
print("mapa ok")

# ================= figura 2: parte alta com municipios e rios nomeados
fig, ax = plt.subplots(figsize=(13.5, 6.4))
ub = upper.buffer(1800).bounds
cores_mun = {"Atibaia": "#EDE7D6", "Mairiporã": "#E4EBD9", "Campo Limpo Paulista": "#E6E3F0", "Jarinu": "#F2E1D9"}
munz = mun[mun.geometry.intersects(upper.buffer(1800))]
for _, r in munz.iterrows(): gpd.GeoSeries([r.geometry], crs=31983).plot(ax=ax, color=cores_mun.get(r["nome"], "#F5F3EE"), zorder=1)
munz.boundary.plot(ax=ax, color="#7B8597", lw=0.9, ls="--", zorder=2)
gpd.GeoSeries([upper], crs=31983).plot(ax=ax, color="none", ec="#A8620F", lw=2.4, zorder=6)
estilo = {"Rio Jundiaí": ("#08306B", 2.8), "Ribeirão Jundiaizinho": ("#1F5FA8", 1.8), "Córrego das Taipas": ("#2E9E8F", 1.4), "Córrego Pedra Vermelha": ("#8A4FBF", 1.4),
          "Córrego Canjica": ("#D98C1F", 1.4), "Córrego Teassucanga": ("#C0392B", 1.4), "Córrego Rio Acima": ("#5C7A29", 1.4)}
for nome, (cor, lw_) in estilo.items():
    sub = dren[dren["NORIOCOMP"] == nome]
    if len(sub) == 0: continue
    sub.plot(ax=ax, color=cor, lw=lw_, zorder=5)
    uni = unary_union(sub.geometry.values)
    ln = uni if uni.geom_type == "LineString" else max(list(uni.geoms), key=lambda g_: g_.length)
    p = ln.interpolate(0.5, normalized=True)
    pos = {"Córrego Canjica": (334.6e3, 7426.2e3, "right"), "Córrego Teassucanga": (340.6e3, 7427.6e3, "left")}.get(nome)
    px, py, ha_ = (pos if pos else (p.x, p.y + 350, "center"))
    ax.text(px, py, nome, fontsize=8.5, color=cor, fontweight="bold", ha=ha_, zorder=9, path_effects=[pe.withStroke(linewidth=2.6, foreground="white")])
cl.plot(ax=ax, marker="^", color="#d7191c", edgecolor="k", markersize=90, zorder=10)
ax.text(319870 + 500, 7432300 - 1500, "Exutório\n(Campo Limpo Paulista)", fontsize=8, zorder=10, path_effects=[pe.withStroke(linewidth=2.4, foreground="white")])
for _, r in munz.iterrows():
    if r["ov_alta"] > 0.5:
        p = r.geometry.intersection(upper.buffer(1800)).representative_point()
        pm = {"Atibaia": (337.5e3, 7433.0e3), "Mairiporã": (343.2e3, 7423.2e3), "Campo Limpo Paulista": (320.6e3, 7436.0e3), "Jarinu": (326.5e3, 7435.9e3)}.get(r["nome"], (p.x, p.y))
        ax.text(pm[0], pm[1], f"{r['nome'].upper()}\n({r['ov_alta']:.0f} km² da parte alta)".replace(".", ","), fontsize=8, ha="center", color="#14213D", alpha=0.9, zorder=8,
                path_effects=[pe.withStroke(linewidth=2.4, foreground="white", alpha=0.7)])
ax.set_xlim(ub[0], ub[2]); ax.set_ylim(ub[1], ub[3]); ax.set_aspect("equal")
ax.xaxis.set_major_locator(MultipleLocator(5000)); ax.yaxis.set_major_locator(MultipleLocator(5000))
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v/1000:.0f}")); ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v/1000:.0f}"))
ax.tick_params(labelsize=8); ax.set_xlabel("E (km, UTM 23S)", fontsize=8); ax.set_ylabel("N (km)", fontsize=8); ax.grid(True, color="#d0d0d0", lw=0.4, ls=":")
L = 5000; sx, sy = ub[0] + 1200, ub[1] + 900
for k, c in enumerate(("k", "w")): ax.add_patch(mpatches.Rectangle((sx + k * L / 2, sy), L / 2, 260, fc=c, ec="k", lw=0.8, zorder=20))
for dx, t in ((0, "0"), (L / 2, "2,5"), (L, "5 km")): ax.text(sx + dx, sy + 450, t, ha="center", fontsize=8, zorder=20)
ax.annotate("", xy=(ub[2] - 1500, ub[3] - 700), xytext=(ub[2] - 1500, ub[3] - 2700), arrowprops=dict(arrowstyle="-|>", color="k", lw=1.4, mutation_scale=12), zorder=20)
ax.text(ub[2] - 1500, ub[3] - 600, "N", ha="center", fontsize=10, fontweight="bold", zorder=20)
ax.set_title("Parte alta da bacia do rio Jundiaí: municípios e rios", fontsize=11)
fig.text(0.01, 0.0, "Fontes: limites municipais do IBGE; rede de drenagem e limite da parte alta do projeto.", fontsize=7)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(OUT, "mapa_alta_jundiai_municipios_rios.png"), dpi=170, bbox_inches="tight", pad_inches=0.12); plt.close(fig)
print("mapa 2 ok")
