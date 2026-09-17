import os
import numpy as np
import pandas as pd
from osgeo import gdal
from scipy.optimize import brentq

gdal.UseExceptions()

BASE = r"C:\TCC"
PASTA_DADOS = os.path.join(BASE, "Dados Iniciais")
CAMINHO_S_CN1 = os.path.join(PASTA_DADOS, "S - Seco.tif")

df = pd.read_excel(
    os.path.join(PASTA_DADOS, "eventos_processados_manuais.xlsx"), sheet_name="Sheet1"
)

s_ds = gdal.Open(CAMINHO_S_CN1)


def volume_para_lambda(P, S, valid, lam):
    Q = np.zeros_like(P)
    Q[valid] = np.where(
        P[valid] <= lam * S[valid],
        0,
        (P[valid] - lam * S[valid]) ** 2 / (P[valid] + (1 - lam) * S[valid]),
    )
    return np.sum(Q[valid]) / 1000.0 * 900.0


resultados = []
for numero_evento in range(1, 18):
    PASTA_EVENTO = os.path.join(BASE, f"Evento {numero_evento}")
    caminho_idw = os.path.join(PASTA_EVENTO, f"ChuvaIDW{numero_evento}.tif")

    p_ds = gdal.Open(caminho_idw)
    p_band = p_ds.GetRasterBand(1)
    p_nodata = p_band.GetNoDataValue() or -9999
    P = p_band.ReadAsArray().astype(np.float64)

    s_aligned = gdal.Warp(
        "", s_ds, format="MEM",
        width=p_ds.RasterXSize, height=p_ds.RasterYSize,
        outputBounds=(
            p_ds.GetGeoTransform()[0],
            p_ds.GetGeoTransform()[3] + p_ds.RasterYSize * p_ds.GetGeoTransform()[5],
            p_ds.GetGeoTransform()[0] + p_ds.RasterXSize * p_ds.GetGeoTransform()[1],
            p_ds.GetGeoTransform()[3],
        ),
        dstSRS=p_ds.GetProjection(),
        resampleAlg=gdal.GRA_NearestNeighbour,
    )
    S = s_aligned.GetRasterBand(1).ReadAsArray().astype(np.float64)
    s_nodata = s_aligned.GetRasterBand(1).GetNoDataValue() or -9999

    valid = (P != p_nodata) & (S != s_nodata) & np.isfinite(P) & np.isfinite(S)

    ev_index = 0 if numero_evento == 1 else numero_evento
    v_medido = df.iloc[ev_index]["T_R_m3"]
    chuva_evento = df.iloc[ev_index]["Chuva_evento_mm"]

    def erro(lam):
        return volume_para_lambda(P, S, valid, lam) - v_medido

    # lambda pequeno -> abstracao inicial baixa -> MAIS escoamento (volume maior)
    # lambda grande -> MENOS escoamento (volume menor)
    v_volume_maximo = volume_para_lambda(P, S, valid, 0.001)  # lambda minimo -> volume maximo
    v_volume_minimo = volume_para_lambda(P, S, valid, 0.6)    # lambda maximo -> volume minimo

    if v_medido > v_volume_maximo:
        lam_otimo = np.nan
        obs = f"medido > volume maximo possivel (lambda=0.001 -> {v_volume_maximo:,.0f}) - precisaria de lambda<0.001"
    elif v_medido < v_volume_minimo:
        lam_otimo = np.nan
        obs = f"medido < volume minimo possivel (lambda=0.6 -> {v_volume_minimo:,.0f}) - precisaria de lambda>0.6"
    else:
        lam_otimo = brentq(erro, 0.001, 0.6, xtol=1e-5)
        obs = ""

    resultados.append({
        "evento": numero_evento,
        "T_R_m3_medido": v_medido,
        "Chuva_evento_mm": chuva_evento,
        "lambda_otimo": lam_otimo,
        "obs": obs,
    })

out = pd.DataFrame(resultados)
pd.set_option("display.width", 200)
print(out.to_string(index=False))

validos = out.dropna(subset=["lambda_otimo"])
print(f"\n{len(validos)} de 17 eventos com lambda otimo dentro do range [0.001, 0.6]")
if len(validos) >= 3:
    r = validos["lambda_otimo"].corr(validos["Chuva_evento_mm"])
    print(f"Correlacao lambda_otimo x Chuva_evento_mm: {r:.3f}")

    # ajuste log-linear: lambda = a * Chuva_evento_mm^b
    logx = np.log(validos["Chuva_evento_mm"])
    logy = np.log(validos["lambda_otimo"])
    b, loga = np.polyfit(logx, logy, 1)
    a = np.exp(loga)
    print(f"Ajuste log-log: lambda = {a:.4f} * Chuva_evento_mm ^ {b:.4f}")

    pred = a * validos["Chuva_evento_mm"] ** b
    resid = (pred - validos["lambda_otimo"]) / validos["lambda_otimo"] * 100
    print(f"Erro do ajuste (%) por evento:\n{resid.to_string()}")

out.to_csv(os.path.join(PASTA_DADOS, "lambda_otimo_por_evento.csv"), index=False)
print("\nCSV salvo.")
