"""
DIAGNOSTICO parte 3 (nao e resultado final): quanto do erro de volume e
recuperavel com um lambda que depende do evento?

Motivacao (partes 1 e 2): com o volume MEDIDO, o NSE do SY salta de 0,37
para 0,80. E o erro do volume e sistematico (r=+0,63 com a lamina de chuva
do evento; o lambda otimo por evento tambem cresce com a chuva, r=+0,57).
Logo, um lambda que dependa da chuva do evento - exatamente a abordagem de
Baert et al. (2026) e a discussao de Brandao et al. (2025), os artigos que
o orientador indicou - pode recuperar parte desses 0,43 de NSE.

Usa um SUBSTITUTO EXATO do pipeline, sem reprocessar raster:
    soma(E_unit) = 11,8 * [A^2*(RI/R)/3,6e6]^0,56 * soma_k(Q_k^1,12 * K*C*LS)
(vem de E_unit = 11,8*(Q*pr*A)^0,56*K*C*LS*P com pr = (Q/1000)*A*(RI/R)/3600)

Tudo avaliado com leave-one-out (17 eventos e pouca amostra - o ajuste
in-sample e otimista).
"""

import os
import numpy as np
import pandas as pd
from osgeo import gdal
from scipy.optimize import brentq

gdal.UseExceptions()

BASE = r"C:\TCC"
PASTA_DADOS = os.path.join(BASE, "Dados Iniciais")


def le(caminho):
    ds = gdal.Open(caminho)
    b = ds.GetRasterBand(1)
    nd = b.GetNoDataValue()
    a = b.ReadAsArray().astype(np.float64)
    a = np.where((a != nd) & np.isfinite(a), a, np.nan)
    gt = ds.GetGeoTransform()
    ds = None
    return a, gt


# Grade de referencia = a do E_unit/ChuvaIDW (K, C, LS ja estao nela).
# O raster S esta numa grade diferente, precisa ser realinhado.
REF = os.path.join(BASE, "Evento 1", "ChuvaIDW1.tif")
ref_ds = gdal.Open(REF)
gt_ref = ref_ds.GetGeoTransform()
proj_ref = ref_ds.GetProjection()
NC, NR = ref_ds.RasterXSize, ref_ds.RasterYSize
ref_ds = None
AREA = abs(gt_ref[1]) * abs(gt_ref[5])

caminho_s_alinhado = os.path.join(PASTA_DADOS, "_S_seco_alinhado_tmp.tif")
gdal.Warp(caminho_s_alinhado, os.path.join(PASTA_DADOS, "S - Seco.tif"),
          format="GTiff", width=NC, height=NR,
          outputBounds=(gt_ref[0], gt_ref[3] + NR * gt_ref[5],
                        gt_ref[0] + NC * gt_ref[1], gt_ref[3]),
          dstSRS=proj_ref, resampleAlg=gdal.GRA_Bilinear, dstNodata=-9999)

S, gt_s = le(caminho_s_alinhado)
K, _ = le(os.path.join(PASTA_DADOS, "K_raster.tif"))
C, _ = le(os.path.join(PASTA_DADOS, "C_raster.tif"))
LS, _ = le(os.path.join(PASTA_DADOS, "LS_raster.tif"))
print(f"grades: S={S.shape} K={K.shape} C={C.shape} LS={LS.shape} area_pixel={AREA:.2f} m2")

W_ESP = K * C * LS  # peso espacial fixo (P=1)

df_ev = pd.read_excel(os.path.join(PASTA_DADOS, "eventos_processados_manuais.xlsx"),
                      sheet_name="Sheet1")


def ev_index(n):
    return 0 if n == 1 else n


def col_ev(nome):
    return np.array([df_ev.iloc[ev_index(n)][nome] for n in range(1, 18)], dtype=float)


SY_obs = col_ev("SYY_t")
RI = col_ev("Intensidade_60min_mm/h")
R_ev = col_ev("Chuva_evento_mm")
den_nse = np.sum((SY_obs - SY_obs.mean()) ** 2)

vol = pd.read_csv(os.path.join(PASTA_DADOS,
                               "comparacao_volumes_medido_vs_calculado.csv")).sort_values("evento")
V_med = vol["T_R_m3_medido"].to_numpy(dtype=float)
V_calc_ref = vol["Vol_CN1_calc"].to_numpy(dtype=float)

P_rasters = []
for n in range(1, 18):
    p, _ = le(os.path.join(BASE, f"Evento {n}", f"ChuvaIDW{n}.tif"))
    P_rasters.append(p)

VALIDO = np.isfinite(S) & np.isfinite(W_ESP) & np.isfinite(P_rasters[0])
print(f"pixels validos: {VALIDO.sum()}")

S_v = S[VALIDO]
W_v = W_ESP[VALIDO]
P_v = [p[VALIDO] for p in P_rasters]


def q_pixel(i, lam):
    P = P_v[i]
    ia = lam * S_v
    q = np.where(P > ia, (P - ia) ** 2 / (P + (1 - lam) * S_v), 0.0)
    return q


def volume_m3(i, lam):
    return np.sum(q_pixel(i, lam)) / 1000.0 * AREA


def energia(i, lam):
    """soma_k(Q^1.12 * K*C*LS) - parte espacial de soma(E_unit)."""
    return np.sum(q_pixel(i, lam) ** 1.12 * W_v)


CONST = 11.8 * (AREA ** 2 / 3.6e6) ** 0.56


