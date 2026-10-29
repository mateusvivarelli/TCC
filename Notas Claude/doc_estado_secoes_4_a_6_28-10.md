# Estado do Google Doc, seções 4 a 6 (cópia de 29/10/2026 00:30, ANTES de reescrever)

Texto do Doc "TCC arquivo" nas seções 4 (Metodologia), 5 (Resultados e Discussão) e 6 (Conclusões). **Está no modelo antigo (dois componentes, λ = 0,20)**; serve só para ver a estrutura, os títulos, a numeração e o que existe de tabelas e figuras. Equações aparecem como `[EQUAÇÃO]` (o Docs as guarda como objeto). Corpo das tabelas omitido (só cabeçalho e dimensões).


# 4. METODOLOGIA

## 4.1 Visão geral
O trabalho estima, para cada um dos 17 eventos, quanta erosão cada pixel da bacia produz e quanto sedimento chega ao exutório, e compara o resultado com o sedimento medido. A Figura 4 resume o fluxo. Para cada evento:
a chuva medida nos dois postos é interpolada para todos os pixels (seção 4.2.4);
o método SCS-CN converte a chuva de cada pixel em escoamento direto, segundo o número de curva do pixel (seção 4.3);
a vazão de pico local do pixel e a erosão local são calculadas pela fórmula de Williams, aplicada pixel a pixel (seção 4.4);
a erosão dos pixels é somada, e o sedimento do evento é escrito como a soma de dois termos: o das encostas (soma dos pixels) e o da vazão de base (da bacia) (seção 4.5);
os dois parâmetros de escala do modelo são calibrados contra o sedimento medido no exutório, em escala logarítmica (seção 4.6);
o desempenho é avaliado por validação cruzada leave-one-out aninhada, com métricas pouco sensíveis ao evento dominante (seções 4.7 e 4.8);

> [IMAGEM]

Figura 4. Fluxograma do método.
O modelo foi aplicado de duas formas, que diferem apenas na origem da água de cada evento: o Modelo Calculado (MC), em que o escoamento vem da chuva pelo SCS-CN (uma previsão), e o Modelo Forçado ao Medido (MFM), em que o volume de escoamento direto e a vazão de base são os medidos (uma referência que indica o desempenho possível com uma boa estimativa da água).

## 4.2 Preparação dos dados

### 4.2.1 Variáveis de cada evento e pixels de cálculo
Todos os dados espaciais foram colocados na mesma grade, a do raster de chuva (884 * 365 pixels, SIRGAS 2000 / UTM 23S, pixel de 29,992 * 29,925 m = 897,49 m²). O raster de número de curva, que tinha outra grade (973 * 362), foi reamostrado pelo vizinho mais próximo, isto é, cada pixel da grade de cálculo recebe o valor do pixel do raster original que contém o seu centro. O cálculo da erosão só é feito nos pixels em que existem, ao mesmo tempo, número de curva, K, C e LS (153.855 pixels, 138,1 km²); os demais ficam sem valor. As variáveis usadas em cada evento estão na Tabela 7.
Tabela 7. Variáveis usadas em cada evento.

> [TABELA] cabeçalho: Símbolo | Significado | Unidade


### 4.2.2 Fatores K, C, LS e P
Os fatores K e C foram atribuídos por classe (Tabela 5): cada pixel recebe o valor da classe de solo ou de uso do polígono que contém o seu centro. Essa regra reproduz exatamente os rasters de K e de C usados no trabalho (verificado pixel a pixel). O fator LS vem do modelo digital de elevação, pela formulação de Moore e Burch (1986). O fator P é igual a 1,0 em toda a bacia, porque não há práticas conservacionistas ativas.

### 4.2.3 Número de curva e retenção S
O número de curva CN (de 0 a 100) mede quanto um pixel tende a gerar escoamento: valores altos, como os de áreas urbanizadas, indicam pouca infiltração; valores baixos, como os de mata, indicam muita infiltração. O CN foi obtido do cruzamento do uso com o solo, para a condição de umidade média (AMC II), e convertido para a condição seca (AMC I) por

> [EQUAÇÃO]

(CHOW; MAIDMENT; MAYS, 1988; o resultado reproduz o raster usado em menos de 10^-5). O CN médio passa de 71,6 (AMC II) para 52,5 (AMC I). A retenção potencial máxima S (mm), que é a quantidade de chuva que o solo pode absorver antes de gerar escoamento, é

> [EQUAÇÃO]

e vale 255,7 mm em média na bacia (de 12 a 558 mm entre os pixels).

