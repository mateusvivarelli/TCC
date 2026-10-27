import sys
import numpy as np, pandas as pd
sys.stdout.reconfigure(encoding="utf-8")
DI = r"C:\TCC\Dados Iniciais"
ev = pd.read_excel(DI + r"\eventos_processados_manuais.xlsx", sheet_name="Sheet1").iloc[:18]
h = pd.read_excel(DI + r"\Dados_finais_histereses_corrigido.xlsx", sheet_name="Planilha1").iloc[:, :8]
h.columns = ["Data", "P1", "P2", "Ptot", "Q", "CSS", "Bt", "CSSBt"]; h["Data"] = pd.to_datetime(h["Data"]); h = h.set_index("Data")
A_BACIA = 138.08e6
print(f"serie de chuva: {h.index.min()} a {h.index.max()} | horas com chuva ausente nos postos: P1 {h.P1.isna().sum()}, P2 {h.P2.isna().sum()}")
print("\nNEH-4 (USDA-SCS, 1972), chuva antecedente de 5 dias: estacao de crescimento AMC I < 35,6 mm; II 35,6-53,3; III > 53,3 | dormente: I < 12,7; II 12,7-27,9; III > 27,9")
print(f"\n{'ev':>2} {'inicio':<17} {'P5 (mm)':>8} {'AMC (cresc.)':>12} {'AMC (dorm.)':>11} | {'R (mm)':>6} {'coef. escoamento direto medido':>30} {'Qb inicio':>9}")
rows = []
for n in range(1, 18):
    r = ev.iloc[0 if n == 1 else n]; t0 = pd.to_datetime(r["Inicio"])
    ant = h.loc[t0 - pd.Timedelta(hours=120): t0 - pd.Timedelta(hours=1)]
    p5 = float((0.307 * ant.P1.fillna(0) + 0.693 * ant.P2.fillna(0)).sum())
    w = h.loc[r["Inicio"]:r["Fim"]]; vd = float((w.Q - w.Bt).sum() * 3600)
    R = float(r["Chuva_evento_mm"]); cr = vd / (R / 1000 * A_BACIA)
    cl = lambda p, a, b: "I" if p < a else ("II" if p <= b else "III")
    rows.append((n, p5, cl(p5, 35.6, 53.3), cl(p5, 12.7, 27.9), R, cr, float(r["Qb_inicio"])))
    print(f"{n:>2} {t0.strftime('%d/%m/%Y %Hh'):<17} {p5:8.1f} {rows[-1][2]:>12} {rows[-1][3]:>11} | {R:6.1f} {100*cr:29.1f}% {rows[-1][6]:9.2f}")
d = pd.DataFrame(rows, columns=["ev", "P5", "amc_c", "amc_d", "R", "cr", "qb"])
print("\ncontagem AMC (estacao de crescimento):", d.amc_c.value_counts().to_dict(), "| (dormente):", d.amc_d.value_counts().to_dict())
print(f"correlacao P5 x coeficiente de escoamento direto: {np.corrcoef(d.P5, d.cr)[0,1]:.2f} | Spearman {d.P5.rank().corr(d.cr.rank()):.2f}")
print(f"correlacao vazao inicial (umidade da bacia) x coeficiente: {np.corrcoef(d.qb, d.cr)[0,1]:.2f}")
print(f"correlacao chuva do evento x coeficiente: {np.corrcoef(d.R, d.cr)[0,1]:.2f}")

# ---- parte 2: AMC por evento x CN-I constante (lambda 0,05, S convertido)
# ver C:/Users/user/AppData/Local/Temp/claude/C--TCC/6f697bf5-4a56-4dbc-a537-266e661ffede/scratchpad/amc_evento.py (depende do cabecalho de calcular_sy_dois_componentes.py)
