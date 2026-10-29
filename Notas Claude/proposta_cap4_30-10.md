# Proposta do capítulo 4: RESULTADOS E DISCUSSÃO (30/10/2026)

Sessão na nuvem, sem acesso ao usuário nem ao Doc. **Nada foi aplicado no Doc.** Substitui o capítulo 5 antigo do Doc e as propostas `proposta_secao5.md` de 29/10. Estrutura pedida pelo Luis (S20 a S31; C21 a C31): 4.1 Escoamento superficial direto; 4.2 Resultados do Modelo Calculado de Erosão (MC); 4.3 Comparação do modelo calculado de erosão com outros modelos (sem subitens); 4.4 Mapas de erosão por evento de chuva; 4.5 Erosão média da bacia hidrográfica e áreas críticas; 4.6 Fontes de incerteza e limitações (proposta minha, decisão 1 do plano).

Forma (C21): prosa corrida de relatório técnico, sem rótulos em negrito no começo dos parágrafos e sem listas. As notas para o usuário ficam em blocos "> Nota" depois de cada seção e **não vão para o Doc**.

Fontes dos números: `TCC_Texto/tabelas/tab_volumes.md`, `tab_mc_mfm_eventos.md`, `tab_classes_uso.md`, `tab_classes_solo.md`, `TCC_Texto/figuras/escada_gargalo.csv`, `Scripts/_ic_original.py` (IC original), `relatorio_regeneracao_oficial_28-10.md`, `revisao_processo_29-10.md` (R1.3, R2.2, R2.3: recomputações independentes) e `proposta_secao5.md` (números conferidos na revisão). Não recalculei nada que dependa dos rasters; onde falta número, "[a calcular no PC: ...]". A IC aparece **só com os valores originais**.

Numeração: Tabelas 11 a 16 e Figuras 5 a 11 (ver `mapa_figuras_tabelas_30-10.md`).

---

# 4. RESULTADOS E DISCUSSÃO

## 4.1 Escoamento superficial direto

O primeiro passo do modelo é transformar a chuva em escoamento superficial direto, e é nele que se concentra a maior parte do erro do modelo calculado. A Tabela 11 e a Figura 5 comparam, evento a evento, o volume de escoamento direto calculado pelo SCS-CN com o medido no exutório (volume total menos a vazão de base, seção 3.2). No conjunto dos 17 eventos, os dois volumes quase coincidem: o SCS-CN soma 15,7 milhões de m³, contra 15,3 milhões de m³ medidos, um viés de +2,9%. Esse acerto no total resulta da escolha da condição de umidade e da razão de abstração inicial (seção 3.4.1.3), que foi feita justamente para aproximar os dois volumes, e não deve ser lido como bom desempenho evento a evento.

Tabela 11. Escoamento direto por evento: medido e calculado pelo SCS-CN.

| Evento | Chuva R (mm) | Medido Vdir (10³ m³) | SCS-CN (10³ m³) | SCS-CN / medido |
|---|---|---|---|---|
| 1 | 23,4 | 224 | 36 | 0,16 |
| 2 | 57,3 | 1.731 | 521 | 0,30 |
| 3 | 65,4 | 585 | 751 | 1,28 |
| 4 | 36,2 | 987 | 154 | 0,16 |
| 5 | 60,9 | 832 | 695 | 0,83 |
| 6 | 34,5 | 183 | 158 | 0,86 |
| 7 | 35,5 | 650 | 142 | 0,22 |
| 8 | 82,5 | 1.250 | 1.336 | 1,07 |
| 9 | 92,9 | 801 | 1.725 | 2,15 |
| 10 | 25,8 | 552 | 57 | 0,10 |
| 11 | 74,0 | 1.479 | 997 | 0,67 |
| 12 | 23,7 | 101 | 63 | 0,62 |
| 13 | 74,9 | 735 | 1.073 | 1,46 |
| 14 | 82,2 | 931 | 1.363 | 1,46 |
| 15 | 139,4 | 2.177 | 3.963 | 1,82 |
| 16 | 97,7 | 1.595 | 1.934 | 1,21 |
| 17 | 65,6 | 449 | 734 | 1,64 |
| Total | - | 15.263 | 15.702 | 1,03 |

Fonte: elaborado pelo autor.

[IMAGEM] Figura 5

Figura 5. Escoamento direto por evento: calculado pelo SCS-CN (CN-I, λ = 0,05, S convertido) contra o medido. A faixa indica o fator 2.

Fonte: elaborado pelo autor.

Evento a evento, o erro é grande. O erro percentual absoluto mediano do volume é de 46%, o médio é de 54%, e só 65% dos eventos (11 de 17) ficam dentro de fator 2. A razão entre o calculado e o medido vai de 0,10 no evento 10 a 2,15 no evento 9, e o NSE do volume é de -0,39: como previsão de cada evento, o SCS-CN erra mais do que erraria prevendo sempre a média dos eventos. Os erros se compensam no total porque têm um sentido sistemático. O método superestima o escoamento nos eventos de maior chuva (3, 8, 9 e 13 a 17) e subestima nos de menor chuva; nos eventos 1, 4, 7 e 10, o volume calculado é menos de um quarto do medido. Na curva do SCS-CN, o escoamento cresce mais que proporcionalmente com a chuva, porque a fração retida diminui à medida que a chuva aumenta. Nos eventos medidos, porém, a fração da chuva que escoa não depende da lâmina de chuva: a correlação entre o coeficiente de escoamento medido e a chuva do evento é de -0,01. A forma da curva do método não corresponde, portanto, à resposta desta bacia, e o acerto do total esconde um erro sistemático de forma.

