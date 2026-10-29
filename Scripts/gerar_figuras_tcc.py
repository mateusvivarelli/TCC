"""
Figuras do texto do TCC (15/10/2026; refeitas em 28/10/2026 com o MODELO OFICIAL: CN-I, lambda 0,05 com S convertido
(Woodward et al., 2003), so escoamento direto, c em log, LOO):
dispersao observado x simulado, escoamento direto SCS-CN x medido, mapa medio.
Saidas em TCC_Texto/figuras/: fig_dispersao.png, fig_volume_direto.png, fig_mapa_sy_medio.png
(fig_decomposicao.png, encostas x termo de base, deixou de existir junto com o termo de base)
"""
import os
import sys

import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.ticker
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from osgeo import gdal

gdal.UseExceptions()
sys.stdout.reconfigure(encoding="utf-8")
DI = r"C:\TCC\Dados Iniciais"; FIG = r"C:\TCC\TCC_Texto\figuras"
os.makedirs(FIG, exist_ok=True)
N = 17
AZUL, CINZA, VERM, LARANJA = "#1f5fa8", "#9a9a9a", "#c0392b", "#d98b1d"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})

sd = pd.read_csv(os.path.join(DI, "comparacao_SY_lambda005_woodward.csv")).sort_values("evento")
ev = pd.read_excel(os.path.join(DI, "eventos_processados_manuais.xlsx"), sheet_name="Sheet1").iloc[:18]
R_ = [ev.iloc[0 if n == 1 else n] for n in range(1, N + 1)]
SY = np.array([float(r["SYY_t"]) for r in R_]); V = np.array([float(r["T_R_m3"]) for r in R_]); QP = np.array([float(r["Q_pico"]) for r in R_])
KLSC = 0.031 * 0.536 * 0.267
ids = np.arange(N)

# ---- IC refeita em LOO (lei de potencia, log) e referencia SY = c*chuva em LOO
Dq = V * QP; ic = np.zeros(N); chuva = np.array([float(r["Chuva_evento_mm"]) for r in R_]); ch = np.zeros(N)
for i in range(N):
    m = ids != i; b, a = np.polyfit(np.log(Dq[m]), np.log(SY[m] / KLSC), 1); ic[i] = np.exp(a) * Dq[i] ** b * KLSC
    ch[i] = np.exp(np.mean(np.log(SY[m]) - np.log(chuva[m]))) * chuva[i]
B = sd.SY_calc_LOO_t.to_numpy(); F = sd.SY_forc_LOO_t.to_numpy()

# ---- Figura 1: dispersao observado x simulado (log-log, faixa de fator 2)
fig, ax = plt.subplots(2, 2, figsize=(10.5, 9.4), sharex=True, sharey=True); ax = ax.ravel()
lim = np.array([10, 30000])
for a_, (tit, sim, cor) in zip(ax, (("SY = c * chuva do evento\n(referência simples, só chuva)", ch, CINZA),
                                    ("Modelo calculado: MUSLE espacializada,\nescoamento direto do SCS-CN (só chuva)", B, AZUL),
                                    ("Modelo forçado: MUSLE espacializada,\nescoamento direto medido", F, VERM),
                                    ("IC (concentrada), com volume total e\npico medidos", ic, LARANJA))):
    a_.fill_between(lim, lim / 2, lim * 2, color="#e8eef6", label="faixa de fator 2")
    a_.plot(lim, lim, color="k", lw=0.8)
    a_.scatter(SY, sim, c=cor, s=34, zorder=3, edgecolor="white", linewidth=0.5)
    for i in range(N):
        a_.annotate(str(i + 1), (SY[i], sim[i]), fontsize=7, xytext=(3, 3), textcoords="offset points", color="#444")
    r = sim / SY; dentro = 100 * np.mean((r >= 0.5) & (r <= 2))
    a_.set_xscale("log"); a_.set_yscale("log"); a_.set_xlim(lim); a_.set_ylim(lim)
    ticks = [10, 100, 1000, 10000]
    for eixo in (a_.xaxis, a_.yaxis):
        eixo.set_major_locator(matplotlib.ticker.FixedLocator(ticks)); eixo.set_major_formatter(matplotlib.ticker.FixedFormatter([f"{t:,}".replace(",", ".") for t in ticks]))
        eixo.set_minor_locator(matplotlib.ticker.NullLocator())
    a_.set_title(tit, fontsize=10); a_.text(0.04, 0.93, f"dentro de fator 2: {dentro:.0f}%\nerro mediano: {np.median(100*np.abs(sim-SY)/SY):.0f}%", transform=a_.transAxes, va="top", fontsize=9)
    a_.set_xlabel("Sedimento medido (t)")
