"""Gera Planilhas/planilha_calculos_concentrados.xlsx: calculos fora dos rasters, so com formulas vivas, sem estilo.
Entradas: Dados Iniciais/Dados_finais_histereses_corrigido.xlsx, comparacao_SY_lambda005_woodward.csv,
eventos_processados_manuais.xlsx (Q_pico) e TCC_Texto/tabelas/tab_eventos.md."""
import re, datetime as dt, pandas as pd, openpyxl
from openpyxl import Workbook
from openpyxl.utils import get_column_letter as L

N = 17
csv = pd.read_csv("Dados Iniciais/comparacao_SY_lambda005_woodward.csv")
src = openpyxl.load_workbook("Dados Iniciais/Dados_finais_histereses_corrigido.xlsx", data_only=True).active
serie = [r[:7] for r in src.iter_rows(min_row=2, values_only=True) if r[4] is not None]
qp_src = openpyxl.load_workbook("Dados Iniciais/eventos_processados_manuais.xlsx", data_only=True).active
hd = [c.value for c in qp_src[1]]
qpico = [r[hd.index("Q_pico")] for r in qp_src.iter_rows(min_row=2, values_only=True)
         if r[0] not in ("1B", None) and r[hd.index("T_R_m3")]]

def dtp(s):
    m = re.match(r"(\d+)/(\d+)/(\d+) (\d+)h", s)
    return dt.datetime(2000 + int(m[3]), int(m[2]), int(m[1]), int(m[4]))
tab = []
for l in open("TCC_Texto/tabelas/tab_eventos.md", encoding="utf-8").read().splitlines()[2:2 + N]:
    c = [x.strip() for x in l.strip("|").split("|")]
    tab.append((int(c[0]), dtp(c[1]), dtp(c[2]), *[float(x.replace(",", ".")) for x in c[4:8]]))

wb = Workbook()

# ---------- serie ----------
ws = wb.active; ws.title = "serie"
ws.append(["Data", "Q_m3s", "CSS_mgL", "Bt_planilha_m3s", "Bt_Eckhardt_m3s", "Q_x_CSS_t_por_h"])
ws["H1"], ws["I1"] = "alfa", 0.995
ws["H2"], ws["I2"] = "BFImax", 0.70
for i, (d, p1, p2, pt, q, css, bt) in enumerate(serie):
    r = i + 2
    ws.cell(r, 1, d); ws.cell(r, 2, q); ws.cell(r, 3, css); ws.cell(r, 4, bt)
    if i == 0:
        ws.cell(r, 5, f"=D{r}")
    else:
        ws.cell(r, 5, f"=MIN(B{r},((1-$I$2)*$I$1*E{r-1}+(1-$I$1)*$I$2*B{r})/(1-$I$1*$I$2))")
    ws.cell(r, 6, f"=B{r}*C{r}*3.6/1000")
last = len(serie) + 1
S = lambda col: f"serie!${col}$2:${col}${last}"

# ---------- eventos ----------
we = wb.create_sheet("eventos")
we.append(["evento", "inicio", "fim", "P_DBT5_mm", "P_CampoLimpo_mm", "R_mm", "RI_mm_h", "Qpico_m3s", "TR_m3",
           "SomaBt_m3", "SomaBt_Eckhardt_m3", "V_dir_m3", "V_SCS_m3", "V_SCS_sobre_V_dir", "SomaE_MC", "SomaE_MFM", "SY_obs_t"])
for i, (ev, ini, fim, p1, p2, r_, ri) in enumerate(tab):
    r = i + 2
    we.cell(r, 1, ev); we.cell(r, 2, ini); we.cell(r, 3, fim); we.cell(r, 4, p1); we.cell(r, 5, p2)
    we.cell(r, 6, f"=0.307*D{r}+0.693*E{r}"); we.cell(r, 7, ri); we.cell(r, 8, qpico[i])
    win = f'{S("A")},">="&B{r},{S("A")},"<="&C{r}'
    we.cell(r, 9, f'=SUMIFS({S("B")},{win})*3600')
    we.cell(r, 10, f'=SUMIFS({S("D")},{win})*3600')
    we.cell(r, 11, f'=SUMIFS({S("E")},{win})*3600')
    we.cell(r, 12, f"=I{r}-J{r}")
    we.cell(r, 13, float(csv.V_dir_SCS_m3[i])); we.cell(r, 14, f"=M{r}/L{r}")
    we.cell(r, 15, float(csv.soma_E_unit_calc_t[i])); we.cell(r, 16, float(csv.soma_E_unit_forc_t[i]))
    we.cell(r, 17, f'=SUMIFS({S("F")},{win})')
R0, R1 = 2, N + 1

