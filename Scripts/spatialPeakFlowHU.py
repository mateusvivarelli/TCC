"""
ATENCAO: esta versao ("pulso unico" - trata o volume inteiro do evento
como se fosse liberado num unico pulso do tamanho de Tp) foi SUBSTITUIDA
por Scripts/spatialPeakFlowHU_convolucao.py, porque os eventos duram de
23h a 149h enquanto o Tp da bacia e de ~4h - com o volume recalibrado
(lambda=0.05, ver secao 3.4 das notas) o erro aqui piorou muito (+364%
em vez de +103%). Mantido como registro do que foi tentado; ver
notas_qgis_calibracao_qp.md secao 3.6.

Espacializacao/estimativa da vazao de pico (Qp) via Hidrograma Unitario
Triangular do SCS, substituindo o Metodo Racional (invalido para uma
bacia de 138 km2 - ver notas_qgis_calibracao_qp.md, secao 3.2/3.3).

Reaproveita os rasters Qvol{n}_CN{1,2,3}.tif ja gerados pelo
spatialRain.py (volume de escoamento direto, m3, por evento e cenario
de CN) e o comprimento do curso d'agua principal obtido a partir da
rede de drenagem digitalizada (drenagem.shp).

Passos:
1. Monta um grafo a partir de drenagem.shp e calcula o comprimento do
   curso d'agua principal (exutorio -> ponto mais distante da rede).
2. Calcula o tempo de concentracao (Kirpich, forma SI/Tucci) e o tempo
   de pico do HU-SCS.
3. Calcula o vazao de pico unitaria (m3/s por cm de escoamento direto).
4. Para cada evento/cenario de CN, converte o volume ja calculado em
   lamina media sobre a area oficial da bacia (138 km2) e aplica a
   vazao de pico unitaria.
5. Compara com Q_pico medido e salva um CSV de resultado.
"""

import os
import numpy as np
import pandas as pd
import networkx as nx
from osgeo import gdal, ogr

gdal.UseExceptions()
ogr.UseExceptions()

# ============================================================
# CONFIGURACOES GERAIS
# ============================================================

BASE = r"C:\TCC"
PASTA_DADOS = os.path.join(BASE, "Dados Iniciais")

CAMINHO_DRENAGEM = os.path.join(PASTA_DADOS, "drenagem.shp")
CAMINHO_DEM = os.path.join(PASTA_DADOS, "MDE 30m.tif")
CAMINHO_EXCEL = os.path.join(PASTA_DADOS, "eventos_processados_manuais.xlsx")

# Exutorio real da bacia: unico ponto onde drenagem.shp cruza o limite
# de "Mascara Jundiai.shp" (ver Scripts/_find_outlet.py). NAO e o ponto
# DBT5 usado como posto de chuva (esse fica fora da bacia).
OUTLET_X = 318980.7663669552
OUTLET_Y = 7432307.0820886735

# Area oficial da bacia no exutorio (informada pelo usuario; o flow
# accumulation deu ~109.79 km2, ~20% abaixo - possivel imprecisao da
# mascara/MDE, ver notas_qgis_calibracao_qp.md secao 3.3)
AREA_BACIA_KM2 = 138.0

CN_LABELS = ["CN1", "CN2", "CN3"]
TOL_NO = 0.01  # tolerancia (m) para casar nos da rede de drenagem


# ============================================================
# 1. COMPRIMENTO DO CURSO D'AGUA PRINCIPAL (via rede de drenagem)
# ============================================================

def chave_no(x, y):
    return (round(x / TOL_NO) * TOL_NO, round(y / TOL_NO) * TOL_NO)


def comprimento_curso_principal():
    ds = ogr.Open(CAMINHO_DRENAGEM)
    layer = ds.GetLayer()

    grafo = nx.Graph()
    for feat in layer:
        geom = feat.GetGeometryRef()
        if geom is None:
            continue
        linhas = []
        gtype = geom.GetGeometryType()
        if gtype in (ogr.wkbLineString, ogr.wkbLineString25D):
            linhas = [geom]
        elif gtype in (ogr.wkbMultiLineString, ogr.wkbMultiLineString25D):
            linhas = [geom.GetGeometryRef(i) for i in range(geom.GetGeometryCount())]

        for linha in linhas:
            n = linha.GetPointCount()
            if n < 2:
                continue
            p0 = linha.GetPoint(0)
            p1 = linha.GetPoint(n - 1)
            comprimento = linha.Length()
            k0, k1 = chave_no(*p0[:2]), chave_no(*p1[:2])
            if grafo.has_edge(k0, k1):
                if grafo[k0][k1]["weight"] > comprimento:
                    grafo[k0][k1]["weight"] = comprimento
            else:
                grafo.add_edge(k0, k1, weight=comprimento)

    no_exutorio = chave_no(OUTLET_X, OUTLET_Y)
    if no_exutorio not in grafo:
        raise RuntimeError(
            "No do exutorio nao encontrado na rede de drenagem "
            "(esperado casar exatamente com drenagem.shp)."
        )

    distancias = nx.single_source_dijkstra_path_length(
        grafo, no_exutorio, weight="weight"
    )
    no_mais_distante = max(distancias, key=distancias.get)
    L_m = distancias[no_mais_distante]

    return L_m, no_mais_distante


