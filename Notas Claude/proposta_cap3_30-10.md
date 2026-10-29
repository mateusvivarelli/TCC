# Proposta do capítulo 3: MATERIAIS E MÉTODOS (30/10/2026)

Sessão na nuvem, sem acesso ao usuário nem ao Doc. **Nada foi aplicado no Doc.** Este arquivo substitui, para o capítulo 3, as propostas de 29/10 (`proposta_secao4.md`), já com a estrutura pedida pelo Luis (S11, S14 a S19) e com o que sai do capítulo 2 (C9, C11, C12, C15, C16).

Convenções:
- Equações em texto simples, marcadas `[EQUAÇÃO]`, para o usuário criar no editor de equações do Docs. Subscrito escrito com "_" (por exemplo, E_unit,k = E com subscrito "unit,k"); o índice k é o pixel e o índice n é o evento, como no Doc.
- Caracteres de teclado: `*` e `-`, decimais com vírgula; especiais só λ, α, β, ², ³ e Σ.
- Legendas: identificação acima da tabela/figura, "Fonte:" abaixo.
- Citações no padrão do Doc (caixa alta dentro dos parênteses). Nível de leitura de cada obra citada no fim do arquivo.
- "[a calcular no PC: ...]" marca número que depende dos rasters (não há rasters na nuvem).
- As seções 3.1 a 3.3 já estão no Doc; aqui só o que muda nelas (detalhe dos pares de troca em `ajustes_cap1_a_3_30-10.md`). O texto novo começa na 3.4.

---

# 3. MATERIAIS E MÉTODOS

## 3.1 Área de estudo

Sem mudança (texto atual do Doc, com a Figura 1).

## 3.2 Dados observados de vazão e descarga sólida de sedimentos em suspensão

Texto atual com as sugestões S9, S10 e S12 aceitas, mais o parágrafo da série de vazão de base vindo da 2.4 (item 5.3 de `ajustes_cap1_a_3_30-10.md`). Tabelas 1 e 2 sem mudança de conteúdo; Tabela 3 só com os valores medidos (item 5.4 do mesmo arquivo).

## 3.3 Dados geoespaciais

Texto atual com S13 aceita, mais a frase do CN-I (31 a 95) e a frase do LS e da escala do mapa de solos vindas da 2.3 e da 2.6 (itens 5.5 a 5.8 de `ajustes_cap1_a_3_30-10.md`). Tabelas 4 a 6 e Figuras 2 e 3 sem mudança.

---

## 3.4 Espacialização da MUSLE

O trabalho estima, para cada um dos 17 eventos, a erosão produzida em cada pixel da bacia e o sedimento que chega ao exutório, e compara o resultado com a carga de sedimentos medida. A Figura 4 resume o fluxo. Para cada evento, a chuva medida nos dois postos é interpolada para todos os pixels (seção 3.4.1.4); o método SCS-CN converte a chuva de cada pixel em escoamento superficial direto, segundo o número de curva do pixel (seção 3.4.2); a vazão de pico local e a erosão local de cada pixel são calculadas pela fórmula de Williams aplicada pixel a pixel (seção 3.4.3); e a soma da erosão dos pixels, multiplicada por um coeficiente de escala c, dá o sedimento do evento (seção 3.4.4). O coeficiente c é calibrado contra a carga medida no exutório, em escala logarítmica (seção 3.4.5), e o desempenho é avaliado por validação cruzada leave-one-out (seção 3.4.6), com as métricas da seção 3.4.7. O modelo é comparado com outras formulações (seção 3.4.8), e os mapas de erosão são analisados por classe de uso, de solo e de declividade (seção 3.4.9).

[IMAGEM] Figura 4

Figura 4. Fluxograma do método.

Fonte: elaborado pelo autor.

(Arquivo: `TCC_Texto/figuras/mapas/fig_fluxograma.png`, já regerado com o modelo oficial. Conferir antes se a imagem não traz a palavra "água" para o escoamento; ver item G.)

O modelo foi aplicado de duas formas, que diferem apenas na origem do escoamento superficial direto de cada evento. No Modelo Calculado de Erosão (MC), o escoamento vem da chuva pelo SCS-CN: é uma previsão, que só usa a chuva dos postos. No Modelo Forçado ao Medido (MFM), o volume de escoamento direto de cada evento é o medido no exutório, e o SCS-CN apenas o distribui no espaço: é uma referência, que mostra o desempenho que a mesma formulação de erosão atingiria se o escoamento fosse bem estimado (seção 3.4.4).

Todos os cálculos foram feitos em Python, com as bibliotecas NumPy, pandas, SciPy e GDAL, em uma rotina que lê os rasters e as séries de cada evento, calcula o escoamento, a erosão e o sedimento dos 17 eventos, calibra e valida o coeficiente e gera as tabelas e os mapas. O QGIS foi usado na preparação dos rasters (recorte, reprojeção e conferência).

> Nota (não vai para o Doc): o parágrafo da rotina responde ao objetivo específico 2, que não era descrito no método (revisão de 29/10, R3.4). Bibliotecas conferidas nos `import` de `Scripts/calcular_sy_lambda005_woodward.py` (numpy, pandas, osgeo.gdal, scipy). O uso do QGIS vem das notas do projeto ("raster de chuva do QGIS"); o usuário deve confirmar o que exatamente foi feito no QGIS.

### 3.4.1 Preparação dos dados

#### 3.4.1.1 Variáveis de cada evento e pixels de cálculo

Todos os dados espaciais foram colocados na mesma grade, a do raster de chuva (884 * 365 pixels, SIRGAS 2000 / UTM 23S, pixel de 29,992 * 29,925 m, área Apix = 897,49 m²). O raster de número de curva, que tinha outra grade (973 * 362), foi reamostrado pelo vizinho mais próximo, isto é, cada pixel da grade de cálculo recebe o valor do pixel do raster original que contém o seu centro. O cálculo da erosão só é feito nos pixels em que existem, ao mesmo tempo, número de curva, K, C e LS (153.855 pixels, 138,1 km²); os demais ficam sem valor. As variáveis usadas estão na Tabela 7.

