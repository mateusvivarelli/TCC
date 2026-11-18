# Perguntas prováveis da banca: especialista em hidrologia e sedimentos

Leitura feita como membro de banca com doutorado na área, depois de ler o texto final do TCC e assistir à apresentação (slides 1 a 36; 35 e 36 são de apoio).

---

## 1. Perguntas prováveis, da mais perigosa para a menos

### P1. "Se, com o escoamento medido, a MUSLE espacializada não é melhor que a regra SY = c·Vdir, o que sustenta o mapa de áreas críticas? Como você sabe que as áreas críticas estão no lugar certo?"
- **Motivação:** slides 24, 26, 27 e 30; seções 4.3, 4.5 e 5. O próprio trabalho conclui que não foi possível isolar o papel da fórmula e dos fatores K, LS e C, mas o título e a conclusão apresentam o mapa como o principal produto.
- **Resposta sugerida:** "Os dados do exutório só testam a soma da bacia. Qualquer distribuição espacial com o mesmo total teria o mesmo desempenho. Por isso o mapa não foi validado e eu não afirmo que ele está certo: ele mostra, em termos relativos, onde a erosão seria maior com os fatores K, LS e C da literatura e com o escoamento do SCS-CN. Ele serve para indicar onde verificar primeiro, e não como diagnóstico confirmado. A forma de testá-lo é medir sedimento em sub-bacias e verificar as manchas em campo ou em imagens." (Base: 4.3, último parágrafo; 4.5, ressalvas; 4.6, sétima fonte; 5, primeira frente.)
- **Risco:** alto. Esta é a pergunta central do trabalho. Não tente defender que o mapa está validado.

### P2. "No slide 35 você diz que 13 de 17 eventos têm laço horário. No texto (2.5), citando Murillo-Bermúdez e Martim (2022), são 13 em forma de oito e 4 horários. Qual dos dois está certo?"
- **Motivação:** slide 35 ("13 de 17 eventos com laço horário (planilha de eventos)") contra a seção 2.5. O orientador, que está na banca, é autor do artigo citado.
- **Resposta sugerida:** o texto e os slides não batem, e não há como defender os dois ao mesmo tempo. Antes da defesa, corrija o slide 35 para a classificação publicada (13 em oito e 4 horários) ou explique de onde vem a classificação da planilha e por que ela difere da publicada. Se a pergunta surgir mesmo assim: "A classificação publicada é a do artigo: 13 em oito e 4 horários. O número do slide veio da planilha de eventos e usa outro critério. Nas conclusões vale o que está no texto."
- **Risco:** alto, porque o autor do artigo está na sala.

### P3. "Você usou CN-I, a condição seca, em todos os eventos, que são de novembro a fevereiro, na estação chuvosa. Os eventos 13 e 14, e também 15 e 16, vêm um logo depois do outro. Que sentido físico tem isso?"
- **Motivação:** slide 16 (CN-II 81,0 → CN-I 64,2); seções 3.4.1.3 e 4.6; Tabela 2 (evento 15 vai até 09/02 01h e o evento 16 começa em 09/02 14h).
- **Resposta sugerida:** "Nenhum sentido físico de umidade antecedente. O CN-I, junto com λ = 0,05 e a conversão de Woodward, foi uma configuração escolhida porque aproxima o volume total de escoamento direto dos 17 eventos (viés de +3%). O texto diz isso na seção 3.4.1.3: é uma condição única, escolhida pelo volume, e não uma medida da umidade de cada evento. O CN tabelado da base nacional gera escoamento demais nesta bacia, e o CN-I funciona como uma correção de escala. O passo correto seria definir a umidade antecedente de cada evento pela chuva dos 5 dias anteriores e testar as alternativas com validação cruzada aninhada (seção 5)."
- **Risco:** alto. Admita logo que é calibração disfarçada; não tente justificar pela umidade do solo.

### P4. "O seu escoamento direto 'medido' depende do filtro de Eckhardt com BFImax = 0,70. O próprio Eckhardt sugere 0,25 para rio perene em rocha cristalina, que é o caso. No hidrograma do evento 11, a vazão de base sobe de cerca de 1 para 5 m³/s durante o evento. E se o BFImax fosse 0,25?"
- **Motivação:** slide 13 (curva tracejada da vazão de base) e slide 31 (item 4); seções 2.4, 3.2 e 4.6. A vazão de base fica com 47% do volume dos eventos.
- **Resposta sugerida:** "A série veio junto com os dados e eu só a reproduzi. Não fiz análise de sensibilidade. Com um BFImax menor, o escoamento direto aumentaria em todos os eventos. Isso mudaria a configuração do SCS-CN escolhida para acertar o volume, que precisaria gerar mais escoamento, e também mudaria o MFM e a regra com o escoamento direto, embora essas duas versões devam mudar de forma parecida, porque as duas usam o mesmo Vdir. O resultado com o volume total, que inclui a vazão de base e explica 88% da carga, não depende do filtro. É uma limitação, registrada na seção 4.6."
- **Risco:** alto. Cuidado: a escolha do CN-I depende do Vdir, que depende do BFImax. Mostre que você entende essa cadeia.