Esse comportamento é coerente com a literatura de avaliação do método. Baert et al. (2026), em 154 eventos de uma bacia agrícola belga, encontraram NSE máximo de 0,13 para o volume de eventos com formulações fixas da razão de abstração inicial, e NSE negativo com a conversão de Woodward et al. (2003); Valle Junior, Rodrigues e Oliveira (2019) concluíram que o SCS-CN não foi adequado para a bacia do Guariroba, onde uma relação simples entre escoamento e chuva teve melhor desempenho. Parte do erro, no entanto, vem dos dados de entrada, e não do método. A chuva de cada pixel é interpolada a partir de apenas dois postos, um deles fora da bacia, de modo que núcleos de chuva intensa entre os postos não são representados. Os eventos foram delimitados manualmente sobre o hidrograma, e o escoamento direto medido depende da separação da vazão de base, que também é uma estimativa (seção 4.6). O erro de 46% é, portanto, o erro do conjunto formado pela chuva interpolada, pelo método e pela forma de medir o escoamento direto.

A Figura 6 mostra a chuva de cada evento interpolada nos pixels. O gradiente leste-oeste varia entre os eventos conforme o que cada posto registrou: a chuva é maior a oeste, perto do posto de Campo Limpo, em 13 dos 17 eventos, e maior a leste, perto do posto DBT5, nos eventos 1, 2, 4 e 17; no evento 12, o DBT5 não registrou chuva, e toda a variação vem de um só posto. Com dois postos, a chuva interpolada é sempre um gradiente suave entre os dois pontos, sem estrutura interna.

[IMAGEM] Figura 6

Figura 6. Chuva total de cada evento, interpolada pelo inverso do quadrado da distância a partir de dois postos.

Fonte: elaborado pelo autor.

O escoamento direto calculado em cada evento (Figura 7) acompanha a lâmina de chuva e o número de curva. Nos eventos de menor chuva (1, 4, 6, 7, 10 e 12), o escoamento fica abaixo de poucos milímetros em quase toda a bacia; no evento 15, o maior (139 mm), passa de 30 mm em boa parte da porção oeste e central. Em todos os eventos, os maiores valores aparecem no extremo oeste, perto do exutório, e na mancha urbana da porção centro-sul, onde o número de curva é mais alto (Figura 3), e os menores na cabeceira, a leste, que recebe menos chuva na maioria dos eventos e tem cobertura de mata. O padrão espacial do escoamento é, assim, o produto do gradiente da chuva e do mapa de número de curva; como só se mede a vazão no exutório, esse padrão não pôde ser verificado.

[IMAGEM] Figura 7

Figura 7. Escoamento direto calculado pelo SCS-CN (CN-I, λ = 0,05, S convertido) em cada evento.

Fonte: elaborado pelo autor.

> Notas. (1) C24, C26, S20. Figura 5 = `TCC_Texto/figuras/fig_volume_direto.png` (o gráfico calculado x medido que suponho ser o da reunião; pergunta no item I). Figura 6 = `mapa_04_chuva_eventos.png`; Figura 7 = `mapa_05_escoamento_eventos.png`. (2) Tabela 11 = colunas do SCS-CN que saem da Tabela 3, mais R da Tabela 2 (sem recálculo). (3) Números conferidos na revisão de 29/10 (R1.3, R2.1): viés +2,9%, erro mediano 46,3%, médio 53,9%, NSE -0,39, razão 0,10 a 2,15, superestima 8 eventos, r = -0,01. "11 de 17 em fator 2": 65% de 17 = 11; contei na Tabela 11: razões entre 0,5 e 2: eventos 3, 5, 6, 8, 11, 12, 13, 14, 15, 16, 17 = 11. Confere. (4) Descrição dos mapas feita olhando `mapa_05` nesta sessão: "abaixo de poucos milímetros" e "passa de 30 mm" são leitura visual da escala de cores (não medi). "Mancha urbana da porção centro-sul" é minha leitura (área azul em E 335 km, N 7.427 km); conferir no mapa de uso (Figura 2). (5) Baert: NSE máximo 0,13 e negativo com Woodward (-0,87), lote A, texto completo. Valle Junior: lote A, texto completo.

---

## 4.2 Resultados do Modelo Calculado de Erosão (MC)

O MC usa apenas a chuva dos dois postos. Com o coeficiente calibrado c = 0,0344 t por unidade de E_unit, o erro percentual absoluto mediano na validação cruzada foi de 81%, e só 6 dos 17 eventos (35%) ficaram dentro de fator 2; o NSE em escala logarítmica foi de -0,69 e a correlação de Spearman, de 0,59 (Tabela 13, na seção 4.3). A Tabela 12 mostra o sedimento simulado em cada evento, no ajuste e na validação cruzada, e a Figura 8 compara o simulado com o medido. Os resultados no ajuste e na validação cruzada são próximos, porque um único coeficiente, ajustado sobre 16 ou 17 eventos, muda pouco de uma rodada para outra: a perda de desempenho do MC não vem da calibração.

Tabela 12. Sedimento por evento (t): medido e simulado pelo MC e pelo MFM.

| Evento | Medido | MC, ajuste | MC, validação cruzada | Erro MC (%) | MFM, ajuste | MFM, validação cruzada | Erro MFM (%) |
|---|---|---|---|---|---|---|---|
| 1 | 266 | 74 | 69 | -74 | 357 | 364 | +37 |
| 2 | 2.040 | 990 | 946 | -54 | 2.437 | 2.464 | +21 |
| 3 | 928 | 2.556 | 2.723 | +193 | 1.249 | 1.272 | +37 |
| 4 | 1.380 | 424 | 394 | -71 | 2.146 | 2.206 | +60 |
| 5 | 1.372 | 2.034 | 2.085 | +52 | 1.609 | 1.625 | +18 |
| 6 | 199 | 463 | 488 | +146 | 352 | 365 | +84 |
| 7 | 1.317 | 269 | 244 | -82 | 940 | 920 | -30 |
| 8 | 2.109 | 3.202 | 3.287 | +56 | 1.921 | 1.909 | -9 |
| 9 | 1.155 | 3.396 | 3.633 | +215 | 929 | 917 | -21 |
| 10 | 847 | 100 | 88 | -90 | 785 | 782 | -8 |
| 11 | 1.822 | 1.406 | 1.383 | -24 | 1.410 | 1.387 | -24 |
| 12 | 211 | 205 | 204 | -3 | 226 | 227 | +8 |
| 13 | 1.196 | 2.919 | 3.086 | +158 | 1.235 | 1.238 | +3 |
| 14 | 1.731 | 3.702 | 3.882 | +124 | 1.562 | 1.552 | -10 |
| 15 | 3.829 | 10.361 | 11.026 | +188 | 3.422 | 3.399 | -11 |
| 16 | 1.736 | 3.036 | 3.144 | +81 | 1.580 | 1.571 | -10 |
| 17 | 1.710 | 2.157 | 2.188 | +28 | 804 | 767 | -55 |

