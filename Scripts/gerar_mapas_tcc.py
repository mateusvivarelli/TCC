"""
MAPAS DO TCC (15/10/2026): todos com titulo, escala grafica, seta do norte, legenda e coordenadas UTM (SIRGAS 2000 / UTM 23S).

  mapa_01_area_estudo.png      relevo (sombreado), rede de drenagem, postos pluviometricos e exutorio
  mapa_02_solo_uso.png         classes de solo e de uso, com % da area
  mapa_03_fatores.png          K, C, LS e CN (AMC I)
  mapa_04_chuva_eventos.png    chuva interpolada (IDW) nos 17 eventos
  mapa_05_escoamento_eventos.png  escoamento direto (SCS-CN, lambda 0,20) nos 17 eventos
  mapa_06_sedimento_eventos.png   sedimento das encostas (modelo calculado) nos 17 eventos
  mapa_07_sedimento_medio.png  sedimento medio e areas criticas: modelo calculado e forcado ao medido
  mapa_08_evento11.png         cadeia do evento 11 (chuva, S, Q, E_unit, SY)
  fig_fluxograma.png           fluxograma do metodo
Tambem salva TCC_Texto/tabelas/_rasters_forcado (SY forcado medio) em Dados Iniciais/SY_medio_eventos_forcado.tif
"""
import os
import sys

import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from matplotlib.colors import LightSource, ListedColormap, PowerNorm
from matplotlib.lines import Line2D
from osgeo import gdal
from pyproj import Transformer
from scipy.optimize import least_squares

gdal.UseExceptions()
sys.stdout.reconfigure(encoding="utf-8")
BASE = r"C:\TCC"; DI = os.path.join(BASE, "Dados Iniciais"); OUT = os.path.join(BASE, "TCC_Texto", "figuras", "mapas")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 9, "axes.titlesize": 10})
N = 17
COEF, EXPO = 11.8, 0.56

# ---------------------------------------------------------------- dados base
mask_gdf = gpd.read_file(os.path.join(DI, "Máscara Jundiaí.shp"))
dren = gpd.read_file(os.path.join(DI, "drenagem.shp"))
tr = Transformer.from_crs(4326, 31983, always_xy=True)
EST = {"DBT5": tr.transform(-46.4809, -23.2646), "Campo Limpo Paulista": tr.transform(-46.760284, -23.208778)}


def le(p):
    ds = gdal.Open(p); b = ds.GetRasterBand(1)
    a = b.ReadAsArray().astype(np.float64); nd = b.GetNoDataValue()
    ok = np.isfinite(a) & (a > -1e30)
    if nd is not None:
        ok &= a != nd
    return np.where(ok, a, np.nan), ds


K, ds0 = le(os.path.join(DI, "K_raster.tif")); C, _ = le(os.path.join(DI, "C_raster.tif")); LS, _ = le(os.path.join(DI, "LS_moore.tif"))
gt = ds0.GetGeoTransform(); ny, nx = K.shape; A = abs(gt[1] * gt[5])
EXT = (gt[0], gt[0] + nx * gt[1], gt[3] + ny * gt[5], gt[3])            # xmin, xmax, ymin, ymax da grade 884x365
o = gdal.Warp("", gdal.Open(os.path.join(DI, "S - Seco.tif")), format="MEM", width=nx, height=ny,
              outputBounds=(gt[0], gt[3] + ny * gt[5], gt[0] + nx * gt[1], gt[3]), dstSRS=ds0.GetProjection(), resampleAlg=gdal.GRA_NearestNeighbour)
S = o.GetRasterBand(1).ReadAsArray().astype(np.float64); S = np.where(S > -1e30, S, np.nan)
valido = np.isfinite(S) & np.isfinite(K) & np.isfinite(C) & np.isfinite(LS)
ev = pd.read_excel(os.path.join(DI, "eventos_processados_manuais.xlsx"), sheet_name="Sheet1").iloc[:18]
EV = [ev.iloc[0 if n == 1 else n] for n in range(1, N + 1)]


