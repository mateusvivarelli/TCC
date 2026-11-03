# Lote E - leitura dos 5 PDFs novos (02/11/2026)

* Quem leu: subagente da sessão do PC (Claude Code), a pedido da sessão principal.
* Regra: nada aqui foi aplicado ao Doc. Só proposta de redação. Frases recomendadas só dizem o que o PDF sustenta.
* Como li: a ferramenta de leitura de PDF por páginas não funcionou neste PC (falta o programa pdftoppm). Por isso extraí o texto de 4 PDFs com pdftotext (o texto vem junto no arquivo) e li o texto extraído. O PDF 3 (Gray e Gartner) é um arquivo de imagens, sem texto; renderizei as 20 páginas e usei o OCR do Windows (reconhecimento de caracteres). Conferi uma página (a 6) olhando a imagem: o OCR bateu. Números isolados do OCR (preços, percentuais) podem ter erro; não usei nenhum número do PDF 3 nas frases recomendadas.
* Páginas: cito a página impressa na obra. Para o USGS TM 3-C4, página do PDF = página impressa + 10 (a numeração impressa começa na página 11 do arquivo).

---

## 1. Tabela-resumo

Legenda: confirmada / parcialmente / NÃO CONFIRMADA / não se aplica (n.a.).

| PDF | Obra identificada | Nível de leitura | A (validação) | B (turbidez, carga) | C (Minella, histerese) | D (chuva, incerteza de entrada) |
|---|---|---|---|---|---|---|
| 1. cawley10a.pdf | Cawley e Talbot (2010), JMLR 11:2079-2107 | Texto completo extraído (29 p.). Li inteiros: resumo, introdução, 4.1, 4.4, 5 (5.1 a 5.3) e 6. Seções 2, 3, 4.2 e 4.3 (descrição dos classificadores e experimentos) só por varredura | **parcialmente** (núcleo confirmado; 2 trechos precisam de ajuste) | n.a. | n.a. | n.a. |
| 2. TM3C4.pdf | Rasmussen, Gray, Glysson e Ziegler (2009, rev. 2011), USGS TM 3-C4 | Texto extraído (63 p. no arquivo, 52 impressas). Li: capa, resumo, introdução, sensores, relação turbidez-CSS (conjunto de calibração, valores atípicos, adequação, duração), início do desenvolvimento do modelo, cálculo da carga (eqs. 9 e 10), validação e manutenção, mudança de sensor, fatores que afetam a relação, resumo. NÃO li em detalhe: as seções estatísticas de regressão (p. 12 a 22 impressas: correlação, transformação, resíduos, fator de correção de viés, intervalos de predição, regressão múltipla) nem os apêndices (exemplos de KS, OR, FL, CA; NWIS; critérios de qualidade da água) | n.a. | **confirmada** (com 2 ajustes de redação) | n.a. | n.a. |
| 3. Technological advances... .pdf | Gray e Gartner (2009), Water Resources Research 45, W00D29 | Texto completo (20 p.), por OCR. Li o texto de todas as páginas; as listas de referências (p. 17 a 20) só por varredura | n.a. | **confirmada** | n.a. | n.a. |
| 4. minella.pdf | **NÃO é Minella et al. (2008).** É Minella, Merten e Magnago (2011), Rev. Bras. Eng. Agríc. Ambiental 15(12):1306-1313, sobre histerese | Texto completo (8 p.) | n.a. | n.a. | **parcialmente**: a parte da histerese e da variação entre eventos é sustentada; a parte da calibração da turbidez NÃO CONFIRMADA (esse assunto é do artigo de 2008, que não está nos PDFs) | n.a. |
| 5. 1-s2.0-S0022169415003856-main.pdf | Ochoa-Rodriguez et al. (2015), Journal of Hydrology 531:389-407 (não é Faurès nem Williams) | Parcial: li resumo, introdução (p. 389-391), dados de chuva (2.3), seleção das resoluções e início da caracterização das tempestades (3.1 e 3.2), e a seção 5 de conclusões (p. 404-405). Seção 4 (resultados, p. 396-404) só por busca de palavras-chave e leitura de trechos | n.a. | n.a. | n.a. | **parcialmente**: sustenta a ideia geral de incerteza por resolução da chuva de entrada; NÃO trata de IDW, de delimitação de eventos nem de densidade de postos além de uma frase; escala e contexto (urbano, 1 a 800 ha, radar) são outros |

