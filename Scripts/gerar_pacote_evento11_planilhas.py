"""
Pacote de auditoria do EVENTO 11 - PARTE 2: planilhas (com formulas vivas).

Le dados_evento11.pkl (parte 1) e escreve em C:/TCC/Evento11_Auditoria/1_Planilhas:

  01_Evento11_Observado_e_Hidrologia.xlsx
      serie horaria -> volume/sedimento observados -> chuva ponderada ->
      SCS-CN concentrado -> hidrograma unitario (Qp)
  02_Evento11_Pixel_a_Pixel.xlsx
      154.667 pixels: IDW -> CN/S -> Q -> pr -> E_unit -> SY (previsao pura
      e volume restrito) + calibracao de c (17 eventos) + metricas

Todas as celulas calculadas sao FORMULAS do Excel (com valor em cache), de
modo que o orientador pode clicar em qualquer celula e ver a conta.

Roda com o Python do QGIS (precisa de xlsxwriter).
"""

import os
import pickle
import sys

import numpy as np
import pandas as pd
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell, xl_col_to_name
from osgeo import gdal

gdal.UseExceptions()
sys.stdout.reconfigure(encoding="utf-8")

BASE = r"C:\TCC"
DI = os.path.join(BASE, "Dados Iniciais")
OUT = os.path.join(BASE, "Evento11_Auditoria")
PLAN = os.path.join(OUT, "1_Planilhas")
os.makedirs(PLAN, exist_ok=True)

with open(os.path.join(OUT, "dados_evento11.pkl"), "rb") as fh:
    D = pickle.load(fh)

LAMBDA = 0.05

# ======================================================================
# DADOS DA PLANILHA 01 (hidrologia)
# ======================================================================
ev_df = pd.read_excel(os.path.join(DI, "eventos_processados_manuais.xlsx"), sheet_name="Sheet1").iloc[:18]
linha = D["linha"]

hor = pd.read_excel(os.path.join(DI, "Dados_finais_histereses_corrigido.xlsx"), sheet_name="Planilha1").iloc[:, :8]
hor.columns = ["Data", "P1", "P2", "Ptot", "Q", "CSS", "Bt", "CSSBt"]
hor["Data"] = pd.to_datetime(hor["Data"])
hor = hor.set_index("Data")
jan = hor.loc[linha["Inicio"]:linha["Fim"]].copy()
NH = len(jan)

# pesos dos postos (minimos quadrados, 17 eventos) - igual ao script da convolucao
p1_17, p2_17, r_17 = [], [], []
for n in range(1, 18):
    r = ev_df.iloc[0 if n == 1 else n]
    p1_17.append(r["chuva_p1_mm"]); p2_17.append(r["chuva_p2_mm"]); r_17.append(r["Chuva_evento_mm"])
p1_17, p2_17, r_17 = map(np.array, (p1_17, p2_17, r_17))
w1 = float(np.sum((p1_17 - p2_17) * (r_17 - p2_17)) / np.sum((p1_17 - p2_17) ** 2))
w1 = min(max(w1, 0.0), 1.0)

# S medio da bacia (CN-1) recortado pela mascara, como no script da convolucao
tmp = os.path.join(OUT, "_s_clip_tmp.tif")
gdal.Warp(tmp, os.path.join(DI, "S - Seco.tif"), format="GTiff",
          cutlineDSName=os.path.join(DI, "Máscara Jundiaí.shp"), cropToCutline=True, dstNodata=-9999)
_ds = gdal.Open(tmp)
_a = _ds.GetRasterBand(1).ReadAsArray().astype(float)
S_MEDIO = float(np.mean(_a[_a != -9999]))
_ds = None
os.remove(tmp)

A_BAC, L_KM, HM = 138.0, 37.587, 147.1
TC_FORMULA = (4 * np.sqrt(A_BAC) + 1.5 * L_KM) / (0.8 * np.sqrt(HM))
TC = 10.652   # valor adotado no script spatialPeakFlowHU_convolucao.py (formula com A, L, Hm arredondados da 10,6536)
FP = 2.08 * 0.5377
DUR = 1.0
TP = DUR / 2 + 0.6 * TC
TB = 2.67 * TP
QPUH = FP * A_BAC / TP
NUH = int(np.ceil(TB)) + 1                  # 20 ordenadas (h = 0..19)
hh = np.arange(NUH)
uh = np.clip(np.where(hh <= TP, QPUH * hh / TP, QPUH * (TB - hh) / (TB - TP)), 0, None)

pb = w1 * jan["P1"].fillna(0).to_numpy() + (1 - w1) * jan["P2"].fillna(0).to_numpy()
pc = np.cumsum(pb)
qc = np.where(pc <= LAMBDA * S_MEDIO, 0.0, (pc - LAMBDA * S_MEDIO) ** 2 / (pc + (1 - LAMBDA) * S_MEDIO))
qi = np.diff(qc, prepend=0.0)
qi_cm = qi / 10
hid = np.convolve(qi_cm, uh)
QP_CALC = float(hid.max())
print(f"w1={w1:.6f}  S_medio={S_MEDIO:.4f}  Tc={TC:.4f}  Tp={TP:.4f}  Tb={TB:.4f}  qpUH={QPUH:.4f}  Qp_calc={QP_CALC:.4f}")
csv_qp = pd.read_csv(os.path.join(DI, "comparacao_qpico_convolucao_medido_vs_calculado.csv"))
print("Qp (csv do projeto) evento 11:", float(csv_qp.loc[csv_qp.evento == 11, "Qp_calc_convolucao"].iloc[0]))

# ======================================================================
# WORKBOOK 01
# ======================================================================
wb = xlsxwriter.Workbook(os.path.join(PLAN, "01_Evento11_Observado_e_Hidrologia.xlsx"))
F = dict(
    h=wb.add_format({"bold": True, "bg_color": "#1F4E78", "font_color": "white", "text_wrap": True, "valign": "top", "border": 1}),
    t=wb.add_format({"bold": True, "font_size": 14}),
    b=wb.add_format({"bold": True}),
    wrap=wb.add_format({"text_wrap": True, "valign": "top"}),
    inp=wb.add_format({"bg_color": "#FFF2CC", "border": 1}),
    inp2=wb.add_format({"bg_color": "#FFF2CC", "border": 1, "num_format": "0.0000"}),
    f2=wb.add_format({"num_format": "0.00"}),
    f3=wb.add_format({"num_format": "0.000"}),
    f4=wb.add_format({"num_format": "0.0000"}),
    f1=wb.add_format({"num_format": "#,##0.0"}),
    f0=wb.add_format({"num_format": "#,##0"}),
    dt=wb.add_format({"num_format": "dd/mm/yyyy hh:mm"}),
    res=wb.add_format({"bold": True, "bg_color": "#E2EFDA", "border": 1, "num_format": "#,##0.00"}),
    res4=wb.add_format({"bold": True, "bg_color": "#E2EFDA", "border": 1, "num_format": "0.0000"}),
    pct=wb.add_format({"num_format": "0.00"}),
    ok=wb.add_format({"bg_color": "#C6EFCE"}),
    aviso=wb.add_format({"bg_color": "#FCE4D6", "text_wrap": True, "valign": "top", "border": 1}),
)

# ---- Roteiro ---------------------------------------------------------
ws = wb.add_worksheet("Roteiro")
ws.set_column("A:A", 120)
txt = [
    ("EVENTO 11 (04-08/jul/2019) - Planilha 01: dados observados e hidrologia", "t"),
    ("", None),
    ("Cores: celula AMARELA = dado de entrada (digitado/copiado das planilhas do projeto); celula VERDE = resultado-chave; demais = formulas do Excel (clique na celula para ver a conta).", "wrap"),
    ("", None),
    ("Abas, na ordem do raciocinio:", "b"),
    ("Evento      - a linha do evento 11 em eventos_processados_manuais.xlsx (todas as colunas) e o que cada uma faz no modelo.", "wrap"),
    ("Serie_horaria - 92 leituras horarias (chuva nos 2 postos, vazao, CSS). Reproduz T_R_m3, SYY_t, SSY_Ris, SSY_Fall e Q_pico da planilha de eventos. Tambem calcula a chuva de bacia, o escoamento SCS-CN concentrado e a separacao de vazao de base.", "wrap"),
    ("Pesos_postos - peso w1 do posto DBT5 (minimos quadrados nos 17 eventos), usado na chuva de bacia.", "wrap"),
    ("HU          - Tc (Giandotti), Tp, Tb e ordenadas do hidrograma unitario triangular do SCS.", "wrap"),
    ("Convolucao  - matriz de convolucao (chuva efetiva x HU) -> hidrograma calculado e Qp. Serve SO para validar o Qp: o Qp NAO alimenta o mapa de sedimentos.", "wrap"),
    ("Checagem    - tabela final: valor da planilha do projeto x valor recalculado aqui.", "wrap"),
    ("", None),
    ("A parte espacial (pixel a pixel) esta na planilha 02.", "b"),
]
for i, (s, f) in enumerate(txt):
    ws.write(i, 0, s, F.get(f))

