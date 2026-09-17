"""
Estimativa da vazao de pico (Qp) via convolucao do Hidrograma Unitario
Triangular do SCS com o hietograma real (horario) de chuva efetiva de
cada evento.

Isso substitui a versao "pulso unico" de spatialPeakFlowHU.py, que
superestimava muito o Qp porque os eventos duram de 23h a 149h (media
~72h) enquanto o tempo de pico da bacia (Tp) e de ~4h - tratar o volume
inteiro do evento como um unico pulso do tamanho de Tp nao faz sentido
quando a chuva esta espalhada por muito mais tempo que isso.

Fonte dos dados horarios: Dados Iniciais/Dados_finais_histereses_corrigido.xlsx
(serie horaria de chuva nos 2 postos e vazao medida, Nov/2018 em diante).

Passos:
1. Deriva um peso w1 (entre os 2 postos de chuva) que reproduz o total
   espacial ja usado (Chuva_evento_mm) a partir dos totais pontuais
   (chuva_p1_mm, chuva_p2_mm) - por minimos quadrados nos 17 eventos.
2. Para cada evento, monta o hietograma horario "de bacia" (P_bruto)
   combinando os 2 postos com esse peso.
3. Converte P_bruto acumulado em escoamento efetivo acumulado (CN-SCS,
   com o S medio da bacia no cenario CN-1 e lambda=0.05, ja calibrados
   em notas_qgis_calibracao_qp.md), e tira o incremento hora a hora -
   isso da o hietograma de chuva efetiva.
4. Convolui esse hietograma efetivo com o Hidrograma Unitario Triangular
   do SCS (recalculado para duracao unitaria D=1h, coerente com o passo
   horario dos dados) e pega o pico do hidrograma resultante.
5. Compara com Q_pico medido (da planilha de eventos) e, como checagem
   extra, com o proprio maximo da serie horaria medida dentro da janela
   do evento.
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

# Tc pela formula de Giandotti (mais adequada que Kirpich para bacias
# medias/grandes mistas no Brasil - Kirpich foi desenvolvida para bacias
# agricolas pequenas). Ver notas_qgis_calibracao_qp.md secao 3.10 para o
# processo completo de teste (Kirpich, Giandotti, Ven Te Chow, e uma
# tentativa de "calibrar Tc" que se mostrou redundante com o fator de pico
# abaixo - Tc sozinho nao reduz o erro real, so troca de forma com FATOR_PICO).
Tc_h = 10.652  # Giandotti: (4*sqrt(A)+1.5*L)/(0.8*sqrt(Hm)), A=138km2, L=37.587km, Hm=147.1m

# Fator de pico do HU-SCS: o padrao e 2,08 (equivalente ao PRF=484 em
# unidades imperiais), calibrado para bacias tipicas dos EUA. E documentado
# na literatura que bacias mais planas/com mais atenuacao (varzeas, uso do
# solo misto) precisam de um fator de pico reduzido (PRF tao baixo quanto
# 100-300 em alguns manuais, ou seja 0,2-0,62 do padrao). Calibramos esse
# fator diretamente contra os 17 eventos (minimizando o erro percentual
# absoluto medio, mantendo Tc fixo em Giandotti): fator_calibrado/2,08 =
# 0,538 -> dentro da faixa documentada para bacias atenuadas. Com a baixa
# declividade media desta bacia (0,0119 m/m), isso faz sentido fisico.
FATOR_PICO = 2.08 * 0.5377  # = 1.1184, calibrado (ver secao 3.10)

# ============================================================
# 1. S MEDIO DA BACIA (CN-1) - RECORTADO PELA MASCARA
# ============================================================

s_clip_path = os.path.join(PASTA_DADOS, "_s_cn1_clip_mascara_tmp.tif")
gdal.Warp(
    s_clip_path, CAMINHO_S_CN1, format="GTiff",
    cutlineDSName=CAMINHO_MASCARA, cropToCutline=True, dstNodata=-9999,
)
s_ds = gdal.Open(s_clip_path)
s_band = s_ds.GetRasterBand(1)
s_arr = s_band.ReadAsArray().astype(np.float64)
s_nodata = s_band.GetNoDataValue()
s_valid = s_arr != s_nodata
S_MEDIO = float(np.nanmean(s_arr[s_valid]))
s_band = None
s_ds = None
os.remove(s_clip_path)

print(f"S medio da bacia (CN-1): {S_MEDIO:.2f} mm")

# ============================================================
# 2. HIDROGRAMA UNITARIO TRIANGULAR (D = 1 h)
# ============================================================

D_h = 1.0
Tp_h = D_h / 2 + 0.6 * Tc_h
Tb_h = 2.67 * Tp_h
qp_UH = FATOR_PICO * AREA_BACIA_KM2 / Tp_h  # m3/s por cm, para 1h de chuva efetiva

print(f"Tp (D=1h) = {Tp_h:.3f} h ; Tb = {Tb_h:.3f} h ; qp_UH = {qp_UH:.3f} m3/s/cm")

horas_uh = np.arange(0, int(np.ceil(Tb_h)) + 1)
uh = np.where(
    horas_uh <= Tp_h,
    qp_UH * horas_uh / Tp_h,
    qp_UH * (Tb_h - horas_uh) / (Tb_h - Tp_h),
)
uh = np.clip(uh, 0, None)

# ============================================================
# 3. CARREGA SERIE HORARIA E PLANILHA DE EVENTOS
# ============================================================

df_horario = pd.read_excel(CAMINHO_EXCEL_HORARIO, sheet_name="Planilha1")
df_horario = df_horario.iloc[:, :5]
df_horario.columns = ["Data", "P_dbt5", "P_campo", "PrecTotal", "Q_medido_serie"]
df_horario["Data"] = pd.to_datetime(df_horario["Data"])
df_horario = df_horario.set_index("Data")

df_eventos = pd.read_excel(CAMINHO_EXCEL_EVENTOS, sheet_name="Sheet1")

# ============================================================
# 4. DERIVA O PESO w1 ENTRE OS 2 POSTOS (por minimos quadrados)
#    a partir de chuva_p1_mm / chuva_p2_mm / Chuva_evento_mm
# ============================================================

p1_tot, p2_tot, p_evento_tot = [], [], []
for numero_evento in range(1, 18):
    ev_index = 0 if numero_evento == 1 else numero_evento
    row = df_eventos.iloc[ev_index]
    p1_tot.append(row["chuva_p1_mm"])
    p2_tot.append(row["chuva_p2_mm"])
    p_evento_tot.append(row["Chuva_evento_mm"])

p1_tot = np.array(p1_tot)
p2_tot = np.array(p2_tot)
p_evento_tot = np.array(p_evento_tot)

# Chuva_evento_mm ~= w1*p1 + (1-w1)*p2  =>  Chuva_evento_mm - p2 = w1*(p1-p2)
A = (p1_tot - p2_tot).reshape(-1, 1)
b = (p_evento_tot - p2_tot)
w1 = float(np.linalg.lstsq(A, b, rcond=None)[0][0])
w1 = min(max(w1, 0.0), 1.0)
print(f"\nPeso w1 (posto DBT5) ajustado por minimos quadrados: {w1:.3f}")
print(f"(peso do posto Campo Limpo Paulista = {1 - w1:.3f})")

# ============================================================
# 5. LOOP DOS EVENTOS: HIETOGRAMA -> CHUVA EFETIVA -> CONVOLUCAO
# ============================================================

resultados = []
for numero_evento in range(1, 18):
    ev_index = 0 if numero_evento == 1 else numero_evento
    row = df_eventos.iloc[ev_index]
    inicio, fim = row["Inicio"], row["Fim"]
    q_pico_medido = row["Q_pico"]

    janela = df_horario.loc[inicio:fim]
    if janela.empty:
        print(f"Evento {numero_evento}: janela horaria vazia, pulando.")
        continue

    p_bruto = w1 * janela["P_dbt5"].fillna(0) + (1 - w1) * janela["P_campo"].fillna(0)
    p_bruto = p_bruto.to_numpy()

    p_cum = np.cumsum(p_bruto)
    q_cum = np.where(
        p_cum <= LAMBDA * S_MEDIO,
        0.0,
        (p_cum - LAMBDA * S_MEDIO) ** 2 / (p_cum + (1 - LAMBDA) * S_MEDIO),
    )
    q_incremental_mm = np.diff(q_cum, prepend=0.0)
    q_incremental_cm = q_incremental_mm / 10.0

    # convolucao com o HU horario
    hidrograma = np.convolve(q_incremental_cm, uh)
    qp_calc = float(np.max(hidrograma))

    q_medido_serie_max = float(janela["Q_medido_serie"].max())

    resultados.append({
        "evento": numero_evento,
        "Q_pico_medido_planilha": q_pico_medido,
        "Q_pico_medido_serie_horaria": q_medido_serie_max,
        "Qp_calc_convolucao": qp_calc,
        "erro_%": (qp_calc - q_pico_medido) / q_pico_medido * 100,
    })

out_df = pd.DataFrame(resultados)
pd.set_option("display.width", 200)
print("\n" + "=" * 70)
print("RESULTADO: Qp CALCULADO (convolucao HU-SCS horaria) x Qp MEDIDO")
print("=" * 70)
print(out_df.to_string(index=False))

print(f"\nerro medio = {out_df['erro_%'].mean():.1f}%  "
      f"erro medio abs = {out_df['erro_%'].abs().mean():.1f}%  "
      f"std = {out_df['erro_%'].std():.1f}%")

caminho_saida = os.path.join(
    PASTA_DADOS, "comparacao_qpico_convolucao_medido_vs_calculado.csv"
)
out_df.to_csv(caminho_saida, index=False)
print(f"\nCSV salvo em: {caminho_saida}")
