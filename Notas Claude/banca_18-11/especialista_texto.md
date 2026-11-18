# Perguntas esperadas na defesa: avaliador especialista em hidrologia e sedimentos

Persona: pesquisador de nível de doutor em hidrologia e sedimentos (MUSLE/USLE, SCS-CN, vazão de base, turbidez, validação). Exigente com coerência física, unidades, hipóteses e validação.

Base: somente o texto final do TCC (TCC_texto_final.md). Conferi as contas do Apêndice A e das tabelas 2, 3, 11 a 16; elas batem, salvo os pontos da Parte 3.

Algumas contas que fiz a partir das tabelas e que ajudam nas respostas (não estão escritas no TCC):
- Coeficiente de escoamento direto medido (Vdir / (R x 137,8 km²)): de 3% (eventos 6 e 12) a 22% (evento 2), cerca de 10% no conjunto. Com a vazão de base, cerca de 20%.
- Retenção média S0,05 = 489,9 mm, o que dá um CN "equivalente" de cerca de 34 (25.400 / (254 + 490)). A abstração inicial média é 0,05 x 490 = cerca de 24,5 mm, maior que a chuva dos eventos 1 e 12 (cerca de 23 mm).
- Os eventos 15 e 16 estão separados por só 13 h (15 termina em 09/02/20 01h e 16 começa em 09/02/20 14h). Os eventos 13 e 14 estão separados por 3 dias.

---

## Parte 1. Perguntas prováveis (da mais provável ou perigosa para a menos)

### 1. Condição seca (CN-I) na estação chuvosa
(a) "Você usou CN-I, condição seca, para todos os eventos. Mas 16 dos 17 eventos são entre novembro e março, e o evento 16 começa 13 horas depois de um evento de 139 mm. Que sentido físico tem chamar isso de condição seca? Isso não é só um parâmetro de ajuste com outro nome?"
(b) Seção 3.4.1.3 ("A condição seca é... escolhida pelo volume, e não uma medida da umidade antecedente"); Tabela 2 (datas); seção 3.1 (clima úmido).
(c) Resposta sugerida: admitir logo. O TCC diz que o CN-I é "uma condição única para o conjunto de eventos, escolhida pelo volume, e não uma medida da umidade antecedente de cada evento" (3.4.1.3). Ou seja, na prática foi um ajuste do CN ao volume total. Dá para defender que o coeficiente de escoamento direto medido é baixo (cerca de 10% no conjunto), e que um CN tabelado na condição média geraria escoamento demais. Isso é coerente com solos profundos e intemperizados e com muita água indo para a vazão de base. Mas o rótulo "AMC I" não deve ser defendido como umidade real. Frase honesta: "Eu não estou dizendo que o solo estava seco. Usei a conversão para CN-I como forma de baixar o CN tabelado até o volume medido. É um CN efetivo da bacia, e essa escolha foi feita com os mesmos dados (3.4.6)."
(d) Risco: alto.

### 2. Unidades da fórmula de Williams no pixel
(a) "Williams usa volume em m³ vezes pico em m³/s. Você multiplica Q em milímetros pela área em m² e pelo pico. Milímetro vezes metro quadrado não é metro cúbico. Qual é a unidade de E_unit? E, se tudo vai para o c, o que sobra da MUSLE?"
(b) Seção 3.4.3 ("com Q_k em mm, pr,k em m³/s e Apix em m², como em Hao et al."); Apêndice A, passo V (13,00 x 5,17x10^-4 x 897,49).
(c) Resposta sugerida: o TCC já diz que E_unit é "um índice relativo de erosão, e não uma massa" e que "as constantes de escala e de unidade ficam todas no coeficiente c" (3.4.3). Q em mm vezes Apix em m² é 1.000 vezes o volume em m³. Como o expoente é fixo (0,56), esse fator vira uma constante multiplicativa (1.000^0,56) e é absorvido por c. Por isso não muda nenhum resultado relativo nem as métricas. O que sobra da MUSLE é a forma: erosão proporcional a Q^1,12 x K x LS x C. Vale ter essa conta pronta e dizer que manteve a convenção de Hao para poder comparar.
(d) Risco: alto.

