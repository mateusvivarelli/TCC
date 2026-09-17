"""
Calibra os parametros do mecanismo de geracao de Qp (Tc, fator de pico
do HU-SCS, e o peso w1 entre os 2 postos de chuva na disaggregacao
horaria) usando o volume MEDIDO (T_R_m3) como entrada e Qp MEDIDO como
alvo - ou seja, testa o quao bom e o mecanismo em si (Tc + HU-SCS +
disaggregacao horaria), sem nenhuma interferencia do erro do volume
calculado pelo modelo CN-SCS.
"""

import os
import numpy as np
import pandas as pd
from osgeo import gdal
from scipy.optimize import minimize

gdal.UseExceptions()

BASE = r"C:\TCC"
PASTA_DADOS = os.path.join(BASE, "Dados Iniciais")
CAMINHO_S_CN1 = os.path.join(PASTA_DADOS, "S - Seco.tif")
CAMINHO_MASCARA = os.path.join(PASTA_DADOS, "Máscara Jundiaí.shp")

AREA_BACIA_KM2 = 138.0
LAMBDA = 0.05

s_clip_path = os.path.join(PASTA_DADOS, "_s_tmp6.tif")
gdal.Warp(s_clip_path, CAMINHO_S_CN1, format="GTiff",
          cutlineDSName=CAMINHO_MASCARA, cropToCutline=True, dstNodata=-9999)
s_ds = gdal.Open(s_clip_path)
s_band = s_ds.GetRasterBand(1)
s_arr = s_band.ReadAsArray().astype(np.float64)
s_nodata = s_band.GetNoDataValue()
S_MEDIO = float(np.nanmean(s_arr[s_arr != s_nodata]))
s_band = None
s_ds = None
os.remove(s_clip_path)

df_horario = pd.read_excel(PASTA_DADOS + r"\Dados_finais_histereses_corrigido.xlsx", sheet_name="Planilha1")
df_horario = df_horario.iloc[:, :5]
df_horario.columns = ["Data", "P_dbt5", "P_campo", "PrecTotal", "Q_medido_serie"]
df_horario["Data"] = pd.to_datetime(df_horario["Data"])
df_horario = df_horario.set_index("Data")

df_eventos = pd.read_excel(PASTA_DADOS + r"\eventos_processados_manuais.xlsx", sheet_name="Sheet1")

EVENTOS = []
for numero_evento in range(1, 18):
    ev_index = 0 if numero_evento == 1 else numero_evento
    row = df_eventos.iloc[ev_index]
    inicio, fim = row["Inicio"], row["Fim"]
    janela = df_horario.loc[inicio:fim]
    if janela.empty:
        continue
    EVENTOS.append({
        "evento": numero_evento,
        "p_dbt5": janela["P_dbt5"].fillna(0).to_numpy(),
        "p_campo": janela["P_campo"].fillna(0).to_numpy(),
        "q_pico_medido": row["Q_pico"],
        "t_r_m3_medido": row["T_R_m3"],
    })


def monta_uh(tc_h, fator_pico, d_h=1.0):
    tp_h = d_h / 2 + 0.6 * tc_h
    tb_h = 2.67 * tp_h
    qp_uh = fator_pico * AREA_BACIA_KM2 / tp_h
    horas = np.arange(0, int(np.ceil(tb_h)) + 1)
    uh = np.where(horas <= tp_h, qp_uh * horas / tp_h, qp_uh * (tb_h - horas) / (tb_h - tp_h))
    return np.clip(uh, 0, None)


def calcula_erros(params):
    tc_h, fator_pico, w1 = params
    if tc_h <= 0.1 or fator_pico <= 0.01 or not (0 <= w1 <= 1):
        return None
    uh = monta_uh(tc_h, fator_pico)
    erros = []
    for ev in EVENTOS:
        p_bruto = w1 * ev["p_dbt5"] + (1 - w1) * ev["p_campo"]
        p_cum = np.cumsum(p_bruto)
        q_cum = np.where(p_cum <= LAMBDA * S_MEDIO, 0.0,
                          (p_cum - LAMBDA * S_MEDIO) ** 2 / (p_cum + (1 - LAMBDA) * S_MEDIO))
        q_incr_mm = np.diff(q_cum, prepend=0.0)

        total_modelo_mm = np.sum(q_incr_mm)
        total_medido_mm = ev["t_r_m3_medido"] / (AREA_BACIA_KM2 * 1e6) * 1000.0
        if total_modelo_mm <= 0:
            return None
        fator = total_medido_mm / total_modelo_mm
        q_incr_mm = q_incr_mm * fator

        q_incr_cm = q_incr_mm / 10.0
        hidrograma = np.convolve(q_incr_cm, uh)
        qp_calc = float(np.max(hidrograma))
        erros.append((qp_calc - ev["q_pico_medido"]) / ev["q_pico_medido"] * 100)
    return np.array(erros)


def custo(params):
    erros = calcula_erros(params)
    if erros is None:
        return 1e6
    return np.abs(erros).mean()


# ponto inicial: Tc=Giandotti, fator_pico=1.1184, w1=0.307 (ja calibrados antes)
x0 = [10.652, 1.1184, 0.307]
res = minimize(custo, x0, method="Nelder-Mead",
               options={"xatol": 1e-4, "fatol": 1e-4, "maxiter": 5000})

tc_final, fator_final, w1_final = res.x
print(f"Otimizacao convergiu: {res.success}, custo final (erro abs medio) = {res.fun:.3f}%")
print(f"Tc = {tc_final:.3f} h")
print(f"Fator de pico = {fator_final:.4f}")
print(f"w1 (peso DBT5) = {w1_final:.4f}  (peso Campo Limpo = {1-w1_final:.4f})")

erros_finais = calcula_erros(res.x)
print(f"\nerro medio = {erros_finais.mean():.2f}%")
print(f"erro absoluto medio = {np.abs(erros_finais).mean():.2f}%")
print(f"desvio padrao = {erros_finais.std():.2f}%")

print("\nPor evento:")
for i, ev in enumerate(EVENTOS):
    print(f"  evento {ev['evento']:>2}: medido={ev['q_pico_medido']:>7.2f}  erro={erros_finais[i]:>7.1f}%")

# comparacao: parametros antigos (Tc=Giandotti, fator=1.1184, w1=0.307 fixo)
erros_antigos = calcula_erros([10.652, 1.1184, 0.307])
print(f"\n--- Comparacao com os parametros anteriores (nao otimizados p/ Q medido) ---")
print(f"erro medio = {erros_antigos.mean():.2f}%  erro abs = {np.abs(erros_antigos).mean():.2f}%  "
      f"std = {erros_antigos.std():.2f}%")