# ---- Evento ----------------------------------------------------------
ws = wb.add_worksheet("Evento")
ws.set_column("A:A", 28); ws.set_column("B:B", 24); ws.set_column("C:C", 90)
ws.write(0, 0, "Linha do evento 11 em eventos_processados_manuais.xlsx (aba Sheet1, linha de indice 11)", F["t"])
for j, h in enumerate(["Coluna", "Valor", "Uso no modelo"]):
    ws.write(2, j, h, F["h"])
uso_col = {
    "Inicio": "janela do evento (inicio) - recorta a serie horaria",
    "Fim": "janela do evento (fim) - recorta a serie horaria",
    "Q_pico": "Qp MEDIDO (validacao da convolucao HU)",
    "T_R_m3": "volume MEDIDO total (= soma das 92 vazoes horarias x 3600) - usado no fator f do volume restrito",
    "Ris_R_m3": "parcela do volume ate o pico (ramo ascendente)",
    "Fall_R_m3": "parcela do volume apos o pico (ramo descendente)",
    "chuva_p1_mm": "chuva total no posto DBT5 -> IDW",
    "chuva_p2_mm": "chuva total no posto Campo Limpo Paulista -> IDW",
    "Chuva_evento_mm": "R: lamina do evento (media ponderada dos 2 postos) -> denominador de RI/R no calculo de pr",
    "Intensidade_60min_mm/h": "RI: intensidade maxima em 60 min -> numerador de RI/R no calculo de pr",
    "SYY_t": "SY OBSERVADO (t) - alvo da calibracao de c",
    "SSY_Ris_t": "SY observado no ramo ascendente (t)",
    "SSY_Fall_t": "SY observado no ramo descendente (t)",
    "Duracao_horas": "duracao da janela (h)",
    "i60_p1_mm/h": "intensidade 60 min no posto DBT5",
    "i60_p2_mm/h": "intensidade 60 min no posto Campo Limpo Paulista (RI usa o MAIOR dos dois)",
    "Qb_inicio": "vazao de base no inicio do evento (m3/s)",
}
r = 3
for col, val in linha.items():
    if str(col).startswith("Unnamed"):
        continue
    ws.write(r, 0, str(col))
    if isinstance(val, pd.Timestamp):
        ws.write_datetime(r, 1, val.to_pydatetime(), F["dt"])
    elif isinstance(val, str):
        ws.write(r, 1, val)
    elif pd.isna(val):
        ws.write(r, 1, "")
    else:
        ws.write_number(r, 1, float(val), F["inp"] if col in uso_col else None)
    ws.write(r, 2, uso_col.get(col, ""))
    r += 1

# ---- Pesos_postos ----------------------------------------------------
ws = wb.add_worksheet("Pesos_postos")
ws.set_column("A:F", 16)
ws.write(0, 0, "Peso w1 do posto DBT5 na chuva de bacia (minimos quadrados nos 17 eventos)", F["t"])
ws.write(1, 0, "Modelo: R_evento = w1*p1 + (1-w1)*p2  =>  (R-p2) = w1*(p1-p2).  Solucao por minimos quadrados pela origem: w1 = SUM[(p1-p2)(R-p2)] / SUM[(p1-p2)^2].")
for j, h in enumerate(["Evento", "p1 DBT5 (mm)", "p2 CLP (mm)", "R_evento (mm)", "p1-p2", "R-p2", "R estimado (mm)"]):
    ws.write(3, j, h, F["h"])
for i in range(17):
    rr = 4 + i
    ws.write(rr, 0, i + 1)
    ws.write_number(rr, 1, float(p1_17[i]), F["inp"]); ws.write_number(rr, 2, float(p2_17[i]), F["inp"])
    ws.write_number(rr, 3, float(r_17[i]), F["inp"])
    ws.write_formula(rr, 4, f"=B{rr+1}-C{rr+1}", F["f3"], float(p1_17[i] - p2_17[i]))
    ws.write_formula(rr, 5, f"=D{rr+1}-C{rr+1}", F["f3"], float(r_17[i] - p2_17[i]))
    ws.write_formula(rr, 6, f"=$B$24*B{rr+1}+(1-$B$24)*C{rr+1}", F["f3"], float(w1 * p1_17[i] + (1 - w1) * p2_17[i]))
ws.write(22, 0, "Calculo de w1", F["b"])
ws.write(23, 0, "w1 (DBT5)")
ws.write_formula(23, 1, "=MIN(MAX(SUMPRODUCT(E5:E21,F5:F21)/SUMSQ(E5:E21),0),1)", F["res4"], w1)
ws.write(24, 0, "1 - w1 (CLP)")
ws.write_formula(24, 1, "=1-B24", F["res4"], 1 - w1)
ws.write(25, 0, "Obs.: para o evento 11, w1*62,8 + (1-w1)*79,0 reproduz Chuva_evento_mm = 74,0396 (ver aba Checagem).")
wb.define_name("w1_DBT5", "=Pesos_postos!$B$24")

# ---- Serie_horaria ---------------------------------------------------
ws = wb.add_worksheet("Serie_horaria")
hdr = ["Data/hora", "P DBT5 (mm/h)", "P Campo Limpo (mm/h)", "Q medida (m3/s)", "CSS (mg/L)", "Q base Bt (m3/s)",
       "Volume na hora (m3) = Q*3600", "Carga na hora (t) = Q*CSS*3600/1e6", "Ramo (asc ate o pico, desc depois)",
       "P bacia (mm) = w1*P1+(1-w1)*P2", "P acumulada (mm)", "Q SCS acumulado (mm)", "Q SCS incremental (mm)",
       "Q SCS incremental (cm)", "Escoamento direto medido (m3) = (Q-Bt)*3600"]
for j, h in enumerate(hdr):
    ws.write(0, j, h, F["h"])
ws.set_row(0, 60)
ws.set_column("A:A", 17); ws.set_column("B:O", 15)
ws.freeze_panes(1, 1)
FIRST, LAST = 2, NH + 1   # linhas Excel
Qv = jan["Q"].to_numpy(float); Cv = jan["CSS"].to_numpy(float); Bv = jan["Bt"].to_numpy(float)
ipk = int(np.argmax(Qv))
for i in range(NH):
    rr = i + 1; xr = rr + 1
    ws.write_datetime(rr, 0, jan.index[i].to_pydatetime(), F["dt"])
    ws.write_number(rr, 1, float(jan["P1"].iloc[i]), F["inp"])
    ws.write_number(rr, 2, float(jan["P2"].iloc[i]), F["inp"])
    ws.write_number(rr, 3, float(Qv[i]), F["inp"])
    ws.write_number(rr, 4, float(Cv[i]), F["inp"])
    ws.write_number(rr, 5, float(Bv[i]), F["inp"])
    ws.write_formula(rr, 6, f"=D{xr}*3600", F["f1"], Qv[i] * 3600)
    ws.write_formula(rr, 7, f"=D{xr}*E{xr}*3600/1000000", F["f3"], Qv[i] * Cv[i] * 3600 / 1e6)
    ws.write_formula(rr, 8, f'=IF(A{xr}<=$R$8,"asc","desc")', None, "asc" if i <= ipk else "desc")
    ws.write_formula(rr, 9, f"=w1_DBT5*B{xr}+(1-w1_DBT5)*C{xr}", F["f3"], pb[i])
    ws.write_formula(rr, 10, f"=SUM(J${FIRST}:J{xr})", F["f3"], pc[i])
    ws.write_formula(rr, 11, f"=IF(K{xr}<=$R$4*$R$5,0,(K{xr}-$R$4*$R$5)^2/(K{xr}+(1-$R$4)*$R$5))", F["f4"], qc[i])
    ws.write_formula(rr, 12, f"=L{xr}" if i == 0 else f"=L{xr}-L{xr-1}", F["f4"], qi[i])
    ws.write_formula(rr, 13, f"=M{xr}/10", F["f4"], qi_cm[i])
    ws.write_formula(rr, 14, f"=(D{xr}-F{xr})*3600", F["f1"], (Qv[i] - Bv[i]) * 3600)

rng = lambda c: f"${c}${FIRST}:${c}${LAST}"
# bloco de parametros e resultados (colunas Q:S)
ws.set_column("Q:Q", 52); ws.set_column("R:R", 16); ws.set_column("S:S", 60)
ws.write(0, 16, "Parametros e resultados", F["h"]); ws.write(0, 17, "Valor", F["h"]); ws.write(0, 18, "Comentario", F["h"])
rows = []
def put(r, nome, formula, val, com="", fmt=None, inp=False):
    ws.write(r, 16, nome)
    if formula is None:
        ws.write_number(r, 17, val, F["inp2"] if inp else fmt)
    else:
        ws.write_formula(r, 17, formula, fmt or F["res"], val)
    ws.write_string(r, 18, com)

