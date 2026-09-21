"""
DIAGNOSTICO parte 2 (nao e resultado final).

a) O erro do volume (CN-SCS) e sistematico em relacao a alguma variavel do
   evento? Se for, da pra corrigi-lo -> e ai o ganho vai direto pro SY
   (parte 1 mostrou: volume perfeito leva o NSE de 0,37 para 0,80).
b) Metricas honestas (leave-one-out) para cada alternativa em disputa,
   incluindo o experimento de alfa/beta livres (secao 10 das notas).
c) O lambda otimo por evento e previsivel a partir de variaveis do evento?
   (abordagem Baert et al. 2026 - se for, melhora o volume)
"""

import os
import numpy as np
import pandas as pd
from osgeo import gdal

gdal.UseExceptions()

BASE = r"C:\TCC"
PASTA_DADOS = os.path.join(BASE, "Dados Iniciais")

df_ev = pd.read_excel(os.path.join(PASTA_DADOS, "eventos_processados_manuais.xlsx"),
                      sheet_name="Sheet1")


def ev_index(n):
    return 0 if n == 1 else n


def col_ev(nome):
    return np.array([df_ev.iloc[ev_index(n)][nome] for n in range(1, 18)], dtype=float)


SY_obs = col_ev("SYY_t")
den_nse = np.sum((SY_obs - SY_obs.mean()) ** 2)


def nse(sim):
    return 1 - np.sum((SY_obs - sim) ** 2) / den_nse


vol = pd.read_csv(os.path.join(PASTA_DADOS, "comparacao_volumes_medido_vs_calculado.csv"))
vol = vol.sort_values("evento")
V_med = vol["T_R_m3_medido"].to_numpy(dtype=float)
V_calc = vol["Vol_CN1_calc"].to_numpy(dtype=float)
erro_vol = 100 * (V_calc - V_med) / V_med

print("=" * 78)
print("a) O erro do volume CN-SCS e sistematico em relacao a alguma variavel?")
print("=" * 78)
candidatas = ["Chuva_evento_mm", "Intensidade_60min_mm/h", "Duracao_horas",
              "Ap5_pond_mm", "Ap10_pond_mm", "Ap14_pond_mm", "Qb_inicio", "IEI"]
print(f"{'variavel':<26} {'r(erro_vol)':>12} {'r(log ratio)':>14}")
log_ratio = np.log(V_calc / V_med)
for c in candidatas:
    if c not in df_ev.columns:
        continue
    v = col_ev(c)
    if np.isnan(v).any():
        continue
    print(f"{c:<26} {np.corrcoef(v, erro_vol)[0,1]:>12.3f} "
          f"{np.corrcoef(v, log_ratio)[0,1]:>14.3f}")

# ------------------------------------------------------------
print()
print("=" * 78)
print("b) Metricas honestas: leave-one-out de cada alternativa")
print("=" * 78)

Eunit_soma = np.empty(17)
for n in range(1, 18):
    ds = gdal.Open(os.path.join(BASE, f"Evento {n}", f"E_unit{n}.tif"))
    band = ds.GetRasterBand(1)
    nodata = band.GetNoDataValue()
    arr = band.ReadAsArray().astype(np.float64)
    Eunit_soma[n - 1] = np.nansum(np.where((arr != nodata) & np.isfinite(arr), arr, np.nan))
    ds = None


def loo_escala(x):
    """Leave-one-out de SY = c*x (1 parametro)."""
    sim = np.empty(17)
    for i in range(17):
        m = np.ones(17, dtype=bool)
        m[i] = False
        ci = np.sum(x[m] * SY_obs[m]) / np.sum(x[m] ** 2)
        sim[i] = ci * x[i]
    return sim


def metricas(sim, rotulo):
    erro = 100 * (sim - SY_obs) / SY_obs
    print(f"{rotulo:<46} NSE={nse(sim):>7.4f} | erro medio={erro.mean():>+6.1f}% | "
          f"abs={np.abs(erro).mean():>5.1f}%")


# baseline adotado
c0 = np.sum(Eunit_soma * SY_obs) / np.sum(Eunit_soma ** 2)
metricas(c0 * Eunit_soma, "baseline SY=c*E_unit (in-sample)")
metricas(loo_escala(Eunit_soma), "baseline SY=c*E_unit (leave-one-out)")

# volume perfeito
f = V_med / V_calc
Eunit_corr = Eunit_soma * f ** 1.12
c1 = np.sum(Eunit_corr * SY_obs) / np.sum(Eunit_corr ** 2)
metricas(c1 * Eunit_corr, "volume medido + SY=c*E_unit (in-sample)")
metricas(loo_escala(Eunit_corr), "volume medido + SY=c*E_unit (leave-one-out)")

# alfa/beta livres (secao 10): SY = alfa*(...)^beta -> em nivel agregado,
# equivale a reescalar o termo de energia por pixel. Reproduz aproximando
# pelo efeito agregado: E_unit ~ (energia)^0.56, entao (energia)^beta =
# E_unit^(beta/0.56) a menos de constantes por pixel. Usamos a aproximacao
# agregada so para comparar estabilidade (o valor exato esta na secao 10).
for beta in (0.2793, 0.4, 0.56, 0.7):
    x = Eunit_soma ** (beta / 0.56)
    sim_in = (np.sum(x * SY_obs) / np.sum(x ** 2)) * x
    print()
    metricas(sim_in, f"expoente beta={beta:.4f} (in-sample, aprox. agregada)")
    metricas(loo_escala(x), f"expoente beta={beta:.4f} (leave-one-out)")

# ------------------------------------------------------------
print()
print("=" * 78)
print("c) O lambda otimo por evento e previsivel? (se for, melhora o volume)")
print("=" * 78)
cam_lam = os.path.join(PASTA_DADOS, "lambda_otimo_por_evento.csv")
if os.path.exists(cam_lam):
    lam = pd.read_csv(cam_lam)
    print("colunas:", list(lam.columns))
    col_l = [c for c in lam.columns if "lambda" in c.lower()]
    if col_l:
        lv = lam[col_l[0]].to_numpy(dtype=float)
        print(f"lambda otimo: min={np.nanmin(lv):.4f} max={np.nanmax(lv):.4f} "
              f"mediana={np.nanmedian(lv):.4f}")
        ok = np.isfinite(lv)
        print(f"\n{'variavel':<26} {'r(lambda)':>10}")
        for c in candidatas:
            if c not in df_ev.columns:
                continue
            v = col_ev(c)[: len(lv)]
            m = ok & np.isfinite(v)
            if m.sum() > 3:
                print(f"{c:<26} {np.corrcoef(v[m], lv[m])[0,1]:>10.3f}")
else:
    print("arquivo de lambda otimo nao encontrado")
