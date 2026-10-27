import sys
import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding="utf-8")
DI = r"C:\TCC\Dados Iniciais"
OUT = r"C:\TCC\Comparacao_Modelos_TCC.xlsx"

ev = pd.read_excel(DI + r"\eventos_processados_manuais.xlsx", sheet_name="Sheet1").iloc[:18]
R = [ev.iloc[0 if n == 1 else n] for n in range(1, 18)]
SY = np.array([float(r["SYY_t"]) for r in R])
vol = pd.read_csv(DI + r"\comparacao_volumes_medido_vs_calculado.csv").sort_values("evento")
qpc = pd.read_csv(DI + r"\comparacao_qpico_convolucao_medido_vs_calculado.csv").sort_values("evento")
cmp_ = pd.read_csv(DI + r"\comparacao_SY_previsao_vs_restrito.csv").sort_values("evento")
V_med = vol["T_R_m3_medido"].to_numpy(float); V_calc = vol["Vol_CN1_calc"].to_numpy(float)
QP_med = vol["Q_pico_medido"].to_numpy(float); QP_calc = qpc["Qp_calc_convolucao"].to_numpy(float)
E_prev = cmp_["soma_E_unit_previsao_t"].to_numpy(float); E_rest = cmp_["soma_E_unit_restrito_t"].to_numpy(float)
nb = pd.read_csv(DI + r"\comparacao_SY_modelo_com_base.csv").sort_values("evento")   # modelo com vazao de base (15/10/2026)
S_base = nb["SY_sim_t"].to_numpy(float); L_base = nb["SY_loo_t"].to_numpy(float)
E_base = nb["soma_E_unit_t"].to_numpy(float); V_dir_obs = nb["V_direto_obs_m3"].to_numpy(float)
R_chuva = np.array([float(r["Chuva_evento_mm"]) for r in R])
sd = pd.read_csv(DI + r"\comparacao_SY_so_direto.csv").sort_values("evento")   # modelo adotado em 26/10/2026 (so escoamento direto)
E_sdc = sd["soma_E_unit_calc_t"].to_numpy(float); E_sdf = sd["soma_E_unit_forc_t"].to_numpy(float)

den = np.sum((SY - SY.mean()) ** 2)


def nse(s):
    return 1 - np.sum((SY - s) ** 2) / den


def wia(s):
    om = SY.mean()
    return 1 - np.sum((SY - s) ** 2) / np.sum((np.abs(s - om) + np.abs(SY - om)) ** 2)


def pbias(s):
    return 100 * np.sum(s - SY) / np.sum(SY)


def escala(x):
    c = np.sum(x * SY) / np.sum(x ** 2)
    sim = c * x
    loo = np.empty(17)
    for i in range(17):
        m = np.ones(17, bool); m[i] = False
        loo[i] = (np.sum(x[m] * SY[m]) / np.sum(x[m] ** 2)) * x[i]
    return c, sim, loo


# alfa/beta livres e FCI/DSC: valores por evento obtidos nos experimentos (saidas dos scripts, 17/09 e 02/10/2026)
SIM_AB = np.array([402.31, 1166.06, 1774.47, 830.32, 1512.46, 798.67, 665.33, 1864.47, 1893.59, 423.83, 1297.32, 535.14, 1806.80, 1969.22, 3132.09, 1783.68, 1665.70])
SIM_FCI = np.array([44, 458, 1275, 219, 993, 255, 141, 1469, 1497, 58, 600, 127, 1379, 1729, 4683, 1287, 1049], float)