put(2, "w1 (peso DBT5)", "=w1_DBT5", w1, "aba Pesos_postos", F["f4"])
put(3, "lambda (Ia = lambda*S)", None, LAMBDA, "adotado: 0,05 (calibrado; ver notas)", inp=True)
put(4, "S medio da bacia, CN-I (mm)", None, S_MEDIO, "media do raster S - Seco recortado pela mascara (script spatialPeakFlowHU_convolucao.py)", inp=True)
put(6, "Q medida maxima (m3/s)", f"=MAX({rng('D')})", float(Qv.max()), "igual ao Q_pico da planilha de eventos")
put(7, "Data/hora do pico", f"=INDEX({rng('A')},MATCH(MAX({rng('D')}),{rng('D')},0))", 0.0, "", F["dt"])
ws.write_formula(7, 17, f"=INDEX({rng('A')},MATCH(MAX({rng('D')}),{rng('D')},0))", F["dt"], (jan.index[ipk] - pd.Timestamp("1899-12-30")).total_seconds() / 86400)
put(8, "Numero de leituras horarias", f"=COUNT({rng('D')})", NH, "91 intervalos de 1 h, 92 pontos")
put(9, "Soma da chuva DBT5 (mm)", f"=SUM({rng('B')})", float(jan['P1'].sum()), "planilha: chuva_p1_mm = 62,800003")
put(10, "Soma da chuva Campo Limpo (mm)", f"=SUM({rng('C')})", float(jan['P2'].sum()), "planilha: chuva_p2_mm = 79,000002")
put(11, "Chuva de bacia, soma (mm) = R", f"=SUM({rng('J')})", float(pb.sum()), "planilha: Chuva_evento_mm = 74,039628")
put(12, "Volume total medido T_R (m3) = soma(Q)*3600", f"=SUM({rng('G')})", float((Qv * 3600).sum()), "planilha: T_R_m3 = 2.436.681,6  (INCLUI vazao de base!)")
put(13, "Ris_R (m3): ate o pico", f'=SUMIF({rng("I")},"asc",{rng("G")})', float((Qv[:ipk+1]*3600).sum()), "planilha: Ris_R_m3 = 1.283.688,0")
put(14, "Fall_R (m3): depois do pico", f'=SUMIF({rng("I")},"desc",{rng("G")})', float((Qv[ipk+1:]*3600).sum()), "planilha: Fall_R_m3 = 1.152.993,6")
put(15, "SY observado SYY_t (t) = soma(Q*CSS*3600/1e6)", f"=SUM({rng('H')})", float((Qv*Cv*3600/1e6).sum()), "planilha: SYY_t = 1.821,7535 (carga TOTAL: inclui sedimento da vazao de base)")
put(16, "SSY_Ris (t): ate o pico", f'=SUMIF({rng("I")},"asc",{rng("H")})', float((Qv[:ipk+1]*Cv[:ipk+1]*3600/1e6).sum()), "planilha: SSY_Ris_t = 1.239,8365")
put(17, "SSY_Fall (t): depois do pico", f'=SUMIF({rng("I")},"desc",{rng("H")})', float((Qv[ipk+1:]*Cv[ipk+1:]*3600/1e6).sum()), "planilha: SSY_Fall_t = 581,9170")
put(19, "Volume da vazao de base Bt (m3) = soma(Bt)*3600", f"=SUM({rng('F')})*3600", float(Bv.sum()*3600), "Bt = linha de base da serie (separacao feita pelos autores dos dados)")
put(20, "Escoamento direto medido (m3) = soma(Q-Bt)*3600", f"=SUM({rng('O')})", float(((Qv-Bv)*3600).sum()), "")
put(21, "Fracao do T_R que e vazao de base", "=R20/R13", float(Bv.sum()*3600/((Qv*3600).sum())), "ATENCAO: o T_R_m3 usado como 'volume medido' contem vazao de base", F["res4"])
put(23, "Chuva de bacia acumulada final (mm)", f"=K{LAST}", float(pc[-1]), "")
put(24, "Escoamento SCS-CN concentrado total (mm)", f"=L{LAST}", float(qc[-1]), "usando S medio e P de bacia (visao concentrada)")
put(25, "Escoamento SCS-CN concentrado (m3) = mm/1000*138 km2", f"=R25/1000*138*1000000", float(qc[-1]/1000*138e6), "so para comparar com o espacializado (IDW pixel a pixel)")
ws.write(27, 16, "Leitura do aviso:", F["b"])
ws.merge_range(28, 16, 33, 18,
               "T_R_m3 (planilha) = soma das 92 vazoes horarias x 3600, ou seja, volume TOTAL escoado no exutorio, que inclui a vazao de base. "
               "O SCS-CN calcula apenas o escoamento DIRETO. Para o evento 11: total 2,437 milhoes m3; vazao de base (Bt) ~0,96 milhao m3; "
               "direto ~1,479 milhao m3. Ver o impacto no fator f do volume restrito na planilha 02 e no texto da conversa.",
               F["aviso"])

# grafico
ch = wb.add_chart({"type": "column"})
ch.add_series({"name": "P bacia (mm/h)", "categories": f"=Serie_horaria!$A${FIRST}:$A${LAST}", "values": f"=Serie_horaria!$J${FIRST}:$J${LAST}", "y2_axis": True, "fill": {"color": "#9DC3E6"}})
ln = wb.add_chart({"type": "line"})
ln.add_series({"name": "Q medida (m3/s)", "categories": f"=Serie_horaria!$A${FIRST}:$A${LAST}", "values": f"=Serie_horaria!$D${FIRST}:$D${LAST}", "line": {"color": "#C00000"}})
ln.add_series({"name": "Q base Bt (m3/s)", "categories": f"=Serie_horaria!$A${FIRST}:$A${LAST}", "values": f"=Serie_horaria!$F${FIRST}:$F${LAST}", "line": {"color": "#7F7F7F", "dash_type": "dash"}})
ch.combine(ln)
ch.set_title({"name": "Evento 11: chuva de bacia e vazao"})
ch.set_size({"width": 900, "height": 320})
ch.set_x_axis({"date_axis": False, "num_format": "dd/mm hh", "interval_unit": 12})
ch.set_y2_axis({"name": "mm/h", "reverse": True})
ch.set_y_axis({"name": "m3/s"})
ws.insert_chart(36, 16, ch)

# ---- HU --------------------------------------------------------------
wh = wb.add_worksheet("HU")
wh.set_column("A:A", 46); wh.set_column("B:B", 16); wh.set_column("C:C", 70)
wh.write(0, 0, "Hidrograma unitario triangular do SCS (D = 1 h)", F["t"])
hp = [
    ("A, area da bacia (km2)", None, A_BAC, "area adotada nos scripts (138)"),
    ("L, comprimento do talvegue (km)", None, L_KM, "medido no MDE/drenagem"),
    ("Hm, altitude media (m)", None, HM, ""),
    ("Tc Giandotti adotado (h)", None, TC, "valor usado no script (10,652). Formula: Tc=(4*raiz(A)+1,5*L)/(0,8*raiz(Hm)); com A, L e Hm arredondados acima da 10,6536 (celula D6)"),
    ("D, duracao unitaria (h)", None, DUR, "passo horario dos dados"),
    ("Tp = D/2 + 0,6*Tc (h)", "=B7/2+0.6*B6", TP, "tempo de pico"),
    ("Tb = 2,67*Tp (h)", "=2.67*B8", TB, "tempo de base do triangulo SCS"),
    ("Fator de pico (2,08*0,5377)", "=2.08*0.5377", FP, "2,08 e o padrao SCS; 0,5377 e o fator de reducao calibrado nos 17 eventos"),
    ("qp do HU (m3/s por cm) = fator*A/Tp", "=B10*B3/B8", QPUH, "ordenada de pico do HU para 1 cm de chuva efetiva"),
    ("Numero de ordenadas (h = 0..ceil(Tb))", "=ROUNDUP(B9,0)+1", NUH, ""),
]
for i, (nome, fml, val, com) in enumerate(hp):
    rr = 2 + i
    wh.write(rr, 0, nome)
    if fml is None:
        wh.write_number(rr, 1, val, F["inp2"])
    else:
        wh.write_formula(rr, 1, fml, F["res4"], val)
    wh.write(rr, 2, com)
wh.write_formula(5, 3, "=(4*SQRT(B3)+1.5*B4)/(0.8*SQRT(B5))", F["f4"], TC_FORMULA)
wh.write(14, 0, "Ordenadas do HU", F["b"])
wh.write(15, 0, "h (horas)", F["h"]); wh.write(15, 1, "u(h) (m3/s por cm)", F["h"])
for k in range(NUH):
    wh.write(16 + k, 0, k)
    wh.write_formula(16 + k, 1, f"=IF(A{17+k}<=$B$8,$B$11*A{17+k}/$B$8,MAX($B$11*($B$9-A{17+k})/($B$9-$B$8),0))", F["f4"], float(uh[k]))
wh.write(16 + NUH + 1, 0, "Soma das ordenadas (m3/s*h por cm) - mede quanto do volume unitario o triangulo carrega")
wh.write_formula(16 + NUH + 1, 1, f"=SUM(B17:B{16+NUH})", F["f4"], float(uh.sum()))
wh.write(16 + NUH + 2, 0, "Volume unitario ideal da bacia (m3/s*h por cm) = A*10/3,6")
wh.write_formula(16 + NUH + 2, 1, "=B3*10/3.6", F["f4"], A_BAC * 10 / 3.6)
wh.write(16 + NUH + 3, 0, "Fracao do volume unitario retida pelo HU (=~54%: o fator de pico e um fator de escala empirico)")
wh.write_formula(16 + NUH + 3, 1, f"=B{16+NUH+2}/B{16+NUH+3}", F["res4"], float(uh.sum() / (A_BAC * 10 / 3.6)))
wb.define_name("HU_ord", f"=HU!$B$17:$B${16+NUH}")