# ---------------------------------------------------------------- elementos cartograficos
def seta_norte(ax, x=0.93, y=0.80, tam=0.11, fs=9):
    ax.annotate("", xy=(x, y + tam), xytext=(x, y), xycoords="axes fraction", textcoords="axes fraction",
                arrowprops=dict(arrowstyle="-|>", color="k", lw=1.4, mutation_scale=11), zorder=20)
    ax.text(x, y + tam + 0.025, "N", transform=ax.transAxes, ha="center", va="bottom", fontsize=fs, fontweight="bold", zorder=20)


def escala(ax, km=5, x0=0.05, y0=0.06, fs=8, compacta=False):
    """barra grafica com 2 segmentos (dados em metros UTM)"""
    xl, yl = ax.get_xlim(), ax.get_ylim()
    L = km * 1000.0; xi = xl[0] + (xl[1] - xl[0]) * x0; yi = yl[0] + (yl[1] - yl[0]) * y0; h = (yl[1] - yl[0]) * 0.014
    for k, cor in enumerate(("k", "w")):
        ax.add_patch(mpatches.Rectangle((xi + k * L / 2, yi), L / 2, h, facecolor=cor, edgecolor="k", lw=0.8, zorder=20))
    rotulos = ((0, "0"), (L, f"{km:g} km")) if compacta else ((0, "0"), (L / 2, f"{km/2:g}".replace(".", ",")), (L, f"{km:g} km"))
    for dx_, txt in rotulos:
        ax.text(xi + dx_, yi + 1.8 * h, txt, ha="center", va="bottom", fontsize=fs, zorder=20,
                bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.7))


def moldura(ax, ext=EXT, grade=True, km=5, titulo=None, fs_t=10, ticks=True, norte=True, compacta=False):
    ax.set_xlim(ext[0], ext[1]); ax.set_ylim(ext[2], ext[3]); ax.set_aspect("equal")
    if ticks:
        ax.xaxis.set_major_locator(mticker.MultipleLocator(10000)); ax.yaxis.set_major_locator(mticker.MultipleLocator(5000))
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v/1000:.0f}")); ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v/1000:.0f}"))
        ax.tick_params(labelsize=7, length=2)
        if grade:
            ax.grid(True, color="#d0d0d0", lw=0.4, ls=":")
        ax.set_xlabel("E (km, UTM 23S)", fontsize=7); ax.set_ylabel("N (km)", fontsize=7)
    else:
        ax.set_xticks([]); ax.set_yticks([])
    for s_ in ax.spines.values():
        s_.set_linewidth(0.8)
    if titulo:
        ax.set_title(titulo, fontsize=fs_t)
    if norte:
        seta_norte(ax, x=0.94, y=0.55, tam=0.28, fs=7) if compacta else seta_norte(ax)
    escala(ax, km=km, fs=6.5 if compacta else 8, compacta=compacta)


def contorno(ax, cor="k", lw=0.7):
    mask_gdf.boundary.plot(ax=ax, color=cor, lw=lw, zorder=8)


def mostra(ax, arr, cmap, vmin=None, vmax=None, norm=None, alpha=1.0):
    return ax.imshow(np.ma.masked_invalid(arr), extent=EXT, cmap=cmap, vmin=None if norm else vmin, vmax=None if norm else vmax, norm=norm,
                     origin="upper", interpolation="nearest", zorder=3, alpha=alpha)


# ================================================================= MAPA 1: area de estudo
dem, dsm = le(os.path.join(DI, "MDE 30m.tif")); gm = dsm.GetGeoTransform()
extd = (gm[0], gm[0] + dsm.RasterXSize * gm[1], gm[3] + dsm.RasterYSize * gm[5], gm[3])
dem_f = np.where(np.isfinite(dem), dem, np.nanmean(dem))
hill = LightSource(azdeg=315, altdeg=40).hillshade(dem_f, vert_exag=3, dx=abs(gm[1]), dy=abs(gm[5]))
fig, ax = plt.subplots(figsize=(11, 5.2))
hill_im = ax.imshow(hill, extent=extd, cmap="Greys", alpha=0.55, origin="upper", zorder=2)
im = ax.imshow(np.ma.masked_invalid(dem), extent=extd, cmap="terrain", alpha=0.55, origin="upper", zorder=3)
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch
_g = mask_gdf.geometry.iloc[0]
_polys = list(_g.geoms) if _g.geom_type == "MultiPolygon" else [_g]
_verts, _codes = [], []
for _pg in _polys:
    for _ring in [_pg.exterior] + list(_pg.interiors):
        _xy = np.asarray(_ring.coords); _verts += list(_xy) + [_xy[0]]; _codes += [MPath.MOVETO] + [MPath.LINETO] * (len(_xy) - 1) + [MPath.CLOSEPOLY]
