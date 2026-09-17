"""
ATENCAO: este script implementa o Metodo Racional (Qp = C*i*A/3,6) por
pixel usando o flow accumulation. Foi SUBSTITUIDO por
Scripts/spatialPeakFlowHU.py (Hidrograma Unitario Triangular do SCS),
porque a bacia (~138 km2) e grande demais para o Metodo Racional, que
so e valido para bacias pequenas (~2-3 km2, raramente ate ~8 km2) - o
resultado aqui superestimava a vazao de pico em 10x-80x. Mantido apenas
como registro do que foi tentado; ver notas_qgis_calibracao_qp.md
secao 3.2/3.3 para a explicacao completa.
"""

import os
import numpy as np
import pandas as pd
from osgeo import gdal

gdal.UseExceptions()

# ============================================================
# CONFIGURACOES GERAIS
# ============================================================

BASE = r"C:\TCC"
PASTA_DADOS = os.path.join(BASE, "Dados Iniciais")

CAMINHO_FLOWACC = os.path.join(PASTA_DADOS, "qp_spatial", "flowaccFINAL.sdat")
CAMINHO_EXCEL = os.path.join(PASTA_DADOS, "eventos_processados_manuais.xlsx")

# Grade de referencia: mesma grade usada pelo spatialRain.py para os
# rasters de chuva/Q/Qvol (fixa entre eventos, baseada na extensao do
# CN TCC.tif com PIXEL_SIZE=30 no IDW).
CAMINHO_GRADE_REF = os.path.join(BASE, "Evento 1", "ChuvaIDW1.tif")

# Coordenadas do exutorio real da bacia (onde Q_pico e T_R_m3 foram
# medidos): ponto unico onde drenagem.shp cruza o limite de
# "Mascara Jundiai.shp", identificado em Scripts/_find_outlet.py.
# Ja na mesma CRS da grade de referencia (SIRGAS 2000 / UTM 23S,
# EPSG:31983) - NAO e o ponto DBT5 (esse fica fora da bacia, ver
# notas_qgis_calibracao_qp.md secao 3.1).
EXUTORIO_X = 318980.7663669552
EXUTORIO_Y = 7432307.0820886735

# Raio (em pixels) da janela de busca para "encaixar" o ponto do
# exutorio no pixel de maior flow accumulation (canal mapeado) ali perto
JANELA_SNAP_PX = 4

CN_LABELS = ["CN1", "CN2", "CN3"]


# ============================================================
# ALINHA O FLOW ACCUMULATION A GRADE DE REFERENCIA
# ============================================================

ref_ds = gdal.Open(CAMINHO_GRADE_REF)
ref_gt = ref_ds.GetGeoTransform()
ref_proj = ref_ds.GetProjection()
ref_xsize = ref_ds.RasterXSize
ref_ysize = ref_ds.RasterYSize

flowacc_ds = gdal.Open(CAMINHO_FLOWACC)

flowacc_alinhado_path = os.path.join(PASTA_DADOS, "flowacc_alinhado_m2.tif")

gdal.Warp(
    flowacc_alinhado_path,
    flowacc_ds,
    format="GTiff",
    width=ref_xsize,
    height=ref_ysize,
    outputBounds=(
        ref_gt[0],
        ref_gt[3] + ref_ysize * ref_gt[5],
        ref_gt[0] + ref_xsize * ref_gt[1],
        ref_gt[3],
    ),
    dstSRS=ref_proj,
    resampleAlg=gdal.GRA_NearestNeighbour,
)

print(f"Flow accumulation alinhado salvo em: {flowacc_alinhado_path}")

flowacc_al_ds = gdal.Open(flowacc_alinhado_path)
flowacc_band = flowacc_al_ds.GetRasterBand(1)
flowacc_nodata = flowacc_band.GetNoDataValue()
if flowacc_nodata is None:
    flowacc_nodata = 0

A_m2 = flowacc_band.ReadAsArray().astype(np.float64)
A_km2 = A_m2 / 1.0e6


# ============================================================
# LOCALIZA O PIXEL DO EXUTORIO (SNAP AO CANAL)
# ============================================================

col0 = int((EXUTORIO_X - ref_gt[0]) / ref_gt[1])
row0 = int((EXUTORIO_Y - ref_gt[3]) / ref_gt[5])

r0 = max(row0 - JANELA_SNAP_PX, 0)
r1 = min(row0 + JANELA_SNAP_PX + 1, ref_ysize)
c0 = max(col0 - JANELA_SNAP_PX, 0)
c1 = min(col0 + JANELA_SNAP_PX + 1, ref_xsize)

janela = A_km2[r0:r1, c0:c1]
idx_local = np.unravel_index(np.argmax(janela), janela.shape)
row_exutorio = r0 + idx_local[0]
col_exutorio = c0 + idx_local[1]
area_exutorio_km2 = A_km2[row_exutorio, col_exutorio]

print("")
print(f"Pixel nominal do exutorio (sem snap): linha={row0}, coluna={col0}")
print(f"Pixel do exutorio apos snap ao canal: linha={row_exutorio}, coluna={col_exutorio}")
print(f"Area de drenagem no exutorio (snapped): {area_exutorio_km2:,.3f} km2")


# ============================================================
# LEITURA DA PLANILHA DE EVENTOS MEDIDOS
# ============================================================