### P5. "Você diz que c 'faz o papel de uma taxa de transferência de sedimentos'. A SDR não tem unidade e fica entre 0 e 1. O seu c é 't por unidade de E_unit' e muda de 0,0344 para 0,0222 quando você só troca o escoamento. Afinal, o que é c?"
- **Motivação:** slide 19 (o segundo item do slide diz que c faz o papel de taxa de transferência); seção 3.4.4 e Tabela 9.
- **Resposta sugerida:** "c é um coeficiente de escala calibrado. Ele reúne a entrega de sedimento até o exutório, a diferença de escala entre a equação de Williams e o pixel, as unidades e parte do erro do escoamento. Por isso o texto diz que ele não deve ser lido como uma taxa de transferência física (3.4.4). Prova disso: se o volume do pixel entrasse em m³ em vez de mm × m², o índice ficaria 1000^0,56 ≈ 48 vezes menor e c passaria a cerca de 1,6 no MC e 1,1 no MFM, valores maiores que 1 e sem sentido como SDR. A semelhança com a SDR é só de papel na equação, não de valor."
- **Risco:** alto. Sugestão: no slide 19, troque "faz o papel de uma taxa de transferência" por "ocupa o lugar da conectividade de Hao et al., mas é só um fator de escala".

### P6. "Os mapas dos slides 19, 28 e 29 estão em 'kg por pixel' e se chamam 'sedimento'. No texto, o mesmo c·E_unit se chama 'erosão'. Isso é erosão local ou sedimento que chega ao rio?"
- **Motivação:** slides 19 ("Sedimento estimado"), 28 ("sedimento por evento") e 29 ("sedimento médio") contra as seções 3.4.4 e 3.4.9 ("mapa de erosão"). Se c inclui a entrega, c·E_k é a parte do pixel na carga do exutório, supondo a mesma entrega em toda a bacia. Não é a erosão local.
- **Resposta sugerida:** "É uma grandeza relativa. Como c é o mesmo em toda a bacia, o mapa de c·E_k tem o mesmo padrão espacial do índice de erosão local. O valor em kg só significa a parcela de cada pixel na carga do exutório se a entrega fosse a mesma em toda a bacia, e o modelo não sustenta essa hipótese. Por isso, o mapa deve ser lido pelo padrão e pela ordem dos pixels, não pelo valor absoluto em kg." Padronize o termo: use "erosão relativa" nos slides ou explique a unidade.
- **Risco:** médio a alto.

### P7. "Por que o MC é pior que a regra proporcional à chuva? Esse resultado depende do critério de calibração?"
- **Motivação:** slides 21 e 36; seções 4.2 e 4.3. No slide 36, com calibração linear o MC erra 44,8% (a regra erra 38,8%). Com o critério de erro relativo, o MC erra 40,4% e a regra 51,7%, ou seja, o MC fica melhor.
- **Resposta sugerida:** "A razão física é que o SCS-CN supõe que a fração da chuva que escoa cresce com a chuva, mas nesta bacia ela não cresceu (r = −0,01). O método superestima as chuvas grandes, subestima as pequenas, e o expoente 1,12 amplia o erro (4.2). Mas a ordem entre o MC e a regra depende do critério: com o critério em log, o do trabalho, o MC é claramente pior (p = 0,02). Com outros critérios, ele fica perto da regra ou um pouco melhor. O que não muda com o critério: o MC erra de 40 a 80%, e com o escoamento medido o erro cai para cerca de 20%." Atenção: a frase da seção 4.3, "o MC continua pior que o modelo simples com a chuva em todos os subconjuntos testados", fala de subconjuntos de eventos, não de critérios.
- **Risco:** alto, se a banca perceber que a frase "pior que o modelo simples" do resumo e da conclusão depende do critério em log.

