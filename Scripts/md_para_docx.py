"""
Converte o rascunho do TCC (Markdown simples) em .docx no formato da Informacao
CCPG 004/2017 (Unicamp, TCC lato sensu), adotado como modelo:

  - A4; Arial 12; justificado; espacamento 1,5 (texto e referencias);
    margens sup/esq 3,0 cm e inf/dir 2,0 cm; paragrafo 2,0 cm
  - pre-textuais sem numeracao (capa, folha de rosto, ficha, dedicatoria,
    agradecimentos, resumo, abstract, listas, sumario); todas contam como pagina
  - numeracao continua no canto superior direito a partir da Introducao
  - corpo; referencias; apendices

Preenche {{TABELA_SY}}, {{SY_MEDIA}}, {{SY_MIN}}, {{SY_MAX}} a partir de
Dados Iniciais/comparacao_SY_previsao_vs_restrito.csv.

Uso: python-qgis.bat md_para_docx.py entrada.md saida.docx
"""
import os
import re
import sys

import pandas as pd
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Cm, RGBColor

sys.stdout.reconfigure(encoding="utf-8")
src, dst = sys.argv[1], sys.argv[2]
txt = open(src, encoding="utf-8").read()
# {{INCLUDE:caminho}} insere o conteudo de um arquivo (relativo a pasta do .md), ex.: tabelas geradas por gerar_tabelas_tcc.py
txt = re.sub(r"\{\{INCLUDE:(.+?)\}\}", lambda m: open(os.path.join(os.path.dirname(os.path.abspath(src)), m.group(1)), encoding="utf-8").read().strip("\n"), txt)

# ------------------------------------------------------------------ dados
ptbr = lambda s: s.replace(",", "X").replace(".", ",").replace("X", ".")
cmp_ = pd.read_csv(r"C:\TCC\Dados Iniciais\comparacao_SY_previsao_vs_restrito.csv").sort_values("evento")
lin = ["| Evento | SY observado (t) | SY previsão pura (t) | Erro (%) | SY volume restrito (t) | Erro (%) |", "|---|---|---|---|---|---|"]
for _, r in cmp_.iterrows():
    lin.append(ptbr(f"| {int(r.evento)} | {r.SY_obs_t:,.1f} | {r.SY_previsao_t:,.1f} | {r['erro_previsao_%']:+.1f} | {r.SY_restrito_t:,.1f} | {r['erro_restrito_%']:+.1f} |"))
lin.append(ptbr(f"| **Total** | {cmp_.SY_obs_t.sum():,.1f} | {cmp_.SY_previsao_t.sum():,.1f} | | {cmp_.SY_restrito_t.sum():,.1f} | |"))
fmt = lambda v: ptbr(f"{v:,.1f}")
# tabela por evento do modelo de dois componentes e tabela da escada de informacao (rascunho 02)
try:
    b2 = pd.read_csv(r"C:\TCC\Dados Iniciais\comparacao_SY_dois_componentes.csv").sort_values("evento")
    lb = ["**Tabela 11.** Sedimento por evento (t): medido e simulado pelo modelo calculado, com a decomposição em encostas e vazão de base.", "",
          "| Evento | Medido | Encostas | Base | Total simulado | Erro no ajuste (%) | Erro na validação cruzada (%) |", "|---|---|---|---|---|---|---|"]
    for _, r in b2.iterrows():
        lb.append(ptbr(f"| {int(r.evento)} | {r.SY_obs_t:,.0f} | {r.SY_encostas_t:,.0f} | {r.SY_base_t:,.0f} | {r.SY_total_sim_t:,.0f} | {r.erro_pct:+.0f} | {r.erro_LOO_pct:+.0f} |"))
    tab_b = "\n".join(lb)
    es = pd.read_csv(r"C:\TCC\TCC_Texto\figuras\escada_gargalo.csv")
    cab = ["| Água | Modelo | Erro mediano (%) | Dentro de fator 2 (%) | NSE em log | Spearman |", "|---|---|---|---|---|---|"]
    nomes = {"N1": "Calculada da chuva", "N2": "N2: volume previsto por regressão", "N3": "N3: volume direto medido, base estimada", "N4": "Forçada ao medido"}
    le_ = ["**Tabela 13.** Desempenho do modelo de dois componentes e do teste simples com os mesmos insumos (validação cruzada; calibração em log).", ""] + cab
    li_ = [] + cab
    for _, r in es.iterrows():
        k = r.nivel.split(":")[0]
        linha_ = ptbr(f"| {nomes[k]} | {r.modelo} | {r.MedAPE:,.1f} | {r.fator2:,.0f} | {r.NSE_log:,.2f} | {r.Spearman:,.2f} |")
        (le_ if k in ("N1", "N4") else li_).append(linha_)
    tab_e = "\n".join(le_); tab_i = "\n".join(li_)