Fonte: elaborado pelo autor. Erros da validação cruzada, (simulado - medido) / medido.

[IMAGEM] Figura 8

Figura 8. Sedimento simulado contra o medido nos 17 eventos: modelo simples com a chuva, MC e MFM (validação cruzada) e modelo concentrado da IC (valores originais, ajuste nos 17 eventos da IC). A faixa indica o fator 2; os números identificam os eventos.

Fonte: elaborado pelo autor; painel da IC com os valores de Vivarelli et al. (2025).

Os erros do MC são grandes nos dois sentidos. O modelo superestima 10 eventos e subestima 7: no evento 10, prevê 10% do sedimento medido, e no evento 9, 3,1 vezes o medido. Esses erros seguem os erros do escoamento direto da seção 4.1. Em 15 dos 17 eventos, o erro do sedimento tem o mesmo sinal do erro do escoamento: os eventos com escoamento muito subestimado (1, 2, 4, 7 e 10) têm o sedimento subestimado, e os de escoamento superestimado (3, 9, 13, 14 e 15) têm o sedimento superestimado. As exceções são os eventos 5 e 6, em que o escoamento calculado é próximo do medido (razões de 0,83 e 0,86) e o sedimento é superestimado, porque o coeficiente c, ajustado ao conjunto, compensa o viés médio dos outros eventos. A correlação entre o logaritmo do erro do sedimento e o logaritmo da razão entre o escoamento calculado e o medido é de 0,96: o erro do escoamento explica 91% da variância do erro do sedimento.

Esse resultado tem uma explicação direta na formulação. Como E_unit é proporcional a Q^1,12 (seção 3.4.3), um erro no escoamento passa ao sedimento ligeiramente ampliado: escoamento calculado com a metade do medido dá, em média, sedimento com cerca de 46% do valor que se obteria com o escoamento medido (0,5^1,12). Os fatores K, C e LS são os mesmos em todos os eventos e não mudam de um evento para outro; tudo o que diferencia um evento do outro no MC vem da chuva e da sua conversão em escoamento. Quando o SCS-CN erra a forma da relação entre chuva e escoamento, superestimando os eventos grandes e subestimando os pequenos, o MC herda esse erro e o amplia um pouco. É por isso que o MC fica pior que uma regra simples proporcional à chuva (seção 4.3): a regra simples também usa só a chuva, mas não passa pela curva do SCS-CN, que é justamente a parte que falha nesta bacia. Baert et al. (2026) chegaram a uma conclusão semelhante: com volume e pico previstos, a MUSLE teve NSE de validação cruzada próximo de zero para o sedimento (-0,03 e 0,01), e com o volume e o pico medidos chegou a 0,66; o termo de escoamento da equação amplifica os erros da estimativa hidrológica.

O resultado do MC não indica, portanto, que a fórmula de erosão ou a espacialização sejam inadequadas, mas que, nesta bacia e com estes dados, a cadeia que começa em dois postos de chuva e passa pelo SCS-CN com número de curva tabelado não reproduz o escoamento de cada evento. A seção 4.3 verifica o que acontece quando esse elo é substituído pelo escoamento medido.

> Notas. (1) C23, C25, S21. Tabela 12 = `tab_mc_mfm_eventos.md` com as colunas de erro no ajuste e a razão SCS-CN/medido retiradas (C22: colunas estreitas; a razão já está na Tabela 11). (2) Figura 8 = `fig_dispersao.png` (painel da IC já com valores originais; eixo y do painel da IC diz "IC: ajuste nos próprios 17 eventos"). Atenção: no painel da IC, a carga "medida" é a da planilha da IC, não a do TCC (diferem em vários eventos); a legenda proposta diz isso de forma curta. (3) Conferidos na revisão de 29/10: 10 superestimados e 7 subestimados; razões 0,10 e 3,15; sinal igual em 15 de 17, exceções 5 e 6; correlação 0,96 e 91% (§33 das notas; "não refeitos, dependem das somas de E_unit", mas o sinal foi refeito). (4) 0,5^1,12 = 0,46 (conta minha). (5) Baert: NSE -0,03 e 0,01 com previsão fora da amostra; 0,66 com Q e qp medidos (lote A).

---

## 4.3 Comparação do modelo calculado de erosão com outros modelos

A Tabela 13 reúne o desempenho de todos os modelos e a Figura 9 resume a comparação mais importante: o efeito de trocar o escoamento calculado pelo medido.

Tabela 13. Desempenho dos modelos (calibração em escala logarítmica; carga total de sedimentos).

| Modelo | Informação medida | Avaliação | Erro mediano (%) | Fator 2 (%) | NSE log | Spearman |
|---|---|---|---|---|---|---|
| Simples com a chuva, SY = c_R * R | chuva | validação cruzada | 41,9 | 82 | 0,53 | 0,63 |
| MC | chuva | validação cruzada | 81,1 | 35 | -0,69 | 0,59 |
| Simples com o escoamento, SY = c_V * Vdir | escoamento direto | validação cruzada | 15,9 | 94 | 0,85 | 0,90 |
| MFM | escoamento direto | validação cruzada | 20,6 | 94 | 0,84 | 0,83 |
| IC (VIVARELLI et al., 2025) | volume total e pico | ajuste (17 eventos da IC) | 22,5 | 100 | 0,91 | 0,93 |

Fonte: elaborado pelo autor; linha da IC calculada com os valores simulados e medidos de Vivarelli et al. (2025).

[IMAGEM] Figura 9

Figura 9. Erro percentual mediano e eventos dentro de fator 2 com o escoamento calculado a partir da chuva e com o escoamento forçado ao medido: MUSLE espacializada, modelo simples com a chuva e modelo concentrado da IC (valores originais).

Fonte: elaborado pelo autor.

