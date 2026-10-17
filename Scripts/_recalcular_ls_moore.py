"""Recalcula o fator LS pela formula de Moore e Burch (1986) / Moore et al. (1991),
a partir do MDE CORRIGIDO em UTM (SIRGAS 2000 / 23S), substituindo o `LS Alto.tif`
herdado da IC, que estava em WGS 84 geografico e nao varia com a declividade
(correlacao LS x declividade = 0,047; ver conferencia de 16/10/2026).

    LS = (As/22,13)^0,4 * (sen(beta)/0,0896)^1,3

As = area de contribuicao especifica (m2/m) = area acumulada / largura da celula.
Sem limite, As chega a 4,6 milhoes de m nos pixels de canal (a bacia inteira
drenando por uma celula), o que gera LS absurdo - a USLE descreve erosao de
ENCOSTA, nao de canal. Por isso As e limitado a um comprimento de rampa maximo
(LIMITE_AS, em metros). Ambas as versoes sao geradas e comparadas.

Saidas: Dados Iniciais/LS_moore.tif (com limite) e LS_moore_sem_limite.tif
"""
import os
import numpy as np
from osgeo import gdal

gdal.UseExceptions()
BASE = r"C:\TCC"
DI = os.path.join(BASE, "Dados Iniciais")
QP = os.path.join(DI, "qp_spatial")

LIMITE_AS = 200.0   # m - comprimento de rampa maximo admitido (USLE: dezenas a ~200 m)

# grade de referencia = a dos demais fatores (K, C) e do E_unit
ref = gdal.Open(os.path.join(DI, "K_raster.tif"))
gt = ref.GetGeoTransform()
proj = ref.GetProjection()
NX, NY = ref.RasterXSize, ref.RasterYSize
CELL = abs(gt[1])
bounds = (gt[0], gt[3] + NY * gt[5], gt[0] + NX * gt[1], gt[3])


def warp(caminho, alg=gdal.GRA_Bilinear):
    ds = gdal.Warp("", caminho, format="MEM", width=NX, height=NY, outputBounds=bounds,
                   dstSRS=proj, resampleAlg=alg, dstNodata=-9999)
    a = ds.GetRasterBand(1).ReadAsArray().astype(np.float64)
    ds = None
    return np.where((a != -9999) & np.isfinite(a), a, np.nan)


def le(caminho):
    ds = gdal.Open(caminho)
    b = ds.GetRasterBand(1)
    nd = b.GetNoDataValue()
    a = b.ReadAsArray().astype(np.float64)
    ds = None
    return np.where((a != nd) & np.isfinite(a), a, np.nan)


def salva(caminho, arr):
    out = gdal.GetDriverByName("GTiff").Create(caminho, NX, NY, 1, gdal.GDT_Float32)
    out.SetGeoTransform(gt)
    out.SetProjection(proj)
    b = out.GetRasterBand(1)
    b.WriteArray(np.where(np.isfinite(arr), arr, -9999).astype(np.float32))
    b.SetNoDataValue(-9999)
    b.FlushCache()
    out = None


slope_pct = warp(os.path.join(QP, "slope_pct.tif"))
flowacc_m2 = warp(os.path.join(QP, "flowacc_corrigido.tif"))
LS_velho = le(os.path.join(DI, "LS_raster.tif"))

beta = np.arctan(slope_pct / 100.0)
sin_b = np.sin(beta)
As = flowacc_m2 / CELL

print(f"grade {NY}x{NX}, celula {CELL:.1f} m")
print(f"As (area de contribuicao especifica, m): mediana={np.nanmedian(As):.0f} "
      f"p90={np.nanpercentile(As, 90):.0f} max={np.nanmax(As):,.0f}")
print(f"declividade: media={np.nanmean(slope_pct):.2f}%  "
      f"sen(beta) media={np.nanmean(sin_b):.4f}")

# piso para evitar divisao por zero em pixels planos
sin_b_calc = np.clip(sin_b, 1e-4, None)

LS_sem = (As / 22.13) ** 0.4 * (sin_b_calc / 0.0896) ** 1.3
As_lim = np.clip(As, None, LIMITE_AS)
LS_com = (As_lim / 22.13) ** 0.4 * (sin_b_calc / 0.0896) ** 1.3

ok = np.isfinite(LS_com) & np.isfinite(LS_velho)

print(f"\n{'versao':<28} {'media':>9} {'mediana':>9} {'p95':>9} {'max':>12}")
for nome, arr in (("LS antigo (da IC)", LS_velho),
                  ("LS Moore sem limite", LS_sem),
                  (f"LS Moore (As<={LIMITE_AS:.0f} m)", LS_com)):
    v = arr[ok]
    print(f"{nome:<28} {np.nanmean(v):>9.3f} {np.nanmedian(v):>9.3f} "
          f"{np.nanpercentile(v, 95):>9.3f} {np.nanmax(v):>12,.1f}")

print(f"\nCORRELACAO COM A DECLIVIDADE (o teste que o LS antigo reprovou):")
s = slope_pct[ok]
for nome, arr in (("LS antigo (da IC)", LS_velho),
                  (f"LS Moore (As<={LIMITE_AS:.0f} m)", LS_com)):
    v = arr[ok]
    print(f"  {nome:<28} linear={np.corrcoef(s, v)[0,1]:>6.3f}  "
          f"log={np.corrcoef(np.log(s + 0.01), np.log(np.clip(v, 1e-9, None)))[0,1]:>6.3f}")

print(f"\nLS por faixa de declividade (Moore, As<={LIMITE_AS:.0f} m):")
v = LS_com[ok]
for lo, hi in [(0, 2), (2, 5), (5, 10), (10, 20), (20, 30), (30, 45), (45, 70), (70, 200)]:
    sel = (s >= lo) & (s < hi)
    if sel.sum() > 50:
        print(f"  {lo:>3}-{hi:<4}%  n={sel.sum():>7}  LS medio={v[sel].mean():>7.3f}  "
              f"(antigo {LS_velho[ok][sel].mean():.3f})")

print(f"\ncorrelacao espacial LS novo x LS antigo: "
      f"{np.corrcoef(LS_com[ok], LS_velho[ok])[0,1]:.4f}")

salva(os.path.join(DI, "LS_moore.tif"), np.where(np.isfinite(LS_velho), LS_com, np.nan))
salva(os.path.join(DI, "LS_moore_sem_limite.tif"), np.where(np.isfinite(LS_velho), LS_sem, np.nan))
print(f"\nsalvos: Dados Iniciais/LS_moore.tif e LS_moore_sem_limite.tif")