# ---------- calibracao ----------
wc = wb.create_sheet("calibracao")
# modelos: (nome, coluna de x em eventos)
models = [("MC", "O"), ("MFM", "P"), ("chuva", "F"), ("Vdir", "L"), ("TR", "I")]
hdr = ["evento", "ln_SY_obs"]
for m, _ in models:
    hdr += [f"ln_x_{m}", f"SY_ajuste_{m}", f"c_LOO_{m}", f"SY_LOO_{m}"]
wc.append(hdr)
for i in range(N):
    r = i + 2
    wc.cell(r, 1, f"=eventos!A{r}"); wc.cell(r, 2, f"=LN(eventos!Q{r})")
    for k, (m, col) in enumerate(models):
        c0 = 3 + 4 * k
        lx, sa, cl, sl = (L(c0 + j) for j in range(4))
        wc.cell(r, c0, f"=LN(eventos!{col}{r})")
        wc.cell(r, c0 + 1, f"=${lx}$21*eventos!{col}{r}")
        wc.cell(r, c0 + 2, f"=EXP((SUM($B$2:$B$18)-$B{r}-(SUM({lx}$2:{lx}$18)-{lx}{r}))/16)")
        wc.cell(r, c0 + 3, f"={cl}{r}*eventos!{col}{r}")
wc.cell(21, 1, "c")
for k in range(len(models)):
    lx = L(3 + 4 * k)
    wc.cell(21, 3 + 4 * k, f"=EXP(AVERAGE($B$2:$B$18)-AVERAGE({lx}2:{lx}18))")

# ---------- metricas ----------
wm = wb.create_sheet("metricas")
hdr = ["evento", "ln_SY_obs", "rank_SY_obs"]
for m, _ in models + [("IC", None)]:
    hdr += [f"razao_ajuste_{m}", f"razao_LOO_{m}", f"erro_LOO_pct_{m}", f"abs_erro_LOO_pct_{m}", f"ln_SY_LOO_{m}", f"rank_LOO_{m}"]
wm.append(hdr)
# IC (aba propria) precisa existir antes; colunas SY_LOO da IC em ic!M
for i in range(N):
    r = i + 2
    wm.cell(r, 1, f"=eventos!A{r}"); wm.cell(r, 2, f"=calibracao!B{r}")
    wm.cell(r, 3, f"=RANK(eventos!Q{r},eventos!$Q$2:$Q$18,1)+(COUNTIF(eventos!$Q$2:$Q$18,eventos!Q{r})-1)/2")
    for k in range(len(models) + 1):
        c0 = 4 + 6 * k
        if k < len(models):
            base = 3 + 4 * k
            adj, loo = f"calibracao!{L(base+1)}{r}", f"calibracao!{L(base+3)}{r}"
        else:
            adj, loo = f"ic!K{r}", f"ic!L{r}"
        rl = f"{L(c0+1)}"
        wm.cell(r, c0, f"={adj}/eventos!Q{r}")
        wm.cell(r, c0 + 1, f"={loo}/eventos!Q{r}")
        wm.cell(r, c0 + 2, f"=({L(c0+1)}{r}-1)*100")
        wm.cell(r, c0 + 3, f"=ABS({L(c0+2)}{r})")
        wm.cell(r, c0 + 4, f"=LN({loo})")
        wm.cell(r, c0 + 5, f"=RANK({loo},{('calibracao!'+L(base+3)+'$2:'+L(base+3)+'$18') if k < len(models) else 'ic!$L$2:$L$18'},1)+(COUNTIF({('calibracao!'+L(base+3)+'$2:'+L(base+3)+'$18') if k < len(models) else 'ic!$L$2:$L$18'},{loo})-1)/2")
# resumo (linhas 21 em diante): rotulo em A, valor na coluna razao_LOO de cada modelo
labels = ["erro_mediano_LOO_pct", "dentro_fator2_pct", "NSE_log_LOO", "NSE_linear_LOO", "Spearman_LOO",
          "erro_mediano_ajuste_pct", "NSE_log_ajuste"]
for j, lab in enumerate(labels):
    wm.cell(21 + j, 1, lab)
for k, (m, _) in enumerate(models + [("IC", None)]):
    c0 = 4 + 6 * k
    ra, rl, ab, ln, rk = L(c0), L(c0 + 1), L(c0 + 3), L(c0 + 4), L(c0 + 5)
    if k < len(models):
        loo = f"calibracao!{L(3+4*k+3)}$2:{L(3+4*k+3)}$18"
    else:
        loo = "ic!$L$2:$L$18"
    wm.cell(21, c0 + 1, f"=MEDIAN({ab}2:{ab}18)")
    wm.cell(22, c0 + 1, f'=COUNTIFS({rl}2:{rl}18,">=0.5",{rl}2:{rl}18,"<=2")/17*100')
    wm.cell(23, c0 + 1, f"=1-SUMXMY2({ln}2:{ln}18,$B$2:$B$18)/DEVSQ($B$2:$B$18)")
    wm.cell(24, c0 + 1, f"=1-SUMXMY2({loo},eventos!$Q$2:$Q$18)/DEVSQ(eventos!$Q$2:$Q$18)")
    wm.cell(25, c0 + 1, f"=CORREL({rk}2:{rk}18,$C$2:$C$18)")