### 4.2.4 Chuva espacializada
Os dois postos medem a chuva em pontos. Para estimar a chuva em cada pixel, usa-se o inverso do quadrado da distância (IDW, potência 2): quanto mais perto de um posto, maior o peso dele.

> [EQUAÇÃO]

em que d1 e d2 são as distâncias (m) do centro do pixel aos postos, em coordenadas UTM; os postos foram projetados de latitude e longitude (EPSG:4326) para SIRGAS 2000 / UTM 23S: DBT5 em E 348.520,8 m e N 7.426.415,3 m, e Campo Limpo em E 319.862,4 m e N 7.432.277,5 m. Com apenas dois postos, um deles fora da bacia, o resultado é um gradiente suave entre os pontos, que muda de evento para evento conforme a chuva medida em cada posto. Esse cálculo reproduz o raster de chuva do QGIS com diferença menor que 10^-5 mm.

## 4.3 Escoamento direto por pixel (SCS-CN)
Para cada pixel, o escoamento direto Q (mm) depende da chuva P e da retenção S do pixel:

> [EQUAÇÃO]


> [EQUAÇÃO]

O termo λS é a abstração inicial, a chuva que o solo absorve antes de qualquer escoamento. Adotou-se λ = 0,20 (valor padrão do método), compatível com o uso do CN tabelado (seção 2.3). O escoamento calculado é só o direto: não inclui a vazão de base. A condição de umidade seca (AMC I) foi herdada da fase em que o modelo foi calibrado contra o volume total. Pixels em que a chuva é menor que λS não geram escoamento; no evento 11, por exemplo, isso acontece em 10% dos pixels.

## 4.4 Vazão de pico local e erosão local
A fórmula de Williams (seção 2.2) usa o volume e a vazão de pico do escoamento. Seguindo Hao et al. (2022), cada pixel tem a sua própria vazão de pico, calculada sem roteamento hidráulico: o escoamento do pixel, em volume por segundo, é ponderado pela concentração temporal da chuva do evento, isto é, pela razão entre a intensidade máxima (RI) e a lâmina total (R):

> [EQUAÇÃO]

Em palavras: Qk/1000 é a lâmina em metros, multiplicada pela área do pixel Apix (897,49 m²) dá o volume escoado no pixel (m³); a razão RI/R (por hora) indica a fração da chuva que cai na hora mais intensa; a divisão por 3.600 converte horas em segundos. Eventos em que a chuva se concentra em poucas horas (RI/R alto) têm picos locais maiores. Essa razão é um número único por evento; a variação de pr entre pixels vem só de Qk.
A erosão local é a fórmula de Williams aplicada ao pixel, com os coeficientes originais:

> [EQUAÇÃO]

com Q em mm, pr em m³/s e Apix em m², como em Hao et al. (2022). Como pr é proporcional a Q, Eunit é proporcional a Q1,12. Eunit é um índice relativo de erosão, não uma massa em toneladas: os coeficientes de Williams foram ajustados em escala de bacia, e o produto Q * pr * A em um pixel de 897 m² está fora da faixa para a qual eles foram ajustados. O fator c1 da seção seguinte converte esse índice em toneladas.

## 4.5 Sedimento do evento: modelo de dois componentes
O sedimento medido no exutório inclui o transportado pela vazão de base, que o SCS-CN não representa (seção 3.2). Por isso, o sedimento de cada evento foi escrito como a soma de dois termos:

> [EQUAÇÃO]

O primeiro termo é a erosão das encostas: a soma de Eunit sobre todos os pixels de cálculo, com Q igual ao escoamento direto, multiplicada por c1. O segundo termo representa a contribuição da vazão de base: o volume de referência Qbinicio * Tchuva * 3600 (m³), que é a vazão que o rio já tinha no início do evento, mantida durante o tempo de chuva, multiplicado por c2. A base é um termo único da bacia, não é distribuída pelos pixels. A duração usada é a da chuva e não a do hidrograma, porque a duração do hidrograma só é conhecida depois que ele passa e acompanha o volume observado, o que antecipava o resultado. Os parâmetros c1 e c2 (não negativos) convertem cada termo em toneladas; c1 absorve também a diferença de escala entre o coeficiente de Williams e o pixel e não deve ser lido como razão de entrega de sedimentos. O mapa de áreas críticas mostra somente a parcela das encostas (c1 * Eunit,k).
As duas versões do modelo diferem na origem da água (Tabela 8):
Modelo Calculado (MC): Q vem do SCS-CN e a base é o volume de referência acima. Só usa a chuva dos postos, a vazão inicial e a duração da chuva.
Modelo Forçado ao Medido (MFM): o volume de escoamento direto é forçado ao valor medido, Vdir. O SCS-CN apenas distribui esse volume no espaço: todos os pixels são multiplicados pelo mesmo fator f = Vdir / VSCS, em que VSCS é o volume que o SCS-CN calcularia, e o escoamento do pixel é limitado à chuva do pixel, Q = min(f * QSCS, P), porque o escoamento não pode superar a chuva (esse limite atua em poucos pixels). O termo de base usa a vazão de base medida, Vbase = Σ Bt * 3600, em lugar do volume de referência. Não é previsão: mostra o desempenho que o modelo atingiria se a água fosse bem estimada.
Tabela 8. Origem da água em cada versão do modelo de dois componentes.