O modelo simples com a chuva, em que o sedimento é proporcional à lâmina do evento, usa a mesma informação que o MC e teve erro mediano de 41,9%, com 82% dos eventos dentro de fator 2, contra 81,1% e 35% do MC. Evento a evento, o MC foi pior que a regra simples em 14 dos 17 eventos; a mediana da diferença entre os erros dos dois modelos é de +32,6 pontos percentuais, com intervalo de confiança de 95% de +3,1 a +117,5 pontos, e o teste de Wilcoxon pareado dá p = 0,02. A diferença não se explica pelo acaso: com a mesma chuva, a passagem pelo SCS-CN piora a estimativa. A regra simples, por outro lado, não é um bom modelo, apenas um modelo menos errado: ainda erra 42% na mediana, superestima os eventos pequenos (o evento 6 em 3,7 vezes) e não informa onde o sedimento é produzido.

O Modelo Forçado ao Medido mantém a fórmula de erosão, os fatores K, C e LS e o padrão espacial do MC e troca apenas o volume de escoamento direto pelo medido. Com essa troca, o erro mediano cai de 81,1% para 20,6%, a fração dentro de fator 2 sobe de 35% para 94%, o NSE em log passa de -0,69 para 0,84 e o Spearman, de 0,59 para 0,83. Só o evento 17 fica fora do fator 2 (-55%). Como nada mais muda entre as duas versões, a diferença mostra que o elo que limita o MC é a conversão da chuva em escoamento.

Esse resultado precisa, porém, ser lido com uma ressalva importante. A carga medida em cada evento é a soma, hora a hora, do produto da vazão pela concentração de sedimentos, isto é, o volume escoado multiplicado por uma concentração média. Entre os 17 eventos, o volume varia muito mais que a concentração: a variância do logaritmo do volume total é de 0,66, contra 0,08 da variância do logaritmo da concentração média, e o logaritmo do volume sozinho explica 88% da variância do logaritmo da carga. Qualquer modelo que receba o volume medido acerta, por construção, a ordem de grandeza da carga. O modelo simples com o escoamento direto medido, sem MUSLE, teve erro mediano de 15,9%, 94% dos eventos dentro de fator 2 e NSE em log de 0,85, números próximos aos do MFM. A mediana da diferença entre os erros do MFM e da regra simples é de +1,6 pontos, com intervalo de confiança de 95% de -5,5 a +10,4 pontos (Wilcoxon, p = 0,52), e o MFM foi melhor em 6 dos 17 eventos: com 17 eventos, os dois não se distinguem. Com o escoamento medido, a MUSLE espacializada não melhora a estimativa do sedimento total do evento em relação a uma regra proporcional ao volume. O bom desempenho do MFM mostra o peso do volume medido; não é uma validação da fórmula de erosão nem do mapa.

Há também um padrão nos erros do MFM que vem da própria fórmula. A MUSLE faz o sedimento crescer com a potência 1,12 do escoamento, enquanto, nesta bacia, a carga medida cresce com a potência 0,94 do volume de escoamento direto. Por isso, o MFM tende a superestimar os eventos pequenos (o evento 6 em 84%, o 1 em 37%) e a subestimar os grandes (o 15 em 11%). O expoente 0,56 de Williams, ajustado em outras bacias e mantido aqui, é uma das razões pelas quais a MUSLE não supera a regra linear com o volume.

A formulação concentrada da Iniciação Científica (VIVARELLI et al., 2025) usa o volume total e a vazão de pico medidos no hidrograma do evento, com os fatores médios da bacia e coeficientes ajustados aos próprios 17 eventos. Com os valores originais, ela tem erro percentual absoluto mediano de 22,5%, todos os eventos dentro de fator 2, NSE em log de 0,91, NSE linear de 0,83 e Spearman de 0,93; o erro médio com sinal é de +4,2% (simulado acima do medido), com erros de -37% a +60%. Esses números são da mesma ordem que os do MFM (20,6% e 94%), mas a comparação é só indicativa, por três motivos. Os números da IC são de ajuste, sem validação cruzada, e com dois parâmetros livres, contra um do MFM; a lista de eventos da IC tem o evento de 24/11/2018 no lugar do de 17/12/2018; e a carga medida atribuída a vários eventos difere da usada neste trabalho, como nos eventos de 30/12/2019 (129 t na IC, 211 t aqui) e de 20/02/2020 (1.456 t na IC, 1.710 t aqui). Por isso não se fez teste pareado entre os dois. O que a comparação permite dizer é que a espacialização, quando recebe o escoamento medido, chega a um erro da mesma ordem que o da formulação concentrada, e acrescenta o mapa; não permite dizer que um seja melhor que o outro. A IC, assim como o MFM, não é uma previsão: depende do hidrograma do próprio evento, medido no mesmo lugar e ao mesmo tempo que a carga.

O evento 17 (20/02/2020) é o mais difícil para todos os modelos que usam o escoamento medido: o MFM o subestima em 55%, a regra com o escoamento direto em 61% e a IC em 47%. A sua carga por metro cúbico de escoamento direto é de 3.806 mg/L, contra 1.085 a 2.088 mg/L nos outros 16 eventos. Uma explicação possível é a curva de turbidez e concentração operar fora da faixa em que foi calibrada, já que as maiores concentrações da série correspondem a turbidez muito acima de 250 NTU, valor em que a regressão por partes de Murillo-Bermúdez et al. (2023) muda de trecho; outra é uma fonte de sedimento que o modelo não representa, como uma obra ou um deslizamento. O evento foi mantido, porque não há base para excluí-lo; sem ele, o MFM passaria a ter erro mediano de 15,3% e todos os eventos dentro de fator 2, e as conclusões desta seção não mudariam. O mesmo vale para o evento 15, o maior, que domina o NSE linear: sem ele, o MFM mantém 20,6% de erro mediano e 94% dentro de fator 2, e o MC continua pior que a regra com a chuva em todos os subconjuntos testados.

