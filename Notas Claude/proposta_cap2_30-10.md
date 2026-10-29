# Proposta do capítulo 2: FUNDAMENTAÇÃO TEÓRICA, versão enxuta (30/10/2026)

Sessão na nuvem, sem acesso ao usuário nem ao Doc. **Nada foi aplicado no Doc.** Pedido do Luis: o capítulo 2 só expõe como as coisas funcionam e quais os problemas, sem dizer o que o trabalho faz (C9, C11, C12, C15, C16); a medição de sedimentos vira item separado com teoria de medição e artigos de dados de alta resolução (C10); "otimista" vira termo técnico (C14); as equações das métricas vão para o capítulo 3 (C13).

**Limitação desta sessão (importante):** a rede bloqueou todos os sites de periódicos, e nenhuma obra nova pôde ser lida (`leitura_referencias/loteE_medicao_e_validacao.md`). Pela regra do usuário, **não citei nenhuma obra nova**. Onde o Luis pediu "mais artigos além do meu" (2.5) e uma referência para a validação aninhada (2.8), deixei marcadores `[REFERÊNCIA A LER: ...]` com as candidatas. O texto foi escrito para funcionar sem elas; quando forem lidas, basta inserir a chamada.

Convenções: as do arquivo `proposta_cap3_30-10.md`. Seções 2.1 e 2.2 quase sem mudança; as 2.3 a 2.8 vêm com o texto final.

---

# 2. FUNDAMENTAÇÃO TEÓRICA

## 2.1 Erosão hídrica em escala de evento

Sem mudança (texto atual do Doc).

## 2.2 USLE e MUSLE

Texto atual do Doc, com uma troca no último parágrafo (item 4.1 de `ajustes_cap1_a_3_30-10.md`: "ajustou o coeficiente e o expoente por regressão aos dados de 17 eventos").

> Nota: o parágrafo da IC fica no capítulo 2 porque descreve um trabalho anterior (literatura), e não o que este trabalho faz; o uso da IC como comparação está na 3.4.8. Se o Luis preferir, o parágrafo inteiro vai para a 3.4.8.

## 2.3 Método SCS-CN

(Parágrafos 1 a 5 do Doc atual mantidos, inclusive as equações; saem a frase "Na bacia estudada, o CN em AMC II varia..." e o parágrafo "Neste trabalho adotou-se λ = 0,05...". Texto final:)

O método do número de curva do Serviço de Conservação do Solo dos Estados Unidos (SCS-CN) é a abordagem empírica mais usada para estimar o escoamento direto de um evento a partir da chuva (UNITED STATES, 1972; CHOW; MAIDMENT; MAYS, 1988). O escoamento Q (mm) depende da chuva P (mm), da retenção potencial máxima S (mm) e da abstração inicial, tomada como fração λ de S:

[EQUAÇÃO] (as três equações atuais do Doc)

O número de curva CN (0 a 100, com valores tabelados na prática entre 30 e 98) depende do grupo hidrológico do solo, do uso e ocupação, da condição hidrológica e das práticas de manejo, sendo tabelado para a condição de umidade antecedente média (AMC II). Os valores correspondentes às condições seca (AMC I) e úmida (AMC III) são obtidos por conversões empíricas (CHOW; MAIDMENT; MAYS, 1988):

[EQUAÇÃO] (atual)

O valor padrão da razão de abstração inicial é λ = 0,20, mas há discussão sobre ele. (parágrafo atual de Woodward, Brandão e Valle Junior, sem mudança)

Como o CN tabelado vale para λ = 0,20, usar λ = 0,05 exige converter a retenção S. Woodward et al. (2003) propuseram, com os mesmos dados, uma relação de potência entre as retenções obtidas com λ = 0,05 e com λ = 0,20:

[EQUAÇÃO] (atual, em polegadas)

em que S0,05 e S0,20 são as retenções potenciais máximas, em polegadas, para λ = 0,05 e λ = 0,20, respectivamente. Com S em milímetros, a mesma relação se escreve:

[EQUAÇÃO] (atual, em mm)

A relação é uma regressão entre valores de S ajustados a bacias norte-americanas, com chuvas de pelo menos 25,4 mm, e a tabela dos autores cobre números de curva de 35 a 100; fora dessas faixas, o seu uso é extrapolação.

