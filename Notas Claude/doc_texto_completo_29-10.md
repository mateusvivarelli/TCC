# Texto atual do Google Doc "TCC arquivo" (cópia de 29/10/2026 00:30)

Cópia só de leitura, para o revisor. Seções 1 a 3 e Resumo/Abstract: **versão atual, no modelo oficial**. Seções 4 a 6: **ainda no modelo antigo** (serão substituídas pelas propostas de `Notas Claude/proposta_secao*.md`). Equações aparecem como `[EQUAÇÃO]`; imagens como `[IMAGEM]`; tabelas com todas as linhas.

UNIVERSIDADE ESTADUAL DE CAMPINAS
FACULDADE DE ENGENHARIA CIVIL, ARQUITETURA E URBANISMO
DEPARTAMENTO DE RECURSOS HÍDRICOS
MATEUS GUILHERME VIVARELLI
ESPACIALIZAÇÃO DA EQUAÇÃO UNIVERSAL MODIFICADA DE PERDA DE SOLO (MUSLE) PARA IDENTIFICAÇÃO DE ÁREAS CRÍTICAS DE EROSÃO: ESTUDO DE CASO NA BACIA DO RIO JUNDIAÍ
CAMPINAS
2026
UNIVERSIDADE ESTADUAL DE CAMPINAS
FACULDADE DE ENGENHARIA CIVIL, ARQUITETURA E URBANISMO
DEPARTAMENTO DE RECURSOS HÍDRICOS
MATEUS GUILHERME VIVARELLI
ESPACIALIZAÇÃO DA EQUAÇÃO UNIVERSAL MODIFICADA DE PERDA DE SOLO (MUSLE) PARA IDENTIFICAÇÃO DE ÁREAS CRÍTICAS DE EROSÃO: ESTUDO DE CASO NA BACIA DO RIO JUNDIAÍ
Trabalho final de curso apresentado à Faculdade de Engenharia Civil, Arquitetura e Urbanismo da Universidade Estadual de Campinas como requisito para a obtenção do título de Engenheiro Civil. Feito sob a orientação do Me. Luis Fernando Murillo-Bermúdez e co-orientação do Prof. Dr. André Luís Sotero Salustiano Martim.
CAMPINAS
2026
DEDICATÓRIA
AGRADECIMENTOS
“— Sabe, eu andei pensando…
— Sempre um passatempo perigoso.”
John Flanagan, Halt em Perigo
RESUMO
	A Equação Universal Modificada de Perda de Solo (Modified Universal Soil Loss Equation; MUSLE) estima a produção de sedimentos em bacias hidrográficas em eventos de chuva. Este trabalho visa reproduzir a MUSLE de maneira espacializada, em pixels de 30 x 30 metros, na parte alta da bacia do rio Jundiaí (137,8 km², São Paulo, Brasil). Para 17 eventos monitorados entre 2018 e 2020, o escoamento foi calculado pelo método SCS-CN sobre a chuva interpolada de dois postos, com taxa de abstração inicial de 0,05 e retenção convertida pela relação de Woodward et al. (2003). A erosão local seguiu Hao et al. (2022), com a MUSLE alimentada apenas pelo escoamento direto, já que a vazão de base não produz erosão nas encostas. O coeficiente de escala foi calibrado em escala logarítmica e validado por leave-one-out. Com a chuva como única entrada, o modelo acertou 35% dos eventos dentro de fator 2 (erro mediano de 81%), abaixo de uma regra simples com a chuva do evento (82%; erro mediano de 42%), porque o SCS-CN erra o escoamento direto em 46% na mediana dos eventos. Com o escoamento direto forçado ao valor medido, o acerto sobe a 94% dos eventos e o erro mediano cai a 21%. O gargalo está, portanto, em transformar chuva em escoamento. Nessas condições, a espacialização tem desempenho equivalente ao da formulação concentrada (erro mediano de 16%) e acrescenta o mapa de áreas críticas, que permite direcionar medidas de contenção.
Palavras-chave: MUSLE; produção de sedimentos; SCS-CN; modelagem distribuída; SIG; bacia do rio Jundiaí.
ABSTRACT
	The Modified Universal Soil Loss Equation (MUSLE) estimates sediment yield in watersheds during rainfall events. This work aims to spatialize MUSLE at a 30 x 30 m pixel scale in the upper Jundiaí River basin (137.8 km², São Paulo, Brazil). For 17 rainfall events monitored between 2018 and 2020, runoff was computed with the SCS-CN method over rainfall interpolated from two gauges, using an initial abstraction ratio of 0.05 with retention converted by the relation of Woodward et al. (2003). Local erosion followed Hao et al. (2022), with MUSLE driven by direct runoff only, since baseflow does not cause hillslope erosion. The scale coefficient was calibrated on a logarithmic scale and validated by leave-one-out cross-validation. With rainfall as the only input, the model placed 35% of the events within a factor of 2 (median error of 81%), below a simple rule based on event rainfall (82%; median error of 42%), because SCS-CN misestimates direct runoff by 46% in the median event. With direct runoff forced to measured values, the hit rate rises to 94% and the median error drops to 21%. The bottleneck is therefore the conversion of rainfall into runoff. Under these conditions, spatialization performs equivalently to the lumped formulation (median error of 16%) and adds the map of critical areas, which allows erosion control measures to be targeted.
Keywords: MUSLE; sediment yield; SCS-CN; distributed modelling; GIS; Jundiaí River basin.
SUMÁRIO

# 1. INTRODUÇÃO

## 1.1 Contexto
O transporte de sedimentos fluviais é um problema ambiental, social e econômico: afeta a gestão dos recursos hídricos, a qualidade da água, a vida útil de reservatórios e a ocorrência de enchentes. A bacia hidrográfica do rio Jundiaí, no estado de São Paulo, reúne áreas urbanizadas e usos como campo e silvicultura (no alto curso, 14,1% e cerca de 42% da área, respectivamente; seção 3.1), o que a torna vulnerável a processos erosivos e ao aumento da carga de sedimentos nos cursos d'água. Nesse contexto, os modelos hidrossedimentológicos subsidiam o planejamento territorial, a conservação do solo e a recuperação ambiental.
A erosão hídrica em escala de evento é especialmente importante porque é nos eventos de chuva intensa que se movimenta a maior parte do sedimento. Estatísticas de muitas bacias indicam que poucos eventos de alta intensidade podem responder por mais da metade da produção anual de sedimentos (HAO et al., 2022). Abordagens anuais, como a Equação Universal de Perda de Solo Revisada (RUSLE; RENARD et al., 1997), fornecem estimativas úteis da perda média, mas não representam eventos individuais nem a contribuição desproporcional de poucos eventos à exportação anual (BAERT et al., 2026).
Para avaliar a erosão em bacias existem abordagens de natureza distinta: o monitoramento de sedimentos no exutório; os modelos empíricos, como a Equação Universal de Perda de Solo (USLE; WISCHMEIER; SMITH, 1978), a RUSLE e a Equação Universal Modificada de Perda de Solo (Modified Universal Soil Loss Equation; MUSLE; WILLIAMS, 1975); e os modelos distribuídos baseados em processos, como o WEPP e o LISEM, que exigem muitos parâmetros físicos e calibração (HAO et al., 2022). A MUSLE substitui a erosividade da chuva por um termo de energia do escoamento, que combina o volume e a vazão de pico, e por isso estima a produção de sedimentos de cada evento.
Por essa razão, a MUSLE é a formulação de produção de sedimentos do modelo SWAT (NEITSCH et al., 2011) e tem ampla difusão, com aplicações em diferentes países e climas e resultados de acurácia variável entre os estudos (SADEGHI et al., 2014). Essas aplicações são detalhadas na seção 2.2.
Em uma Iniciação Científica anterior (IC; VIVARELLI et al., 2025), a produção de sedimentos na bacia foi quantificada com a MUSLE. Essa aplicação foi concentrada: as características topográficas, de solo e de uso foram resumidas em valores médios para toda a bacia, e o volume e a vazão de pico foram obtidos do hidrograma medido. A simplificação permite validar o modelo no exutório, mas impede identificar as áreas que mais geram sedimento e representar a heterogeneidade local.

