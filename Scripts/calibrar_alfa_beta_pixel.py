"""
Experimento (17/09/2026): testar se recalibrar alfa e beta diretamente na
formula por pixel (em vez dos valores fixos de Williams 1975/Hao et al.,
11,8 e 0,56) melhora o ajuste contra SY_obs.

    E_unit_k(alfa, beta) = alfa * (Q_k * pr_k * Area_unit)^beta * K_k * C_k * P_k * LS_k
    SY_sim = soma_k E_unit_k(alfa, beta)

Ressalva metodologica (ver conversa): com apenas 17 observacoes de nivel
bacia para identificar 2 parametros que atuam numa soma nao-linear de
~145 mil pixels, o ajuste e mal-condicionado e sujeito a overfitting -
os parametros de Williams (1975) sao validados em parcelas experimentais
de campo (escala de pixel), nao recalibraveis so com dado agregado de
saida de bacia. Este script existe para comparar objetivamente o
resultado, nao para substituir a abordagem adotada (baseline com alfa/beta
fixos e escala c calibrada - ver calcular_sy_final.py).
"""

import os
import numpy as np
import pandas as pd
from osgeo import gdal
from scipy.optimize import differential_evolution, minimize

gdal.UseExceptions()

BASE = r"C:\TCC"
PASTA_DADOS = os.path.join(BASE, "Dados Iniciais")
P_CONST = 1.0


def carrega(caminho):
    ds = gdal.Open(caminho)
    band = ds.GetRasterBand(1)
    nodata = band.GetNoDataValue()
    arr = band.ReadAsArray().astype(np.float64)
    return np.where((arr != nodata) & np.isfinite(arr), arr, np.nan)


K = carrega(os.path.join(PASTA_DADOS, "K_raster.tif"))
LS = carrega(os.path.join(PASTA_DADOS, "LS_raster.tif"))
C = carrega(os.path.join(PASTA_DADOS, "C_raster.tif"))

ds_ref = gdal.Open(os.path.join(PASTA_DADOS, "K_raster.tif"))
gt = ds_ref.GetGeoTransform()
area_pixel_m2 = abs(gt[1]) * abs(gt[5])

# ============================================================
# 1. SY_obs (mesma indexacao ja usada nos outros scripts)
# ============================================================

df_eventos = pd.read_excel(
    os.path.join(PASTA_DADOS, "eventos_processados_manuais.xlsx"), sheet_name="Sheet1"
)


def ev_index(n):
    return 0 if n == 1 else n


SY_obs = np.array([df_eventos.iloc[ev_index(n)]["SYY_t"] for n in range(1, 18)], dtype=float)

# ============================================================
# 2. Pre-carrega base (Q*pr*Area, K*C*P*LS) por evento - fixo,
#    nao depende de alfa/beta, calculado uma unica vez
# ============================================================

base_qpr_list = []
fatores_list = []

for n in range(1, 18):
    PASTA_EVENTO = os.path.join(BASE, f"Evento {n}")
    Q = carrega(os.path.join(PASTA_EVENTO, f"Q{n}_CN1.tif"))
    pr = carrega(os.path.join(PASTA_EVENTO, f"pr{n}.tif"))

    valido = np.isfinite(Q) & np.isfinite(pr) & np.isfinite(K) & np.isfinite(LS) & np.isfinite(C)
    base_qpr = np.clip(Q[valido] * pr[valido] * area_pixel_m2, 0, None)
    fatores = K[valido] * C[valido] * P_CONST * LS[valido]

    base_qpr_list.append(base_qpr)
    fatores_list.append(fatores)
    print(f"Evento {n}: {valido.sum()} pixels validos")

# ============================================================
# 3. Calibra alfa e beta (differential_evolution, maximizando NSE bruto,
#    mesmo objetivo usado na calibracao FCI0/kFCI para comparacao justa)
# ============================================================


def sy_sim_vetor(params):
    alfa, beta = params
    out = np.empty(17)
    for i in range(17):
        out[i] = alfa * np.sum((base_qpr_list[i] ** beta) * fatores_list[i])
    return out


obs_mean = np.mean(SY_obs)
den_nse_fixo = np.sum((SY_obs - obs_mean) ** 2)


def neg_nse(params):
    sy_sim = sy_sim_vetor(params)
    F = 1 - np.sum((SY_obs - sy_sim) ** 2) / den_nse_fixo
    return -F


# limites: beta entre 0,1 e 2 (faixa fisicamente razoavel para uma relacao
# potencia erosao~escoamento; 0,56 de Williams e 0,807 da IC caem dentro
# dessa faixa); alfa positivo, com range amplo o suficiente pra nao
# artificialmente restringir a escala
bounds = [(1e-6, 1000.0), (0.1, 2.0)]

print("\nCalibrando alfa e beta livremente (differential_evolution)...")
de = differential_evolution(neg_nse, bounds, seed=0, tol=1e-12, maxiter=1000,
                             popsize=30, polish=True, workers=1)
print(f"DE: alfa={de.x[0]:.6f}, beta={de.x[1]:.6f}, NSE={-de.fun:.4f}")

polido = minimize(neg_nse, de.x, method="L-BFGS-B", bounds=bounds,
                   options={"ftol": 1e-14, "gtol": 1e-12, "maxiter": 5000})
alfa_cal, beta_cal = polido.x
print(f"Polido: alfa={alfa_cal:.6f}, beta={beta_cal:.6f}, NSE={-polido.fun:.4f}")

# ============================================================
# 4. Validacao
# ============================================================

SY_sim = sy_sim_vetor(polido.x)


def nse(obs, sim):
    return 1 - np.sum((obs - sim) ** 2) / np.sum((obs - np.mean(obs)) ** 2)


def wia(obs, sim):
    om = np.mean(obs)
    return 1 - np.sum((obs - sim) ** 2) / np.sum((np.abs(sim - om) + np.abs(obs - om)) ** 2)


def pbias(obs, sim):
    return 100 * np.sum(sim - obs) / np.sum(obs)


erro_pct = 100 * (SY_sim - SY_obs) / SY_obs

print(f"\n=== RESULTADO (alfa={alfa_cal:.6f}, beta={beta_cal:.6f}) ===")
print(f"Comparacao: Williams/Hao fixos = alfa=11,8 beta=0,56 | IC (escala diferente) = alfa=0,277 beta=0,807")
print(f"NSE={nse(SY_obs, SY_sim):.4f} | WIA={wia(SY_obs, SY_sim):.4f} | PBIAS={pbias(SY_obs, SY_sim):.2f}%")
print(f"Erro medio={erro_pct.mean():.2f}% | erro absoluto medio={np.abs(erro_pct).mean():.2f}%")

print(f"\n{'Evento':>7} | {'SY_obs(t)':>10} | {'SY_sim(t)':>10} | {'erro%':>8}")
for n in range(1, 18):
    print(f"{n:>7} | {SY_obs[n-1]:>10.2f} | {SY_sim[n-1]:>10.2f} | {erro_pct[n-1]:>7.1f}%")

print("\n=== COMPARACAO COM O BASELINE ADOTADO (alfa/beta fixos, so escala c) ===")
print("Baseline (calcular_sy_final.py): NSE=0,3714 | erro medio=-19,2% | erro absoluto medio=44,4%")
print(f"Este experimento (alfa/beta livres): NSE={nse(SY_obs, SY_sim):.4f} | "
      f"erro medio={erro_pct.mean():.2f}% | erro absoluto medio={np.abs(erro_pct).mean():.2f}%")

print("\nConcluido.")