# ---- Convolucao ------------------------------------------------------
wc = wb.add_worksheet("Convolucao")
NK = NH + NUH - 1
wc.write(0, 0, "Convolucao: hidrograma(k) = soma_j [ chuva efetiva incremental(j) em cm  x  u(k-j) ]", F["t"])
wc.write(1, 0, "Linha j = hora da chuva efetiva; coluna k = hora do hidrograma. Cada celula = incremento(j) x u(k-j) quando 0 <= k-j <= 19. A linha 'Q total' soma cada coluna.")
wc.set_column(0, 0, 8); wc.set_column(1, 1, 12); wc.set_column(2, 2 + NK, 7)
wc.write(3, 0, "j", F["h"]); wc.write(3, 1, "ef (cm)", F["h"])
HR = 4  # linha (0-based) do cabecalho de k
wc.write(HR - 1, 0, "k ->")
for k in range(NK):
    wc.write(HR, 2 + k, k, F["h"])
for j in range(NH):
    rr = HR + 1 + j
    wc.write(rr, 0, j)
    wc.write_formula(rr, 1, f"=Serie_horaria!N{FIRST+j}", F["f4"], float(qi_cm[j]))
    for k in range(NK):
        kk = k - j
        val = float(qi_cm[j] * uh[kk]) if 0 <= kk < NUH else 0.0
        cell_k = f"{xl_col_to_name(2+k)}${HR+1}"
        wc.write_formula(rr, 2 + k, f"=IF(AND({cell_k}-$A{rr+1}>=0,{cell_k}-$A{rr+1}<={NUH-1}),INDEX(HU_ord,{cell_k}-$A{rr+1}+1)*$B{rr+1},0)", F["f2"], val)
rt = HR + 1 + NH
wc.write(rt, 0, "Q total", F["b"])
c0, c1 = xl_col_to_name(2), xl_col_to_name(2 + NK - 1)
for k in range(NK):
    col = xl_col_to_name(2 + k)
    wc.write_formula(rt, 2 + k, f"=SUM({col}{HR+2}:{col}{HR+1+NH})", F["f2"], float(hid[k]))
wc.write(rt + 2, 0, "Qp calculado (m3/s) = MAX(Q total)", F["b"])
wc.write_formula(rt + 2, 5, f"=MAX({c0}{rt+1}:{c1}{rt+1})", F["res"], QP_CALC)
wb.define_name("Qp_calc", f"=Convolucao!$F${rt+3}")
wc.freeze_panes(HR + 1, 2)

# ---- Checagem --------------------------------------------------------
wk = wb.add_worksheet("Checagem")
wk.set_column("A:A", 56); wk.set_column("B:E", 20)
wk.write(0, 0, "Valores da planilha do projeto x recalculados nesta planilha", F["t"])
for j, h in enumerate(["Grandeza", "Planilha do projeto", "Recalculado aqui", "Diferenca", "Dif. %"]):
    wk.write(2, j, h, F["h"])
chk = [
    ("Chuva DBT5 (mm)", float(linha["chuva_p1_mm"]), "=Serie_horaria!R10", float(jan["P1"].sum())),
    ("Chuva Campo Limpo (mm)", float(linha["chuva_p2_mm"]), "=Serie_horaria!R11", float(jan["P2"].sum())),
    ("Chuva de bacia R (mm)", float(linha["Chuva_evento_mm"]), "=Serie_horaria!R12", float(pb.sum())),
    ("T_R_m3 (m3)", float(linha["T_R_m3"]), "=Serie_horaria!R13", float((Qv * 3600).sum())),
    ("Ris_R_m3 (m3)", float(linha["Ris_R_m3"]), "=Serie_horaria!R14", float((Qv[:ipk+1] * 3600).sum())),
    ("Fall_R_m3 (m3)", float(linha["Fall_R_m3"]), "=Serie_horaria!R15", float((Qv[ipk+1:] * 3600).sum())),
    ("SYY_t (t)", float(linha["SYY_t"]), "=Serie_horaria!R16", float((Qv*Cv*3600/1e6).sum())),
    ("SSY_Ris_t (t)", float(linha["SSY_Ris_t"]), "=Serie_horaria!R17", float((Qv[:ipk+1]*Cv[:ipk+1]*3600/1e6).sum())),
    ("SSY_Fall_t (t)", float(linha["SSY_Fall_t"]), "=Serie_horaria!R18", float((Qv[ipk+1:]*Cv[ipk+1:]*3600/1e6).sum())),
    ("Q_pico medido (m3/s)", float(linha["Q_pico"]), "=Serie_horaria!R7", float(Qv.max())),
    ("Qp calculado (convolucao HU) x Qp do CSV do projeto (m3/s)", float(csv_qp.loc[csv_qp.evento == 11, "Qp_calc_convolucao"].iloc[0]), "=Qp_calc", QP_CALC),
]
for i, (nome, plan, fml, val) in enumerate(chk):
    rr = 3 + i
    wk.write(rr, 0, nome)
    wk.write_number(rr, 1, plan, F["inp2"])
    wk.write_formula(rr, 2, fml, F["f4"], val)
    wk.write_formula(rr, 3, f"=C{rr+1}-B{rr+1}", F["f4"], val - plan)
    wk.write_formula(rr, 4, f"=IF(B{rr+1}=0,0,D{rr+1}/B{rr+1}*100)", F["f4"], (val - plan) / plan * 100)
rr = 3 + len(chk) + 1
wk.write(rr, 0, "Qp calculado x medido: erro %", F["b"])
wk.write_formula(rr, 1, f"=(Qp_calc-{float(linha['Q_pico'])})/{float(linha['Q_pico'])}*100", F["res"], (QP_CALC - float(linha['Q_pico'])) / float(linha['Q_pico']) * 100)
wb.close()
print("planilha 01 ok")
if "so01" in sys.argv:
    sys.exit(0)

# ======================================================================
# WORKBOOK 02 - pixel a pixel
# ======================================================================
TESTE = "teste" in sys.argv
if TESTE:
    for _k in ["iy","ix","P","CN2","CN1","S","solo","usoc","K","C","LS","valido","Q","pr","E","SY","Qo","pro","Eo","SYo"]:
        D[_k] = D[_k][:300]
N = len(D["iy"])
est = D["est"]
wb = xlsxwriter.Workbook(os.path.join(PLAN, "02_Evento11_Pixel_a_Pixel_TESTE.xlsx" if "teste" in sys.argv else "02_Evento11_Pixel_a_Pixel.xlsx"), {"constant_memory": True})
G = dict(
    h=wb.add_format({"bold": True, "bg_color": "#1F4E78", "font_color": "white", "text_wrap": True, "valign": "top", "border": 1}),
    t=wb.add_format({"bold": True, "font_size": 14}),
    b=wb.add_format({"bold": True}),
    wrap=wb.add_format({"text_wrap": True, "valign": "top"}),
    inp=wb.add_format({"bg_color": "#FFF2CC", "border": 1}),
    inp6=wb.add_format({"bg_color": "#FFF2CC", "border": 1, "num_format": "0.000000"}),
    inp_big=wb.add_format({"bg_color": "#FFF2CC", "border": 1, "num_format": "#,##0.0000"}),
    f1=wb.add_format({"num_format": "#,##0.0"}),
    f2=wb.add_format({"num_format": "0.00"}),
    f4=wb.add_format({"num_format": "0.0000"}),
    f6=wb.add_format({"num_format": "0.000000"}),
    f8=wb.add_format({"num_format": "0.00000000"}),
    sci=wb.add_format({"num_format": "0.000E+00"}),
    res=wb.add_format({"bold": True, "bg_color": "#E2EFDA", "border": 1, "num_format": "#,##0.0000"}),
    res6=wb.add_format({"bold": True, "bg_color": "#E2EFDA", "border": 1, "num_format": "0.000000"}),
    hi=wb.add_format({"bg_color": "#FFFF99", "num_format": "0.000"}),
    hib=wb.add_format({"bg_color": "#FFFF99", "bold": True}),
    hi4=wb.add_format({"bg_color": "#FFFF99", "num_format": "#,##0.0000"}),
    hi1=wb.add_format({"bg_color": "#FFFF99", "num_format": "0.0"}),
)
# ordem das abas (constant_memory exige escrever cada aba por vez, mas a ordem de criacao define a ordem final)
w_rot = wb.add_worksheet("Roteiro")
w_par = wb.add_worksheet("Parametros")
w_cls = wb.add_worksheet("Classes")
w_pix = wb.add_worksheet("Pixels")
w_res = wb.add_worksheet("Resumo")
w_cal = wb.add_worksheet("Calibracao_c")
w_con = wb.add_worksheet("Conferencia")

PIX_FIRST, PIX_LAST = 2, N + 1


def pr_(c):
    return f"Pixels!${c}${PIX_FIRST}:${c}${PIX_LAST}"


# ---- Parametros ------------------------------------------------------
ws = w_par
ws.set_column("A:A", 34); ws.set_column("B:B", 22); ws.set_column("C:C", 16); ws.set_column("D:D", 100)
ws.write(0, 0, "Parametros do evento 11 (celula amarela = entrada; verde = resultado de outra aba)", G["t"])
for j, h in enumerate(["Nome (usado nas formulas)", "Valor", "Unidade", "Origem / significado"]):
    ws.write(2, j, h, G["h"])