c_mod, s_mod, l_mod = escala((V_calc * QP_calc) ** 0.56)
c_med, s_med, l_med = escala((V_med * QP_med) ** 0.56)
c_prev, s_prev, l_prev = escala(E_prev)
c_rest, s_rest, l_rest = escala(E_rest)
c_tr, s_tr, l_tr = escala(V_med)
c_vd, s_vd, l_vd = escala(V_dir_obs)
c_ch, s_ch, l_ch = escala(R_chuva)
c_sdc, s_sdc, l_sdc = escala(E_sdc)
c_sdf, s_sdf, l_sdf = escala(E_sdf)
c_base = np.sum(E_base * SY) / np.sum(E_base ** 2)
XS = {"Concentrada — D e qp do modelo (só escala)": (V_calc * QP_calc) ** 0.56,
      "Concentrada — D e qp medidos (só escala)": (V_med * QP_med) ** 0.56,
      "Espacializada — Q do modelo (previsão pura, λ = 0,05, sem vazão de base)": E_prev,
      "Espacializada — Q forçado ao volume medido total (volume restrito)": E_rest,
      "ADOTADO — Espacializada — calculado: Q = só escoamento direto do SCS-CN (λ = 0,20)": E_sdc,
      "ADOTADO — Espacializada — forçado: Q reescalado para o escoamento direto medido": E_sdf,
      "Não adotado (até 26/10/2026) — Espacializada — Q = escoamento direto (λ = 0,20) + vazão de base prevista": E_base,
      "Sem MUSLE — SY = c · volume total medido (T_R)": V_med,
      "Sem MUSLE — SY = c · escoamento direto medido": V_dir_obs,
      "Sem MUSLE — SY = c · chuva do evento": R_chuva}


def nse_sem15(rot, sim):
    m = np.arange(17) != 14
    if rot in XS:
        x = XS[rot]; c = np.sum(x[m] * SY[m]) / np.sum(x[m] ** 2); sim = c * x
    return 1 - np.sum((SY[m] - sim[m]) ** 2) / np.sum((SY[m] - SY[m].mean()) ** 2)


def nse_log(sim):
    lo, ls = np.log(SY), np.log(np.clip(sim, 1e-6, None))
    return 1 - np.sum((lo - ls) ** 2) / np.sum((lo - lo.mean()) ** 2)

# confere com os valores documentados
print(f"conf novo: adotado NSE={nse(S_base):.4f} (0,501) LOO={nse(L_base):.4f} (0,380) | c*T_R NSE={nse(s_tr):.4f} (0,809) LOO={nse(l_tr):.4f} (0,765)")
print(f"conf: conc.modelo NSE={nse(s_mod):.4f} (0,4412) | conc.medidos NSE={nse(s_med):.4f} (0,8476) | prev NSE={nse(s_prev):.4f} (0,3714) "
      f"LOO={nse(l_prev):.4f} (0,2816) | rest NSE={nse(s_rest):.4f} (0,8052) LOO={nse(l_rest):.4f} (0,7759) | AB NSE={nse(SIM_AB):.4f} (0,6121) | FCI NSE={nse(SIM_FCI):.4f} (0,2056)")