Resposta curta sobre o PDF 5: não é Faurès et al. (1995) nem Williams (1989). Ele cita os dois (Faurès na introdução, p. 390), mas não é nenhum deles.

---

## 2. Cada obra

### 2.1 Cawley e Talbot (2010) - PDF 1 (afirmação A)

* Referência ABNT: CAWLEY, G. C.; TALBOT, N. L. C. On over-fitting in model selection and subsequent selection bias in performance evaluation. **Journal of Machine Learning Research**, v. 11, p. 2079-2107, 2010. DOI: não consta no PDF (revista de acesso aberto; endereço oficial jmlr.org/papers/v11/cawley10a.html, conforme nota anterior, não conferido agora).
* Nível de leitura: ver tabela. Páginas citadas abaixo são as impressas (2079 a 2107; página do arquivo + 2078).
* O que a obra diz de útil:
  * O modelo tem parâmetros (ajustados no treino) e hiperparâmetros (escolhas de nível acima, como o parâmetro de regularização e "a escolha da função de kernel"). Escolher os hiperparâmetros otimizando um critério calculado em uma amostra finita (por exemplo, o erro da validação cruzada) também pode sobreajustar, e esse sobreajuste pode ser grande (p. 2079-2080, 2084-2085, 2094).
  * A consequência para a avaliação: se a escolha do modelo é feita antes e depois o desempenho é calculado nos mesmos dados, a estimativa fica otimista ("viés de seleção"). Para evitar, a seleção do modelo deve ser tratada como parte do ajuste e refeita a cada nova amostra (p. 2080, 2094-2095, 2103).
  * Mostram com dados reais de referência (13 conjuntos): quando a escolha dos hiperparâmetros usa todos os dados e a validação cruzada de 10 partes é feita depois com esses valores fixos (protocolo "externo"), o erro estimado é menor que no protocolo "interno" (a escolha refeita dentro de cada partição). O viés foi positivo nos 13 conjuntos e estatisticamente significativo em 11 deles, mesmo com só 2 hiperparâmetros (p. 2102-2103, tabela 8). O texto explica a razão: os dados de teste já foram "vistos" na escolha (p. 2102).
  * O termo "validação cruzada aninhada" ("nested cross-validation" ou "double cross", de Stone, 1974) aparece uma vez, de passagem (p. 2080). O nome que os autores usam no resto do artigo é protocolo "interno".
  * O resumo do artigo diz que a conclusão vale para qualquer prática de seleção de modelo que otimize um critério avaliado em amostra finita, não só validação cruzada.
* Conferência da afirmação A, por parte:

| Parte da frase do TCC | Veredito | Onde |
|---|---|---|
| Escolher modelo e avaliar nos mesmos dados dá desempenho enviesado para cima ("viés de otimismo") | Confirmada para a ESCOLHA do modelo (hiperparâmetros). O artigo usa "optimistic bias" e "selection bias" | p. 2079, 2096-2098, 2102-2103 |
| "Quando os PARÂMETROS são ajustados aos mesmos dados usados para avaliá-lo..." | Parcialmente. O artigo trata da escolha de hiperparâmetros/modelo; a ideia clássica de avaliar parâmetros nos próprios dados de treino é pressuposta (dados de teste separados), mas não é o tema nem é demonstrada | p. 2080-2082 |
| "A validação cruzada simples corrige apenas o viés dos parâmetros refeitos em cada rodada" | NÃO CONFIRMADA nessa forma. O artigo não diz isso. Diz que a validação cruzada estima o desempenho de um modelo ajustado (com viés levemente pessimista, p. 2082) e que ela fica otimista se a escolha foi feita antes, com todos os dados | p. 2082, 2102 |
| "Escolhas feitas antes, observando todos os dados, como a de uma formulação ou de um valor fixo de parâmetro, continuam a produzir viés de otimismo" | Confirmada para valores de hiperparâmetros fixados olhando todos os dados (seção 5.3). "Formulação" entra por analogia: os autores contam a escolha da função de kernel como hiperparâmetro (p. 2079). Atenção: o viés vem de a escolha ter sido OTIMIZADA com esses dados. Valor fixado por literatura, sem olhar o desempenho nos dados, não cai nesse argumento | p. 2079, 2102-2103 |
| "Para eliminá-lo, essas escolhas precisam ser repetidas dentro de cada rodada... validação cruzada aninhada" | Confirmada (protocolo interno; o termo "aninhada" aparece só uma vez) | p. 2080, 2095, 2103 |

