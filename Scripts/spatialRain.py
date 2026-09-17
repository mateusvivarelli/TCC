import os
import processing
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsVectorFileWriter
)
import numpy as np
from osgeo import gdal


# ============================================================
# CONFIGURAÇÕES GERAIS
# ============================================================

PASTA_DADOS = r"C:/TCC/Dados Iniciais"

# Razao de abstracao inicial (Ia = LAMBDA * S). O valor classico do SCS
# e 0,2, mas foi testado e calibrado nesta bacia (ver
# notas_qgis_calibracao_qp.md, secao 2.1): com LAMBDA=0,05 e o cenario
# CN-1 (S - Seco.tif, ja que a maioria dos eventos se classifica como
# AMC-I), o erro medio de volume cai de -62,6% para +0,5%. CN-1 e
# LAMBDA=0,05 sao o par adotado como calibracao final; os cenarios
# CN-2/CN-3 continuam sendo gerados apenas para fins de comparacao/
# analise de sensibilidade no texto do TCC.
LAMBDA = 0.05


# ============================================================
# RASTERS S DOS TRÊS CENÁRIOS
# ============================================================

caminho_s_cn1 = os.path.join(
    PASTA_DADOS,
    "S - Seco.tif"
)

caminho_s_cn2 = os.path.join(
    PASTA_DADOS,
    "S.tif"
)

caminho_s_cn3 = os.path.join(
    PASTA_DADOS,
    "S - Úmido.tif"
)


# Dicionário dos três cenários
caminhos_s = {
    "CN-1": caminho_s_cn1,
    "CN-2": caminho_s_cn2,
    "CN-3": caminho_s_cn3
}


# ============================================================
# DICIONÁRIOS PARA ARMAZENAR OS RESULTADOS
# ============================================================

# Volume total calculado para cada evento e CN
volumes_eventos = {
    "CN-1": {},
    "CN-2": {},
    "CN-3": {}
}


# ============================================================
# LOOP DOS EVENTOS 1 A 17
# ============================================================

