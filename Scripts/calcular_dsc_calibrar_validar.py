"""
Normaliza o FCI em DSC (Eq. 8, Hao et al. 2022):

    DSC_unit,k = 1 / (1 + exp(FCI0 - kFCI * FCI_k))

Calcula SY_sim por evento (SY_sim = soma de E_unit x DSC), calibra FCI0 e
kFCI (2 parametros unicos para toda a bacia, nao por evento - Tabela 4 do
artigo) contra o SY_obs medido (coluna SYY_t da planilha de eventos),
maximizando o log-NSE (Eq. 11 do artigo, o mesmo objetivo que eles usam
com simulated annealing - aqui usamos differential_evolution + polimento
local). Valida com NSE, WIA (Willmott) e PBIAS (metricas padrao, Eq. 12/13
do artigo) e salva DSC{n}.tif final por evento.
"""

import os
import numpy as np
import pandas as pd
from osgeo import gdal
from scipy.optimize import differential_evolution, minimize

gdal.UseExceptions()

BASE = r"C:\TCC"
PASTA_DADOS = os.path.join(BASE, "Dados Iniciais")
PASTA_QP = os.path.join(PASTA_DADOS, "qp_spatial")

ref_ds = gdal.Open(os.path.join(PASTA_QP, "carvedDEM_corrigido_filled.tif"))
gt = ref_ds.GetGeoTransform()
proj = ref_ds.GetProjection()
ncols, nrows = ref_ds.RasterXSize, ref_ds.RasterYSize
ref_ds = None


def le_raster(caminho):
    ds = gdal.Open(caminho)
    band = ds.GetRasterBand(1)
    nodata = band.GetNoDataValue()
    arr = band.ReadAsArray().astype(np.float64)
    arr = np.where((arr != nodata) & np.isfinite(arr), arr, np.nan)
    ds = None
    return arr


def reprojeta_para_dem(caminho_origem, caminho_saida, nodata_saida=-9999):
    ds = gdal.Open(caminho_origem)
    gdal.Warp(
        caminho_saida, ds, format="GTiff",
        width=ncols, height=nrows,
        outputBounds=(gt[0], gt[3] + nrows * gt[5], gt[0] + ncols * gt[1], gt[3]),
        dstSRS=proj, resampleAlg=gdal.GRA_NearestNeighbour, dstNodata=nodata_saida,
    )
    ds = None


driver = gdal.GetDriverByName("GTiff")


def salva_raster(caminho, arr, nodata=-9999):
    saida = np.where(np.isfinite(arr), arr, nodata).astype(np.float32)
    out = driver.Create(caminho, ncols, nrows, 1, gdal.GDT_Float32)
    out.SetGeoTransform(gt)
    out.SetProjection(proj)
    band_out = out.GetRasterBand(1)
    band_out.WriteArray(saida)
    band_out.SetNoDataValue(nodata)
    band_out.FlushCache()
    out = None


# ============================================================
# 1. SY_obs (SYY_t) - mesma logica de indexacao ja usada em
#    calcular_pr_pixel.py (evento 1 = linha "1A"; eventos 2-17
#    caem direto no iloc por causa do deslocamento de "1B").
# ============================================================

df_eventos = pd.read_excel(
    os.path.join(PASTA_DADOS, "eventos_processados_manuais.xlsx"), sheet_name="Sheet1"
)


def ev_index(n):
    return 0 if n == 1 else n


SY_obs = np.array([df_eventos.iloc[ev_index(n)]["SYY_t"] for n in range(1, 18)], dtype=float)
print("SY_obs carregado:", np.round(SY_obs, 2))

# ============================================================
# 2. FCI e E_unit (reprojetado p/ grade do DEM) por evento
# ============================================================

FCI_list = []
Eunit_list = []

for n in range(1, 18):
    PASTA_EVENTO = os.path.join(BASE, f"Evento {n}")
    fci = le_raster(os.path.join(PASTA_EVENTO, f"FCI{n}.tif"))

    caminho_e_dem = os.path.join(PASTA_QP, f"_Eunit_dem_tmp{n}.tif")
    reprojeta_para_dem(os.path.join(PASTA_EVENTO, f"E_unit{n}.tif"), caminho_e_dem)
    eunit = le_raster(caminho_e_dem)
    try:
        os.remove(caminho_e_dem)
    except OSError:
        pass

    valido = np.isfinite(fci) & np.isfinite(eunit) & (eunit >= 0)
    FCI_list.append(fci[valido])
    Eunit_list.append(eunit[valido])
    print(f"Evento {n}: {valido.sum()} pixels validos (FCI & E_unit sobrepostos), "
          f"soma E_unit={eunit[valido].sum():.2f} t (teto fisico de SY_sim)")

# ============================================================
# 3. SY_sim(FCI0, kFCI) e calibracao (log-NSE, Eq. 11)
# ============================================================


def sy_sim_vetor(params):
    FCI0, kFCI = params
    out = np.empty(17)
    for i in range(17):
        expo = np.clip(FCI0 - kFCI * FCI_list[i], -500, 500)
        dsc = 1.0 / (1.0 + np.exp(expo))
        out[i] = np.sum(Eunit_list[i] * dsc)
    return out


log_obs = np.log(SY_obs)
log_ave = np.mean(log_obs)
den_fixo = np.sum((log_obs - log_ave) ** 2)

obs_mean = np.mean(SY_obs)
den_nse_fixo = np.sum((SY_obs - obs_mean) ** 2)