* Ressalva geral: o contexto é aprendizado de máquina (classificadores de kernel), não hidrologia. A transposição para a escolha de formulação do modelo hidrológico é do TCC; o artigo sustenta o princípio, não a aplicação.
* Frase recomendada (ajustada ao que o PDF sustenta):
  "Quando a escolha do modelo (por exemplo, a formulação ou o valor de um parâmetro) é feita observando todos os dados e o desempenho é calculado depois sobre esses mesmos dados, a estimativa de desempenho tende a ser otimista. A validação cruzada simples refaz o ajuste dos parâmetros em cada rodada, mas não elimina esse viés quando a escolha foi feita antes; para evitá-lo, a escolha também deve ser repetida dentro de cada rodada, procedimento chamado de validação cruzada aninhada (CAWLEY; TALBOT, 2010)."
* Observação para o texto: a parte "parâmetros ajustados aos mesmos dados" é o caso clássico; se quiser apoio direto, ela está melhor em Varma e Simon (2006) (ainda não lido).

---

### 2.2 Rasmussen et al. (2009) - PDF 2 (afirmação B)

* Referência ABNT: RASMUSSEN, P. P.; GRAY, J. R.; GLYSSON, G. D.; ZIEGLER, A. C. **Guidelines and procedures for computing time-series suspended-sediment concentrations and loads from in-stream turbidity-sensor and streamflow data**. Reston: U.S. Geological Survey, 2009. 52 p. (Techniques and Methods, book 3, chap. C4). Versão revisada em 2011 (é a que está no PDF). DOI: não consta no PDF.
* Nota de formato: a NBR 6023:2018 manda indicar todos os autores, mas permite só o primeiro seguido de "et al."; no Doc, "(RASMUSSEN et al., 2009)".
* O que a obra diz de útil:
  * É um manual do USGS para obter séries de CSS e de carga a partir de turbidez e vazão contínuas, usando regressão ajustada a amostras (p. 1-3).
  * A turbidez é um índice relativo de espalhamento e absorção de luz, "não uma medida direta de partículas"; tamanho, forma e cor das partículas afetam a medida (p. 5, 25). Partículas maiores que cerca de 90 micrometros (areia muito fina) deixam a relação enviesada para menos; partículas escuras também (p. 25).
  * A CSS que alimenta o ajuste vem de amostras físicas, que devem representar a CSS média da seção (p. 1, 8).
  * Faixa de validade: o conjunto de calibração deve cobrir a faixa observada de turbidez, CSS e vazão; os valores mínimo e máximo de turbidez do conjunto são os "limites ideais" do modelo; fora deles é preciso entendimento do processo e julgamento hidrológico (p. 10-12). Sensores saturam no máximo de registro (cerca de 1.000 a 2.000 para os nefelométricos), e valores perto disso devem ficar fora do ajuste (p. 8).
  * Carga: SSL = CSS x vazão x constante de unidade (eq. 9); cargas diárias, mensais ou anuais saem de soma, ao longo do tempo, dos valores instantâneos (eq. 10) (p. 22).
  * Validação: os modelos "nunca devem ser considerados estáticos"; verificar com novas amostras, por exemplo anualmente (típico: pelo menos 4 a 10 amostras por ano em várias vazões), e testar mudança de relação (p. 22-24).
* Conferência da afirmação B (com a obra 2.3 junto):