### 3. O que a MUSLE acrescenta, se ela empata com SY = c x Vdir?
(a) "Com o volume medido, sua MUSLE espacializada não supera uma reta de carga contra volume. Com a chuva, ela perde para uma reta de carga contra chuva. Então, no exutório, a MUSLE não serviu para nada?"
(b) Seção 4.3 (Tabela 13; diferença +1,6 pontos, IC de -5,5 a +10,4; Wilcoxon p = 0,52); Conclusões ("não permitiu avaliar separadamente a contribuição da fórmula").
(c) Resposta sugerida: concordar, porque é a conclusão do próprio trabalho (Conclusões, 4.º parágrafo). No exutório, K, LS e C são os mesmos em todos os eventos (4.2). A única coisa que muda entre eventos é o escoamento. Por isso, nenhum teste no exutório consegue avaliar os fatores da MUSLE. O ganho da espacialização é o mapa relativo, e não uma previsão melhor da carga (Resumo; 4.5). Não tentar defender que a MUSLE "funcionou" no exutório.
(d) Risco: alto.

### 4. O mapa de áreas críticas é artefato de dois postos?
(a) "Você mesmo mostra que 63% da variação espacial do mapa vem do termo de escoamento, isto é, da chuva interpolada de dois postos e de um CN nacional. Então o mapa de áreas críticas não é, em boa parte, o gradiente do IDW?"
(b) Seção 4.5 (partição 37,1% / 62,9%; "essa parcela do padrão é a menos confiável do mapa"); 4.1 (Figura 6, gradiente suave).
(c) Resposta sugerida: o TCC reconhece isso (4.5). Há três argumentos para equilibrar. (i) Em escala linear, K x LS x C sozinho explica R² = 0,58 do mapa (4.5), e a conclusão depende da escala. (ii) A classificação por uso, solo e declividade (Tabelas 14 a 16) vem sobretudo dos fatores fixos. (iii) O termo G_k inclui o CN, que também depende do uso e do solo, de modo que nem toda essa parcela é gradiente de chuva. Mas a honestidade pede dizer: "a parte leste–oeste do mapa vem dos dois postos e eu não a considero confiável. As classes críticas (lavoura, silvicultura e campo em encosta íngreme) são mais robustas que a posição exata das manchas." Seria bom ter (ou citar como trabalho futuro) um mapa feito com chuva uniforme na bacia, para mostrar o que muda.
(d) Risco: alto.

### 5. Sem conectividade, isso é mapa de erosão ou de produção de sedimentos?
(a) "Hao et al. só chegam ao exutório porque usam conectividade por pixel. Você trocou por um c único. Um pixel íngreme a 100 m do rio e outro no topo de um divisor pesam igual. Por que não calculou o índice de conectividade de Borselli, que só precisa do MDE e do C?"
(b) Seções 2.6, 3.4.4, 4.5 (ressalva 1) e Conclusões (3.ª frente).
(c) Resposta sugerida: o texto deixa claro que o mapa mostra "onde a erosão local é produzida, e não onde o sedimento chega à rede de drenagem" (3.4.4 e 4.5). A razão honesta para não usar o índice: com um único ponto de medição e 17 eventos, não haveria como calibrar ou testar um índice por pixel. Ele só mudaria o mapa, sem dado para verificar. Isso aparece como trabalho futuro (Conclusões). Se o aluno não testou, não deve dizer que "não mudaria nada".
(d) Risco: alto.

### 6. Vazão de base: BFImax 0,70 e a cadeia de dependências
(a) "Quem gerou a série de vazão de base? Você reproduz com BFImax = 0,70, mas o próprio Eckhardt sugere 0,25 para rio perene em rocha cristalina. Se a base estiver superestimada, o seu Vdir está subestimado. E o CN-I foi escolhido para bater com esse Vdir. Você testou outro BFImax?"
(b) Seções 2.4, 3.2 ("série fornecida com os dados... reproduzida"), 4.6 (4.ª fonte).
(c) Resposta sugerida: o TCC reconhece que 0,70 está acima do valor de referência e que a série "pode atribuir à vazão de base uma parte do volume que seria escoamento direto" (4.6). Não foi feita análise de sensibilidade. O ponto que o aluno deve dizer antes da banca: o BFImax afeta tudo em sequência (Vdir, MFM, modelo simples com Vdir e a própria escolha da configuração do SCS-CN). Com BFImax menor, o Vdir cresce, e o CN-I + lambda 0,05 talvez já não fosse escolhido. A conclusão principal (o escoamento é o gargalo) provavelmente se mantém, mas os números mudam. Pode lembrar que o aquífero fraturado está sob um manto de intemperismo espesso (Cambissolos), que pode se comportar como meio poroso, o que ajudaria a explicar uma base alta. Mas isso é hipótese, não foi verificado no TCC.
(d) Risco: alto.

