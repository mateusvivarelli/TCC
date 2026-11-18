"""Acrescenta ao PowerPoint do autor (modelo FECFAU, layout "Titulo e Conteudo") os slides sugeridos:
o slide de solo e uso depois do mapa grande da bacia (slide 8) e os slides de resultados em diante.
Os slides 1 a 19 do autor nao sao alterados. Tambem troca a fonte do tema (Aptos) por Calibri.

Entrada: Apresentacao/slideTCC_18-11.pptx
Saida:   Apresentacao/slideTCC_18-11_sugestoes.pptx
Uso: python Scripts/slides_defesa/4_slides_no_modelo_do_autor.py  (depois de 1_figuras_slides.py e 2_monta_slides.js)
"""
import copy
import os
import re

from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FIG = os.path.join(BASE, "TCC_Texto", "figuras")
SRC = os.path.join(BASE, "Apresentacao", "slideTCC_18-11.pptx")
DST = os.path.join(BASE, "Apresentacao", "slideTCC_18-11_sugestoes.pptx")
REF = os.path.join(BASE, "TCC_Texto", "slides", "slides_defesa_completo.pptx")   # de onde vem a fala (anotacoes)

TEXT, MUTED, ORANGE, BLUE, TINT, LINE, WHITE = "262626", "5F6670", "C77B12", "3D85C6", "EEF3FA", "C9D3E0", "FFFFFF"
X0, W, Y0 = 0.58, 12.17, 1.95       # area de conteudo abaixo da faixa azul
FONTE_Y = 6.85

p = Presentation(SRC)
LAY = p.slide_layouts[1]           # Titulo e Conteudo (faixa azul + logo)

# ---- fala dos slides: anotacoes do deck de referencia, pelo titulo
falas = {}
for s in Presentation(REF).slides:
    tit = [sh.text_frame.text for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
    if s.has_notes_slide and len(tit) > 1:
        falas[tit[1].strip()] = s.notes_slide.notes_text_frame.text


def rgb(h):
    return RGBColor.from_string(h)


NOVOS = []


def novo(titulo, fala_de=None, fala=None):
    s = p.slides.add_slide(LAY); NOVOS.append(s)
    s.shapes.title.text = titulo
    for ph in list(s.placeholders):
        if ph.placeholder_format.idx != 0:
            ph._element.getparent().remove(ph._element)
    txt = fala if fala is not None else falas.get(fala_de or "", "")
    if txt:
        s.notes_slide.notes_text_frame.text = txt
    return s


def runs_md(par, texto, size, color=TEXT, bold=False, italic=False, font=None):
    """texto com _{sub} e ^{sup}"""
    pos = 0
    for m in list(re.finditer(r"([_^])\{([^}]*)\}", texto)) + [None]:
        fim = m.start() if m else len(texto)
        pedacos = [(texto[pos:fim], None)]
        if m:
            pedacos.append((m.group(2), "-25000" if m.group(1) == "_" else "30000"))
            pos = m.end()
        for t, base in pedacos:
            if not t:
                continue
            r = par.add_run(); r.text = t
            f = r.font; f.size = Pt(size); f.bold = bold; f.italic = italic; f.color.rgb = rgb(color)
            if font:
                f.name = font
            if base:
                r._r.get_or_add_rPr().set("baseline", base)


def caixa_texto(s, x, y, w, h, linhas, size=16, color=TEXT, bold=False, italic=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font=None, espaco=6):
    """linhas: lista de str ou de listas [(texto, {opcoes})]"""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    for a in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, a, 0)
    for i, ln in enumerate(linhas if isinstance(linhas, list) else [linhas]):
        par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        par.alignment = align; par.space_after = Pt(espaco)
        partes = ln if isinstance(ln, list) else [(ln, {})]
        for t, o in partes:
            runs_md(par, t, o.get("size", size), o.get("color", color), o.get("bold", bold), o.get("italic", italic), o.get("font", font))
    return tb