| Parte da frase | Veredito | Onde (R = Rasmussen; G = Gray e Gartner) |
|---|---|---|
| Carga = "integral no tempo" de vazão x CSS | Confirmada na substância. A palavra "integral" não aparece; o manual calcula por soma numérica dos valores instantâneos (eq. 9 e 10). Sugestão: escrever "soma ao longo do tempo" ou "integração numérica" | R p. 1, 22; G p. 2-3, 8 |
| CSS só medida diretamente em amostras coletadas na seção | Confirmada | R p. 1, 5, 8; G p. 2-3 |
| Turbidez é grandeza contínua correlacionada com a CSS | Confirmada. R diz que a turbidez é "muitas vezes proporcional" à CSS (não sempre); G mostra um caso em que a regressão explica cerca de 93% da variância (rio Kansas) | R p. 1; G p. 6 |
| Ajusta-se curva de calibração local entre turbidez e CSS das amostras | Confirmada ("específica do local") | R p. 1, 6; G p. 5-6 |
| A CSS obtida assim é uma estimativa | Confirmada; R trata a incerteza de forma estatística (intervalos de predição) | R p. 2; G p. 5-6 |
| Relação depende de tamanho, forma e cor das partículas | Confirmada | R p. 5, 25; G p. 5-6, 8 |
| Curva só confiável na faixa de turbidez coberta pelas amostras | Confirmada, com ajuste: o manual fala em "limites ideais" e em julgamento fora deles, não em "só confiável"; e alerta para saturação do sensor | R p. 8, 10-12; G p. 6, 8, 17 |
| Deve ser revisada periodicamente | Confirmada | R p. 22-23, 25; G p. 2, 16 |

* Frase recomendada (junta R e G; a citação dupla vai no fim):
  "A carga de sedimentos em suspensão é a soma, ao longo do tempo, do produto entre a vazão e a concentração de sedimentos em suspensão (CSS) (RASMUSSEN et al., 2009). A CSS só é medida diretamente em amostras coletadas na seção; a turbidez, medida de forma contínua e correlacionada com a CSS, permite estimá-la por uma curva de calibração ajustada localmente às amostras (RASMUSSEN et al., 2009; GRAY; GARTNER, 2009). Essa CSS é uma estimativa: a turbidez também depende do tamanho, da forma e da cor das partículas, a curva deve ser usada de preferência na faixa de turbidez coberta pelas amostras do ajuste e precisa ser verificada periodicamente com novas amostras (RASMUSSEN et al., 2009; GRAY; GARTNER, 2009)."

---

### 2.3 Gray e Gartner (2009) - PDF 3 (afirmação B)

* Referência ABNT: GRAY, J. R.; GARTNER, J. W. Technological advances in suspended-sediment surrogate monitoring. **Water Resources Research**, v. 45, n. 4, art. W00D29, 20 p., 2009. DOI: 10.1029/2008WR007063. (O DOI aparece no cabeçalho e na citação sugerida do próprio artigo; o número do fascículo, 4, vem do cabeçalho do arquivo da Wiley.)
* Nível de leitura: texto completo por OCR (arquivo é só imagem). Páginas citadas são as do artigo (1 a 20, rodapé "n of 20").
* O que a obra diz de útil:
  * Compara quatro técnicas de monitoramento contínuo que substituem amostras (turbidez, laser, diferença de pressão, retroespalhamento acústico). Para o TCC interessa só a turbidez (seção 2.1, p. 5-8).
  * O método tradicional (amostras) é caro e dá poucas observações, em geral uma por dia ou menos, o que obriga a estimar a CSS por interpolação ou por curva de transporte (p. 2-3).
  * Turbidimetros precisam de calibração empírica local para dar estimativas confiáveis de CSS na seção (p. 5-6, 16). A resposta depende de tamanho, cor, forma e composição das partículas; mudanças de tamanho e de cor exigem recalibração (p. 6, 8). Há saturação do sinal acima de um valor máximo, e a leitura em um ponto pode não representar a seção (p. 8, 17).
  * Cada técnica precisa de calibração periódica com amostras tradicionais, e a necessidade deve diminuir com o tempo (p. 2, 16).
  * A carga em suspensão é obtida multiplicando a CSS pela vazão (p. 3, 8).
* Frase: ver a frase combinada em 2.2. Se quiser frase própria curta: "A turbidez medida de forma contínua só fornece estimativas de CSS depois de calibrada, no local, com amostras tradicionais, e a calibração deve ser refeita periodicamente (GRAY; GARTNER, 2009)."
* Ponto de atenção: o artigo avalia instrumentos nos EUA, com foco em rios de porte médio e grande; os valores de preço e de faixa de CSS são de 2008 e não devem ir para o TCC.

---

### 2.4 Minella, Merten e Magnago (2011) - PDF 4 (afirmação C)

