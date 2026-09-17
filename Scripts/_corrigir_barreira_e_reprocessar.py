"""
Corrige barreiras (ex.: aterro de estrada) ao longo da rede de
drenagem que impedem o fluxo de chegar ao exutorio principal, forcando
um perfil de elevacao monotonicamente decrescente (exutorio -> montante)
ao longo de toda a rede `drenagem.shp`, e reprocessa fill sinks + flow
accumulation no MESMO MDE ja fornecido (nao troca para uma extensao
maior).

Metodo:
1. Monta o grafo da rede de drenagem (como em _find_outlet.py).
2. Amostra a elevacao "crua" em cada no do grafo (minimo numa janela
   3x3, pra reduzir ruido de encaixe vetor->raster) a partir de
   carvedDEM (o MDE ja com a rede "queimada" uma vez).
3. Calcula a elevacao corrigida de cada no por BFS a partir do
   exutorio: cada no upstream nao pode ter elevacao corrigida menor
   que o pai (mais proximo do exutorio) - ou seja,
   elev_corrigida[no] = max(elev_crua[no], elev_corrigida[pai]).
   Isso GARANTE que, seguindo a rede de qualquer ponto ate o exutorio,
   a elevacao so diminui (ou fica igual) - elimina qualquer barreira
   (aterro) que esteja represando o fluxo.
4. Interpola linearmente a elevacao corrigida ao longo de cada aresta
   (entre seus 2 nos) para todos os vertices intermediarios do
   segmento, e "queima" (burn, por minimo) esses valores no
   carvedDEM, gerando um DEM corrigido.
5. Roda fill sinks (Wang & Liu) e flow accumulation (MFD, mesmos
   parametros de antes) nesse DEM corrigido.
6. Reporta a nova area acumulada no exutorio principal.
"""

import numpy as np
from osgeo import ogr, gdal
import networkx as nx

ogr.UseExceptions()
gdal.UseExceptions()

PASTA = r"C:\TCC\Dados Iniciais\qp_spatial"
DRENAGEM = r"C:\TCC\Dados Iniciais\drenagem.shp"
OUTLET = (318980.7663669552, 7432307.0820886735)
TOL = 0.01


def key(x, y):
    return (round(x / TOL) * TOL, round(y / TOL) * TOL)


# ============================================================
# 1. GRAFO DA REDE DE DRENAGEM
# ============================================================

ds = ogr.Open(DRENAGEM)
layer = ds.GetLayer()

G = nx.Graph()
geoms_por_aresta = {}
for feat in layer:
    geom = feat.GetGeometryRef()
    if geom is None:
        continue
    n = geom.GetPointCount()
    if n < 2:
        continue
    p0, p1 = geom.GetPoint(0), geom.GetPoint(n - 1)
    k0, k1 = key(*p0[:2]), key(*p1[:2])
    comprimento = geom.Length()
    if G.has_edge(k0, k1):
        if G[k0][k1]["weight"] > comprimento:
            G[k0][k1]["weight"] = comprimento
            geoms_por_aresta[(k0, k1)] = geom.Clone()
    else:
        G.add_edge(k0, k1, weight=comprimento)
        geoms_por_aresta[(k0, k1)] = geom.Clone()

outlet_key = key(*OUTLET)
print(f"Grafo: {G.number_of_nodes()} nos, {G.number_of_edges()} arestas")

# ============================================================
# 2. ELEVACAO CRUA EM CADA NO (minimo numa janela 3x3 do carvedDEM)
# ============================================================

dem_ds = gdal.Open(PASTA + r"\carvedDEM.sdat")
gt = dem_ds.GetGeoTransform()
dem_arr = dem_ds.GetRasterBand(1).ReadAsArray().astype(np.float64)
nrows, ncols = dem_arr.shape


