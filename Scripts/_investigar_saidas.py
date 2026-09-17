from osgeo import gdal, ogr
import numpy as np

gdal.UseExceptions()
ogr.UseExceptions()

PASTA = r"C:\TCC\Dados Iniciais"
MASCARA = PASTA + r"\Máscara Jundiaí.shp"

# flow accumulation D8 (recem gerado) - concentra tudo num unico caminho,
# bom pra achar pontos de saida distintos
flow_ds = gdal.Open(PASTA + r"\qp_spatial\flowacc_D8.tif")
gt = flow_ds.GetGeoTransform()
xsize, ysize = flow_ds.RasterXSize, flow_ds.RasterYSize
flow_band = flow_ds.GetRasterBand(1)
flow_arr = flow_band.ReadAsArray().astype(np.float64)
flow_nodata = flow_band.GetNoDataValue()

# rasteriza o poligono da mascara nessa mesma grade
driver = gdal.GetDriverByName("MEM")
mask_ds = driver.Create("", xsize, ysize, 1, gdal.GDT_Byte)
mask_ds.SetGeoTransform(gt)
mask_ds.SetProjection(flow_ds.GetProjection())
mask_vec = ogr.Open(MASCARA)
mask_layer = mask_vec.GetLayer()
gdal.RasterizeLayer(mask_ds, [1], mask_layer, burn_values=[1])
mascara_arr = mask_ds.GetRasterBand(1).ReadAsArray()

dentro = mascara_arr == 1

# ------------------------------------------------------------
# acha pixels de "borda": dentro do poligono mas com pelo menos
# 1 vizinho (dos 8) fora do poligono -> possiveis pontos de saida
# ------------------------------------------------------------
borda = np.zeros_like(dentro)
for dr in (-1, 0, 1):
    for dc in (-1, 0, 1):
        if dr == 0 and dc == 0:
            continue
        vizinho_fora = np.zeros_like(dentro)
        r0, r1 = max(dr, 0), ysize + min(dr, 0)
        c0, c1 = max(dc, 0), xsize + min(dc, 0)
        vizinho_fora[r0:r1, c0:c1] = (mascara_arr[r0-dr:r1-dr, c0-dc:c1-dc] == 0)
        borda |= (dentro & vizinho_fora)

valores_borda = np.where(borda, flow_arr, np.nan)
valido = borda & (flow_arr != flow_nodata) & np.isfinite(flow_arr)

rows, cols = np.where(valido)
vals = flow_arr[valido]
ordem = np.argsort(-vals)  # decrescente

print(f"Total de pixels de borda validos: {valido.sum()}")
print("\nTop 20 pixels de borda com maior flow accumulation (possiveis pontos de saida):")
for i in ordem[:20]:
    r, c = rows[i], cols[i]
    x = gt[0] + (c + 0.5) * gt[1]
    y = gt[3] + (r + 0.5) * gt[5]
    print(f"  linha={r} col={c}  X={x:.1f} Y={y:.1f}  area={vals[i]/1e6:.3f} km2")

# soma de TODOS os pixels de borda cuja area acumulada e razoavelmente grande
# (pra evitar somar ruido de pixels de borda com area=1 celula)
grandes = vals[vals > 900 * 10]  # > 10 celulas
print(f"\nSoma de todos os pixels de borda com area > 9000 m2: {grandes.sum()/1e6:.3f} km2 "
      f"({len(grandes)} pixels)")
