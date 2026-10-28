"""Figuras ilustrativas (27/10/2026, nao sao do TCC): configuracoes testadas, agua, sedimento e mapa do candidato
(CN-I, lambda 0,05, S convertido por Woodward et al., 2003) contra o adotado hoje. Saida: Figuras/ilustrativas_27-10/."""
import os
import sys

import numpy as np
import pandas as pd
from osgeo import gdal
from scipy.optimize import least_squares
from scipy.stats import spearmanr

gdal.UseExceptions()
sys.stdout.reconfigure(encoding="utf-8")
BASE = r"C:\TCC"; DI = os.path.join(BASE, "Dados Iniciais")
COEF, EXPO, LAM, N = 11.8, 0.56, 0.20, 17
rng = np.random.default_rng(15102026)


def le(p):
    ds = gdal.Open(p); b = ds.GetRasterBand(1)
    a = b.ReadAsArray().astype(np.float64); nd = b.GetNoDataValue()
    ok = np.isfinite(a) & (a > -1e30)
    if nd is not None:
        ok &= a != nd
    return np.where(ok, a, np.nan), ds


def salva(caminho, arr, ref_ds, nodata=-9999.0):
    out = gdal.GetDriverByName("GTiff").Create(caminho, arr.shape[1], arr.shape[0], 1, gdal.GDT_Float32)
    out.SetGeoTransform(ref_ds.GetGeoTransform()); out.SetProjection(ref_ds.GetProjection())
    b = out.GetRasterBand(1); b.WriteArray(np.where(np.isfinite(arr), arr, nodata).astype(np.float32)); b.SetNoDataValue(nodata)
    b.FlushCache(); out = None


K, ds0 = le(os.path.join(DI, "K_raster.tif")); C, _ = le(os.path.join(DI, "C_raster.tif")); LS, _ = le(os.path.join(DI, "LS_moore.tif"))
gt = ds0.GetGeoTransform(); ny, nx = K.shape; A = abs(gt[1] * gt[5])
o = gdal.Warp("", gdal.Open(os.path.join(DI, "S - Seco.tif")), format="MEM", width=nx, height=ny,
              outputBounds=(gt[0], gt[3] + ny * gt[5], gt[0] + nx * gt[1], gt[3]), dstSRS=ds0.GetProjection(), resampleAlg=gdal.GRA_NearestNeighbour)
S = o.GetRasterBand(1).ReadAsArray().astype(np.float64); S = np.where(S > -1e30, S, np.nan)
valido = np.isfinite(S) & np.isfinite(K) & np.isfinite(C) & np.isfinite(LS)
KCLS = (K * C * LS)[valido]; Sv = S[valido]

ev = pd.read_excel(os.path.join(DI, "eventos_processados_manuais.xlsx"), sheet_name="Sheet1").iloc[:18]
h = pd.read_excel(os.path.join(DI, "Dados_finais_histereses_corrigido.xlsx"), sheet_name="Planilha1").iloc[:, :8]
h.columns = ["Data", "P1", "P2", "Ptot", "Q", "CSS", "Bt", "CSSBt"]; h["Data"] = pd.to_datetime(h["Data"]); h = h.set_index("Data")

SY = np.zeros(N); TR = np.zeros(N); BTV = np.zeros(N); RI = np.zeros(N); R = np.zeros(N); Qb0 = np.zeros(N); durH = np.zeros(N); durR = np.zeros(N)
Pv = []
for n in range(1, N + 1):
    r = ev.iloc[0 if n == 1 else n]; w = h.loc[r["Inicio"]:r["Fim"]]
    SY[n - 1] = r["SYY_t"]; TR[n - 1] = r["T_R_m3"]; BTV[n - 1] = w.Bt.sum() * 3600
    RI[n - 1] = r["Intensidade_60min_mm/h"]; R[n - 1] = r["Chuva_evento_mm"]; Qb0[n - 1] = r["Qb_inicio"]
    durH[n - 1] = r["Duracao_horas"]; durR[n - 1] = max(r["Tempo_precipitacao_p1_h"], r["Tempo_precipitacao_p2_h"])
    Pv.append(le(os.path.join(BASE, f"Evento {n}", f"ChuvaIDW{n}.tif"))[0][valido])
VD = TR - BTV
print(f"duracao da chuva (h): min={durR.min():.0f} max={durR.max():.0f} | duracao da janela (h): min={durH.min():.0f} max={durH.max():.0f} | r(durR, durH)={np.corrcoef(durR, durH)[0,1]:.2f}")


def qdir(i, lam=LAM):
    p = Pv[i]
    return np.where(p <= lam * Sv, 0.0, (p - lam * Sv) ** 2 / (p + (1 - lam) * Sv))