Há ainda um contraste entre as duas estações chuvosas. O MFM superestima todos os eventos de 2018/19 (eventos 1 a 6, de +18% a +84%) e subestima os de 2020 (eventos 14 a 17, de -10% a -55%). A carga por metro cúbico de escoamento direto é, em média, maior nos eventos de 2019/20 (cerca de 1.700 mg/L sem o evento 17) do que nos de 2018/19 (cerca de 1.480 mg/L). A causa não foi identificada: pode ser uma mudança na disponibilidade de sedimento na bacia, no sensor de turbidez ou na relação entre turbidez e concentração ao longo do tempo. Esse tipo de variação não é representado por um modelo com um único coeficiente c para todos os eventos.

Em resumo, a comparação mostra uma hierarquia clara entre o escoamento calculado e o medido, e nenhuma diferença mensurável entre as formulações que recebem o escoamento medido. O limite do modelo calculado está na transformação da chuva em escoamento; com o escoamento medido, a contribuição própria da espacialização não está no total do evento, mas no mapa, que é analisado nas seções 4.4 e 4.5.

> Notas. (1) S22, C28, C29, S31: sem subitens; nada sobre modelo de dois componentes. (2) Tabela 13: números do TCC conferidos na revisão de 29/10 (R1.3); IC = valores originais (`_ic_original.py`, igual ao `escada_gargalo.csv`: 22,46%; 100%; 0,91; 0,93). **Nada da "IC refeita".** (3) Bootstrap e Wilcoxon: revisão de 29/10, R2.2 (MC x chuva: +32,6 [+3,1; +117,5], 3 de 17 melhor → pior em 14, p 0,020; MFM x Vdir: +1,6 [-5,5; +10,4], p 0,52, 6 de 17). A comparação pareada MFM x IC foi retirada (era com a IC refeita). (4) Variâncias 0,66/0,08 e 88%: revisão R1.2, achado 8 (usa o volume total TR; com Vdir, 87%). (5) Expoentes 1,12 x 0,94: revisão R2.3. (6) Evento 17: 3.806 mg/L e faixa 1.085 a 2.088 (proposta 5.7, conferida R2.1); "turbidez muito acima de 250 NTU": a concentração máxima de 4.602 mg/L corresponde a cerca de 9.000 NTU pela lei de potência (pontos da reunião); a regressão por partes com quebra em 250 NTU é do **resumo** de Murillo-Bermúdez et al. (2023) (só resumo lido). Qual curva foi usada é pergunta ao Luis; se ele disser que foi a lei de potência de 2022, trocar o fim da frase por "acima da faixa de turbidez das amostras usadas na calibração da curva (MURILLO-BERMÚDEZ; MARTIM, 2022)" **só se** essa faixa estiver no artigo de 2022 (não conferido nesta sessão). (7) Sensibilidade sem 15 e 17: revisão R2.3. (8) Contraste das estações: revisão achado 15 (versão "sem o 17"). "2020" para os eventos 14 a 17 (todos em 2020). (9) Figura 9 = `escada_gargalo.png`, que hoje diz "Água calculada/forçada": **regerar** com "Escoamento calculado/forçado" (item G). (10) O modelo SY = c * TR (17,6%) não entra (não descrito no método); a frase dos 88% usa o volume total como informação, não como modelo.

---

## 4.4 Mapas de erosão por evento de chuva

A Figura 10 mostra a erosão produzida em cada pixel em cada evento pelo MC, com a mesma escala de cores em todos os eventos. Os pontos de maior erosão são os mesmos em todos os eventos e mudam de intensidade, mas não de lugar: o padrão espacial é dado sobretudo pelos fatores fixos K, C e LS, enquanto a chuva e o escoamento definem a intensidade geral do evento e modulam o padrão no sentido leste-oeste. Nos eventos de menor chuva (1, 4, 6, 7, 10 e 12), a erosão é baixa em quase toda a bacia; nos eventos 9, 14, 15 e 16, os de maior lâmina, as mesmas manchas da porção central e oeste se intensificam. A cabeceira, a leste, produz pouca erosão em todos os eventos, porque recebe menos chuva na maior parte deles, tem número de curva mais baixo e é coberta sobretudo por mata nativa, com o menor fator C entre as classes com erosão.

[IMAGEM] Figura 10

Figura 10. Erosão produzida em cada pixel em cada evento (MC).

Fonte: elaborado pelo autor.

Como o MFM multiplica o escoamento de todos os pixels de um evento pelo mesmo fator, os seus mapas por evento têm o mesmo padrão dos do MC, com outra intensidade: no MFM, os eventos de escoamento subestimado pelo SCS-CN (por exemplo, 1, 4, 7 e 10) ficam mais intensos, e os superestimados (por exemplo, 9 e 15), menos. Os mapas por evento mostram, assim, onde a erosão se concentra em cada evento, mas a diferença entre eventos deve ser lida com a ressalva da seção 4.1: a intensidade de cada mapa depende do escoamento calculado, que erra 46% na mediana.

> Notas. (1) S24 a S27. Figura 10 = `mapa_06_sedimento_eventos.png`. **Não abri o `mapa_06` nesta sessão**: a frase "eventos 9, 14, 15 e 16 se intensificam" é dedução dos maiores volumes do SCS-CN (Tabela 11: 15, 16, 9, 14 em ordem) e do padrão do `mapa_05` e do `mapa_07`, que abri. O usuário deve olhar a figura antes de manter. (2) O rótulo interno do `mapa_06` ainda diz "Sedimento das encostas" (relatório de 28/10): regerar ou aceitar. (3) "mata nativa com o menor C entre as classes com erosão": C = 0,015 (Tabela 6), confere. (4) O mapa de erosão por evento do MFM não existe como figura; o parágrafo diz só o que decorre da formulação.

---

## 4.5 Erosão média da bacia hidrográfica e áreas críticas

A Figura 11 mostra a erosão média dos 17 eventos em cada pixel e as áreas críticas, definidas como os 5% dos pixels com maior erosão média, para o MC e o MFM. Os dois mapas são muito parecidos: a correlação entre eles é de 0,98, e 94,2% dos pixels críticos coincidem. Essa coincidência era esperada e não é uma validação, porque os dois modelos distribuem o escoamento pelo mesmo padrão do SCS-CN e usam os mesmos K, C e LS; ela indica apenas que o padrão espacial pouco depende de como se estima o volume de cada evento.