CFG = [
    # rotulo, sim, loo, params, usa_medido, espacial, c, observacao, grupo
    ("Chute da média (NSE = 0 por definição)", np.full(17, SY.mean()), None, 0, "—", "—", None,
     "Referência: prever sempre a média dos 17 sedimentos medidos. Qualquer modelo útil precisa ficar acima de NSE = 0.", "ref"),
    ("Concentrada — D e qp do modelo (só escala)", s_mod, l_mod, 1, "Não", "Não", c_mod,
     "SY = c·(D·qp)^0,56, com D = volume do SCS-CN e qp = pico do HU-SCS (Fase 1). K, LS, C e P absorvidos em c.", "conc"),
    ("Concentrada — D e qp medidos (só escala)", s_med, l_med, 1, "Sim (D e qp)", "Não", c_med,
     "Mesma fórmula, com D = T_R_m3 e qp = Q_pico medidos. Teto da formulação concentrada com entrada perfeita.", "conc"),
    ("Espacializada — Q do modelo (previsão pura, λ = 0,05, sem vazão de base)", s_prev, l_prev, 1, "Não", "Sim", c_prev,
     "SY = c·ΣE_unit, com Q de cada pixel pelo SCS-CN (CN-I, λ = 0,05). Versão anterior (até 14/10/2026): calibrada contra o volume TOTAL, que inclui vazão de base.", "esp"),
    ("Espacializada — Q forçado ao volume medido total (volume restrito)", s_rest, l_rest, 1, "Sim (volume)", "Sim", c_rest,
     "Q de cada pixel multiplicado pelo fator f do evento para o volume total bater T_R_m3 (limite Q ≤ chuva). Não é previsão pura; T_R_m3 inclui vazão de base.", "esp"),
    ("ADOTADO — Espacializada — calculado: Q = só escoamento direto do SCS-CN (λ = 0,20)", s_sdc, l_sdc, 1, "Não", "Sim", c_sdc,
     "SY = c·ΣE_unit, com Q de cada pixel pelo SCS-CN (CN-I, λ = 0,20), sem termo de vazão de base (decisão de 26/10/2026). Aqui c por mínimos quadrados lineares, como nas demais linhas; no texto do TCC c é calibrado em log (tab_resultados.md).", "esp"),
    ("ADOTADO — Espacializada — forçado: Q reescalado para o escoamento direto medido", s_sdf, l_sdf, 1, "Sim (volume direto)", "Sim", c_sdf,
     "Q de cada pixel reescalado para o escoamento direto medido do evento (T_R − ΣBt·3600; limite Q ≤ chuva). Sem termo de base. Não é previsão: usa o volume medido. c por mínimos quadrados lineares nesta planilha.", "esp"),
    ("Não adotado (até 26/10/2026) — Espacializada — Q = escoamento direto (λ = 0,20) + vazão de base prevista", S_base, L_base, 2, "Parcial (Qb inicial e duração)", "Sim", c_base,
     "Q do pixel = SCS-CN (CN-I, λ = 0,20) + lâmina de base uniforme = kb·Qb_inicio·duração (kb = 1,93). LOO aninhado (kb e c refeitos sem o evento). A duração é a da janela observada.", "esp"),
    ("Sem MUSLE — SY = c · volume total medido (T_R)", s_tr, l_tr, 1, "Sim (volume)", "Não", c_tr,
     "Referência trivial: sedimento proporcional ao volume total medido. Empata ou supera os modelos espacializados.", "bench"),
    ("Sem MUSLE — SY = c · escoamento direto medido", s_vd, l_vd, 1, "Sim (volume)", "Não", c_vd,
     "Mesma referência, com o escoamento direto (T_R − Σ Bt·3600).", "bench"),
    ("Sem MUSLE — SY = c · chuva do evento", s_ch, l_ch, 1, "Sim (chuva)", "Não", c_ch,
     "Referência trivial: sedimento proporcional à lâmina de chuva do evento (não usa vazão).", "bench"),
    ("Espacializada — α e β livres (experimento, não adotado)", SIM_AB, None, 2, "Não", "Sim", None,
     "α = 4,22 e β = 0,28 ajustados na fórmula por pixel (NSE bruto). Só in-sample; instável em eventos pequenos.", "exp"),
    ("Espacializada — com FCI/DSC de Hao (descartado)", SIM_FCI, None, 2, "Não", "Sim", None,
     "Eq. 8 exata, objetivo NSE bruto: FCI₀ = 3,17 (limite da busca) e k = 4,90. Só in-sample; valores por evento arredondados.", "exp"),
]

wb = Workbook()
thin = Side(style="thin", color="C6CFDB")
BORDA = Border(left=thin, right=thin, top=thin, bottom=thin)
HEAD = PatternFill("solid", fgColor="1F5FA8")
FILL = {"ref": "EEEEEE", "conc": "FFF4E0", "esp": "E7F1FB", "exp": "F6E9F6", "bench": "E6F4EA"}


def cab(ws, row, vals, widths=None):
    for j, v in enumerate(vals, 1):
        c = ws.cell(row=row, column=j, value=v)
        c.font = Font(bold=True, color="FFFFFF"); c.fill = HEAD; c.border = BORDA
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")