def soma_eunit(i, lam):
    return CONST * (RI[i] / R_ev[i]) ** 0.56 * energia(i, lam)


# ------------------------------------------------------------
print("\n" + "=" * 78)
print("0. VALIDACAO do substituto (lambda=0,05, o atual) contra os valores conhecidos")
print("=" * 78)
v05 = np.array([volume_m3(i, 0.05) for i in range(17)])
e05 = np.array([soma_eunit(i, 0.05) for i in range(17)])
print(f"volume: erro relativo medio vs CSV da Fase 1 = "
      f"{100*np.mean(np.abs(v05-V_calc_ref)/V_calc_ref):.2f}%")
print(f"soma E_unit evento 1={e05[0]:.1f} t (esperado ~836), "
      f"evento 15={e05[14]:.1f} t (esperado ~39818)")


def metricas(sim, rotulo):
    nse = 1 - np.sum((SY_obs - sim) ** 2) / den_nse
    erro = 100 * (sim - SY_obs) / SY_obs
    print(f"{rotulo:<52} NSE={nse:>7.4f} | medio={erro.mean():>+6.1f}% | "
          f"abs={np.abs(erro).mean():>5.1f}%")
    return nse


def escala_loo(x):
    sim = np.empty(17)
    for i in range(17):
        m = np.ones(17, dtype=bool)
        m[i] = False
        ci = np.sum(x[m] * SY_obs[m]) / np.sum(x[m] ** 2)
        sim[i] = ci * x[i]
    return sim


print("\n" + "=" * 78)
print("1. lambda otimo por evento (bate o volume medido exatamente)")
print("=" * 78)
lam_opt = np.empty(17)
for i in range(17):
    f = lambda L: volume_m3(i, L) - V_med[i]
    try:
        lam_opt[i] = brentq(f, 1e-4, 0.95, xtol=1e-6)
    except ValueError:
        lam_opt[i] = np.nan
print("lambda otimo:", np.round(lam_opt, 4))
ok = np.isfinite(lam_opt)
print(f"validos: {ok.sum()}/17 | r(lambda, chuva)={np.corrcoef(R_ev[ok], lam_opt[ok])[0,1]:.3f} | "
      f"r(log-log)={np.corrcoef(np.log(R_ev[ok]), np.log(lam_opt[ok]))[0,1]:.3f}")

print("\n" + "=" * 78)
print("2. lambda(P) = a * chuva^b, com validacao leave-one-out")
print("=" * 78)


def ajusta_lambda_modelo(mask):
    x = np.log(R_ev[mask & ok])
    y = np.log(lam_opt[mask & ok])
    b, loga = np.linalg.lstsq(np.vstack([x, np.ones(len(x))]).T, y, rcond=None)[0]
    return np.exp(loga), b


a_all, b_all = ajusta_lambda_modelo(np.ones(17, dtype=bool))
print(f"ajuste com todos os eventos: lambda = {a_all:.5f} * chuva^{b_all:.3f}")

e_lam_in = np.empty(17)
e_lam_loo = np.empty(17)
v_lam_loo = np.empty(17)
for i in range(17):
    lam_i_in = np.clip(a_all * R_ev[i] ** b_all, 1e-4, 0.95)
    e_lam_in[i] = soma_eunit(i, lam_i_in)
    m = np.ones(17, dtype=bool)
    m[i] = False
    a_i, b_i = ajusta_lambda_modelo(m)
    lam_i = np.clip(a_i * R_ev[i] ** b_i, 1e-4, 0.95)
    e_lam_loo[i] = soma_eunit(i, lam_i)
    v_lam_loo[i] = volume_m3(i, lam_i)

print("\n--- qualidade do VOLUME (o que estamos tentando consertar) ---")
err_v_atual = 100 * (v05 - V_med) / V_med
err_v_novo = 100 * (v_lam_loo - V_med) / V_med
nse_v_atual = 1 - np.sum((V_med - v05) ** 2) / np.sum((V_med - V_med.mean()) ** 2)
nse_v_novo = 1 - np.sum((V_med - v_lam_loo) ** 2) / np.sum((V_med - V_med.mean()) ** 2)
print(f"lambda=0,05 fixo (atual):     NSE_vol={nse_v_atual:>7.4f} | "
      f"medio={err_v_atual.mean():>+6.1f}% | abs={np.abs(err_v_atual).mean():>5.1f}%")
print(f"lambda(chuva), leave-one-out: NSE_vol={nse_v_novo:>7.4f} | "
      f"medio={err_v_novo.mean():>+6.1f}% | abs={np.abs(err_v_novo).mean():>5.1f}%")

print("\n--- propagacao para o SY (SY = c * soma(E_unit), c por minimos quadrados) ---")
c0 = np.sum(e05 * SY_obs) / np.sum(e05 ** 2)
metricas(c0 * e05, "lambda=0,05 fixo (atual, in-sample)")
metricas(escala_loo(e05), "lambda=0,05 fixo (atual, leave-one-out)")
c1 = np.sum(e_lam_in * SY_obs) / np.sum(e_lam_in ** 2)
metricas(c1 * e_lam_in, "lambda(chuva) (in-sample)")
metricas(escala_loo(e_lam_loo), "lambda(chuva) (leave-one-out, honesto)")

e_perf = np.array([soma_eunit(i, lam_opt[i]) if ok[i] else np.nan for i in range(17)])
if np.isfinite(e_perf).all():
    metricas(escala_loo(e_perf), "lambda otimo por evento (TETO, nao realizavel)")