### 7. A validação cruzada de um parâmetro só não é quase trivial?
(a) "Com um só parâmetro, o leave-one-out mal muda o c, e as suas métricas de ajuste e de validação são praticamente iguais. O otimismo de verdade está nas escolhas de CN-I, lambda e Woodward. Quantas configurações você testou antes de escolher essa? E o que as outras davam?"
(b) Seções 3.4.6 ("as métricas da validação cruzada tendem a ser um pouco otimistas"), 3.4.1.3 e 4.2 ("Os resultados no ajuste e na validação cruzada são próximos").
(c) Resposta sugerida: concordar que o LOO de c sozinho protege pouco, e que o próprio texto diz que a validação aninhada não foi feita (3.4.6). O TCC não informa quantas combinações foram testadas nem o resultado delas. O aluno deve ter essa lista pronta (por exemplo, CN-II com lambda 0,20, CN-II com lambda 0,05, CN-I com 0,20...) e dizer qual foi o critério (viés de volume). Ressalva importante: mesmo com a configuração escolhida pelos dados, o MC ficou pior que o modelo simples com a chuva. Então o otimismo, se existe, não muda a conclusão principal. A palavra "um pouco" (3.4.6) não foi medida; melhor dizer "tendem a ser otimistas, em grau não estimado".
(d) Risco: alto.

### 8. Woodward em cima do CN-I: dupla redução e CN equivalente de cerca de 34
(a) "Você baixou o CN para a condição seca e depois ainda aplicou Woodward, que aumenta S. A retenção média ficou em 490 mm, o que equivale a um CN perto de 34 numa bacia úmida. Isso é plausível? E a fórmula de Woodward foi obtida com CN tabelado em condição média, não com CN-I."
(b) Seções 2.3, 3.4.1.3 (S0,05 médio de 489,9 mm; 8,4% dos pixels com CN-I abaixo de 35; extrapolação), 4.6.
(c) Resposta sugerida: o texto reconhece a extrapolação (8,4% dos pixels e eventos 1 e 12) e cita Baert et al. (2026), com NSE de -0,87 usando Woodward (2.3 e 4.6). Defesa possível: o valor só é "absurdo" se for lido como propriedade física do solo. Como o coeficiente de escoamento direto medido é de cerca de 10%, um CN efetivo baixo é coerente com os dados. Mas a combinação não tem base física por evento; é um ajuste. Dizer isso claramente.
(d) Risco: médio a alto.

### 9. Pico local sem roteamento, e o MFM não força o pico
(a) "No MFM você força o volume, mas não o pico. Williams depende do pico. Seu pico é Q_k x RI/R, um número por evento que nem vem do hidrograma. Por que não usar o pico medido? Você testou o modelo sem o termo de pico?"
(b) Seções 3.4.3 ("o pico local não traz informação espacial além da que já está no escoamento"), 3.4.4, Tabela 2 (Q pico medido existe).
(c) Resposta sugerida: o texto explica que, como RI/R é único por evento, o pico só dá mais peso aos eventos de chuva concentrada (3.4.3). O TCC não testa o efeito do termo RI/R nem do pico medido. Resposta honesta: "Segui Hao et al. para manter o método. O pico entra como (RI/R)^0,56 por evento. Não testei separadamente quanto ele melhora ou piora." Também é bom corrigir: o MFM não representa "o escoamento estimado corretamente", só o volume.
(d) Risco: médio a alto.