# ------------------------------------------------------------- Resumo
ws = wb.active; ws.title = "Resumo"
ws["A1"] = "Comparação dos modelos de produção de sedimentos — 17 eventos (Alto Jundiaí)"
ws["A1"].font = Font(bold=True, size=13, color="1F5FA8")
ws["A2"] = ("NSE: 1 = perfeito; 0 = tão bom quanto chutar a média; negativo = pior que a média. PBIAS = Σ(S−O)/ΣO×100 (negativo = subestima). "
            "In-sample: o parâmetro foi ajustado nos mesmos 17 eventos; leave-one-out: cada evento é previsto sem usá-lo no ajuste.")
ws["A2"].alignment = Alignment(wrap_text=True); ws.merge_cells("A2:N2"); ws.row_dimensions[2].height = 34
cab(ws, 4, ["Modelo", "Parâmetros livres", "Usa dado medido do evento?", "Espacializada?", "c (se aplicável)", "NSE in-sample", "NSE leave-one-out",
            "WIA (in-sample)", "PBIAS % (in-sample)", "Erro médio %", "Erro absoluto médio % (in-sample)", "NSE sem o evento 15 (c refeito)", "NSE em log (in-sample)", "Observação"])
ws.row_dimensions[4].height = 46
for i, (nome, sim, loo, npar, usa, esp, c, obs, g) in enumerate(CFG, 5):
    err = 100 * (sim - SY) / SY
    vals = [nome, npar, usa, esp, c, nse(sim), (nse(loo) if loo is not None else "—"), wia(sim), pbias(sim), err.mean(), np.abs(err).mean(), nse_sem15(nome, sim), nse_log(sim), obs]
    for j, v in enumerate(vals, 1):
        cell = ws.cell(row=i, column=j, value=v)
        cell.border = BORDA; cell.fill = PatternFill("solid", fgColor=FILL[g])
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="left" if j in (1, 14) else "center")
        if j == 5 and isinstance(v, float): cell.number_format = "0.0000"
        if j in (6, 7, 8, 12, 13) and isinstance(v, float): cell.number_format = "0.000"
        if j in (9, 10, 11) and isinstance(v, float): cell.number_format = '0.0'
    ws.row_dimensions[i].height = 48
r0 = 5 + len(CFG) + 1
r1 = r0
ws.cell(row=r1, column=1, value="Legenda de cores").font = Font(bold=True)
for k, (g, t) in enumerate([("ref", "Referência"), ("conc", "Concentrada (um D e um qp por evento)"), ("esp", "Espacializada (pixel a pixel)"), ("bench", "Referência sem MUSLE (modelo trivial)"), ("exp", "Experimento não adotado")], 1):
    c = ws.cell(row=r1 + k, column=1, value=t); c.fill = PatternFill("solid", fgColor=FILL[g]); c.border = BORDA
for j, w in enumerate([58, 11, 19, 13, 11, 11, 13, 11, 12, 11, 15, 14, 13, 80], 1):
    ws.column_dimensions[get_column_letter(j)].width = w
ws.freeze_panes = "B5"

# ------------------------------------------------------------- SY por evento
w2 = wb.create_sheet("SY_por_evento")
w2["A1"] = "Sedimento por evento (t): medido e simulado por cada modelo, e erro percentual"; w2["A1"].font = Font(bold=True, size=12, color="1F5FA8")
heads = ["Evento", "SY medido (t)"] + [c[0] for c in CFG]
cab(w2, 3, heads); w2.row_dimensions[3].height = 70
for n in range(17):
    w2.cell(row=4 + n, column=1, value=n + 1).alignment = Alignment(horizontal="center")
    w2.cell(row=4 + n, column=2, value=float(SY[n])).number_format = "#,##0.0"
    for j, cf in enumerate(CFG):
        c = w2.cell(row=4 + n, column=3 + j, value=float(cf[1][n])); c.number_format = "#,##0.0"