Tabela 7. Variáveis usadas no modelo.

| Símbolo | Significado | Unidade |
|---|---|---|
| P1, P2 | chuva total do evento nos postos DBT5 e Campo Limpo | mm |
| R | lâmina de chuva do evento (Tabela 2) | mm |
| RI | maior intensidade de chuva em 60 min entre os dois postos | mm/h |
| P_k | chuva do evento interpolada no pixel k | mm |
| CN_k, S_k | número de curva e retenção potencial máxima do pixel k | -, mm |
| Q_k | escoamento superficial direto no pixel k | mm |
| pr,k | vazão de pico local do pixel k | m³/s |
| K_k, C_k, LS_k, P | fatores da USLE no pixel k | (Tabela 4) |
| E_unit,k | índice de erosão local do pixel k | índice relativo |
| c | coeficiente de escala do modelo | t por unidade de E_unit |
| TR | volume total escoado no exutório no evento | m³ |
| Bt | vazão de base na hora t | m³/s |
| Vdir | escoamento direto medido, TR - Σ Bt * 3.600 | m³ |
| SYobs | carga de sedimentos medida no evento (total) | t |
| SY | sedimento simulado no evento | t |

Fonte: elaborado pelo autor.

> Nota: saíram da Tabela 7 antiga Tchuva, Vbase e Qbinicio (eram do modelo de dois componentes) e entraram as variáveis por pixel. RI definido como "maior intensidade entre os dois postos" porque é o que a planilha traz (revisão de 29/10, achado 1).

#### 3.4.1.2 Fatores K, C, LS e P

Os fatores K e C foram atribuídos por classe (Tabelas 5 e 6): cada pixel recebe o valor da classe de solo ou de uso do polígono que contém o seu centro. Essa regra reproduz exatamente os rasters de K e de C usados no trabalho (verificado pixel a pixel). Os valores por classe são os da Iniciação Científica anterior (VIVARELLI et al., 2025) e não foram recalibrados. Nas áreas urbanizadas e nos corpos d'água, C é zero, e nas áreas urbanas sem classe de solo, K é zero; esses pixels têm erosão nula no modelo.

O fator LS foi calculado sobre o modelo digital de elevação corrigido, em projeção UTM, pela formulação de Moore e Burch (1986), baseada na potência do escoamento:

[EQUAÇÃO] LS_k = (As,k / 22,13)^0,4 * (sen β_k / 0,0896)^1,3

em que As,k é a área de contribuição específica do pixel (área a montante dividida pela largura da célula, em m) e β_k é a declividade do pixel. Adotou-se As máxima de 200 m: sem limite, a área de contribuição chega a milhões de metros nos pixels de canal, onde a USLE, que descreve a erosão de encosta, deixa de valer. O LS médio na bacia é 7,80. O fator P é igual a 1,0 em toda a bacia, porque não há práticas conservacionistas mapeadas.

> Notas: (1) atribuição dos expoentes 0,4 e 1,3 a Moore e Burch (1986) pendente (podem ser de Moore e Wilson, 1992); Moore e Burch lido só pelo resumo. (2) O limite de 200 m é escolha do TCC (o AH 537 não fixa esse valor). (3) Atenção ao símbolo: β aqui é a declividade; na IC (seção 3.4.8) β é o expoente. Se o usuário preferir, usar θ_k para a declividade, mas θ não está na lista de caracteres permitidos; alternativa: "sen(declividade_k)".

#### 3.4.1.3 Número de curva, razão de abstração inicial e retenção S

O número de curva vem do raster BR_CN-2022 da ANA (2024), na condição de umidade média (CN-II), com valores de 52 a 98 e média de 71,6 nos pixels de cálculo (seção 3.3). Adotou-se a condição seca (CN-I) para os 17 eventos, obtida pela conversão de Chow, Maidment e Mays (1988):

[EQUAÇÃO] CN-I_k = 4,2 * CN-II_k / (10 - 0,058 * CN-II_k)

Essa conversão reproduz o raster de CN seco usado no trabalho (diferença menor que 10^-5). O CN passa a variar de 31 a 95, com média de 52,5. A retenção potencial máxima correspondente ao CN tabelado, definido para λ = 0,20, é:

[EQUAÇÃO] S0,20,k = 25,4 * (1000 / CN-I_k - 10)

e tem média de 255,7 mm na bacia (de 12 a 558 mm entre os pixels).

Adotou-se a razão de abstração inicial λ = 0,05, com a retenção convertida pela relação de Woodward et al. (2003) (seção 2.3), escrita em milímetros:

[EQUAÇÃO] S0,05,k = 25,4 * 1,33 * (S0,20,k / 25,4)^1,15

A retenção convertida tem média de 489,9 mm na bacia e é maior que S0,20 em todos os pixels, como esperado: com abstração inicial menor, a retenção precisa ser maior para gerar um escoamento da mesma ordem.

A combinação de CN-I, λ = 0,05 e retenção convertida foi escolhida porque, com ela, o volume de escoamento direto calculado no conjunto dos 17 eventos ficou próximo do medido (viés de +3%; seção 4.1). A condição seca é, portanto, uma condição única para o conjunto de eventos, escolhida pelo volume, e não uma medida da umidade antecedente de cada evento. Essa escolha foi feita observando os mesmos eventos usados na avaliação, o que é considerado na seção 3.4.6. Na bacia, 8,4% dos pixels têm CN-I abaixo de 35 e os eventos 1 e 12 têm lâmina abaixo de 25,4 mm, fora das faixas em que a relação de Woodward foi obtida (seção 2.3); nesses casos, a conversão é extrapolação.