### P8. "No slide 31 você diz que 'cerca de 3/4 do erro vem da hidrologia'. Como chegou a isso?"
- **Motivação:** slide 31 ((81 − 21)/81 ≈ 74%). O texto não faz essa conta e, na seção 4.3, avisa que o ganho do MFM vem em parte do fato de a carga medida também depender do volume.
- **Resposta sugerida:** "É uma conta simples, (81 − 21)/81, e não uma partição do erro. Medianas de erro não se somam, e parte da queda vem de o volume medido e a carga virem do mesmo hidrograma (4.3). O número que eu sustento é outro: o erro do escoamento explica 91% da variância do erro do sedimento no MC (4.2)." O melhor é tirar o "3/4" do slide.
- **Risco:** médio a alto.

### P9. "Na fórmula do pixel, Q está em mm, pr em m³/s e Apix em m². Nos slides 3 e 4, Q é volume em m³. A equação de Williams está sendo usada com as unidades certas?"
- **Motivação:** slides 3, 4 e 18; seção 3.4.3.
- **Resposta sugerida:** "Q em mm vezes Apix em m² dá 1000 vezes o volume em m³. Isso só multiplica o índice por uma constante (1000^0,56), que vai para dentro de c. Por isso E_unit é tratado como índice relativo, e não como toneladas (3.4.3). Segui a forma de Hao et al. (2022). Com um único c calibrado, a constante não muda nenhum resultado."
- **Risco:** médio.

### P10. "O seu pico local é o volume do pixel vezes RI/R, sem roteamento e sem área de contribuição. Então o pico não traz nada. Isso ainda é MUSLE, ou é uma USLE ponderada por Q^1,12?"
- **Motivação:** slide 17 (o próprio slide diz que o pico local não traz informação espacial nova); seção 3.4.3.
- **Resposta sugerida:** "Na prática, sim. Como RI/R é um número por evento, a erosão de cada pixel é proporcional a Q^1,12·K·LS·C, e o RI/R só dá peso aos eventos de chuva concentrada. Segui Hao et al. (2022). O texto mostra ainda que o expoente efetivo, 1,12, é maior que a relação observada nesta bacia entre carga e volume, 0,94 (4.6), o que ajuda a explicar a ampliação do erro."
- **Risco:** médio.

### P11. "Por que não calibrou o expoente 0,56, ou o 11,8, como fizeram Avanzi et al. (2008) e o seu próprio trabalho de 2025?"
- **Motivação:** slides 6 e 20; seções 2.2 e 3.4.5; Tabela 9. A relação observada tem expoente 0,94, contra 1,12 no modelo.
- **Resposta sugerida:** "Mantive os coeficientes de Williams e calibrei só c, para ter um parâmetro só e uma validação cruzada limpa. Com 17 eventos, um segundo parâmetro aumenta o viés de otimismo. Calibrar o expoente em log provavelmente aproximaria o MFM da regra com o volume, sem mudar a conclusão. Não testei, e isso fica como sugestão."
- **Risco:** médio.

### P12. "A chuva vem de dois postos, um fora da bacia, interpolada por IDW com potência 2 sem teste. No mapa, a cabeceira recebe menos chuva em 13 dos 17 eventos, mas na seção 3.1 você diz que ela tende a ser a parte mais chuvosa. E 63% da variação espacial do mapa vem do escoamento. O padrão leste-oeste do mapa não é um artefato?"
- **Motivação:** slides 14 e 27 ("63% do escoamento"); seções 3.1, 3.4.1.4, 4.1 e 4.5.
- **Resposta sugerida:** "Pode ser, em parte. A seção 4.5 diz que essa é a parte menos confiável do mapa. Com dois postos, a chuva é sempre um gradiente suave entre eles, e um posto fora da bacia, a leste, comanda a cabeceira. Os 63% são em escala log; em escala linear, o produto K·LS·C sozinho explica R² = 0,58. Ou seja, as manchas de uso e declive existem independentemente da chuva, mas a intensidade relativa entre leste e oeste depende dos postos. Mais postos ou radar resolveriam isso (seção 5)."
- **Risco:** médio a alto. A contradição com a seção 3.1 é fácil de notar.

### P13. "A sua validação cruzada refaz só o c. Com um parâmetro e 16 eventos, ajuste e validação ficam quase iguais. As escolhas que pesam (CN-I, λ, Woodward) foram feitas olhando os 17 eventos. O que a validação cruzada valida de fato?"
- **Motivação:** slide 20; seção 3.4.6.
- **Resposta sugerida:** "Ela retira o viés do ajuste de c, e mais nada. O texto diz que as escolhas do SCS-CN foram feitas antes, com os mesmos eventos, e que por isso as métricas tendem a ser otimistas. A validação cruzada aninhada não foi feita (3.4.6). O valor dela está em comparar os modelos sob o mesmo procedimento. Como o MC já vai mal mesmo com esse viés a favor, a conclusão sobre o escoamento continua de pé."
- **Risco:** médio a alto.

