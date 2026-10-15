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

# ------------------------------------------------------------------ dados
ptbr = lambda s: s.replace(",", "X").replace(".", ",").replace("X", ".")
cmp_ = pd.read_csv(r"C:\TCC\Dados Iniciais\comparacao_SY_previsao_vs_restrito.csv").sort_values("evento")
lin = ["| Evento | SY observado (t) | SY previsão pura (t) | Erro (%) | SY volume restrito (t) | Erro (%) |", "|---|---|---|---|---|---|"]
for _, r in cmp_.iterrows():
    lin.append(ptbr(f"| {int(r.evento)} | {r.SY_obs_t:,.1f} | {r.SY_previsao_t:,.1f} | {r['erro_previsao_%']:+.1f} | {r.SY_restrito_t:,.1f} | {r['erro_restrito_%']:+.1f} |"))
lin.append(ptbr(f"| **Total** | {cmp_.SY_obs_t.sum():,.1f} | {cmp_.SY_previsao_t.sum():,.1f} | | {cmp_.SY_restrito_t.sum():,.1f} | |"))
fmt = lambda v: ptbr(f"{v:,.1f}")
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
    hs.paragraph_format.space_before = Pt(12); hs.paragraph_format.space_after = Pt(6)
    hs.paragraph_format.keep_with_next = True
doc.styles["Heading 1"].font.all_caps = True

TOKEN = re.compile(r"(\*\*.+?\*\*|\*.+?\*|`.+?`|\[PENDENTE[^\]]*\]|\[conferir[^\]]*\]|\[PREENCHER[^\]]*\]|\[completar[^\]]*\]|\[CIDADE\]|\[UNIDADE\]|\[CURSO\])")
HL = 7  # amarelo


def runs(par, s, bold_all=False, size=None):
    for part in TOKEN.split(s):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            r = par.add_run(part[2:-2]); r.bold = True
            if "PENDENTE" in part or "conferir" in part:
                r.font.highlight_color = HL
        elif part.startswith("`") and part.endswith("`"):
            r = par.add_run(part[1:-1]); r.font.name = "Consolas"
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            r = par.add_run(part[1:-1]); r.italic = True
        elif re.match(r"^\[(PENDENTE|conferir|PREENCHER|completar|CIDADE|UNIDADE|CURSO)", part):
            r = par.add_run(part.replace("`", "")); r.font.highlight_color = HL
        else:
            r = par.add_run(part)
        if bold_all:
            r.bold = True
        if size:
            r.font.size = Pt(size)


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
        if ln.startswith("### "):
            doc.add_heading(ln[4:], level=2)
        elif ln.strip() in ("---", ""):
            pass
        elif ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            rows = [r for r in rows if not all(re.fullmatch(r":?-+:?", c) for c in r)]
            t = doc.add_table(rows=len(rows), cols=len(rows[0])); t.style = "Table Grid"
            for a, row in enumerate(rows):
                for b, c in enumerate(row):
                    cell = t.cell(a, b); cell.text = ""
                    cp = cell.paragraphs[0]; cp.paragraph_format.line_spacing = 1.0
                    runs(cp, c, bold_all=(a == 0), size=10)
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
                    r = p.add_run(b); r.italic = True
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
        else:
            p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Cm(2.0)
            runs(p, ln)
        i += 1


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
