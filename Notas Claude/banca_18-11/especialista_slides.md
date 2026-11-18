# Perguntas da banca: especialista em hidrologia e sedimentos

Base: apenas os 36 slides (imagens) e as falas do apresentador. O texto do TCC não foi lido. Quando digo "a apresentação não dá base", quer dizer que a resposta não está nos slides nem nas falas e o aluno precisa buscá-la no TCC ou nos scripts.

---

## 1. Perguntas prováveis (da mais provável/perigosa para a menos)

### P1. "Se a regra simples com o volume erra 16% e a MUSLE espacializada com o mesmo volume erra 21%, o que a MUSLE acrescenta? Por que eu usaria a MUSLE?"
- **Slides:** 24, 26, 30 (2ª conclusão).
- **Resposta sugerida:** "No exutório, nada que eu consiga medir: com 17 eventos, a diferença (+1,6 ponto; IC −5,5 a +10,4; p = 0,52) não se distingue de zero. O ganho da MUSLE espacializada não está na carga total, e sim no mapa: ela distribui a carga pelos pixels conforme K, LS, C e o escoamento local, o que a regra com o volume não faz. Mas reconheço que esse mapa não foi validado no espaço (slide 32)." Não tente defender que a MUSLE "é melhor" no total; os próprios slides mostram que não é.
- **Risco:** alto.

### P2. "As unidades da sua equação estão certas? No slide 18 você multiplica Q em mm por área em m² e por vazão em m³/s. Williams usa volume em m³. E esse c = 0,0344 'por unidade de E' tem que unidade?"
- **Slides:** 4 (Q em m³), 15 (Q em mm), 17, 18, 19.
- **Conta que a banca pode fazer:** no pixel de exemplo, 13,0 × 5,17·10⁻⁴ × 897 = 6,03, ou seja, Q entrou em mm. Em m³ seria 0,013 × 897 = 11,67 m³, e o termo (·)^0,56 fica cerca de 1000^0,56 ≈ 48 vezes menor. Como c é calibrado, o resultado final não muda, mas: (i) E deixa de estar em toneladas; (ii) com as unidades de Williams, a soma de E no evento 11 daria cerca de 854 t, e o c "correto" seria cerca de 1,6 a 2,1, ou seja, **maior que 1**. Isso não pode ser uma taxa de transferência de sedimentos (que vai de 0 a 1).
- **Resposta sugerida:** "Q entrou em mm por conveniência; o fator de unidade (cerca de 1000^0,56) é constante e é absorvido por c, por isso as previsões e os mapas relativos não mudam. Por isso mesmo c não deve ser lido como taxa de transferência: ele junta o fator de unidade, o efeito de escala (Williams é para bacia inteira, aqui é por pixel) e o viés do escoamento." Convém corrigir o slide 19, que diz que c "faz o papel de uma taxa de transferência de sedimentos". A apresentação não dá base para defender essa leitura de c.
- **Risco:** alto (é fácil de conferir na hora com os números do slide 18).

### P3. "Suas áreas críticas ficam no centro e no oeste. A chuva interpolada também é maior no oeste. Com dois postos, um deles fora da bacia, isso não é um artefato da interpolação?"
- **Slides:** 14, 27 (63% do padrão vem do escoamento), 28, 31.
- **Conta que a banca pode fazer:** com S = 244 mm, Q a 63 mm de chuva ≈ 8,8 mm e a 79 mm ≈ 14,3 mm (+63%); elevado a 1,12, dá cerca de +73% de erosão só pelo gradiente de chuva do evento 11.
- **Resposta sugerida:** "Em parte, sim. O próprio slide 27 mostra que 63% da variação espacial (em log) vem do escoamento, ou seja, da chuva de dois postos e do CN, e eu digo que essa é a parte menos confiável do mapa. As manchas dentro de cada região vêm de K, LS e C (uso), mas a diferença leste–oeste é fortemente influenciada pelo gradiente de chuva. Para separar isso, eu teria que rodar o mapa com chuva uniforme e ver quanto as áreas críticas mudam." Se ele tiver esse teste no TCC, citar; a apresentação não mostra.
- **Risco:** alto.