## 1.2 Problema e justificativa
Uma MUSLE concentrada fornece uma única estimativa para a bacia, e por isso não indica onde o sedimento é gerado nem quais classes de solo, uso e relevo mais contribuem. Espacializar o modelo em células permite representar a heterogeneidade dos fatores K, LS, C e do número de curva, distribuir o escoamento a partir da chuva interpolada entre os postos e mapear, para cada evento, as áreas críticas de erosão. Um modelo em células também permite separar duas fontes de erro, a estimativa da água (chuva transformada em escoamento) e a fórmula de erosão, e assim identificar o que limita a qualidade das estimativas.
Novas medições de sedimentos são difíceis e caras, porque dependem da coincidência entre eventos de chuva significativos e campanhas de campo, e a bacia não dispõe de seções adicionais de monitoramento. A premissa deste trabalho é aproveitar a base de dados existente, de escoamento e de descarga sólida em suspensão em 17 eventos no exutório, e substituir o modelo concentrado por um modelo espacializado. Assim é possível verificar o modelo em escala de bacia, mapear a erosão gerada em cada evento e identificar o que limita a qualidade das estimativas. Como só há medição no exutório, o mapa de áreas críticas é um resultado relativo, sem validação espacial.

## 1.3 Objetivos

### 1.3.1 Objetivo geral:
Desenvolver e aplicar a espacialização da MUSLE em escala de evento, em ambiente de Sistemas de Informação Geográfica (SIG), para identificar áreas críticas de erosão na parte alta da bacia do rio Jundiaí e avaliar o que limita a qualidade das estimativas.

### 1.3.2 Objetivos específicos:
Espacializar o escoamento superficial de cada um dos 17 eventos pelo método SCS-CN, a partir da chuva interpolada dos postos, e calcular a vazão de pico local (pr) por pixel, segundo Hao et al. (2022);
Implementar uma rotina computacional em Python/SIG que automatize o cálculo espacializado da MUSLE;
Validar o modelo distribuído por validação cruzada, comparando o sedimento simulado com a carga medida na seção de controle em cada evento, com métricas pouco sensíveis a um único evento;
Comparar o modelo espacializado com modelos simples e com a formulação concentrada da IC, para verificar se a espacialização custa precisão;
Identificar o fator que mais limita a qualidade das estimativas (o escoamento ou a erosão);
Mapear as áreas críticas de erosão e quantificar a contribuição de cada classe de uso e de solo.

# 2. FUNDAMENTAÇÃO TEÓRICA

