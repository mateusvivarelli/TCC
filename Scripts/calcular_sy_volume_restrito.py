"""
Versao do pipeline espacializado com o VOLUME DE ESCOAMENTO OBSERVADO usado
como restricao (sufixo "_obs" em todas as saidas).

Motivacao (secao 12 das notas): o diagnostico de 21/09/2026 mostrou que o
erro do SY e quase todo herdado do volume do CN-SCS (erro absoluto 47%), nao
da estrutura espacial nem da MUSLE. Com o volume corrigido para o medido, o
NSE do SY vai de 0,28 para 0,77 (leave-one-out).

O que faz: reescala Q{n}_CN1.tif por um fator unico por evento, de modo que o
volume total da bacia bata exatamente T_R_m3 medido. O PADRAO ESPACIAL do
CN-SCS (que vem do CN e da chuva interpolada) e preservado; so o total e
restringido pela medicao. Depois refaz pr, E_unit e SY com esse Q.

Precedente na literatura: Baert et al. (2026) usam exatamente essa
configuracao (volume e pico observados como entrada da MUSLE) como caso de
referencia. Deve ser descrito no TCC como "volume observado usado como
restricao", NAO como previsao pura - os dois mapas (previsao pura e restrito)
sao apresentados lado a lado, e a diferenca entre eles quantifica a parcela
hidrologica do erro.

Saidas (todas com sufixo _obs, sem sobrescrever os resultados atuais):
    Evento {n}/Q{n}_CN1_obs.tif, pr{n}_obs.tif, E_unit{n}_obs.tif, SY{n}_obs.tif
    Dados Iniciais/SY_medio_eventos_obs.tif
    Dados Iniciais/comparacao_SY_previsao_vs_restrito.csv
"""

import os
import numpy as np
import pandas as pd
from osgeo import gdal

gdal.UseExceptions()

BASE = r"C:\TCC"
PASTA_DADOS = os.path.join(BASE, "Dados Iniciais")
P_CONST = 1.0

df_ev = pd.read_excel(os.path.join(PASTA_DADOS, "eventos_processados_manuais.xlsx"),
                      sheet_name="Sheet1")


def ev_index(n):
    return 0 if n == 1 else n


def le_raster(caminho):
    ds = gdal.Open(caminho)
    band = ds.GetRasterBand(1)
    nodata = band.GetNoDataValue()
    arr = band.ReadAsArray().astype(np.float64)
    arr = np.where((arr != nodata) & np.isfinite(arr), arr, np.nan)
    gt = ds.GetGeoTransform()
    proj = ds.GetProjection()
    ds = None
    return arr, gt, proj


driver = gdal.GetDriverByName("GTiff")


def salva_raster(caminho, arr, gt, proj, nodata=-9999):
    nrows, ncols = arr.shape
    saida = np.where(np.isfinite(arr), arr, nodata).astype(np.float32)
    out = driver.Create(caminho, ncols, nrows, 1, gdal.GDT_Float32)
    out.SetGeoTransform(gt)
    out.SetProjection(proj)
    b = out.GetRasterBand(1)
    b.WriteArray(saida)
    b.SetNoDataValue(nodata)
    b.FlushCache()
    out = None


K, gt_ref, proj_ref = le_raster(os.path.join(PASTA_DADOS, "K_raster.tif"))
C, _, _ = le_raster(os.path.join(PASTA_DADOS, "C_raster.tif"))
LS, _, _ = le_raster(os.path.join(PASTA_DADOS, "LS_raster.tif"))
AREA = abs(gt_ref[1]) * abs(gt_ref[5])
print(f"grade de referencia: {K.shape}, area do pixel = {AREA:.2f} m2")

SY_obs = np.array([df_ev.iloc[ev_index(n)]["SYY_t"] for n in range(1, 18)], dtype=float)

linhas = []
Eunit_obs_soma = np.empty(17)
Eunit_prev_soma = np.empty(17)
Eunit_obs_rasters = []
violacoes_total = 0

print(f"\n{'ev':>3} {'V_calc(m3)':>13} {'V_med(m3)':>13} {'fator':>7} "
      f"{'Q>P (pixels)':>13} {'E_unit prev':>12} {'E_unit obs':>12}")