> Notas: (1) "viés de +3%" é o volume total SCS-CN/medido 15,7/15,3 milhões de m³ (conferido em 29/10). (2) Não cito o critério dos 5 dias do NEH-4 (original não lido; o NRCS 2004 o abandonou): a justificativa do CN-I fica pelo volume. Se o usuário quiser a frase do NEH, ela está em `proposta_secao4.md` (4.2.3) e exige NRCS (2004) na lista. (3) "λ = 0,20" aparece só como valor de definição do CN tabelado, permitido pela regra do usuário. (4) Chow, Maidment e Mays (1988) não acessado (fórmula conferida em fonte secundária e contra a tabela do NEH-630).

#### 3.4.1.4 Chuva espacializada

Os dois postos medem a chuva em pontos. Para estimar a chuva em cada pixel, usou-se o inverso do quadrado da distância (IDW, potência 2), em que o peso de cada posto decresce com o quadrado da distância ao pixel (seção 2.7):

[EQUAÇÃO] P_k = (P1 * d2,k² + P2 * d1,k²) / (d1,k² + d2,k²)

em que P1 e P2 são as chuvas medidas nos postos DBT5 e Campo Limpo, e d1,k e d2,k são as distâncias (m) do centro do pixel k a cada posto, em coordenadas UTM. Os postos foram projetados de latitude e longitude (EPSG:4326) para SIRGAS 2000 / UTM 23S: DBT5 em E 348.520,8 m e N 7.426.415,3 m, e Campo Limpo em E 319.862,4 m e N 7.432.277,5 m. Com apenas dois postos, um deles fora da bacia, o resultado é um gradiente suave entre os pontos, que muda de evento para evento conforme a chuva medida em cada posto. Esse cálculo reproduz o raster de chuva do QGIS com diferença menor que 10^-5 mm.

A lâmina de chuva do evento, R, usada na concentração temporal da chuva (seção 3.4.3), é a da planilha de eventos (Tabela 2). Ela corresponde, com diferença de até 0,6 mm, à média ponderada dos dois postos com pesos de 0,307 (DBT5) e 0,693 (Campo Limpo), e a intensidade RI é a maior intensidade horária registrada entre os dois postos.

> Notas: (1) a origem da coluna `Chuva_evento_mm` não está documentada (pergunta ao Luis no item I); os pesos 0,307/0,693 são os de mínimos quadrados que reproduzem a coluna (resíduo máximo 0,57 mm, evento 16; revisão de 29/10, achado 3). Por isso o texto diz "corresponde" e não "foi calculada". Quando o Luis responder, trocar pela origem real. (2) A frase da reprodução do QGIS vem do Doc atual; não verificável na nuvem.

### 3.4.2 Escoamento direto por pixel (SCS-CN)

Para cada pixel, o escoamento superficial direto Q_k (mm) depende da chuva P_k e da retenção S0,05,k do pixel, com abstração inicial igual a 0,05 * S0,05,k:

[EQUAÇÃO] Q_k = (P_k - 0,05 * S0,05,k)² / (P_k + 0,95 * S0,05,k), se P_k > 0,05 * S0,05,k

[EQUAÇÃO] Q_k = 0, se P_k <= 0,05 * S0,05,k

O escoamento calculado é só o direto; a vazão de base não entra no cálculo da erosão. O volume de escoamento direto do evento calculado pelo SCS-CN é V_SCS = Σk Q_k / 1000 * Apix (m³), comparado com o volume medido Vdir na seção 4.1.

> Nota: forma geral com λ (seção 2.3) e substituição λ = 0,05 é álgebra; no evento 11 nenhum pixel fica sem escoamento; no conjunto, 14,0% dos pares pixel-evento não geram escoamento (checagem de 27/10, item d; não reconferido nesta sessão).

### 3.4.3 Vazão de pico local e erosão local

A fórmula de Williams (seção 2.2) usa o volume e a vazão de pico do escoamento. Seguindo Hao et al. (2022), cada pixel tem a sua própria vazão de pico, calculada sem roteamento hidráulico: o volume escoado no pixel é ponderado pela concentração temporal da chuva do evento, medida pela razão entre a intensidade máxima RI e a lâmina R:

[EQUAÇÃO] pr,k = (Q_k / 1000) * Apix * (RI / R) / 3600

O produto (Q_k / 1000) * Apix é o volume escoado no pixel (m³). A razão RI/R (por hora) é maior quando a chuva do evento se concentra em poucas horas, e a divisão por 3.600 passa de horas para segundos. Como RI/R é um único número por evento, pr,k é proporcional a Q_k em todos os pixels: o pico local não traz informação espacial além da que já está no escoamento, e o seu papel é dar mais peso aos eventos de chuva concentrada. Nos eventos 1 e 12, RI/R passa de 1, porque RI vem do posto mais intenso e R é a lâmina ponderada dos dois postos (no evento 12, o posto DBT5 não registrou chuva); por isso RI/R é tratado como um índice de concentração temporal da chuva, e não como a fração da chuva que cai na hora mais intensa.

A erosão local é a fórmula de Williams aplicada ao pixel, com os coeficientes originais:

[EQUAÇÃO] E_unit,k = 11,8 * (Q_k * pr,k * Apix)^0,56 * K_k * C_k * LS_k * P

com Q_k em mm, pr,k em m³/s e Apix em m², como em Hao et al. (2022). Como pr,k é proporcional a Q_k, E_unit,k é proporcional a Q_k^1,12.

E_unit,k é um índice relativo de erosão, e não uma massa em toneladas, por dois motivos. Primeiro, a equação de Williams foi ajustada para bacias inteiras, com o volume do evento em m³ e o pico em m³/s, e aqui é aplicada a pixels de 897 m², com o escoamento em mm; os valores do produto Q_k * pr,k * Apix ficam muito abaixo da faixa em que os coeficientes 11,8 e 0,56 foram obtidos. Segundo, a equação é côncava (expoente 0,56): a soma dos valores calculados nos pixels não é igual ao valor que a equação daria para a bacia inteira; para n pixels iguais, a razão entre os dois é n^0,12. As constantes de escala e de unidade ficam, assim, todas no coeficiente c (seção 3.4.4), que converte a soma dos índices em toneladas.