### P4. "Você usou CN-I, condição seca, em todos os eventos, e λ = 0,05, escolhidos para acertar o volume total dos mesmos 17 eventos. Isso não é calibração disfarçada? E a validação cruzada não pega isso."
- **Slides:** 16 ("Limitação: escolhida olhando os mesmos 17 eventos"), 20, 22, 31.
- **Resposta sugerida:** "Sim, é uma escolha feita olhando os mesmos dados, e está escrito no slide 16 como limitação. A validação cruzada só deixa de fora o evento no ajuste de c; a escolha de CN-I e λ não foi refeita a cada rodada, então o MC está até otimista. Mesmo assim ele erra 81% na mediana, o que reforça a conclusão de que a conversão chuva → escoamento é o gargalo." Esperar uma pergunta seguinte: "Por que condição seca se o evento 11 teve 12–14 mm nas 9 h antes e o evento 2 teve escoamento medido 3,3 vezes maior que o calculado?" Resposta: a umidade antecedente variou entre eventos e um CN fixo não acompanha isso (slide 31, item 3: a fração escoada não cresceu com a chuva, r = −0,01). A apresentação não diz se foi testado um CN variável pela chuva antecedente de 5 dias.
- **Risco:** alto.

### P5. "O resultado principal, 81% contra 42%, depende do critério de calibração. No seu slide de apoio, com critério linear o MC erra 45% e a regra com a chuva 39%. Por que você apresenta justamente o critério em que o MC fica pior?"
- **Slides:** 20, 21, 36.
- **Resposta sugerida:** "O critério em log foi escolhido antes, porque o evento 15 responde por 48,7% da variabilidade da carga e dominaria um ajuste linear, e porque minimizar o erro em log equivale a maximizar o NSE em log, a função objetivo de Hao et al. (2022). O que não muda com o critério: o MC erra de 40 a 81%, nunca fica melhor que a regra com a chuva de forma clara, e o MFM fica em cerca de 20% em qualquer critério." Admitir que o "81%" deve ser lido como "40 a 80%, conforme o critério", e que a frase "cerca de 3/4 do erro vem da hidrologia" (slide 31) também muda: com critério linear seria cerca de metade.
- **Risco:** alto se a banca vir o slide 36 ou perguntar sobre sensibilidade; médio caso contrário.

### P6. "Como foi feita a separação da vazão de base? BFImax = 0,70 é o valor de Eckhardt para aquífero poroso perene. Essa bacia é de embasamento cristalino. Com 0,25, seu 'escoamento direto medido' mudaria bastante."
- **Slides:** 13 (linha tracejada subindo até cerca de 5 m³/s), 22 (rodapé), 31 (item 4).
- **Resposta sugerida:** "Usei filtro digital com BFImax = 0,70 (o método só aparece no slide 31). Reconheço que o escoamento direto 'medido' depende dessa escolha e é incerto; isso afeta o MFM, a regra com o volume e a comparação do slide 22." A apresentação não diz qual filtro (provavelmente Eckhardt), qual α, nem por que 0,70, nem se houve teste de sensibilidade. O aluno precisa ter essa justificativa pronta, porque é um ponto clássico para um avaliador de hidrologia.
- **Risco:** alto.

### P7. "Como a turbidez virou concentração? Quantas amostras tem a curva, qual a faixa medida, qual o R²? Seu pico do evento 11 é cerca de 2.700 mg/L: isso está dentro da curva ou é extrapolação? O sensor satura? A captação da SABESP fica no mesmo ponto da estação de vazão?"
- **Slides:** 12, 13, 32.
- **Resposta sugerida:** os slides só dizem "convertida por curva de calibração" e "curva turbidez × CSS sem incerteza estimada" (slide 32). A apresentação **não dá base** para responder número de amostras, faixa, R², extrapolação, saturação ou posição da captação. Preparar essas informações (provavelmente de Murillo-Bermúdez e Martim, 2022, ou Murillo-Bermúdez et al., 2023) e, se possível, dizer quanto a carga mudaria com a faixa de confiança da curva.
- **Risco:** alto (é a base de todo o dado observado de sedimento).