L_m, no_cabeceira = comprimento_curso_principal()
print(f"Comprimento do curso d'agua principal: {L_m:.1f} m ({L_m/1000:.3f} km)")
print(f"Ponto de cabeceira (mais distante do exutorio): {no_cabeceira}")


# ============================================================
# 2. TEMPO DE CONCENTRACAO E TEMPO DE PICO (HU-SCS)
# ============================================================

dem_ds = gdal.Open(CAMINHO_DEM)
dem_gt = dem_ds.GetGeoTransform()
dem_arr = dem_ds.GetRasterBand(1).ReadAsArray().astype(np.float64)


def elevacao_em(x, y):
    col = int((x - dem_gt[0]) / dem_gt[1])
    row = int((y - dem_gt[3]) / dem_gt[5])
    return dem_arr[row, col]


h_exutorio = elevacao_em(OUTLET_X, OUTLET_Y)
h_cabeceira = elevacao_em(*no_cabeceira)
delta_h = h_cabeceira - h_exutorio

L_km = L_m / 1000.0
S = delta_h / L_m

print(f"H exutorio = {h_exutorio:.2f} m ; H cabeceira = {h_cabeceira:.2f} m ; "
      f"Delta H = {delta_h:.2f} m ; S = {S:.5f} m/m")

# Kirpich (forma SI / Tucci): Tc em horas, L em km, S em m/m
Tc_h = 0.0663 * (L_km ** 0.77) * (S ** -0.385)

# Relacoes padrao do HU-SCS: D = 0.133*Tc (duracao unitaria),
# Tl = 0.6*Tc (tempo de retardo), Tp = D/2 + Tl
Tp_h = 0.667 * Tc_h

# Vazao de pico unitaria do HU-SCS (SI): qp = 2.08*A/Tp [m3/s por cm]
qp_unitario = 2.08 * AREA_BACIA_KM2 / Tp_h

print(f"Tc (Kirpich) = {Tc_h:.3f} h ({Tc_h*60:.1f} min)")
print(f"Tp = {Tp_h:.3f} h")
print(f"qp unitario (HU-SCS) = {qp_unitario:.3f} m3/s por cm de escoamento direto")


# ============================================================
# 3. APLICA AOS 17 EVENTOS (reaproveita os Qvol* ja calculados)
# ============================================================

df = pd.read_excel(CAMINHO_EXCEL, sheet_name="Sheet1")

resultados = []
for numero_evento in range(1, 18):
    ev_index = 0 if numero_evento == 1 else numero_evento
    linha_excel = df.iloc[ev_index]
    q_pico_medido = linha_excel["Q_pico"]

    linha_resultado = {"evento": numero_evento, "Q_pico_medido": q_pico_medido}

    for cn in CN_LABELS:
        caminho_qvol = os.path.join(
            BASE, f"Evento {numero_evento}", f"Qvol{numero_evento}_{cn}.tif"
        )
        ds = gdal.Open(caminho_qvol)
        band = ds.GetRasterBand(1)
        nodata = band.GetNoDataValue()
        arr = band.ReadAsArray().astype(np.float64)
        valido = arr != nodata
        vol_total_m3 = np.sum(arr[valido])

        qr_mm = vol_total_m3 / (AREA_BACIA_KM2 * 1.0e6) * 1000.0
        qr_cm = qr_mm / 10.0

        linha_resultado[f"Qp_{cn}_calc"] = qp_unitario * qr_cm

    resultados.append(linha_resultado)

out_df = pd.DataFrame(resultados)
for cn in CN_LABELS:
    out_df[f"erro_{cn}_%"] = (
        (out_df[f"Qp_{cn}_calc"] - out_df["Q_pico_medido"])
        / out_df["Q_pico_medido"] * 100
    )

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)
print("\n" + "=" * 70)
print("RESULTADO: Qp CALCULADO (HU-SCS) x Qp MEDIDO")
print("=" * 70)
print(out_df.to_string(index=False))

print("\nResumo do erro percentual:")
for cn in CN_LABELS:
    col = f"erro_{cn}_%"
    print(
        f"{cn}: media={out_df[col].mean():.1f}%  "
        f"media_abs={out_df[col].abs().mean():.1f}%  "
        f"std={out_df[col].std():.1f}%"
    )

caminho_saida = os.path.join(
    PASTA_DADOS, "comparacao_qpico_HU-SCS_medido_vs_calculado.csv"
)
out_df.to_csv(caminho_saida, index=False)
print(f"\nCSV salvo em: {caminho_saida}")
