"""
DIAGNOSTICO (nao e resultado final): separa as fontes de erro do modelo
espacializado adotado (SY = c * E_unit) para orientar o que ainda vale a
pena tentar antes da redacao do TCC.

Perguntas respondidas:
1. Se o volume de escoamento (Fase 1, erro absoluto 47%) fosse perfeito,
   quanto o modelo espacial melhoraria? (teto hidrologico)
2. A razao SY_obs/E_unit (que e o papel fisico do "c") varia muito entre
   eventos? Alguma variavel do evento explica essa variacao?
3. Como o modelo espacial se compara com a MUSLE concentrada (abordagem
   da IC) usando os MESMOS graus de liberdade (so uma escala calibrada)?

Nota sobre o expoente 1,12: em E_unit = 11,8*(Q*pr*A)^0,56*K*C*LS*P com
pr = (Q/1000)*A*(RI/R)/3600, o produto Q*pr e proporcional a Q^2, logo
E_unit ~ Q^1,12. Reescalar Q por um fator f (para bater o volume medido)
multiplica a soma de E_unit por f^1,12 - nao precisa reprocessar raster.
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


SY_obs = np.array([df_ev.iloc[ev_index(n)]["SYY_t"] for n in range(1, 18)], dtype=float)
obs_mean = SY_obs.mean()
den_nse = np.sum((SY_obs - obs_mean) ** 2)


def nse(sim):
    return 1 - np.sum((SY_obs - sim) ** 2) / den_nse


def ajusta_escala(x):
    """Minimos quadrados pela origem + metricas."""
    c = np.sum(x * SY_obs) / np.sum(x ** 2)
    sim = c * x
    erro = 100 * (sim - SY_obs) / SY_obs
    return c, nse(sim), erro.mean(), np.abs(erro).mean()


# ------------------------------------------------------------
# E_unit por evento (mesma leitura do calcular_sy_final.py)
# ------------------------------------------------------------
Eunit_soma = np.empty(17)
for n in range(1, 18):
    ds = gdal.Open(os.path.join(BASE, f"Evento {n}", f"E_unit{n}.tif"))
    band = ds.GetRasterBand(1)
    nodata = band.GetNoDataValue()
    arr = band.ReadAsArray().astype(np.float64)
    arr = np.where((arr != nodata) & np.isfinite(arr), arr, np.nan)
    Eunit_soma[n - 1] = np.nansum(arr)
    ds = None

# ------------------------------------------------------------
# Volumes medido x calculado (Fase 1)
# ------------------------------------------------------------
vol = pd.read_csv(os.path.join(PASTA_DADOS, "comparacao_volumes_medido_vs_calculado.csv"))
vol = vol.sort_values("evento")
V_med = vol["T_R_m3_medido"].to_numpy(dtype=float)
V_calc = vol["Vol_CN1_calc"].to_numpy(dtype=float)
Qp_med = vol["Q_pico_medido"].to_numpy(dtype=float)

print("=" * 78)
print("1. BASELINE ATUAL (adotado): SY = c * E_unit, com Q do modelo CN-SCS")
print("=" * 78)
c0, nse0, em0, ea0 = ajusta_escala(Eunit_soma)
print(f"c={c0:.6f} | NSE={nse0:.4f} | erro medio={em0:+.1f}% | erro abs medio={ea0:.1f}%")

print()
print("=" * 78)
print("2. TETO HIDROLOGICO: e se o volume de escoamento fosse perfeito?")
print("   (reescala Q por evento para bater T_R_m3 medido; E_unit ~ Q^1.12)")
print("=" * 78)
f = V_med / V_calc
Eunit_corr = Eunit_soma * f ** 1.12
c1, nse1, em1, ea1 = ajusta_escala(Eunit_corr)
print(f"fator de correcao de volume por evento: min={f.min():.2f} max={f.max():.2f}")
print(f"c={c1:.6f} | NSE={nse1:.4f} | erro medio={em1:+.1f}% | erro abs medio={ea1:.1f}%")
print(f">>> ganho de NSE sobre o baseline: {nse1 - nse0:+.4f}")

print()
print("=" * 78)
print("3. COMPARACAO com MUSLE CONCENTRADA (abordagem da IC), mesmos graus")
print("   de liberdade (so uma escala calibrada, alfa/beta fixos de Williams)")
print("=" * 78)
# Y ~ (D*qp)^0.56, D e qp MEDIDOS (K,LS,C,P entram como constantes -> absorvidos na escala)
x_lump_med = (V_med * Qp_med) ** 0.56
c2, nse2, em2, ea2 = ajusta_escala(x_lump_med)
print(f"[concentrada, D e qp MEDIDOS]    c={c2:.4g} | NSE={nse2:.4f} | "
      f"erro medio={em2:+.1f}% | erro abs={ea2:.1f}%")

# mesma coisa com D e qp do MODELO (Fase 1)
qp_csv = pd.read_csv(os.path.join(PASTA_DADOS,
                                  "comparacao_qpico_convolucao_medido_vs_calculado.csv"))
col_calc = [c for c in qp_csv.columns if "calc" in c.lower()]
qp_calc = qp_csv.sort_values(qp_csv.columns[0])[col_calc[0]].to_numpy(dtype=float)
x_lump_mod = (V_calc * qp_calc) ** 0.56
c3, nse3, em3, ea3 = ajusta_escala(x_lump_mod)
print(f"[concentrada, D e qp do MODELO]  c={c3:.4g} | NSE={nse3:.4f} | "
      f"erro medio={em3:+.1f}% | erro abs={ea3:.1f}%")

print()
print("=" * 78)
print("4. A razao SY_obs/E_unit (o papel fisico do 'c') varia entre eventos?")
print("   Se alguma variavel do evento explicar essa variacao, da pra trocar o")
print("   'c' constante por um 'c' que depende do evento (abordagem tipo Baert 2026)")
print("=" * 78)
razao = SY_obs / Eunit_soma
print(f"razao: min={razao.min():.4f} max={razao.max():.4f} media={razao.mean():.4f} "
      f"cv={razao.std()/razao.mean():.2f}")

candidatas = ["Chuva_evento_mm", "Intensidade_60min_mm/h", "Duracao_horas", "T_R_m3",
              "Q_pico", "Ap5_pond_mm", "Ap10_pond_mm", "CSS_pico", "Qb_inicio",
              "IEI", "TLe_h", "Iflow"]
print(f"\n{'variavel':<26} {'r(razao)':>10} {'r(log razao)':>14}")
for col in candidatas:
    if col not in df_ev.columns:
        continue
    v = np.array([df_ev.iloc[ev_index(n)][col] for n in range(1, 18)], dtype=float)
    if np.isnan(v).any():
        continue
    r = np.corrcoef(v, razao)[0, 1]
    r_log = np.corrcoef(np.log(v + 1e-9), np.log(razao))[0, 1]
    print(f"{col:<26} {r:>10.3f} {r_log:>14.3f}")

print()
print("=" * 78)
print("5. TETO COMBINADO: volume perfeito + 'c' dependente do melhor preditor")
print("=" * 78)
melhor_col, melhor_r = None, 0.0
for col in candidatas:
    if col not in df_ev.columns:
        continue
    v = np.array([df_ev.iloc[ev_index(n)][col] for n in range(1, 18)], dtype=float)
    if np.isnan(v).any():
        continue
    r_log = np.corrcoef(np.log(v + 1e-9), np.log(razao))[0, 1]
    if abs(r_log) > abs(melhor_r):
        melhor_col, melhor_r = col, r_log
print(f"melhor preditor da razao (em log): {melhor_col} (r={melhor_r:.3f})")
if melhor_col:
    v = np.array([df_ev.iloc[ev_index(n)][melhor_col] for n in range(1, 18)], dtype=float)
    # c_evento = a * v^b  -> ajusta a,b em log
    A = np.vstack([np.log(v + 1e-9), np.ones(17)]).T
    b, loga = np.linalg.lstsq(A, np.log(razao), rcond=None)[0]
    c_ev = np.exp(loga) * (v + 1e-9) ** b
    sim = c_ev * Eunit_soma
    erro = 100 * (sim - SY_obs) / SY_obs
    print(f"c_evento = {np.exp(loga):.4g} * {melhor_col}^{b:.3f}")
    print(f"NSE={nse(sim):.4f} | erro medio={erro.mean():+.1f}% | "
          f"erro abs medio={np.abs(erro).mean():.1f}%  (ATENCAO: 2 parametros extras,")
    print("  ajustado nos mesmos 17 eventos - precisa validacao cruzada leave-one-out)")

    # leave-one-out honesto
    sim_loo = np.empty(17)
    for i in range(17):
        m = np.ones(17, dtype=bool)
        m[i] = False
        Ai = np.vstack([np.log(v[m] + 1e-9), np.ones(m.sum())]).T
        bi, logai = np.linalg.lstsq(Ai, np.log(razao[m]), rcond=None)[0]
        sim_loo[i] = np.exp(logai) * (v[i] + 1e-9) ** bi * Eunit_soma[i]
    erro_loo = 100 * (sim_loo - SY_obs) / SY_obs
    print(f"leave-one-out: NSE={nse(sim_loo):.4f} | erro abs medio={np.abs(erro_loo).mean():.1f}%")

    # baseline com leave-one-out, para comparacao justa
    sim_loo_base = np.empty(17)
    for i in range(17):
        m = np.ones(17, dtype=bool)
        m[i] = False
        ci = np.sum(Eunit_soma[m] * SY_obs[m]) / np.sum(Eunit_soma[m] ** 2)
        sim_loo_base[i] = ci * Eunit_soma[i]
    print(f"baseline atual em leave-one-out: NSE={nse(sim_loo_base):.4f} | "
          f"erro abs medio={np.abs(100*(sim_loo_base-SY_obs)/SY_obs).mean():.1f}%")