### P8. "A MUSLE estima erosão das encostas pelo escoamento superficial. Mas a carga que você mede inclui a parcela da vazão de base e, pelo laço horário, sedimento perto do canal. Você calibra c contra 100% da carga. Isso é coerente?"
- **Slides:** 13, 32, 35 (13 de 17 eventos com laço horário; 72% da carga na parcela do escoamento direto; pico de CSS 25 h antes do pico de vazão).
- **Resposta sugerida:** "Não é totalmente coerente, e c absorve essa diferença. No evento 11, cerca de 72% da carga está na parcela do escoamento direto (supondo a mesma concentração na vazão de base), e o laço horário indica sedimento disponível perto do canal. O modelo não representa nem fonte do canal nem dinâmica dentro do evento; isso está nas limitações." Também lembrar que é só carga em suspensão; arraste de fundo não foi medido (a apresentação não fala disso).
- **Risco:** médio-alto.

### P9. "A carga é a soma de vazão × concentração, e o volume vem da mesma vazão. O R² de 88% entre carga e volume e o bom desempenho da regra com o volume não vêm em parte dessa variável em comum?"
- **Slides:** 24, 25 (volume explica 88%), 26, 35.
- **Resposta sugerida:** "Sim, existe correlação 'de construção' entre carga e volume, porque os dois usam a mesma série de vazão. Por isso digo que o MFM e a regra com o volume não são previsões: servem para isolar o efeito do escoamento (slide 23)." A apresentação não dá base para dizer quanto dessa correlação é espúria; um jeito de mostrar é comparar a concentração média do evento (carga/volume) com as variáveis do modelo.
- **Risco:** médio.

### P10. "No MFM você multiplica o escoamento de todos os pixels pelo mesmo f. Nos eventos pequenos, f é 6 a 10 (eventos 1, 4 e 10). Nesses eventos o SCS-CN só gera escoamento nos pixels de CN alto. Multiplicar esse padrão por 10 é fisicamente razoável?"
- **Slides:** 22 (dados do gráfico), 23.
- **Conta:** f = 224/36 ≈ 6,2 (ev. 1); 987/154 ≈ 6,4 (ev. 4); 552/57 ≈ 9,7 (ev. 10); no outro extremo, 0,46 (ev. 9) e 0,55 (ev. 15).
- **Resposta sugerida:** "Não é uma representação física; é um teste. O fator corrige o volume total, mas mantém o padrão espacial do SCS-CN, que nos eventos pequenos está concentrado nos pixels de CN alto. Por isso uso o MFM para a carga no exutório, e o mapa principal é o do MC. A coincidência de 94% entre MC e MFM é esperada, pois é o mesmo padrão; não é validação." A fala menciona que f é "limitado à chuva do pixel", mas o slide não; vale colocar no slide.
- **Risco:** médio.

### P11. "O seu pico local é Q vezes RI/R, um número igual para todos os pixels. Então ele não traz informação espacial. E no slide de apoio a intensidade explica 0% da carga. Por que manter o pico? Você testou sem ele?"
- **Slides:** 17, 22 (Q^1,12), 35.
- **Resposta sugerida:** "Mantive para seguir Hao et al. (2022). No espaço ele só torna a erosão proporcional a Q^1,12 em vez de Q^0,56; entre eventos dá mais peso a chuvas concentradas. Como a intensidade máxima sozinha não explica a carga, ele pode até piorar o MC." A apresentação não mostra o teste sem o pico. Se o aluno tiver, ótimo; se não, dizer que seria um teste simples a fazer.
- **Risco:** médio.

### P12. "Na dispersão do MC os pontos ficam acima da linha nos eventos grandes e abaixo nos pequenos: a inclinação em log é maior que 1. Um c multiplicativo nunca corrige isso. Por que não calibrou também o expoente 0,56, como fazem vários trabalhos com MUSLE?"
- **Slides:** 6 ("11,8 e 0,56 são os valores originais"), 20, 21.
- **Resposta sugerida:** "Com um único parâmetro multiplicativo, a calibração só corrige o viés; a ordem dos eventos (Spearman) e a forma do erro vêm da estrutura do modelo. Mantive 0,56 para não ajustar mais parâmetros com só 17 eventos e para testar a estrutura original. Calibrar o expoente compensaria o erro do SCS-CN, mas esconderia a causa." A apresentação não mostra se ajustar o expoente foi testado.
- **Risco:** médio.

