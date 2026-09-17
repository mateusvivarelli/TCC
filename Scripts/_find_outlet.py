from osgeo import ogr, gdal
import numpy as np

gdal.UseExceptions()
ogr.UseExceptions()

mask_ds = ogr.Open(r"C:\TCC\Dados Iniciais\Máscara Jundiaí.shp")
mask_layer = mask_ds.GetLayer()
mask_feat = mask_layer.GetNextFeature()
mask_geom = mask_feat.GetGeometryRef()
boundary = mask_geom.GetBoundary()

drain_ds = ogr.Open(r"C:\TCC\Dados Iniciais\drenagem.shp")
drain_layer = drain_ds.GetLayer()

pontos = []
for feat in drain_layer:
    geom = feat.GetGeometryRef()
    if geom is None:
        continue
    inter = geom.Intersection(boundary)
    if inter is None or inter.IsEmpty():
        continue
    gtype = inter.GetGeometryType()
    # coleta pontos (pode ser Point, MultiPoint, ou GeometryCollection)
    if gtype in (ogr.wkbPoint, ogr.wkbPoint25D):
        pontos.append((inter.GetX(), inter.GetY()))
    elif gtype in (ogr.wkbMultiPoint, ogr.wkbGeometryCollection, ogr.wkbMultiPoint25D):
        for i in range(inter.GetGeometryCount()):
            g = inter.GetGeometryRef(i)
            if g.GetGeometryType() in (ogr.wkbPoint, ogr.wkbPoint25D):
                pontos.append((g.GetX(), g.GetY()))

print(f"Pontos de cruzamento drenagem x limite da mascara: {len(pontos)}")
for p in pontos:
    print(p)

# amostra o flow accumulation (grade grande, nativa) em cada ponto
flow_ds = gdal.Open(r"C:\TCC\Dados Iniciais\qp_spatial\flowaccFINAL.sdat")
fgt = flow_ds.GetGeoTransform()
fband = flow_ds.GetRasterBand(1)
farr = fband.ReadAsArray().astype(np.float64)
fnodata = fband.GetNoDataValue()

print("\nFlow accumulation (km2) em cada ponto de cruzamento:")
melhor = None
for (x, y) in pontos:
    col = int((x - fgt[0]) / fgt[1])
    row = int((y - fgt[3]) / fgt[5])
    if 0 <= row < farr.shape[0] and 0 <= col < farr.shape[1]:
        val = farr[row, col]
        area_km2 = val / 1e6 if val != fnodata else float("nan")
    else:
        area_km2 = float("nan")
    print(f"  ({x:.1f}, {y:.1f}) -> linha={row}, coluna={col}, area={area_km2:.4f} km2")
    if not np.isnan(area_km2) and (melhor is None or area_km2 > melhor[2]):
        melhor = (x, y, area_km2)

print("\nMelhor candidato (maior area acumulada) = provavel exutorio principal:")
print(melhor)