except Exception as e:
    tab_b = tab_e = tab_i = f"[PENDENTE: tabela nao gerada: {e}]"
txt = txt.replace("{{TABELA_B}}", tab_b).replace("{{TABELA_ESCADA}}", tab_e).replace("{{TABELA_INTERM}}", tab_i)
txt = (txt.replace("{{TABELA_SY}}", "\n".join(lin))
          .replace("{{SY_MEDIA}}", fmt(cmp_.SY_obs_t.mean()))
          .replace("{{SY_MIN}}", fmt(cmp_.SY_obs_t.min()))
          .replace("{{SY_MAX}}", fmt(cmp_.SY_obs_t.max())))

# ------------------------------------------------------------------ separa o md em blocos "## "
TITULO = re.search(r"^# (.+)$", txt, re.M).group(1)
partes = re.split(r"^## ", txt, flags=re.M)
cabeca, blocos = partes[0], partes[1:]
resumo = next((b for b in blocos if b.startswith("RESUMO")), None)
abstract = next((b for b in blocos if b.startswith("ABSTRACT")), None)
nota = re.search(r"^> \*\*Como ler este rascunho\.\*\*(.+)$", cabeca, re.M)
corpo = [b for b in blocos if b is not resumo and b is not abstract]

# ------------------------------------------------------------------ documento
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
sec.top_margin = sec.left_margin = Cm(3.0)
sec.bottom_margin = sec.right_margin = Cm(2.0)
FONTE = "Arial"
st = doc.styles["Normal"]
st.font.name = FONTE; st.font.size = Pt(12)
st.element.rPr.rFonts.set(qn("w:eastAsia"), FONTE)
st.paragraph_format.line_spacing = 1.5
st.paragraph_format.space_after = Pt(0)
for h in ("Heading 1", "Heading 2", "Heading 3"):
    hs = doc.styles[h]
    hs.font.name = FONTE; hs.font.size = Pt(12); hs.font.bold = True; hs.font.color.rgb = RGBColor(0, 0, 0)
    hs.element.rPr.rFonts.set(qn("w:eastAsia"), FONTE)
    for _att in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        hs.element.rPr.rFonts.attrib.pop(qn(_att), None)
    hs.element.rPr.rFonts.set(qn("w:ascii"), FONTE); hs.element.rPr.rFonts.set(qn("w:hAnsi"), FONTE)
    hs.paragraph_format.space_before = Pt(12); hs.paragraph_format.space_after = Pt(6)
    hs.paragraph_format.keep_with_next = True
doc.styles["Heading 1"].font.all_caps = True

TOKEN = re.compile(r"(\*\*.+?\*\*|\*.+?\*|`.+?`|\[PENDENTE[^\]]*\]|\[conferir[^\]]*\]|\[PREENCHER[^\]]*\]|\[completar[^\]]*\]|\[CIDADE\]|\[UNIDADE\]|\[CURSO\])")
HL = 7  # amarelo


SUBSUP = re.compile(r"(?<=[A-Za-z0-9ΣΔλµ₁₂)])(_[A-Za-z0-9]+(?:,[A-Za-z0-9]+)*|\^[−+-]?[0-9]+(?:,[0-9]+)?)")


def _add(par, texto, bold=False, italic=False, hl=False, size=None, bold_all=False):
    """adiciona texto convertendo X_abc em subscrito e X^0,56 em sobrescrito"""
    for pedaco in SUBSUP.split(texto):
        if not pedaco:
            continue
        sub = re.fullmatch(r"_[A-Za-z0-9]+(?:,[A-Za-z0-9]+)*", pedaco) is not None
        sup = re.fullmatch(r"\^[−+-]?[0-9]+(?:,[0-9]+)?", pedaco) is not None
        r = par.add_run(pedaco[1:] if (sub or sup) else pedaco)
        if sub:
            r.font.subscript = True
        if sup:
            r.font.superscript = True
        r.bold = bool(bold or bold_all) or None
        r.italic = True if italic else None
        if hl:
            r.font.highlight_color = HL
        if size:
            r.font.size = Pt(size)