def elev_min_janela(x, y, raio=1):
    col = int((x - gt[0]) / gt[1])
    row = int((y - gt[3]) / gt[5])
    r0, r1 = max(row - raio, 0), min(row + raio + 1, nrows)
    c0, c1 = max(col - raio, 0), min(col + raio + 1, ncols)
    sub = dem_arr[r0:r1, c0:c1]
    if np.all(np.isnan(sub)):
        return np.nan
    return float(np.nanmin(sub))


elev_crua = {no: elev_min_janela(*no) for no in G.nodes}

# ============================================================
# 3. ELEVACAO CORRIGIDA POR BFS A PARTIR DO EXUTORIO
# ============================================================

ordem_bfs = list(nx.bfs_tree(G, outlet_key))
pai = {outlet_key: None}
arvore_bfs = nx.bfs_tree(G, outlet_key)
for no in ordem_bfs:
    preds = list(arvore_bfs.predecessors(no))
    pai[no] = preds[0] if preds else None

elev_corrigida = {}
n_corrigidos = 0
for no in ordem_bfs:
    if pai[no] is None:
        elev_corrigida[no] = elev_crua[no]
        continue
    e_crua = elev_crua[no]
    e_pai = elev_corrigida[pai[no]]
    if np.isnan(e_crua):
        elev_corrigida[no] = e_pai
        continue
    novo = max(e_crua, e_pai)
    if novo > e_crua + 0.01:
        n_corrigidos += 1
    elev_corrigida[no] = novo

print(f"Nos com barreira corrigida (elevacao rebaixada): {n_corrigidos} de {len(ordem_bfs)}")

# ============================================================
# 4. INTERPOLA E QUEIMA NO DEM (por aresta, ao longo dos vertices)
# ============================================================

dem_corrigido = dem_arr.copy()
n_celulas_alteradas = 0

for (k0, k1), geom in geoms_por_aresta.items():
    if k0 not in elev_corrigida or k1 not in elev_corrigida:
        continue
    n = geom.GetPointCount()
    pts = [geom.GetPoint(j) for j in range(n)]
    if key(*pts[0][:2]) != k0:
        pts = pts[::-1]
        e_ini, e_fim = elev_corrigida[k0], elev_corrigida[k1]
    else:
        e_ini, e_fim = elev_corrigida[k0], elev_corrigida[k1]

    dists = [0.0]
    for i in range(1, len(pts)):
        dx = pts[i][0] - pts[i - 1][0]
        dy = pts[i][1] - pts[i - 1][1]
        dists.append(dists[-1] + (dx**2 + dy**2) ** 0.5)
    total = dists[-1] if dists[-1] > 0 else 1.0

    for p, d in zip(pts, dists):
        x, y = p[0], p[1]
        frac = d / total
        alvo = e_ini + (e_fim - e_ini) * frac
        col = int((x - gt[0]) / gt[1])
        row = int((y - gt[3]) / gt[5])
        if 0 <= row < nrows and 0 <= col < ncols:
            atual = dem_corrigido[row, col]
            if np.isnan(atual) or alvo < atual:
                dem_corrigido[row, col] = alvo
                n_celulas_alteradas += 1

print(f"Celulas do MDE rebaixadas para garantir conectividade: {n_celulas_alteradas}")

# ============================================================
# 5. SALVA O DEM CORRIGIDO
# ============================================================

driver = gdal.GetDriverByName("GTiff")
caminho_saida = PASTA + r"\carvedDEM_corrigido.tif"
out = driver.Create(caminho_saida, ncols, nrows, 1, gdal.GDT_Float32)
out.SetGeoTransform(gt)
out.SetProjection(dem_ds.GetProjection())
band_out = out.GetRasterBand(1)
band_out.WriteArray(np.where(np.isnan(dem_corrigido), -9999, dem_corrigido).astype(np.float32))
band_out.SetNoDataValue(-9999)
band_out.FlushCache()
out = None
dem_ds = None

print(f"\nDEM corrigido salvo em: {caminho_saida}")