_clip = PathPatch(MPath(_verts, _codes), transform=ax.transData, fc="none", ec="none")
ax.add_patch(_clip); im.set_clip_path(_clip); hill_im.set_clip_path(_clip)
dren.plot(ax=ax, color="#2b7bba", lw=0.5, zorder=6)
dren[dren.NORIOCOMP == "Rio Jundiaí"].plot(ax=ax, color="#08306b", lw=1.8, zorder=7)
contorno(ax, "k", 1.4)
ax.scatter(*EST["DBT5"], marker="^", s=90, c="#d7191c", edgecolor="k", zorder=10)
ax.scatter(*EST["Campo Limpo Paulista"], marker="^", s=90, c="#d7191c", edgecolor="k", zorder=10)
ax.annotate("DBT5\n(fora da bacia)", EST["DBT5"], xytext=(0, 12), textcoords="offset points", ha="center", fontsize=8, zorder=11, bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.8))
ax.annotate("Campo Limpo Paulista\n(posto de chuva e seção de controle)", EST["Campo Limpo Paulista"], xytext=(8, -28), textcoords="offset points", fontsize=8, zorder=11, bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.8))
moldura(ax, ext=(316500, 352000, 7422500, 7436500), titulo="Área de estudo: parte alta da bacia do rio Jundiaí (137,8 km²)", km=5)
cb = plt.colorbar(im, ax=ax, fraction=0.025, pad=0.01); cb.set_label("Altitude (m)", fontsize=8); cb.ax.tick_params(labelsize=7)
leg = [Line2D([0], [0], color="k", lw=1.4, label="Limite da bacia"), Line2D([0], [0], color="#08306b", lw=1.8, label="Rio Jundiaí"),
       Line2D([0], [0], color="#2b7bba", lw=0.8, label="Rede de drenagem"),
       Line2D([0], [0], marker="^", color="w", markerfacecolor="#d7191c", markeredgecolor="k", markersize=9, label="Posto pluviométrico")]
ax.legend(handles=leg, loc="lower right", fontsize=8, framealpha=0.95, title="Legenda", title_fontsize=8)
fig.text(0.01, 0.005, "Fonte: MDE (USGS), drenagem e limite da bacia do projeto; postos conforme planilha de eventos. Sombreamento a 315°.", fontsize=7)
fig.tight_layout(rect=(0, 0.02, 1, 1)); fig.savefig(os.path.join(OUT, "mapa_01_area_estudo.png"), dpi=170); plt.close(fig)
print("mapa 1 ok")

# ================================================================= MAPA 2: solo e uso (classes)
ped = gpd.read_file(os.path.join(BASE, "Pedologia Alto.shp"), encoding="utf-8")
uso = gpd.read_file(os.path.join(BASE, "Uso Solo Alto.shp"), encoding="utf-8")
ped_c = gpd.clip(ped, mask_gdf); uso_c = gpd.clip(uso, mask_gdf)
area_bac = mask_gdf.geometry.iloc[0].area
cores_solo = {"Argissolos Vermelho-Amarelos": "#d95f02", "Cambissolos Háplicos": "#e6ab02", "Neossolos Litólicos": "#7570b3",
              "Afloramento Rochoso": "#666666", "Área Urbana": "#bdbdbd"}
cores_uso = {"Mata Nativa": "#1b7837", "Silvicultura": "#7fbc41", "Campo": "#d9ef8b", "Lavoura Temporária": "#fdae61",
             "Solo exposto": "#a6611a", "Mineração": "#5e3c99", "Afloramento Rochoso": "#666666", "Área Urbanizada": "#bdbdbd", "Corpos D'Água": "#4575b4"}