Mesmo bem calibrado, o SCS-CN tem baixa capacidade de previsão do volume de eventos individuais. (parágrafo atual de Baert e Valle Junior, sem mudança)

> Notas: (1) C9 e C16 resolvidos. (2) O parágrafo de Baert termina com "um valor único mais baixo de λ não resolve" e o de Valle Junior com "Q = C*P teve melhor desempenho": os dois são "quais são os problemas", que o Luis quer no capítulo 2. (3) USDA-SCS (1972) e Chow (1988) não lidos no original (lote B); já estão no Doc assim; decisão de "apud" no roteiro K.

## 2.4 Escoamento direto e vazão de base

O hidrograma medido no exutório é a soma do escoamento direto, gerado pela chuva do evento, e da vazão de base, água subterrânea que já alimentava o rio. O SCS-CN calcula somente o escoamento direto. A separação entre as duas componentes não é observável e depende do método adotado; entre os mais usados estão os filtros digitais recursivos de Lyne e Hollick (1979) e de Eckhardt (2005). O filtro de Eckhardt tem dois parâmetros: a constante de recessão (a), que pode ser estimada da curva de recessão, e o índice máximo de vazão de base (BFImax), a fração máxima da vazão total que a vazão de base pode representar a longo prazo. O BFImax não é mensurável e é escolhido pelo usuário; Eckhardt (2005) sugeriu valores de ordem de grandeza conforme o regime do rio e o tipo de aquífero, 0,80 para rios perenes com aquífero poroso, 0,50 para rios efêmeros com aquífero poroso e 0,25 para rios perenes com aquífero em rocha dura (ECKHARDT, 2012). Como o parâmetro é escolhido, a vazão de base obtida por filtro é uma estimativa, e o escoamento direto obtido pela diferença entre a vazão total e a de base herda essa incerteza.

> Notas: (1) C10: sai o título "... e medição de sedimentos em suspensão" e o 2º parágrafo (vai para a 2.5). (2) O que é do trabalho (série fornecida, a = 0,995, BFImax 0,70) vai para a 3.2. (3) **Valores-guia de BFImax:** lote A (Eckhardt 2012, HESS 16, texto completo, que confirma por escrito 0,80 e 0,50 como sugestões de 2005 e usa 0,25 no exemplo; Eckhardt 2005 só resumo). Por isso a chamada é "(ECKHARDT, 2012)". **Eckhardt (2012) não está na lista de referências do TCC: acrescentar.** Referência a conferir no PDF: ECKHARDT, K. Technical Note: Analytical sensitivity analysis of a two parameter recursive digital baseflow separation filter. Hydrology and Earth System Sciences, v. 16, n. 2, p. 451-455, 2012. DOI: https://doi.org/10.5194/hess-16-451-2012 (título e DOI de memória/registro do lote A; **conferir antes de colar**). (4) Este parágrafo prepara uma discussão importante da 4.6: a bacia é de embasamento cristalino com aquífero fraturado (3.1), para o qual o valor-guia é 0,25, e a série usada corresponde a BFImax 0,70.

## 2.5 Medição de sedimentos em suspensão

A carga de sedimentos em suspensão transportada por um rio em um evento é a integral, no tempo, do produto da vazão pela concentração de sedimentos em suspensão (CSS). A vazão pode ser registrada continuamente por estações fluviométricas, mas a CSS só é medida diretamente em amostras de água coletadas na seção, com amostradores manuais integradores na vertical ou com amostradores automáticos, e determinada em laboratório por filtração ou evaporação. Como as amostras são caras e esparsas, e os eventos de chuva são curtos e difíceis de acompanhar em campo, a carga dos eventos, em que se concentra a maior parte do transporte de sedimentos (seção 2.1), é a mais difícil de medir.