> Notas: (1) Explicação do pico local e do E_unit pedida pelo Luis na reunião (`pontos_discussao_e_reuniao_29-10.md`, "Luis pediu: explicar melhor o Qpico"). (2) O fator 1/1000 não aparece na fórmula impressa em Hao et al. (2022), segundo o lote A; é correção de unidade absorvida por c (frase opcional; não reconferida). (3) Williams (1975) não lido no original; equação e coeficientes por fonte secundária e AH 537. Não afirmo a faixa exata das bacias de Williams; "muito abaixo da faixa" decorre da ordem de grandeza (Q_k * pr,k * Apix no pixel de exemplo do Anexo vale cerca de 6 * 10^-3, contra volumes de 10^5 a 10^6 m³ e picos de 10 m³/s nas bacias).

### 3.4.4 Sedimento do evento e versões do modelo

O sedimento simulado do evento n é proporcional à soma da erosão local de todos os pixels de cálculo:

[EQUAÇÃO] SY_n = c * Σk E_unit,k,n

em que a soma é feita sobre os 153.855 pixels de cálculo e c (t por unidade de E_unit) converte o índice em toneladas.

A formulação segue Hao et al. (2022) sem o índice de conectividade. Na escala da bacia, a MUSLE dispensa a razão de entrega de sedimentos (seção 2.2); aplicada ao pixel, ela estima a erosão local, e a parte que chega ao exutório precisa de um fator. Hao et al. (2022) usam um grau de conectividade de cada pixel; aqui esse papel é feito pelo coeficiente c, que é único para toda a bacia. O coeficiente representa, assim, uma conectividade média da bacia e absorve também a diferença de escala entre a equação de Williams e o pixel (seção 3.4.3); por isso não deve ser lido como uma razão de entrega. Como c é o mesmo em todos os pixels, o mapa de c * E_unit,k mostra onde a erosão local é produzida, e não onde o sedimento efetivamente chega à rede de drenagem.

O alvo da calibração, SYobs, é a carga total medida no evento (seção 3.2). Toda a carga medida é comparada com a erosão das encostas, que é o que o modelo representa: admite-se que o sedimento do evento foi mobilizado pelo escoamento superficial e que a vazão de base atua apenas como meio de transporte. Parte da carga pode vir do canal e das margens, que o modelo não separa (seção 4.6).

As duas versões do modelo diferem na origem do escoamento direto (Tabela 8). No MC, Q_k é o calculado pelo SCS-CN a partir da chuva interpolada (seção 3.4.2). No MFM, o volume de escoamento direto de cada evento é forçado ao valor medido, Vdir = TR - Σ Bt * 3.600: o escoamento de todos os pixels é multiplicado pelo mesmo fator f_n = Vdir,n / V_SCS,n, e o escoamento de cada pixel é limitado à chuva do pixel, porque o escoamento não pode superar a chuva:

[EQUAÇÃO] Q_MFM,k = min(f_n * Q_k, P_k)

O SCS-CN, no MFM, apenas distribui no espaço o volume medido. O limite Q <= P atua nos eventos em que f_n é grande (o SCS-CN subestimou muito o volume) e, nesses, o volume distribuído fica um pouco abaixo do medido [a calcular no PC: soma de Q_MFM,k * Apix / 1000 contra Vdir por evento; maior perda esperada no evento 10, f = 9,75]. O MFM não é uma previsão: depende do volume medido no mesmo hidrograma em que se mede a carga.

Tabela 8. Versões do modelo.

| Versão | Escoamento direto por pixel | Informação medida usada |
|---|---|---|
| Modelo Calculado de Erosão (MC) | Q_k do SCS-CN (CN-I, λ = 0,05, S convertido), a partir da chuva interpolada | chuva nos dois postos |
| Modelo Forçado ao Medido (MFM) | Q_k do SCS-CN multiplicado por f_n = Vdir,n / V_SCS,n, limitado a P_k | chuva nos dois postos e volume de escoamento direto medido |

Fonte: elaborado pelo autor.

> Notas: (1) C17 resolvido: sai SY = c1 * Σ + c2 * (Qb,inicio * Tchuva * 3600). (2) Os valores de c ficam só na Tabela 9 (evita repetir). (3) f_n: 9,75 (ev 10), 6,4 (ev 4), 6,3 (ev 1), de `comparacao_SY_lambda005_woodward.csv` (revisão de 29/10, achado 2).

### 3.4.5 Calibração do coeficiente c

O coeficiente c foi ajustado aos 17 eventos em escala logarítmica, minimizando a soma dos quadrados dos erros dos logaritmos:

[EQUAÇÃO] min_c Σn [ ln(SYobs,n) - ln(c * Σk E_unit,k,n) ]²

O problema tem solução direta, a média geométrica das razões entre a carga medida e a soma dos índices:

[EQUAÇÃO] ln c = (1/N) * Σn [ ln(SYobs,n) - ln(Σk E_unit,k,n) ]

com N = 17 eventos. O critério pesa os eventos pelo erro relativo e evita que um único evento muito grande comande o ajuste: o evento 15 responde por 48,7% da soma dos quadrados dos desvios da carga medida em relação à média, e dominaria um ajuste em escala linear. No ajuste, minimizar essa soma equivale a maximizar o NSE em escala logarítmica (seção 3.4.7), que Hao et al. (2022) também usaram como função objetivo. A calibração é feita separadamente para o MC e para o MFM. A Tabela 9 reúne os parâmetros fixos e os calibrados.

Tabela 9. Parâmetros fixos e calibrados.

| Parâmetro | Valor | Origem |
|---|---|---|
| Coeficiente e expoente de Williams | 11,8 e 0,56 | Williams (1975), mantidos |
| Número de curva | CN-II convertido para CN-I | ANA (2024); Chow, Maidment e Mays (1988) |
| Razão de abstração inicial λ | 0,05 | Woodward et al. (2003) |
| Retenção S0,05 | 25,4 * 1,33 * (S0,20 / 25,4)^1,15 (mm) | Woodward et al. (2003) |
| Área de contribuição específica máxima (LS) | 200 m | adotado |
| P (práticas conservacionistas) | 1,0 | sem práticas na bacia |
| c do MC (t por unidade de E_unit) | 0,0344 | calibrado em log, 17 eventos |
| c do MFM (t por unidade de E_unit) | 0,0222 | calibrado em log, 17 eventos |