for n in range(1, 18):
    pasta = os.path.join(BASE, f"Evento {n}")
    row = df_ev.iloc[ev_index(n)]
    RI = float(row["Intensidade_60min_mm/h"])
    R_evento = float(row["Chuva_evento_mm"])
    V_med = float(row["T_R_m3"])

    Q, gt, proj = le_raster(os.path.join(pasta, f"Q{n}_CN1.tif"))
    P_chuva, _, _ = le_raster(os.path.join(pasta, f"ChuvaIDW{n}.tif"))

    valido = np.isfinite(Q) & np.isfinite(K) & np.isfinite(C) & np.isfinite(LS)

    V_calc = np.nansum(np.where(valido, Q, 0.0)) / 1000.0 * AREA
    fator = V_med / V_calc

    Q_obs = np.where(valido, Q * fator, np.nan)

    # checagem fisica: escoamento nao pode passar da chuva do pixel
    excede = valido & np.isfinite(P_chuva) & (Q_obs > P_chuva)
    n_excede = int(np.sum(excede))
    violacoes_total += n_excede
    if n_excede:
        Q_obs = np.where(excede, P_chuva, Q_obs)

    salva_raster(os.path.join(pasta, f"Q{n}_CN1_obs.tif"), Q_obs, gt, proj)

    pr_obs = np.where(valido, Q_obs / 1000.0 * AREA * (RI / R_evento) / 3600.0, np.nan)
    salva_raster(os.path.join(pasta, f"pr{n}_obs.tif"), pr_obs, gt, proj)

    base = np.where(valido, np.maximum(Q_obs * pr_obs * AREA, 0.0), np.nan)
    E_obs = np.where(valido, 11.8 * base ** 0.56 * K * C * P_CONST * LS, np.nan)
    salva_raster(os.path.join(pasta, f"E_unit{n}_obs.tif"), E_obs, gt, proj)
    Eunit_obs_rasters.append(E_obs)
    Eunit_obs_soma[n - 1] = np.nansum(E_obs)

    E_prev, _, _ = le_raster(os.path.join(pasta, f"E_unit{n}.tif"))
    Eunit_prev_soma[n - 1] = np.nansum(E_prev)

    print(f"{n:>3} {V_calc:>13,.0f} {V_med:>13,.0f} {fator:>7.3f} {n_excede:>13,} "
          f"{Eunit_prev_soma[n-1]:>12,.0f} {Eunit_obs_soma[n-1]:>12,.0f}")

print(f"\npixels com Q>P corrigidos (limitados a chuva): {violacoes_total:,} "
      f"de {17 * int(np.sum(np.isfinite(K))):,} ({100*violacoes_total/(17*np.sum(np.isfinite(K))):.3f}%)")

# ------------------------------------------------------------
# Calibra c e avalia (in-sample e leave-one-out)
# ------------------------------------------------------------
den = np.sum((SY_obs - SY_obs.mean()) ** 2)


def avalia(x, rotulo):
    c = np.sum(x * SY_obs) / np.sum(x ** 2)
    sim = c * x
    sim_loo = np.empty(17)
    for i in range(17):
        m = np.ones(17, dtype=bool)
        m[i] = False
        ci = np.sum(x[m] * SY_obs[m]) / np.sum(x[m] ** 2)
        sim_loo[i] = ci * x[i]
    nse = 1 - np.sum((SY_obs - sim) ** 2) / den
    nse_loo = 1 - np.sum((SY_obs - sim_loo) ** 2) / den
    err = 100 * (sim - SY_obs) / SY_obs
    err_loo = 100 * (sim_loo - SY_obs) / SY_obs
    wia = 1 - np.sum((SY_obs - sim) ** 2) / np.sum(
        (np.abs(sim - SY_obs.mean()) + np.abs(SY_obs - SY_obs.mean())) ** 2)
    pbias = 100 * np.sum(sim - SY_obs) / np.sum(SY_obs)
    print(f"\n--- {rotulo} ---")
    print(f"c = {c:.6f}")
    print(f"in-sample     : NSE={nse:.4f} | WIA={wia:.4f} | PBIAS={pbias:+.2f}% | "
          f"erro medio={err.mean():+.1f}% | abs={np.abs(err).mean():.1f}%")
    print(f"leave-one-out : NSE={nse_loo:.4f} | erro medio={err_loo.mean():+.1f}% | "
          f"abs={np.abs(err_loo).mean():.1f}%")
    return c, sim, err