Uma alternativa é usar uma grandeza medida de forma contínua e correlacionada com a CSS, como a turbidez, que mede a atenuação ou o espalhamento da luz pelas partículas em suspensão. Ajustada uma curva de calibração local entre a turbidez e a CSS das amostras, a série contínua de turbidez é convertida em série de CSS (MURILLO-BERMÚDEZ et al., 2023). A CSS assim obtida é uma estimativa, e não uma medida direta: a relação entre turbidez e concentração depende do tamanho, da forma e da cor das partículas, que mudam entre eventos e ao longo de um mesmo evento, e a curva só é confiável na faixa de turbidez coberta pelas amostras usadas no ajuste. Na bacia do alto Jundiaí, Murillo-Bermúdez et al. (2023) compararam diferentes regressões entre turbidez e CSS e obtiveram o melhor ajuste com uma regressão linear por partes, com mudança de comportamento em 250 NTU; nas turbidezes mais altas, que ocorrem nos picos dos eventos, a curva tem a maior incerteza, justamente quando a carga é maior. [REFERÊNCIA A LER: Rasmussen et al. (2009), USGS TM 3-C4, sobre o uso de turbidez como substituto da CSS e a revisão periódica da curva; Gray e Gartner (2009), WRR, sobre tecnologias substitutas.]

Séries de alta resolução temporal, como as de turbidez horária ou subhorária, permitem acompanhar a variação da concentração dentro de cada evento. Em muitos eventos, a concentração não acompanha a vazão de forma unívoca: para a mesma vazão, a concentração é diferente na subida e na descida do hidrograma, o que forma um laço de histerese no gráfico de concentração contra vazão. O sentido do laço indica, de modo qualitativo, se o sedimento vem de fontes próximas e rapidamente esgotadas ou de fontes distantes que chegam depois do pico. No alto Jundiaí, Murillo-Bermúdez e Martim (2022) analisaram 17 eventos com vazão de pelo menos 10 m³/s, com a vazão registrada a cada 10 minutos pela rede telemétrica do DAEE e a turbidez medida de hora em hora na estação de tratamento de água da SABESP, e encontraram laços em forma de oito em 13 eventos e laços no sentido horário em 4. A existência de histerese mostra que a carga de um evento não pode ser estimada só pela vazão por uma relação fixa, e que a concentração média de cada evento varia com a disponibilidade de sedimento na bacia. [REFERÊNCIA A LER: Williams (1989), J. Hydrology, classificação dos laços de histerese; Minella et al. (2008), Hydrological Processes, turbidez em bacia rural brasileira.]

> Notas: (1) C10. (2) Leitura: Murillo-Bermúdez e Martim (2022) texto completo (lote C): vazão do DAEE/SAISP a cada 10 min, turbidez horária da ETA da SABESP, eventos com Q >= 10 m³/s, 17 eventos, 13 em oito e 4 horários, DH-48 e ISCO, filtração. Murillo-Bermúdez et al. (2023) **só resumo** (lote C): turbidez da ETA, amostradores, granulometria, um ano hidrológico, regressões comparadas por R², MSPE, PRESS, melhor a linear por partes com quebra em 250 NTU. (3) As frases gerais do 1º parágrafo e do início do 2º (integral Q * CSS; amostradores integradores; filtração e evaporação; turbidez depende de tamanho, forma e cor das partículas) são conhecimento corrente de hidrossedimentologia, mas **não as li em obra desta lista**; por isso não levam citação. Quando o lote E for lido, apoiar essas frases em Rasmussen et al. (2009) ou Gray e Gartner (2009). Se o usuário não quiser frase sem citação, cortar "que mede a atenuação ... em suspensão" e "depende do tamanho ... evento". (4) "O sentido do laço indica ... fontes próximas ou distantes": interpretação clássica (Williams, 1989), **não lida**; se o lote E não for lido, cortar essa frase. (5) Ficou de fora: a frase "Neste trabalho, a carga total medida é atribuída ao escoamento superficial..." (vai para 3.4.4).

## 2.6 MUSLE espacializada

Hao et al. (2022) propuseram aplicar a MUSLE por pixel, em escala de evento. A vazão de pico local de cada pixel é calculada a partir do escoamento do próprio pixel, ponderado pela concentração temporal da chuva (razão entre a intensidade máxima e a lâmina do evento), sem roteamento; a erosão local resulta da fórmula de Williams, com o escoamento do pixel dado pelo SCS-CN. Para chegar ao sedimento no exutório, os autores multiplicam a erosão de cada pixel por um grau de conectividade de sedimentos, entre 0 e 1, calibrado em cada bacia. Em três bacias chinesas de 1.310 a 8.973 km², com 58 eventos e vários pluviômetros por bacia, o modelo atingiu NSE de 0,70 a 0,83 no ajuste.