Fonte: elaborado pelo autor, com base em Williams (1975), ANA (2024), Chow, Maidment e Mays (1988) e Woodward et al. (2003).

> Notas: (1) Saiu a linha "IC refeita: α e β" (regra do usuário: só IC original; a IC vai na Tabela 10). (2) Saiu a linha dos pesos 0,307/0,693 (origem incerta; ver 3.4.1.4). Se o Luis confirmar a origem, volta como "Pesos dos postos na lâmina R". (3) 48,7%: conferido na revisão de 29/10 (R1.3).

### 3.4.6 Validação cruzada

Um parâmetro ajustado aos mesmos dados usados para avaliar o modelo produz uma estimativa de desempenho enviesada para cima, o viés de otimismo (seção 2.8). Para reduzir esse viés, cada evento foi previsto com um coeficiente ajustado sem ele, pela validação cruzada leave-one-out, procedimento também usado por Hao et al. (2022) na MUSLE espacializada: retira-se um evento; ajusta-se c aos 16 eventos restantes, pela equação da seção 3.4.5; prevê-se o sedimento do evento retirado; e repete-se o procedimento para os 17 eventos. As métricas da seção 3.4.7 são calculadas sobre as 17 previsões. Os modelos de comparação da seção 3.4.8 que têm parâmetros ajustados pelo TCC passam pelo mesmo procedimento. Os resultados no ajuste, com os 17 eventos, são mostrados à parte e só têm valor de diagnóstico.

A validação leave-one-out refaz apenas o coeficiente c. As escolhas da condição de umidade (CN-I), da razão de abstração inicial (λ = 0,05) e da conversão da retenção foram feitas antes, observando o volume de escoamento direto dos mesmos 17 eventos (seção 3.4.1.3), e não são refeitas em cada rodada. Uma estimativa livre desse viés exigiria a validação cruzada aninhada, em que todas as escolhas feitas com os dados são repetidas dentro de cada rodada, usando só os eventos de calibração, e o evento retirado serve apenas para o teste [REFERÊNCIA A LER: Varma e Simon (2006) ou Cawley e Talbot (2010); ver lote E]. Com 17 eventos, essa repetição deixaria cada escolha apoiada em 16 eventos e não foi feita; as métricas da validação cruzada devem, portanto, ser lidas como uma estimativa um pouco otimista para essas escolhas. Duas observações reduzem o problema: as escolhas seguiram o volume de escoamento, e não a carga de sedimentos que é avaliada; e os 17 eventos foram mantidos com a mesma lista e a mesma janela em todas as versões.

> Notas: (1) C14, C15, C19. **A referência da validação aninhada (C19) ficou pendente:** a rede desta sessão bloqueou todos os sites de periódicos (BMC, JMLR, PMC, USGS, SciELO, doi.org), e nenhuma obra do lote E pôde ser lida (`leitura_referencias/loteE_medicao_e_validacao.md`). Pela regra do usuário, não citei. Candidatas abertas para o usuário baixar e ler: Varma e Simon (2006), BMC Bioinformatics 7:91 (validação aninhada e viés na seleção de parâmetros); Cawley e Talbot (2010), JMLR 11 (sobreajuste na seleção de modelos). Depois de ler, trocar o marcador "[REFERÊNCIA A LER ...]" pela chamada. O LOO cita Hao et al. (2022), que fizeram validação leave-one-out (lote A, texto completo). (2) "aninhada" sai do título: com um só parâmetro e sem escolhas refeitas em cada rodada, a validação feita não é aninhada; o texto explica o que a aninhada faria. (3) A frase "as escolhas seguiram o volume, não a carga" é da revisão de 29/10 (achado 9), sem números de configurações descartadas (regra do usuário).

### 3.4.7 Métricas de desempenho

Sejam O_n a carga medida e S_n a carga simulada no evento n, com n de 1 a N = 17, e Ō a média das cargas medidas. As métricas principais não dependem da variância dos dados e, por isso, não são dominadas por um único evento.

O erro percentual absoluto de cada evento e a sua mediana sobre os eventos (MedAPE) são:

[EQUAÇÃO] EPA_n = 100 * |S_n - O_n| / O_n

[EQUAÇÃO] MedAPE = mediana(EPA_1, ..., EPA_N)

A mediana evita que erros muito grandes em poucos eventos dominem a métrica. Não se usa a média do erro percentual absoluto, porque ela pune mais a superestimativa (que pode passar de 100%) do que a subestimativa (limitada a 100%) e, por isso, favorece modelos que subestimam.

A fração de eventos dentro de fator 2 é o percentual de eventos em que o simulado fica entre a metade e o dobro do medido:

[EQUAÇÃO] F2 = (100 / N) * [número de eventos com 0,5 <= S_n / O_n <= 2]

A eficiência de Nash-Sutcliffe (NSE; NASH; SUTCLIFFE, 1970) é calculada em escala logarítmica, que dá peso ao erro relativo:

[EQUAÇÃO] NSE_log = 1 - Σn [ln(O_n) - ln(S_n)]² / Σn [ln(O_n) - média(ln O)]²

Vale 1 para um ajuste perfeito, 0 quando o modelo erra tanto quanto prever sempre a média dos logaritmos e é negativa quando erra mais. A versão linear, NSE = 1 - Σn (O_n - S_n)² / Σn (O_n - Ō)², é mostrada como medida secundária, porque é dominada pelo evento 15.

A correlação de ordem de Spearman (ρ) avalia se o modelo ordena os eventos corretamente, sem depender da magnitude. Sem empates, ela é:

[EQUAÇÃO] ρ = 1 - 6 * Σn d_n² / [N * (N² - 1)]