for numero_evento in range(1, 18):

    NOME_EVENTO = str(numero_evento)

    print("")
    print("")
    print("==================================================")
    print(f"PROCESSANDO EVENTO {NOME_EVENTO}")
    print("==================================================")


    # ========================================================
    # PASTA DO EVENTO
    # ========================================================

    PASTA_EVENTO = os.path.join(
        os.path.dirname(PASTA_DADOS),
        f"Evento {NOME_EVENTO}"
    )

    os.makedirs(
        PASTA_EVENTO,
        exist_ok=True
    )


    # ========================================================
    # CAMINHOS DOS ARQUIVOS
    # ========================================================

    caminho_csv = os.path.normpath(
        os.path.join(
            PASTA_DADOS,
            "ESTPLUV",
            f"ESTPLUV_{NOME_EVENTO}.csv"
        )
    )

    caminho_cn = os.path.normpath(
        os.path.join(
            PASTA_DADOS,
            "CN TCC.tif"
        )
    )


    # ========================================================
    # LEITURA DO CSV DE CHUVA
    # ========================================================

    caminho_uri = caminho_csv.replace(
        "\\",
        "/"
    )

    uri = (
        f"file:///{caminho_uri}"
        f"?delimiter=;&xField=lon&yField=lat&crs=EPSG:4326"
    )

    csv_layer = QgsVectorLayer(
        uri,
        f"chuva_{NOME_EVENTO}",
        "delimitedtext"
    )

    QgsProject.instance().addMapLayer(
        csv_layer
    )


    # ========================================================
    # CARREGA CN DE REFERÊNCIA
    # ========================================================

    cn_layer = QgsRasterLayer(
        caminho_cn,
        "CN"
    )

    QgsProject.instance().addMapLayer(
        cn_layer
    )


    # ========================================================
    # REPROJEÇÃO DOS PONTOS
    # ========================================================

    resultado = processing.run(
        "native:reprojectlayer",
        {
            'INPUT': csv_layer,
            'TARGET_CRS': cn_layer.crs(),
            'OUTPUT': 'memory:'
        }
    )

    csv_proj = resultado['OUTPUT']

    csv_proj.setName(
        f"chuva_proj_{NOME_EVENTO}"
    )

    QgsProject.instance().addMapLayer(
        csv_proj
    )


    # ========================================================
    # SALVA SHAPEFILE
    # ========================================================

    caminho_shp = os.path.join(
        PASTA_EVENTO,
        f"EstPluv{NOME_EVENTO}.shp"
    )

    QgsVectorFileWriter.writeAsVectorFormat(
        csv_proj,
        caminho_shp,
        "UTF-8",
        csv_proj.crs(),
        "ESRI Shapefile"
    )


    # ========================================================
    # EXTENSÃO ESPACIAL
    # ========================================================

    extent = cn_layer.extent()

    extent_string = (
        f"{extent.xMinimum()},"
        f"{extent.xMaximum()},"
        f"{extent.yMinimum()},"
        f"{extent.yMaximum()} "
        f"[{cn_layer.crs().authid()}]"
    )


    # ========================================================
    # CAMPO DE PRECIPITAÇÃO
    # ========================================================

    idx_p = csv_proj.fields().indexOf(
        "P"
    )


    # ========================================================
    # INTERPOLAÇÃO IDW
    # ========================================================

    saida_idw = os.path.join(
        PASTA_EVENTO,
        f"ChuvaIDW{NOME_EVENTO}.tif"
    )

    layers_data = (
        f"{caminho_shp}::~::0::~::{idx_p}::~::0"
    )

    processing.run(
        "qgis:idwinterpolation",
        {
            'INTERPOLATION_DATA': layers_data,
            'DISTANCE_COEFFICIENT': 2,
            'EXTENT': extent_string,
            'PIXEL_SIZE': 30.0,
            'OUTPUT': saida_idw
        }
    )


    # ========================================================
    # ADICIONA RASTER DE CHUVA
    # ========================================================

    idw = QgsRasterLayer(
        saida_idw,
        f"ChuvaIDW{NOME_EVENTO}"
    )

    QgsProject.instance().addMapLayer(
        idw
    )


    # ========================================================
    # ABRE RASTER DE CHUVA
    # ========================================================

    chuva_gdal = gdal.Open(
        saida_idw
    )

    if chuva_gdal is None:
        print(
            f"ERRO: não foi possível abrir "
            f"{saida_idw}"
        )
        continue


    bandP = chuva_gdal.GetRasterBand(1)

    P = bandP.ReadAsArray().astype(
        np.float32
    )

    nodataP = bandP.GetNoDataValue()

    if nodataP is None:
        nodataP = -9999


    # ========================================================
    # LOOP DOS TRÊS CNs
    # ========================================================

    for CN in ["CN-1", "CN-2", "CN-3"]:

        print("")
        print(
            f"Calculando {CN} "
            f"para o Evento {NOME_EVENTO}"
        )


        # ====================================================
        # SELECIONA O RASTER S
        # ====================================================

        caminho_s = caminhos_s[CN]

        s_gdal = gdal.Open(
            caminho_s
        )

        if s_gdal is None:
            print(
                f"ERRO: não foi possível abrir "
                f"{caminho_s}"
            )
            continue


        bandS = s_gdal.GetRasterBand(1)

        nodataS = bandS.GetNoDataValue()

        if nodataS is None:
            nodataS = -9999


        # ====================================================
        # ALINHA O RASTER S AO RASTER DE CHUVA
        # ====================================================

        s_alinhado = gdal.Warp(
            "",
            s_gdal,
            format="MEM",
            width=chuva_gdal.RasterXSize,
            height=chuva_gdal.RasterYSize,
            outputBounds=(
                chuva_gdal.GetGeoTransform()[0],

                chuva_gdal.GetGeoTransform()[3]
                + chuva_gdal.RasterYSize
                * chuva_gdal.GetGeoTransform()[5],

                chuva_gdal.GetGeoTransform()[0]
                + chuva_gdal.RasterXSize
                * chuva_gdal.GetGeoTransform()[1],

                chuva_gdal.GetGeoTransform()[3]
            ),
            dstSRS=chuva_gdal.GetProjection(),
            resampleAlg=gdal.GRA_NearestNeighbour
        )


        # Lê S alinhado
        S = (
            s_alinhado
            .GetRasterBand(1)
            .ReadAsArray()
            .astype(np.float32)
        )


        # ====================================================
        # MÁSCARA DE PIXELS VÁLIDOS
        # ====================================================

        mask = (
            (P == nodataP) |
            (S == nodataS) |
            np.isnan(P) |
            np.isnan(S)
        )


        Q = np.full(
            P.shape,
            -9999,
            dtype=np.float32
        )

        valid = ~mask


        # ====================================================
        # CÁLCULO DE Q
        # ====================================================

        Q[valid] = np.where(
            P[valid] <= LAMBDA * S[valid],

            0,

            (
                P[valid]
                - LAMBDA * S[valid]
            ) ** 2
            /
            (
                P[valid]
                + (1 - LAMBDA) * S[valid]
            )
        )


        # ====================================================
        # RASTER Q
        # ====================================================

        saida_q = os.path.join(
            PASTA_EVENTO,
            f"Q{NOME_EVENTO}_{CN.replace('-', '')}.tif"
        )

        driver = gdal.GetDriverByName(
            "GTiff"
        )

        out = driver.Create(
            saida_q,
            chuva_gdal.RasterXSize,
            chuva_gdal.RasterYSize,
            1,
            gdal.GDT_Float32
        )

        out.SetGeoTransform(
            chuva_gdal.GetGeoTransform()
        )

        out.SetProjection(
            chuva_gdal.GetProjection()
        )

        band_out = out.GetRasterBand(1)

        band_out.WriteArray(Q)

        band_out.SetNoDataValue(
            -9999
        )

        band_out.FlushCache()

        out.FlushCache()

        out = None


        # ====================================================
        # ADICIONA RASTER Q AO QGIS
        # ====================================================

        q_layer = QgsRasterLayer(
            saida_q,
            f"Q{NOME_EVENTO} {CN}"
        )

        QgsProject.instance().addMapLayer(
            q_layer
        )


        # ====================================================
        # CONVERSÃO DE Q PARA VOLUME
        # ====================================================

        saida_vol = os.path.join(
            PASTA_EVENTO,
            f"Qvol{NOME_EVENTO}_{CN.replace('-', '')}.tif"
        )


        Q_vol_matriz = np.full(
            Q.shape,
            -9999,
            dtype=np.float32
        )


        # Q em mm
        # divide por 1000 → metros
        # pixel = 30 x 30 = 900 m²

        Q_vol_matriz[valid] = (
            Q[valid] / 1000.0
        ) * 900.0


        # ====================================================
        # CRIA RASTER DE VOLUME
        # ====================================================

        out_vol = driver.Create(
            saida_vol,
            chuva_gdal.RasterXSize,
            chuva_gdal.RasterYSize,
            1,
            gdal.GDT_Float32
        )

        out_vol.SetGeoTransform(
            chuva_gdal.GetGeoTransform()
        )

        out_vol.SetProjection(
            chuva_gdal.GetProjection()
        )

        band_vol = out_vol.GetRasterBand(1)

        band_vol.WriteArray(
            Q_vol_matriz
        )

        band_vol.SetNoDataValue(
            -9999
        )

        band_vol.FlushCache()

        out_vol.FlushCache()

        out_vol = None


        # ====================================================
        # ADICIONA RASTER DE VOLUME AO QGIS
        # ====================================================

        vol_layer = QgsRasterLayer(
            saida_vol,
            f"Qvol{NOME_EVENTO} {CN}"
        )

        QgsProject.instance().addMapLayer(
            vol_layer
        )


        # ====================================================
        # SOMA DO VOLUME
        # ====================================================

        v_calc_total = np.sum(
            Q_vol_matriz[valid]
        )


        # Guarda resultado
        volumes_eventos[CN][numero_evento] = (
            v_calc_total
        )


        # ====================================================
        # MOSTRA RESULTADO
        # ====================================================

        print(
            f"Evento {NOME_EVENTO} | "
            f"{CN} | "
            f"Volume = "
            f"{v_calc_total:,.2f} m³"
        )


