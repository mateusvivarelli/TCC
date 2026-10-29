"""Aplica ao md_para_docx.py o suporte a equacoes nativas do Word (OMML).
O gerador escreve cada equacao em UnicodeMath (formato linear) num paragrafo de estilo 'Equacao';
atualizar_sumario_word.ps1 converte esses paragrafos em equacoes (OMaths.Add + BuildUp).
Colar o docx no Google Docs converte as equacoes do Word em equacoes do Docs."""
p = r"C:\TCC\Scripts\md_para_docx.py"
s = open(p, encoding="utf-8", newline="").read()

LINEAR = r'''
# equacoes em UnicodeMath (formato linear); o Word as constroi com BuildUp (atualizar_sumario_word.ps1)
LINEAR = {
    "Y = 11,8 · (Q · qp)^0,56 · K · LS · C · P": "Y=11,8·(Q·qp)^(0,56)·K·LS·C·P",
    "S = 25,4 · (1000 / CN − 10)": "S=25,4·(1000/CN−10)",
    "Q = (P − λS)² / (P + (1 − λ)S),  para P > λS": 'Q=((P−λS)^2)/(P+(1−λ)S)," , para "P>λS',
    "Q = 0,  para P ≤ λS": 'Q=0," , para "P≤λS',
    "CN_I = 4,2 · CN_II / (10 − 0,058 · CN_II)": "CN_I=(4,2·CN_II)/(10−0,058·CN_II)",
    "S = 25,4 · (1000 / CN_I − 10)": "S=25,4·(1000/CN_I−10)",
    "SY_obs = Σ (Q · CSS · 3600 / 10⁶)  (t)": 'SY_(obs)=∑▒((Q·CSS·3600)/10^6)" (t)"',
    "b(t) = [ (1 − BFImax) · a · b(t − 1) + (1 − a) · BFImax · Q(t) ] / (1 − a · BFImax),  com b(t) ≤ Q(t)":
        'b(t)=((1−BFI_(max))·a·b(t−1)+(1−a)·BFI_(max)·Q(t))/(1−a·BFI_(max))," , com "b(t)≤Q(t)',
    "LS = (A_s / 22,13)^0,4 · (sen β / 0,0896)^1,3": 'LS=(A_s/22,13)^(0,4)·("sen" β/0,0896)^(1,3)',
    "P(x) = (P₁/d₁² + P₂/d₂²) / (1/d₁² + 1/d₂²)": "P(x)=(P_1/d_1^2+P_2/d_2^2)/(1/d_1^2+1/d_2^2)",
    "pr_k = (Q_k / 1000) · A_pix · (RI / R) / 3600   (m³/s)": 'pr_k=((Q_k/1000)·A_(pix)·(RI/R))/3600" (m³/s)"',
    "E_unit,k = 11,8 · (Q_k · pr_k · A_pix)^0,56 · K_k · LS_k · C_k · P_k": "E_(unit,k)=11,8·(Q_k·pr_k·A_(pix))^(0,56)·K_k·LS_k·C_k·P_k",
    "SY = c₁ · Σₖ E_unit,k  +  c₂ · (Qb_inicio · T_chuva · 3600)": "SY=c_1·∑_(k)▒E_(unit,k)+c_2·(Qb_(inicio)·T_(chuva)·3600)",
    "mínimo de Σₙ [ ln(SY_obs,n) − ln(c₁ · Σ E_unit,n + c₂ · V_ref,n) ]²,  com c₁ ≥ 0 e c₂ ≥ 0":
        '"mín" ∑_(n)▒[ln(SY_(obs,n))−ln(c_1·E_(unit,n)+c_2·V_(ref,n))]^2," , com "c_1≥0" e "c_2≥0',
}
'''
if "LINEAR = {" not in s:
    s = s.replace("TOKEN = re.compile(", LINEAR + "\nTOKEN = re.compile(", 1)

# estilo Equacao
if '"Equacao"' not in s:
    s = s.replace('doc.styles["Heading 1"].font.all_caps = True',
                  'doc.styles["Heading 1"].font.all_caps = True\nfrom docx.enum.style import WD_STYLE_TYPE\n_eq_st = doc.styles.add_style("Equacao", WD_STYLE_TYPE.PARAGRAPH); _eq_st.base_style = doc.styles["Normal"]', 1)

old = '''                eq = bool(re.search(r"[=·]", b)) and len(b) < 120 and not b.startswith(("**", "Nota", "[", "Esboço"))
                if eq:'''
new = '''                if b in LINEAR:
                    p.style = doc.styles["Equacao"]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(6)
                    p.add_run(LINEAR[b])
                    continue
                eq = bool(re.search(r"[=·]", b)) and len(b) < 120 and not b.startswith(("**", "Nota", "[", "Esboço"))
                if eq:'''
assert old in s
s = s.replace(old, new, 1)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
