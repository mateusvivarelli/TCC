"""
Gera o relatorio de resultados para o orientador, em PDF com formatacao ABNT
(A4; margens 3cm esquerda/superior e 2cm direita/inferior; Times New Roman 12;
entrelinhas 1,5; texto justificado; recuo de primeira linha 1,25cm; titulos
numerados progressivamente; tabelas em padrao IBGE com titulo acima e fonte
abaixo; referencias em ordem alfabetica conforme NBR 6023).

Saida: Relatorio_Resultados_TCC.pdf
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, Image, KeepTogether)

BASE = r"C:\TCC"
SAIDA = os.path.join(BASE, "Relatorio_Resultados_TCC.pdf")
FIGURA = os.path.join(BASE, "Figuras", "comparacao_previsao_vs_volume_restrito.png")

FONTE = "Times-Roman"
FONTE_B = "Times-Bold"
FONTE_I = "Times-Italic"
CORPO = 12
ENTRE = CORPO * 1.5

corpo = ParagraphStyle("corpo", fontName=FONTE, fontSize=CORPO, leading=ENTRE,
                       alignment=TA_JUSTIFY, firstLineIndent=1.25 * cm,
                       spaceAfter=0, allowWidows=0, allowOrphans=0)
corpo_sem_recuo = ParagraphStyle("corpo_sr", parent=corpo, firstLineIndent=0)
titulo_secao = ParagraphStyle("t1", fontName=FONTE_B, fontSize=CORPO, leading=ENTRE,
                              alignment=TA_LEFT, spaceBefore=ENTRE, spaceAfter=6)
titulo_sub = ParagraphStyle("t2", fontName=FONTE_B, fontSize=CORPO, leading=ENTRE,
                            alignment=TA_LEFT, spaceBefore=10, spaceAfter=4)
tit_doc = ParagraphStyle("td", fontName=FONTE_B, fontSize=14, leading=20,
                         alignment=TA_CENTER, spaceAfter=4)
ident = ParagraphStyle("id", fontName=FONTE, fontSize=11, leading=15,
                       alignment=TA_CENTER, spaceAfter=2)
legenda = ParagraphStyle("leg", fontName=FONTE, fontSize=10, leading=13,
                         alignment=TA_LEFT, spaceBefore=8, spaceAfter=3)
fonte_tab = ParagraphStyle("ft", fontName=FONTE, fontSize=10, leading=13,
                           alignment=TA_LEFT, spaceBefore=3, spaceAfter=10)
cel = ParagraphStyle("cel", fontName=FONTE, fontSize=10, leading=13, alignment=TA_LEFT)
cel_b = ParagraphStyle("celb", fontName=FONTE_B, fontSize=10, leading=13, alignment=TA_LEFT)
cel_c = ParagraphStyle("celc", parent=cel, alignment=TA_CENTER)
cel_cb = ParagraphStyle("celcb", parent=cel_b, alignment=TA_CENTER)
ref = ParagraphStyle("ref", fontName=FONTE, fontSize=CORPO, leading=CORPO * 1.15,
                     alignment=TA_JUSTIFY, spaceAfter=CORPO)

LARGURA_UTIL = A4[0] - 3 * cm - 2 * cm


def p(texto, estilo=corpo):
    return Paragraph(texto, estilo)


def tabela(dados, larguras, titulo, fonte):
    t = Table(dados, colWidths=larguras, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (-1, 0), 1.0, colors.black),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black),
        ("LINEBELOW", (0, -1), (-1, -1), 1.0, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return KeepTogether([p(titulo, legenda), t, p(fonte, fonte_tab)])


hist = []
A = hist.append

# ---------------- identificacao ----------------
A(p("ESPACIALIZAÇÃO DA EQUAÇÃO UNIVERSAL MODIFICADA DE PERDA DE SOLO (MUSLE) "
    "PARA IDENTIFICAÇÃO DE ÁREAS CRÍTICAS DE EROSÃO", tit_doc))
A(p("Relatório parcial de resultados — Bacia do Alto rio Jundiaí", tit_doc))
A(Spacer(1, 10))
A(p("Aluno: Mateus Guilherme Vivarelli", ident))
A(p("Orientador: Prof. Dr. André Luís Sotero Salustiano Martim", ident))
A(p("Coorientador: Luis Fernando Murillo Bermudéz", ident))
A(p("Setembro de 2026", ident))
A(Spacer(1, 16))

# ---------------- 1 ----------------
A(p("1 OBJETIVO", titulo_secao))
A(p("Este relatório apresenta os resultados da espacialização da MUSLE na parte alta da bacia "
    "do rio Jundiaí, com base nos 17 eventos de chuva monitorados entre 2018 e 2020. O objetivo "
    "do trabalho é gerar um <i>mapa</i> de produção de sedimentos — identificando as áreas de "
    "maior geração, os chamados <i>hot spots</i> erosivos — em substituição à abordagem "
    "concentrada adotada na Iniciação Científica, que produzia um único valor por evento para "
    "toda a bacia."))

# ---------------- 2 ----------------
A(p("2 DADOS UTILIZADOS", titulo_secao))
A(p("Foram utilizados dados medidos em campo entre 2018 e 2020: séries horárias de chuva em dois "
    "postos pluviométricos (DBT5, situado fora da bacia, e Campo Paulista, próximo ao exutório), "
    "série horária de vazão e concentração de sedimentos em suspensão na seção de controle. "
    "Desses registros derivam, para cada evento, o volume escoado, a vazão de pico e a produção "
    "total de sedimentos, esta última utilizada como alvo de calibração."))
A(p("A base cartográfica compreende o modelo digital de elevação (MDE), o mapa pedológico "
    "(fator K, média 0,039), o mapa de uso e ocupação do solo (fator C, média 0,050) e o fator "
    "topográfico LS (média 0,536). O fator de práticas conservacionistas P foi mantido constante "
    "e igual a 1,0. A grade de trabalho tem resolução de 30 m, totalizando cerca de 154 mil "
    "células sobre os 137,8 km² da bacia."))

# ---------------- 3 ----------------
A(p("3 METODOLOGIA", titulo_secao))

A(p("3.1 Modelagem hidrológica espacializada", titulo_sub))
A(p("A chuva de cada evento foi interpolada espacialmente e o método SCS-CN aplicado célula a "
    "célula. Duas decisões de calibração foram adotadas: o cenário de umidade antecedente seco "
    "(AMC I) e a recalibração da razão de abstração inicial de λ = 0,2 (valor padrão) para "
    "λ = 0,05. O erro médio do volume escoado caiu de -62,6% para +0,5%. A escolha de λ = 0,05 "
    "encontra respaldo em Brandão et al. (2025), que avaliaram 3.578 bacias em escala global."))
A(p("Adicionalmente, identificou-se que o MDE não representava um aterro de estrada com passagem "
    "de água, criando uma barreira artificial de drenagem. Após a correção, a área de "
    "contribuição passou de 109,79 km² para 137,80 km², valor consistente com a delimitação de "
    "campo."))
A(p("A vazão de pico da bacia foi estimada por convolução horária com hidrograma unitário do SCS "
    "(tempo de concentração de Giandotti, 10,65 h, e fator de pico recalibrado), obtendo erro "
    "médio de -38,4%. Cabe destacar que esse resultado constitui uma <b>validação do modelo "
    "hidrológico</b> da bacia e não é utilizado como entrada do mapa de erosão — a vazão de pico "
    "empregada na MUSLE espacializada é a formulação local descrita a seguir."))

A(p("3.2 MUSLE espacializada", titulo_sub))
A(p("Seguiu-se a metodologia de Hao et al. (2022). Para cada célula, calcula-se primeiro uma "
    "vazão de pico local, obtida a partir do escoamento da própria célula ponderado pela razão "
    "entre a intensidade máxima de 60 minutos e a lâmina total do evento — sem roteamento "
    "hidráulico e sem delimitação de sub-bacias. Em seguida, aplica-se a formulação de Williams "
    "(1975) célula a célula, com os coeficientes α = 11,8 e β = 0,56 mantidos em seus valores "
    "originais, obtendo-se a erosão local por célula."))
A(p("A produção de sedimentos que efetivamente atinge o exutório é então obtida por uma relação "
    "de escala linear, com <b>um único parâmetro livre</b>, calibrado contra os 17 valores "
    "medidos."))

A(p("3.3 Restrição pelo volume observado", titulo_sub))
A(p("O diagnóstico das fontes de erro (seção 5.2) mostrou que o desempenho do modelo é limitado "
    "quase integralmente pela estimativa do volume escoado, e não pela estrutura espacial ou pela "
    "formulação da MUSLE. Três tentativas de corrigir esse volume de forma puramente preditiva "
    "foram testadas e descartadas por não resistirem à validação cruzada (seção 5.3)."))
A(p("Adotou-se, então, o uso do volume medido como <b>restrição</b>: o raster de escoamento de "
    "cada evento é reescalado por um fator único, de modo que o total da bacia iguale o volume "
    "observado. O padrão espacial gerado pelo SCS-CN é integralmente preservado; apenas o total é "
    "ancorado na medição. Essa configuração tem precedente direto em Baert et al. (2026), que a "
    "utilizam como caso de referência."))

# ---------------- 4 glossario ----------------
A(p("4 TERMOS TÉCNICOS EMPREGADOS", titulo_secao))
A(p("Para facilitar a leitura dos resultados, esclarecem-se os termos estatísticos utilizados.",
    corpo))

glossario = [
    ("NSE (coeficiente de eficiência de Nash-Sutcliffe)",
     "compara o erro do modelo ao erro que se cometeria simplesmente adotando a média das "
     "observações. NSE = 1 indica ajuste perfeito; NSE = 0 indica que o modelo não é melhor que a "
     "média; valores negativos indicam desempenho pior que a média. É a métrica mais usada em "
     "hidrologia."),
    ("WIA (índice de concordância de Willmott)",
     "varia de 0 a 1 e mede a concordância entre simulado e observado. É menos sensível a valores "
     "extremos que o NSE. Valores acima de 0,90 indicam concordância muito boa."),
    ("PBIAS (viés percentual)",
     "mede a tendência sistemática do modelo: positivo indica superestimação, negativo indica "
     "subestimação, e valores próximos de zero indicam ausência de viés. Observação importante: o "
     "PBIAS pode ser próximo de zero mesmo com erros individuais grandes, caso eles se cancelem."),
    ("Erro absoluto médio",
     "média dos erros percentuais de cada evento tomados em módulo. Como não há cancelamento "
     "entre superestimações e subestimações, complementa a leitura do PBIAS."),
    ("<i>In-sample</i> (dentro da amostra)",
     "métrica calculada com o parâmetro ajustado nos mesmos dados usados para avaliá-lo. É uma "
     "medida otimista, pois o modelo já \"viu\" a resposta."),
    ("Validação cruzada <i>leave-one-out</i>",
     "procedimento em que, para cada evento, o parâmetro é recalibrado usando apenas os outros 16 "
     "eventos, e o evento excluído é então previsto. Fornece uma estimativa honesta do desempenho "
     "fora da amostra, adequada a conjuntos pequenos. É o mesmo procedimento de validação adotado "
     "por Hao et al. (2022)."),
    ("Sobreajuste (<i>overfitting</i>)",
     "situação em que o modelo possui parâmetros livres em número suficiente para ajustar o ruído "
     "dos dados de calibração. Apresenta excelente desempenho dentro da amostra e desempenho ruim "
     "fora dela. É detectado justamente pela diferença entre a métrica <i>in-sample</i> e a "
     "métrica por validação cruzada."),
    ("Parcimônia",
     "princípio segundo o qual, para desempenho equivalente, o modelo com menos parâmetros livres "
     "é preferível, por ser menos suscetível a sobreajuste."),
    ("λ (razão de abstração inicial)",
     "fração da retenção potencial do solo que é consumida antes do início do escoamento "
     "superficial, no método SCS-CN."),
    ("AMC (condição de umidade antecedente)",
     "classificação do estado de umidade do solo antes do evento: AMC I (seco), II (médio) e III "
     "(úmido). Determina qual valor de CN se aplica."),
    ("<i>Hot spots</i> erosivos",
     "células situadas no percentil superior de produção de sedimentos — as áreas críticas que o "
     "trabalho se propõe a identificar."),
]
for termo, definicao in glossario:
    A(p(f"<b>{termo}:</b> {definicao}", corpo_sem_recuo))
    A(Spacer(1, 5))

# ---------------- 5 resultados ----------------
A(p("5 RESULTADOS", titulo_secao))

A(p("5.1 Desempenho do modelo", titulo_sub))
A(p("A Tabela 1 apresenta o desempenho nas duas configurações: previsão pura, em que o escoamento "
    "provém integralmente do modelo SCS-CN, e a configuração com o volume observado usado como "
    "restrição."))

dados1 = [
    [p("Métrica", cel_cb), p("Previsão pura", cel_cb), p("Volume restrito", cel_cb)],
    [p("NSE (validação cruzada)", cel), p("0,2816", cel_c), p("<b>0,7759</b>", cel_c)],
    [p("NSE (<i>in-sample</i>)", cel), p("0,3714", cel_c), p("0,8052", cel_c)],
    [p("WIA", cel), p("0,8683", cel_c), p("<b>0,9462</b>", cel_c)],
    [p("PBIAS", cel), p("-21,3%", cel_c), p("<b>-1,0%</b>", cel_c)],
    [p("Erro absoluto médio", cel), p("46,1%", cel_c), p("<b>27,8%</b>", cel_c)],
]
A(tabela(dados1, [7.0 * cm, 4.5 * cm, 4.5 * cm],
         "Tabela 1 – Desempenho do modelo espacializado nas duas configurações",
         "Fonte: elaborado pelo autor (2026)."))

A(p("5.2 Decomposição das fontes de erro", titulo_sub))
A(p("Para identificar a origem do erro, o modelo foi avaliado mantendo-se toda a estrutura "
    "constante e variando apenas a qualidade da entrada hidrológica (Tabela 2)."))

dados2 = [
    [p("Configuração", cel_cb), p("NSE", cel_cb)],
    [p("Espacializada, escoamento do modelo SCS-CN", cel), p("0,28", cel_c)],
    [p("Espacializada, volume escoado observado", cel), p("0,78", cel_c)],
    [p("Concentrada (MUSLE clássica), volume e pico modelados", cel), p("0,44", cel_c)],
    [p("Concentrada, volume e pico observados", cel), p("0,85", cel_c)],
]
A(tabela(dados2, [11.5 * cm, 4.5 * cm],
         "Tabela 2 – Desempenho em função da qualidade da entrada hidrológica",
         "Fonte: elaborado pelo autor (2026)."))

A(p("A leitura é direta: a estrutura espacial não é a fonte do erro. Com entrada hidrológica de "
    "boa qualidade, o modelo espacializado atinge NSE entre 0,78 e 0,81. Observa-se ainda que a "
    "espacialização não degrada o desempenho em relação à formulação concentrada quando a "
    "qualidade da entrada é a mesma — ou seja, o mapa é obtido sem custo de acurácia."))

A(p("5.3 Tentativas de melhoria preditiva do volume escoado", titulo_sub))
A(p("Antes de recorrer ao volume observado, três alternativas puramente preditivas foram "
    "testadas. Nenhuma se sustentou:"))
A(p("a) <b>Calibração de λ evento a evento:</b> constatou-se que, em 5 dos 17 eventos, "
    "<i>nenhum</i> valor de λ reproduz o volume medido — mesmo com λ tendendo a zero, o cenário "
    "AMC I gera escoamento insuficiente. Trata-se, portanto, de limitação do próprio CN, e não do "
    "parâmetro λ.", corpo_sem_recuo))
A(p("b) <b>λ como função da lâmina precipitada:</b> houve melhora dentro da amostra, mas piora em "
    "validação cruzada — sobreajuste característico de amostra pequena.", corpo_sem_recuo))
A(p("c) <b>Classificação padrão de AMC pela chuva antecedente de cinco dias:</b> resultou em "
    "degradação acentuada do desempenho.", corpo_sem_recuo))
A(Spacer(1, 6))
A(p("Esse conjunto de resultados reproduz, de forma independente, o achado central de Baert et "
    "al. (2026) — nenhuma generalização de λ apresenta bom desempenho fora da amostra — e é "
    "coerente com Valle Junior et al. (2019), que documentaram inadequação estrutural do método "
    "SCS-CN em bacia brasileira."))

A(p("5.4 Robustez do mapa", titulo_sub))
A(p("A correlação espacial entre o mapa médio obtido nas duas configurações é de 0,994, e 96,9% "
    "dos <i>hot spots</i> coincidem. Ou seja, a localização das áreas críticas é robusta à "
    "correção hidrológica: esta afeta a magnitude por evento, não o padrão espacial. Trata-se de "
    "propriedade desejável, uma vez que o objetivo do trabalho é justamente identificar onde a "
    "erosão se concentra."))
A(p("As áreas classificadas como críticas apresentam fator C médio de 0,247, contra 0,050 na "
    "média da bacia, e fator LS médio de 0,791, contra 0,537 — coerente com a concentração de "
    "erosão em usos do solo mais agressivos associados a maior declividade."))

if os.path.exists(FIGURA):
    from reportlab.lib.utils import ImageReader
    iw, ih = ImageReader(FIGURA).getSize()
    larg = LARGURA_UTIL
    alt = larg * ih / iw
    A(p("Figura 1 – Mapa de produção de sedimentos nas duas configurações e desempenho por evento",
        legenda))
    A(Image(FIGURA, width=larg, height=alt))
    A(p("Fonte: elaborado pelo autor (2026).", fonte_tab))

# ---------------- 6 ----------------
A(p("6 DISCUSSÃO", titulo_secao))
A(p("Os resultados obtidos são considerados satisfatórios pelas razões a seguir."))
A(p("<b>a) Superam o artigo de referência.</b> Hao et al. (2022) reportam NSE superior a 0,70 e "
    "WIA superior a 0,89 nas três bacias estudadas. A configuração adotada atinge NSE de 0,78 e "
    "WIA de 0,95, com formulação mais simples.", corpo_sem_recuo))
A(p("<b>b) Superam o benchmark mais recente do problema.</b> Baert et al. (2026), analisando 154 "
    "eventos, obtiveram NSE de 0,66 para a MUSLE alimentada com volume e pico observados, e NSE "
    "próximo de zero com entradas modeladas. Os dois resultados aqui obtidos (0,78 com volume "
    "observado e 0,28 com volume modelado) situam-se acima dos casos correspondentes.",
    corpo_sem_recuo))
A(p("<b>c) As métricas são conservadoras.</b> O valor principal decorre de validação cruzada, e "
    "não do ajuste dentro da amostra, que é reportado separadamente.", corpo_sem_recuo))
A(p("<b>d) O modelo é parcimonioso.</b> Há um único parâmetro livre para 17 observações, com α e "
    "β mantidos nos valores originais de Williams (1975). Para comparação, a Iniciação Científica "
    "ajustou dois parâmetros, e a formulação com índice de conectividade exigiria outros dois.",
    corpo_sem_recuo))
A(Spacer(1, 6))
A(p("Registre-se ainda que a etapa de conectividade de sedimentos proposta por Hao et al. (2022) "
    "foi integralmente implementada e testada, incluindo a identificação e correção de um erro na "
    "rotina, mas em nenhuma configuração superou a relação de escala linear. A hipótese mais "
    "provável é de diferença de escala: as bacias do artigo original têm de 1.310 a 8.973 km², "
    "portanto 10 a 65 vezes maiores que o Alto Jundiaí. Esse resultado será reportado como achado "
    "do trabalho, e não omitido."))

# ---------------- 7 ----------------
A(p("7 LIMITAÇÕES", titulo_secao))
A(p("<b>a)</b> A configuração com volume restrito não constitui previsão pura: seu desempenho é "
    "condicionado ao conhecimento do volume medido. Para bacia não monitorada, o valor aplicável "
    "seria 0,28. Isso é metodologicamente legítimo, uma vez que o objetivo é mapear eventos "
    "observados e não prever eventos futuros, mas será declarado nesses termos.", corpo_sem_recuo))
A(p("<b>b)</b> A erosão calculada por célula deve ser interpretada como índice relativo de "
    "contribuição, e não como tonelagem absoluta daquela célula: o coeficiente de Williams foi "
    "calibrado para volumes e vazões em escala de bacia. O total do mapa, esse sim, está em "
    "toneladas reais, por estar ancorado na medição.", corpo_sem_recuo))
A(p("<b>c)</b> A precipitação provém de apenas dois postos, um deles externo à bacia. A "
    "variabilidade espacial da chuva no mapa corresponde, portanto, a um gradiente interpolado "
    "entre dois pontos, o que representa provavelmente a maior fonte de erro residual.",
    corpo_sem_recuo))
A(p("<b>d)</b> O mapa não foi validado espacialmente, uma vez que não há medições distribuídas de "
    "sedimento no interior da bacia. A validação é agregada, apoiada pelas verificações de "
    "coerência física descritas na seção 5.4.", corpo_sem_recuo))

# ---------------- 8 ----------------
A(p("8 PRÓXIMOS PASSOS", titulo_secao))
A(p("Com a etapa de modelagem concluída, o trabalho segue para a produção das figuras finais e a "
    "redação do texto. Solicita-se ao orientador manifestação quanto a dois pontos: (i) a adoção "
    "da configuração com volume observado como restrição enquanto resultado principal, mantendo a "
    "previsão pura como comparação; e (ii) a forma de reportar a etapa de conectividade "
    "descartada."))

# ---------------- referencias ----------------
A(p("REFERÊNCIAS", titulo_secao))
referencias = [
    "BAERT, P.; HERPOEL, M.; MEERSMANS, J.; BIELDERS, C.; DEGRÉ, A. A regime-based framework for "
    "linking runoff initiation and event-scale sediment export in a small temperate agricultural "
    "loess catchment. <b>Catena</b>, v. 274, art. 110497, 2026. DOI: 10.1016/j.catena.2026.110497.",

    "BORSELLI, L.; CASSI, P.; TORRI, D. Prolegomena to sediment and flow connectivity in the "
    "landscape: A GIS and field numerical assessment. <b>Catena</b>, v. 75, n. 3, p. 268-277, "
    "2008. DOI: 10.1016/j.catena.2008.07.006.",

    "BRANDÃO, A. R. A.; SCHWAMBACK, D.; BALLARIN, A. S.; RAMIREZ-AVILA, J. J.; VASCONCELOS NETO, "
    "J. G.; OLIVEIRA, P. T. S. Toward a better understanding of curve number and initial "
    "abstraction ratio values from a large sample of watersheds perspective. <b>Journal of "
    "Hydrology</b>, v. 655, art. 132941, 2025. DOI: 10.1016/j.jhydrol.2025.132941.",

    "HAO, R. et al. Incorporating sediment connectivity index into MUSLE model to explore soil "
    "erosion and sediment yield relationships at event scale. <b>Journal of Hydrology</b>, v. 614, "
    "art. 128579, 2022. DOI: 10.1016/j.jhydrol.2022.128579.",

    "VALLE JUNIOR, L. C. G.; RODRIGUES, D. B. B.; OLIVEIRA, P. T. S. Initial abstraction ratio and "
    "Curve Number estimation using rainfall and runoff data from a tropical watershed. <b>RBRH</b>, "
    "Porto Alegre, v. 24, e5, 2019. DOI: 10.1590/2318-0331.241920170199.",

    "VIVARELLI, M. et al. Aplicação da equação universal de perda de solo modificada e calibração "
    "com dados de campo em uma bacia hidrográfica antropizada. Artigo (Iniciação Científica) – "
    "Universidade Estadual de Campinas, Campinas, 2025.",

    "WILLIAMS, J. R. Sediment-yield prediction with universal equation using runoff energy factor. "
    "In: <b>Present and prospective technology for predicting sediment yield and sources</b>. "
    "ARS-S-40. Washington, DC: US Department of Agriculture, 1975. p. 244-252.",
]
for r in referencias:
    A(p(r, ref))


def rodape(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONTE, 10)
    canvas.drawRightString(A4[0] - 2 * cm, A4[1] - 2 * cm, str(doc.page))
    canvas.restoreState()


doc = SimpleDocTemplate(SAIDA, pagesize=A4,
                        leftMargin=3 * cm, rightMargin=2 * cm,
                        topMargin=3 * cm, bottomMargin=2 * cm,
                        title="Relatório de Resultados — TCC MUSLE Jundiaí",
                        author="Mateus Guilherme Vivarelli")
doc.build(hist, onFirstPage=rodape, onLaterPages=rodape)
print("gerado:", SAIDA)