Aplicada ao pixel, a fórmula de Williams deixa de ter o significado de produção de sedimentos da bacia: ela foi ajustada com o volume e o pico de bacias inteiras, e o valor calculado em uma célula é uma medida da erosão local, que só chega ao exutório em parte. Sem um fator que represente a entrega ou a conectividade, a soma da erosão dos pixels não corresponde ao sedimento medido no exutório.

> Notas: (1) 1º parágrafo = atual (2.5 do Doc), sem mudança. (2) 2º parágrafo novo, só teoria, para substituir o parágrafo "Neste trabalho..." (C11), que vai para 3.4.4. Não leva citação nova: decorre da 2.2 (Williams ajustada em bacia; Neitsch: dispensa a razão de entrega na escala da bacia) e do 1º parágrafo (Hao: conectividade). Se o Luis achar redundante, cortar.

## 2.7 Dados espaciais e interpolação da chuva

Em modelos distribuídos, os fatores da MUSLE e do SCS-CN são representados em formato raster, uma grade regular em que cada célula (pixel) tem um valor. Os fatores K e C costumam ser atribuídos por classe, a partir de mapas temáticos de solo e de uso e cobertura, com valores de erodibilidade e de cobertura obtidos em ensaios ou na literatura; a qualidade do resultado depende, assim, da escala dos mapas e da representatividade dos valores adotados para cada classe. O fator topográfico LS é derivado de um modelo digital de elevação; formulações baseadas na potência do escoamento, como a de Moore e Burch (1986), substituem o comprimento da encosta pela área de contribuição a montante por unidade de largura (área de contribuição específica), o que permite calculá-lo célula a célula em terrenos complexos. O número de curva pode ser obtido do cruzamento de mapas de uso e cobertura com mapas de solos classificados em grupos hidrológicos; para solos brasileiros, Sartori, Lombardi Neto e Genovez (2005) propuseram uma classificação hidrológica adaptada.

A chuva é medida em pontos (postos pluviométricos) e precisa ser interpolada para a grade. No método do inverso da distância (IDW), a chuva de cada célula é a média das chuvas dos postos ponderada pelo inverso da distância elevada a uma potência, em geral 2; o método é simples e reproduz exatamente o valor medido em cada posto, mas não representa a variação da chuva entre os postos, e, com poucos postos, o resultado é um gradiente suave entre eles. A densidade de postos limita, portanto, a representação da variabilidade espacial da chuva, sobretudo em chuvas convectivas, que são intensas e localizadas. [REFERÊNCIA A LER: Faurès et al. (1995), J. Hydrology, efeito da densidade de pluviômetros no escoamento de uma bacia pequena.]

> Notas: (1) C12: sai tudo o que é escolha do trabalho (Moore e Burch aplicado ao MDE em UTM, limite de 200 m, ANA 2024, CN-I, escala 1:250.000), que vai para 3.3 e 3.4.1. (2) Leitura: Moore e Burch (1986) só resumo (lote B; o resumo trata da base física do LS pela potência do escoamento, o que sustenta a frase); Sartori, Lombardi Neto e Genovez (2005) texto completo (lote C). (3) Frases sobre IDW: definição matemática padrão, sem citação; a frase "a densidade de postos limita..." não tem obra lida; manter sem citação ou cortar se o lote E não for lido. (4) Título novo: "Dados espaciais e interpolação da chuva" (era "Dados espaciais em SIG").

## 2.8 Avaliação e validação de modelos

A eficiência de Nash-Sutcliffe (NSE; NASH; SUTCLIFFE, 1970) compara o erro quadrático do modelo com a variância dos dados: vale 1 para um ajuste perfeito, 0 quando o modelo é tão bom quanto prever sempre a média, e é negativa quando é pior. Por usar o quadrado do erro, o NSE é dominado pelos eventos de maior magnitude. Quando poucos eventos são muito maiores que os demais, o NSE pode refletir o acerto de um único evento.

Duas medidas ajudam a reduzir essa sensibilidade: o NSE calculado sobre os logaritmos, que dá peso ao erro relativo, mas passa a ser dominado pelos menores eventos; e métricas baseadas em erro percentual, como a mediana do erro percentual absoluto e a fração de eventos com o simulado entre 0,5 e 2 vezes o medido (critério de fator 2). A correlação de ordem de Spearman avalia se o modelo ordena os eventos corretamente, sem depender da magnitude. Hao et al. (2022) também usaram um NSE em escala logarítmica como função objetivo na calibração do modelo espacializado.