fig, axs = plt.subplots(1, 2, figsize=(13, 5.4))
for ax, gdf, camp, cores, tit in ((axs[0], ped_c, "Subordem", cores_solo, "Classes de solo (mapa pedológico)"), (axs[1], uso_c, "CLASSE", cores_uso, "Uso e cobertura do solo")):
    pat = []
    for cl, cor in cores.items():
        sel = gdf[gdf[camp] == cl]
        if len(sel):
            sel.plot(ax=ax, color=cor, lw=0, zorder=3)
            pat.append(mpatches.Patch(color=cor, label=f"{cl} ({100*sel.geometry.area.sum()/area_bac:.1f}%)".replace(".", ",")))
    contorno(ax, "k", 1.0); moldura(ax, titulo=tit, km=5)
    ax.legend(handles=pat, loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, fontsize=7.5, framealpha=0.95, title="Legenda (% da área da bacia)", title_fontsize=8)
fig.suptitle("Solo e uso do solo na área de estudo", fontsize=11, y=0.98)
fig.text(0.01, 0.005, "Fonte: Plano de Bacias (Consórcio Profill-Rhama, 2020), conforme a IC. Recorte pela máscara da bacia.", fontsize=7)
fig.tight_layout(rect=(0, 0.02, 1, 0.95)); fig.savefig(os.path.join(OUT, "mapa_02_solo_uso.png"), dpi=170); plt.close(fig)
print("mapa 2 ok")

# ================================================================= MAPA 3: K, C, LS, CN
cn1, _ = le(os.path.join(BASE, "Evento11_Auditoria", "3_Rasters_QGIS", "CN_I_alinhado.tif"))
fig, axs = plt.subplots(2, 2, figsize=(13, 7.6))
for ax, arr, cmap, tit, rot, vmax in ((axs[0, 0], K, "YlOrBr", "Erodibilidade do solo, K", "K (t·h/MJ/mm)", None),
                                      (axs[0, 1], C, "YlGn_r", "Cobertura e manejo, C", "C (adimensional)", None),
                                      (axs[1, 0], LS, "magma_r", "Fator topográfico, LS", "LS (adimensional)", np.nanpercentile(LS, 99.5)),
                                      (axs[1, 1], cn1, "RdYlBu_r", "Número de curva, condição seca (AMC I)", "CN (adimensional)", None)):
    im = mostra(ax, arr, cmap, vmin=np.nanmin(arr), vmax=vmax if vmax else np.nanmax(arr)); contorno(ax)
    moldura(ax, titulo=tit, km=5); cb = plt.colorbar(im, ax=ax, fraction=0.03, pad=0.01); cb.set_label(rot, fontsize=8); cb.ax.tick_params(labelsize=7)
fig.suptitle("Fatores espacializados da MUSLE e do SCS-CN", fontsize=11, y=1.0)
fig.text(0.01, 0.005, "Pixels de ~30 m (897,49 m²). C = 0 em áreas urbanas e corpos d'água; LS limitado ao percentil 99,5 na escala de cores.", fontsize=7)
fig.tight_layout(rect=(0, 0.015, 1, 0.97)); fig.savefig(os.path.join(OUT, "mapa_03_fatores.png"), dpi=170); plt.close(fig)
print("mapa 3 ok")