def runs(par, s, bold_all=False, size=None):
    for part in TOKEN.split(s):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            _add(par, part[2:-2], bold=True, hl=("PENDENTE" in part or "conferir" in part), size=size, bold_all=bold_all)
        elif part.startswith("`") and part.endswith("`"):
            _add(par, part[1:-1], size=size, bold_all=bold_all)
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            _add(par, part[1:-1], italic=True, size=size, bold_all=bold_all)
        elif re.match(r"^\[(PENDENTE|conferir|PREENCHER|completar|CIDADE|UNIDADE|CURSO)", part):
            _add(par, part.replace("`", ""), hl=True, size=size, bold_all=bold_all)
        else:
            _add(par, part, size=size, bold_all=bold_all)


def centro(texto, negrito=False, tam=12, espaco_depois=0, antes=0, hl=False):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_after = Pt(espaco_depois); p.paragraph_format.space_before = Pt(antes)
    runs(p, texto)
    for r in p.runs:
        r.font.size = Pt(tam); r.bold = negrito or r.bold
        if hl:
            r.font.highlight_color = HL
    return p


def quebra():
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def titulo_pre(texto):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(18)
    r = p.add_run(texto); r.bold = True


def campo(par, instr):
    for tipo, val in (("begin", None), (None, instr), ("separate", None), ("end", None)):
        r = par.add_run()
        if tipo:
            e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), tipo)
        else:
            e = OxmlElement("w:instrText"); e.set(qn("xml:space"), "preserve"); e.text = val
        r._r.append(e)


# ---------------- 1. Primeira folha (capa)
centro("UNIVERSIDADE ESTADUAL DE CAMPINAS", True, 12)
centro("[UNIDADE]", False, 12, 150, hl=True)
centro("MATEUS VIVARELLI", True, 12, 120)
centro(TITULO.upper(), True, 14, 180)
centro("[CIDADE]", False, 12)
centro("2026", False, 12)
centro("Rascunho 01 — 15/10/2026", False, 9, 0, 24, hl=True)
quebra()

# ---------------- 2. Folha de rosto
centro("MATEUS VIVARELLI", True, 12, 90)
centro(TITULO.upper(), True, 14, 60)
p = doc.add_paragraph(); p.paragraph_format.left_indent = Cm(8.0); p.paragraph_format.line_spacing = 1.0
p.paragraph_format.space_after = Pt(36)
runs(p, "Trabalho de conclusão de curso apresentado à [UNIDADE] da Universidade Estadual de Campinas como parte dos requisitos exigidos para a obtenção do título de [CURSO].", size=11)
p = doc.add_paragraph(); p.paragraph_format.line_spacing = 1.0; p.paragraph_format.space_after = Pt(60)
r = p.add_run("ESTE EXEMPLAR CORRESPONDE À VERSÃO FINAL DO TRABALHO APRESENTADO PELO ALUNO MATEUS VIVARELLI E ORIENTADO PELO(A) PROF(A). DR(A). "); r.font.size = Pt(10)
r = p.add_run("[PREENCHER: nome do orientador]"); r.font.size = Pt(10); r.font.highlight_color = HL
centro("[CIDADE]", False, 12)
centro("2026", False, 12)
quebra()

# ---------------- 3. Ficha catalografica (verso)
centro("[PENDENTE: ficha catalográfica — solicitar à biblioteca da Unidade após as correções, pelo formulário do site do SBU (http://www.sbu.unicamp.br, \"Solicitar Ficha Catalográfica\"). Deve ser impressa no verso da folha de rosto.]", False, 11, 0, 200)
quebra()

# ---------------- 4. Dedicatoria / 5. Agradecimentos (opcionais)
titulo_pre("DEDICATÓRIA")
centro("[opcional]", False, 11, hl=True)
quebra()
titulo_pre("AGRADECIMENTOS")
centro("[opcional]", False, 11, hl=True)
quebra()


# ---------------- Resumo / Abstract
def bloco_simples(bloco):
    linhas = bloco.strip().split("\n")
    titulo_pre(linhas[0].strip())
    for ln in linhas[1:]:
        if not ln.strip():
            continue
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        palavras = ln.startswith("**Palavras") or ln.startswith("**Keywords")
        if palavras:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.5 if palavras else 1.0
        if not ln.startswith("**"):
            p.paragraph_format.first_line_indent = Cm(2.0)
        runs(p, ln)


if resumo:
    bloco_simples(resumo); quebra()
if abstract:
    bloco_simples(abstract); quebra()