def edir(i, lam=LAM):
    Q = qdir(i, lam); pr = Q / 1000.0 * A * (RI[i] / R[i]) / 3600.0
    return np.sum(COEF * np.maximum(Q * pr * A, 0.0) ** EXPO * KCLS)


E05 = np.array([edir(i, 0.05) for i in range(N)])
E20 = np.array([edir(i, 0.20) for i in range(N)])
X2 = {"chuva": Qb0 * durR * 3600.0, "hidrograma": Qb0 * durH * 3600.0, "observada": BTV}


def fit2(x1, x2, y):
    f = lambda p: np.log(np.clip(p[0] * x1 + p[1] * x2, 1e-9, None)) - np.log(y)
    best = None
    for s0 in ([y.mean() / x1.mean(), 0.0], [0.0, y.mean() / x2.mean()], [0.5 * y.mean() / x1.mean(), 0.5 * y.mean() / x2.mean()]):
        r = least_squares(f, s0, bounds=(0, np.inf), x_scale="jac")
        if best is None or r.cost < best.cost:
            best = r
    return best.x


def fit1(x, y):
    return np.exp(np.mean(np.log(y) - np.log(x)))



# ===================== FIGURAS ILUSTRATIVAS (27/10/2026) - nao sao figuras do TCC =====================
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
OUT = os.path.join(BASE, "Figuras", "ilustrativas_27-10"); os.makedirs(OUT, exist_ok=True)
AZUL, LARANJA, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
TXT, TXT2, GRADE, FUNDO = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#b5b4ae",
                     "axes.labelcolor": TXT2, "xtick.color": TXT2, "ytick.color": TXT2, "figure.facecolor": FUNDO, "axes.facecolor": FUNDO})

# ---- A: as cinco configuracoes testadas (numeros dos testes de 27/10)
cfg = ["CN-I, λ 0,20\n(adotado hoje)", "CN-I, λ 0,05\nsem converter", "CN-I, λ 0,05\nS convertido\n(candidato)", "CN-II, λ 0,20", "AMC de cada\nevento, λ 0,05"]
vies = [-12, 94, 3, 173, 85]; mc = [97.9, 63.2, 81.1, 67.5, 72.6]; mf = [38.7, 18.5, 20.6, 19.8, 18.4]
mc2 = [24, 47, 35, 41, 59]; mf2 = [94, 94, 94, 94, 94]
fig, ax = plt.subplots(1, 3, figsize=(17.5, 5.4))
x = np.arange(len(cfg)); cores = [AZUL] * len(cfg); cores[2] = LARANJA
paineis = ((ax[0], vies, "1. A água: viés do escoamento direto do SCS-CN\n(soma dos 17 eventos x medido; ideal = 0)", None, None, None),
           (ax[1], mc, "2. Modelo calculado (só chuva):\nerro mediano do sedimento", 41.9, "SY = c · chuva (41,9%)", mc2),
           (ax[2], mf, "3. Modelo forçado (água medida): erro mediano do sedimento\n(todas as configurações com 94% em fator 2)", 16.3, "IC concentrada (16,3%)", None))
for a_, val, tit, ref, reflab, sub in paineis:
    b = a_.bar(x, val, 0.62, color=cores, zorder=3)
    a_.axhline(0, color="#8d8c86", lw=0.8, zorder=2)
    if ref is not None:
        a_.axhline(ref, color=TXT2, lw=1.2, ls="--", zorder=4)
        a_.text(-0.45, ref + 0.8, reflab, ha="left", va="bottom", fontsize=8.5, color=TXT2, zorder=5, bbox=dict(fc=FUNDO, ec="none", pad=1))
    for i, rr in enumerate(b):
        v = val[i]
        lab = (f"{v:+.0f}%" if a_ is ax[0] else f"{v:.0f}%") if sub is None else f"{v:.0f}%\n({sub[i]}% em fator 2)"
        a_.text(rr.get_x() + rr.get_width() / 2, v + (3 if v >= 0 else -3), lab, ha="center", va="bottom" if v >= 0 else "top", fontsize=8.5, color=TXT)
    a_.set_xticks(x); a_.set_xticklabels(cfg, fontsize=8); a_.set_title(tit, fontsize=10, color=TXT, loc="left")
    a_.yaxis.grid(True, color=GRADE, lw=0.6, zorder=0); a_.set_axisbelow(True)
ax[0].set_ylabel("%"); ax[1].set_ylabel("erro percentual mediano (%)"); ax[1].set_ylim(0, 122); ax[2].set_ylim(0, 46); ax[0].set_ylim(-30, 200)
fig.suptitle("Só o candidato (laranja) acerta a água e corrige o modelo forçado; os outros melhoram o sedimento inflando a água",
             fontsize=11.5, color=TXT, x=0.01, ha="left")
fig.tight_layout(rect=(0, 0, 1, 0.93)); fig.savefig(os.path.join(OUT, "A_configuracoes_testadas.png"), dpi=150); plt.close(fig)