# ================================================================= MAPAS 4-6: 17 eventos
def multiplos(arqs, cmap, rot, titulo, nome, vmin=0.0, vmax=None, fator=1.0, nota="", gamma=1.0):
    arrs = [le(a)[0] * fator for a in arqs]
    for a_ in arrs:
        a_[~valido] = np.nan
    vmax = vmax if vmax else float(np.nanpercentile(np.concatenate([a_[np.isfinite(a_)] for a_ in arrs]), 99.5))
    fig = plt.figure(figsize=(14, 11.2)); gs = fig.add_gridspec(5, 4, hspace=0.22, wspace=0.10, height_ratios=[1, 1, 1, 1, 1], left=0.03, right=0.985, top=0.93, bottom=0.07)
    im = None
    for i, a_ in enumerate(arrs):
        ax = fig.add_subplot(gs[i // 4, i % 4])
        im = mostra(ax, a_, cmap, norm=PowerNorm(gamma=gamma, vmin=vmin, vmax=vmax) if gamma != 1 else None, vmin=vmin, vmax=vmax); contorno(ax, lw=0.5)
        r = EV[i]
        moldura(ax, ticks=False, km=5, compacta=True, titulo=f"Evento {i+1} ({pd.to_datetime(r['Inicio']).strftime('%d/%m/%Y')}; R = {r['Chuva_evento_mm']:.0f} mm)".replace(".", ","), fs_t=8.5)
        ax.title.set_fontsize(8.5)
    axl = fig.add_subplot(gs[4, 1:]); axl.axis("off")
    cax = axl.inset_axes([0.05, 0.55, 0.9, 0.16]); cb = fig.colorbar(im, cax=cax, orientation="horizontal"); cb.set_label(rot, fontsize=9); cb.ax.tick_params(labelsize=8)
    axl.text(0.5, 0.15, nota, ha="center", va="center", fontsize=8, transform=axl.transAxes)
    fig.suptitle(titulo, fontsize=12, y=0.985)
    fig.savefig(os.path.join(OUT, nome), dpi=150); plt.close(fig)


multiplos([os.path.join(BASE, f"Evento {n}", f"ChuvaIDW{n}.tif") for n in range(1, N + 1)], "Blues", "Chuva interpolada do evento (mm)",
          "Chuva total de cada evento, interpolada por IDW a partir de dois postos", "mapa_04_chuva_eventos.png", vmin=0,
          nota="Escala comum a todos os eventos. Escala gráfica de 5 km em cada mapa; norte para cima; limite da bacia em preto.")
multiplos([os.path.join(BASE, f"Evento {n}", f"Qdir{n}_b2.tif") for n in range(1, N + 1)], "PuBuGn", "Escoamento direto (mm)",
          "Escoamento direto calculado pelo SCS-CN (CN seco, λ = 0,20) em cada evento", "mapa_05_escoamento_eventos.png", vmin=0, gamma=0.5,
          nota="Escala comum a todos os eventos, com realce dos valores baixos (raiz quadrada); valores acima do percentil 99,5 saturados. Escala gráfica de 5 km; norte para cima.")
multiplos([os.path.join(BASE, f"Evento {n}", f"SY{n}_b2.tif") for n in range(1, N + 1)], "YlOrRd", "Sedimento das encostas (kg por pixel)",
          "Sedimento produzido nas encostas em cada evento (MC)", "mapa_06_sedimento_eventos.png", vmin=0, fator=1000.0, gamma=0.5,
          nota="Escala comum a todos os eventos, com realce dos valores baixos (raiz quadrada); valores acima do percentil 99,5 saturados.\nMostra só a parcela das encostas (c₁ · E_unit). Escala gráfica de 5 km; norte para cima.")
print("mapas 4-6 ok")

# ================================================================= B forcado ao medido (mapa medio)
h = pd.read_excel(os.path.join(DI, "Dados_finais_histereses_corrigido.xlsx"), sheet_name="Planilha1").iloc[:, :8]
h.columns = ["Data", "P1", "P2", "Ptot", "Q", "CSS", "Bt", "CSSBt"]; h["Data"] = pd.to_datetime(h["Data"]); h = h.set_index("Data")
SY = np.zeros(N); VD = np.zeros(N); BTV = np.zeros(N); RI = np.zeros(N); R = np.zeros(N)
Pv = []; KCLS = (K * C * LS)[valido]; Sv = S[valido]
for n in range(1, N + 1):
    r = EV[n - 1]; w = h.loc[r["Inicio"]:r["Fim"]]
    SY[n - 1] = r["SYY_t"]; VD[n - 1] = (w.Q - w.Bt).sum() * 3600; BTV[n - 1] = w.Bt.sum() * 3600; RI[n - 1] = r["Intensidade_60min_mm/h"]; R[n - 1] = r["Chuva_evento_mm"]
    Pv.append(le(os.path.join(BASE, f"Evento {n}", f"ChuvaIDW{n}.tif"))[0][valido])


def qf(i, V=None):
    p = Pv[i]; Q = np.where(p <= 0.2 * Sv, 0.0, (p - 0.2 * Sv) ** 2 / (p + 0.8 * Sv))
    if V is not None:
        Q = np.minimum(V / (Q.sum() / 1000.0 * A) * Q, p)
    return Q


def Ep(Q, i):
    pr = Q / 1000.0 * A * (RI[i] / R[i]) / 3600.0
    return COEF * np.maximum(Q * pr * A, 0.0) ** EXPO * KCLS


Qforc = [qf(i, VD[i]) for i in range(N)]; Eforc = [Ep(Qforc[i], i) for i in range(N)]
Esum = np.array([e.sum() for e in Eforc])
fobj = lambda p: np.log(np.clip(p[0] * Esum + p[1] * BTV, 1e-9, None)) - np.log(SY)
best = min((least_squares(fobj, s0, bounds=(0, np.inf), x_scale="jac") for s0 in ([SY.mean() / Esum.mean(), 0.0], [0.0, SY.mean() / BTV.mean()], [0.5 * SY.mean() / Esum.mean(), 0.5 * SY.mean() / BTV.mean()])), key=lambda r: r.cost)
c1f, c2f = best.x
print(f"B forcado: c1 = {c1f:.5f}  c2 = {c2f:.6f}")
SYf_mean = np.full((ny, nx), np.nan); SYf_mean[valido] = np.mean([c1f * e for e in Eforc], axis=0)
SYc_mean, _ = le(os.path.join(DI, "SY_medio_eventos_b2.tif"))
for nome, arr in (("SY_medio_eventos_forcado.tif", SYf_mean),):
    outd = gdal.GetDriverByName("GTiff").Create(os.path.join(DI, nome), nx, ny, 1, gdal.GDT_Float32)
    outd.SetGeoTransform(gt); outd.SetProjection(ds0.GetProjection()); b_ = outd.GetRasterBand(1)
    b_.WriteArray(np.where(np.isfinite(arr), arr, -9999).astype(np.float32)); b_.SetNoDataValue(-9999); b_.FlushCache(); outd = None

# ================================================================= MAPA 7: sedimento medio e areas criticas
fig, axs = plt.subplots(2, 2, figsize=(13, 8))
for col, (arr, nome) in enumerate(((SYc_mean, "Modelo Calculado (MC): água estimada da chuva"), (SYf_mean, "Modelo Forçado ao Medido (MFM): água medida"))):
    v = arr[np.isfinite(arr)]; vmax = np.percentile(v * 1000, 99.5)
    im = mostra(axs[0, col], arr * 1000, "YlOrRd", vmin=0, vmax=vmax); contorno(axs[0, col])
    moldura(axs[0, col], titulo=f"Sedimento médio dos 17 eventos\n{nome}", km=5)
    cb = plt.colorbar(im, ax=axs[0, col], fraction=0.03, pad=0.01); cb.set_label("kg por pixel (médio por evento)", fontsize=8); cb.ax.tick_params(labelsize=7)
    q95 = np.nanpercentile(v, 95); hot = np.where(np.isfinite(arr), np.where(arr >= q95, 1.0, 0.0), np.nan)
    axs[1, col].imshow(np.ma.masked_invalid(np.where(np.isfinite(arr), 0.0, np.nan)), extent=EXT, cmap=ListedColormap(["#f0f0f0"]), zorder=2)
    axs[1, col].imshow(np.ma.masked_where(hot != 1, hot), extent=EXT, cmap=ListedColormap(["#b10026"]), zorder=4, interpolation="nearest")
    contorno(axs[1, col]); moldura(axs[1, col], titulo="Áreas críticas: 5% dos pixels de maior contribuição", km=5)
    axs[1, col].legend(handles=[mpatches.Patch(color="#b10026", label="Áreas críticas (5% superiores)"), mpatches.Patch(color="#f0f0f0", ec="k", label="Demais áreas da bacia")],
                       loc="lower right", fontsize=7, framealpha=0.92)
a_ = SYc_mean[valido]; b_ = SYf_mean[valido]
fig.suptitle("Sedimento médio e áreas críticas (correlação entre os dois mapas: r = " + f"{np.corrcoef(a_, b_)[0,1]:.2f}".replace(".", ",") + ")", fontsize=11, y=1.0)
fig.text(0.01, 0.005, "Parcela das encostas apenas. Áreas críticas = pixels acima do percentil 95 de cada mapa. Valores em kg por pixel de 897 m².", fontsize=7)
fig.tight_layout(rect=(0, 0.015, 1, 0.97)); fig.savefig(os.path.join(OUT, "mapa_07_sedimento_medio.png"), dpi=170); plt.close(fig)
q1, q2 = np.nanpercentile(SYc_mean[valido], 95), np.nanpercentile(SYf_mean[valido], 95)
print(f"mapa 7 ok | r(calculado, forcado) = {np.corrcoef(a_, b_)[0,1]:.3f} | areas criticas coincidentes = {100*np.sum((a_>=q1)&(b_>=q2))/np.sum(a_>=q1):.1f}%")

# ================================================================= MAPA 8: cadeia do evento 11
E11 = Path = None
pastas = os.path.join(BASE, "Evento 11")
q11, _ = le(os.path.join(pastas, "Qdir11_b2.tif")); e11, _ = le(os.path.join(pastas, "E_unit11_b2.tif")); s11, _ = le(os.path.join(pastas, "SY11_b2.tif")); p11, _ = le(os.path.join(pastas, "ChuvaIDW11.tif"))
fig, axs = plt.subplots(2, 3, figsize=(14, 7.2))
pan = [(p11, "Blues", "Chuva do evento (IDW)", "mm", None), (S, "YlOrBr", "Retenção potencial S (CN seco)", "mm", None),
       (q11, "PuBuGn", "Escoamento direto (SCS-CN, λ = 0,20)", "mm", None), (e11 * 1000, "YlOrRd", "Índice de erosão E_unit (Williams)", "kg por pixel, sem calibrar", 99.5),
       (s11 * 1000, "YlOrRd", "Sedimento das encostas (c₁ · E_unit)", "kg por pixel", 99.5), (None, None, None, None, None)]
for ax, (arr, cm, tit, rot, pc) in zip(axs.ravel(), pan):
    if arr is None:
        ax.axis("off"); continue
    arr = np.where(valido, arr, np.nan)
    im = mostra(ax, arr, cm, vmin=np.nanmin(arr), vmax=np.nanpercentile(arr, pc) if pc else np.nanmax(arr)); contorno(ax)
    moldura(ax, titulo=tit, km=5); cb = plt.colorbar(im, ax=ax, fraction=0.03, pad=0.01); cb.set_label(rot, fontsize=8); cb.ax.tick_params(labelsize=7)
_c2 = pd.read_csv(os.path.join(DI, "comparacao_SY_dois_componentes.csv")).set_index("evento").loc[11]
_s11, _e11, _b11 = _c2.SY_total_sim_t, _c2.SY_encostas_t, _c2.SY_base_t
axs[1, 2].text(0.02, 0.9, "Evento 11 (04 a 08/07/2019)", fontsize=10, fontweight="bold", transform=axs[1, 2].transAxes, va="top")
axs[1, 2].text(0.02, 0.8, f"Chuva ponderada: {EV[10]['Chuva_evento_mm']:.1f} mm\nIntensidade máxima em 60 min: {EV[10]['Intensidade_60min_mm/h']:.1f} mm/h\n"
               f"Volume total medido: {EV[10]['T_R_m3']/1e6:.2f} milhões de m³\nSedimento medido: {EV[10]['SYY_t']:,.0f} t\n\n"
               f"MC: {_s11:,.0f} t\n   encostas {_e11:,.0f} t + vazão de base {_b11:,.0f} t".replace(",", "."), fontsize=9, transform=axs[1, 2].transAxes, va="top", linespacing=1.5)
fig.suptitle("Da chuva ao sedimento no evento 11: etapas espaciais do modelo", fontsize=12, y=1.0)
fig.tight_layout(rect=(0, 0, 1, 0.97)); fig.savefig(os.path.join(OUT, "mapa_08_evento11.png"), dpi=170); plt.close(fig)
print("mapa 8 ok")

# ================================================================= FLUXOGRAMA
fig, ax = plt.subplots(figsize=(12, 8.6)); ax.set_xlim(0, 12); ax.set_ylim(-1.2, 7.7); ax.axis("off")


def caixa(xc, y, w, h, txt, cor, fs=9):
    ax.add_patch(mpatches.FancyBboxPatch((xc - w / 2, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.12", fc=cor, ec="#333", lw=1.0, zorder=3))
    ax.text(xc, y + h / 2, txt, ha="center", va="center", fontsize=fs, zorder=4, linespacing=1.35)


def seta(x0, y0, x1, y1, ls="-"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", lw=1.3, color="#333", linestyle=ls), zorder=2)


ent, pro, res, obs = "#dbe9f6", "#fff2cc", "#e2f0d9", "#fce4d6"
C1, C2, C3, W = 2.2, 6.0, 9.8, 3.5
caixa(C1, 6.6, W, 0.85, "Chuva horária\nnos 2 postos (17 eventos)", ent)
caixa(C2, 6.6, W, 0.85, "Mapas de solo, uso e relevo\n→ CN, K, C e LS (raster de 30 m)", ent)
caixa(C3, 6.6, W, 0.85, "Medições no exutório:\nvazão, sedimento e vazão de base", obs)
caixa(C1, 5.2, W, 0.85, "Interpolação IDW\n→ chuva P em cada pixel", pro)
caixa(C2, 5.2, W, 0.85, "SCS-CN (λ = 0,20)\n→ escoamento direto Q do pixel", pro)
caixa(C3, 5.2, W, 0.85, "Sedimento medido SY_obs = Σ Q·CSS\nvolume direto e base medidos", obs)
caixa(C2, 3.8, W + 0.6, 0.85, "pr = Q·(RI/R);  E_unit = 11,8·(Q·pr·A)^0,56·K·LS·C\n(erosão local do pixel, índice relativo)", pro, 8.5)
caixa(C3, 3.8, W, 0.85, "Termo de base\nMC: Qb_inicio × T_chuva\nMFM: Σ Bt medida", pro, 8.5)
caixa(C2, 2.4, W, 0.85, "Soma de E_unit sobre os pixels\n(parcela das encostas)", pro)
caixa(6.4, 0.7, 8.2, 1.0, "SY = c₁ · ΣE_unit  +  c₂ · (termo de base)\nc₁ e c₂ ajustados em escala logarítmica contra SY_obs; validação leave-one-out aninhada", res)
caixa(3.0, -0.9, 4.6, 0.8, "Mapa de áreas críticas\n(c₁ · E_unit em cada pixel)", res, 8.5)
caixa(9.4, -0.9, 4.6, 0.8, "Métricas e comparação com\ntestes simples e com a IC", res, 8.5)
for (x0, y0, x1, y1) in ((C1, 6.6, C1, 6.05), (C2, 6.6, C2, 6.05), (C3, 6.6, C3, 6.05), (C1 + W / 2, 5.62, C2 - W / 2, 5.62),
                         (C2, 5.2, C2, 4.65), (C3, 5.2, C3, 4.65), (C2, 3.8, C2, 3.25), (C2, 2.4, C2, 1.7), (C3, 3.8, C3, 1.7),
                         (4.2, 0.7, 3.4, -0.1), (8.6, 0.7, 9.0, -0.1)):
    seta(x0, y0, x1, y1)
# alvo da calibracao: linha tracejada pela margem direita ate a caixa da equacao
ax.plot([C3 + W / 2, 11.85, 11.85], [5.62, 5.62, 1.2], ls="--", lw=1.3, color="#7a3b16", zorder=2)
seta(11.85, 1.2, 10.5, 1.2, ls="--")
ax.text(11.75, 3.6, "alvo da calibração", rotation=90, fontsize=8, color="#7a3b16", ha="right", va="center")
fig.suptitle("Fluxograma do método (azul: entradas; amarelo: cálculos; laranja: dados medidos usados como alvo ou, no MFM, como entrada; verde: resultados)", fontsize=9.5, y=0.97)
fig.savefig(os.path.join(OUT, "fig_fluxograma.png"), dpi=170, bbox_inches="tight"); plt.close(fig)
print("fluxograma ok")