def marcadores(s, x, y, w, h, itens, size=16, color=TEXT):
    tb = caixa_texto(s, x, y, w, h, itens, size=size, color=color, espaco=8)
    for par in tb.text_frame.paragraphs:
        pPr = par._p.get_or_add_pPr(); pPr.set("marL", "228600"); pPr.set("indent", "-228600")
        bu = etree.SubElement(pPr, qn("a:buChar")); bu.set("char", "•")
    return tb


def retangulo(s, x, y, w, h, fill=TINT, line=LINE):
    r = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    r.adjustments[0] = 0.06
    r.fill.solid(); r.fill.fore_color.rgb = rgb(fill)
    r.line.color.rgb = rgb(line); r.line.width = Pt(1); r.shadow.inherit = False
    r.text_frame.text = ""
    return r


def cartao(s, x, y, w, h, titulo, corpo, fill=TINT, line=LINE, cor_titulo=BLUE, size=15, centro=False):
    retangulo(s, x, y, w, h, fill, line)
    al = PP_ALIGN.CENTER if centro else PP_ALIGN.LEFT
    caixa_texto(s, x + 0.15, y + 0.12, w - 0.3, h - 0.24, [[(titulo, {"bold": True, "color": cor_titulo, "size": size + 2})], corpo],
                size=size, align=al, anchor=MSO_ANCHOR.MIDDLE if centro else MSO_ANCHOR.TOP)


def equacao(s, x, y, w, h, texto, size=20):
    retangulo(s, x, y, w, h)
    caixa_texto(s, x + 0.1, y, w - 0.2, h, texto.split("\n"), size=size, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, font="Cambria Math", espaco=0)


def numero(s, x, y, w, grande, pequeno, cor=TEXT):
    caixa_texto(s, x, y, w, 0.75, [grande], size=38, bold=True, color=cor, anchor=MSO_ANCHOR.BOTTOM)
    caixa_texto(s, x, y + 0.78, w, 0.7, [pequeno], size=14, color=MUTED)


def imagem(s, rel, x, y, w, h):
    f = os.path.join(FIG, rel); iw, ih = Image.open(f).size; r = iw / ih
    ww, hh = (w, w / r) if w / r <= h else (h * r, h)
    s.shapes.add_picture(f, Inches(x + (w - ww) / 2), Inches(y + (h - hh) / 2), Inches(ww), Inches(hh))