em que d_n é a diferença entre a posição do evento n na ordem dos medidos e na ordem dos simulados.

Para o escoamento direto (seção 4.1), além das mesmas métricas aplicadas aos volumes, usa-se o viés de volume do conjunto dos eventos:

[EQUAÇÃO] Viés = 100 * (Σn V_SCS,n - Σn Vdir,n) / Σn Vdir,n

Para comparar dois modelos avaliados nos mesmos 17 eventos, calculou-se, evento a evento, a diferença entre os erros percentuais absolutos dos dois modelos, e o intervalo de confiança de 95% da mediana dessas diferenças foi obtido por reamostragem dos eventos com reposição (bootstrap, 4.000 reamostragens).

> Notas: (1) C13. Nash e Sutcliffe (1970) não lido no original (lote B): a equação é a forma padrão; se o usuário quiser citar só obra lida, usar "(NASH; SUTCLIFFE, 1970 apud ...)" com uma fonte lida que traga a equação, ou manter como está (decisão no roteiro K). A fórmula do Spearman é a forma padrão sem empates; não há citação (se a banca pedir, citar um livro de estatística lido). (2) O bootstrap só se aplica a modelos do TCC nos mesmos eventos (MC x regra da chuva; MFM x regra do volume). **Não se aplica à IC**, que tem outra lista de eventos e valores originais (seção 3.4.8). (3) A frase sobre a média do erro percentual favorecer a subestimativa é do Doc atual (4.8); reescrita com o motivo.

### 3.4.8 Comparação com outros modelos de erosão

Para saber o que a espacialização acrescenta e de onde vem o erro, o modelo foi comparado com três tipos de formulação (Tabela 10). Todas foram avaliadas com as mesmas métricas (seção 3.4.7) e, com exceção do modelo da IC, pela mesma validação cruzada.

O primeiro é o próprio MFM (seção 3.4.4), que usa a mesma fórmula de erosão, os mesmos fatores e o mesmo padrão espacial do MC, e só troca o volume de escoamento direto calculado pelo medido. A comparação MC x MFM isola o efeito da estimativa do escoamento.

O segundo tipo são modelos simples, sem MUSLE, em que o sedimento do evento é proporcional a uma única grandeza medida: a lâmina de chuva do evento, SY_n = c_R * R_n, que usa a mesma informação que o MC; e o volume de escoamento direto medido, SY_n = c_V * Vdir,n, que usa a mesma informação que o MFM. Os coeficientes c_R e c_V são calibrados em escala logarítmica, pela mesma equação da seção 3.4.5, e validados por leave-one-out. Se o modelo espacializado não superar o modelo simples com a mesma informação, o desempenho vem da informação medida, e não da fórmula de erosão.

O terceiro é a formulação concentrada da Iniciação Científica anterior (VIVARELLI et al., 2025), que aplicou a MUSLE à bacia inteira na forma:

[EQUAÇÃO] Y_n = α * (D_n * qp,n)^β * K * LS * C * P

com o volume escoado D_n (m³) e a vazão de pico qp,n (m³/s) medidos no hidrograma de cada evento, incluindo a vazão de base, e os fatores K, LS e C médios da bacia (0,031; 0,536; 0,267). O coeficiente α = 0,277 e o expoente β = 0,807 foram ajustados por regressão aos 17 eventos da própria IC, sem validação cruzada. Neste trabalho, a IC é usada com os seus valores originais (coeficientes e cargas simuladas publicados), sem recalibração, e as mesmas métricas da seção 3.4.7 foram calculadas sobre os 17 pares de carga medida e simulada da IC. Duas diferenças impedem uma comparação pareada com o MFM: a lista de eventos da IC tem o evento de 24/11/2018 no lugar do de 17/12/2018 usado neste trabalho, e a carga medida atribuída a vários eventos difere da deste trabalho (por exemplo, 129 t contra 211 t no evento de 30/12/2019 e 1.456 t contra 1.710 t no de 20/02/2020). Por isso, a IC é comparada lado a lado, sem bootstrap, e as suas métricas são de ajuste, e não de validação cruzada.

Tabela 10. Modelos de comparação.

| Modelo | Equação | Informação medida usada | Parâmetros e avaliação |
|---|---|---|---|
| MC | SY = c * Σk E_unit,k | chuva | c em log; validação cruzada |
| MFM | SY = c * Σk E_unit,k, com Q forçado a Vdir | chuva e escoamento direto | c em log; validação cruzada |
| Simples com a chuva | SY = c_R * R | chuva | c_R em log; validação cruzada |
| Simples com o escoamento direto | SY = c_V * Vdir | escoamento direto | c_V em log; validação cruzada |
| IC (VIVARELLI et al., 2025) | Y = α * (D * qp)^β * K * LS * C * P | volume total e vazão de pico | α = 0,277 e β = 0,807 da IC; ajuste nos 17 eventos da IC, sem validação cruzada |

Fonte: elaborado pelo autor, com a formulação e os coeficientes de Vivarelli et al. (2025).

> Notas: (1) S19. (2) **IC só com valores originais**: Y simulado da planilha da IC ("CLP Resultados Calibrados"), guardado em `Scripts/_ic_original.py`; nada recalculado. Métricas: MedAPE 22,5%; F2 100%; NSE log 0,91; NSE linear 0,83; Spearman 0,93; erro médio com sinal +4,2% (simulado acima), faixa -37% a +60%. (3) K, LS e C médios da IC (0,031; 0,536; 0,267) e α, β por regressão: lote C (texto completo do artigo da IC). O lote C registra que não se sabe como a IC calculou as médias de K e C. (4) Cargas do evento 12 (30/12/2019) e 17 (20/02/2020): `Y_OBS` de `_ic_original.py` (129,3 e 1.455,7 t) contra Tabela 3 (211 e 1.710 t). (5) Não cito o modelo SY = c * TR (volume total, 17,6%) da revisão de 29/10, porque não foi pedido nem está nas figuras; se o usuário quiser, entra como sexta linha.

### 3.4.9 Mapas de erosão e áreas críticas