### P14. "A comparação com o modelo concentrado de 2025 é justa? Ele foi ajustado nos próprios eventos, usa o volume total com a vazão de base e o pico medido. No gráfico do slide 24, ele aparece no grupo 'escoamento direto forçado ao medido'."
- **Motivação:** slides 24 e 26; seções 3.4.8 e 4.3.
- **Resposta sugerida:** "Não é justa, e por isso a chamo de indicativa: o concentrado tem vantagem, porque foi avaliado no ajuste e usa o volume total, que sozinho explica 88% da carga. Eu poderia ter recalibrado α e β com leave-one-out; não fiz. O rótulo do gráfico deveria dizer 'com o volume medido', e não 'escoamento direto'." Corrija o rótulo do slide 24 e, se possível, inclua no gráfico a barra da regra com o volume (16%), que é a comparação mais importante.
- **Risco:** médio.

### P15. "Como são medidos o sedimento e a turbidez? A turbidez é da água bruta da SABESP: a captação fica no mesmo ponto da estação do DAEE? Quantas amostras da curva estão acima de 250 NTU? A MUSLE estima a produção total, mas você mede só o sedimento em suspensão."
- **Motivação:** slide 12; seções 2.5, 3.2 e 4.6.
- **Resposta sugerida:** "A concentração vem da curva por partes de Murillo-Bermúdez et al. (2023), com quebra em 250 NTU, e a incerteza é maior justamente nos picos. Não estimei essa incerteza. A carga de fundo não foi medida, então o alvo é a carga em suspensão, e o c absorve essa diferença." Sobre a posição da captação em relação à estação e o número de amostras acima de 250 NTU, o texto não responde: confirme com o orientador antes da defesa.
- **Risco:** médio.

### P16. "Se o pico de concentração chega cerca de 25 h antes do pico de vazão, há sedimento disponível perto do canal. Você calibra c com a carga total, inclusive a parte levada pela vazão de base e a vinda do canal. Isso não infla c e o mapa?"
- **Motivação:** slides 13, 32 e 35; seções 3.4.4 e 4.6.
- **Resposta sugerida:** "Infla c, mas não muda o padrão do mapa, porque c é o mesmo em todos os pixels. A seção 3.4.4 admite que toda a carga é atribuída às encostas. No evento 11, cerca de 72% da carga está na parcela do escoamento direto, supondo a mesma concentração na vazão de base (slide 35). Separar as fontes do canal exigiria traçadores ou balanço por sub-bacia."
- **Risco:** médio.

### P17. "O evento 17 tem 3.806 mg/L de concentração média, quase o dobro dos outros. E os resíduos do MFM têm tendência: os primeiros eventos ficam superestimados e os últimos, subestimados. O que aconteceu?"
- **Motivação:** seção 4.3 e Tabela 12. Não aparece nos slides.
- **Resposta sugerida:** "Não identifiquei a causa. As hipóteses são uma fonte pontual, como obra ou deslizamento, uma mudança na curva de turbidez ou uma deriva do sensor. Mantive o evento porque não há base para excluí-lo; sem ele, o MFM vai a 15,3% e a conclusão não muda. A tendência no tempo indica que um c único não representa a variação da disponibilidade de sedimento ou da medição (4.3 e 4.6)."
- **Risco:** médio.

### P18. "Os valores de C: silvicultura com 0,121, mais que o dobro do campo (0,05), sendo que eucalipto formado costuma ter C baixo. A silvicultura responde por 24% da erosão. Solo exposto e mineração com C = 1 adotado. Quanto do ranking das classes vem desses números?"
- **Motivação:** slides 9, 27 e 29; Tabelas 6 e 14; seção 4.5.
- **Resposta sugerida:** "Quase todo. Na contribuição por classe de uso, o C define a ordem. Os valores vêm de Vivarelli et al. (2025) e de Silva et al. (2016), e não foram recalibrados nem testados por sensibilidade. O 0,121 vale para plantio com manejo e idade variáveis; em talhões formados, o C seria menor e a silvicultura cairia no ranking. O texto diz que o destaque da mineração e do solo exposto vem em parte do C = 1 adotado (4.5)."
- **Risco:** médio.