[IMAGEM] Figura 11

Figura 11. Erosão média dos 17 eventos e áreas críticas (5% dos pixels de maior erosão média), para o MC e o MFM.

Fonte: elaborado pelo autor.

As áreas críticas formam manchas na porção central e oeste da bacia, entre cerca de 3 e 12 km do exutório, faixas estreitas na borda sul e poucas manchas isoladas na porção centro-sul; a cabeceira, a leste, quase não tem pixels críticos. A contribuição para a erosão é muito desigual entre os usos do solo (Tabela 14). O campo ocupa 29,0% da área e responde por 37,4% da erosão média do MC; a silvicultura ocupa 12,7% e responde por 24,2%; a lavoura temporária ocupa 3,9% e responde por 20,9%; o solo exposto ocupa 0,5% e responde por 8,2%; e a mata nativa, que ocupa 39,6% da área, responde por 7,5%. Por unidade de área, a lavoura temporária produz cerca de cinco vezes a média da bacia, e o solo exposto, cerca de 18 vezes. A mineração, com poucos pixels e C = 1 adotado, responde por 1,8%. Campo, silvicultura e lavoura temporária, que somam 46% da área, respondem por 83% da erosão média. Entre os solos (Tabela 15), 92,9% da erosão vem dos Cambissolos Háplicos, que têm o maior K (0,0475) e ocupam 68,6% da área; os Argissolos Vermelho-Amarelos, com 17,6% da área e K de 0,0351, respondem por 7,1%. As porcentagens do MFM são quase iguais às do MC.

Tabela 14. Contribuição de cada classe de uso para a erosão média (MC e MFM).

| Classe de uso | Área (%) | Erosão, MC (%) | Erosão, MFM (%) | Erosão por área, MC (média da bacia = 100) |
|---|---|---|---|---|
| Mata Nativa | 39,6 | 7,5 | 6,7 | 19 |
| Campo | 29,0 | 37,4 | 37,4 | 129 |
| Área Urbanizada | 14,1 | 0,0 | 0,0 | 0 |
| Silvicultura | 12,7 | 24,2 | 23,0 | 191 |
| Lavoura Temporária | 3,9 | 20,9 | 20,0 | 530 |
| Solo exposto | 0,5 | 8,2 | 10,8 | 1.772 |
| Corpos D'Água | 0,2 | 0,0 | 0,0 | 0 |
| Mineração | 0,0 | 1,8 | 2,1 | 3.784 |
| Afloramento Rochoso | 0,0 | 0,0 | 0,0 | 66 |

Fonte: elaborado pelo autor.

Tabela 15. Contribuição de cada classe de solo para a erosão média (MC e MFM).

| Classe de solo | Área (%) | Erosão, MC (%) | Erosão, MFM (%) | Erosão por área, MC (média da bacia = 100) |
|---|---|---|---|---|
| Cambissolos Háplicos | 68,6 | 92,9 | 92,7 | 135 |
| Argissolos Vermelho-Amarelos | 17,6 | 7,1 | 7,3 | 40 |
| Área Urbana | 13,7 | 0,0 | 0,0 | 0 |
| Afloramento Rochoso | 0,1 | 0,0 | 0,0 | 7 |
| Neossolos Litólicos | 0,0 | 0,0 | 0,0 | 0 |

Fonte: elaborado pelo autor.

A declividade é o terceiro fator que organiza o mapa. Pela formulação de Moore e Burch (1986), o fator LS cresce com a potência 1,3 do seno da declividade, de modo que pixels íngremes podem ter LS dezenas de vezes maior que pixels quase planos sob o mesmo uso e o mesmo solo. A Tabela 16 mostra a contribuição de cada classe de declividade: [a calcular no PC: área (%) e erosão média do MC e do MFM (%) por classe de declividade de 0 a 3%, 3 a 8%, 8 a 20%, 20 a 45%, 45 a 75% e acima de 75%]. [Texto a completar com o resultado, no modelo: "As classes de 20 a 45% e acima de 45% ocupam X% da área e respondem por Y% da erosão; as áreas planas, perto da rede de drenagem e na mancha urbana, quase não contribuem."] Nos pixels críticos, a combinação mais frequente é [a calcular no PC: cruzamento de uso, solo e classe de declividade nos 5% de pixels críticos; ex.: campo ou silvicultura sobre Cambissolo em declividade acima de 20%].

Tabela 16. Contribuição de cada classe de declividade para a erosão média (MC e MFM).

| Declividade (%) | Área (%) | Erosão, MC (%) | Erosão, MFM (%) |
|---|---|---|---|
| 0 a 3 | [PC] | [PC] | [PC] |
| 3 a 8 | [PC] | [PC] | [PC] |
| 8 a 20 | [PC] | [PC] | [PC] |
| 20 a 45 | [PC] | [PC] | [PC] |
| 45 a 75 | [PC] | [PC] | [PC] |
| acima de 75 | [PC] | [PC] | [PC] |

Fonte: elaborado pelo autor.

Para medir quanto do padrão espacial vem dos fatores fixos e quanto vem do escoamento (seção 3.4.9), calculou-se o R² entre a erosão média de cada pixel e o produto K * LS * C. Em escala logarítmica, o produto K * LS * C explica [a calcular no PC: R² de ln Ē_k em ln(K*LS*C)] da variação espacial da erosão média entre os pixels com erosão, e o termo de escoamento, que reúne a chuva e o número de curva, explica [a calcular no PC: R² de ln Ē_k em ln G_k]; pela partição da seção 3.4.9, [X]% da variação espacial pode ser atribuída aos fatores fixos e [100 - X]% ao escoamento. Em escala linear, a correlação entre o mapa do MC e o produto K * LS * C é de 0,77 (0,76 no MFM), o que corresponde a um R² de cerca de 0,59 [confirmar no PC]: cerca de 60% da variação espacial da erosão média acompanha os fatores fixos, e o restante vem principalmente da distribuição do escoamento, ou seja, do gradiente de chuva entre os postos e do número de curva. Na prática, isso quer dizer que o mapa de áreas críticas não é apenas um mapa de K * LS * C: pixels com o mesmo produto de fatores têm erosão maior no oeste da bacia, onde chove mais na maioria dos eventos e o número de curva é mais alto. Como a chuva vem de dois postos e o número de curva de uma base nacional, essa parcela do padrão é a menos confiável do mapa.