Quando os parâmetros de um modelo são ajustados aos mesmos dados usados para avaliá-lo, o desempenho calculado é uma estimativa enviesada para cima do desempenho que o modelo teria em dados novos; essa diferença é chamada de viés de otimismo, e cresce com o número de parâmetros e de escolhas ajustadas e diminui com o número de dados. A validação cruzada reduz esse viés separando os dados de ajuste dos dados de teste: na forma leave-one-out, cada observação é prevista por um modelo ajustado sem ela, e o desempenho é calculado sobre essas previsões; Hao et al. (2022) usaram esse procedimento na MUSLE espacializada. A validação cruzada simples corrige apenas o viés dos parâmetros refeitos em cada rodada. Escolhas feitas antes, observando todos os dados, como a de uma formulação ou de um valor fixo de parâmetro, continuam a produzir viés de otimismo; para eliminá-lo, essas escolhas também precisam ser repetidas dentro de cada rodada, com os dados de ajuste daquela rodada, o que se chama validação cruzada aninhada. [REFERÊNCIA A LER: Varma e Simon (2006), BMC Bioinformatics 7:91; Cawley e Talbot (2010), JMLR 11.] Baert et al. (2026), por exemplo, avaliaram as previsões de volume e de sedimento fora da amostra, por validação cruzada repetida, e obtiveram desempenho muito inferior ao do ajuste com os mesmos dados.

> Notas: (1) C13 (equações vão para 3.4.7), C14 ("otimista" -> "estimativa enviesada para cima ... viés de otimismo", com definição), C15 (a parte aplicada ao trabalho foi para 3.4.6), C19 (validação aninhada definida; referência pendente por falta de rede). (2) 1º e 2º parágrafos = Doc atual, sem mudança. (3) "cresce com o número de parâmetros e diminui com o número de dados": afirmação geral de estatística, sem obra lida; se o usuário preferir, cortar essa oração. (4) Baert: lote A (validação cruzada 5 vezes, repetida 10; volume NSE 0,94 no diagnóstico contra 0,21 a 0,40 fora da amostra; sedimento 0,46 a 0,48 contra -0,03 e 0,01). A frase "desempenho muito inferior ao do ajuste" resume isso sem números; se quiser números, usar os do volume (0,94 contra 0,21 a 0,40). (5) Nash e Sutcliffe (1970): não lido no original; já citado assim no Doc.

---

## Referências deste capítulo e nível de leitura

| Referência | Nível (fonte do registro) | Seção | Na lista do TCC? |
|---|---|---|---|
| Baert et al. (2026) | texto completo, sem suplementos (lote A) | 2.3, 2.8 | sim |
| Brandão et al. (2025) | texto completo (lote A) | 2.3 | sim |
| Chow, Maidment e Mays (1988) | não acessado (lote B) | 2.3 | sim |
| Eckhardt (2005) | só resumo (lote A) | 2.4 | sim |
| **Eckhardt (2012)** | texto completo (lote A) | 2.4 | **não: acrescentar** |
| Hao et al. (2022) | texto completo (lote A) | 2.6, 2.8 | sim |
| Lyne e Hollick (1979) | original não acessado; só fontes secundárias (lote B) | 2.4 | sim |
| Moore e Burch (1986) | só resumo (lote B) | 2.7 | sim |
| Murillo-Bermúdez e Martim (2022) | texto completo (lote C) | 2.5 | sim |
| Murillo-Bermúdez et al. (2023) | só resumo (lote C) | 2.5 | sim |
| Nash e Sutcliffe (1970) | não acessado (lote B) | 2.8 | sim |
| Sartori, Lombardi Neto e Genovez (2005) | texto completo (lote C) | 2.7 | sim |
| United States (1972), NEH-4 | não acessado (lote B) | 2.3 | sim |
| Valle Junior, Rodrigues e Oliveira (2019) | texto completo (lote A) | 2.3 | sim |
| Woodward et al. (2003) | texto completo do manuscrito (lote A) | 2.3 | sim |
| Varma e Simon (2006); Cawley e Talbot (2010); Rasmussen et al. (2009); Gray e Gartner (2009); Williams (1989); Minella et al. (2008); Faurès et al. (1995) | **não acessíveis nesta sessão (rede bloqueada); não citados**; marcadores no texto | 2.5, 2.7, 2.8 | não |