tabK, tabC = D["tab_K"], D["tab_C"]
fvol = D["f"]
sumE, sumEo = float(np.nansum(D["E"])), float(np.nansum(D["Eo"]))
_cmp = D["cmp_csv"]
_SY17 = _cmp["SY_obs_t"].to_numpy(float)
_Ep = _cmp["soma_E_unit_previsao_t"].to_numpy(float).copy(); _Er = _cmp["soma_E_unit_restrito_t"].to_numpy(float).copy()
_Ep[10] = sumE; _Er[10] = sumEo
c_pura = float(np.sum(_Ep * _SY17) / np.sum(_Ep ** 2)); c_restr = float(np.sum(_Er * _SY17) / np.sum(_Er ** 2))
D["SY"] = c_pura * D["E"]; D["SYo"] = c_restr * D["Eo"]
params = [
    ("p_lambda", LAMBDA, "-", "Ia = lambda*S (razao de abstracao inicial). 0,05 em vez do classico 0,2 (calibracao do projeto; Valle Junior et al. 2019; Brandao 2025).", "inp"),
    ("dx_pix", D["dx"], "m", "tamanho do pixel em X (grade 884 x 365 do raster CN, SIRGAS 2000 / UTM 23S)", "inp_big"),
    ("dy_pix", D["dy"], "m", "tamanho do pixel em Y", "inp_big"),
    ("A_pixel", None, "m2", "area do pixel = dx*dy (897,49 m2; NAO 900)", "f"),
    ("X0_canto", D["X0"], "m", "coordenada X do canto superior esquerdo da grade", "inp_big"),
    ("Y0_canto", D["Y0"], "m", "coordenada Y do canto superior esquerdo da grade", "inp_big"),
    ("x_DBT5", float(est.x_utm[0]), "m", "posto Desemboque do Tunel 5 (lon -46,4809 / lat -23,2646) reprojetado para UTM 23S (QGIS: Reprojetar camada, EPSG:4326 -> 31983)", "inp_big"),
    ("y_DBT5", float(est.y_utm[0]), "m", "idem", "inp_big"),
    ("x_CLP", float(est.x_utm[1]), "m", "posto Rio Jundiai em Campo Limpo Paulista (lon -46,760284 / lat -23,208778) reprojetado", "inp_big"),
    ("y_CLP", float(est.y_utm[1]), "m", "idem", "inp_big"),
    ("P_DBT5", float(est.P[0]), "mm", "chuva total do evento no posto DBT5 (planilha de eventos: chuva_p1_mm)", "inp6"),
    ("P_CLP", float(est.P[1]), "mm", "chuva total do evento no posto Campo Limpo (chuva_p2_mm)", "inp6"),
    ("RI_mmh", D["RI"], "mm/h", "intensidade maxima de 60 min do evento = MAIOR entre os 2 postos (11,8 no DBT5; 9,4 no CLP)", "inp6"),
    ("R_evento_mm", D["R_EV"], "mm", "lamina de chuva do evento = 0,3068*62,8 + 0,6932*79,0 (aba Pesos_postos da planilha 01)", "inp6"),
    ("V_med_m3", D["V_MED"], "m3", "volume medido T_R_m3 (planilha de eventos) = soma das 92 vazoes horarias x 3600 (inclui vazao de base)", "inp_big"),
    ("SY_obs_t", D["SY_OBS"], "t", "SY observado do evento (SYY_t) = soma(Q*CSS*3600/1e6)", "inp_big"),
    ("coef_W", 11.8, "-", "coeficiente de Williams (1975) da MUSLE: 11,8 (SI: t, m3, m3/s)", "inp"),
    ("exp_M", 0.56, "-", "expoente de Williams (1975): 0,56", "inp"),
    ("fator_P", 1.0, "-", "pratica conservacionista: P = 1 (sem praticas) na bacia toda", "inp"),
    ("fator_f", None, "-", "f = V_med / V_calc (aba Resumo). Reescala Q para o volume medido (variante 'volume restrito')", "link"),
    ("c_pura", None, "-", "c da previsao pura (aba Calibracao_c): SY = c * E_unit", "link"),
    ("c_restr", None, "-", "c do volume restrito (aba Calibracao_c)", "link"),
]
pname = {}
for i, (nome, val, un, com, tipo) in enumerate(params):
    rr = 3 + i
    pname[nome] = f"=Parametros!$B${rr+1}"
    ws.write(rr, 0, nome)
    if nome == "A_pixel":
        ws.write_formula(rr, 1, "=B5*B6", G["res6"], D["A_pix"])
    elif nome == "fator_f":
        ws.write_formula(rr, 1, "=Resumo!B13", G["res6"], fvol)
    elif nome == "c_pura":
        ws.write_formula(rr, 1, "=Calibracao_c!B22", G["res6"], c_pura)
    elif nome == "c_restr":
        ws.write_formula(rr, 1, "=Calibracao_c!L22", G["res6"], c_restr)
    else:
        ws.write_number(rr, 1, float(val), G[tipo] if tipo in G else G["inp"])
    ws.write(rr, 2, un); ws.write(rr, 3, com)
    wb.define_name(nome, f"=Parametros!$B${rr+1}")

# ---- Classes ---------------------------------------------------------
ws = w_cls
ws.set_column("A:A", 36); ws.set_column("B:B", 12); ws.set_column("C:C", 14); ws.set_column("D:D", 70)
ws.write(0, 0, "Tabelas de classe -> fator (K e C) e origem do LS", G["t"])
ws.write(2, 0, "K - erodibilidade (t.h/MJ/mm). Origem: Pedologia Alto.shp, campo Valor (Plano de Bacias, Consorcio Profill-Rhama 2020; valores por classe da IC)", G["b"])
for j, h in enumerate(["Classe de solo (campo Subordem)", "K", "Pixels (COUNTIF)", "Observacao"]):
    ws.write(3, j, h, G["h"])
cnt_solo = pd.Series(D["solo"]).value_counts()
cnt_uso = pd.Series(D["usoc"]).value_counts()
for i, rw in tabK.iterrows():
    rr = 4 + i
    ws.write(rr, 0, rw["Subordem"]); ws.write_number(rr, 1, float(rw["first"]), G["inp"])
    ws.write_formula(rr, 2, f'=COUNTIF({pr_("L")},A{rr+1})', None, int(cnt_solo.get(rw["Subordem"], 0)))
    if rw["Subordem"] == "Área Urbana":
        ws.write(rr, 3, "K = 0: area urbana nao produz erosao no modelo (e tambem zera qualquer pixel sobreposto)")
nK = len(tabK)
wb.define_name("Classes_K", f"=Classes!$A$5:$B${4+nK}")
r0 = 4 + nK + 2
ws.write(r0, 0, "C - uso e manejo (-). Origem: Uso Solo Alto.shp, campo Valor (Plano de Bacias 2020; valores da IC)", G["b"])
for j, h in enumerate(["Classe de uso (campo CLASSE)", "C", "Pixels (COUNTIF)", "Observacao"]):
    ws.write(r0 + 1, j, h, G["h"])
for i, rw in tabC.iterrows():
    rr = r0 + 2 + i
    ws.write(rr, 0, rw["CLASSE"]); ws.write_number(rr, 1, float(rw["first"]), G["inp"])
    ws.write_formula(rr, 2, f'=COUNTIF({pr_("N")},A{rr+1})', None, int(cnt_uso.get(rw["CLASSE"], 0)))
    if rw["CLASSE"] in ("Área Urbanizada", "Corpos D'Água"):
        ws.write(rr, 3, "C = 0: sem erosao (urbano / agua)")
nC = len(tabC)
wb.define_name("Classes_C", f"=Classes!$A${r0+3}:$B${r0+2+nC}")
rr = r0 + 2 + nC + 1
ws.write(rr, 0, "LS - fator topografico", G["b"])
ws.write(rr + 1, 0, "Nao e recalculado nesta planilha: vem de LS_raster.tif (metodo de Moore et al. 1991 no SAGA a partir do MDE, segundo a IC). A coluna LS da aba Pixels e o valor do raster amostrado no centro do pixel.")
ws.write(rr + 2, 0, "Pixels sem classe de solo/uso/LS (656): coluna 'Valido'=0 -> sem E_unit (so entram no volume 'todos os pixels').")

# ---- Roteiro (colunas da aba Pixels) ---------------------------------
ws = w_rot
ws.set_column("A:A", 8); ws.set_column("B:B", 38); ws.set_column("C:C", 80); ws.set_column("D:D", 60)
ws.write(0, 0, "EVENTO 11 - Planilha 02: modelo pixel a pixel (154.667 pixels)", G["t"])
ws.write(2, 0, "Como ler: a aba Pixels tem uma linha por pixel; todas as colunas em formula usam as constantes da aba Parametros. Clique em qualquer celula para ver a conta. As abas Resumo, Calibracao_c e Conferencia fecham o modelo.", G["wrap"])
for j, h in enumerate(["Col.", "Variavel", "Formula (em palavras / Excel)", "Origem do dado ou funcao no modelo"]):
    ws.write(4, j, h, G["h"])