### P19. "Por que limitar a área de contribuição a 200 m no LS? O LS médio de 7,8 é alto. Isso não determina, por construção, que 78% da erosão venha das encostas acima de 20%?"
- **Motivação:** slide 18 e slide 27 (65% → 78%); seção 3.4.1.2 e Tabela 16.
- **Resposta sugerida:** "O limite evita valores sem sentido nos pixels de canal, onde a área de contribuição chega a milhões de metros. O valor de 200 m é uma escolha, e não testei outros. A concentração em encostas íngremes é esperada pela própria formulação (LS cresce com o seno da declividade elevado a 1,3), então ela descreve o modelo, não confirma nada sobre o campo."
- **Risco:** médio.

### P20. "Como os eventos foram delimitados? Há janelas de até 149 h, eventos colados uns nos outros, e chuva antes do início da janela. Faz sentido aplicar o SCS-CN a uma chuva de seis dias com vários pulsos?"
- **Motivação:** slides 13 e 31 (12 a 14 mm antes da janela no evento 11); Tabela 2; seção 4.6.
- **Resposta sugerida:** "As janelas foram definidas à mão sobre o hidrograma, no trabalho anterior, e eu as mantive para poder comparar. O SCS-CN foi feito para uma chuva única. Em eventos longos com vários pulsos, a infiltração se recupera entre os pulsos e o método perde sentido. É uma limitação sem estimativa quantitativa (4.6). Um critério objetivo, por exemplo um tempo mínimo sem chuva entre eventos, seria o próximo passo."
- **Risco:** médio.

### P21. "O coeficiente de escoamento não cresceu com a chuva (r = −0,01). O que isso diz sobre como o escoamento é gerado nesta bacia? É escoamento superficial por excesso de infiltração?"
- **Motivação:** slide 31 (item 3); seção 4.1.
- **Resposta sugerida:** "Sugere que boa parte do escoamento rápido não é superficial por excesso de infiltração, mas vem de áreas saturadas perto dos canais e de fluxo subsuperficial raso, o que é comum em clima úmido com solos profundos. Isso tem duas consequências: o SCS-CN com CN tabelado não acompanha a resposta, e a MUSLE, que supõe escoamento sobre as encostas, pode localizar mal a erosão. Há a ressalva de que o coeficiente medido depende da separação da vazão de base e da chuva de dois postos (4.1)."
- **Risco:** médio. Pergunta conceitual que costuma separar quem entende o processo.

### P22. "No evento 12, o posto DBT5 marcou 0 mm. É chuva zero ou falha do posto? E de onde vêm os pesos 0,307 e 0,693 da lâmina R?"
- **Motivação:** Tabela 2; seções 3.4.1.4 e 4.6. O RI/R passa de 1 nos eventos 1 e 12.
- **Resposta sugerida:** "Tratei o 0 como chuva zero, como estava na planilha de eventos, mas não verifiquei se foi falha. Os pesos também vêm da planilha." O texto não diz a origem dos pesos (podem ser de Thiessen); confirme antes da defesa. Se não souber, diga isso. "Em parte por isso, o RI/R é tratado só como índice de concentração (3.4.3)."
- **Risco:** médio.

### P23. "Na introdução você diz que o modelo permite prever cenários futuros. Com esses resultados, dá para usá-lo para simular, por exemplo, troca de campo por mata?"
- **Motivação:** seção 1.2 ("podendo gerar predições de cenários futuros"); seção 1.1 (modelos usados para cenários).
- **Resposta sugerida:** "Só em termos relativos e com cautela. Trocar C mudaria o mapa, mas o efeito na carga do exutório não foi validado, porque com o volume medido a fórmula não superou a regra com o volume. Para prever a carga a partir da chuva, o modelo ainda não serve (MC com 81% de erro). Eu retiraria essa frase ou a qualificaria."
- **Risco:** médio a baixo.

### P24. "Com 17 eventos, a diferença entre o MFM e a regra com o volume deu p = 0,52. Isso quer dizer que os dois são iguais, ou que você não tem eventos suficientes para ver a diferença?"
- **Motivação:** slides 24 e 26; seções 3.4.7 e 4.6.
- **Resposta sugerida:** "Quer dizer que não há evidência de diferença, e não que os dois são iguais. O intervalo vai de −5,5 a +10,4 pontos. Por isso as conclusões são qualitativas (4.6)."
- **Risco:** baixo.

### P25. "Qual é a área da bacia: 137,8, 138,1, 138,8 ou 139,3 km²? E por que dizer 'descarga de sedimentos' para uma massa por evento, em toneladas?"
- **Motivação:** slide 8 (138,8 km²) contra as seções 3.1 e 3.3 (137,8 pela acumulação de fluxo, 138,1 da área de cálculo, 139,3 da literatura). "Descarga" costuma indicar uma vazão de massa (t/dia), e não o total do evento.
- **Resposta sugerida:** "137,8 km² pela acumulação de fluxo no MDE. A área de cálculo tem 138,1 km² e a literatura dá 139,3 km²; o 138,8 do mapa está errado e vou corrigir." Sobre o termo: "É a carga, ou produção de sedimentos, do evento; usei 'descarga' no sentido de massa total que sai no evento."
- **Risco:** baixo.