### P13. "Williams ajustou a MUSLE com volume e pico de bacias inteiras. Somar a equação pixel a pixel não dá o mesmo que aplicá-la na bacia, por causa do expoente. Como você trata essa mudança de escala?"
- **Slides:** 10, 19.
- **Conta:** com N pixels iguais, Σ(v·q)^0,56 = N^(−0,12) × (V·Q)^0,56; com N = 153.855, isso é cerca de 0,24, ou seja, a soma dos pixels fica cerca de 4 vezes menor do que a equação aplicada na bacia.
- **Resposta sugerida:** "O slide 19 reconhece que a equação foi feita para bacias inteiras e que c absorve a diferença de escala. É o mesmo procedimento de Hao et al. (2022). Por isso o mapa deve ser lido em termos relativos." Ligar esta resposta à P2.
- **Risco:** médio.

### P14. "Você diz que o erro do escoamento explica 91% do erro do sedimento. Mas o seu modelo é praticamente sedimento ∝ Q^1,12. Isso não é verdade por construção?"
- **Slides:** 22 (nota), 31.
- **Resposta sugerida:** "Em grande parte, sim: a única outra variável que muda entre eventos é RI/R. O número mostra que o erro não vem da parte de erosão (K, LS, C, que são fixos), e sim do escoamento. A evidência independente é o MFM: trocando só o volume, o erro cai de 81% para 21%." Evitar apresentar os 91% como descoberta; apresentar como consequência esperada.
- **Risco:** médio.

### P15. "Por que IDW com dois postos? Com dois pontos, IDW é praticamente um gradiente linear. Não havia outros postos (CEMADEN, ANA, DAEE), radar ou produto de satélite?"
- **Slides:** 12, 14, 31.
- **Resposta sugerida:** "Eram os dois postos com registro horário no período. Com dois postos, a chuva vira um gradiente suave e núcleos de chuva entre eles não aparecem; é a primeira causa de erro que aponto no slide 31. Próximos passos: mais postos ou radar." A apresentação não diz se outras fontes foram procuradas nem como foi feita a "média ponderada" de 74,0 mm (slide 13): ponderada por quê?
- **Risco:** médio.

### P16. "Quais valores de C você usou para campo e silvicultura? Silvicultura costuma ter C baixo. E área urbana com erosão zero: na região de Atibaia e Mairiporã há loteamentos, obras e estradas de terra, que costumam ser grandes fontes de sedimento."
- **Slides:** 9, 18, 27, 29, 32.
- **Resposta sugerida:** "Os valores por classe vêm de Vivarelli et al. (2025), sem recalibração. Área urbana nula é hipótese, e está nas limitações. Solo exposto e mineração têm C = 1 e aparecem como as manchas mais fortes." A apresentação só mostra C = 0,212 para lavoura temporária; não dá base para os valores de campo e silvicultura nem para a unidade de K. Levar uma tabela com K e C por classe (pode ser slide de apoio).
- **Risco:** médio.

### P17. "Como foi calculado o LS? Qual MDE (SRTM, ALOS)? Houve limite de área de contribuição? 65% da bacia com declividade acima de 20% num MDE de 30 m me parece alto."
- **Slides:** 12, 18, 27.
- **Resposta sugerida:** "LS por Moore e Burch (1986), com o MDE de 30 m do USGS." A apresentação não diz qual MDE nem se houve limite de comprimento de rampa ou de área acumulada (sem limite, o LS explode nos fundos de vale). Preparar essas respostas.
- **Risco:** médio.

### P18. "Você reconhece que o mapa mostra onde a erosão é produzida, não onde o sedimento chega ao rio. Por que não usou um índice de conectividade (por exemplo, Borselli) ou uma taxa de transferência distribuída?"
- **Slides:** 19, 27, 32.
- **Resposta sugerida:** "Ficou fora do escopo; está nos próximos passos ('conectividade por pixel'). Com um c único, a transferência é igual em toda a bacia, por isso trato o mapa como de erosão produzida e relativo."
- **Risco:** médio.