Para cada evento, o mapa de erosão é c * E_unit,k em cada pixel (t por pixel). O mapa de erosão média é a média desses valores nos 17 eventos, calculado para o MC e para o MFM. As áreas críticas foram definidas como os 5% dos pixels de cálculo com maior erosão média. A semelhança entre os mapas do MC e do MFM foi medida pela correlação de Pearson entre os valores dos pixels e pela fração de pixels críticos comuns aos dois mapas.

A contribuição de cada classe de uso e de solo foi calculada como a soma da erosão média dos pixels da classe dividida pela soma da bacia, e comparada com a participação da classe na área. A mesma análise foi feita por classes de declividade do terreno, obtida do MDE (0 a 3%, 3 a 8%, 8 a 20%, 20 a 45%, 45 a 75% e acima de 75%), e pelo cruzamento de uso, solo e declividade nos pixels críticos.

Para medir quanto do padrão espacial vem dos fatores fixos e quanto vem do escoamento (C31), usou-se o fato de que, em cada pixel, a erosão média se escreve como o produto de dois termos:

[EQUAÇÃO] Ē_k = c * 11,8 * P * (K_k * LS_k * C_k) * G_k, com G_k = (1/17) * Σn (Q_k,n * pr,k,n * Apix)^0,56

O primeiro termo, K_k * LS_k * C_k, é fixo; o segundo, G_k, reúne a chuva e o número de curva de cada pixel (escoamento e pico local). Em escala logarítmica, ln Ē_k = constante + ln(K_k * LS_k * C_k) + ln G_k, e a variância de ln Ē_k entre os pixels com erosão se divide entre os dois termos. Calculou-se: (a) o R² da regressão de ln Ē_k em ln(K_k * LS_k * C_k), que é a fração da variação espacial explicada só pelos fatores fixos; (b) o R² da regressão de ln Ē_k em ln G_k, que é a fração explicada só pelo escoamento; e (c) a partição do R² total (igual a 1, pois a decomposição é exata) entre os dois termos pela média dos ganhos de R² nas duas ordens de entrada, que reparte a parcela comum. A mesma análise foi feita em escala linear, com o R² entre Ē_k e K_k * LS_k * C_k, que corresponde ao quadrado da correlação de Pearson. Os pixels com erosão nula (área urbanizada e corpos d'água) ficam fora dessa análise.

> Notas: (1) C31, S19. (2) Números: todos "[a calcular no PC]" (precisam dos rasters). A correlação de Pearson de 0,77 (MC) e 0,76 (MFM) com K*C*LS calculada em 28/10 dá R² linear de cerca de 0,59 e 0,58 (só a conta 0,77² e 0,76²; não verificado). (3) Classes de declividade: são as usuais de relevo (plano a escarpado). Elas vêm de classificação da Embrapa que **não li**; por isso o texto não cita fonte. Se o usuário quiser citar, ler a fonte antes. (4) A partição pela média dos ganhos nas duas ordens é a ideia da decomposição de Lindeman, Merenda e Gold (LMG); não li a obra original, por isso o texto descreve o cálculo sem citar. (5) Script sugerido para o PC no roteiro K.

---

# APÊNDICE A - EXEMPLO NUMÉRICO: O EVENTO 11

(Título: o Luis chamou de "Anexo 1" (C20). Pela NBR 14724, o texto elaborado pelo próprio autor é apêndice; "anexo" é material de terceiros. Proponho "APÊNDICE A"; pergunta ao Luis no item I. O conteúdo é o mesmo.)

Este apêndice acompanha o cálculo do evento 11 (04 a 08/07/2019) do início ao fim, com um pixel de exemplo, escolhido entre os pixels de lavoura temporária sobre Argissolo Vermelho-Amarelo com erosão alta, na posição E 330,18 km e N 7.432,86 km. As Figuras A1 e A2 mostram os campos espaciais de cada etapa e a Tabela A1 reúne os resultados.

**Chuva.** Os postos DBT5 e Campo Limpo registraram 62,8 mm e 79,0 mm, e a lâmina do evento é R = 74,0 mm. A maior intensidade horária foi RI = 11,8 mm/h, de modo que a concentração temporal da chuva é RI/R = 11,8 / 74,0 = 0,159 por hora; o evento 11 é um evento longo (91 h), de chuva pouco concentrada. Interpolada pelo IDW, a chuva varia de 63,2 a 79,0 mm na bacia, com média de 73,5 mm nos pixels de cálculo, maior a oeste, perto do posto de Campo Limpo. O pixel de exemplo recebe P = 75,4 mm.

**Retenção.** O pixel tem CN-II = 81,0. Pela conversão para a condição seca, CN-I = 4,2 * 81,0 / (10 - 0,058 * 81,0) = 64,2. A retenção correspondente ao CN tabelado é S0,20 = 25,4 * (1000 / 64,2 - 10) = 141,9 mm, e a retenção convertida para λ = 0,05 é S0,05 = 25,4 * 1,33 * (141,9 / 25,4)^1,15 = 244,2 mm. Na bacia, a retenção convertida tem média de 489,9 mm.

**Escoamento direto.** A abstração inicial do pixel é 0,05 * 244,2 = 12,2 mm. Como a chuva (75,4 mm) é maior que a abstração inicial, há escoamento: Q = (75,4 - 12,2)² / (75,4 + 0,95 * 244,2) = 13,00 mm. Na bacia, o escoamento médio dos pixels é 7,2 mm, todos os pixels geram algum escoamento, e o volume calculado pelo SCS-CN é de 997 mil m³, contra 1.479 mil m³ de escoamento direto medido (razão 0,67).

**Pico local.** O volume escoado no pixel é 13,00 / 1000 * 897,49 = 11,67 m³, e o pico local é pr = 11,67 * 0,159 / 3600 = 5,17 * 10^-4 m³/s.

**Erosão local.** Com K = 0,0351, C = 0,212 e LS = 4,869, o índice de erosão do pixel é E_unit = 11,8 * (13,00 * 5,17 * 10^-4 * 897,49)^0,56 * 0,0351 * 0,212 * 4,869 = 1,167. Multiplicado pelo coeficiente do MC (c = 0,0344), dá 0,0401 t, ou 40,1 kg de sedimento produzido no pixel no evento.

**Sedimento do evento.** A soma de E_unit nos 153.855 pixels de cálculo é 40.885, e o MC estima SY = 0,0344 * 40.885 = 1.406 t no ajuste. Na validação cruzada, com c refeito sem o evento 11, a estimativa é 1.383 t. A carga medida é 1.822 t: o MC subestima o evento em 24% na validação cruzada, coerente com o escoamento calculado ser 67% do medido. No MFM, o escoamento de todos os pixels é multiplicado por f = 1.479 / 997 = 1,48; a soma dos índices passa a 63.451 (1,55 vez a do MC, que é 1,48^1,12, como esperado pela proporcionalidade de E_unit a Q^1,12), e, com c = 0,0222, o MFM estima 1.410 t no ajuste e 1.387 t na validação cruzada, também 24% abaixo do medido.

Tabela A1. Resultados do evento 11 e do pixel de exemplo.

| Grandeza | Valor |
|---|---|
| Lâmina R; intensidade RI; RI/R | 74,0 mm; 11,8 mm/h; 0,159 por hora |
| Chuva nos pixels: média (mínimo a máximo) | 73,5 mm (63,2 a 79,0 mm) |
| Pixel: chuva P | 75,4 mm |
| Pixel: CN-II; CN-I | 81,0; 64,2 |
| Pixel: S0,20; S0,05 | 141,9 mm; 244,2 mm |
| Pixel: abstração inicial; escoamento Q | 12,2 mm; 13,00 mm |
| Pixel: pico local pr | 5,17 * 10^-4 m³/s |
| Pixel: K; C; LS | 0,0351; 0,212; 4,869 |
| Pixel: E_unit; sedimento c * E_unit (MC) | 1,167; 40,1 kg |
| Bacia: escoamento médio; volume SCS-CN; volume medido | 7,2 mm; 997 mil m³; 1.479 mil m³ |
| MC: Σ E_unit; SY no ajuste; SY na validação cruzada | 40.885; 1.406 t; 1.383 t (-24%) |
| MFM: Σ E_unit; SY no ajuste; SY na validação cruzada | 63.451; 1.410 t; 1.387 t (-24%) |
| Carga medida SYobs | 1.822 t |

Fonte: elaborado pelo autor.

[IMAGEM] Figura A1 (página inteira)

Figura A1. Evento 11: chuva interpolada, retenção S0,05 e escoamento direto calculado pelo SCS-CN.

Fonte: elaborado pelo autor.

[IMAGEM] Figura A2 (página inteira)

Figura A2. Evento 11: índice de erosão E_unit e sedimento produzido em cada pixel (MC).

Fonte: elaborado pelo autor.

> Notas: (1) C20: imagens maiores. A figura atual (`TCC_Texto/figuras/mapas/mapa_08_evento11.png`) tem os cinco painéis juntos; proponho dividir em duas figuras de página inteira (A1 com 3 painéis; A2 com 2). Isso exige regerar no PC com `gerar_mapas_tcc.py` (precisa dos rasters). Se não der, usar a imagem atual em página inteira, com orientação paisagem, como "Figura A1" única. (2) Números conferidos: copiados de `tab_evento11_passo_a_passo.md` (conferida em 29/10 contra o CSV); contas refeitas à mão nesta sessão: CN-I = 340,2 / 5,302 = 64,2; S0,20 = 25,4 * 5,576 = 141,6 mm (a tabela dá 141,9, diferença de arredondamento do CN-I: com CN-I 64,16 dá 141,9); 13,00 * 0,89749 = 11,67 m³; 11,67 * 0,159 / 3600 = 5,15 * 10^-4 (a tabela dá 5,17 com RI/R não arredondado, 11,8/74,0 = 0,1595); 0,0344 * 1,167 = 0,0401 t; 1.383 / 1.822 - 1 = -24%. (3) "Maior a oeste, perto de Campo Limpo": Campo Limpo (79,0 mm) é o posto oeste (E 319.862) e o máximo do raster é 79,0 mm. (4) "Sedimento produzido no pixel" no lugar de "sedimento das encostas" (o rótulo dentro do `mapa_08` ainda diz "Sedimento das encostas": regerar).

---

## Referências citadas neste capítulo e nível de leitura

| Referência | Nível de leitura (fonte do registro) | Onde |
|---|---|---|
| ANA (2024) | ficha de metadados, planilha e Nota Técnica 9/2025 (lote C) | 3.3, 3.4.1.3, Tabela 9 |
| Chow, Maidment e Mays (1988) | livro não acessado; fórmula conferida em fonte secundária e na tabela do NEH-630 (lote B) | 3.4.1.3, Tabela 9 |
| Hao et al. (2022) | texto completo (lote A) | 3.4.3, 3.4.4, 3.4.5, 3.4.6 |
| Moore e Burch (1986) | só resumo (lote B) | 3.4.1.2 |
| Nash e Sutcliffe (1970) | não acessado; definição por fonte secundária (lote B) | 3.4.7 |
| Varma e Simon (2006) ou Cawley e Talbot (2010) | **não acessível nesta sessão (rede bloqueada); não citado**, marcador no texto | 3.4.6 |
| Vivarelli et al. (2025) | texto completo do artigo e do relatório PIBIC (lote C); valores da planilha do Drive (29/10) | 3.4.1.2, 3.4.8, Tabela 10 |
| Williams (1975) | original não acessado; AH 537 e fontes secundárias (lote B) | 3.4.3, Tabela 9 |
| Woodward et al. (2003) | texto completo do manuscrito; Eq. 8 conferida (lote A) | 3.4.1.3, Tabela 9 |

As obras com nível "não acessado" ou "só resumo" já estão citadas no Doc atual; a decisão sobre "apud" ou troca de fonte está no roteiro K.