O mapa serve, assim, para indicar onde priorizar medidas de contenção da erosão em termos relativos: as manchas de campo, silvicultura e lavoura temporária sobre Cambissolos, nas encostas mais íngremes da porção central e oeste, e os poucos pixels de solo exposto e mineração, que têm a maior erosão por unidade de área. Em uma bacia de abastecimento como a do alto Jundiaí, essas manchas são os alvos naturais de práticas conservacionistas, de recomposição da cobertura em áreas de campo degradado e de controle da erosão em áreas de solo exposto. Três ressalvas limitam esse uso. Primeiro, os valores de K e C por classe vêm da IC; na conferência das fontes, os valores do campo (C = 0,050) e da lavoura temporária (C = 0,212) não puderam ser confirmados nas obras citadas, e o K do Cambissolo é o de uma amostra individual. Isso não altera o sedimento total de cada evento, porque o coeficiente c absorve a escala, mas altera o peso relativo das classes no mapa. Segundo, o mapa mostra onde a erosão local é produzida, e não onde o sedimento chega à rede de drenagem, porque o modelo não tem conectividade nem roteamento (seção 3.4.4). Terceiro, o mapa não pôde ser validado no espaço, porque só há medição de sedimento no exutório.

A área urbana tem erosão nula por hipótese do modelo: o mapa de uso classifica toda a mancha urbana como superfície impermeável (C = 0), e os pixels sem classe de solo receberam K = 0. Na realidade, áreas urbanas produzem sedimento em obras, vias não pavimentadas, loteamentos em implantação e terrenos de solo exposto, que podem ser fontes importantes em eventos de chuva intensa. Com um mapa de uso de maior resolução, seria possível separar, dentro da mancha urbana, os parques e áreas verdes (que se comportariam como mata ou silvicultura), os corpos d'água e o solo exposto urbano, e atribuir a cada um o seu fator C. Como a área urbanizada ocupa 14,1% da bacia e está concentrada perto do exutório, essa simplificação pode subestimar a contribuição urbana e deslocar para as áreas rurais uma parte do sedimento que o coeficiente c atribui a elas.

> Notas. (1) S28 a S30, C31, orientações da reunião (uso do mapa, área urbana). (2) Tabelas 14 e 15 = `tab_classes_uso.md` e `tab_classes_solo.md`, com as colunas "kg/pixel" retiradas (C22: colunas estreitas; os kg/pixel mudaram muito entre modelos e confundem) e a última coluna renomeada "Erosão por área (média da bacia = 100)", que é a "Contribuição / área (%)" do arquivo. Se o usuário quiser os kg/pixel, voltar com eles numa tabela separada. (3) Contas conferidas na revisão (R2.1): 37,4/24,2/20,9/8,2/7,5; 530 e 1.772; 92,9; 45,6% da área e 82,5% (arredondados 46% e 83%). (4) "entre cerca de 3 e 12 km do exutório": leitura visual minha do `mapa_07` (exutório no extremo oeste, E ~319 km; manchas entre E ~322 e ~331 km). Conferir. (5) Declividade e R² log: **todos a calcular no PC** (script no roteiro K). Pearson 0,77/0,76: relatório de 28/10; R² 0,59 = 0,77² (conta minha; o R² de uma regressão linear simples é o quadrado de Pearson, mas confirmar no PC). Frase "pixels com o mesmo produto de fatores têm erosão maior no oeste" decorre do gradiente de chuva e do CN (Figuras 6 e 7); é qualitativa. (6) K e C sem fonte confirmada: lote D. (7) "Bacia de abastecimento": a 3.2 diz que a turbidez é medida na estação de tratamento da SABESP; a frase não traz número. (8) Moore e Burch: só resumo; o expoente 1,3 está na equação usada (3.4.1.2). (9) A frase sobre "concentrada perto do exutório" é leitura do mapa de uso (Figura 2) que **não abri** nesta sessão; conferir antes de manter (no `mapa_07`, a mancha sem erosão grande fica no centro-sul, E ~333 a 336 km).

---

## 4.6 Fontes de incerteza e limitações

Os resultados das seções anteriores dependem de uma cadeia de etapas, e cada uma acrescenta incerteza. Esta seção as reúne na ordem em que entram no modelo, da medição ao mapa.

A primeira fonte é a delimitação dos eventos. As janelas dos 17 eventos foram definidas manualmente, observando o hidrograma, com início e fim escolhidos pelo analista. Essa escolha afeta ao mesmo tempo a chuva atribuída ao evento, o volume escoado e a carga medida: chuva que cai antes do início da janela ou depois do fim fica de fora, e uma recessão longa aumenta o volume e a carga sem chuva correspondente. As durações das janelas usadas aqui diferem de 1 a 2 horas das de Murillo-Bermúdez e Martim (2022) para os mesmos eventos, e um evento da lista original (24/11/2018) não foi usado. Nenhum dos trabalhos consultados trata da incerteza da delimitação manual de eventos; ela é, portanto, uma limitação própria deste trabalho, sem estimativa quantitativa.

A segunda é a chuva. Com dois postos, um deles fora da bacia, a chuva de cada pixel é um gradiente suave entre dois pontos, que não representa núcleos de chuva convectiva entre eles. A lâmina do evento R e a intensidade RI vêm de fontes diferentes: R é uma média ponderada dos dois postos, e RI é a maior intensidade entre eles; por isso, nos eventos 1 e 12, a razão RI/R passa de 1. No evento 12, o posto DBT5 não registrou chuva, e toda a chuva da bacia vem de um só posto. Hao et al. (2022) aplicaram a MUSLE espacializada em bacias de 1.310 a 8.973 km² com vários pluviômetros por bacia; aqui a densidade de postos é muito menor que a das aplicações em que o método foi desenvolvido.