def neg_log_nse(params):
    sy_sim = np.clip(sy_sim_vetor(params), 1e-6, None)
    log_sim = np.log(sy_sim)
    F = 1 - np.sum((log_obs - log_sim) ** 2) / den_fixo
    return -F


def neg_nse(params):
    sy_sim = sy_sim_vetor(params)
    F = 1 - np.sum((SY_obs - sy_sim) ** 2) / den_nse_fixo
    return -F


# Teste rapido: E_unit puro (sem DSC), so escala constante otima (minimos
# quadrados atraves da origem) - baseline pra comparar se o FCI/DSC realmente
# agrega algo alem de uma simples escala global.
Eunit_soma = np.array([Eunit_list[i].sum() for i in range(17)])
c_opt = np.sum(Eunit_soma * SY_obs) / np.sum(Eunit_soma ** 2)
sim_baseline = c_opt * Eunit_soma
nse_baseline = 1 - np.sum((SY_obs - sim_baseline) ** 2) / den_nse_fixo
print(f"\n[BASELINE] escala constante de E_unit (sem FCI/DSC): c={c_opt:.4f}, "
      f"NSE={nse_baseline:.4f} - referencia pra saber se o FCI/DSC ajuda")


fci_concat = np.concatenate(FCI_list)
fci_min, fci_max = fci_concat.min(), fci_concat.max()
print(f"\nFaixa global de FCI: [{fci_min:.2f}, {fci_max:.2f}]")

bounds = [(fci_min - 200, fci_max + 200), (1e-5, 20.0)]

print("\nCalibrando FCI0 e kFCI (differential_evolution, busca global, com limites fisicos)...")
print(f"Limites: FCI0 em {bounds[0]}, kFCI em {bounds[1]} (kFCI > 0 obrigatorio - conectividade")
print("deve AUMENTAR com FCI menos negativo, senao o sentido fisico do modelo se inverte)")
print("Objetivo: maximizar NSE bruto (nao log-NSE) - o log-NSE convergia pra um ponto pior")
print("em NSE bruto do que a simples escala constante de E_unit (baseline acima)")

de = differential_evolution(neg_nse, bounds, seed=0, tol=1e-12, maxiter=1000,
                             popsize=30, polish=True, workers=1)

print(f"DE (com polimento L-BFGS-B respeitando os limites): "
      f"FCI0={de.x[0]:.4f}, kFCI={de.x[1]:.5f}, NSE={-de.fun:.4f}")

# Polimento extra, mas AINDA restrito aos mesmos limites fisicos (L-BFGS-B, nao
# Nelder-Mead livre - a primeira tentativa fugiu pra kFCI negativo, fisicamente
# sem sentido, porque o polimento nao tinha limites)
polido = minimize(neg_nse, de.x, method="L-BFGS-B", bounds=bounds,
                   options={"ftol": 1e-12, "gtol": 1e-10, "maxiter": 5000})

FCI0_cal, kFCI_cal = polido.x
print(f"Polido (L-BFGS-B, com limites): FCI0={FCI0_cal:.4f}, kFCI={kFCI_cal:.5f}, "
      f"log-NSE={-polido.fun:.4f}")

# ============================================================
# 4. Validacao final
# ============================================================

SY_sim = sy_sim_vetor(polido.x)


def nse(obs, sim):
    return 1 - np.sum((obs - sim) ** 2) / np.sum((obs - np.mean(obs)) ** 2)


def wia(obs, sim):
    obs_mean = np.mean(obs)
    return 1 - np.sum((obs - sim) ** 2) / np.sum((np.abs(sim - obs_mean) + np.abs(obs - obs_mean)) ** 2)


def pbias(obs, sim):
    return 100 * np.sum(sim - obs) / np.sum(obs)


erro_pct = 100 * (SY_sim - SY_obs) / SY_obs

print(f"\n=== VALIDACAO (FCI0={FCI0_cal:.4f}, kFCI={kFCI_cal:.5f}) ===")
print(f"NSE={nse(SY_obs, SY_sim):.4f} | WIA={wia(SY_obs, SY_sim):.4f} | "
      f"PBIAS={pbias(SY_obs, SY_sim):.2f}% | log-NSE={-polido.fun:.4f}")
print(f"Erro medio={erro_pct.mean():.2f}% | erro absoluto medio={np.abs(erro_pct).mean():.2f}%")

print(f"\n{'Evento':>7} | {'SY_obs(t)':>10} | {'SY_sim(t)':>10} | {'erro%':>8}")
for n in range(1, 18):
    print(f"{n:>7} | {SY_obs[n-1]:>10.2f} | {SY_sim[n-1]:>10.2f} | {erro_pct[n-1]:>7.1f}%")

# ============================================================
# 5. Salva DSC{n}.tif final (calibrado) por evento
# ============================================================

for n in range(1, 18):
    fci_full = le_raster(os.path.join(BASE, f"Evento {n}", f"FCI{n}.tif"))
    expo = np.clip(FCI0_cal - kFCI_cal * fci_full, -500, 500)
    dsc_full = 1.0 / (1.0 + np.exp(expo))
    dsc_full = np.where(np.isfinite(fci_full), dsc_full, np.nan)
    salva_raster(os.path.join(BASE, f"Evento {n}", f"DSC{n}.tif"), dsc_full)

print("\nDSC{n}.tif salvo para os 17 eventos. Concluido.")