### 10. Carga total contra erosão de encosta movida só por escoamento direto
(a) "Você calcula erosão só com o escoamento direto, mas calibra contra a carga total, que inclui sedimento que passa durante a vazão de base, do leito e das margens. Isso é coerente? Que fração da carga é de canal?"
(b) Seções 3.2 ("SYobs é a carga total do evento, incluindo a parcela transportada pela vazão de base"), 3.4.4, 4.6.
(c) Resposta sugerida: o texto admite a hipótese ("admite-se que o sedimento gerado no evento foi mobilizado pelo escoamento superficial") e que o c absorve isso (3.4.4). Não há dado para separar as fontes (precisaria de fingerprinting ou de amostragem nas encostas). Dizer que é uma limitação e que, por isso, o c não é uma taxa de transferência física.
(d) Risco: médio.

### 11. Turbidez medida na ETA da SABESP
(a) "A turbidez é medida na estação de tratamento, em água bruta captada. Qual a distância e o tempo de viagem até a seção? Os picos dos eventos passam de 250 NTU? A curva foi feita com quantas amostras nessa faixa? Qual a incerteza na carga?"
(b) Seções 2.5 ("nas turbidezes mais altas... a curva tem a maior incerteza"), 3.2, 4.6 (5.ª fonte, "essa incerteza não foi estimada").
(c) Resposta sugerida: a curva vem de Murillo-Bermúdez et al. (2023), com regressão por partes e quebra em 250 NTU (2.5). O TCC não traz o número de amostras, a faixa coberta, a defasagem nem a incerteza; apenas reconhece a limitação (4.6). O aluno deve ler o artigo de 2023 antes da defesa para responder com números, ou dizer claramente que usou a série de CSS pronta.
(d) Risco: médio.

### 12. "Por construção" e correlação espúria
(a) "Você diz que qualquer modelo com o volume acerta a carga 'por construção'. Carga é volume vezes concentração, então regredir carga contra volume tem o volume dos dois lados. Isso é correlação espúria, não acerto. E o seu R² de 88% vem daí."
(b) Seção 4.3 ("Qualquer modelo que receba o volume medido acerta, por construção, a ordem de grandeza da carga"); Figura 11.
(c) Resposta sugerida: concordar e ajustar a palavra. Não é "por construção"; é porque, nesses 17 eventos, a concentração média varia pouco (variância do log de 0,08 contra 0,66 do volume; 4.3). Esse é justamente o argumento do TCC: o bom resultado do MFM não valida a MUSLE, porque está dominado pelo volume. Melhor dizer "em grande parte por causa do volume" do que "por construção".
(d) Risco: médio.

### 13. Comparação com Vivarelli et al. (2025) é justa?
(a) "Você compara a sua validação cruzada com o ajuste do modelo concentrado nos próprios dados. E o modelo concentrado tem K, LS e C constantes: na prática é uma curva de potência de D x qp com dois parâmetros. Que conclusão dá para tirar?"
(b) Seções 3.4.8 e 4.3 ("a comparação é só indicativa"); Resumo e Conclusões ("da mesma ordem").
(c) Resposta sugerida: o texto já diz que é indicativa (4.3). Acrescentar: como K, LS e C médios são constantes, o modelo concentrado é de fato uma regressão de potência sobre volume total e pico; ele ter 100% em fator 2 no ajuste não mostra que a MUSLE concentrada é melhor. A única conclusão segura é que a espacialização não piora o erro quando recebe o volume medido, e acrescenta o mapa.
(d) Risco: médio.

### 14. Seleção e delimitação dos eventos
(a) "Como esses 17 eventos foram escolhidos? São os mesmos de Murillo-Bermúdez e Martim (2022), com pico acima de 10 m³/s? As janelas vão de 23 a 149 horas e foram feitas a olho. Os eventos 15 e 16 estão praticamente colados. A recessão de um não entra no outro?"
(b) Seções 2.5 (17 eventos com vazão de pelo menos 10 m³/s), 3.2 (Tabela 2), 4.6 (1.ª fonte).
(c) Resposta sugerida: o TCC não diz explicitamente o critério de seleção nem se os 17 eventos são os mesmos de 2022. Os picos da Tabela 2 vão de 10,3 a 30,4 m³/s, o que sugere que sim. O aluno deve confirmar com o orientador e dizer. Sobre as janelas, o texto admite a delimitação manual como limitação sem quantificação (4.6). Para 15 e 16, reconhecer que a separação é difícil e que parte da recessão de 15 pode estar no volume e na carga de 16.
(d) Risco: médio.