### P19. "Como os 17 eventos foram escolhidos e delimitados? São de nov/2018 a fev/2020, com um buraco entre julho e dezembro de 2019. Eventos de 4 dias com vários picos, como o 11, são um 'evento' para a MUSLE?"
- **Slides:** 12, 13, 28 (datas só nos títulos pequenos), 31 (item 2).
- **Resposta sugerida:** "A delimitação foi manual e é uma das causas de erro: no evento 11, 12 a 14 mm caíram nas 9 h antes da janela e ficaram fora." A apresentação não dá o critério de seleção nem o período. Preparar: critério de início e fim, mínimo de chuva, disponibilidade simultânea dos dois postos, da vazão e da turbidez.
- **Risco:** médio.

### P20. "Seu trabalho anterior (Vivarelli et al., 2025), o modelo concentrado, tem as melhores métricas. O que este TCC traz de novo? E a comparação é justa, se o concentrado não teve validação cruzada e usa o pico medido?"
- **Slides:** 24, 26, 30.
- **Resposta sugerida:** "A novidade é a distribuição espacial (o mapa) e a separação de onde vem o erro: com chuva prevista, o problema está no escoamento. A comparação com o concentrado é só indicativa, como digo nos slides; os dois usam informação medida no exutório, nenhum é previsão a partir da chuva." Atenção: a 3ª conclusão (slide 30) diz que a espacialização "chega a um erro da mesma ordem do modelo concentrado", mas quem chega é o MFM, que usa o volume medido. Deixar isso explícito na fala.
- **Risco:** médio.

### P21. "O que é a 'regra simples com a chuva' exatamente? Carga = c × chuva média? Ela aparece pela primeira vez nos resultados."
- **Slides:** 21, 24, 26.
- **Resposta sugerida:** pela legenda do slide 24, é SY = c × chuva do evento, com c ajustado da mesma forma (log, validação cruzada). Serve como modelo de referência: um modelo físico precisa ser melhor que ela para valer a pena. Convém apresentá-la no método.
- **Risco:** baixo-médio.

### P22. "Com 17 eventos e uma validação cruzada que só reajusta um parâmetro multiplicativo, a validação cruzada quase não muda nada (1.406 contra 1.383 t no evento 11). Ela está testando o quê? E os valores de p, com tantos testes?"
- **Slides:** 20, 21, 24, 32, 35.
- **Resposta sugerida:** "Com um parâmetro, a validação cruzada é um teste honesto, mas fraco: mostra que o resultado não depende de usar o próprio evento no ajuste. O que realmente pesa é a estrutura do modelo. Por isso trato as conclusões como qualitativas e os valores de p como indícios (slides 32 e 35)."
- **Risco:** baixo.

### P23. "Por que as áreas críticas são os 5% de maior erosão? Se fossem 10%, as conclusões (46% da área, 83% da erosão) mudariam?"
- **Slides:** 27, 30.
- **Resposta sugerida:** "O limiar de 5% é uma escolha para destacar os pixels mais críticos." A apresentação não mostra sensibilidade ao limiar. Atenção: 46% → 83% se refere às três classes de uso, não às áreas críticas de 5%; a 4ª conclusão mistura as duas coisas.
- **Risco:** baixo.

---

## 2. O que a apresentação não explica bem ou explica de forma confusa