# ---- B: escoamento direto SCS-CN x medido por evento, adotado x candidato
sd = pd.read_csv(os.path.join(DI, "comparacao_SY_so_direto.csv")).sort_values("evento")
cd = pd.read_csv(os.path.join(DI, "comparacao_SY_lambda005_woodward.csv")).sort_values("evento")
fig, ax = plt.subplots(figsize=(6.4, 5.8)); lv = np.array([3, 8000])
ax.fill_between(lv, lv / 2, lv * 2, color="#e8eef6", zorder=1, label="faixa de fator 2"); ax.plot(lv, lv, color="#8d8c86", lw=0.8, zorder=2)
for i in range(N):
    x0, y0, y1 = sd.V_dir_medido_m3.iloc[i] / 1e3, sd.V_dir_SCS_m3.iloc[i] / 1e3, cd.V_dir_SCS_m3.iloc[i] / 1e3
    ax.plot([x0, x0], [y0, y1], color="#c9c8c2", lw=0.8, zorder=2)
    ax.annotate(str(i + 1), (x0, max(y0, y1)), xytext=(3, 3), textcoords="offset points", fontsize=7, color=TXT2)
for d_, cor, lab in ((sd, AZUL, "CN-I, λ 0,20 (adotado hoje)"), (cd, LARANJA, "CN-I, λ 0,05, S convertido (candidato)")):
    ax.scatter(d_.V_dir_medido_m3 / 1e3, d_.V_dir_SCS_m3 / 1e3, s=46, color=cor, edgecolor=FUNDO, linewidth=1.5, zorder=3, label=lab)
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(lv); ax.set_ylim(lv)
ax.set_xlabel("escoamento direto medido (mil m³)"); ax.set_ylabel("escoamento direto do SCS-CN (mil m³)")
ax.set_title("A água: nos eventos pequenos, o candidato deixa de zerar\no escoamento (linha cinza = mesmo evento)", fontsize=10, color=TXT, loc="left")
ax.legend(frameon=False, fontsize=8.5, loc="upper left"); fig.tight_layout(); fig.savefig(os.path.join(OUT, "B_volume_scs_x_medido.png"), dpi=150); plt.close(fig)

# ---- C: sedimento simulado x medido (LOO), configuracao candidata
fig, axs = plt.subplots(2, 2, figsize=(10, 9.2), sharex=True, sharey=True); lim = np.array([40, 15000])
pain = [("SY = c · chuva (referência, só chuva)", cd.SY_chuva_LOO_t, "#8d8c86"), ("Calculado, candidato (só chuva)", cd.SY_calc_LOO_t, AZUL),
        ("Forçado, candidato (água medida)", cd.SY_forc_LOO_t, LARANJA), ("IC concentrada (volume e pico medidos)", cd.SY_IC_LOO_t, AQUA)]
obs = cd.SY_obs_t.to_numpy()
for a_, (tit, sim, cor) in zip(axs.ravel(), pain):
    sim = sim.to_numpy()
    a_.fill_between(lim, lim / 2, lim * 2, color="#e8eef6", zorder=1); a_.plot(lim, lim, color="#8d8c86", lw=0.8, zorder=2)
    a_.scatter(obs, sim, s=44, color=cor, edgecolor=FUNDO, linewidth=1.5, zorder=3)
    for i in range(N):
        a_.annotate(str(i + 1), (obs[i], sim[i]), xytext=(3, 3), textcoords="offset points", fontsize=7, color=TXT2)
    r_ = sim / obs
    a_.text(0.04, 0.95, f"erro mediano {np.median(100*np.abs(sim-obs)/obs):.0f}%\n{100*np.mean((r_>=0.5)&(r_<=2)):.0f}% dentro de fator 2",
            transform=a_.transAxes, va="top", fontsize=9, color=TXT)
    a_.set_xscale("log"); a_.set_yscale("log"); a_.set_xlim(lim); a_.set_ylim(lim); a_.set_title(tit, fontsize=10, color=TXT, loc="left")
for a_ in axs[1]:
    a_.set_xlabel("sedimento medido (t)")
for a_ in axs[:, 0]:
    a_.set_ylabel("sedimento simulado, validação cruzada (t)")
fig.suptitle("O sedimento: com a água medida, o modelo espacializado candidato empata com a IC", fontsize=11.5, color=TXT, x=0.01, ha="left")
fig.tight_layout(rect=(0, 0, 1, 0.95)); fig.savefig(os.path.join(OUT, "C_sedimento_candidato.png"), dpi=150); plt.close(fig)

# ---- D: onde cai a agua: % do volume em pixels sem erosao (C = 0 ou K = 0)
Cv, Kv = C[valido], K[valido]; zero = (Cv == 0) | (Kv == 0)
Sc = 25.4 * 1.33 * (Sv / 25.4) ** 1.15