# ---------------- Listas
titulo_pre("LISTA DE ABREVIATURAS E SIGLAS")
siglas = [
    ("AMC", "Condição de umidade antecedente (*Antecedent Moisture Condition*)"),
    ("CN", "Número de curva (*Curve Number*)"),
    ("CSS", "Concentração de sedimentos em suspensão"),
    ("D8", "Algoritmo de direção de fluxo de oito direções"),
    ("DSC", "Grau de conectividade de sedimentos (*Degree of Sediment Connectivity*)"),
    ("FCI", "Índice de conectividade funcional (*Functional Connectivity Index*)"),
    ("HU", "Hidrograma unitário"),
    ("IC", "Iniciação Científica"),
    ("IDW", "Interpolação pelo inverso da distância (*Inverse Distance Weighting*)"),
    ("MDE", "Modelo digital de elevação"),
    ("MUSLE", "Equação Universal Modificada de Perda de Solo"),
    ("NSE", "Eficiência de Nash-Sutcliffe"),
    ("PBIAS", "Viés percentual (*Percent Bias*)"),
    ("SCS-CN", "Método do número de curva do Soil Conservation Service"),
    ("SIG", "Sistema de Informação Geográfica"),
    ("USLE", "Equação Universal de Perda de Solo"),
    ("WIA", "Índice de concordância de Willmott"),
]
simb = [
    ("A_pix", "Área do pixel (m²)"), ("C", "Fator de cobertura e manejo (–)"), ("c", "Fator de escala empírico de calibração (–)"),
    ("E_unit", "Erosão local por pixel, não calibrada (t)"), ("K", "Erodibilidade do solo (t·h/MJ/mm)"),
    ("LS", "Fator topográfico (–)"), ("P", "Chuva (mm); como fator da MUSLE, práticas conservacionistas (–)"),
    ("pr", "Vazão de pico local do pixel (m³/s)"), ("Q", "Escoamento superficial (mm)"),
    ("qp", "Vazão de pico (m³/s)"), ("R", "Lâmina de chuva do evento (mm)"),
    ("RI", "Intensidade máxima de chuva em 60 min (mm/h)"), ("S", "Retenção potencial máxima do SCS-CN (mm)"),
    ("SY", "Produção de sedimentos (t)"), ("λ", "Razão de abstração inicial (–)"),
]
for titulo_lista, itens in (("LISTA DE ABREVIATURAS E SIGLAS", siglas), ("LISTA DE SÍMBOLOS", simb)):
    titulo_pre(titulo_lista)
    for a, b in itens:
        p = doc.add_paragraph(); p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.left_indent = Cm(3.0); p.paragraph_format.first_line_indent = Cm(-3.0)
        r = p.add_run(a + "\t"); r.bold = True
        runs(p, b)
    quebra()

# ---------------- Sumario (campo TOC; o Word atualiza ao abrir)
titulo_pre("SUMÁRIO")
p = doc.add_paragraph()
campo(p, 'TOC \\o "1-2" \\h \\z \\u')
quebra()

# ---------------- Nota do rascunho (remover na versao final)
titulo_pre("NOTA SOBRE ESTE RASCUNHO (remover na versão final)")
if nota:
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY; p.paragraph_format.line_spacing = 1.15
    runs(p, nota.group(1).strip())
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY; p.paragraph_format.line_spacing = 1.15
runs(p, "Formato seguido: Informação CCPG nº 004/2017 (Unicamp), A4, Arial 12, justificado, espaçamento 1,5, margens 3/3/2/2 cm, parágrafo de 2 cm, páginas pré-textuais contadas e não numeradas. **[PENDENTE: confirmar com a coordenação se o curso exige modelo próprio e Termo de Autorização.]**")

# ---------------- Secao textual (numeracao a partir daqui)
sec2 = doc.add_section(WD_SECTION.NEW_PAGE)
sec2.header.is_linked_to_previous = False
hp = sec2.header.paragraphs[0]; hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
campo(hp, "PAGE")
for r in hp.runs:
    r.font.size = Pt(12); r.font.name = FONTE