base = 4 + 17 + 2
w2.cell(row=base, column=1, value="Erro % = (simulado − medido) / medido × 100").font = Font(bold=True)
cab(w2, base + 1, ["Evento", "—"] + [c[0] for c in CFG]); w2.row_dimensions[base + 1].height = 70
for n in range(17):
    w2.cell(row=base + 2 + n, column=1, value=n + 1).alignment = Alignment(horizontal="center")
    for j, cf in enumerate(CFG):
        c = w2.cell(row=base + 2 + n, column=3 + j, value=float(100 * (cf[1][n] - SY[n]) / SY[n])); c.number_format = "0.0"
for j in range(1, 3 + len(CFG)):
    w2.column_dimensions[get_column_letter(j)].width = 15 if j > 2 else (8 if j == 1 else 14)
w2.freeze_panes = "C4"

# ------------------------------------------------------------- Entradas
w3 = wb.create_sheet("Entradas")
w3["A1"] = "Entradas e quantidades intermediárias por evento"; w3["A1"].font = Font(bold=True, size=12, color="1F5FA8")
h3 = ["Evento", "Chuva do evento R (mm)", "Intensidade 60 min RI (mm/h)", "RI/R (1/h)", "Duração (h)", "Volume medido (m³)", "Volume calculado, SCS-CN (m³)",
      "Fator f = medido/calculado", "Q pico medido (m³/s)", "Q pico calculado, HU-SCS (m³/s)", "ΣE_unit previsão pura (t)", "ΣE_unit volume restrito (t)",
      "SY medido (t)", "SY medido / ΣE (previsão)", "SY medido / ΣE (restrito)",
      "Vazão de base observada, Σ Bt (m³)", "Escoamento direto observado (m³)", "Escoamento direto SCS-CN λ = 0,20 (m³)", "Vazão de base prevista (m³)", "Volume total previsto, LOO (m³)", "Erro do volume total previsto (%)"]
cab(w3, 3, h3); w3.row_dimensions[3].height = 62
for n in range(17):
    r = R[n]; Rm = float(r["Chuva_evento_mm"]); RI = float(r["Intensidade_60min_mm/h"])
    row = [n + 1, Rm, RI, RI / Rm, float(r["Duracao_horas"]), V_med[n], V_calc[n], V_med[n] / V_calc[n], QP_med[n], QP_calc[n], E_prev[n], E_rest[n],
           SY[n], SY[n] / E_prev[n], SY[n] / E_rest[n], nb["V_base_obs_m3"].iloc[n], nb["V_direto_obs_m3"].iloc[n], nb["V_dir_SCS_m3"].iloc[n],
           nb["V_base_prev_m3"].iloc[n], nb["V_total_prev_loo_m3"].iloc[n], nb["erro_V_total_pct"].iloc[n]]
    fm = [None, "0.0", "0.0", "0.000", "0", "#,##0", "#,##0", "0.00", "0.0", "0.0", "#,##0", "#,##0", "#,##0.0", "0.000", "0.000", "#,##0", "#,##0", "#,##0", "#,##0", "#,##0", "0.0"]
    for j, (v, f) in enumerate(zip(row, fm), 1):
        c = w3.cell(row=4 + n, column=j, value=float(v) if j > 1 else v)
        if f: c.number_format = f
        c.alignment = Alignment(horizontal="center")
for j in range(1, 22):
    w3.column_dimensions[get_column_letter(j)].width = 16
w3.freeze_panes = "B4"