### 15. Fatores K e C de outros lugares
(a) "O K e o C vêm de trabalhos no Rio Grande do Sul, no cerrado goiano, no oeste paulista. O C de campo é 0,05, o mesmo da média da bacia. Mineração e afloramento com C = 1. Urbano com C = 0 e K = 0. Quanto o mapa de classes depende disso?"
(b) Tabelas 5 e 6; seções 3.3, 4.5 ("a mineração e o solo exposto aparecem em destaque em parte porque têm C = 1 adotado"), 4.6 (7.ª fonte).
(c) Resposta sugerida: o texto diz que os valores foram adotados de Vivarelli et al. (2025) e não recalibrados (3.3), e que o mapa é "relativo sob os valores adotados" (4.6). Como K e C são constantes no tempo, não dá para calibrá-los com dados do exutório (ver pergunta 3). Admitir que a ordem entre lavoura, silvicultura e campo depende diretamente dos valores de C (0,212; 0,121; 0,050). Afloramento rochoso com C = 1 é estranho fisicamente; explicar que tem área praticamente nula.
(d) Risco: médio.

### 16. Área de contribuição limitada a 200 m no LS
(a) "Por que 200 m? Você testou 100 ou 300 m? O LS médio de 7,8 é alto. Quanto do mapa crítico muda com esse limite?"
(b) Seções 3.3 e 3.4.1.2.
(c) Resposta sugerida: o texto justifica o limite pelo fato de a USLE não valer em canal (3.4.1.2), mas não justifica o número 200 nem traz sensibilidade. Resposta honesta: "escolhi um valor comum para comprimento máximo de encosta. Não testei a sensibilidade; o valor afeta a intensidade do mapa, mas não as métricas no exutório, porque o LS é constante no tempo e vai para o c." (Esta última parte é correta pelo próprio raciocínio do TCC, 4.2.)
(d) Risco: médio.

### 17. Chuva: dois postos, pesos 0,307/0,693 e IDW
(a) "De onde vêm os pesos 0,307 e 0,693 da lâmina R? Se é Thiessen, por que nos pixels você usa IDW e não Thiessen? E RI vem do posto mais intenso, R da média: no evento 12, RI/R = 1,38. Isso é coerente?"
(b) Seções 3.4.1.4 ("Ela corresponde à média ponderada dos dois postos com pesos de 0,307 e 0,693"), 3.4.3, 4.6 (2.ª fonte).
(c) Resposta sugerida: o TCC não diz de onde vêm os pesos; diz só que R é "a da planilha de eventos". O aluno deve saber a origem (provavelmente Thiessen ou a fração de área). Sobre RI/R maior que 1, o texto já diz que é tratado como índice e não como fração (3.4.3). Admitir a mistura de fontes. Como o RI/R é por evento e entra com expoente 0,56, o efeito é um fator por evento.
(d) Risco: médio.

### 18. Expoente 1,12 fixo contra 0,94 observado
(a) "Seu modelo faz a erosão crescer com Q^1,12, mas a carga medida cresce com o volume elevado a 0,94. Por que manter os coeficientes de Williams em vez de calibrar o expoente, como fizeram Avanzi e o próprio Vivarelli?"
(b) Seções 2.2, 3.4.3, 4.2, 4.6 (6.ª fonte).
(c) Resposta sugerida: a escolha foi manter um só parâmetro calibrado, para reduzir o otimismo com 17 eventos (2.8, 3.4.5). O texto reconhece que 1,12 é maior que 0,94 (4.6) e que isso amplia um pouco o erro do escoamento (4.2). Calibrar o expoente aproximaria o MFM do modelo simples com Vdir, mas continuaria sem testar K, LS e C.
(d) Risco: médio.