roteiro = [
    ("A", "id", "contador 1..N", "chave p/ achar o pixel no QGIS (camada Pixels_Evento11.shp, campo id)"),
    ("B,C", "lin, col", "indices da linha e coluna do pixel na grade 884x365", "posicao no raster"),
    ("D", "X (m)", "=X0_canto + (col+0,5)*dx_pix", "centro do pixel (UTM 23S)"),
    ("E", "Y (m)", "=Y0_canto - (lin+0,5)*dy_pix", "idem"),
    ("F,G", "d2 aos postos (m2)", "=(X-x_posto)^2 + (Y-y_posto)^2", "distancia ao quadrado ate DBT5 e Campo Limpo"),
    ("H", "P (mm)", "=(P_DBT5/d2_DBT5 + P_CLP/d2_CLP) / (1/d2_DBT5 + 1/d2_CLP)", "IDW potencia 2 com 2 postos. Reproduz o raster do QGIS (Interpolacao IDW, coef. 2) com dif < 1e-5 mm"),
    ("I", "CN (AMC II)", "valor do raster CN TCC.tif amostrado no centro do pixel", "QGIS/GDAL: Warp (vizinho mais proximo) do raster 973x362 para a grade 884x365. CN-II = mapa uso x grupo hidrologico (origem a confirmar)"),
    ("J", "CN (AMC I, seco)", "=4,2*CN_II/(10-0,058*CN_II)", "conversao CN-II -> CN-I (Hawkins; Chow et al. 1988). Reproduz CN TCC - Seco.tif com dif < 4e-6"),
    ("K", "S (mm)", "=25,4*(1000/CN_I - 10)", "retencao potencial maxima (SCS). Reproduz S - Seco.tif com dif < 2e-5 mm"),
    ("L", "Classe de solo", "ponto-em-poligono em Pedologia Alto.shp (campo Subordem)", "QGIS: 'Unir atributos por localizacao' (ponto no centro do pixel)"),
    ("M", "K", "=PROCV(classe de solo; tabela Classes_K)", "reproduz K_raster.tif em 100% dos pixels"),
    ("N", "Classe de uso", "ponto-em-poligono em Uso Solo Alto.shp (campo CLASSE)", "idem"),
    ("O", "C", "=PROCV(classe de uso; tabela Classes_C)", "reproduz C_raster.tif em 100% dos pixels"),
    ("P", "LS", "valor do raster LS_raster.tif", "Moore et al. (1991), SAGA, MDE"),
    ("Q", "Valido", "=SE(M, O e P existem; 1; 0)", "1 = pixel entra no calculo de E_unit"),
    ("R", "Q (mm)", "=SE(P<=lambda*S; 0; (P-lambda*S)^2/(P+(1-lambda)*S))", "escoamento SCS-CN do pixel (previsao pura)"),
    ("S", "pr (m3/s)", "=Q/1000*A_pixel*RI/R/3600", "vazao de pico local (Hao et al. 2022, Eq. 3)"),
    ("T", "E_unit (t)", "=SE(Valido; 11,8*MAX(Q*pr*A_pixel;0)^0,56*K*C*P*LS; \"\")", "MUSLE por pixel (Hao et al. 2022, Eq. 1). Sai em toneladas/pixel (nao calibrado)"),
    ("U", "SY (t)", "=c_pura*E_unit", "producao de sedimentos do pixel (previsao pura)"),
    ("V", "Q volume restrito (mm)", "=SE(Valido; MIN(fator_f*Q; P); \"\")", "Q reescalado para o volume medido, limitado a chuva do pixel"),
    ("W", "pr restrito (m3/s)", "=Q_restr/1000*A_pixel*RI/R/3600", ""),
    ("X", "E_unit restrito (t)", "=11,8*MAX(Q_restr*pr_restr*A_pixel;0)^0,56*K*C*P*LS", ""),
    ("Y", "SY restrito (t)", "=c_restr*E_unit_restr", "producao de sedimentos do pixel (volume restrito)"),
]
for i, rw in enumerate(roteiro):
    for j, v in enumerate(rw):
        ws.write(5 + i, j, v, G["wrap"])

# ---- Pixels ----------------------------------------------------------
ws = w_pix
titulos = ["id", "lin", "col", "X (m)", "Y (m)", "d2 ao DBT5 (m2)", "d2 ao Campo Limpo (m2)", "P (mm)", "CN AMC II", "CN AMC I", "S (mm)",
           "Classe de solo", "K", "Classe de uso", "C", "LS", "Valido", "Q (mm)", "pr (m3/s)", "E_unit (t)", "SY previsao pura (t)",
           "Q restrito (mm)", "pr restrito (m3/s)", "E_unit restrito (t)", "SY restrito (t)"]
for j, h in enumerate(titulos):
    ws.write(0, j, h, G["h"])
ws.set_row(0, 45)
ws.set_column("A:C", 8); ws.set_column("D:E", 13); ws.set_column("F:G", 14); ws.set_column("H:K", 10)
ws.set_column("L:L", 26); ws.set_column("M:M", 8); ws.set_column("N:N", 20); ws.set_column("O:Q", 8); ws.set_column("R:Y", 13)
ws.freeze_panes(1, 3)
fm = {"f1": G["f1"], "f2": G["f2"], "f4": G["f4"], "f6": G["f6"], "f8": G["f8"], "sci": G["sci"]}
iy, ix = D["iy"], D["ix"]
P_, CN2_, CN1_, S_, K_, C_, LS_ = D["P"], D["CN2"], D["CN1"], D["S"], D["K"], D["C"], D["LS"]
Q_, pr_v, E_, SY_, Qo_, pro_, Eo_, SYo_ = D["Q"], D["pr"], D["E"], D["SY"], D["Qo"], D["pro"], D["Eo"], D["SYo"]
val_ = D["valido"]
xs = D["X0"] + (ix + 0.5) * D["dx"]
ys = D["Y0"] - (iy + 0.5) * D["dy"]
d2a = (xs - est.x_utm[0]) ** 2 + (ys - est.y_utm[0]) ** 2
d2b = (xs - est.x_utm[1]) ** 2 + (ys - est.y_utm[1]) ** 2
fl = lambda v: "" if (v is None or (isinstance(v, float) and np.isnan(v))) else float(v)
for i in range(N):
    r = i + 1; n = r + 1
    ws.write_number(r, 0, i + 1)
    ws.write_number(r, 1, int(iy[i])); ws.write_number(r, 2, int(ix[i]))
    ws.write_formula(r, 3, f"=X0_canto+(C{n}+0.5)*dx_pix", fm["f2"], float(xs[i]))
    ws.write_formula(r, 4, f"=Y0_canto-(B{n}+0.5)*dy_pix", fm["f2"], float(ys[i]))
    ws.write_formula(r, 5, f"=(D{n}-x_DBT5)^2+(E{n}-y_DBT5)^2", fm["f1"], float(d2a[i]))
    ws.write_formula(r, 6, f"=(D{n}-x_CLP)^2+(E{n}-y_CLP)^2", fm["f1"], float(d2b[i]))
    ws.write_formula(r, 7, f"=(P_DBT5/F{n}+P_CLP/G{n})/(1/F{n}+1/G{n})", fm["f4"], float(P_[i]))
    ws.write_number(r, 8, float(CN2_[i]), fm["f4"])
    ws.write_formula(r, 9, f"=4.2*I{n}/(10-0.058*I{n})", fm["f4"], float(CN1_[i]))
    ws.write_formula(r, 10, f"=25.4*(1000/J{n}-10)", fm["f4"], float(S_[i]))
    ws.write_string(r, 11, str(D["solo"][i]))
    kv = K_[i]; cv = C_[i]; lv = LS_[i]
    ws.write_formula(r, 12, f'=IFERROR(VLOOKUP(L{n},Classes_K,2,FALSE),"")', fm["f4"], fl(kv))
    ws.write_string(r, 13, str(D["usoc"][i]))
    ws.write_formula(r, 14, f'=IFERROR(VLOOKUP(N{n},Classes_C,2,FALSE),"")', fm["f4"], fl(cv))
    if np.isnan(lv):
        ws.write_blank(r, 15, None)
    else:
        ws.write_number(r, 15, float(lv), fm["f6"])
    ws.write_formula(r, 16, f"=IF(COUNT(M{n},O{n},P{n})=3,1,0)", None, int(val_[i]))
    ws.write_formula(r, 17, f"=IF(H{n}<=p_lambda*K{n},0,(H{n}-p_lambda*K{n})^2/(H{n}+(1-p_lambda)*K{n}))", fm["f6"], float(Q_[i]))
    ws.write_formula(r, 18, f"=R{n}/1000*A_pixel*RI_mmh/R_evento_mm/3600", fm["sci"], float(pr_v[i]))
    v = bool(val_[i])
    ws.write_formula(r, 19, f'=IF(Q{n}=1,coef_W*MAX(R{n}*S{n}*A_pixel,0)^exp_M*M{n}*O{n}*fator_P*P{n},"")', fm["sci"], fl(E_[i]) if v else "")
    ws.write_formula(r, 20, f'=IF(Q{n}=1,c_pura*T{n},"")', fm["sci"], fl(SY_[i]) if v else "")
    ws.write_formula(r, 21, f'=IF(Q{n}=1,MIN(fator_f*R{n},H{n}),"")', fm["f6"], fl(Qo_[i]) if v else "")
    ws.write_formula(r, 22, f'=IF(Q{n}=1,V{n}/1000*A_pixel*RI_mmh/R_evento_mm/3600,"")', fm["sci"], fl(pro_[i]) if v else "")
    ws.write_formula(r, 23, f'=IF(Q{n}=1,coef_W*MAX(V{n}*W{n}*A_pixel,0)^exp_M*M{n}*O{n}*fator_P*P{n},"")', fm["sci"], fl(Eo_[i]) if v else "")
    ws.write_formula(r, 24, f'=IF(Q{n}=1,c_restr*X{n},"")', fm["sci"], fl(SYo_[i]) if v else "")