# ------------------------------------------------------------- Leia-me
w4 = wb.create_sheet("Leia-me")
linhas = [
    "Como esta planilha foi feita",
    "Gerada/atualizada em 15/10/2026 (modelo adotado trocado em 26/10/2026) por Scripts/gerar_planilha_comparacao.py a partir de: eventos_processados_manuais.xlsx, comparacao_volumes_medido_vs_calculado.csv,",
    "comparacao_qpico_convolucao_medido_vs_calculado.csv, comparacao_SY_previsao_vs_restrito.csv, comparacao_SY_modelo_com_base.csv (vazão de base, não adotado) e comparacao_SY_so_direto.csv (adotado).",
    "",
    "O que cada modelo é",
    "• Chute da média: prever sempre a média dos sedimentos medidos. Dá NSE = 0 por definição; é a régua mínima.",
    "• Concentrada: um único volume D e um único pico qp por evento para a bacia toda com os expoentes fixos de Williams (0,56). Só a escala c é ajustada.",
    "• Espacializada: a MUSLE é calculada em cada pixel e somada. 'Q do modelo' usa o escoamento do SCS-CN; 'Q forçado' reescala o Q do raster para o volume total bater o volume medido.",
    "• ADOTADO (26/10/2026): só escoamento direto, sem termo de vazão de base. Calculado: Q do SCS-CN (λ = 0,20); forçado: Q reescalado para o escoamento direto medido. Compara-se com a carga TOTAL medida (todo o sedimento do evento é atribuído ao escoamento superficial).",
    "• Nesta planilha todas as escalas c são ajustadas por mínimos quadrados lineares; no texto do TCC a calibração adotada é em log (ver TCC_Texto/tabelas/).",
    "• Não adotado (15 a 26/10/2026): Q = escoamento direto + lâmina de vazão de base prevista, uniforme (kb·Qb_inicio·duração). Removido: a vazão de base não produz erosão nas encostas.",
    "• Sem MUSLE: modelos triviais (SY proporcional ao volume ou à chuva), com um parâmetro c. Servem de régua: um modelo espacializado só se justifica se superar isso.",
    "• α e β livres e FCI/DSC são experimentos que não foram adotados (valores só in-sample).",
    "",
    "Pontos de atenção",
    "• T_R_m3 (volume 'medido') = soma das vazões horárias × 3600: é o volume TOTAL, inclui a vazão de base (34–55%). SYY_t é a carga total (Q·CSS). O SCS-CN calcula só escoamento direto.",
    "• NSE in-sample é otimista; o leave-one-out (c, e no modelo adotado também kb, refeitos sem o evento testado) é o valor honesto. Para α/β livres e FCI/DSC não foi calculado.",
    "• O evento 15 responde por 49% da variância do SY medido; veja a coluna 'NSE sem o evento 15'. Com n = 17, os intervalos são largos (bootstrap do NSE do modelo adotado: [−0,96; 0,88]).",
    "• 'Q forçado', 'D e qp medidos' e os modelos 'Sem MUSLE' usam dado medido do evento; não são previsões puras e não devem ser comparados diretamente com a previsão de Hao et al. (2022).",
    "• No modelo adotado, a duração é a janela observada do evento, kb é ajustado nos mesmos 17 eventos e λ foi fixado em 0,20 (padrão) depois de ver diagnósticos com outros valores.",
    "• Os valores por evento de α/β livres e de FCI/DSC vêm das saídas de calibrar_alfa_beta_pixel.py (17/09) e da recalibração com a Eq. 8 exata (02/10); o FCI/DSC está arredondado em t.",
]
for i, t in enumerate(linhas, 1):
    c = w4.cell(row=i, column=1, value=t)
    if t in ("Como esta planilha foi feita", "O que cada modelo é", "Pontos de atenção"):
        c.font = Font(bold=True, color="1F5FA8")
    c.alignment = Alignment(wrap_text=True, vertical="top")
w4.column_dimensions["A"].width = 150
wb.save(OUT)
print("salvo:", OUT)
for nome, sim, loo, *_ in CFG:
    print(f"{nome[:58]:<58} NSE={nse(sim):7.3f} LOO={(nse(loo) if loo is not None else float('nan')):7.3f} WIA={wia(sim):.3f} PBIAS={pbias(sim):+7.1f}")