def frac(Sx, lam):
    out = []
    for i in range(N):
        p = Pv[i]; Q = np.where(p <= lam * Sx, 0.0, (p - lam * Sx) ** 2 / (p + (1 - lam) * Sx)); out.append(Q[zero].sum() / Q.sum())
    return 100 * np.array(out)


f20, f05 = frac(Sv, 0.20), frac(Sc, 0.05)
fig, ax = plt.subplots(figsize=(11, 4.4)); xe = np.arange(1, N + 1); w = 0.38
ax.bar(xe - w / 2 - 0.02, f20, w, color=AZUL, zorder=3, label="CN-I, λ 0,20 (adotado hoje)")
ax.bar(xe + w / 2 + 0.02, f05, w, color=LARANJA, zorder=3, label="CN-I, λ 0,05, S convertido (candidato)")
ax.axhline(100 * zero.mean(), color=TXT2, ls="--", lw=1.1, zorder=4)
ax.text(0.6, 100 * zero.mean() + 1.5, f"fração da bacia sem erosão ({100*zero.mean():.0f}%)", ha="left", fontsize=8.5, color=TXT2)
ax.set_xticks(xe); ax.set_xlabel("evento (chuva do evento em mm, abaixo)"); ax.set_xticklabels([f"{n}\n{R[n-1]:.0f}" for n in xe], fontsize=8)
ax.set_ylabel("% do volume em pixel sem erosão"); ax.set_ylim(0, 100); ax.yaxis.grid(True, color=GRADE, lw=0.6, zorder=0); ax.set_axisbelow(True)
ax.set_title("Por que λ 0,20 falha: nas chuvas pequenas, a água vai para as áreas urbanas (C = 0), onde o modelo não erode",
             fontsize=10, color=TXT, loc="left")
ax.legend(frameon=False, fontsize=8.5, loc="upper right"); fig.tight_layout(); fig.savefig(os.path.join(OUT, "D_agua_em_pixels_sem_erosao.png"), dpi=150); plt.close(fig)

# ---- E: mapas medios do forcado (adotado x candidato) e coincidencia das areas criticas
ma, _ = le(os.path.join(DI, "SY_medio_eventos_forcado_sd.tif")); mn, _ = le(os.path.join(DI, "SY_medio_eventos_forcado_l05w.tif"))
qa, qn = np.nanpercentile(ma[valido], 95), np.nanpercentile(mn[valido], 95)
cat = np.full(ma.shape, np.nan); cat[valido] = 0
cat[valido & (ma >= qa) & (mn >= qn)] = 3; cat[valido & (ma >= qa) & (mn < qn)] = 1; cat[valido & (ma < qa) & (mn >= qn)] = 2
lin, col = np.where(valido); r0, r1, c0, c1 = lin.min(), lin.max() + 1, col.min(), col.max() + 1
fig, axs = plt.subplots(1, 3, figsize=(16, 4.6))
vmax = np.nanpercentile(np.concatenate([ma[valido], mn[valido]]) * 1000, 99)
for a_, m_, tit in ((axs[0], ma, "Forçado, adotado hoje (λ 0,20)"), (axs[1], mn, "Forçado, candidato (λ 0,05, S convertido)")):
    im = a_.imshow((m_ * 1000)[r0:r1, c0:c1], cmap="Oranges", vmin=0, vmax=vmax); a_.set_title(tit, fontsize=10, color=TXT, loc="left"); a_.axis("off")
cb = fig.colorbar(im, ax=axs[:2], fraction=0.025, pad=0.01); cb.set_label("sedimento médio por evento (kg/pixel)", fontsize=8.5, color=TXT2)
axs[2].imshow(cat[r0:r1, c0:c1], cmap=ListedColormap(["#ecebe6", AZUL, LARANJA, "#b10026"]), vmin=-0.5, vmax=3.5, interpolation="nearest"); axs[2].axis("off")
pc = 100 * np.sum(cat == 3) / np.sum(cat >= 2)
axs[2].set_title(f"Áreas críticas (5% superiores): {pc:.0f}% coincidem", fontsize=10, color=TXT, loc="left")
axs[2].legend(handles=[mpatches.Patch(color="#b10026", label="crítica nos dois"), mpatches.Patch(color=AZUL, label="só no adotado"),
                       mpatches.Patch(color=LARANJA, label="só no candidato")], loc="lower right", fontsize=8, frameon=False)
fig.suptitle("O mapa: trocar a configuração quase não muda onde estão as áreas críticas", fontsize=11.5, color=TXT, x=0.01, ha="left")
fig.savefig(os.path.join(OUT, "E_mapas_forcado_adotado_x_candidato.png"), dpi=150, bbox_inches="tight"); plt.close(fig)
print("figuras em", OUT, sorted(os.listdir(OUT)))