print("aba Pixels ok")

# ---- Resumo ----------------------------------------------------------
ws = w_res
ws.set_column("A:A", 62); ws.set_column("B:B", 20); ws.set_column("C:C", 80)
ws.write(0, 0, "Resumo do evento 11 (todas as celulas sao formulas sobre a aba Pixels)", G["t"])
for j, h in enumerate(["Grandeza", "Valor", "Formula / comentario"]):
    ws.write(2, j, h, G["h"])
valid_mask = D["valido"].astype(bool)
Vsum_valid = float(np.nansum(np.where(valid_mask, Q_, 0)))
res_rows = [
    (3, "Pixels na tabela (com CN, logo com Q)", f"=COUNT({pr_('R')})", N, "G['f1']"),
    (4, "Pixels validos para E_unit (com K, C e LS)", f"=SUM({pr_('Q')})", int(valid_mask.sum()), None),
    (5, "Chuva IDW media sobre os pixels (mm)", f"=AVERAGE({pr_('H')})", float(np.mean(P_)), "f4"),
    (6, "Escoamento Q medio sobre os pixels (mm)", f"=AVERAGE({pr_('R')})", float(np.mean(Q_)), "f4"),
    (7, "V_calc, todos os pixels com Q, usando 900 m2 (m3)", f"=SUM({pr_('R')})/1000*900", float(np.nansum(Q_) / 1000 * 900), "res"),
    (8, "V_calc, todos os pixels com Q, usando A_pixel (m3)", f"=SUM({pr_('R')})/1000*A_pixel", float(np.nansum(Q_) / 1000 * D["A_pix"]), "res"),
    (9, "V_calc, so pixels validos, usando A_pixel (m3)  [usado no f]", f'=SUMIF({pr_("Q")},1,{pr_("R")})/1000*A_pixel', Vsum_valid / 1000 * D["A_pix"], "res"),
    (10, "V_med (m3) - planilha de eventos", "=V_med_m3", D["V_MED"], "res"),
    (11, "Erro do volume do SCS-CN (900 m2) em relacao a V_med (%)", "=(B8-B11)/B11*100", (np.nansum(Q_) / 1000 * 900 - D["V_MED"]) / D["V_MED"] * 100, "f4"),
    (12, "f = V_med / V_calc(validos)  [fator do volume restrito]", "=B11/B10", D["f"], "res6"),
    (13, "Pixels em que f*Q passou da chuva do pixel (Q limitado a P)", f'=SUMPRODUCT(({pr_("Q")}=1)*(fator_f*{pr_("R")}>{pr_("H")}))', D["n_exc"], None),
    (15, "SOMA de E_unit - previsao pura (t)", f"=SUM({pr_('T')})", sumE, "res"),
    (16, "SOMA de E_unit - volume restrito (t)", f"=SUM({pr_('X')})", sumEo, "res"),
    (17, "c da previsao pura (aba Calibracao_c)", "=c_pura", c_pura, "res6"),
    (18, "c do volume restrito (aba Calibracao_c)", "=c_restr", c_restr, "res6"),
    (20, "SY simulado - previsao pura (t) = c * soma(E_unit)", f"=SUM({pr_('U')})", float(np.nansum(SY_)), "res"),
    (21, "SY simulado - volume restrito (t)", f"=SUM({pr_('Y')})", float(np.nansum(SYo_)), "res"),
    (22, "SY observado (t) = SYY_t", "=SY_obs_t", D["SY_OBS"], "res"),
    (23, "Erro % - previsao pura = (sim-obs)/obs*100", "=(B21-B23)/B23*100", (np.nansum(SY_) - D["SY_OBS"]) / D["SY_OBS"] * 100, "res"),
    (24, "Erro % - volume restrito", "=(B22-B23)/B23*100", (np.nansum(SYo_) - D["SY_OBS"]) / D["SY_OBS"] * 100, "res"),
    (26, "SY medio por pixel - previsao pura (t/pixel)", f"=B21/B5", float(np.nansum(SY_) / valid_mask.sum()), "sci"),
    (27, "SY medio por pixel - volume restrito (t/pixel)", f"=B22/B5", float(np.nansum(SYo_) / valid_mask.sum()), "sci"),
    (28, "SY medio por hectare - previsao pura (t/ha)", f"=B21/(B5*A_pixel/10000)", float(np.nansum(SY_) / (valid_mask.sum() * D["A_pix"] / 1e4)), "f4"),
    (29, "SY medio por hectare - volume restrito (t/ha)", f"=B22/(B5*A_pixel/10000)", float(np.nansum(SYo_) / (valid_mask.sum() * D["A_pix"] / 1e4)), "f4"),
]
coms = {
    3: "numero de pixels da tabela", 4: "Valido=1", 5: "media simples da chuva interpolada", 6: "media simples de Q",
    7: "e o que os scripts Qvol*.tif / CSV do projeto usam (900 m2); gera 'erro de volume' de -17,76% contra T_R",
    8: "mesma soma com a area real do pixel", 9: "e o V_calc do script de volume restrito",
    10: "T_R_m3 = soma(Q)*3600 (inclui vazao de base)", 11: "erro do volume do SCS-CN em relacao ao T_R (positivo = superestima)",
    12: "f > 1: o SCS-CN subestima o volume TOTAL medido; mas T_R inclui vazao de base (ver planilha 01)",
    13: "caso fisico: escoamento nao pode superar a chuva",
    15: "E_unit nao calibrado", 16: "", 17: "c = soma(E_n*SY_n)/soma(E_n^2), 17 eventos", 18: "",
    20: "", 21: "", 22: "", 23: "negativo = subestima", 24: "",
    26: "", 27: "", 28: "area dos pixels validos", 29: "",
}
heads = {14: "EROSAO / MUSLE", 19: "SEDIMENTOS NO EXUTORIO DA BACIA", 25: "NORMALIZACAO"}
fmap = {"res": G["res"], "res6": G["res6"], "f4": G["f4"], "sci": G["sci"], "G['f1']": G["f1"], None: None}
linhas_res = {rw[0]: rw for rw in res_rows}
for rr in range(3, 30):
    if rr in heads:
        ws.write(rr, 0, heads[rr], G["b"])
    elif rr in linhas_res:
        _, nome, fml, val, fmt = linhas_res[rr]
        ws.write(rr, 0, nome)
        ws.write_formula(rr, 1, fml, fmap[fmt], float(val))
        ws.write(rr, 2, coms.get(rr, ""))

# ---- Calibracao_c ----------------------------------------------------
ws = w_cal
ws.set_column("A:A", 14); ws.set_column("B:V", 14)
ws.write(0, 0, "Calibracao de c (minimos quadrados pela origem, 17 eventos) e metricas", G["t"])
ws.write(1, 0, "SY_sim = c * soma(E_unit). c = soma(E*SY_obs)/soma(E^2). SOMA(E_unit) dos eventos 1-10 e 12-17 vem dos rasters ja gerados (E_unit{n}.tif / E_unit{n}_obs.tif); a do evento 11 e a formula sobre a aba Pixels.")
cab = ["Evento", "SY_obs (t)", "SOMA E pura (t)", "E*SY", "E^2", "SY_sim (t)", "erro %", "(sim-obs)^2", "(obs-media)^2", "SY_sim LOO (t)", "erro LOO %",
       "SOMA E restrita (t)", "E*SY", "E^2", "SY_sim (t)", "erro %", "(sim-obs)^2", "SY_sim LOO (t)", "erro LOO %"]
# colunas pura: B..K (1..10); restrita: L..S (11..18)
for j, h in enumerate(cab):
    ws.write(3, j, h, G["h"])
