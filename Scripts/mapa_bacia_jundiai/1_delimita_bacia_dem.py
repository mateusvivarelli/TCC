import os, heapq, glob, sys, json
import numpy as np
from osgeo import gdal, ogr, osr
from pyproj import Transformer
gdal.UseExceptions()
sys.stdout.reconfigure(encoding='utf-8')
D = r"C:\Users\user\AppData\Local\Temp\claude\60ed5afc26073541\6f697bf5-4a56-4dbc-a537-266e661ffede\scratchpad\mapa_bacia"
tr = Transformer.from_crs(4326, 31983, always_xy=True)
x0, y0 = tr.transform(-47.65, -23.70); x1, y1 = tr.transform(-46.30, -22.85)
xmin, xmax = min(x0, x1), max(x0, x1) + 0; ymin, ymax = min(y0, y1), max(y0, y1)
RES = 150.0
tiles = glob.glob(D + r"\dem\t_*.tif")
vrt = gdal.BuildVRT(D + r"\dem.vrt", tiles)
ds = gdal.Warp(D + r"\dem_utm.tif", vrt, dstSRS="EPSG:31983", outputBounds=(xmin, ymin, xmax, ymax), xRes=RES, yRes=RES, resampleAlg=gdal.GRA_Bilinear, dstNodata=-9999)
Z = ds.GetRasterBand(1).ReadAsArray().astype(np.float64)
gt = ds.GetGeoTransform(); ny, nx = Z.shape
print("DEM", Z.shape, "min/max", np.nanmin(Z[Z > -9000]), Z.max())
Z[Z < -9000] = np.nan
# ---- preenchimento de depressoes (priority-flood com epsilon)
EPS = 1e-4
F = Z.copy(); nanmask = np.isnan(F)
F[nanmask] = -1e6
closed = np.zeros(Z.shape, bool); heap = []
def edge(i, j):
    return i == 0 or j == 0 or i == ny - 1 or j == nx - 1
for i in range(ny):
    for j in range(nx):
        if edge(i, j):
            heapq.heappush(heap, (F[i, j], i, j)); closed[i, j] = True
nb = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
while heap:
    z, i, j = heapq.heappop(heap)
    for di, dj in nb:
        a, b = i + di, j + dj
        if 0 <= a < ny and 0 <= b < nx and not closed[a, b]:
            closed[a, b] = True
            if F[a, b] <= z:
                F[a, b] = z + EPS
            heapq.heappush(heap, (F[a, b], a, b))
print("depressoes preenchidas")
# ---- direcao D8 (maior declive)
dist = [np.hypot(di, dj) * RES for di, dj in nb]
best = np.full(Z.shape, -1.0); down = np.full(Z.shape, -1, np.int8)
Fp = np.pad(F, 1, mode='constant', constant_values=-1e9)
for k, (di, dj) in enumerate(nb):
    nbz = Fp[1 + di:1 + di + ny, 1 + dj:1 + dj + nx]
    sl = (F - nbz) / dist[k]
    upd = sl > best
    best[upd] = sl[upd]; down[upd] = k
# bordas: escoam para fora
idx = np.arange(ny * nx).reshape(ny, nx)
nxt = np.full(ny * nx, -1, np.int64)
for k, (di, dj) in enumerate(nb):
    sel = down == k
    ii, jj = np.where(sel)
    a, b = ii + di, jj + dj
    ok = (a >= 0) & (a < ny) & (b >= 0) & (b < nx)
    nxt[idx[ii[ok], jj[ok]]] = idx[a[ok], b[ok]]
# ---- acumulacao
order = np.argsort(-F.ravel(), kind='stable')
acc = np.ones(ny * nx)
for c in order:
    n = nxt[c]
    if n >= 0: acc[n] += acc[c]
areakm2 = acc * (RES * RES) / 1e6
np.save(D + r"\nxt.npy", nxt); np.save(D + r"\acc.npy", acc); np.save(D + r"\F.npy", F)
json.dump({"gt": gt, "ny": ny, "nx": nx}, open(D + r"\geo.json", "w"))
# ---- exutorio da parte alta (Campo Limpo Paulista)
ex, ey = tr.transform(-46.760284, -23.208778)
cj = int((ex - gt[0]) / gt[1]); ci = int((ey - gt[3]) / gt[5])
best_c = None; best_a = 0
for i in range(ci - 5, ci + 6):
    for j in range(cj - 5, cj + 6):
        if acc[i * nx + j] > best_a: best_a = acc[i * nx + j]; best_c = (i, j)
print("exutorio: celula", best_c, "area acumulada km2", best_a * RES * RES / 1e6)
# ---- seguir o rio a jusante ate a foz (confluencia com um rio muito maior)
c = best_c[0] * nx + best_c[1]; path = [c]
while True:
    n = nxt[path[-1]]
    if n < 0: break
    path.append(n)
    if len(path) > 20000: break
pa = areakm2[path]
print("trajeto", len(path), "celulas")
foz = None
for k in range(1, len(path) - 1):
    if pa[k + 1] > 3.0 * pa[k] and pa[k + 1] > 1500:
        foz = path[k]; break
if foz is None: foz = path[-1]
fi, fj = divmod(foz, nx)
fx = gt[0] + (fj + 0.5) * gt[1]; fy = gt[3] + (fi + 0.5) * gt[5]
print("foz: celula", (fi, fj), "area km2", areakm2[foz], "utm", fx, fy, "lonlat", Transformer.from_crs(31983, 4326, always_xy=True).transform(fx, fy))
# ---- bacia de contribuicao da foz
mark = np.zeros(ny * nx, bool); mark[foz] = True
for c in order[::-1]:
    n = nxt[c]
    if n >= 0 and mark[n]: mark[c] = True
M = mark.reshape(ny, nx).astype(np.uint8)
print("bacia: celulas", M.sum(), "area km2", M.sum() * RES * RES / 1e6)
drv = gdal.GetDriverByName("MEM"); mds = drv.Create("", nx, ny, 1, gdal.GDT_Byte); mds.SetGeoTransform(gt)
srs = osr.SpatialReference(); srs.ImportFromEPSG(31983); mds.SetProjection(srs.ExportToWkt()); mds.GetRasterBand(1).WriteArray(M)
out = D + r"\bacia_jundiai_total.gpkg"
if os.path.exists(out): os.remove(out)
od = ogr.GetDriverByName("GPKG").CreateDataSource(out); lyr = od.CreateLayer("bacia", srs, ogr.wkbPolygon); lyr.CreateField(ogr.FieldDefn("v", ogr.OFTInteger))
gdal.Polygonize(mds.GetRasterBand(1), mds.GetRasterBand(1), lyr, 0)
od = None
print("ok")