### 19. Promessa de cenários futuros
(a) "Na justificativa você diz que o modelo pode gerar predições de cenários futuros. Com 81% de erro mediano com a chuva, ele pode?"
(b) Seção 1.2 ("podendo gerar predições de cenários futuros"); 4.2.
(c) Resposta sugerida: dizer que, em valor absoluto, não, com estes dados. Em termos relativos (trocar o C de uma classe e ver como muda a erosão local), o mapa pode indicar tendências, mas sem validação espacial. Melhor tirar a frase ou reescrevê-la como possibilidade futura.
(d) Risco: médio.

### 20. Tendência dos erros do MFM ao longo da série
(a) "Os primeiros eventos são superestimados e os últimos, subestimados. Isso não indica mudança na curva de turbidez, no sensor, no uso do solo ou na disponibilidade de sedimento? Você investigou?"
(b) Seção 4.3 ("A causa não foi identificada"); 4.6.
(c) Resposta sugerida: o texto admite que não identificou a causa. Hipóteses possíveis: troca ou deriva do turbidímetro, nova calibração da curva, esgotamento ou renovação de sedimento ao longo da estação chuvosa, obras. Também vale notar que a concentração média por m³ de escoamento direto é mais alta nos últimos eventos (cerca de 1.600 a 1.900 mg/L nos eventos 13 a 16 e 3.800 mg/L no 17, contra cerca de 1.100 a 1.650 mg/L nos eventos 1 a 6; conta feita com a Tabela 3). Não afirmar uma causa.
(d) Risco: médio.

### 21. Evento 17
(a) "O evento 17 tem 3.806 mg/L por m³ de escoamento direto, quase o dobro dos outros. Você olhou o hidrograma, o turbidograma, se houve saturação do sensor ou alguma obra?"
(b) Seção 4.3.
(c) Resposta sugerida: o TCC manteve o evento "porque não há base para excluí-lo" e mostra que as conclusões não mudam sem ele (4.3). Boa resposta. Cuidado: "3.806 mg/L" é carga dividida por volume de escoamento direto, não uma concentração medida; dizer isso se perguntarem.
(d) Risco: baixo a médio.

### 22. Por que falar de histerese se o modelo não usa?
(a) "Você dedicou um parágrafo à histerese. Onde ela entra no modelo?"
(b) Seção 2.5.
(c) Resposta sugerida: ela justifica por que a carga foi obtida somando Q x CSS hora a hora a partir da turbidez, e não por uma curva-chave instantânea de vazão contra concentração (2.5, última frase). Ela não entra no modelo de erosão, que é por evento.
(d) Risco: baixo.

### 23. Escalas diferentes dos dados
(a) "Pixel de 30 m, solos do CN em 1:250.000, uso de 2020 para K e C e MapBiomas 2022 para o CN. Qual é a resolução efetiva do seu mapa?"
(b) Seções 3.3 e 4.6.
(c) Resposta sugerida: o texto reconhece as duas coisas (3.3). A resolução efetiva é a do dado mais grosseiro em cada fator: o LS tem detalhe de 30 m, mas o solo (e, portanto, K e parte do CN) não. As manchas críticas devem ser lidas como regiões, não como pixels.
(d) Risco: baixo a médio.

### 24. Métricas: por que não o NSE linear como principal?
(a) "Por que usar mediana do erro e fator 2 em vez do NSE linear, que é o padrão da área?"
(b) Seções 2.8 e 3.4.7.
(c) Resposta sugerida: o evento 15 responde por 48,7% da soma dos quadrados (3.4.5) e dominaria o NSE linear. Com 17 eventos, métricas relativas são mais estáveis. O texto informa o NSE linear do modelo concentrado (0,83), mas não o do MC e do MFM na Tabela 13. Ter esses números à mão.
(d) Risco: baixo.

---

## Parte 2. Pontos fracos mais sérios (visão do especialista)

1. **O mapa de áreas críticas não foi validado e depende muito dos dados menos confiáveis.** Não há medição dentro da bacia, não há conectividade, e cerca de 63% da variação espacial em escala log vem do escoamento (dois postos, um fora da bacia, e CN de base nacional). O produto principal do trabalho (o mapa) é justamente a parte que não pôde ser testada (4.5, 4.6).