## 2.1 Erosão hídrica em escala de evento
A erosão hídrica é o processo de desagregação, transporte e deposição de partículas de solo pela ação da chuva e do escoamento superficial. Parte do material erodido nas encostas se deposita antes de chegar à rede de drenagem, e a fração que alcança o exutório define a produção de sedimentos da bacia (SY). Em escala de evento, a produção de sedimentos é muito concentrada no tempo: Hao et al. (2022), citando estatísticas de 1.314 bacias, apontam que cerca de dez eventos de alta intensidade podem responder por mais da metade da produção anual. Por isso, modelos de evento, e não de média anual, são mais adequados para diagnosticar quais episódios e quais áreas geram a maior parte do sedimento.
Em escala de evento, a resposta da bacia não depende apenas do total de chuva. Em bacias agrícolas temperadas, Baert et al. (2026) destacam que uma chuva moderada pode gerar escoamento e exportação de sedimentos expressivos quando cai sobre solo úmido, com pouca proteção da cultura ou com alta conectividade hidrológica, enquanto uma chuva mais intensa pode ter resposta limitada quando a capacidade de armazenamento e de infiltração ainda é alta. Abordagens anuais, como a RUSLE (RENARD et al., 1997), estimam a perda média e não representam eventos individuais nem a contribuição desproporcional de poucos eventos à exportação anual de sedimentos.
A relação entre a erosão nas encostas e o sedimento que chega ao exutório é intermediada pela conectividade de sedimentos, isto é, a capacidade de o material ser transportado pela paisagem até um ponto de interesse (como um curso d'água ou um exutório). Nas três bacias estudadas por Hao et al. (2022), a conectividade ficou abaixo de 0,5 em cerca de 80% da área, o que indica que a maior parte do sedimento erodido se deposita antes de chegar ao exutório.

## 2.2 USLE e MUSLE
A Equação Universal de Perda de Solo (USLE; WISCHMEIER; SMITH, 1978) estima a perda média anual de solo pelo produto de seis fatores: erosividade da chuva, erodibilidade do solo (K), comprimento e declividade da encosta (LS), cobertura e manejo (C) e práticas conservacionistas (P). Williams (1975) propôs substituir o fator de erosividade da chuva por um fator de energia do escoamento, o que dá origem à USLE modificada (MUSLE) e permite estimar a produção de sedimentos de um evento isolado:

> [EQUAÇÃO]

em que Y é a produção de sedimentos do evento (t), Q é o volume de escoamento (m³), qp é a vazão de pico (m³/s) e K, LS, C e P são os fatores da USLE. Os coeficientes 11,8 e 0,56 foram ajustados empiricamente por Williams em escala de bacia. Como a equação usa o volume e o pico do escoamento, sua qualidade depende da qualidade da estimativa hidrológica. Baert et al. (2026), em 154 eventos de escoamento monitorados entre 2015 e 2023 em uma bacia agrícola belga de 0,84 km², dos quais 46 com sedimento medido, alimentaram a MUSLE com volume e pico previstos por diferentes formulações da razão de abstração inicial e obtiveram NSE de validação cruzada próximo de zero para o sedimento (-0,03 e 0,01), mesmo com o volume e o pico melhorados.
A MUSLE é a formulação de produção de sedimentos do modelo SWAT, no qual é aplicada a cada unidade de resposta hidrológica. Segundo a documentação do modelo, a substituição da chuva pelo escoamento aumenta a precisão da estimativa, dispensa a razão de entrega de sedimentos e permite calcular a produção de sedimentos de tempestades individuais (NEITSCH et al., 2011).
A equação também tem ampla difusão em estudos locais, em geral com a calibração de seus coeficientes. No Brasil, Avanzi et al. (2008) a calibraram em uma microbacia de 286 ha em Aracruz, ES, e obtiveram coeficiente de 14,96 e expoente de 0,59, em vez de 11,8 e 0,56; Hoppen, Salvador e Michel (2019) mostraram, na bacia do rio Cunha, SC, que a escolha do método de cálculo do fator LS altera os valores ótimos dos parâmetros de calibração. No exterior, Reda, Moges e Kendie (2024) a combinaram com o SCS-CN, com razão de abstração inicial reduzida (λ = 0,023), na bacia do rio Tekeze, na Etiópia, e Azmeri et al. (2024) a aplicaram em SIG na sub-bacia de Krueng Peuto, na Indonésia, concluindo que o escoamento foi o fator de maior efeito. Sadeghi et al. (2014) revisaram 49 trabalhos e concluíram que a acurácia da MUSLE varia com a forma de obtenção das entradas, com a escala e com o uso do solo.
Na bacia do Alto Jundiaí, a Iniciação Científica que precedeu este trabalho (VIVARELLI et al., 2025) aplicou a forma concentrada da equação (volume e pico medidos, fatores médios da bacia) e ajustou os coeficientes aos dados de campo, obtendo um modelo capaz de reproduzir o sedimento de 17 eventos, mas que não indica onde a erosão ocorre.

## 2.3 Método SCS-CN
O método do número de curva do Serviço de Conservação do Solo dos Estados Unidos (SCS-CN) é a abordagem empírica mais usada para estimar o escoamento direto de um evento a partir da chuva (USDA-SCS, 1972; CHOW; MAIDMENT; MAYS, 1988). O escoamento Q (mm) depende da chuva P (mm), da retenção potencial máxima S (mm) e da abstração inicial, tomada como fração λ de S:

> [EQUAÇÃO]


> [EQUAÇÃO]


> [EQUAÇÃO]

O número de curva CN (0 a 100, com valores tabelados na prática entre 30 e 98) depende do grupo hidrológico do solo, do uso e ocupação, da condição hidrológica e das práticas de manejo, sendo tabelado para a condição de umidade antecedente média (AMC II). Os valores correspondentes às condições seca (AMC I) e úmida (AMC III) são obtidos por conversões empíricas (CHOW; MAIDMENT; MAYS, 1988):

> [EQUAÇÃO]

Na bacia estudada, o CN em AMC II varia de 52 a 98 (média 71,6), resultando em valores de 31 a 95 em AMC I, cenário adotado neste trabalho.
O valor padrão da razão de abstração inicial é λ = 0,20, mas há discussão sobre ele. Woodward et al. (2003) analisaram dados de 307 bacias e parcelas dos Estados Unidos e encontraram que λ = 0,05 ajustou melhor que 0,20 em 252 dos casos. Brandão et al. (2025), em 3.578 bacias do mundo, também obtiveram desempenho melhor com λ = 0,05 do que com 0,20, com associação desse valor a regiões áridas, maior área de cultivo, áreas urbanas e solos arenosos; os mesmos autores associam λ = 0,20 a clima úmido e a mais pastagem, e o desempenho absoluto foi baixo (menos de 15% das bacias com NSE acima de 0,5). Em bacia brasileira (Guariroba, MS), Valle Junior, Rodrigues e Oliveira (2019) estimaram λ mediano de 0,045. Nesses três trabalhos, o CN é calibrado em conjunto com λ.
Como o CN tabelado vale para λ = 0,20, usar λ = 0,05 exige converter a retenção S; sem a conversão, o escoamento calculado seria superestimado em 94%. Woodward et al. (2003) propuseram, com os mesmos dados, uma relação de potência entre as retenções obtidas com λ = 0,05 e com λ = 0,20:

> [EQUAÇÃO]

em que S0,05 e S0,20 são as retenções potenciais máximas, em polegadas, para λ = 0,05 e λ = 0,20, respectivamente. No cálculo, com S em milímetros, a relação foi aplicada na forma:

> [EQUAÇÃO]

Neste trabalho adotou-se λ = 0,05 com S convertido por essa relação, porque é a configuração em que o volume calculado mais se aproxima do escoamento direto medido (viés de +3%, contra -12% com λ = 0,20). A relação é uma regressão entre valores de S ajustados a bacias norte-americanas, para chuvas de pelo menos 25,4 mm. Na bacia estudada, 8,4% dos pixels têm CN em AMC I abaixo de 35, fora da faixa tabelada pelos autores, o que é extrapolação. A escolha foi feita observando os mesmos 17 eventos, e isso é discutido nas limitações.
Mesmo bem calibrado, o SCS-CN tem baixa capacidade de previsão do volume de eventos individuais. Baert et al. (2026), em 154 eventos de escoamento de uma bacia agrícola belga de 0,84 km², encontraram NSE máximo de 0,13 para o volume com formulações fixas ou da literatura; com a conversão de Woodward, o NSE do volume foi negativo (-0,87). Em previsão fora da amostra, formulações calibradas por regimes tiveram NSE de 0,21, e a regressão contínua, de 0,40. Os autores apontam o início do escoamento (a abstração inicial) como uma das principais incertezas da modelagem de erosão em escala de evento e concluem que um valor único mais baixo de λ não resolve. Valle Junior et al. (2019) concluíram que o SCS-CN não foi adequado à bacia do Guariroba, onde uma relação simples entre escoamento e chuva (Q = C*P) teve melhor desempenho (NSE de 0,66).

## 2.4 Escoamento direto, vazão de base e medição de sedimentos em suspensão
O hidrograma medido no exutório é a soma do escoamento direto, gerado pela chuva do evento, e da vazão de base, água subterrânea que já alimentava o rio. O SCS-CN calcula somente o escoamento direto. A separação entre as duas componentes não é observável e depende do método adotado; entre os mais usados estão os filtros digitais recursivos de Lyne e Hollick (1979) e de Eckhardt (2005). O filtro de Eckhardt tem dois parâmetros: a constante de recessão (a) e o índice máximo de vazão de base (BFImax), que não é medido e é escolhido pelo usuário. Neste trabalho, a série de vazão de base foi fornecida junto com os dados de monitoramento. Ela é reproduzida pelo filtro de Eckhardt com a = 0,995 (passo horário) e BFImax = 0,70, com diferença mediana de 0,002 m³/s; outros valores de BFImax e o filtro de Lyne e Hollick não a reproduzem. A série serve para obter o escoamento direto medido, usado no modelo forçado ao medido.
A carga de sedimentos em suspensão é estimada, em estações automatizadas, a partir da turbidez, convertida em concentração de sedimentos em suspensão (CSS) por curvas de calibração (MURILLO-BERMÚDEZ et al., 2023). A CSS é, portanto, uma estimativa, e não uma medida direta. Integrando o produto Q * CSS sobre o tempo, obtém-se a carga do evento, que inclui o sedimento carreado pela vazão de base. Neste trabalho, a carga total medida é atribuída ao escoamento superficial, que mobiliza o sedimento nas encostas; a vazão de base é tratada apenas como a água que o transporta.

## 2.5 MUSLE espacializada
Hao et al. (2022) propuseram aplicar a MUSLE por pixel, em escala de evento. A vazão de pico local de cada pixel é calculada a partir do escoamento do próprio pixel, ponderado pela concentração temporal da chuva (razão entre a intensidade máxima e a lâmina do evento), sem roteamento; a erosão local resulta da fórmula de Williams, com o escoamento do pixel dado pelo SCS-CN. Para chegar ao sedimento no exutório, os autores multiplicam a erosão de cada pixel por um grau de conectividade de sedimentos, entre 0 e 1, calibrado em cada bacia. Em três bacias chinesas de 1.310 a 8.973 km², com 58 eventos e vários pluviômetros por bacia, o modelo atingiu NSE de 0,70 a 0,83 no ajuste.
Neste trabalho, a formulação de Hao et al. (2022) é usada sem a conectividade: a soma da erosão dos pixels é multiplicada por um único coeficiente de escala, calibrado contra o sedimento medido no exutório. Esse coeficiente faz o papel de uma conectividade média da bacia e absorve também a diferença de escala entre a equação de Williams, ajustada em bacias, e o pixel.

## 2.6 Dados espaciais em SIG
Os fatores da MUSLE são espacializados em formato raster, com a mesma grade da chuva e do CN. A chuva é interpolada a partir dos postos pelo inverso da distância (IDW), em que o peso de cada posto decresce com o quadrado da distância; com poucos postos, o resultado é um gradiente suave entre eles. Os fatores K e C são atribuídos por classe de solo e de uso, a partir de mapas temáticos. O fator LS é derivado do modelo digital de elevação; neste trabalho, pela formulação de Moore e Burch (1986), baseada na potência do escoamento, aplicada ao MDE corrigido em projeção UTM. A área de contribuição específica foi limitada a 200 m, valor adotado neste trabalho: sem limite, ela chega a milhões de metros nos pixels de canal, onde a USLE, que descreve a erosão de encosta, deixa de valer. O número de curva em condição média (CN-II) vem da base nacional da ANA (2024), que cruza o uso e cobertura do MapBiomas com os solos do IBGE, classificados em grupos hidrológicos segundo Sartori, Lombardi Neto e Genovez (2005); o CN em condição seca (CN-I) foi obtido pela conversão de Chow, Maidment e Mays (1988). O mapa de solos usado pela ANA tem escala 1:250.000, mais grosseira que a grade de 30 m.

## 2.7 Avaliação e validação de modelos
A eficiência de Nash-Sutcliffe (NSE; NASH; SUTCLIFFE, 1970) compara o erro quadrático do modelo com a variância dos dados: vale 1 para um ajuste perfeito, 0 quando o modelo é tão bom quanto prever sempre a média, e é negativa quando é pior. Por usar o quadrado do erro, o NSE é dominado pelos eventos de maior magnitude. Quando poucos eventos são muito maiores que os demais, o NSE pode refletir o acerto de um único evento.
Duas medidas ajudam a reduzir essa sensibilidade: o NSE calculado sobre os logaritmos, que dá peso ao erro relativo, mas passa a ser dominado pelos menores eventos; e métricas baseadas em erro percentual, como a mediana do erro percentual absoluto e a fração de eventos com o simulado entre 0,5 e 2 vezes o medido (critério de fator 2). A correlação de ordem de Spearman avalia se o modelo ordena os eventos corretamente, sem depender da magnitude. Hao et al. (2022) também usaram um NSE em escala logarítmica como função objetivo na calibração do modelo espacializado.
Parâmetros ajustados aos mesmos dados que se usam para avaliar o modelo levam a desempenho otimista. A validação cruzada leave-one-out corrige em parte esse problema: cada evento é previsto com parâmetros ajustados sem ele. A validação cruzada não corrige, porém, o otimismo das escolhas feitas observando os mesmos dados, como a da razão de abstração inicial (seção 2.3).

# 3. ÁREA DE ESTUDO E DADOS

## 3.1 Área de estudo
A área de estudo é a parte alta da bacia do rio Jundiaí, a montante da seção de controle (Rio Jundiaí em Campo Limpo Paulista), com 137,8 km² de área de contribuição, obtida por acumulação de fluxo sobre o modelo digital de elevação (MDE) até o exutório (139,3 km² segundo MURILLO-BERMÚDEZ; MARTIM, 2022). A bacia tem forma alongada, no sentido leste-oeste, com altitudes entre cerca de 724 e 1.314 m, e uma rede de drenagem densa, cujo eixo principal é o rio Jundiaí (Figura 1). O uso do solo é dominado por mata nativa (39,6% da área), campo (29,0%), áreas urbanizadas (14,1%) e silvicultura (12,7%); a lavoura temporária ocupa 3,9% e o solo exposto, 0,5%; os 0,3% restantes são corpos d'água, mineração e afloramento rochoso. Os solos são, em sua maioria, Cambissolos Háplicos (68,6%) e Argissolos Vermelho-Amarelos (17,6%), e 13,7% da área é urbana e não tem classe de solo (Figura 2). O exutório adotado no MDE fica cerca de 900 m a jusante da estação de medição, o que acrescenta pouca área.
O clima regional é subtropical úmido, sem estação seca pronunciada, com chuvas concentradas entre outubro e março. No mapa climático do Plano de Bacias (CONSÓRCIO PROFILL-RHAMA, 2020), segundo a classificação de Köppen, a cabeceira do Jundiaí aparece em Cfb, com Cfa nos trechos mais baixos. A precipitação média anual nos municípios das Bacias PCJ varia de 1.195 a 1.609 mm, e os menores totais ocorrem nos municípios a jusante das sub-bacias do Capivari e do Jundiaí, de modo que a cabeceira tende a estar na porção mais chuvosa da sub-bacia (CONSÓRCIO PROFILL-RHAMA, 2020). Geologicamente, a sub-bacia do Jundiaí é dominada pelo embasamento cristalino pré-cambriano (86,1% da área), constituído de granitoides ígneos a metamórficos, xistos e rochas metassedimentares, com aquífero do tipo fraturado, seguido de depósitos cenozoicos (9,9%) e do Grupo Tubarão (4,1%) (CONSÓRCIO PROFILL-RHAMA, 2020). A área de captação abrange os municípios de Mairiporã, Atibaia, Jarinu e Campo Limpo Paulista (MURILLO-BERMÚDEZ; MARTIM, 2022), sendo neste último que se localiza a seção de controle. As áreas urbanizadas ocupam 14,1% da área de estudo (Figura 2).

> [IMAGEM]

Figura 1. Área de estudo: parte alta da bacia do rio Jundiaí (137,8 km²), com o relevo, a rede de drenagem, a seção de controle e os dois postos pluviométricos (o posto DBT5 fica fora da bacia).

## 3.2 Dados observados
Os dados observados vêm de duas fontes: os dois postos pluviométricos e a seção de controle no exutório. A vazão é registrada pela rede telemétrica do Departamento de Águas e Energia Elétrica (DAEE), integrada ao Sistema de Alerta a Inundações de São Paulo (SAISP), em intervalos de 10 minutos; a turbidez é medida de hora em hora na estação de tratamento de água da SABESP, em amostras de água bruta do rio (MURILLO-BERMÚDEZ; MARTIM, 2022). As séries utilizadas neste trabalho estão em passo horário (Tabela 1). Os 17 eventos, de novembro de 2018 a fevereiro de 2020, estão descritos na Tabela 2.
Tabela 1. Dados observados em campo.

| Dado | Origem | Uso |
|---|---|---|
| Chuva horária | 2 postos: Desemboque do Túnel 5 (DBT5, fora da bacia, a leste) e Rio Jundiaí em Campo Limpo Paulista (próximo ao exutório) | Entrada do modelo |
| Vazão horária (Q) | Seção de controle no exutório | Volume e pico observados |
| Vazão de base (Bt) | Filtro de Eckhardt (2005) aplicado à vazão horária (seção 2.4) | Separação do escoamento direto |
| Concentração de sedimentos em suspensão (CSS) | Seção de controle, a partir de turbidez (MURILLO-BERMÚDEZ et al., 2023) | Carga de sedimentos observada |
| Eventos | 17 eventos, de 11/2018 a 02/2020, janelas de 23 a 149 h | Unidade de análise |

Tabela 2. Características dos 17 eventos: janela, duração, chuva nos postos (P; DBT5 e Campo Limpo), chuva ponderada (R), intensidade máxima em 60 min (RI), vazão de pico, vazão antes do evento e duração da chuva (T chuva).

| Evento | Início | Fim | Dur. (h) | P DBT5 (mm) | P Campo Limpo (mm) | R (mm) | RI (mm/h) | Q pico (m³/s) | Q inicial (m³/s) | T chuva (h) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 22/11/18 09h | 23/11/18 23h | 38 | 32,8 | 19,2 | 23,4 | 23,6 | 10,3 | 1,28 | 9 |
| 2 | 30/11/18 22h | 03/12/18 04h | 54 | 64,0 | 54,4 | 57,3 | 19,0 | 30,4 | 1,70 | 17 |
| 3 | 17/12/18 22h | 20/12/18 22h | 72 | 51,0 | 71,8 | 65,4 | 53,2 | 16,6 | 1,15 | 13 |
| 4 | 24/12/18 06h | 26/12/18 23h | 65 | 57,0 | 27,0 | 36,2 | 35,2 | 17,0 | 1,59 | 9 |
| 5 | 04/01/19 19h | 08/01/19 17h | 94 | 24,0 | 77,2 | 60,9 | 36,6 | 22,1 | 1,71 | 17 |
| 6 | 16/01/19 12h | 17/01/19 13h | 25 | 11,0 | 44,8 | 34,5 | 29,4 | 14,7 | 1,26 | 5 |
| 7 | 25/01/19 00h | 28/01/19 10h | 82 | 29,0 | 38,4 | 35,5 | 15,4 | 16,4 | 1,32 | 12 |
| 8 | 15/02/19 13h | 20/02/19 05h | 112 | 48,4 | 97,6 | 82,5 | 30,6 | 20,4 | 1,53 | 30 |
| 9 | 25/02/19 15h | 01/03/19 13h | 94 | 57,0 | 108,8 | 92,9 | 23,0 | 11,8 | 1,61 | 38 |
| 10 | 17/03/19 05h | 19/03/19 16h | 59 | 14,4 | 30,8 | 25,8 | 12,6 | 10,6 | 2,54 | 7 |
| 11 | 04/07/19 12h | 08/07/19 07h | 91 | 62,8 | 79,0 | 74,0 | 11,8 | 20,9 | 0,94 | 23 |
| 12 | 30/12/19 09h | 31/12/19 08h | 23 | 0,0 | 34,2 | 23,7 | 32,8 | 13,1 | 0,92 | 2 |
| 13 | 02/01/20 11h | 04/01/20 17h | 54 | 43,8 | 88,6 | 74,9 | 36,6 | 16,0 | 1,06 | 15 |
| 14 | 07/01/20 18h | 10/01/20 19h | 73 | 37,8 | 101,8 | 82,2 | 37,4 | 22,3 | 2,27 | 17 |
| 15 | 02/02/20 20h | 09/02/20 01h | 149 | 86,0 | 163,0 | 139,4 | 47,8 | 28,4 | 1,23 | 37 |
| 16 | 09/02/20 14h | 13/02/20 21h | 103 | 63,6 | 113,6 | 97,7 | 15,8 | 23,1 | 2,68 | 35 |
| 17 | 20/02/20 09h | 22/02/20 10h | 49 | 68,0 | 64,6 | 65,6 | 43,0 | 21,4 | 1,77 | 14 |
| Média |  |  | 73 | 44,2 | 71,5 | 63,1 | 29,6 | 18,6 | 1,56 | 18 |

Da série horária obtêm-se, para cada evento, o volume escoado total, a vazão de pico Qpico (m³/s) e a carga de sedimentos observada somada sobre as leituras horárias da janela do evento. A carga observada varia de 199 a 3.829 t por evento (média de 1.403 t; soma de 23.846 t).
O volume medido inclui a vazão de base. Em todos os 17 eventos, o volume TR é exatamente a soma das vazões horárias na janela do evento, ou seja, o volume total escoado no exutório. A vazão de base (coluna Bt da série), separada pelo filtro de Eckhardt (seção 2.4), corresponde a 34% a 55% desse volume por evento (47% no conjunto), e o escoamento direto restante soma 15,3 de 28,9 milhões de m³ (Tabela 3). O SCS-CN calcula só o escoamento direto. SYobs é a carga total do evento.
Tabela 3. Volume total, vazão de base e escoamento direto medidos; escoamento direto calculado pelo SCS-CN; sedimento medido.

| Evento | Volume total TR (10³ m³) | Vazão de base Σ Bt (10³ m³) | Base (% do total) | Direto medido (10³ m³) | SCS-CN, λ = 0,05 (10³ m³) | SCS-CN / medido | Sedimento medido (t) |
|---|---|---|---|---|---|---|---|
| 1 | 409 | 185 | 45 | 224 | 36 | 0,16 | 266 |
| 2 | 2.630 | 899 | 34 | 1.731 | 521 | 0,30 | 2.040 |
| 3 | 1.070 | 485 | 45 | 585 | 751 | 1,28 | 928 |
| 4 | 1.704 | 716 | 42 | 987 | 154 | 0,16 | 1.380 |
| 5 | 1.840 | 1.008 | 55 | 832 | 695 | 0,83 | 1.372 |
| 6 | 325 | 142 | 44 | 183 | 158 | 0,86 | 199 |
| 7 | 1.301 | 651 | 50 | 650 | 142 | 0,22 | 1.317 |
| 8 | 2.581 | 1.331 | 52 | 1.250 | 1.336 | 1,07 | 2.109 |
| 9 | 1.737 | 936 | 54 | 801 | 1.725 | 2,15 | 1.155 |
| 10 | 1.236 | 684 | 55 | 552 | 57 | 0,10 | 847 |
| 11 | 2.437 | 958 | 39 | 1.479 | 997 | 0,67 | 1.822 |
| 12 | 187 | 87 | 46 | 101 | 63 | 0,62 | 211 |
| 13 | 1.198 | 464 | 39 | 735 | 1.073 | 1,46 | 1.196 |
| 14 | 1.822 | 891 | 49 | 931 | 1.363 | 1,46 | 1.731 |
| 15 | 4.280 | 2.103 | 49 | 2.177 | 3.963 | 1,82 | 3.829 |
| 16 | 3.293 | 1.699 | 52 | 1.595 | 1.934 | 1,21 | 1.736 |
| 17 | 883 | 434 | 49 | 449 | 734 | 1,64 | 1.710 |
| Total | 28.934 | 13.671 | 47 | 15.263 | 15.702 | 1,03 | 23.846 |


## 3.3 Dados cartográficos
Os dados cartográficos são os mapas temáticos de solo e de uso do Plano de Bacias (CONSÓRCIO PROFILL-RHAMA, 2020), dos quais saem os fatores K e C, com os valores por classe adotados na Iniciação Científica anterior (VIVARELLI et al., 2025); o modelo digital de elevação, que fornece o relevo e o fator LS; e o número de curva (CN) da base nacional da Agência Nacional de Águas e Saneamento Básico (ANA, 2024), convertido para a condição de umidade seca (Tabelas 4 a 6; Figuras 2 e 3).
Tabela 4. Dados cartográficos.

| Fator | Fonte | Valor médio |
|---|---|---|
| K | mapa pedológico (CONSÓRCIO PROFILL-RHAMA, 2020), valor de K por classe de solo da IC | 0,039 |
| C | mapa de uso do solo (CONSÓRCIO PROFILL-RHAMA, 2020), valor de C por classe de uso da IC | 0,050 |
| LS | MDE de 30 m (USGS), corrigido e com área acumulada no SAGA/QGIS; LS por Moore e Burch (1986), com rampa limitada a 200 m | 7,80 |
| P | constante | 1,0 |
| CN | raster BR_CN-2022 da ANA (30 m), CN-II convertido para CN-I (Chow, Maidment e Mays, 1988) | 52,5 (CN-I) |


> [IMAGEM]

Figura 2. Classes de solo e de uso do solo na área de estudo, com a participação de cada classe na área da bacia.
Tabela 5. Valores de K por classe de solo e participação de cada classe nos pixels de cálculo.

| Classe de solo | K (t h MJ-1 mm-1) | Pixels de cálculo (%) |
|---|---|---|
| Cambissolos Háplicos | 0,0475 | 68,6 |
| Neossolos Litólicos | 0,0463 | 0,0 |
| Argissolos Vermelho-Amarelos | 0,0351 | 17,6 |
| Afloramento Rochoso | 0,0087 | 0,1 |
| Área Urbana | 0,0000 | 13,7 |

Tabela 6. Valores de C por classe de uso e participação de cada classe nos pixels de cálculo.

| Classe de uso | C | Pixels de cálculo (%) |
|---|---|---|
| Afloramento Rochoso | 1,000 | 0,0 |
| Solo exposto | 1,000 | 0,5 |
| Mineração | 1,000 | 0,0 |
| Lavoura Temporária | 0,212 | 3,9 |
| Silvicultura | 0,121 | 12,7 |
| Campo | 0,050 | 29,0 |
| Mata Nativa | 0,015 | 39,6 |
| Corpos D'Água | 0,000 | 0,2 |
| Área Urbanizada | 0,000 | 14,1 |


> [IMAGEM]

Figura 3. Fatores espacializados: erodibilidade (K), cobertura e manejo (C), fator topográfico (LS) e número de curva para a condição seca (CN-I).
Todos os rasters usam a mesma grade de 884 * 365 pixels de ~30 m (29,992 * 29,925 m; área do pixel de 897,49 m²), em SIRGAS 2000 / UTM 23S. Cerca de 154,7 mil pixels têm número de curva e 153,9 mil têm todos os fatores (K, C, LS e CN), o que corresponde a 138,1 km²; a diferença de cerca de 810 pixels vem de bordas em que os mapas de solo, uso e relevo não coincidem, e esses pixels ficam de fora do cálculo da erosão. Nas áreas urbanizadas e nos corpos d'água, o fator C é zero, e nas áreas sem classe de solo (urbanas), K é zero: esses pixels têm erosão nula no modelo.
Os valores de CN não foram calculados neste trabalho: vêm do raster BR_CN-2022 da ANA (2024), de 30 m, reprojetado para SIRGAS 2000 / UTM 23S. Essa base combina o uso e a cobertura da terra do MapBiomas (coleção 2023, ano de 2022) com o mapa pedológico do IBGE, e os solos são classificados em grupos hidrológicos com base em Sartori, Lombardi Neto e Genovez (2005). O raster corresponde à condição de umidade média (CN-II) e, na área de estudo, assume valores entre 52 e 98, com média de 71,6 nos pixels de cálculo. A condição seca (CN-I), usada no modelo, foi obtida do CN-II pela conversão empírica de Chow, Maidment e Mays (1988) e tem média de 52,5. O CN deriva do uso da terra do MapBiomas de 2022, enquanto K e C derivam do mapa de uso do Plano de Bacias (2020), o que se reconhece como limitação.

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

| Símbolo | Significado | Unidade |
|---|---|---|
| P1, P2 | chuva total do evento nos postos DBT5 e Campo Limpo | mm |
| R | lâmina de chuva do evento | mm |
| RI | intensidade máxima de chuva em 60 min | mm/h |
| Tchuva | duração da chuva | h |
| TR | volume total escoado no exutório | m³ |
| Vbase | volume da vazão de base | m³ |
| Vdir | volume de escoamento direto | m³ |
| Qbinicio | vazão no início do evento | m³/s |
| Qpico | vazão de pico | m³/s |
| SYobs | carga de sedimentos medida (total) | t |


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

| Versão | Escoamento direto (termo 1) | Vazão de base (termo 2) |
|---|---|---|
| Modelo calculado (MC) | SCS-CN, a partir da chuva | Qbinicio * Tchuva |
| Modelo forçado ao medido (MFM) | Volume medido, distribuído pelo padrão do SCS-CN | Vazão de base medida (Bt) |


## 4.6 Calibração dos parâmetros
Os parâmetros c1 e c2 foram ajustados aos 17 sedimentos medidos minimizando o erro em escala logarítmica:

> [EQUAÇÃO]

em que Vref,n é o volume de referência do termo de base. Esse critério pesa os eventos pelo erro relativo e evita que um único evento muito grande (o evento 15 responde por 48,7% da variância linear da carga medida e por 49% do peso na calibração por mínimos quadrados lineares) comande o ajuste. O problema foi resolvido por mínimos quadrados não lineares com limites (algoritmo de região de confiança), a partir de três pontos de partida, e a melhor solução foi mantida. A Tabela 9 reúne os parâmetros fixos e calibrados.
Tabela 9. Parâmetros fixos e calibrados dos modelos.

| Parâmetro | Valor | Origem |
|---|---|---|
| Coeficiente de Williams (11,8) e expoente (0,56) | 11,8 e 0,56 | Williams (1975), mantidos |
| λ (razão de abstração inicial) | 0,20 | valor padrão do SCS-CN (CN tabelado) |
| Peso do posto DBT5 / Campo Limpo na lâmina do evento | 0,307 / 0,693 | mínimos quadrados nos 17 eventos |
| P (práticas conservacionistas) | 1,0 | sem práticas na bacia |
| MC: c1 (t por unidade de Eunit) | 0,0035 | calibrado em log, 17 eventos |
| MC: c2 (t por m³ de volume de base de referência) | 0,01311 | calibrado em log, 17 eventos |
| MFM: c1 | 0,0099 | calibrado em log, 17 eventos |
| MFM: c2 (t por m³ de vazão de base medida) | 0,00114 | calibrado em log, 17 eventos |
| IC refeita: α e β | 0,978 e 0,733 | regressão em log, K = 0,031, LS = 0,536, C = 0,267 (IC: 0,277 e 0,807) |


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

| Grandeza | Valor |
|---|---|
| DBT5 / Campo Limpo | 62,8 mm / 79,0 mm |
| lâmina do evento R = 0,307 * 62,8 + 0,693 * 79,0 | 74,0 mm |
| intensidade máxima RI; razão RI/R | 11,8 mm/h; 0,159 por hora |
| média nos pixels de cálculo (intervalo no raster) | 73,5 mm (63,2 a 79,0 mm) |
| CN-I médio; S médio | 52,5; 255,7 mm |
| Q médio dos pixels; pixels sem escoamento | 5,4 mm; 10% |
| volume calculado pelo SCS-CN / medido | 751 mil m³ / 1.479 mil m³ (razão 0,51) |
| chuva P; CN-II -> CN-I; S | 75,4 mm; 81,0 -> 64,2; 141,9 mm |
| abstração inicial λS; escoamento Q | 28,4 mm; (75,4 - 28,4)² / (75,4 + 0,8 * 141,9) = 11,72 mm |
| vazão de pico local pr | 11,72/1000 * 897,49 * 0,159 / 3600 = 4,66 * 10^-4 m³/s |
| K; C; LS | 0,0351; 0,212; 4,869 |
| índice de erosão Eunit | 11,8 * (11,72 * 4,66 * 10^-4 * 897,49)0,56 * 0,0351 * 0,212 * 4,869 = 1,039 |
| sedimento do pixel c1 * Eunit | 0,00352 * 1,038 = 0,0037 t (3,7 kg) |
| soma de Eunit sobre os pixels | 30.003 |
| termo das encostas c1 * ΣE | 0,00352 * 30.003 = 106 t |
| volume de referência da base Qbinicio * Tchuva * 3600 | 0,945 * 23 * 3.600 = 78.226 m³ |
| termo de base c2 * volume | 0,01311 * 78.226 = 1.025 t |
| MC: validação cruzada | 1.098 t (-40%) |
| MFM: validação cruzada | 1.711 t (-6%) |
| SYobs = Σ Q * CSS | 1.822 t |


> [IMAGEM]

Figura 5. Etapas espaciais do modelo no evento 11: chuva interpolada, retenção S, escoamento direto, índice de erosão Eunit e sedimento das encostas.

# 5. RESULTADOS E DISCUSSÃO

## 5.1 O volume e a carga medidos incluem a vazão de base
Os resultados da seção 3.2 mostram que a comparação direta entre o escoamento calculado pelo SCS-CN e o volume medido é desigual: o modelo calcula apenas o escoamento direto, e o volume medido tem de 34% a 55% de vazão de base (Tabela 3). O resultado mais importante desta fase é, portanto, de definição: qualquer calibração do SCS-CN contra TR ajusta o modelo a uma grandeza que ele não representa.

## 5.2 Resultados do Modelo Calculado (MC)
O MC (só chuva e vazão inicial) obteve c1 = 0,0035 e c2 = 0,0131 t por m³ de volume de referência (Tabela 9). Na validação cruzada, o erro percentual mediano foi de 32,6%, e 71% dos eventos (12 de 17) ficaram dentro de fator 2; o NSE em escala logarítmica foi 0,48 e a correlação de Spearman, 0,72. No ajuste, o MC superestima os eventos 1, 9 e 16 (+105%, +178% e +171%) e subestima os eventos 4, 7, 11 e 12 (de -38% a -58%) (Tabela 11). A Figura 6 compara o sedimento simulado, na validação cruzada, com o medido em cada evento.
Tabela 11. Sedimento por evento (t): medido e simulado pelo MC, com a decomposição em encostas e vazão de base.

| Evento | Medido | Encostas | Base | Total simulado | Erro no ajuste (%) | Erro na validação cruzada (%) |
|---|---|---|---|---|---|---|
| 1 | 266 | 1 | 545 | 546 | +105 | +124 |
| 2 | 2.040 | 53 | 1.366 | 1.419 | -30 | -33 |
| 3 | 928 | 172 | 704 | 876 | -6 | -6 |
| 4 | 1.380 | 11 | 675 | 686 | -50 | -54 |
| 5 | 1.372 | 140 | 1.373 | 1.514 | +10 | +11 |
| 6 | 199 | 12 | 298 | 310 | +56 | +62 |
| 7 | 1.317 | 5 | 745 | 750 | -43 | -47 |
| 8 | 2.109 | 276 | 2.168 | 2.444 | +16 | +17 |
| 9 | 1.155 | 316 | 2.893 | 3.208 | +178 | +196 |
| 10 | 847 | 1 | 839 | 840 | -1 | -1 |
| 11 | 1.822 | 106 | 1.025 | 1.131 | -38 | -40 |
| 12 | 211 | 3 | 87 | 89 | -58 | -61 |
| 13 | 1.196 | 233 | 749 | 982 | -18 | -21 |
| 14 | 1.731 | 325 | 1.819 | 2.144 | +24 | +26 |
| 15 | 3.829 | 1.152 | 2.144 | 3.296 | -14 | -26 |
| 16 | 1.736 | 290 | 4.422 | 4.712 | +171 | +191 |
| 17 | 1.710 | 140 | 1.166 | 1.306 | -24 | -25 |


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

| Modelo | Informação medida usada | Erro mediano | Dentro de fator 2 | NSE em log | Spearman |
|---|---|---|---|---|---|
| SY = c * chuva do evento | chuva | 41,9% | 82% | 0,53 | 0,63 |
| MC | chuva, vazão inicial | 32,6% | 71% | 0,48 | 0,72 |
| SY = c * volume total medido | volume total | 17,6% | 94% | 0,86 | 0,88 |
| MFM | volume direto e vazão de base | 13,6% | 94% | 0,87 | 0,85 |
| IC | volume total e pico | 16,3% | 100% | 0,87 | 0,93 |

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

| Classe de uso | Área (%) | Sedimento, MC (%) | kg/pixel, MC | Sedimento, MFM (%) | kg/pixel, MFM |
|---|---|---|---|---|---|
| Mata Nativa | 39,6 | 6,3 | 0,20 | 5,2 | 0,46 |
| Campo | 29,0 | 39,4 | 1,68 | 39,5 | 4,73 |
| Área Urbanizada | 14,1 | 0,0 | 0,00 | 0,0 | 0,00 |
| Silvicultura | 12,7 | 21,6 | 2,11 | 19,3 | 5,29 |
| Lavoura Temporária | 3,9 | 22,5 | 7,04 | 20,7 | 18,27 |
| Solo exposto | 0,5 | 8,6 | 23,08 | 13,4 | 101,33 |
| Corpos D'Água | 0,2 | 0,0 | 0,00 | 0,0 | 0,00 |
| Mineração | 0,0 | 1,7 | 44,24 | 1,9 | 134,72 |
| Afloramento Rochoso | 0,0 | 0,0 | 0,12 | 0,0 | 0,16 |

Tabela 14. Contribuição de cada classe de solo para o sedimento médio das encostas.

| Classe de solo | Área (%) | Sedimento, MC (%) | kg/pixel, MC | Sedimento, MFM (%) | kg/pixel, MFM |
|---|---|---|---|---|---|
| Cambissolos Háplicos | 68,6 | 93,7 | 1,69 | 93,8 | 4,75 |
| Argissolos Vermelho-Amarelos | 17,6 | 6,3 | 0,44 | 6,2 | 1,22 |
| Área Urbana | 13,7 | 0,0 | 0,00 | 0,0 | 0,00 |
| Afloramento Rochoso | 0,1 | 0,0 | 0,09 | 0,0 | 0,28 |
| Neossolos Litólicos | 0,0 | 0,0 | 0,00 | 0,0 | 0,00 |

A coincidência dos mapas entre o MC e o MFM não constitui validação independente: os dois distribuem a água pelo mesmo padrão do SCS-CN e usam os mesmos K, C e LS.

# 6. CONCLUSÕES
	O volume escoado TR e a carga de sedimentos SYobs medidos no exutório incluem a vazão de base (34% a 55% do volume). O escoamento direto calculado pelo SCS-CN não é comparável a eles sem uma separação ou um termo de base.
	O SCS-CN com λ = 0,20 não prevê o escoamento direto desta bacia (NSE do volume negativo para qualquer λ testado); o erro vem sobretudo da forma da curva chuva-escoamento (o coeficiente de escoamento medido é aproximadamente independente da chuva), e não da umidade antecedente. Recalibrar a conversão melhora o volume, mas não o sedimento.
	O modelo de dois componentes (encostas e vazão de base) é fisicamente coerente, mas, só com chuva e vazão inicial, tem desempenho equivalente ao de uma regra simples com a chuva do evento (erro mediano de 33%; 71% dos eventos dentro de fator 2).
	O gargalo está em transformar chuva em escoamento: com a água forçada ao valor medido (escoamento direto e vazão de base), 94% dos eventos ficam dentro de fator 2 e o erro mediano cai a 14%.
A espacialização não perde precisão em relação a modelos simples com os mesmos insumos, nem à formulação concentrada da IC quando recebe informação equivalente, e acrescenta o mapa de áreas críticas.

# REFERÊNCIAS BIBLIOGRÁFICAS
AGÊNCIA NACIONAL DE ÁGUAS E SANEAMENTO BÁSICO (Brasil). Curva Número na Base Ottocodificada (1985, 2014 e 2022). Brasília: ANA, 2024. Base de dados geoespacial. Disponível em: https://metadados.snirh.gov.br/geonetwork/srv/api/records/d1c36d85-a9d5-4f6a-85f7-71c2dc801a67. Acesso em: 17 out. 2026. 
AVANZI, J. C. et al. Calibração e aplicação do modelo MUSLE em uma microbacia hidrográfica nos Tabuleiros Costeiros brasileiros. Revista Brasileira de Engenharia Agrícola e Ambiental, v. 12, n. 6, p. 563-569, 2008. DOI: https://doi.org/10.1590/S1415-43662008000600001.
AZMERI et al. Interphase modeling of sedimentation rate using the GIS-based modified universal soil loss equation. Applied Geomatics, v. 16, n. 4, p. 1057-1068, 2024. DOI: https://doi.org/10.1007/s12518-024-00599-y.
BAERT, P. et al. A regime-based framework for linking runoff initiation and event-scale sediment export in a small temperate agricultural loess catchment. Catena, v. 274, art. 110497, 2026. DOI: https://doi.org/10.1016/j.catena.2026.110497. 
BRANDÃO, A. R. A. et al. Toward a better understanding of curve number and initial abstraction ratio values from a large sample of watersheds perspective. Journal of Hydrology, v. 655, art. 132941, 2025. DOI: https://doi.org/10.1016/j.jhydrol.2025.132941. 
CHOW, V. T.; MAIDMENT, D. R.; MAYS, L. W. Applied hydrology. New York: McGraw-Hill, 1988. 
CONSÓRCIO PROFILL-RHAMA. Plano de Recursos Hídricos das Bacias Hidrográficas dos Rios Piracicaba, Capivari e Jundiaí, 2020 a 2035: relatório final. Piracicaba: Comitês PCJ; Fundação Agência das Bacias PCJ, 2020. 
ECKHARDT, K. How to construct recursive digital filters for baseflow separation. Hydrological Processes, v. 19, n. 2, p. 507-515, 2005. DOI: https://doi.org/10.1002/hyp.5675. 
HAO, R. et al. Incorporating sediment connectivity index into MUSLE model to explore soil erosion and sediment yield relationships at event scale. Journal of Hydrology, v. 614, art. 128579, 2022. DOI: https://doi.org/10.1016/j.jhydrol.2022.128579. 
HOPPEN, E.; SALVADOR, C.; MICHEL, G. Aplicação da MUSLE considerando diferentes métodos de cálculo do fator topográfico LS. In: SIMPÓSIO BRASILEIRO DE RECURSOS HÍDRICOS, 23., 2019, Foz do Iguaçu. Anais [...]. Porto Alegre: ABRHidro, 2019. Disponível em: https://anais.abrhidro.org.br/job.php?Job=5833. Acesso em: 27 out. 2026.
LYNE, V.; HOLLICK, M. Stochastic time-variable rainfall-runoff modelling. In: HYDROLOGY AND WATER RESOURCES SYMPOSIUM, 1979, Perth. Proceedings [...]. Barton: Institution of Engineers Australia, 1979. p. 89-93. 
MOORE, I. D.; BURCH, G. J. Physical basis of the length-slope factor in the universal soil loss equation. Soil Science Society of America Journal, v. 50, n. 5, p. 1294-1298, 1986. DOI: https://doi.org/10.2136/sssaj1986.03615995005000050042x. 
MURILLO-BERMÚDEZ, L. F.; MARTIM, A. L. S. S. Avaliação qualitativa do efeito de histereses entre vazão e concentração de sedimentos em suspensão no rio Jundiaí, SP. In: INTERNATIONAL WORKSHOP FOR INNOVATION IN SAFE DRINKING WATER, 1., 2022, Campinas. Proceedings [...]. Campinas: Unicamp, 2022. p. 56-60. DOI: https://doi.org/10.20396/iwisdw.n1.2022.4793. 
MURILLO-BERMÚDEZ, L. F.; MARTIM, A. L. S. S.; POLETO, C.; DALFRÉ FILHO, J. G. Correlation of turbidity and suspended sediment concentration in natural water flow using alternative data of water treatment plant, case of study in the upper Jundiaí river, Brazil. International Journal of River Basin Management, v. 21, n. 2, p. 233-241, 2023. DOI: https://doi.org/10.1080/15715124.2021.1961794. 
NASH, J. E.; SUTCLIFFE, J. V. River flow forecasting through conceptual models part I: a discussion of principles. Journal of Hydrology, v. 10, n. 3, p. 282-290, 1970. DOI: https://doi.org/10.1016/0022-1694(70)90255-6. 
NEITSCH, S. L. et al. Soil and Water Assessment Tool theoretical documentation: version 2009. College Station: Texas Water Resources Institute, 2011. (Technical Report, n. 406). Disponível em: https://swat.tamu.edu/media/99192/swat2009-theory.pdf. Acesso em: 27 out. 2026.
REDA, Y.; MOGES, A.; KENDIE, H. Application of the Modified Universal Soil Loss Equation (MUSLE) for the prediction of sediment yield in Agewmariam experimental watershed, Tekeze River basin, Northern Ethiopia. Heliyon, v. 10, n. 15, e35052, 2024. DOI: https://doi.org/10.1016/j.heliyon.2024.e35052.
RENARD, K. G. et al. Predicting soil erosion by water: a guide to conservation planning with the Revised Universal Soil Loss Equation (RUSLE). Washington, DC: USDA, 1997. (Agriculture Handbook, n. 703).
SADEGHI, S. H. R.; GHOLAMI, L.; KHALEDI DARVISHAN, A.; SAEIDI, P. A review of the application of the MUSLE model worldwide. Hydrological Sciences Journal, v. 59, n. 2, p. 365-375, 2014. DOI: https://doi.org/10.1080/02626667.2013.866239.
SARTORI, A.; LOMBARDI NETO, F.; GENOVEZ, A. M. Classificação hidrológica de solos brasileiros para a estimativa da chuva excedente com o método do Serviço de Conservação do Solo dos Estados Unidos. Parte 1: classificação. Revista Brasileira de Recursos Hídricos, v. 10, n. 4, p. 5-18, 2005. DOI: https://doi.org/10.21168/rbrh.v10n4.p5-18. 
USDA-SCS - UNITED STATES DEPARTMENT OF AGRICULTURE, SOIL CONSERVATION SERVICE. National Engineering Handbook, Section 4: hydrology. Washington, DC: USDA-SCS, 1972.
VALLE JUNIOR, L. C. G.; RODRIGUES, D. B. B.; OLIVEIRA, P. T. S. Initial abstraction ratio and Curve Number estimation using rainfall and runoff data from a tropical watershed. RBRH, Porto Alegre, v. 24, e5, 2019. DOI: https://doi.org/10.1590/2318-0331.241920170199.
VIVARELLI, M. G. et al. Aplicação da equação universal de perda de solo modificada e calibração com dados de campo em uma bacia hidrográfica antropizada. Artigo (Iniciação Científica) - Universidade Estadual de Campinas, Campinas, 2025.
WILLIAMS, J. R. Sediment-yield prediction with universal equation using runoff energy factor. In: UNITED STATES DEPARTMENT OF AGRICULTURE. Present and prospective technology for predicting sediment yield and sources. Washington, DC: USDA-ARS, 1975. p. 244-252. (ARS-S-40).
WISCHMEIER, W. H.; SMITH, D. D. Predicting rainfall erosion losses: a guide to conservation planning. Washington, DC: USDA, 1978. (Agriculture Handbook, n. 537). 
WOODWARD, D. E. et al. Runoff curve number method: examination of the initial abstraction ratio. In: WORLD WATER & ENVIRONMENTAL RESOURCES CONGRESS, 2003, Philadelphia. Proceedings [...]. Reston: ASCE, 2003. p. 1-10. DOI: https://doi.org/10.1061/40685(2003)308.