- **Slides 2 a 6:** cinco slides repetem o título para apresentar a equação. Falta a motivação: por que erosão importa na parte alta do Jundiaí (abastecimento, captação da SABESP, assoreamento), qual a lacuna e por que fazer em escala de evento e espacializada. Esses slides não têm anotação de fala.
- **Slide 4:** define Q como volume em m³, mas a partir do slide 15 Q está em mm, e no slide 18 entra em mm na fórmula. Notação inconsistente (ver P2).
- **Slide 5:** K, LS, C e P sem unidade; K = 0,0475 e 0,0351 aparecem no slide 9 sem unidade.
- **Slides 7 e 8:** o mesmo mapa duas vezes (no 7 ele é pequeno e ilegível; o 8 não tem cabeçalho). A área da parte alta (138,8 km²) só aparece na legenda do mapa.
- **Slide 9:** está como "Introdução", mas é material (dados de entrada). Afirma que os Cambissolos têm a maior erodibilidade sem fonte.
- **Slide 10:** "Obtenção de dados espaciais além de hidrossedimentológicos" é vago. "Método de Hao et al. (2022)" é citado sem explicar o que ele é. "Pixels de cerca de 30 m" e depois "897 m²": dizer que é 29,95 m × 29,95 m.
- **Slide 11:** só há o objetivo geral. Os resultados giram em torno de comparar modelos (MC, MFM, regras simples, modelo concentrado) e de achar a origem do erro, o que não aparece no objetivo. A banca vai notar que o objetivo e as conclusões não se encontram.
- **Slide 12:** não diz o período dos dados, quantos eventos (17 aparecem no gráfico sem explicação) nem como foram escolhidos. Siglas não definidas: DBT5, DAEE, SAISP, SABESP, CSS (só em parênteses), MDE, USGS. O gráfico usa vírgula como separador de milhar (4,500), padrão inglês. A curva turbidez × CSS não é mostrada.
- **Slide 13:** aparece a vazão de base, mas o método de separação só é citado no slide 31. "Média ponderada dos 2 postos" sem dizer o peso. Datas sem ano. "1.479 mil m³" é confuso (melhor "1,48 milhão de m³" ou "1.479 × 10³ m³").
- **Slide 14:** IDW com dois postos não é justificado; o expoente 2 não é comentado.
- **Ordem dos slides 15 e 16:** o slide 15 usa S = 244,2 mm e λ = 0,05, que só são explicados no slide 16. Inverter.
- **Slide 15:** a escala de cores do mapa deixa quase tudo branco; não dá para ver o padrão. Os 67% são citados sem dizer que o volume total dos 17 eventos fica em +3% (isso só aparece depois).
- **Slide 16:** não explica por que a condição seca (CN-I) foi escolhida. O "viés de +3%" é um resultado mostrado no método. A relação de Woodward foi deduzida para CN-II; aqui é aplicada sobre CN-I sem comentário. Diz "tabelado (uso × solo)", mas a fonte é o raster BR_CN-2022, que tem seu próprio mapa de uso e solo, diferente do mapa usado para K e C.
- **Slide 17:** o conceito de "pico local" é difícil e o slide diz que ele "não traz informação espacial nova" sem explicar por que, então, entra no modelo. "RI" e "R" não são definidos (RI = intensidade máxima em 1 h; R = chuva do evento). A unidade "/h" de RI/R aparece sem explicação.
- **Slide 18:** E_unit não tem unidade. O mapa não tem barra de cores ("valor relativo"). P = 1 sem justificativa.
- **Slide 19:** "SY_n" e "MC" aparecem antes de serem definidos. "c faz o papel de taxa de transferência de sedimentos" é contraditado pelas unidades (ver P2). "t por unidade de E" é uma unidade estranha.
- **Slide 20:** "o evento 15 responde por 48,7% da variabilidade" não diz de quê (soma dos quadrados dos desvios?). A diferença entre 1.406 t e 1.383 t não é comentada. "Modelo Calculado" é um nome pouco informativo.
- **Slide 21:** o eixo x (carga observada) não tem rótulo nem números. A "regra simples com a chuva" aparece pela primeira vez sem definição no método. O texto lê "MC × regra" (MC primeiro), mas no gráfico o MC está à direita. O padrão dos pontos (inclinação maior que 1) não é comentado.
- **Slide 22:** a dedução do Q^1,12 e os 91% só estão na fala. A frase "superestima as chuvas grandes e subestima as pequenas" não explica o evento 2 (escoamento grande, calculado com só 30%). Separador de milhar em padrão inglês.
- **Slide 23:** "f limitado à chuva do pixel" está só na fala. O c recalibrado (0,0222) não é comparado com o c do MC (0,0344).
- **Slide 24:** o gráfico não mostra a regra com o volume (16%), que é o melhor modelo da comparação; só aparece no quadro de texto. A legenda mistura três séries, mas cada grupo só tem duas. Isso pode parecer escolha conveniente de comparação.
- **Slide 25:** a explicação das métricas vem depois de os resultados já terem sido mostrados; deveria estar no método. O quadro de R² é vago ("o que explica a carga e o padrão do mapa").
- **Slide 26:** 41,9% aqui e 41,8% no slide 36 para o mesmo número.
- **Slide 27:** slide muito denso. A decomposição "37% dos fatores, 63% do escoamento, em escala log" não explica o método. "65% da área com encostas acima de 20%" é um dado forte, sem comentário. O r = 0,98 e os 94% são de comparações diferentes e confundem.
- **Slide 28:** os 17 mapas são pequenos demais para ler; as datas e as chuvas só estão nos títulos minúsculos. A escala de cores é em raiz quadrada e satura no percentil 99,5 (escrito em letra minúscula).
- **Slide 29:** repete o mapa de cima do slide 27; o mapa das áreas críticas aparece três vezes (27, 30 e o próprio 29 quase igual).
- **Slide 30:** a 4ª conclusão junta "sobre Cambissolos, em encostas acima de 20%" com "46% da área, 83% da erosão", mas esses números são só das três classes de uso. A 3ª conclusão atribui à "espacialização" um erro que é do MFM (com volume medido). Nenhuma conclusão responde diretamente ao objetivo do slide 11.
- **Slide 31:** "cerca de 3/4 do erro vem da hidrologia" é uma conta simples ((81 − 21)/81) que supõe que os erros se somam; com outro critério de calibração (slide 36) seria cerca de metade.
- **Slide 33:** o texto "[e-mail de contato]" ainda está como marcador. Preencher ou tirar.
- **Slide 34:** o aviso "[Opcional: confirme se o texto corresponde...]" ainda está no slide. Tirar antes da defesa.
- **Slide 36:** o rodapé mostra o nome de um script ("Scripts/_sensibilidade_criterio_calibracao_18-11.py"). Trocar por "elaborado pelo autor".