2. **A contribuição da MUSLE não é identificável com estes dados.** K, LS e C são constantes no tempo, o c absorve escala, unidades, transferência e erro, e o MFM não se distingue de SY = c x Vdir. O trabalho mostra o peso do escoamento, mas não mostra que a fórmula de erosão acrescenta algo no exutório (4.3, Conclusões).

3. **A configuração hidrológica foi escolhida com os mesmos dados e tem pouca base física.** CN-I na estação chuvosa, lambda 0,05 e conversão de Woodward em extrapolação. Não há validação aninhada, não há lista das configurações testadas, não há análise de sensibilidade. O LOO de um só parâmetro quase não protege contra o otimismo (3.4.1.3, 3.4.6).

4. **Toda a cadeia depende de uma separação de vazão de base que não foi testada.** BFImax = 0,70 acima da referência para rocha cristalina. Muda Vdir, o MFM, o modelo simples e a própria escolha do CN (3.2, 4.6).

5. **Entrada de chuva muito pobre e incoerente.** Dois postos, um fora da bacia; R ponderado com pesos de origem não explicada; RI do posto mais intenso; RI/R maior que 1 em dois eventos (3.4.1.4, 3.4.3).

6. **Uso da fórmula de Williams fora da sua escala e com unidades misturadas.** Q em mm vezes área em m², coeficientes de bacia aplicados em pixels de 900 m², expoente efetivo 1,12 contra 0,94 observado. O resultado só funciona porque tudo vai para o c (3.4.3).

7. **A variável observada também é uma estimativa com incerteza não medida.** CSS por turbidez medida na ETA, curva com maior incerteza nos picos, e carga total que inclui fontes de canal e o período de vazão de base (2.5, 3.4.4, 4.6).

8. **Amostra pequena e curta.** 17 eventos em 16 meses, um só fora da estação chuvosa (evento 11), sem teste independente em outro período. O próprio texto diz que as conclusões são qualitativas (4.6).

---

## Parte 3. Inconsistências, números que não batem, termos ambíguos e afirmações fortes demais

1. **Seção 3.4 (descrição do MFM):** "mostra o desempenho que a mesma formulação de erosão atingiria se o escoamento fosse estimado corretamente pelo método SCS-CN". Forte demais: o MFM força só o volume total do evento; a distribuição espacial e o pico continuam vindo do SCS-CN e de RI/R. A seção 3.4.4 é mais correta ("apenas distribui no espaço o volume medido").

2. **Seção 4.3:** "Qualquer modelo que receba o volume medido acerta, por construção, a ordem de grandeza da carga." Não é "por construção"; é um resultado empírico (concentração média pouco variável nestes eventos). Sugestão: "em grande parte por causa do volume".

3. **Seção 4.1:** "O método superestima o escoamento nos eventos de maior chuva (3, 8, 9 e 13 a 17) e subestima nos de menor chuva", chamado de "sentido sistemático". Os dados não são tão limpos: o evento 11 (74,0 mm) é subestimado (0,67), enquanto os eventos 3 (65,4 mm) e 17 (65,6 mm) são superestimados; o evento 5 (60,9 mm) também é subestimado. Melhor dizer "tende a".

4. **Tabela 2, evento 16:** R = 97,7 mm, mas 0,307 x 63,6 + 0,693 x 113,6 = 98,2 mm. Nos outros 16 eventos a conta bate (diferença de até 0,1 mm). Conferir.

5. **Seção 3.4.1.4:** a origem dos pesos 0,307 e 0,693 não é explicada, e não coincide com o IDW usado nos pixels (a média da chuva interpolada no evento 11 é 73,5 mm contra R = 74,0 mm; Apêndice A). Dizer de onde vêm (Thiessen? planilha do orientador?).

6. **Seção 3.4.3:** "com Q_k em mm, pr,k em m³/s e Apix em m²". O produto não é volume vezes pico (mm x m² = 1.000 x m³). Não muda os resultados, porque vai para o c, mas vale uma frase explicando.

7. **Seção 4.6 (6.ª fonte) e seção 3.4.4:** o c "faz o papel de uma taxa de transferência de sedimentos média". Mas o c tem unidade "t por unidade de E_unit" e absorve escala e unidades; não é uma taxa adimensional. A própria seção 3.4.4 diz que ele "não deve ser lido isoladamente como uma taxa de transferência física". Os dois trechos puxam em direções diferentes.