# ============================================================
# RESULTADO FINAL
# ============================================================

print("")
print("")
print("==============================================================")
print("             RESULTADOS DOS 17 EVENTOS")
print("==============================================================")

print(
    f"{'Evento':>8} | "
    f"{'CN-1 (m³)':>18} | "
    f"{'CN-2 (m³)':>18} | "
    f"{'CN-3 (m³)':>18}"
)

print("--------------------------------------------------------------")


for evento in range(1, 18):

    volume_cn1 = volumes_eventos["CN-1"].get(
        evento,
        np.nan
    )

    volume_cn2 = volumes_eventos["CN-2"].get(
        evento,
        np.nan
    )

    volume_cn3 = volumes_eventos["CN-3"].get(
        evento,
        np.nan
    )

    print(
        f"{evento:>8} | "
        f"{volume_cn1:>18,.2f} | "
        f"{volume_cn2:>18,.2f} | "
        f"{volume_cn3:>18,.2f}"
    )


print("==============================================================")


# ============================================================
# SOMA DOS 17 EVENTOS PARA CADA CN
# ============================================================

total_cn1 = sum(
    volumes_eventos["CN-1"].values()
)

total_cn2 = sum(
    volumes_eventos["CN-2"].values()
)

total_cn3 = sum(
    volumes_eventos["CN-3"].values()
)


print("")
print("==============================================================")
print("             VOLUME TOTAL DOS 17 EVENTOS")
print("==============================================================")

print(
    f"CN-1: {total_cn1:,.2f} m³"
)

print(
    f"CN-2: {total_cn2:,.2f} m³"
)

print(
    f"CN-3: {total_cn3:,.2f} m³"
)

print("==============================================================")