A terceira é o próprio método SCS-CN. O número de curva vem de uma base nacional que cruza o uso do MapBiomas de 2022 com um mapa de solos na escala 1:250.000, e a condição de umidade e a razão de abstração inicial são as mesmas para todos os eventos. A razão λ = 0,05 com a conversão de Woodward et al. (2003) foi a configuração escolhida pelo volume desta bacia, mas não é consenso na literatura. Baert et al. (2026) obtiveram NSE de volume de -0,87 com a fórmula de Woodward e concluíram que um λ fixo mais baixo não resolve a incerteza do início do escoamento; Brandão et al. (2025), em 3.578 bacias, encontraram desempenho médio melhor com λ = 0,05, mas associaram clima úmido e mais pastagem a valores mais altos da razão, e o alto Jundiaí tem clima úmido e 29% de campo. A própria conversão é extrapolada em 8,4% dos pixels (CN-I abaixo de 35) e nos eventos 1 e 12, com menos de 25,4 mm de chuva. Essas escolhas foram feitas observando os mesmos 17 eventos usados na avaliação, e a validação cruzada refaz apenas o coeficiente c (seção 3.4.6).

A quarta é a separação da vazão de base. O escoamento direto medido, que alimenta o MFM e a regra simples com o escoamento, depende da série de vazão de base, reproduzida pelo filtro de Eckhardt com BFImax = 0,70. O BFImax não é mensurável e é escolhido pelo usuário do filtro, e o valor que reproduz a série (0,70) é bem maior que o sugerido por Eckhardt (2005) para rios perenes com aquífero em rocha dura, 0,25 (ECKHARDT, 2012), situação mais próxima da sub-bacia, dominada pelo embasamento cristalino com aquífero fraturado (seção 3.1). A série fornecida pode, assim, atribuir à vazão de base uma parte do volume que seria escoamento direto; o método e os parâmetros com que ela foi gerada não estão documentados na fonte. Com outras separações, o MFM fica entre 15,1% e 21,9% de erro mediano, mantendo 94% dos eventos dentro de fator 2. A hipótese de que a vazão de base só transporta o sedimento também é uma escolha: se a parcela da carga transportada pela vazão de base fosse descontada, admitindo nela a mesma concentração da mistura em cada hora, a carga atribuída ao escoamento direto seria cerca de 66% da total, e o MFM teria erro mediano de 12,9%, sem mudar as conclusões (o MC continua pior que a regra com a chuva, e os modelos com o escoamento medido continuam próximos entre si).

A quinta é a medição do sedimento. A carga medida não é uma medida direta: a concentração de sedimentos em suspensão é estimada a partir da turbidez por uma curva de calibração (seção 2.5). As maiores concentrações da série correspondem a turbidez muito acima da faixa em que a relação muda de trecho na regressão de Murillo-Bermúdez et al. (2023), e é nesses momentos, os picos dos maiores eventos, que se concentra a maior parte da carga. O evento 17, com concentração média por metro cúbico de escoamento direto quase o dobro da dos demais, e o contraste entre as estações de 2018/19 e 2019/20 (seção 4.3) podem estar ligados a essa etapa.

A sexta é a formulação de erosão. A equação de Williams foi aplicada ao pixel com os coeficientes originais, ajustados em bacias, e o expoente 1,12 resultante é maior que a relação observada nesta bacia entre carga e volume (0,94). O coeficiente c é único para toda a bacia e para todos os eventos, e faz o papel de uma conectividade média; Hao et al. (2022) calibraram um índice de conectividade por pixel, que este trabalho não usou. O alvo da calibração é a carga total, que inclui sedimento do canal e das margens, que o modelo não representa.

A sétima é o mapa. Os fatores K e C por classe vêm da IC, com fontes não confirmadas para o campo, a lavoura temporária e o Cambissolo; a área urbana tem erosão nula por hipótese; o padrão espacial do escoamento vem de dois postos e de uma base nacional de número de curva; e não há medição de sedimento dentro da bacia para validar o mapa. O mapa deve ser lido como uma distribuição relativa da erosão local sob os valores adotados.

Por fim, com 17 eventos, as diferenças de 2 a 5 pontos no erro mediano entre modelos não são interpretáveis, e os intervalos de confiança das comparações são largos. As conclusões que resistem a essas incertezas são as qualitativas: o modelo calculado é pior que uma regra simples com a chuva, a diferença entre o escoamento calculado e o medido domina o resultado, e os modelos que recebem o escoamento medido não se distinguem entre si.

> Notas. (1) Orientações do Luis ditadas em 29/10 ("forçar bastante" na defasagem: delimitação manual, dois postos, SCS-CN) e `pontos_discussao_e_reuniao_29-10.md`. (2) "Durações diferem 1 a 2 h" e "CSSmax 4.602 mg/L ~ 9.000 NTU": pontos da reunião (lote C, artigo de 2022 texto completo). A frase sobre a regressão por partes depende de **só resumo** de 2023. (3) Hao: bacias de 1.310 a 8.973 km² e vários pluviômetros (lote A). **Não citei obras sobre densidade de postos, IDW, delimitação de eventos, turbidez de alta frequência e erosão urbana**: o lote E não pôde ser lido (rede bloqueada). Onde caberiam: densidade de postos (2º parágrafo), delimitação (1º), turbidez (5º), erosão urbana (4.5, último parágrafo). (4) Sensibilidade da base (15,1% a 21,9%; 12,9%; 66%): checagens de 27/10, conferidas na revisão (R2.1); "sem mudar as conclusões" na forma corrigida pela revisão (achado 22). (5) BFImax 0,25 para rocha dura: Eckhardt (2012), texto completo (lote A), ver 2.4; a comparação com a geologia da 3.1 é minha. Pergunta ao Luis no item I (como a série foi gerada; 0,70 ou 0,58). Brandão: lote A; usei "valores mais altos da razão" para não escrever λ = 0,20 (regra). (6) "a maior parte da carga se concentra nos picos": afirmação geral, não medida aqui; se o usuário quiser, calcular no PC a fração da carga nas horas com turbidez acima de 250 NTU; senão, cortar o trecho "e é nesses momentos ... carga".