* IMPORTANTE: o arquivo minella.pdf NÃO é o artigo que o Doc cita (Minella et al., 2008, na Hydrological Processes, sobre estimar CSS a partir da turbidez e o "problema da calibração"). É outro artigo do mesmo grupo, de 2011, sobre histerese.
* Referência ABNT: MINELLA, J. P. G.; MERTEN, G. H.; MAGNAGO, P. F. Análise qualitativa e quantitativa da histerese entre vazão e concentração de sedimentos durante eventos hidrológicos. **Revista Brasileira de Engenharia Agrícola e Ambiental**, Campina Grande, v. 15, n. 12, p. 1306-1313, 2011. DOI: não consta no PDF.
* Nível de leitura: texto completo (8 p.). Páginas impressas 1306 a 1313.
* O que a obra diz de útil:
  * Bacia rural pequena (1,19 km2) em Arvorezinha, RS, cultivo de fumo, 19 eventos com vazão lida a cada 10 min e CSS por amostragem durante os eventos e por monitoramento automático de turbidez (p. 1309).
  * A relação entre vazão e CSS tem padrões temporais complexos nos eventos; para a mesma vazão a CSS na subida do hidrograma é diferente da CSS na descida (p. 1306, 1307). Laços horário, anti-horário e em oito (p. 1307-1308).
  * Em 17 dos 19 eventos o laço foi horário (pico de CSS antes do pico de vazão); um foi anti-horário e um em oito (p. 1309). O índice de histerese variou muito entre eventos (média 3,21; de -0,12 a 12,63) (p. 1309).
  * Os autores atribuem essa variação, como provável, à disponibilidade de sedimentos (revolvimento do solo, cobertura, umidade e chuvas em sequência), à intensidade da chuva e ao manejo (p. 1308, 1311-1312). Atenção: os testes estatísticos entre grupos (manejo convencional x conservacionista; chuva maior ou menor que 40 mm) NÃO mostraram diferença significativa, e os autores dizem que são necessários mais eventos (p. 1310-1312).
  * Sobre modelos: muitas vezes os modelos não representam a defasagem entre hidrograma e sedimentograma e, com isso, superestimam a produção de sedimentos, porque a concentração máxima coincide com a vazão máxima (p. 1312). Isso apoia o argumento do TCC sobre a defasagem, mas é sobre modelos de produção de sedimentos de evento, não sobre curvas-chave.
  * Sobre a turbidez: o artigo só informa que a turbidez foi convertida em CSS por uma "curva-chave" do local, estabelecida em Minella et al. (2008) (p. 1309). Não discute calibração, faixa de validade nem incerteza da turbidez.
* Conferência da afirmação C:

| Parte da frase do TCC | Veredito | Onde |
|---|---|---|
| Séries de alta resolução (turbidez horária ou subhoraria) permitem acompanhar a variação da concentração dentro do evento | Parcialmente: o estudo acompanha CSS e vazão dentro do evento (vazão a cada 10 min, turbidez automática e amostras), mas o artigo não informa o intervalo da turbidez e não discute resolução temporal da turbidez | p. 1309 |
| Para a mesma vazão, a concentração difere na subida e na descida (histerese) | Confirmada | p. 1306-1308 |
| A histerese mostra que a carga do evento não pode ser estimada só pela vazão por uma relação fixa | NÃO CONFIRMADA nessas palavras. O artigo não fala de curva-chave de sedimentos. Diz que ignorar a defasagem em modelos leva a superestimar a produção de sedimentos (p. 1312). A conclusão sobre relação fixa é inferência do TCC | p. 1312 |
| A concentração média de cada evento varia com a disponibilidade de sedimento | Parcialmente: o que varia entre eventos é o índice de histerese (forma da relação), e a disponibilidade de sedimento é apontada como causa provável. O artigo não apresenta concentração média por evento como resultado | p. 1309-1312 |
| Problema de calibração da turbidez, faixa de validade, variabilidade da relação | NÃO CONFIRMADA: não está neste PDF (é tema de Minella et al., 2008) | p. 1309 |

* Frase recomendada (só histerese; sem calibração):
  "Em uma bacia rural de 1,19 km2 no sul do Brasil, a concentração de sedimentos em suspensão para uma mesma vazão foi diferente na subida e na descida do hidrograma (histerese), em laço horário em 17 de 19 eventos, e a magnitude dessa defasagem variou bastante entre eventos, o que os autores relacionam, como provável, à disponibilidade de sedimento, ao manejo do solo e à chuva (MINELLA; MERTEN; MAGNAGO, 2011)."