def fonte(s, texto):
    caixa_texto(s, X0, FONTE_Y, W, 0.45, [texto], size=10, color=MUTED, italic=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def grafico_barras(s, x, y, w, h, titulo, cats, series, cores):
    cd = CategoryChartData(); cd.categories = cats
    for nome, vals in series:
        cd.add_series(nome, vals)
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    ch = gf.chart
    ch.has_title = True; ch.chart_title.text_frame.text = titulo
    tp = ch.chart_title.text_frame.paragraphs[0]; tp.runs[0].font.size = Pt(14); tp.runs[0].font.bold = True; tp.runs[0].font.name = "Calibri"
    ch.has_legend = len(series) > 1
    if ch.has_legend:
        ch.legend.position = XL_LEGEND_POSITION.TOP; ch.legend.include_in_layout = False
        ch.legend.font.size = Pt(12); ch.legend.font.name = "Calibri"
    for ax in (ch.category_axis, ch.value_axis):
        ax.tick_labels.font.size = Pt(11); ax.tick_labels.font.name = "Calibri"; ax.tick_labels.font.color.rgb = rgb(MUTED)
    ch.value_axis.major_gridlines.format.line.color.rgb = rgb("E3E7ED")
    ch.value_axis.tick_labels.number_format = "#,##0"; ch.value_axis.tick_labels.number_format_is_linked = False
    plot = ch.plots[0]; plot.gap_width = 45
    for ser, cor in zip(plot.series, cores):
        ser.format.fill.solid(); ser.format.fill.fore_color.rgb = rgb(cor)
    return ch


def mover(slide, depois_de):
    """move o slide recem-criado para logo depois da posicao 'depois_de' (1 = primeiro)"""
    lst = p.slides._sldIdLst; el = lst[-1]; lst.remove(el); lst.insert(depois_de, el)


# =============================================================== slide 9 (depois do mapa grande): solo e uso
s = novo("Introdução: solo e uso", "Solo e uso do solo na parte alta da bacia")
imagem(s, "mapas/mapa_02_solo_uso.png", X0, 1.85, W, 4.0)
caixa_texto(s, X0, 5.95, W, 0.8, [[("Solo: ", {"bold": True, "color": BLUE}), ("Cambissolos Háplicos em 69% da área (K = 0,0475) e Argissolos Vermelho-Amarelos em 18% (K = 0,0351)", {})],
                                 [("Uso: ", {"bold": True, "color": BLUE}), ("mata nativa 40%, campo 29%, área urbana 14%, silvicultura 13%, lavoura temporária 4%", {})]], size=15)
fonte(s, "Fonte: elaborado pelo autor, com os mapas de solo e de uso do Plano de Bacias (Consórcio Profill-Rhama, 2020)")
mover(s, 8)

# =============================================================== resultados
s = novo("Resultados: modelo calculado (MC)", "Modelo calculado: pior que a regra simples com a chuva")
imagem(s, "slides/dispersao_simples_e_MC.png", X0, 1.85, 8.3, 4.9)
caixa_texto(s, 9.1, 1.95, 3.65, 0.4, ["Mesma informação: só a chuva"], size=16, bold=True, color=BLUE)
numero(s, 9.1, 2.35, 3.65, "81% × 42%", "erro mediano: MC × regra simples com a chuva")
numero(s, 9.1, 3.75, 3.65, "35% × 82%", "eventos dentro de fator 2")
caixa_texto(s, 9.1, 5.2, 3.65, 1.5, ["O MC foi pior em 14 dos 17 eventos (Wilcoxon, p = 0,02): de 10% do medido (evento 10) a 3,1 vezes (evento 9)."], size=14)
fonte(s, "Fonte: elaborado pelo autor (validação cruzada, 17 eventos)")

s = novo("Resultados: o erro vem do escoamento", "O erro vem do escoamento calculado")
med = [224, 1731, 585, 987, 832, 183, 650, 1250, 801, 552, 1479, 101, 735, 931, 2177, 1595, 449]
calc = [36, 521, 751, 154, 695, 158, 142, 1336, 1725, 57, 997, 63, 1073, 1363, 3963, 1934, 734]
grafico_barras(s, X0, 1.8, 7.6, 5.0, "Escoamento direto por evento (mil m³)", [str(i) for i in range(1, 18)],
               [("Medido", med), ("Calculado (SCS-CN)", calc)], [BLUE, "E39B3A"])
numero(s, 8.5, 1.85, 2.0, "+3%", "no total dos 17 eventos")
numero(s, 10.6, 1.85, 2.15, "46%", "de erro mediano em cada evento", ORANGE)
marcadores(s, 8.5, 3.45, 4.25, 3.3, [
    "Superestima as chuvas grandes (9, 15) e subestima as pequenas (1, 4, 7, 10): os erros se compensam no total",
    "Em 15 de 17 eventos, o sedimento erra no mesmo sentido do escoamento",
    "A erosão cresce com Q^{1,12}: o erro do escoamento chega ao sedimento um pouco ampliado",
    "Baert et al. (2026): MUSLE com escoamento previsto teve NSE ≈ 0; com o medido, 0,66",
], size=14)
fonte(s, "Fontes: elaborado pelo autor; Baert et al. (2026). Escoamento direto medido = volume total menos a vazão de base")

s = novo("Resultados: modelo forçado ao medido (MFM)", "Modelo forçado ao medido (MFM): troca só o escoamento")
etapas = [("Chuva IDW", ""), ("SCS-CN", "padrão espacial"), ("Q × f", "f = V medido / V calculado"), ("Williams e c", "c recalibrado")]
for i, (a, b) in enumerate(etapas):
    x = X0 + i * 3.1
    destaque = i == 2
    cartao(s, x, 2.0, 2.7, 1.2, a, b, fill="FCEFD9" if destaque else TINT, line="E8C79A" if destaque else LINE, cor_titulo=ORANGE if destaque else BLUE, centro=True)
    if i < 3:
        seta = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + 2.78), Inches(2.45), Inches(0.24), Inches(0.3))
        seta.fill.solid(); seta.fill.fore_color.rgb = rgb(BLUE); seta.line.fill.background()
