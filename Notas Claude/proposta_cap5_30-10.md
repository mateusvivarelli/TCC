# Proposta do capítulo 5: CONCLUSÕES E TRABALHOS FUTUROS (30/10/2026)

Sessão na nuvem, sem acesso ao usuário nem ao Doc. **Nada foi aplicado no Doc.** Substitui o capítulo 6 do Doc e a `proposta_secao6.md` de 29/10. Coerente com `proposta_cap3_30-10.md` e `proposta_cap4_30-10.md`: IC só com valores originais; "não se distingue" no lugar de "equivalente"; o bom desempenho com o escoamento medido mostra o peso do volume, não valida a fórmula de erosão.

Forma: parágrafos corridos (C21 também vale aqui), cada um ligado a um objetivo específico da 1.3.2. Os colchetes com o número do objetivo **não vão para o Doc**.

---

## Mudança proposta nos objetivos específicos (1.3.2)

Proponho mudar só o objetivo 5 e, levemente, o 4 (o 4 já está no item 3.6 de `ajustes_cap1_a_3_30-10.md`).

- Objetivo 5, atual (já com a troca de "água"): "Avaliar o quanto a estimativa do escoamento limita a qualidade das estimativas, comparando o modelo com o escoamento superficial direto calculado e com o escoamento direto forçado ao valor medido;"
- Proposta: "Avaliar o quanto a estimativa do escoamento superficial direto limita a qualidade das estimativas de sedimento, comparando o modelo com o escoamento calculado a partir da chuva e com o escoamento forçado ao valor medido, e com modelos simples que usam a mesma informação;"
- Por quê: o resultado só permite separar o efeito do escoamento; a parte da "fórmula de erosão" não foi isolada, porque, com o escoamento medido, a MUSLE não se distingue de uma regra proporcional ao volume (revisão de 29/10, achado 8). A comparação com os modelos simples é o que permite dizer isso, e passa a fazer parte do objetivo. Os demais objetivos (1, 2, 3 e 6) foram cumpridos como estão escritos e não precisam mudar.

---

# 5. CONCLUSÕES

A MUSLE foi aplicada de forma espacializada, pixel a pixel, em 17 eventos de chuva na parte alta da bacia do rio Jundiaí, com o escoamento superficial direto de cada pixel calculado pelo método SCS-CN a partir da chuva interpolada de dois postos e com a vazão de pico local de cada pixel calculada segundo Hao et al. (2022). Todo o cálculo foi automatizado em uma rotina em Python, que lê os rasters e as séries, calcula os 17 eventos, calibra e valida o coeficiente de escala e gera as tabelas e os mapas. [objetivos 1 e 2]

O método SCS-CN, com o número de curva da base nacional convertido para a condição seca e razão de abstração inicial de 0,05 com a retenção convertida, reproduziu o volume total de escoamento direto dos 17 eventos (viés de +3%), mas não o de cada evento: o erro mediano por evento foi de 46%, o NSE do volume foi negativo e só 65% dos eventos ficaram dentro de fator 2. O método superestima os eventos de maior chuva e subestima os de menor chuva, porque, nesta bacia, a fração da chuva que escoa não cresce com a chuva, como a curva do método supõe. A esse erro se somam a interpolação da chuva a partir de apenas dois postos, a delimitação manual dos eventos e a incerteza da separação da vazão de base. [objetivo 5]

Com a chuva como única entrada, o Modelo Calculado de Erosão (MC) teve erro mediano de 81% e 35% dos eventos dentro de fator 2 na validação cruzada, desempenho pior que o de uma regra simples proporcional à chuva do evento (42% e 82%), e a diferença entre os dois não se explica pelo acaso. O erro do sedimento do MC é quase todo herdado do erro do escoamento, que explica 91% da sua variância, e é ligeiramente ampliado pela formulação, em que a erosão cresce com a potência 1,12 do escoamento. [objetivos 3 e 4]

O elo que mais limita a estimativa do sedimento a partir da chuva é a conversão da chuva em escoamento superficial direto: com o volume de escoamento direto forçado ao medido (MFM), o mesmo modelo, com a mesma fórmula de erosão e os mesmos fatores, passa a erro mediano de 21% e 94% dos eventos dentro de fator 2. Esse ganho vem do volume medido. Como a carga medida é o produto do volume escoado por uma concentração que varia pouco entre os eventos, qualquer modelo que receba o volume medido acerta a ordem de grandeza da carga, e, com o escoamento medido, a MUSLE espacializada não se distinguiu de uma regra simples proporcional ao volume (16% de erro mediano). O trabalho mostra, portanto, o peso do escoamento, mas não permite avaliar separadamente a fórmula de erosão. [objetivo 5]