* Frase fraca para a "relação fixa" (se o Luis quiser manter a ideia): "Modelos que não representam essa defasagem entre vazão e concentração tendem a superestimar a produção de sedimentos do evento (MINELLA; MERTEN; MAGNAGO, 2011)." A frase "a carga do evento não pode ser estimada só pela vazão por uma relação fixa" fica como raciocínio do TCC, sem citação, ou aguarda Williams (1989).
* O que fazer com o marcador do Minella et al. (2008): manter o marcador [REFERÊNCIA A LER] para a parte da calibração da turbidez. Se citar a obra de 2011, ela é uma OBRA DIFERENTE e entra na lista como Minella, Merten e Magnago (2011).
* Avisos de referência (conferir na fonte original):
  * A lista de referências do artigo de 2011 traz o artigo de 2008 com a ordem Minella, Merten, Clarke e Reichert e as páginas "1819-1930" (parece erro de impressão para 1819-1830). A nota anterior (lote E, 30/10) tinha Reichert antes de Clarke. Conferir a ordem dos autores na página da revista antes de montar a referência de 2008.
  * Ele cita Williams (1989) com páginas 89-116; a nota anterior tinha 89-106. Citação secundária pode ter erro; conferir em Williams.
  * Ele usa Williams (1989) para a classificação dos laços (p. 1307-1308) e diz, segundo Williams, que a falta de grande suprimento de sedimentos é a causa mais comum do laço horário em bacias pequenas (p. 1311). Isso é informação de segunda mão; não usar como se tivesse lido Williams.

---

### 2.5 Ochoa-Rodriguez et al. (2015) - PDF 5 (tema D)

* Referência ABNT: OCHOA-RODRIGUEZ, S. et al. Impact of spatial and temporal resolution of rainfall inputs on urban hydrodynamic modelling outputs: a multi-catchment investigation. **Journal of Hydrology**, v. 531, p. 389-407, 2015. DOI: 10.1016/j.jhydrol.2015.05.035. (18 autores; primeiro autor Susana Ochoa-Rodriguez, Imperial College London; coautores incluem Li-Pen Wang, Auguste Gires, Marie-Claire ten Veldhuis e Patrick Willems. Disponível online em 27/05/2015; acesso aberto, licença CC BY-NC-ND.)
* Identificação em relação às candidatas: NÃO é Faurès et al. (1995) (J. Hydrol. 173:309-326) nem Williams (1989). Faurès et al. (1995) é citado por este artigo (introdução, p. 390, e lista de referências) como uma das obras que mostram a necessidade de chuva de alta resolução em bacias urbanas. Lobligeois et al. (2014, HESS 18:575-594, "When does higher spatial resolution rainfall information improve streamflow simulation? An evaluation using 3620 flood events") também é citado aqui (p. 389, 404) e pode ser mais próximo de bacias rurais; não li.
* Nível de leitura: parcial (ver tabela).
* O que a obra diz de útil:
  * Usa chuva de radar de banda X (100 m e 1 min) agregada em 15 combinações até 3.000 m e 10 min, aplicada a modelos hidrodinâmicos semi-distribuídos de 7 bacias urbanas de 3 a 8 km2 na Europa, com 9 eventos (resumo; p. 389, 392-393).
  * Resultado 1: o efeito da resolução da chuva de entrada nas saídas do modelo diminui rapidamente quando a área de drenagem aumenta (resumo; p. 404). Em áreas de cerca de 1 ha, a redução da resolução gerou erros de pico de vazão de até 250%; para áreas de cerca de 800 ha, o erro máximo foi da ordem de 50% (p. 404).
  * Resultado 2: em geral, a resolução temporal da chuva pesa mais que a espacial (resumo; p. 404-405). Resultado 3: há forte interação entre as duas (p. 405).
  * Para qualquer área de drenagem de 1 a 800 ha, uma resolução espacial de 3 km, "que pode ser comparada às distâncias comuns entre pluviômetros", foi insuficiente (p. 405). Para áreas acima de 100 ha, 1 km bastou, desde que o passo de tempo fosse menor que 5 min (p. 405).
  * Limites que os próprios autores dão: os resultados valem para os eventos e para o tipo de modelo (semi-distribuído, calibrado com pluviômetros de baixa resolução espacial); modelos totalmente distribuídos tendem a ser mais sensíveis (p. 405). Os autores dizem que alguns resultados "não são muito robustos e devem ser lidos como tendências" (seção 4).