print("\n" + "=" * 78)
c_prev, sim_prev, err_prev = avalia(Eunit_prev_soma, "PREVISAO PURA (Q do CN-SCS) - resultado atual")
c_obs, sim_obs, err_obs = avalia(Eunit_obs_soma, "VOLUME OBSERVADO COMO RESTRICAO")
print("=" * 78)

print(f"\n{'ev':>3} {'SY_obs(t)':>11} {'SY prev(t)':>11} {'erro%':>8} "
      f"{'SY restr(t)':>12} {'erro%':>8}")
for i in range(17):
    print(f"{i+1:>3} {SY_obs[i]:>11.1f} {sim_prev[i]:>11.1f} {err_prev[i]:>7.1f}% "
          f"{sim_obs[i]:>12.1f} {err_obs[i]:>7.1f}%")
    linhas.append({
        "evento": i + 1, "SY_obs_t": SY_obs[i],
        "SY_previsao_t": sim_prev[i], "erro_previsao_%": err_prev[i],
        "SY_restrito_t": sim_obs[i], "erro_restrito_%": err_obs[i],
        "soma_E_unit_previsao_t": Eunit_prev_soma[i],
        "soma_E_unit_restrito_t": Eunit_obs_soma[i],
    })

pd.DataFrame(linhas).to_csv(
    os.path.join(PASTA_DADOS, "comparacao_SY_previsao_vs_restrito.csv"),
    index=False, encoding="utf-8")

# ------------------------------------------------------------
# Mapas finais
# ------------------------------------------------------------
soma = None
conta = None
for n in range(1, 18):
    sy_pixel = c_obs * Eunit_obs_rasters[n - 1]
    salva_raster(os.path.join(BASE, f"Evento {n}", f"SY{n}_obs.tif"), sy_pixel, gt_ref, proj_ref)
    v = np.isfinite(sy_pixel)
    if soma is None:
        soma = np.where(v, sy_pixel, 0.0)
        conta = v.astype(np.float64)
    else:
        soma += np.where(v, sy_pixel, 0.0)
        conta += v.astype(np.float64)

sy_medio = np.where(conta > 0, soma / np.clip(conta, 1, None), np.nan)
salva_raster(os.path.join(PASTA_DADOS, "SY_medio_eventos_obs.tif"), sy_medio, gt_ref, proj_ref)

print(f"\nSY{{n}}_obs.tif salvo (17 eventos)")
print(f"Mapa medio: Dados Iniciais/SY_medio_eventos_obs.tif")
print(f"SY medio por pixel: min={np.nanmin(sy_medio):.6g} media={np.nanmean(sy_medio):.6g} "
      f"max={np.nanmax(sy_medio):.6g} t/evento")

# ------------------------------------------------------------
# Comparacao do padrao espacial entre os dois mapas
# ------------------------------------------------------------
sy_medio_prev, _, _ = le_raster(os.path.join(PASTA_DADOS, "SY_medio_eventos.tif"))
m = np.isfinite(sy_medio) & np.isfinite(sy_medio_prev)
r = np.corrcoef(sy_medio[m], sy_medio_prev[m])[0, 1]
print(f"\ncorrelacao espacial entre o mapa medio novo e o anterior: r={r:.4f}")

lim_novo = np.nanpercentile(sy_medio[m], 95)
lim_velho = np.nanpercentile(sy_medio_prev[m], 95)
hot_novo = sy_medio[m] >= lim_novo
hot_velho = sy_medio_prev[m] >= lim_velho
print(f"hot spots (top 5%) coincidentes entre os dois mapas: "
      f"{100*np.sum(hot_novo & hot_velho)/np.sum(hot_velho):.1f}%")
print("\nConcluido.")