# ------------------------------------------------------------------ corpo
def render(lines):
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("!["):
            mm = re.match(r"!\[(.*?)\]\((.*?)\)", ln)
            global FIGN
            FIGN += 1
            pic = doc.add_paragraph(); pic.alignment = WD_ALIGN_PARAGRAPH.CENTER; pic.paragraph_format.line_spacing = 1.0
            pic.paragraph_format.keep_with_next = True
            pic.add_run().add_picture(os.path.join(os.path.dirname(os.path.abspath(src)), mm.group(2)), width=Cm(15.5))
            cap = doc.add_paragraph(); cap.alignment = WD_ALIGN_PARAGRAPH.CENTER; cap.paragraph_format.line_spacing = 1.0
            cap.paragraph_format.space_after = Pt(10)
            runs(cap, f"**Figura {FIGN}.** {mm.group(1)}", size=10)
        elif ln.startswith("### "):
            doc.add_heading(ln[4:], level=2)
        elif ln.strip() in ("---", ""):
            pass
        elif ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            rows = [r for r in rows if not all(re.fullmatch(r":?-+:?", c) for c in r)]
            t = doc.add_table(rows=len(rows), cols=len(rows[0])); t.style = "Table Grid"; t.autofit = False
            ncol = len(rows[0]); total_cm = 16.0
            limpa = lambda c: re.sub(r"[*`]", "", c)
            tam = 8 if ncol >= 10 else (9 if ncol >= 7 else 10)
            cw = {8: 0.165, 9: 0.185, 10: 0.205}[tam]            # largura media de um caractere (cm)
            palavra = [max(len(w_) * (1.25 if r is rows[0] else 1.0) for r in rows for w_ in re.split(r"\s+", limpa(r[k])) if w_) for k in range(ncol)]
            pref = [min(max(len(limpa(r[k])) for r in rows), 34) for k in range(ncol)]
            minimo = [palavra[k] * cw + 0.3 for k in range(ncol)]
            if sum(minimo) > total_cm:
                minimo = [m_ * total_cm / sum(minimo) for m_ in minimo]
            sobra = total_cm - sum(minimo)
            extra = [max(pref[k] * cw + 0.3 - minimo[k], 0.0) for k in range(ncol)]
            larg_cm = [minimo[k] + (sobra * extra[k] / sum(extra) if sum(extra) > 0 else sobra / ncol) for k in range(ncol)]
            larg = [Cm(v_) for v_ in larg_cm]
            for k in range(ncol):
                t.columns[k].width = larg[k]
            numerico = re.compile(r"^[+−\-]?[0-9.]+(,[0-9]+)?%?( \(.*\))?$|^—$|^[0-9.,]+ (mm|m³|t|h)$")
            for a, row in enumerate(rows):
                tr = t.rows[a]._tr
                trPr = tr.get_or_add_trPr()
                cs = OxmlElement("w:cantSplit"); trPr.append(cs)
                if a == 0:
                    th = OxmlElement("w:tblHeader"); trPr.append(th)
                for b, c in enumerate(row):
                    cell = t.cell(a, b); cell.text = ""; cell.width = larg[b]
                    cp = cell.paragraphs[0]; cp.paragraph_format.line_spacing = 1.0
                    cp.paragraph_format.space_before = Pt(1); cp.paragraph_format.space_after = Pt(1)
                    if a > 0 and numerico.match(limpa(c).strip()):
                        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    if a == 0:
                        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), "D9E2F3")
                        cell._tc.get_or_add_tcPr().append(shd)
                    runs(cp, c, bold_all=(a == 0), size=tam)
            doc.add_paragraph().paragraph_format.line_spacing = 1.0
            continue
        elif ln.startswith(">"):
            block = []
            while i < len(lines) and lines[i].startswith(">"):
                block.append(lines[i][1:].strip()); i += 1
            for b in block:
                if not b:
                    continue
                p = doc.add_paragraph(); p.paragraph_format.line_spacing = 1.0
                p.paragraph_format.space_after = Pt(6)
                eq = bool(re.search(r"[=·]", b)) and len(b) < 120 and not b.startswith(("**", "Nota", "[", "Esboço"))
                if eq:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    _add(p, b, italic=True)
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                    p.paragraph_format.left_indent = Cm(4.0)   # citacao longa / nota: recuo de 4 cm, espaco simples
                    runs(p, b, size=10)
            continue
        elif re.match(r"^\d+\. ", ln):
            p = doc.add_paragraph(style="List Number"); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            runs(p, re.sub(r"^\d+\. ", "", ln))
        elif ln.startswith("- "):
            p = doc.add_paragraph(style="List Bullet"); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            runs(p, ln[2:])
        elif ln.startswith("**Tabela"):
            p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.LEFT; p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(4); p.paragraph_format.keep_with_next = True
            runs(p, ln, size=10)
        else:
            p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Cm(2.0)
            runs(p, ln)
        i += 1


FIGN = 0
primeiro = True
for b in corpo:
    ls = b.split("\n")
    titulo = ls[0].strip()
    if not primeiro and titulo.startswith(("REFERÊNCIAS", "APÊNDICE", "6.", "7.")):
        quebra()
    primeiro = False
    doc.add_heading(titulo, level=1)
    render(ls[1:])


doc.save(dst)
print("salvo:", dst)