* Relação com os temas do item D:

| Tema | O PDF 5 diz algo? |
|---|---|
| Incerteza de entrada em modelos hidrológicos | Sim, é o tema central: a resolução da chuva de entrada muda as saídas do modelo (p. 389-390, 404-405) |
| Densidade de postos de chuva | Só em uma frase (p. 405: 3 km seria comparável a distâncias comuns entre pluviômetros e é insuficiente em bacias urbanas de 1 a 800 ha). Não estuda densidade de postos |
| Interpolação (IDW) | NÃO. Não há IDW, krigagem nem Thiessen; a chuva vem de radar, e as resoluções grossas são feitas por média no espaço (p. 396) |
| Delimitação de eventos | NÃO. Os 9 eventos foram escolhidos de uma série de radar e o período de pico foi selecionado "manualmente" para análise (p. 393, 396); isso não é um método de delimitação de eventos |
| Resolução temporal da chuva | Sim: abaixo de 5 min para bacias urbanas (p. 404-405). Não se aplica diretamente a uma bacia rural grande com dados horários |

* Para o TCC (cap. 4, incerteza de entrada): serve como evidência geral de que a chuva de entrada, especialmente com poucos pontos, é fonte de incerteza e que o efeito depende da escala da bacia. Para uma bacia maior e rural, o artigo sozinho não prova o tamanho do efeito: a faixa estudada termina em 800 ha, e o contexto é urbano e com modelos de esgoto.
* Frase recomendada (cautelosa):
  "A resolução espacial e temporal da chuva de entrada altera os resultados de modelos hidrológicos, e esse efeito diminui à medida que a área de drenagem aumenta; em bacias urbanas de 1 a 800 ha, uma resolução espacial de 3 km, comparável à distância usual entre pluviômetros, foi insuficiente para reproduzir a resposta simulada (OCHOA-RODRIGUEZ et al., 2015)."
  Ressalva a acrescentar no texto ou na discussão: o estudo é de bacias urbanas, com chuva de radar e modelos de drenagem; serve como indício, não como regra para a bacia do alto Jundiaí.
* Não usar este PDF para sustentar a escolha de IDW nem a delimitação manual dos eventos.

---

## 3. O que ainda falta ler

Nenhum dos 5 PDFs é uma das obras abaixo. Conferi título, autores e DOI no próprio arquivo de cada PDF:

* Varma e Simon (2006), BMC Bioinformatics 7:91: NÃO está entre os PDFs. Continua sem leitura. É a fonte mais direta para "parâmetros ajustados nos mesmos dados dão estimativa otimista" e para a validação aninhada; ajudaria a firmar a primeira metade da afirmação A.
* Faurès et al. (1995), J. Hydrol. 173:309-326: NÃO está entre os PDFs (o PDF 5 só o cita). Continua sem leitura. Serve ao tema da variabilidade espacial da chuva em bacias pequenas.
* Williams (1989), J. Hydrol. 111:89-(106 ou 116, conferir): NÃO está entre os PDFs (o PDF 4 só o cita). Continua sem leitura. Seria a fonte primária da histerese e da frase sobre "relação fixa".
* Minella et al. (2008), Hydrological Processes 22:1819-1830: NÃO está entre os PDFs (o arquivo minella.pdf é o de 2011). Continua sem leitura. É a fonte da parte "calibração da turbidez" da afirmação C.
* Krstajic et al. (2014): citada nas notas anteriores como prioridade; não está entre estes PDFs.
* Possível: Lobligeois et al. (2014) (HESS 18:575-594), citado no PDF 5, para o efeito da resolução da chuva em bacias não urbanas.

Pendências de redação que dependem do usuário e do Luis:
1. A afirmação A: aceitar a versão ajustada (a validação cruzada simples não é descrita assim por Cawley e Talbot) ou buscar Varma e Simon.
2. A afirmação C: decidir se usa Minella, Merten e Magnago (2011) para histerese (obra diferente da citada hoje) e se espera o artigo de 2008 para a parte da turbidez.
3. Tema D: o PDF 5 não substitui uma fonte sobre IDW ou densidade de postos em bacias rurais.