> [TABELA] cabeçalho: Versão | Escoamento direto (termo 1) | Vazão de base (termo 2)


## 4.6 Calibração dos parâmetros
Os parâmetros c1 e c2 foram ajustados aos 17 sedimentos medidos minimizando o erro em escala logarítmica:

> [EQUAÇÃO]

em que Vref,n é o volume de referência do termo de base. Esse critério pesa os eventos pelo erro relativo e evita que um único evento muito grande (o evento 15 responde por 48,7% da variância linear da carga medida e por 49% do peso na calibração por mínimos quadrados lineares) comande o ajuste. O problema foi resolvido por mínimos quadrados não lineares com limites (algoritmo de região de confiança), a partir de três pontos de partida, e a melhor solução foi mantida. A Tabela 9 reúne os parâmetros fixos e calibrados.
Tabela 9. Parâmetros fixos e calibrados dos modelos.

> [TABELA] cabeçalho: Parâmetro | Valor | Origem


## 4.7 Validação cruzada aninhada
Parâmetros ajustados aos mesmos dados usados para avaliar o modelo levam a resultados otimistas. Para evitar isso, cada evento foi previsto com parâmetros ajustados sem ele: (i) retira-se um evento; (ii) ajustam-se c1 e c2 (e, nos modelos de comparação, os parâmetros de cada um) aos 16 eventos restantes; (iii) prevê-se o sedimento do evento retirado; (iv) repete-se para os 17 eventos. As métricas são calculadas sobre as 17 previsões. A validação é aninhada: qualquer etapa que dependa de ajuste é refeita dentro de cada rodada. Os resultados "no ajuste" (sem validação cruzada) são reportados à parte e só têm valor diagnóstico.

## 4.8 Métricas de desempenho
As métricas principais não dependem da variância dos dados e, portanto, não são dominadas por um único evento:
Erro percentual mediano (MedAPE): a mediana de |simulado - medido| / medido * 100 sobre os 17 eventos. A mediana evita que erros muito grandes em poucos eventos dominem. Não se usa a média do erro absoluto percentual, porque ela favorece a subestimativa.
Fração de eventos dentro de fator 2: o percentual de eventos em que o simulado está entre 0,5 e 2 vezes o medido.
Correlação de Spearman: correlação entre as posições (ordens) do simulado e do medido; indica se o modelo ordena os eventos corretamente, sem depender da magnitude.
NSE em escala logarítmica: é o NSE calculado sobre ln(SY) em vez de SY. O NSE compara o erro do modelo com a variação dos próprios dados: vale 1 quando o modelo acerta tudo, 0 quando erra tanto quanto errar prevendo sempre a média dos eventos, e é negativo quando erra mais que isso.

## 4.9 Exemplo numérico: o evento 11
Para acompanhar o cálculo, a Tabela 10 e a Figura 5 mostram o evento 11 (04 a 08/07/2019) do início ao fim, com um pixel de exemplo, escolhido entre os de lavoura temporária sobre Argissolo, com erosão alta (E 330,18 km; N 7.432,86 km).
Tabela 10. O evento 11 passo a passo, com um pixel exemplificado.

> [TABELA] cabeçalho: Grandeza | Valor


> [IMAGEM]

Figura 5. Etapas espaciais do modelo no evento 11: chuva interpolada, retenção S, escoamento direto, índice de erosão Eunit e sedimento das encostas.

# 5. RESULTADOS E DISCUSSÃO

## 5.1 O volume e a carga medidos incluem a vazão de base
Os resultados da seção 3.2 mostram que a comparação direta entre o escoamento calculado pelo SCS-CN e o volume medido é desigual: o modelo calcula apenas o escoamento direto, e o volume medido tem de 34% a 55% de vazão de base (Tabela 3). O resultado mais importante desta fase é, portanto, de definição: qualquer calibração do SCS-CN contra TR ajusta o modelo a uma grandeza que ele não representa.