8. **Resumo e Conclusões:** "sobretudo sobre Cambissolos e em declividades acima de 20%". Os Cambissolos ocupam 68,6% da área e as declividades acima de 20% ocupam 65,0%; respondem por 92,9% e 78,3% da erosão. A concentração existe, mas é moderada; "sobretudo" pode soar mais forte do que é. A concentração forte é por uso (lavoura e solo exposto).

9. **Tabelas 14 e 15, coluna "Erosão por área, MC":** sem unidade e sem explicação. Pelas contas, é um índice com média da bacia = 100 (campo: 37,4 / 29,0 = 1,29, ou seja, 129). Escrever isso no texto ou no título da coluna.

10. **Seção 1.2:** "podendo gerar predições de cenários futuros". Não é sustentado pelos resultados do MC (81% de erro mediano).

11. **Objetivo específico 3 (1.3.2):** "Validar o modelo distribuído por meio da técnica de validação cruzada". A validação é só no exutório e só do c; o modelo distribuído (o mapa) não é validado. Sugestão: "avaliar no exutório".

12. **Seção 3.4.6:** "as métricas da validação cruzada tendem a ser um pouco otimistas". O "um pouco" não foi medido. Sugestão: "tendem a ser otimistas, em grau não estimado".

13. **Seção 4.2:** "o erro do cálculo de escoamento superficial pelo método SCS-CN explica 91% da variância do erro da descarga". Isso é quase automático pela formulação (E proporcional a Q^1,12, com K, LS e C fixos e c único). Não é errado, mas é apresentado como achado; seria bom dizer que é esperado pela estrutura do modelo, como o texto faz em parte no parágrafo seguinte.

14. **Seção 2.4:** "Eckhardt (2005) sugeriu valores... (ECKHARDT, 2012)". Mistura duas citações na mesma frase; deixar claro qual trabalho traz os valores 0,80, 0,50 e 0,25.

15. **Seção 3.1:** "sem estação seca pronunciada, com chuvas concentradas entre outubro e março". As duas ideias soam contraditórias para quem lê; explicar (chove o ano todo, mas a maior parte no verão).

16. **Seção 3.2:** "o volume TR é exatamente a soma das vazões horárias na janela". Falta o "x 3.600 s" (soma das vazões vezes o passo de tempo).

17. **Seção 4.1 contra Tabela 11:** o f do evento 10 é dado como 9,75, mas 552 / 57 = 9,68 com os valores da tabela. Provavelmente é arredondamento (valores sem arredondar); não é erro, mas um avaliador atento pode perguntar.

18. **Seção 2.6 contra 2.8:** em 2.6, Hao et al. (2022) têm NSE de 0,70 a 0,83 "no ajuste"; em 2.8, diz-se que eles usaram leave-one-out. Deixar claro se os 0,70 a 0,83 são do ajuste ou da validação.

19. **Seção 4.6 (6.ª fonte):** "relação observada nesta bacia entre carga e volume (0,94)". Não diz se é o volume total ou o escoamento direto (pelas tabelas, os dois dão perto de 0,93), nem onde esse número foi calculado no texto.

20. **Seção 4.3 (evento 17):** "carga por metro cúbico de escoamento direto é de 3.806 mg/L". Está em unidade de concentração, mas é carga total dividida por volume de escoamento direto, não a concentração média do evento (que usaria o volume total). Termo ambíguo.

21. **Resumo:** "o erro da espacialização é da mesma ordem que o de uma formulação concentrada (22%)". No corpo (4.3) e nas Conclusões há a ressalva de que o concentrado é ajuste, sem validação cruzada; no Resumo essa ressalva não aparece.

22. **Tabela 6 contra Tabela 5:** "Afloramento Rochoso" aparece nos dois mapas, com C = 1,0 (0,0% dos pixels) e K = 0,0087 (0,1% dos pixels). Não é erro (são mapas diferentes), mas C = 1 para rocha é fisicamente estranho e merece uma frase. O mesmo vale para "Área Urbana" (13,7% no mapa de solos) e "Área Urbanizada" (14,1% no mapa de uso).
