"""
DIAGNOSTICO parte 4: escolher o cenario de umidade antecedente (AMC I/II/III)
por evento, em vez de fixar CN-1 para todos.

Motivacao (parte 3): em 5 dos 17 eventos NENHUM lambda reproduz o volume
medido - mesmo com lambda->0 o CN-1 gera escoamento de menos. Isso nao e
problema de lambda, e do proprio CN (S alto demais). A correcao fisica
padrao para isso e classificar a umidade antecedente do solo (AMC) por
evento a partir da chuva dos 5 dias anteriores (P5), em vez de assumir
AMC-I para todos.

Limiares classicos do SCS (estacao de crescimento, que e o caso: eventos
de nov-dez no Sudeste):
    AMC I  : P5 < 35,6 mm
    AMC II : 35,6 <= P5 <= 53,3 mm
    AMC III: P5 > 53,3 mm
"""

import os
import numpy as np
import pandas as pd

BASE = r"C:\TCC"
PASTA_DADOS = os.path.join(BASE, "Dados Iniciais")

df_ev = pd.read_excel(os.path.join(PASTA_DADOS, "eventos_processados_manuais.xlsx"),
                      sheet_name="Sheet1")


def ev_index(n):
    return 0 if n == 1 else n


def col_ev(nome):
    return np.array([df_ev.iloc[ev_index(n)][nome] for n in range(1, 18)], dtype=float)


vol = pd.read_csv(os.path.join(PASTA_DADOS,
                               "comparacao_volumes_medido_vs_calculado.csv")).sort_values("evento")
V_med = vol["T_R_m3_medido"].to_numpy(dtype=float)
V = {1: vol["Vol_CN1_calc"].to_numpy(dtype=float),
     2: vol["Vol_CN2_calc"].to_numpy(dtype=float),
     3: vol["Vol_CN3_calc"].to_numpy(dtype=float)}

P5 = col_ev("Ap5_pond_mm")
SY_obs = col_ev("SYY_t")
den_v = np.sum((V_med - V_med.mean()) ** 2)
den_sy = np.sum((SY_obs - SY_obs.mean()) ** 2)


def classifica(p5):
    if p5 < 35.6:
        return 1
    if p5 <= 53.3:
        return 2
    return 3


amc = np.array([classifica(p) for p in P5])
melhor = np.array([min((abs(V[c][i] - V_med[i]), c) for c in (1, 2, 3))[1] for i in range(17)])

print(f"{'ev':>3} {'P5(mm)':>8} {'AMC(P5)':>8} {'melhor':>7} {'err CN1':>9} "
      f"{'err CN2':>9} {'err CN3':>9}")
for i in range(17):
    e = [100 * (V[c][i] - V_med[i]) / V_med[i] for c in (1, 2, 3)]
    print(f"{i+1:>3} {P5[i]:>8.1f} {amc[i]:>8} {melhor[i]:>7} "
          f"{e[0]:>8.1f}% {e[1]:>8.1f}% {e[2]:>8.1f}%")

print(f"\nconcordancia AMC(P5) x melhor cenario: {(amc == melhor).sum()}/17")


def avalia_vol(sel, rotulo):
    v = np.array([V[sel[i]][i] for i in range(17)])
    err = 100 * (v - V_med) / V_med
    nse = 1 - np.sum((V_med - v) ** 2) / den_v
    print(f"{rotulo:<40} NSE_vol={nse:>7.4f} | medio={err.mean():>+7.1f}% | "
          f"abs={np.abs(err).mean():>5.1f}%")
    return v


print()
v_cn1 = avalia_vol(np.ones(17, dtype=int), "CN-1 para todos (atual)")
v_amc = avalia_vol(amc, "AMC classificado por P5 (fisico)")
v_best = avalia_vol(melhor, "melhor cenario por evento (ORACULO)")

# propagacao para o SY: soma(E_unit) ~ volume^1.12 (aprox. de escala)
print("\n--- propagacao aproximada para o SY (E_unit ~ Q^1,12) ---")
ds = pd.read_csv(os.path.join(PASTA_DADOS, "comparacao_volumes_medido_vs_calculado.csv"))
Eunit_ref = None
try:
    from osgeo import gdal
    gdal.UseExceptions()
    Eunit_ref = np.empty(17)
    for n in range(1, 18):
        d = gdal.Open(os.path.join(BASE, f"Evento {n}", f"E_unit{n}.tif"))
        b = d.GetRasterBand(1)
        nd = b.GetNoDataValue()
        a = b.ReadAsArray().astype(np.float64)
        Eunit_ref[n - 1] = np.nansum(np.where((a != nd) & np.isfinite(a), a, np.nan))
        d = None
except Exception as exc:
    print("nao foi possivel ler E_unit:", exc)

if Eunit_ref is not None:
    def sy_loo(x, rotulo):
        sim = np.empty(17)
        for i in range(17):
            m = np.ones(17, dtype=bool)
            m[i] = False
            ci = np.sum(x[m] * SY_obs[m]) / np.sum(x[m] ** 2)
            sim[i] = ci * x[i]
        err = 100 * (sim - SY_obs) / SY_obs
        nse = 1 - np.sum((SY_obs - sim) ** 2) / den_sy
        print(f"{rotulo:<40} NSE_SY={nse:>7.4f} | medio={err.mean():>+7.1f}% | "
              f"abs={np.abs(err).mean():>5.1f}%")

    sy_loo(Eunit_ref, "CN-1 (atual)")
    sy_loo(Eunit_ref * (v_amc / v_cn1) ** 1.12, "AMC por P5")
    sy_loo(Eunit_ref * (v_best / v_cn1) ** 1.12, "oraculo de cenario")
    sy_loo(Eunit_ref * (V_med / v_cn1) ** 1.12, "volume medido (restricao observada)")