caixa_texto(s, X0, 3.6, 6, 0.4, ["Evento 11"], size=17, bold=True, color=BLUE)
numero(s, X0, 4.0, 3.2, "f = 1,48", "1.479 / 997 mil m³")
numero(s, X0 + 3.6, 4.0, 3.6, "1,55 ×", "a soma do índice (1,48 elevado a 1,12)")
numero(s, X0 + 7.6, 4.0, 4.4, "1.387 t", "validação cruzada, c = 0,0222 (−24% do medido)")
caixa_texto(s, X0, 5.75, W, 0.9, ["O MFM não é uma previsão: usa o volume medido no mesmo hidrograma em que se mede a carga. Serve para isolar o efeito do escoamento."], size=16, italic=True, color=BLUE)
fonte(s, "Fonte: elaborado pelo autor")

s = novo("Resultados: com o escoamento medido", "Com o escoamento medido, o erro cai de 81% para 21%")
imagem(s, "slides/escada_gargalo_vivarelli.png", X0, 1.8, W, 3.6)
cartao(s, X0, 5.5, 5.95, 1.25, "MFM × regra com o volume medido", "21% × 16% de erro mediano; diferença de +1,6 pontos (IC 95%: −5,5 a +10,4; p = 0,52): não se distinguem", size=13)
cartao(s, X0 + 6.22, 5.5, 5.95, 1.25, "MFM × modelo concentrado (Vivarelli et al., 2025)", "21% × 22%: mesma ordem. Comparação indicativa: o concentrado foi ajustado nos próprios eventos, sem validação cruzada", size=13)
fonte(s, "Fonte: elaborado pelo autor; modelo concentrado com os valores originais de Vivarelli et al. (2025)")