---

## 2. Divergências entre o texto e a apresentação

### Números
| Onde | Slide | Texto | Comentário |
|---|---|---|---|
| Área da parte alta | Slide 8 (legenda do mapa): 138,8 km² | 137,8 km² (3.1); 138,1 km² da área de cálculo (3.3); 139,3 km² na literatura | Corrigir o mapa |
| Histerese | Slide 35: "13 de 17 eventos com laço horário" | 2.5: 13 em forma de oito e 4 horários (Murillo-Bermúdez e Martim, 2022) | Contradição séria, com o autor do artigo na banca |
| Regra com a chuva, erro mediano | Slide 36: 41,8% | Tabela 13 e slide 26: 41,9% | Pequena diferença, mas visível |
| Classes de solo e uso | Slide 9 (legenda): Cambissolos 68,5%, Argissolos 17,7%, silvicultura 12,6% | Tabelas 5 e 6: 68,6%, 17,6%, 12,7% | Diferença de base (área do mapa contra pixels de cálculo); não é grave |
| c no evento 11 | Slide 23: "validação cruzada, c = 0,0222" | 0,0222 é o c do ajuste com os 17 eventos (Tabela 9); na validação cruzada, c é recalculado sem o evento 11 | Ajustar o rótulo |
| "3/4 do erro vem da hidrologia" | Slide 31 | Não existe no texto; a seção 4.3 alerta que o ganho do MFM não valida a fórmula | Tirar ou trocar pelo número de 91% |
| Chuva antes da janela no evento 11 (12 a 14 mm, 16%) | Slide 31 | O texto diz que a delimitação é tratada "sem estimativa quantitativa" (4.6) | É informação nova, sem base no texto |
| Intensidade de chuva e concentração (Spearman 0,49; p = 0,04); "0%" explicado pela intensidade; 68% e 72% da carga | Slide 35 | Não estão no texto | São análises novas: estar pronto para explicar como foram feitas |
| Sensibilidade ao critério de calibração | Slide 36 (inteiro) | Não está no texto | Mostra que a frase "MC pior que a regra com a chuva" depende do critério em log, e o texto não diz isso |

### Termos
- **Coeficiente c.** O texto o chama de "coeficiente de escala", diz que ocupa o lugar de uma taxa de transferência média e avisa que "o seu valor não deve ser lido isoladamente como uma taxa de transferência física" (3.4.4). O slide 19 diz que "c faz o papel de uma taxa de transferência de sedimentos média da bacia" e menciona o que ele absorve, mas não traz o aviso. Ficam faltando dois pontos: c tem unidade (t por unidade de E_unit), e o valor dele muda entre o MC e o MFM. O slide 19 também diz "t por unidade de E", enquanto o texto diz "t por unidade de E_unit".
- **Erosão ou sedimento.** O texto chama c·E_unit de "erosão" (mapa de erosão, erosão média). Os slides 19, 28 e 29 chamam a mesma grandeza de "sedimento" (sedimento estimado, sedimento por evento, sedimento médio), em kg por pixel. O slide 27 alterna entre "maior contribuição" (legenda) e "maior erosão" (fonte).
- **"Volume".** Nos slides, "regra com o volume" usa o volume de escoamento direto (Vdir), mas os "88% explicados pelo volume" (slides 25 e 35) usam o volume total, com a vazão de base. O texto diz qual é qual (4.3; Figura 11); os slides não.
- **Nomes dos modelos simples.** O texto usa "modelo simples com a chuva/escoamento", "curva-chave de sedimentos com o escoamento direto" e "modelo de correlação". Os slides usam "regra simples com a chuva" e "regra com o volume". Escolha um nome e use sempre o mesmo.
- **Escoamento "medido".** O slide 13 diz "escoamento direto medido" sem ressalva. O slide 31 põe "medido" entre aspas. O texto usa "medido", mas explica que depende do filtro. Seja coerente, por exemplo com "escoamento direto observado (estimado pelo filtro)".
- **11,8 e 0,56.** O slide 6 diz "constantes de calibração, sem sentido físico". O texto diz "ajustados empiricamente por Williams em escala de bacia". As duas formas são compatíveis, mas o texto é mais preciso, e é ele que explica por que o pixel exige c.