# erro mediano e NSE log do ajuste: precisam de colunas auxiliares -> aba ajuste
wj = wb.create_sheet("ajuste")
hj = ["evento"]
for m, _ in models:
    hj += [f"abs_erro_ajuste_pct_{m}", f"ln_SY_ajuste_{m}"]
wj.append(hj)
for i in range(N):
    r = i + 2
    wj.cell(r, 1, f"=eventos!A{r}")
    for k in range(len(models)):
        sa = f"calibracao!{L(3+4*k+1)}{r}"
        wj.cell(r, 2 + 2 * k, f"=ABS({sa}/eventos!Q{r}-1)*100")
        wj.cell(r, 3 + 2 * k, f"=LN({sa})")
for k in range(len(models)):
    c0 = 4 + 6 * k
    wm.cell(26, c0 + 1, f"=MEDIAN(ajuste!{L(2+2*k)}2:{L(2+2*k)}18)")
    wm.cell(27, c0 + 1, f"=1-SUMXMY2(ajuste!{L(3+2*k)}2:{L(3+2*k)}18,metricas!$B$2:$B$18)/DEVSQ(metricas!$B$2:$B$18)")

# ---------- volume ----------
wv = wb.create_sheet("volume")
wv.append(["evento", "V_dir_m3", "V_SCS_m3", "erro_abs_pct"])
for i in range(N):
    r = i + 2
    wv.cell(r, 1, f"=eventos!A{r}"); wv.cell(r, 2, f"=eventos!L{r}"); wv.cell(r, 3, f"=eventos!M{r}")
    wv.cell(r, 4, f"=ABS(C{r}/B{r}-1)*100")
wv["A21"], wv["B21"] = "vies_total_pct", "=(SUM(C2:C18)/SUM(B2:B18)-1)*100"
wv["A22"], wv["B22"] = "erro_medio_absoluto_pct", "=AVERAGE(D2:D18)"
wv["A23"], wv["B23"] = "erro_mediano_pct", "=MEDIAN(D2:D18)"
wv["A24"], wv["B24"] = "NSE_volume", "=1-SUMXMY2(C2:C18,B2:B18)/DEVSQ(B2:B18)"
wv["A25"], wv["B25"] = "razao_mediana", "=MEDIAN(eventos!N2:N18)"

# ---------- ic ----------
wi = wb.create_sheet("ic")
wi.append(["evento", "D_TR_x_Qpico", "KLSC", "ln_D", "ln_SY_sobre_KLSC", "n_LOO", "Sx", "Sy", "Sxx", "Sxy", "SY_ajuste_t", "SY_LOO_t"])
wi["O1"], wi["P1"] = "K", 0.031
wi["O2"], wi["P2"] = "LS", 0.536
wi["O3"], wi["P3"] = "C", 0.267
wi["O5"], wi["P5"] = "beta", "=SLOPE(E2:E18,D2:D18)"
wi["O6"], wi["P6"] = "alfa", "=EXP(INTERCEPT(E2:E18,D2:D18))"
for i in range(N):
    r = i + 2
    wi.cell(r, 1, f"=eventos!A{r}"); wi.cell(r, 2, f"=eventos!I{r}*eventos!H{r}")
    wi.cell(r, 3, "=$P$1*$P$2*$P$3"); wi.cell(r, 4, f"=LN(B{r})"); wi.cell(r, 5, f"=LN(eventos!Q{r}/C{r})")
    wi.cell(r, 6, 16)
    wi.cell(r, 7, f"=SUM($D$2:$D$18)-D{r}"); wi.cell(r, 8, f"=SUM($E$2:$E$18)-E{r}")
    wi.cell(r, 9, f"=SUMSQ($D$2:$D$18)-D{r}^2"); wi.cell(r, 10, f"=SUMPRODUCT($D$2:$D$18,$E$2:$E$18)-D{r}*E{r}")
    wi.cell(r, 11, f"=$P$6*B{r}^$P$5*C{r}")
    sl = f"((F{r}*J{r}-G{r}*H{r})/(F{r}*I{r}-G{r}^2))"
    wi.cell(r, 12, f"=EXP(((H{r}-{sl}*G{r})/F{r})+{sl}*D{r})*C{r}")

wb.save("Planilhas/planilha_calculos_concentrados.xlsx")
print("ok")