## 5.2 Resultados do Modelo Calculado (MC)
O MC (só chuva e vazão inicial) obteve c1 = 0,0035 e c2 = 0,0131 t por m³ de volume de referência (Tabela 9). Na validação cruzada, o erro percentual mediano foi de 32,6%, e 71% dos eventos (12 de 17) ficaram dentro de fator 2; o NSE em escala logarítmica foi 0,48 e a correlação de Spearman, 0,72. No ajuste, o MC superestima os eventos 1, 9 e 16 (+105%, +178% e +171%) e subestima os eventos 4, 7, 11 e 12 (de -38% a -58%) (Tabela 11). A Figura 6 compara o sedimento simulado, na validação cruzada, com o medido em cada evento.
Tabela 11. Sedimento por evento (t): medido e simulado pelo MC, com a decomposição em encostas e vazão de base.

> [TABELA] cabeçalho: Evento | Medido | Encostas | Base | Total simulado | Erro no ajuste (%) | Erro na validação cruzada (%)


> [IMAGEM]

Figura 6. Sedimento simulado e medido nos 17 eventos, validação leave-one-out, para a referência simples (SY = c * chuva), o MC e a IC. A faixa clara indica fator 2.
Nas previsões do MC, a vazão de base carrega a maior parte do sedimento simulado. Em mediana, as encostas respondem por 9% do sedimento simulado (máximo de 35%) e o termo de base, por 91% (Figura 7). 

> [IMAGEM]

Figura 7. Composição do sedimento simulado pelo MC em cada evento (encostas e vazão de base) e sedimento medido.

## 5.3 O gargalo: transformar chuva em escoamento
Forçando a água ao valor medido, a fração de eventos dentro de fator 2 sobe de 71% para 94%, o erro mediano cai de 32,6% para 13,6% e a parcela das encostas no sedimento simulado passa de 9% para 38% (mediana). O que muda entre as duas versões é só a água; a fórmula de erosão, os fatores do solo, do uso e do relevo e o desenho em dois componentes são os mesmos. A qualidade do sedimento estimado depende, portanto, da qualidade da estimativa do escoamento, e a fórmula de erosão e o desenho em dois componentes não são o limite. O erro mediano de 14% exige, porém, que tanto a água das encostas quanto a vazão de base sejam as medidas.

## 5.4 O modelo de dois componentes e os testes simples
Com os mesmos insumos, o modelo de dois componentes e o teste simples são equivalentes. Na versão MC, o erro mediano do modelo (33%) é próximo ao do simples (38%) e a fração dentro de fator 2 é igual (71%); na versão MFM, o modelo é um pouco melhor (14% contra 20%), com 94% em ambos. A espacialização não perde precisão em relação a modelos simples com os mesmos insumos. 

## 5.5 Comparação com a IC
Tabela 12. Desempenho na validação cruzada (calibração em escala logarítmica; carga total de sedimentos).

> [TABELA] cabeçalho: Modelo | Informação medida usada | Erro mediano | Dentro de fator 2 | NSE em log | Spearman

Como mostra a Tabela 12, a formulação concentrada da IC, com volume e pico medidos do próprio hidrograma, tem desempenho muito bom (100% dos eventos dentro de fator 2 na validação cruzada), semelhante ao do MFM, que recebe informação equivalente. O MC, que só usa a chuva e a vazão inicial, é pior que a IC. A IC, no entanto, não prevê (precisa do hidrograma do evento, que gera também o sedimento medido), não gera mapa e seus coeficientes foram ajustados nos mesmos 17 eventos. Com informação equivalente, a espacialização iguala a qualidade da formulação concentrada e acrescenta o mapa.

## 5.6 Mapas

### 5.6.1 Da chuva ao sedimento, evento a evento
As Figuras 8 a 10 mostram, para os 17 eventos, a chuva interpolada, o escoamento direto calculado pelo SCS-CN e o sedimento das encostas do MC, com a mesma escala de cores em todos os eventos para permitir a comparação. Na chuva (Figura 8), o gradiente leste-oeste varia entre eventos conforme o que cada posto registrou: a chuva é maior a oeste (posto de Campo Limpo) em 13 dos 17 eventos e maior a leste (posto DBT5) nos eventos 1, 2, 4 e 17; no evento 12, o DBT5 não registrou chuva, e no 17 os dois postos medem valores próximos. 
O escoamento direto (Figura 9) acompanha a lâmina de chuva do evento: é quase nulo nos eventos menores (1, 4, 6, 7, 10 e 12) e alto no evento 15, o maior, em que quase toda a porção oeste e central da bacia gera escoamento; o extremo oeste, próximo ao exutório, tem sempre os maiores valores, onde o número de curva é mais alto (Figura 3). O sedimento das encostas (Figura 10) tem sempre os mesmos pontos de maior contribuição, que mudam de intensidade de um evento para outro, mas não de lugar, porque o padrão espacial é dominado pelos fatores fixos (K, C e LS), enquanto a chuva e o escoamento definem a intensidade geral do evento.