### Afirmações que o texto qualifica e o slide não
- **Slide 16:** "λ = 0,05 teve melhor desempenho médio em 3.578 bacias (Brandão et al., 2025)". O texto (2.3 e 4.6) acrescenta três ressalvas: os mesmos autores associam λ = 0,20 a clima úmido e a pastagem, como no alto Jundiaí; o desempenho absoluto foi baixo; e o CN foi calibrado junto com λ. Some-se a isso que Baert et al. tiveram NSE −0,87 com a conversão de Woodward. O slide passa a impressão de que a literatura apoia a escolha.
- **Slide 24 (gráfico):** o modelo concentrado aparece no grupo "escoamento direto forçado ao medido", mas usa o volume total e o pico medido e não passou por validação cruzada. A regra com o volume (16%), que é a comparação decisiva, não aparece no gráfico, só na caixa de texto.
- **Slide 25:** "Todas as métricas usam a previsão do evento que ficou de fora". Isso não vale para o modelo concentrado nem para o R² do mapa.
- **Slide 30:** "Áreas críticas: campo, silvicultura e lavoura temporária sobre Cambissolos, em encostas acima de 20% (46% da área, 83% da erosão)". O par 46% → 83% vale só para as classes de uso. Juntar solo e declividade no mesmo número mistura três análises diferentes (Tabelas 14 a 16).
- **Slide 30:** o slide não repete a conclusão, presente no resumo e na seção 5, de que o MC foi pior que a regra com a chuva.
- **Slide 31 (falas):** as causas aparecem "em ordem de importância provável", e a fala diz que "resolver essas quatro é o que mais melhoraria o resultado". O texto não ordena as causas nem faz essa afirmação.
- **Slide 32:** "parte da carga pode vir do canal (pico de CSS antes da vazão)". O texto diz que parte pode vir do canal e das margens (3.4.4 e 4.6), mas não usa a histerese como argumento. E, pelo texto, a maioria dos laços é em oito, não horária.
- **Slide 35 (falas):** "laço horário, típico de sedimento disponível perto do canal". Essa interpretação não está no texto e entra em conflito com a classificação publicada.
- **Slide 21:** a frase "de 10% do medido (evento 10) a 3,1 vezes (evento 9)" vem logo depois de "pior em 14 dos 17 eventos" e pode ser lida como a diferença em relação à regra. No texto, ela é o erro do MC em relação ao medido.
- **Slides 12 e 22:** os gráficos usam vírgula como separador de milhar (4,500), no formato inglês, enquanto o resto da apresentação usa o formato brasileiro. No slide 21, o eixo x dos gráficos aparece sem rótulo.

---

## 3. Pontos fracos mais sérios da pesquisa

1. **O produto principal, o mapa de áreas críticas, não tem validação, e o desenho do estudo não permite fazê-la.** Com o volume medido, a fórmula com K, LS e C não supera a regra com o volume. Portanto, nada nos dados confirma que a estrutura espacial da MUSLE acrescenta informação. O mapa é consequência dos valores adotados.
2. **A hidrologia é fraca e foi ajustada nos próprios eventos.** O CN-I foi usado em eventos da estação chuvosa, inclusive em eventos seguidos, junto com λ = 0,05 e a conversão de Woodward, que nesta bacia é extrapolada (8,4% dos pixels e os eventos 1 e 12). Tudo isso foi escolhido para acertar o volume total. O volume por evento tem NSE de −0,39, e não houve validação cruzada aninhada.
3. **O escoamento direto observado depende de uma separação de vazão de base discutível.** O BFImax de 0,70, contra 0,25 recomendado para rocha cristalina, deixa 47% do volume como vazão de base. Esse valor alimenta o Vdir, a escolha do CN, o MFM e a regra com o volume, e não houve análise de sensibilidade.
4. **A chuva vem de dois postos, um fora da bacia, interpolados por IDW.** O termo de escoamento responde por 63% da variação espacial do mapa (em log), e o gradiente leste-oeste pode ser um artefato. Ele contradiz a ideia da seção 3.1 de que a cabeceira é a parte mais chuvosa.
5. **Um único c para tudo.** Ele tem unidade, absorve a entrega, a escala, as unidades e o erro do escoamento, e não há conectividade. O mapa em kg mistura erosão local com sedimento entregue, e o valor de c não tem leitura física.
6. **A observação de sedimento tem incerteza não estimada.** A concentração vem da turbidez da água bruta, com uma curva por partes mais incerta nos picos. Mede-se só o sedimento em suspensão, e a carga total inclui a vazão de base e o canal. O evento 17 destoa e os resíduos têm tendência no tempo. A histerese não é representada.
7. **A amostra é pequena e os testes são fracos.** São 17 eventos de 2018 a 2020, com janelas manuais de até 149 h e eventos colados. A validação leave-one-out com um parâmetro quase não difere do ajuste. A conclusão "MC pior que a regra com a chuva" depende do critério de calibração (slide 36).
8. **A MUSLE foi aplicada ao pixel sem roteamento.** O pico local é proporcional a Q, e o modelo se reduz a Q^1,12·K·LS·C. O expoente efetivo (1,12) é maior que o observado entre carga e volume (0,94), e o C da silvicultura (0,121, maior que o do campo) pesa muito no ranking das classes.