---

## 3. Pontos fracos da pesquisa visíveis na apresentação

1. **A hidrologia não funciona evento a evento.** O SCS-CN com dois postos e CN fixo erra 46% no escoamento e o MC erra 81% na carga, pior que uma regra simples com a chuva (14 de 17 eventos; NSE em log −0,69). O trabalho diagnostica bem o problema, mas não testa nenhuma correção (CN variável com a umidade antecedente, outra chuva, etc.).
2. **A contribuição da MUSLE não foi demonstrada.** Com o volume medido, ela não se distingue de carga = c × volume. Tudo o que a MUSLE acrescenta é o mapa, e o mapa não tem validação espacial.
3. **O mapa depende mais da parte menos confiável.** 63% do padrão espacial vem do escoamento (dois postos, um fora da bacia, e CN), K e C foram adotados sem recalibração, a área urbana é zero por hipótese e não há conectividade. As áreas críticas podem refletir em parte o gradiente de chuva interpolado.
4. **Calibração e validação misturadas.** CN-I e λ foram escolhidos olhando os mesmos 17 eventos; a validação cruzada só cobre c. O resultado principal do MC muda de 81% para 40–45% conforme o critério de calibração (slide 36). O modelo concentrado usado como referência não foi validado.
5. **Unidades e escala pouco cuidadas.** Q entra em mm onde a equação pede m³; c não tem significado físico (e, com unidades corretas, seria maior que 1), apesar de ser apresentado como uma taxa de transferência. O pico local é proporcional a Q e não acrescenta informação espacial.
6. **O dado observado de sedimento é incerto e não corresponde ao que o modelo representa.** Curva turbidez × CSS sem incerteza; só sedimento em suspensão; a carga inclui a parcela da vazão de base e fontes perto do canal (laço horário em 13 de 17 eventos); a separação da vazão de base (BFImax = 0,70) é discutível numa bacia cristalina e altera o "escoamento direto medido".
7. **Amostra pequena.** São 17 eventos em cerca de 15 meses, com delimitação manual. As diferenças de poucos pontos não são interpretáveis e os valores de p são só indícios, como o próprio aluno reconhece.

---

## 4. Melhorias concretas nos slides (pensando nos 20 minutos)

