"""
Pacote de auditoria do EVENTO 11 - PARTE 3: painel de mapas (PNG) e projeto QGIS.
Roda com python-qgis.bat depois de gerar_pacote_evento11_dados.py.
"""
import os
import pickle
import sys

import numpy as np
import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding="utf-8")
OUT = r"C:\TCC\Evento11_Auditoria"
RAS = os.path.join(OUT, "3_Rasters_QGIS")
SHP = os.path.join(OUT, "2_Shapefiles_QGIS")

with open(os.path.join(OUT, "dados_evento11.pkl"), "rb") as fh:
    D = pickle.load(fh)

masc = gpd.read_file(os.path.join(SHP, "Mascara_Bacia.shp"))
ext = (D["X0"], D["X0"] + D["nx"] * D["dx"], D["Y0"] - D["ny"] * D["dy"], D["Y0"])
est = D["est"]

c_p, c_r = D["c_pura"], D["c_restr"]
SYp = c_p * D["E_grid"]
SYr = c_r * D["Eo_grid"]
paineis = [
    ("Chuva IDW (mm)", D["P_grid"], "Blues", None),
    ("S, retenção CN-I (mm)", D["S_grid"], "YlOrBr", None),
    ("Q, escoamento SCS-CN (mm)", D["Q_grid"], "viridis", None),
    ("pr, vazão de pico local (m³/s)", D["pr_grid"], "magma", None),
    ("E_unit (t/pixel)", D["E_grid"], "YlOrRd", 99.5),
    ("SY previsão pura (t/pixel)", SYp, "YlOrRd", 99.5),
]
fig, axs = plt.subplots(2, 3, figsize=(16, 7.5))
for ax, (tit, arr, cm, pct) in zip(axs.ravel(), paineis):
    a = np.where(np.isfinite(arr), arr, np.nan)
    vmax = np.nanpercentile(a, pct) if pct else np.nanmax(a)
    im = ax.imshow(a, extent=ext, cmap=cm, vmin=np.nanmin(a), vmax=vmax)
    masc.boundary.plot(ax=ax, color="k", lw=0.7)
    ax.scatter(est.x_utm, est.y_utm, c="red", marker="^", s=40, zorder=5)
    ax.set_xlim(ext[0], ext[1]); ax.set_ylim(ext[2], ext[3])
    ax.set_title(tit, fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
    plt.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
fig.suptitle("Evento 11 (04–08/jul/2019): da chuva ao sedimento  (▲ = posto Campo Limpo; o DBT5 fica fora do recorte, a leste; SY previsão pura, c = %.4f)" % c_p, fontsize=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "Evento11_painel_mapas.png"), dpi=130)
print("painel ok")

# ------------------------------------------------------------------
# Projeto QGIS (caminhos relativos)
# ------------------------------------------------------------------
from qgis.core import (QgsApplication, QgsProject, QgsRasterLayer, QgsVectorLayer, QgsCoordinateReferenceSystem,
                       QgsSingleBandPseudoColorRenderer, QgsColorRampShader, QgsRasterShader, QgsStyle,
                       QgsRasterBandStats, QgsPathResolver)

QgsApplication.setPrefixPath(r"C:\Program Files\QGIS 4.2.1\apps\qgis", True)
app = QgsApplication([], False)
app.initQgis()
proj = QgsProject.instance()
proj.setCrs(QgsCoordinateReferenceSystem("EPSG:31983"))
ramp_of = {"ChuvaIDW11": "Blues", "S_CN_I_alinhado": "YlOrBr", "Q11_CN1": "Viridis", "pr11": "Magma",
           "E_unit11": "YlOrRd", "SY11": "YlOrRd", "Q11_CN1_obs": "Viridis", "pr11_obs": "Magma",
           "E_unit11_obs": "YlOrRd", "SY11_obs": "YlOrRd", "K_raster": "YlOrBr", "C_raster": "YlGn", "LS_raster": "Spectral",
           "CN_II_alinhado": "Spectral", "CN_I_alinhado": "Spectral"}
style = QgsStyle.defaultStyle()
rasters = ["ChuvaIDW11", "CN_II_alinhado", "CN_I_alinhado", "S_CN_I_alinhado", "K_raster", "C_raster", "LS_raster",
           "Q11_CN1", "pr11", "E_unit11", "SY11", "Q11_CN1_obs", "pr11_obs", "E_unit11_obs", "SY11_obs"]
ordem = []
for nome in rasters:
    lyr = QgsRasterLayer(os.path.join(RAS, nome + ".tif"), nome)
    if not lyr.isValid():
        print("invalido", nome); continue
    st = lyr.dataProvider().bandStatistics(1, QgsRasterBandStats.All)
    lo, hi = st.minimumValue, st.maximumValue
    if nome.startswith(("E_unit", "SY", "pr")):
        hi = lo + 0.5 * (hi - lo) if nome.startswith(("E_unit", "SY")) else hi
    cr = style.colorRamp(ramp_of.get(nome, "Viridis"))
    sh = QgsColorRampShader(lo, hi, cr, QgsColorRampShader.Interpolated)
    sh.classifyColorRamp(5, 1, lyr.extent(), lyr.dataProvider())
    rs = QgsRasterShader(); rs.setRasterShaderFunction(sh)
    lyr.setRenderer(QgsSingleBandPseudoColorRenderer(lyr.dataProvider(), 1, rs))
    proj.addMapLayer(lyr, False)
    ordem.append(lyr)
vets = ["Pixels_Evento11", "Estacoes_Chuva_Ev11", "drenagem", "UsoSolo_C", "Pedologia_K", "Mascara_Bacia"]
for nome in vets:
    lyr = QgsVectorLayer(os.path.join(SHP, nome + ".shp"), nome, "ogr")
    if not lyr.isValid():
        print("invalido", nome); continue
    proj.addMapLayer(lyr, False)
    ordem.append(lyr)
root = proj.layerTreeRoot()
for lyr in ordem[::-1]:
    node = root.addLayer(lyr)
    node.setItemVisibilityChecked(lyr.name() in ("Mascara_Bacia", "Estacoes_Chuva_Ev11", "SY11", "ChuvaIDW11") and False or lyr.name() in ("Mascara_Bacia", "Estacoes_Chuva_Ev11", "SY11"))
from qgis.core import Qgis
proj.setFilePathStorage(Qgis.FilePathType.Relative)
ok = proj.write(os.path.join(OUT, "Evento11.qgz"))
print("projeto QGIS gravado:", ok)
app.exitQgis()