s = novo("Resultados: métricas de desempenho", "Como medimos o desempenho")
cards = [
    ("Erro percentual mediano", "|S − O| / O em cada evento; mediana dos 17", "Quanto o modelo erra num evento típico; a mediana não deixa poucos eventos dominarem", "ideal: 0%"),
    ("Fator 2", "% de eventos com S entre O/2 e 2·O", "Quantos eventos ficam na ordem de grandeza certa", "ideal: 100%"),
    ("NSE (em log)", "1 − Σ(ln O − ln S)^{2} / Σ(ln O − ln Ō)^{2}", "Compara o modelo com prever sempre a média; em log, pesa o erro relativo", "1 = perfeito; 0 = média; < 0 = pior"),
    ("Spearman", "correlação entre as posições dos eventos", "Se o modelo ordena os eventos do menor ao maior", "ideal: 1"),
    ("R²", "fração da variação explicada por uma regressão", "O que explica a carga (volume: 88%) e o padrão do mapa", "de 0 a 1"),
    ("Validação cruzada", "deixa um evento de fora e ajusta c nos outros 16", "Todas as métricas usam a previsão do evento que ficou de fora", "17 rodadas"),
]
cw, ch_ = 3.9, 2.3
for i, (a, f_, d, ideal) in enumerate(cards):
    x = X0 + (i % 3) * (cw + 0.235); y = 1.9 + (i // 3) * (ch_ + 0.18)
    retangulo(s, x, y, cw, ch_)
    caixa_texto(s, x + 0.15, y + 0.1, cw - 0.3, 0.4, [a], size=17, bold=True, color=BLUE)
    caixa_texto(s, x + 0.15, y + 0.52, cw - 0.3, 0.45, [f_], size=13, font="Cambria Math")
    caixa_texto(s, x + 0.15, y + 1.0, cw - 0.3, 0.85, [d], size=13)
    caixa_texto(s, x + 0.15, y + 1.88, cw - 0.3, 0.35, [ideal], size=13, bold=True, color=ORANGE)
fonte(s, "Fonte: elaborado pelo autor. Nash e Sutcliffe (1970); Cawley e Talbot (2010). O = carga observada; S = carga simulada")

s = novo("Resultados: comparação dos modelos", "Desempenho de todos os modelos")
linhas_t = [["Modelo", "Informação medida", "Erro mediano", "Fator 2", "NSE log", "Spearman"],
            ["Regra simples com a chuva", "chuva", "41,9%", "82%", "0,53", "0,63"],
            ["MC (MUSLE espacializada)", "chuva", "81,1%", "35%", "−0,69", "0,59"],
            ["Regra simples com o volume", "escoamento direto", "15,9%", "94%", "0,85", "0,90"],
            ["MFM (MUSLE espacializada)", "escoamento direto", "20,6%", "94%", "0,84", "0,83"],
            ["Concentrado (Vivarelli et al., 2025)", "volume total e pico", "22,5%", "100%", "0,91", "0,93"]]
tb = s.shapes.add_table(6, 6, Inches(X0), Inches(1.95), Inches(W), Inches(3.3)).table
for j, wj in enumerate([3.9, 2.5, 1.55, 1.3, 1.4, 1.52]):
    tb.columns[j].width = Inches(wj)
for i, row in enumerate(linhas_t):
    for j, v in enumerate(row):
        c = tb.cell(i, j); c.text = v
        par = c.text_frame.paragraphs[0]; par.alignment = PP_ALIGN.CENTER
        r = par.runs[0]; r.font.size = Pt(16); r.font.bold = i == 0; r.font.color.rgb = rgb(WHITE if i == 0 else TEXT)
        c.fill.solid(); c.fill.fore_color.rgb = rgb(BLUE if i == 0 else (TINT if i % 2 == 0 else WHITE))
        c.vertical_anchor = MSO_ANCHOR.MIDDLE
marcadores(s, X0, 5.45, W, 1.3, [
    "Com a mesma informação (só a chuva), a regra simples supera o MC",
    "Com o escoamento medido, MFM e regra com o volume não se distinguem (diferença de +1,6 pontos; p = 0,52)",
    "O concentrado foi ajustado nos próprios eventos, sem validação cruzada: comparação indicativa",
], size=15)
fonte(s, "Fonte: elaborado pelo autor (Tabela 13 do TCC). Validação cruzada, exceto o modelo concentrado")

s = novo("Resultados: áreas críticas", "Mapa de erosão média e áreas críticas")
imagem(s, "slides/mapa_medio_e_criticas_MC.png", X0, 1.8, 5.4, 5.0)
numero(s, 6.3, 1.85, 3.1, "46% → 83%", "campo, silvicultura e lavoura temporária: % da área → % da erosão")
numero(s, 9.6, 1.85, 3.1, "93%", "da erosão vem dos Cambissolos Háplicos (69% da área)")
numero(s, 6.3, 3.4, 3.1, "65% → 78%", "encostas acima de 20%: % da área → % da erosão")
numero(s, 9.6, 3.4, 3.1, "94%", "das áreas críticas coincidem no MC e no MFM (r = 0,98)", ORANGE)
marcadores(s, 6.3, 5.0, 6.45, 1.8, [
    "Padrão espacial: 37% dos fatores K, LS e C e 63% do escoamento (chuva e CN), em escala log",
    "Mapa relativo: K e C adotados, área urbana sem erosão, sem validação espacial",
    "Mostra onde a erosão é produzida, não onde o sedimento chega ao rio",
], size=14)
fonte(s, "Fonte: elaborado pelo autor. Erosão média dos 17 eventos (MC); áreas críticas = 5% dos pixels de maior erosão")

s = novo("Resultados: sedimento por evento", "Sedimento estimado em cada evento (MC)")
imagem(s, "slides/mapa_17_eventos_MC.png", X0, 1.8, 9.3, 5.0)
marcadores(s, 10.1, 2.0, 2.65, 4.8, [
    "As mesmas manchas se repetem em todos os eventos",
    "A intensidade acompanha a chuva: eventos 8, 9, 15 e 16 os mais fortes",
    "Pouca chuva (1, 4, 6, 7, 10 e 12): erosão baixa em quase toda a bacia",
    "Cabeceira a leste: pouca erosão (menos chuva, CN baixo, mata)",
], size=14)
fonte(s, "Fonte: elaborado pelo autor. Mesma escala de cores em todos os eventos")

s = novo("Resultados: sedimento médio", "Sedimento médio dos 17 eventos (MC)")
imagem(s, "slides/mapa_medio_MC.png", X0, 1.8, W, 5.0)
fonte(s, "Fonte: elaborado pelo autor. Média, em cada pixel, do sedimento estimado nos 17 eventos (kg por pixel de 897 m²)")

# =============================================================== conclusoes e limitacoes
s = novo("Conclusões", "Conclusões")
marcadores(s, X0, 2.0, 5.6, 4.8, [
    "A conversão da chuva em escoamento é o principal limite: com a chuva, o MC erra 81%; com o volume medido, 21%",
    "Com o volume medido, a MUSLE espacializada não se distinguiu da regra com o volume: não se isola a contribuição da fórmula de erosão",
    "A espacialização chega a um erro da mesma ordem do modelo concentrado (22%) e acrescenta o mapa",
    "Áreas críticas: campo, silvicultura e lavoura temporária sobre Cambissolos, em encostas acima de 20% (46% da área, 83% da erosão)",
], size=16)
imagem(s, "slides/mapa_criticas_MC.png", 6.4, 1.95, 6.35, 4.3)
caixa_texto(s, 6.4, 6.3, 6.35, 0.45, ["Áreas críticas: 5% dos pixels de maior erosão média (MC); 94% coincidem com o MFM"], size=12, italic=True, color=MUTED, align=PP_ALIGN.CENTER)

s = novo("Limitações: de onde vem o erro", "Limitações: de onde vem o erro")
numero(s, X0, 1.85, 5.6, "81% → 21%", "erro mediano com o escoamento calculado e com o medido: cerca de 3/4 do erro vem da hidrologia", ORANGE)
numero(s, 6.6, 1.85, 6.1, "91%", "da variação do erro do sedimento é explicada pelo erro do escoamento")
itens = [("Chuva de 2 postos", "um deles fora da bacia; a chuva vira um gradiente suave e núcleos de chuva entre os postos não aparecem"),
         ("Delimitação manual dos eventos", "no evento 11, 12 a 14 mm em cada posto (cerca de 16% da chuva) caíram nas 9 h antes da janela e ficaram fora"),
         ("Forma do SCS-CN", "a fração da chuva que escoa não cresceu com a chuva (r = −0,01); CN-I e λ ajustam o total (+3%), não o erro de cada evento"),
         ("Vazão de base estimada", "o escoamento direto \"medido\" depende do filtro (BFImax = 0,70) e também é incerto")]
for i, (a, b) in enumerate(itens):
    y = 3.45 + i * 0.83
    o = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(X0), Inches(y + 0.08), Inches(0.48), Inches(0.48))
    o.fill.solid(); o.fill.fore_color.rgb = rgb(BLUE); o.line.fill.background()
    o.text_frame.text = str(i + 1); r = o.text_frame.paragraphs[0].runs[0]; r.font.size = Pt(16); r.font.bold = True; r.font.color.rgb = rgb(WHITE)
    o.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    caixa_texto(s, X0 + 0.7, y, W - 0.7, 0.75, [[(a + ": ", {"bold": True, "color": BLUE}), (b, {})]], size=15, anchor=MSO_ANCHOR.MIDDLE)