**Cortar ou juntar (ganha cerca de 3 a 4 minutos):**
- Juntar os slides 2 a 6 em um só: a equação com os termos coloridos e uma linha para cada grupo (grandezas físicas, índices, constantes). Usar o tempo economizado para um slide de motivação (por que importa, lacuna, pergunta da pesquisa).
- Juntar os slides 7 e 8: deixar só o mapa grande (slide 8), com cabeçalho e a área da bacia (138,8 km²) no texto.
- Juntar 15 e 16 em um slide (CN → S → Q, nessa ordem) ou pelo menos inverter a ordem.
- Cortar o slide 29 (repete o 27) ou o mapa de cima do 27. No slide 30, usar uma figura nova ou nenhuma, em vez de repetir o mapa das áreas críticas.
- Mandar o slide 34 para o apoio ou falar em uma frase depois dos agradecimentos.

**Acrescentar ou mudar:**
- **Objetivos (slide 11):** acrescentar 2 ou 3 objetivos específicos que batam com os resultados, por exemplo: (i) mapear a erosão por evento; (ii) avaliar o desempenho no exutório com validação cruzada; (iii) identificar se o erro vem do escoamento ou da fórmula de erosão. Fazer cada conclusão do slide 30 responder a um deles.
- **Dados (slide 12):** colocar o período (nov/2018 a fev/2020), o critério de escolha dos eventos e, numa linha, a curva turbidez × CSS (número de amostras, R², faixa). Definir as siglas ou tirá-las. Trocar o separador de milhar para o padrão brasileiro (4.500).
- **Evento 11 (slide 13):** escrever na tela como foi separada a vazão de base (filtro, BFImax = 0,70) e por que esse valor.
- **Unidades (slides 4, 17, 18, 19):** usar o volume do pixel (m³) na fórmula ou escrever claramente "Q em mm; o fator de unidade é absorvido por c". Tirar do slide 19 a frase de que c "faz o papel de taxa de transferência" e dizer que c é um coeficiente de escala sem significado físico direto.
- **Método:** criar um slide curto "Modelos comparados" logo depois da calibração, com os cinco modelos (regra com chuva, MC, regra com volume, MFM, concentrado), a entrada de cada um e a métrica principal. Mover o slide 25 (métricas) para o método, reduzido a três métricas (erro mediano, fator 2, NSE em log).
- **Slide 21:** pôr rótulo e números no eixo x ("Carga observada (t)"), deixar o MC à esquerda (mesma ordem do texto) e comentar a inclinação dos pontos.
- **Slide 24:** incluir a barra da regra com o volume (16%) no gráfico. É o resultado mais honesto do trabalho e a banca vai procurar por ela.
- **Slide 27:** dividir em dois slides ou cortar números. Deixar "46% → 83%" e "65% → 78%" e uma linha sobre o peso do escoamento (63%) com a ressalva da chuva de dois postos. Se houver, mostrar o teste com chuva uniforme (ver P3).
- **Slide 28:** escolher 4 eventos representativos (pequeno, médio, 11, 15) em tamanho legível, com a data e a chuva visíveis; os 17 mapas podem ir para o apoio.
- **Slide 30:** corrigir a 4ª conclusão ("campo, silvicultura e lavoura temporária ocupam 46% da área e geram 83% da erosão; as áreas críticas ficam sobretudo em Cambissolos e encostas acima de 20%") e a 3ª ("com o volume medido, a MUSLE espacializada chega a um erro da mesma ordem do modelo concentrado").
- **Slide 31:** trocar "cerca de 3/4 do erro" por "a maior parte do erro" e citar a faixa conforme o critério (slide 36).
- **Slides de apoio a preparar (não entram nos 20 minutos):** tabela de K e C por classe com unidades; curva turbidez × CSS; separação de vazão de base com outro BFImax; os 17 mapas por evento; teste com chuva uniforme ou sem o pico local, se existirem.
- **Limpeza final:** tirar o "[e-mail de contato]" (slide 33), o aviso "[Opcional: ...]" (slide 34) e o nome do script (slide 36); padronizar 41,9% / 41,8%.

**Tempo:** com os cortes acima, a apresentação cai de 34 para cerca de 26 a 28 slides principais, cerca de 45 s por slide. É uma folga razoável para os slides densos (20, 22, 26, 27).
