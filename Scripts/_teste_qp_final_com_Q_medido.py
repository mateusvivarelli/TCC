"""
Testa o metodo final de Qp (Tc=Giandotti, fator de pico calibrado=1,1184)
usando o volume MEDIDO (T_R_m3) em vez do calculado pelo modelo CN-SCS,
para isolar se o mecanismo de conversao volume->pico (HU-SCS) esta bom,
sem misturar com o erro ja conhecido do volume calculado.

Mesma logica do script de producao (spatialPeakFlowHU_convolucao.py),
so que o hietograma de chuva efetiva e reescalado (por um fator unico
por evento) para que o volume total bata exatamente com T_R_m3 medido,
mantendo a MESMA forma temporal que o modelo calcula.
"""

import os
import numpy as np
import pandas as pd
from osgeo import gdal

gdal.UseExceptions()

BASE = r"C:\TCC"
PASTA_DADOS = os.path.join(BASE, "Dados Iniciais")

CAMINHO_EXCEL_EVENTOS = os.path.join(PASTA_DADOS, "eventos_processados_manuais.xlsx")
CAMINHO_EXCEL_HORARIO = os.path.join(PASTA_DADOS, "Dados_finais_histereses_corrigido.xlsx")
CAMINHO_S_CN1 = os.path.join(PASTA_DADOS, "S - Seco.tif")
CAMINHO_MASCARA = os.path.join(PASTA_DADOS, "Máscara Jundiaí.shp")

AREA_BACIA_KM2 = 138.0
LAMBDA = 0.05
Tc_h = 10.652
FATOR_PICO = 2.08 * 0.5377

# --- S medio ---
s_clip_path = os.path.join(PASTA_DADOS, "_s_tmp5.tif")
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

# --- HU triangular ---
D_h = 1.0
Tp_h = D_h / 2 + 0.6 * Tc_h
Tb_h = 2.67 * Tp_h
qp_UH = FATOR_PICO * AREA_BACIA_KM2 / Tp_h

horas_uh = np.arange(0, int(np.ceil(Tb_h)) + 1)
uh = np.where(horas_uh <= Tp_h, qp_UH * horas_uh / Tp_h, qp_UH * (Tb_h - horas_uh) / (Tb_h - Tp_h))
uh = np.clip(uh, 0, None)

print(f"Tc={Tc_h}h, Tp={Tp_h:.3f}h, Tb={Tb_h:.3f}h, qp_UH={qp_UH:.3f} m3/s/cm")

# --- dados horarios e peso w1 ---
df_horario = pd.read_excel(CAMINHO_EXCEL_HORARIO, sheet_name="Planilha1")
df_horario = df_horario.iloc[:, :5]
df_horario.columns = ["Data", "P_dbt5", "P_campo", "PrecTotal", "Q_medido_serie"]
df_horario["Data"] = pd.to_datetime(df_horario["Data"])
df_horario = df_horario.set_index("Data")

df_eventos = pd.read_excel(CAMINHO_EXCEL_EVENTOS, sheet_name="Sheet1")

p1_tot, p2_tot, p_evento_tot = [], [], []
for numero_evento in range(1, 18):
    ev_index = 0 if numero_evento == 1 else numero_evento
    row = df_eventos.iloc[ev_index]
    p1_tot.append(row["chuva_p1_mm"]); p2_tot.append(row["chuva_p2_mm"]); p_evento_tot.append(row["Chuva_evento_mm"])
p1_tot, p2_tot, p_evento_tot = map(np.array, (p1_tot, p2_tot, p_evento_tot))
A = (p1_tot - p2_tot).reshape(-1, 1)
b = (p_evento_tot - p2_tot)
w1 = float(np.linalg.lstsq(A, b, rcond=None)[0][0])
w1 = min(max(w1, 0.0), 1.0)

resultados = []
for numero_evento in range(1, 18):
    ev_index = 0 if numero_evento == 1 else numero_evento
    row = df_eventos.iloc[ev_index]
    inicio, fim = row["Inicio"], row["Fim"]
    q_pico_medido = row["Q_pico"]
    t_r_m3_medido = row["T_R_m3"]

    janela = df_horario.loc[inicio:fim]
    if janela.empty:
        continue

    p_bruto = (w1 * janela["P_dbt5"].fillna(0) + (1 - w1) * janela["P_campo"].fillna(0)).to_numpy()
    p_cum = np.cumsum(p_bruto)
    q_cum = np.where(p_cum <= LAMBDA * S_MEDIO, 0.0,
                      (p_cum - LAMBDA * S_MEDIO) ** 2 / (p_cum + (1 - LAMBDA) * S_MEDIO))
    q_incremental_mm = np.diff(q_cum, prepend=0.0)

    # reescala para o volume MEDIDO (mesma forma temporal, volume corrigido)
    total_modelo_mm = np.sum(q_incremental_mm)
    total_medido_mm = t_r_m3_medido / (AREA_BACIA_KM2 * 1e6) * 1000.0
    fator = total_medido_mm / total_modelo_mm if total_modelo_mm > 0 else np.nan
    q_incremental_mm_medido = q_incremental_mm * fator

    q_incremental_cm = q_incremental_mm_medido / 10.0
    hidrograma = np.convolve(q_incremental_cm, uh)
    qp_calc = float(np.max(hidrograma))

    resultados.append({
        "evento": numero_evento,
        "Q_pico_medido": q_pico_medido,
        "T_R_m3_medido": t_r_m3_medido,
        "Qp_calc_com_Q_medido": qp_calc,
        "erro_%": (qp_calc - q_pico_medido) / q_pico_medido * 100,
    })

out_df = pd.DataFrame(resultados)
pd.set_option("display.width", 200)
print("\n" + "=" * 70)
print("TESTE: metodo final de Qp (Tc=Giandotti, fator de pico=1,1184)")
print("usando volume MEDIDO (T_R_m3) em vez do calculado pelo modelo")
print("=" * 70)
print(out_df.to_string(index=False))

print(f"\nerro medio = {out_df['erro_%'].mean():.1f}%  "
      f"erro medio abs = {out_df['erro_%'].abs().mean():.1f}%  "
      f"std = {out_df['erro_%'].std():.1f}%")

caminho_saida = os.path.join(PASTA_DADOS, "comparacao_qpico_metodo_final_com_Q_medido.csv")
out_df.to_csv(caminho_saida, index=False)
print(f"\nCSV salvo em: {caminho_saida}")