---

## 4. O que está no texto, ficou fora da apresentação e precisa estar pronto para resposta

- **Vazão de base:** fica com 34% a 55% do volume de cada evento (47% no total). O BFImax de 0,70 contrasta com o 0,25 sugerido por Eckhardt para rocha cristalina, e a bacia tem 86% de embasamento cristalino com aquífero fraturado (3.1, 3.2 e 4.6). O slide 31 cita o 0,70, mas não o contraste.
- **Extrapolação da relação de Woodward:** 8,4% dos pixels têm CN-I abaixo de 35, e os eventos 1 e 12 têm menos de 25,4 mm de chuva (3.4.1.3). A retenção média S0,05 é de 490 mm.
- **Validação cruzada aninhada não feita:** as métricas tendem a ser otimistas (3.4.6). O slide 16 só diz "escolhida olhando os mesmos 17 eventos".
- **Expoente carga–volume de 0,94 contra 1,12 do modelo** (4.6). Bom argumento para explicar por que o erro é ampliado.
- **Evento 17** (3.806 mg/L; sem ele, o MFM vai a 15,3%) e a **tendência dos resíduos do MFM** (primeiros eventos superestimados, últimos subestimados) (4.3).
- **Sensibilidade à retirada do evento 15** e o NSE linear (4.3). Também o NSE linear do concentrado (0,83) e o intervalo de erros dele (−37% a +60%).
- **Intervalo de confiança da diferença MC contra regra com a chuva:** +3,1 a +117,5 pontos (4.3). O slide 21 só traz o p.
- **Variância do log do volume (0,66) contra a do log da concentração (0,08)** (4.3; Figura 11). É o argumento mais claro de por que qualquer modelo com o volume medido acerta a ordem de grandeza.
- **Partição em escala linear:** R² de 0,58 só com K·LS·C (4.5). O slide 27 dá só a versão em log (37% e 63%), e a conclusão depende da escala.
- **Perda de volume pelo limite Q ≤ P no MFM:** 10,3% no evento 10 (f = 9,75) e 7,6% no evento 1 (4.1).
- **RI/R maior que 1** nos eventos 1 e 12, **DBT5 = 0** no evento 12 e **pesos 0,307 e 0,693** da lâmina R (3.4.1.4 e 3.4.3).
- **IDW com potência 2 sem teste de outras potências** (3.4.1.4).
- **LS de Moore e Burch com área de contribuição limitada a 200 m** e LS médio de 7,80 (3.4.1.2).
- **Diferença de datas e escalas entre as bases:** CN do MapBiomas de 2022, K e C do Plano de 2020, mapa de solos em 1:250.000, eventos de 2018 a 2020 (3.3).
- **Área urbana com erosão nula** por hipótese, concentrada perto do exutório, o que pode transferir carga para as áreas rurais (4.5). O slide 32 menciona isso só de passagem.
- **Solo exposto e mineração:** cerca de 18 vezes a média por unidade de área, com C = 1 adotado (4.5 e Tabela 14).
- **Combinações mais frequentes nos pixels críticos:** lavoura temporária sobre Cambissolo com 20% a 45% de declividade (26,7%), silvicultura na mesma situação (19,2%) e lavoura temporária com 8% a 20% (13,8%) (4.5). É útil se perguntarem "onde, concretamente, agir".
- **Objetivos específicos:** o slide 11 mostra só o objetivo geral. A banca pode cobrar o objetivo de "validar o modelo distribuído". Esteja pronto para dizer que a validação foi feita no exutório, para a soma da bacia, e não no espaço.
- **Mapas por evento do MFM** (4.4): mesmo padrão do MC, com outra intensidade.
- **Revisão de literatura que ajuda a defender o resultado:** Baert et al. (2026), com NSE do volume de −0,87 com a conversão de Woodward; Valle Junior et al. (2019), em que Q = C·P foi melhor que o SCS-CN; Hao et al. (2022), com conectividade abaixo de 0,5 em 80% da área (2.1, 2.3 e 4.1).