cmp_ = D["cmp_csv"]
SYo17 = cmp_["SY_obs_t"].to_numpy(float); Ep17 = cmp_["soma_E_unit_previsao_t"].to_numpy(float); Er17 = cmp_["soma_E_unit_restrito_t"].to_numpy(float)
# usa a soma recalculada (pixels) para o evento 11
Ep17 = Ep17.copy(); Er17 = Er17.copy()
Ep17[10] = sumE; Er17[10] = sumEo
cp = np.sum(Ep17 * SYo17) / np.sum(Ep17 ** 2); cr = np.sum(Er17 * SYo17) / np.sum(Er17 ** 2)
mobs = SYo17.mean()
hl = {11}
for i in range(17):
    r = 4 + i; n = r + 1; ev = i + 1
    ws.write_number(r, 0, ev, G["hib"] if ev == 11 else None)
    ws.write_number(r, 1, float(SYo17[i]), G["inp"])
    if ev == 11:
        ws.write_formula(r, 2, "=Resumo!B16", G["hi4"], sumE)
        ws.write_formula(r, 11, "=Resumo!B17", G["hi4"], sumEo)
    else:
        ws.write_number(r, 2, float(Ep17[i]), G["inp"]); ws.write_number(r, 11, float(Er17[i]), G["inp"])
    for (cE, cEs, cES, cSim, cErr, cSq, cLoo, cLooE, e, c_) in [
        ("C", 3, 4, 5, 6, 7, 9, 10, Ep17[i], cp), ("L", 12, 13, 14, 15, 16, 17, 18, Er17[i], cr)]:
        sy = SYo17[i]
        ws.write_formula(r, cEs, f"={cE}{n}*B{n}", G["f4"], float(e * sy))
        ws.write_formula(r, cES, f"={cE}{n}^2", G["f4"], float(e ** 2))
        cc = "$B$22" if cE == "C" else "$L$22"
        simcol = xl_col_to_name(cSim)
        ws.write_formula(r, cSim, f"={cc}*{cE}{n}", G["hi4"] if ev == 11 else G["f4"], float(c_ * e))
        ws.write_formula(r, cErr, f"=({simcol}{n}-B{n})/B{n}*100", G["hi1"] if ev == 11 else G["f2"], float((c_ * e - sy) / sy * 100))
        ws.write_formula(r, cSq, f"=({simcol}{n}-B{n})^2", G["f1"], float((c_ * e - sy) ** 2))
        if cE == "C":
            ws.write_formula(r, 8, f"=(B{n}-AVERAGE($B$5:$B$21))^2", G["f1"], float((sy - mobs) ** 2))
        ccol_E = xl_col_to_name(cEs); ccol_ES = xl_col_to_name(cES)
        c_loo = (np.sum(Ep17 * SYo17) - e * sy) / (np.sum(Ep17 ** 2) - e ** 2) if cE == "C" else (np.sum(Er17 * SYo17) - e * sy) / (np.sum(Er17 ** 2) - e ** 2)
        ws.write_formula(r, cLoo, f"=(SUM({ccol_E}$5:{ccol_E}$21)-{ccol_E}{n})/(SUM({ccol_ES}$5:{ccol_ES}$21)-{ccol_ES}{n})*{cE}{n}", G["f4"], float(c_loo * e))
        ws.write_formula(r, cLooE, f"=({xl_col_to_name(cLoo)}{n}-B{n})/B{n}*100", G["f2"], float((c_loo * e - sy) / sy * 100))
# linha 22 (indice 21): c ; metricas
r = 21
ws.write(r, 0, "c", G["b"])
ws.write_formula(r, 1, "=SUM(D5:D21)/SUM(E5:E21)", G["res6"], cp)
ws.write_formula(r, 11, "=SUM(M5:M21)/SUM(N5:N21)", G["res6"], cr)
ws.write(r + 1, 0, "NSE (in-sample)", G["b"])
ws.write_formula(r + 1, 1, "=1-SUM(H5:H21)/SUM(I5:I21)", G["res6"], 1 - np.sum((cp * Ep17 - SYo17) ** 2) / np.sum((SYo17 - mobs) ** 2))
ws.write_formula(r + 1, 11, "=1-SUM(Q5:Q21)/SUM(I5:I21)", G["res6"], 1 - np.sum((cr * Er17 - SYo17) ** 2) / np.sum((SYo17 - mobs) ** 2))
ws.write(r + 2, 0, "NSE (leave-one-out)", G["b"])
loop = np.array([(np.sum(Ep17 * SYo17) - Ep17[i] * SYo17[i]) / (np.sum(Ep17 ** 2) - Ep17[i] ** 2) * Ep17[i] for i in range(17)])
loor = np.array([(np.sum(Er17 * SYo17) - Er17[i] * SYo17[i]) / (np.sum(Er17 ** 2) - Er17[i] ** 2) * Er17[i] for i in range(17)])
ws.write_formula(r + 2, 1, "=1-SUMXMY2(B5:B21,J5:J21)/SUM(I5:I21)", G["res6"], 1 - np.sum((loop - SYo17) ** 2) / np.sum((SYo17 - mobs) ** 2))
ws.write_formula(r + 2, 11, "=1-SUMXMY2(B5:B21,R5:R21)/SUM(I5:I21)", G["res6"], 1 - np.sum((loor - SYo17) ** 2) / np.sum((SYo17 - mobs) ** 2))
ws.write(r + 3, 0, "PBIAS % (sim-obs)", G["b"])
ws.write_formula(r + 3, 1, "=(SUM(F5:F21)-SUM(B5:B21))/SUM(B5:B21)*100", G["res6"], (np.sum(cp * Ep17) - SYo17.sum()) / SYo17.sum() * 100)
ws.write_formula(r + 3, 11, "=(SUM(O5:O21)-SUM(B5:B21))/SUM(B5:B21)*100", G["res6"], (np.sum(cr * Er17) - SYo17.sum()) / SYo17.sum() * 100)
ws.write(r + 4, 0, "Erro medio %", G["b"])
ws.write_formula(r + 4, 1, "=AVERAGE(G5:G21)", G["res6"], float(np.mean((cp * Ep17 - SYo17) / SYo17 * 100)))
ws.write_formula(r + 4, 11, "=AVERAGE(P5:P21)", G["res6"], float(np.mean((cr * Er17 - SYo17) / SYo17 * 100)))
ws.write(r + 5, 0, "Erro abs. medio %", G["b"])
ws.write_formula(r + 5, 1, "=SUMPRODUCT(ABS(G5:G21))/17", G["res6"], float(np.mean(np.abs((cp * Ep17 - SYo17) / SYo17 * 100))))
ws.write_formula(r + 5, 11, "=SUMPRODUCT(ABS(P5:P21))/17", G["res6"], float(np.mean(np.abs((cr * Er17 - SYo17) / SYo17 * 100))))
ws.write(r + 7, 0, "Nota: o evento 11 (linha amarela) participa da calibracao de c junto com os outros 16; por isso o erro dele (-58,8% / -33,2%) e 'in-sample'. Com leave-one-out, c e recalculado sem o evento 11 (colunas J e R).")
print("c_pura=%.6f c_restr=%.6f" % (cp, cr))

# ---- Conferencia -----------------------------------------------------
ws = w_con
ws.set_column("A:A", 56); ws.set_column("B:D", 22); ws.set_column("E:E", 60)
ws.write(0, 0, "Conferencia: Excel (formulas desta planilha) x rasters do QGIS/projeto", G["t"])
for j, h in enumerate(["Grandeza", "Raster do projeto (soma)", "Esta planilha (soma)", "Diferenca", "Raster"]):
    ws.write(2, j, h, G["h"])
def soma_r(nome):
    ds = gdal.Open(os.path.join(BASE, "Evento 11", nome + ".tif"))
    b = ds.GetRasterBand(1); a = b.ReadAsArray().astype(float); nd = b.GetNoDataValue()
    return float(a[(a != nd) & np.isfinite(a)].sum())
confer = [
    ("Chuva IDW (mm) - soma nos pixels da tabela", None, f"=SUM({pr_('H')})", float(np.sum(P_)), "ChuvaIDW11.tif (so os pixels da tabela)"),
    ("Q (mm) - soma", soma_r("Q11_CN1"), f"=SUM({pr_('R')})", float(np.nansum(Q_)), "Q11_CN1.tif"),
    ("pr (m3/s) - soma", soma_r("pr11"), f"=SUM({pr_('S')})", float(np.nansum(pr_v)), "pr11.tif"),
    ("E_unit (t) - soma", soma_r("E_unit11"), f"=SUM({pr_('T')})", sumE, "E_unit11.tif"),
    ("SY previsao pura (t) - soma", soma_r("SY11"), f"=SUM({pr_('U')})", float(np.nansum(SY_)), "SY11.tif"),
    ("Q volume restrito (mm) - soma", soma_r("Q11_CN1_obs"), f"=SUM({pr_('V')})", float(np.nansum(Qo_)), "Q11_CN1_obs.tif"),
    ("pr restrito (m3/s) - soma", soma_r("pr11_obs"), f"=SUM({pr_('W')})", float(np.nansum(pro_)), "pr11_obs.tif"),
    ("E_unit restrito (t) - soma", soma_r("E_unit11_obs"), f"=SUM({pr_('X')})", sumEo, "E_unit11_obs.tif"),
    ("SY restrito (t) - soma", soma_r("SY11_obs"), f"=SUM({pr_('Y')})", float(np.nansum(SYo_)), "SY11_obs.tif"),
]
for i, (nome, ras, fml, val, arq) in enumerate(confer):
    rr = 3 + i
    ws.write(rr, 0, nome)
    if ras is None:
        ws.write(rr, 1, "n/a")
        ws.write_formula(rr, 2, fml, G["f4"], val)
    else:
        ws.write_number(rr, 1, ras, G["inp_big"])
        ws.write_formula(rr, 2, fml, G["f4"], val)
        ws.write_formula(rr, 3, f"=C{rr+1}-B{rr+1}", G["f6"], val - ras)
    ws.write(rr, 4, arq)
ws.write(14, 0, "As diferencas (~1e-4 relativo) sao so a precisao float32 dos GeoTIFFs; o calculo em Excel usa dupla precisao.")
wb.close()
print("planilha 02 ok")