ax[0].set_ylabel("Sedimento simulado, validação leave-one-out (t)"); ax[2].set_ylabel("Sedimento simulado, validação leave-one-out (t)")
for a_ in ax[:2]:
    a_.set_xlabel("")
fig.suptitle("Sedimento simulado x medido nos 17 eventos (números = evento)", fontsize=11)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_dispersao.png"), dpi=150); plt.close(fig)

# ---- Figura 2: escoamento direto do SCS-CN x medido (o gargalo do modelo calculado)
fig, ax = plt.subplots(figsize=(5.6, 5.2))
Vm, Vs = sd.V_dir_medido_m3.to_numpy() / 1e3, sd.V_dir_SCS_m3.to_numpy() / 1e3
lv = np.array([3, 6000])
ax.fill_between(lv, lv / 2, lv * 2, color="#e8eef6", label="faixa de fator 2")
ax.plot(lv, lv, color="k", lw=0.8)
ax.scatter(Vm, Vs, c=AZUL, s=36, zorder=3, edgecolor="white", linewidth=0.5)
for i in range(N):
    ax.annotate(str(i + 1), (Vm[i], Vs[i]), fontsize=7, xytext=(3, 3), textcoords="offset points", color="#444")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(lv); ax.set_ylim(lv)
ax.set_xlabel("Escoamento direto medido, T_R - ΣBt (10³ m³)"); ax.set_ylabel("Escoamento direto do SCS-CN, λ = 0,05 com S convertido (10³ m³)")
r_ = Vs / Vm
ax.text(0.04, 0.95, f"dentro de fator 2: {100*np.mean((r_ >= 0.5) & (r_ <= 2)):.0f}%\nerro mediano: {np.median(100*np.abs(Vs-Vm)/Vm):.0f}%",
        transform=ax.transAxes, va="top", fontsize=9)
ax.set_title("Escoamento direto por evento:\nSCS-CN (λ = 0,05, S convertido) x medido", fontsize=10)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_volume_direto.png"), dpi=150); plt.close(fig)
if os.path.exists(os.path.join(FIG, "fig_decomposicao.png")):
    os.remove(os.path.join(FIG, "fig_decomposicao.png"))

# ---- Figura 3: mapa medio do sedimento das encostas (modelo calculado)
def le(p):
    ds = gdal.Open(p); b = ds.GetRasterBand(1); a = b.ReadAsArray().astype(float); nd = b.GetNoDataValue()
    return np.where((a != nd) & np.isfinite(a), a, np.nan), ds.GetGeoTransform()
m, gt = le(os.path.join(DI, "SY_medio_eventos_l05w.tif"))
ny, nx = m.shape; ext = (gt[0], gt[0] + nx * gt[1], gt[3] + ny * gt[5], gt[3])
masc = gpd.read_file(os.path.join(DI, "Máscara Jundiaí.shp"))
fig, ax = plt.subplots(1, 2, figsize=(13, 4.6))
v = m[np.isfinite(m)]
im = ax[0].imshow(m * 1000, extent=ext, cmap="YlOrRd", vmin=0, vmax=np.percentile(v * 1000, 99.5))
masc.boundary.plot(ax=ax[0], color="k", lw=0.7); ax[0].set_xticks([]); ax[0].set_yticks([]); ax[0].axis("off")
ax[0].set_title("Sedimento médio dos 17 eventos, MC (kg por pixel)", fontsize=10)
plt.colorbar(im, ax=ax[0], fraction=0.04, pad=0.02)
q95 = np.nanpercentile(v, 95); hot = np.where(np.isfinite(m), (m >= q95).astype(float), np.nan)
ax[1].imshow(np.where(np.isfinite(m), 0.0, np.nan), extent=ext, cmap="Greys", vmin=0, vmax=3)
ax[1].imshow(np.where(hot == 1, 1.0, np.nan), extent=ext, cmap="Reds_r", vmin=0, vmax=1.6)
masc.boundary.plot(ax=ax[1], color="k", lw=0.7); ax[1].set_xticks([]); ax[1].set_yticks([]); ax[1].axis("off")
ax[1].set_title("Áreas críticas: 5% dos pixels com maior contribuição", fontsize=10)
for a_ in ax:
    a_.set_xlim(ext[0], ext[1]); a_.set_ylim(ext[2], ext[3])
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_mapa_sy_medio.png"), dpi=150); plt.close(fig)
print("figuras ok:", sorted(f for f in os.listdir(FIG) if f.endswith(".png")))