Com o escoamento medido, o erro do modelo espacializado (21%) é da mesma ordem que o da formulação concentrada da Iniciação Científica anterior com os seus valores originais (22%, 100% dos eventos dentro de fator 2), que usa o volume total e a vazão de pico medidos e foi ajustada nos próprios eventos, sem validação cruzada. Como as duas aplicações não usam exatamente os mesmos eventos nem as mesmas cargas medidas, a comparação é indicativa: a espacialização não se mostrou pior, e acrescenta o mapa de onde a erosão é produzida. [objetivo 4]

As áreas críticas de erosão, os 5% de pixels de maior erosão média, ficam nas mesmas manchas da porção central e oeste da bacia nos dois modelos (94% de coincidência). Campo, silvicultura e lavoura temporária, com 46% da área, respondem por 83% da erosão média estimada, e a lavoura temporária e o solo exposto produzem, por unidade de área, cerca de 5 e 18 vezes a média da bacia; 93% da erosão vem dos Cambissolos Háplicos. [a calcular no PC: frase sobre a declividade, por exemplo "as encostas com declividade acima de X% respondem por Y% da erosão"]. Cerca de [a calcular no PC: X]% da variação espacial da erosão média acompanha o produto dos fatores K, LS e C, e o restante vem da distribuição do escoamento, isto é, da chuva e do número de curva. Esses resultados são relativos: dependem dos valores de K e C adotados por classe, consideram a área urbana sem erosão e não puderam ser validados no espaço, porque só há medição de sedimento no exutório. Com essas ressalvas, o mapa indica onde priorizar medidas de contenção da erosão. [objetivo 6]

## Trabalhos futuros

Os resultados indicam que o maior ganho está na estimativa do escoamento, antes de qualquer refinamento da fórmula de erosão. Mais postos pluviométricos na bacia, ou o uso de chuva estimada por radar ou satélite, permitiriam representar a variação da chuva entre os postos atuais; a calibração do número de curva ou da razão de abstração inicial com mais eventos, ou outra forma de gerar o escoamento, poderia corrigir o erro sistemático do SCS-CN, que superestima os eventos grandes e subestima os pequenos. Uma delimitação dos eventos por critério objetivo e documentado, e uma separação da vazão de base com parâmetros justificados pela geologia da bacia, reduziriam a incerteza do escoamento direto medido. Com mais eventos, seria possível fazer uma validação cruzada aninhada, em que também as escolhas do método de escoamento são refeitas em cada rodada.

Do lado do sedimento, a variação da carga por metro cúbico de escoamento entre os eventos, em especial no evento de 20/02/2020 e entre as estações de 2018/19 e 2019/20, pede rever a curva entre turbidez e concentração, sobretudo nas turbidezes altas, e acompanhar a sua validade ao longo do tempo. Para validar o mapa, seria necessário medir sedimento em sub-bacias ou mapear feições erosivas em campo; os valores de K e C por classe deveriam ser conferidos com medidas locais; e um mapa de uso de maior resolução permitiria separar, dentro da mancha urbana, parques, corpos d'água e solo exposto urbano, hoje considerados sem erosão. Por fim, a inclusão de um índice de conectividade de sedimentos, como em Hao et al. (2022), permitiria passar do mapa de erosão local a um mapa do sedimento que efetivamente chega à rede de drenagem.

---

## Notas para o usuário (não vão para o Doc)

- Números: todos de `proposta_cap4_30-10.md` (conferidos na revisão de 29/10); IC = valores originais (22,5% -> "22%"). "93% dos Cambissolos" = 92,9%. "46% da área e 83%": 29,0 + 12,7 + 3,9 = 45,6%; 37,4 + 24,2 + 20,9 = 82,5%.
- Saíram das conclusões antigas: "o modelo de dois componentes", "volume e carga incluem a vazão de base" (é dado, 3.2), "a espacialização não perde precisão / iguala" (mais forte que os dados), "16% da IC" (era a IC refeita).
- Frase da rotina "em Python": as bibliotecas e o QGIS estão descritos na 3.4; conferir com o usuário.
- O parágrafo do objetivo 6 tem dois "[a calcular no PC]"; se os números não forem calculados, cortar as duas frases.
- "Separação da vazão de base com parâmetros justificados pela geologia": liga ao achado do BFImax 0,70 contra o valor-guia 0,25 para rocha dura (2.4 e 4.6).