s = novo("Limitações: o que falta validar", "Limitações: o que falta validar")
cards = [("Mapa sem validação espacial", "Só há medição de sedimento no exutório; não dá para testar se a erosão está onde o mapa aponta"),
         ("K e C adotados", "Valores por classe de Vivarelli et al. (2025), sem recalibração; área urbana com erosão nula"),
         ("c único", "Sem conectividade: o mapa mostra onde a erosão é produzida, não onde o sedimento chega ao rio"),
         ("Medição do sedimento", "Curva turbidez × CSS sem incerteza estimada; parte da carga pode vir do canal (pico de CSS antes da vazão)"),
         ("Poucos eventos", "17 eventos: diferenças de poucos pontos não são interpretáveis; conclusões qualitativas")]
for i, (a, b) in enumerate(cards):
    x = X0 + (i % 3) * (3.9 + 0.235); y = 1.95 + (i // 3) * (2.3 + 0.2)
    cartao(s, x, y, 3.9, 2.3, a, b, size=15)
cartao(s, X0 + 2 * (3.9 + 0.235), 1.95 + 2.5, 3.9, 2.3, "Próximos passos",
       "Medir sedimento em sub-bacias e verificar as áreas críticas em campo; mais postos ou radar; conectividade por pixel; novos eventos", fill="FCEFD9", line="E8C79A", cor_titulo=ORANGE, size=15)

# =============================================================== encerramento
s = novo("Agradecimentos", "Agradecimentos")
caixa_texto(s, X0, 2.1, 8.4, 4.5, [
    [("Me. Luis Fernando Murillo-Bermúdez", {"bold": True, "color": BLUE}), (" — orientação e dados de monitoramento", {})],
    [("Prof. Dr. André Luís Sotero Salustiano Martim", {"bold": True, "color": BLUE}), (" — coorientação", {})],
    [("Dr. Hugo de Oliveira Fagundes e Me. Gustavo Ribeiro da Silva", {"bold": True, "color": BLUE}), (" — banca", {})],
    [("CNPq / PIBIC", {"bold": True, "color": BLUE}), (" — bolsa de iniciação científica", {})],
    [("Família, Larissa e amigos", {"bold": True, "color": BLUE}), (" — apoio durante a graduação", {})]], size=19, espaco=12)
caixa_texto(s, 9.2, 2.9, 3.55, 1.0, ["Obrigado!"], size=44, bold=True, color=BLUE, align=PP_ALIGN.RIGHT)
caixa_texto(s, 9.2, 3.9, 3.55, 0.5, ["[e-mail de contato]"], size=16, color=MUTED, align=PP_ALIGN.RIGHT)

s = novo("Uso de inteligência artificial", "Uso de inteligência artificial")
caixa_texto(s, X0, 1.95, W, 0.4, ["[Opcional: confirme se o texto corresponde ao que você fez e ao que a FECFAU pede]"], size=13, italic=True, color=ORANGE)
for i, (a, b) in enumerate([("Programação", "apoio na escrita e revisão das rotinas em Python"), ("Texto", "revisão de redação e da formatação"), ("Figuras", "apoio na preparação de gráficos e mapas")]):
    cartao(s, X0 + i * 4.135, 2.6, 3.9, 1.6, a, b, centro=True, size=15)
caixa_texto(s, X0, 4.6, W, 0.8, ["As escolhas de método, os cálculos e os resultados foram conferidos pelo autor e discutidos com o orientador."], size=18, color=BLUE)

# =============================================================== apoio (para perguntas)
s = novo("Apoio: a concentração chega antes da vazão", "Apoio: a concentração chega antes da vazão")
imagem(s, "slides/ev11_hidrograma.png", X0, 1.85, 6.8, 3.6)
marcadores(s, X0, 5.6, 6.8, 1.2, ["Evento 11: pico de CSS cerca de 25 h antes do pico de vazão (laço horário)",
                                  "68% da carga passa até o pico de vazão; cerca de 72% na parcela do escoamento direto"], size=14)
numero(s, 7.7, 1.85, 2.4, "88%", "da variação da carga (log) explicada pelo volume", ORANGE)
numero(s, 10.3, 1.85, 2.45, "0%", "explicada só pela intensidade máxima da chuva")
marcadores(s, 7.7, 3.5, 5.05, 3.3, ["13 de 17 eventos com laço horário (planilha de eventos)",
                                    "A intensidade da chuva aparece na concentração média (Spearman 0,49; p = 0,04)",
                                    "O modelo trabalha com o total do evento; a dinâmica dentro do evento e as fontes perto do canal não são representadas"], size=14)
fonte(s, "Fonte: elaborado pelo autor, com os dados de Murillo-Bermúdez e Martim (2022). Valores de p apenas indicativos")

s = novo("Apoio: o critério de calibração", fala=(
    "Se perguntarem se o resultado do MC depende do critério de calibração: depende. Com o critério em log, o do TCC, o MC erra 81% e a regra com a chuva 42%. "
    "Com o critério linear ou com peso relativo, o MC cai para 40 a 45%, perto da regra com a chuva. O que não depende do critério: o MC tem erro alto (40 a 80%), "
    "e com o escoamento medido o MFM fica em cerca de 20% em qualquer critério. O critério em log foi escolhido porque o evento 15 responde por 48,7% da variabilidade "
    "da carga medida e dominaria um ajuste linear; minimizar a soma dos quadrados em log equivale a maximizar o NSE em log, a função objetivo de Hao et al. (2022)."))
linhas_t = [["Modelo", "log (TCC)", "linear", "erro relativo", "mediana das razões"],
            ["MC", "81,1% / 35%", "44,8% / 59%", "40,4% / 59%", "71,1% / 59%"],
            ["MFM", "20,6% / 94%", "20,4% / 94%", "21,1% / 94%", "20,8% / 94%"],
            ["Regra com a chuva", "41,8% / 82%", "38,8% / 88%", "51,7% / 47%", "38,8% / 82%"],
            ["Regra com o volume", "15,9% / 94%", "20,3% / 94%", "19,7% / 94%", "16,1% / 94%"]]
tb = s.shapes.add_table(5, 5, Inches(X0), Inches(1.95), Inches(W), Inches(2.8)).table
for j, wj in enumerate([3.0, 2.3, 2.3, 2.3, 2.27]):
    tb.columns[j].width = Inches(wj)
for i, row in enumerate(linhas_t):
    for j, v in enumerate(row):
        c = tb.cell(i, j); c.text = v
        par = c.text_frame.paragraphs[0]; par.alignment = PP_ALIGN.CENTER
        r = par.runs[0]; r.font.size = Pt(16); r.font.bold = i == 0; r.font.color.rgb = rgb(WHITE if i == 0 else TEXT)
        c.fill.solid(); c.fill.fore_color.rgb = rgb(BLUE if i == 0 else (TINT if i % 2 == 0 else WHITE))
marcadores(s, X0, 5.0, W, 1.7, ["Erro mediano / fração em fator 2, na validação cruzada, para cada critério de ajuste do coeficiente",
                                "O MC depende muito do critério (40 a 81%); o MFM e a regra com o volume quase não dependem",
                                "Log: o evento 15 responde por 48,7% da variabilidade da carga e dominaria um ajuste linear"], size=15)
fonte(s, "Fonte: elaborado pelo autor (Scripts/_sensibilidade_criterio_calibracao_18-11.py)")

# =============================================================== afasta o conteudo da faixa azul
# (o conteudo foi desenhado entre y = 1,8 e 7,3 pol.; comprime para 2,1 a 7,3, como nos slides do autor)
A0, A1, B0 = 1.8, 7.3, 2.1
k = (A1 - B0) / (A1 - A0)
for s in NOVOS:
    for sh in s.shapes:
        if sh == s.shapes.title or sh.top is None:
            continue
        top = sh.top / 914400
        if top < A0 - 0.01:
            continue
        novo_top = B0 + (top - A0) * k
        if sh.shape_type == 13:      # imagem: escala w e h juntos, mantendo o centro
            cx = (sh.left + sh.width / 2); w_, h_ = sh.width * k, sh.height * k
            sh.width, sh.height = int(w_), int(h_); sh.left = int(cx - w_ / 2)
        else:
            sh.height = int(sh.height * k)
        sh.top = int(novo_top * 914400)

# =============================================================== fonte do tema: Calibri
for parte in p.part.package.iter_parts():
    if parte.partname.endswith(".xml") and "/theme/" in str(parte.partname):
        xml = parte.blob.decode("utf-8")
        xml = xml.replace('<a:latin typeface="Aptos Display"', '<a:latin typeface="Calibri"').replace('<a:latin typeface="Aptos"', '<a:latin typeface="Calibri"')
        parte._blob = xml.encode("utf-8")

p.save(DST)
print("ok", DST, len(p.slides), "slides")