> [IMAGEM]

Figura 8. Chuva total de cada evento, interpolada por IDW a partir de dois postos.

> [IMAGEM]

Figura 9. Escoamento direto calculado pelo SCS-CN (CN seco, λ = 0,20) em cada evento.

> [IMAGEM]

Figura 10. Sedimento produzido nas encostas em cada evento (MC).

### 5.6.2 Sedimento médio e áreas críticas
A Figura 11 mostra o sedimento médio dos 17 eventos e as áreas críticas, definidas como os 5% de pixels de maior contribuição, para o MC e para o MFM. Os dois mapas são muito parecidos (correlação de 0,97; 90,9% das áreas críticas coincidem), o que indica que o padrão espacial não depende da forma de estimar a água. A correlação do mapa com o produto K * LS * C é de 0,69 (Spearman de 0,79), o que indica que o padrão espacial carrega também informação da chuva e do escoamento (CN), e não só dos fatores fixos.

> [IMAGEM]

Figura 11. Sedimento médio dos 17 eventos e áreas críticas (5% dos pixels de maior contribuição), para o MC e o MFM.
As áreas críticas se concentram em poucas manchas na porção central e oeste da bacia e em algumas manchas pequenas ao sul. A Tabela 13 mostra que a contribuição é muito desigual entre os usos do solo: a lavoura temporária ocupa 3,9% da área e responde por cerca de 23% do sedimento (21% no MFM); o solo exposto ocupa 0,5% e responde por 9% (13% no MFM); o campo ocupa 29,0% e responde por 39% (40%); a mata nativa ocupa 39,6% e responde por 6% (5%); as áreas urbanizadas, que têm erosão nula no modelo (C = 0), ocupam 14,1%. Em relação aos solos (Tabela 14), 94% do sedimento vem dos Cambissolos, que têm o maior K (0,0475) e ocupam 68,6% da área. Esses resultados dependem dos valores de K e C por classe adotados e não foram validados no espaço, porque só há medição de sedimento no exutório; devem ser lidos como contribuições relativas.
Tabela 13. Contribuição de cada classe de uso para o sedimento médio das encostas (MC e MFM).

> [TABELA] cabeçalho: Classe de uso | Área (%) | Sedimento, MC (%) | kg/pixel, MC | Sedimento, MFM (%) | kg/pixel, MFM

Tabela 14. Contribuição de cada classe de solo para o sedimento médio das encostas.

> [TABELA] cabeçalho: Classe de solo | Área (%) | Sedimento, MC (%) | kg/pixel, MC | Sedimento, MFM (%) | kg/pixel, MFM

A coincidência dos mapas entre o MC e o MFM não constitui validação independente: os dois distribuem a água pelo mesmo padrão do SCS-CN e usam os mesmos K, C e LS.

# 6. CONCLUSÕES
	O volume escoado TR e a carga de sedimentos SYobs medidos no exutório incluem a vazão de base (34% a 55% do volume). O escoamento direto calculado pelo SCS-CN não é comparável a eles sem uma separação ou um termo de base.
	O SCS-CN com λ = 0,20 não prevê o escoamento direto desta bacia (NSE do volume negativo para qualquer λ testado); o erro vem sobretudo da forma da curva chuva-escoamento (o coeficiente de escoamento medido é aproximadamente independente da chuva), e não da umidade antecedente. Recalibrar a conversão melhora o volume, mas não o sedimento.
	O modelo de dois componentes (encostas e vazão de base) é fisicamente coerente, mas, só com chuva e vazão inicial, tem desempenho equivalente ao de uma regra simples com a chuva do evento (erro mediano de 33%; 71% dos eventos dentro de fator 2).
	O gargalo está em transformar chuva em escoamento: com a água forçada ao valor medido (escoamento direto e vazão de base), 94% dos eventos ficam dentro de fator 2 e o erro mediano cai a 14%.
A espacialização não perde precisão em relação a modelos simples com os mesmos insumos, nem à formulação concentrada da IC quando recebe informação equivalente, e acrescenta o mapa de áreas críticas.