df = pd.read_excel(CAMINHO_EXCEL, sheet_name="Sheet1")


# ============================================================
# LOOP DOS EVENTOS 1 A 17
# ============================================================

resultados = []

for numero_evento in range(1, 18):

    NOME_EVENTO = str(numero_evento)
    PASTA_EVENTO = os.path.join(BASE, f"Evento {NOME_EVENTO}")

    ev_index = 0 if numero_evento == 1 else numero_evento
    linha = df.iloc[ev_index]

    q_pico_medido = linha["Q_pico"]
    chuva_evento_mm = linha["Chuva_evento_mm"]
    intensidade_60min = linha["Intensidade_60min_mm/h"]

    if not chuva_evento_mm or pd.isna(chuva_evento_mm) or chuva_evento_mm <= 0:
        print(f"Evento {NOME_EVENTO}: Chuva_evento_mm invalida, pulando.")
        continue

    # Fator que converte a lamina total (P, espacializada por IDW) em uma
    # intensidade de pico (mm/h) por pixel, preservando o padrao espacial
    # do IDW mas calibrado para reproduzir a intensidade de pico medida
    # no evento.
    fator_intensidade = intensidade_60min / chuva_evento_mm

    caminho_idw = os.path.join(PASTA_EVENTO, f"ChuvaIDW{NOME_EVENTO}.tif")
    p_ds = gdal.Open(caminho_idw)
    p_band = p_ds.GetRasterBand(1)
    p_nodata = p_band.GetNoDataValue()
    if p_nodata is None:
        p_nodata = -9999
    P = p_band.ReadAsArray().astype(np.float64)

    linha_resultado = {
        "evento": numero_evento,
        "Q_pico_medido": q_pico_medido,
    }

    for cn in CN_LABELS:
        caminho_q = os.path.join(PASTA_EVENTO, f"Q{NOME_EVENTO}_{cn}.tif")
        if not os.path.exists(caminho_q):
            linha_resultado[f"Qp_{cn}_calc"] = np.nan
            continue

        q_ds = gdal.Open(caminho_q)
        q_band = q_ds.GetRasterBand(1)
        q_nodata = q_band.GetNoDataValue()
        if q_nodata is None:
            q_nodata = -9999
        Q = q_band.ReadAsArray().astype(np.float64)

        valido = (
            (P != p_nodata) &
            (Q != q_nodata) &
            (A_m2 != flowacc_nodata) &
            np.isfinite(P) &
            np.isfinite(Q) &
            np.isfinite(A_km2) &
            (P > 0)
        )

        # Coeficiente de escoamento C = Q/P (mesma base CN-SCS ja usada
        # no calculo do volume, evento a evento e cenario a cenario)
        C = np.zeros_like(P)
        C[valido] = Q[valido] / P[valido]

        i_raster = fator_intensidade * P  # mm/h

        # Metodo Racional: Qp (m3/s) = C * i (mm/h) * A (km2) / 3.6
        Qp = np.zeros_like(P)
        Qp[valido] = C[valido] * i_raster[valido] * A_km2[valido] / 3.6

        caminho_qp = os.path.join(PASTA_EVENTO, f"Qp{NOME_EVENTO}_{cn}.tif")
        driver = gdal.GetDriverByName("GTiff")
        out = driver.Create(
            caminho_qp, ref_xsize, ref_ysize, 1, gdal.GDT_Float32
        )
        out.SetGeoTransform(ref_gt)
        out.SetProjection(ref_proj)
        band_out = out.GetRasterBand(1)
        saida = np.where(valido, Qp, -9999).astype(np.float32)
        band_out.WriteArray(saida)
        band_out.SetNoDataValue(-9999)
        band_out.FlushCache()
        out.FlushCache()
        out = None

        qp_no_exutorio = float(Qp[row_exutorio, col_exutorio])
        linha_resultado[f"Qp_{cn}_calc"] = qp_no_exutorio

        print(
            f"Evento {NOME_EVENTO} | {cn} | "
            f"Qp no exutorio = {qp_no_exutorio:,.3f} m3/s | "
            f"medido = {q_pico_medido:,.3f} m3/s"
        )

    resultados.append(linha_resultado)


# ============================================================
# RESUMO FINAL
# ============================================================

out_df = pd.DataFrame(resultados)
for cn in CN_LABELS:
    col = f"Qp_{cn}_calc"
    out_df[f"erro_{cn}_%"] = (
        (out_df[col] - out_df["Q_pico_medido"]) / out_df["Q_pico_medido"] * 100
    )

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)
print("")
print("==============================================================")
print("      RESULTADO: Qp CALCULADO (RACIONAL) x Qp MEDIDO")
print("==============================================================")
print(out_df.to_string(index=False))

print("")
print("Resumo do erro percentual (media, |media|, desvio padrao):")
for cn in CN_LABELS:
    col = f"erro_{cn}_%"
    print(
        f"{cn}: media={out_df[col].mean():.1f}%  "
        f"media_abs={out_df[col].abs().mean():.1f}%  "
        f"std={out_df[col].std():.1f}%"
    )

caminho_csv_saida = os.path.join(
    PASTA_DADOS, "comparacao_qpico_medido_vs_calculado.csv"
)
out_df.to_csv(caminho_csv_saida, index=False)
print(f"\nCSV salvo em: {caminho_csv_saida}")
