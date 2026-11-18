# Perguntas da banca: professor de hidráulica que não trabalha com erosão

Persona: professor de engenharia civil, área de recursos hídricos, do lado da hidráulica (canais, condutos, obras hidráulicas, saneamento). Conhece bacia, hidrograma, chuva e vazão. Não conhece MUSLE, SCS-CN em detalhe, sedimentos nem estatística de validação. Quer entender a lógica, as unidades, o porquê das escolhas e para que serve o resultado.

Base: apenas o texto final do TCC (TCC_texto_final.md). Quando um número abaixo não está escrito no texto e foi calculado a partir das tabelas, isso está indicado como "(conta feita a partir da Tabela X)".

---

## 1. Perguntas prováveis (da mais provável para a menos provável)

### P1. "Um modelo simples, chuva vezes um coeficiente, acertou mais que o seu. Então para que serve o seu modelo?"
- **O que motivou:** Resumo; Tabela 13; seção 4.3 (MC: erro mediano de 81%, 35% no fator 2; modelo simples com a chuva: 42%, 82%; o MC foi pior em 14 dos 17 eventos, p = 0,02).
- **Resposta sugerida:** "Para estimar só a carga total do evento no exutório, o modelo simples com a chuva é melhor, e o texto diz isso. O MC perde porque passa pelo SCS-CN, que erra a forma da relação chuva-escoamento: superestima as chuvas grandes e subestima as pequenas (seções 4.1 e 4.2). O modelo simples usa a mesma chuva, mas não passa por essa curva. O objetivo do trabalho não era ganhar do modelo simples no exutório. Era mapear onde a erosão acontece, e isso o modelo simples não faz (seções 4.5 e 5)." Ajuda deixar claro que esse resultado também é uma conclusão: ele mostra que o ponto fraco é a conversão da chuva em escoamento.
- **Risco:** alto.

### P2. "E com o escoamento medido, o seu modelo empatou com uma regressão entre carga e volume. A MUSLE acrescentou alguma coisa ao número?"
- **O que motivou:** seção 4.3 (MFM 20,6% contra modelo simples com o escoamento direto 15,9%; intervalo de confiança da diferença de -5,5 a +10,4 pontos; Wilcoxon p = 0,52); Figura 11.
- **Resposta sugerida:** "No número do exutório, não. A carga medida é o volume vezes uma concentração média, e entre os eventos o volume varia muito mais que a concentração (variância do log de 0,66 contra 0,08). Só o volume explica 88% da variação da carga. Qualquer modelo que receba o volume medido acerta a ordem de grandeza da carga. Por isso o texto diz que o bom resultado do MFM não valida a fórmula de erosão (seções 4.3 e 5). O que a MUSLE espacializada acrescenta é a distribuição da erosão dentro da bacia."
- **Risco:** alto.

### P3. "O mapa não foi conferido em nenhum ponto dentro da bacia. Como eu sei que as áreas críticas estão certas?"
- **O que motivou:** seções 4.5 e 4.6 (sétima fonte de incerteza) e 5 ("não puderam ser validados espacialmente"); correlação de 0,98 entre os mapas do MC e do MFM.
- **Resposta sugerida:** "Não dá para saber com os dados que existem: só há medição no exutório. O mapa é relativo, isto é, compara as áreas entre si, e depende dos valores de K e C tirados da literatura. A concordância entre MC e MFM (94% dos pixels críticos em comum) não valida nada, porque os dois usam o mesmo padrão espacial (seção 4.5). O que dá alguma confiança é o resultado bater com o que se espera fisicamente: lavoura, solo exposto e encosta íngreme erodem mais que mata em terreno plano. O próximo passo seria medir em sub-bacias ou conferir em campo ou com imagens (seção 5)."
- **Risco:** alto.

### P4. "Vazão de pico de um pixel de 30 m, sem nenhuma propagação? Isso não é uma vazão de pico."
- **O que motivou:** seção 3.4.3 (pr,k = volume do pixel x RI/R / 3.600, "sem roteamento hidráulico"); Apêndice A (pr = 5,17 x 10⁻⁴ m³/s).
- **Resposta sugerida:** "Concordo, não é uma vazão de pico no sentido hidráulico. É o volume escoado no pixel multiplicado por um índice de concentração da chuva (RI/R, um número por evento) e dividido por 3.600 para passar a segundos. O texto diz que, como RI/R é o mesmo em todos os pixels, o 'pico local' é proporcional ao escoamento e não traz informação espacial nova. A única função dele é dar mais peso aos eventos de chuva concentrada (seção 3.4.3). A forma segue Hao et al. (2022). Tanto não é um pico físico que nos eventos 1 e 12 RI/R passa de 1."
- **Risco:** alto (é o assunto da área do professor).

### P5. "Quais são as unidades do seu índice de erosão e do coeficiente c? Você multiplica milímetro por m³/s por m²."
- **O que motivou:** seção 3.4.3 ("com Q_k em mm, pr,k em m³/s e Apix em m²"); Tabela 7 (E_unit "índice relativo"; c em "t por unidade de E_unit").
- **Resposta sugerida:** "As unidades não fecham, e por isso o texto chama E_unit de índice relativo, e não de toneladas. A equação de Williams é empírica: os números 11,8 e 0,56 foram ajustados com volume em m³ e pico em m³/s de bacias inteiras. Aplicada a um pixel, ela fica fora da faixa em que foi ajustada, e a soma dos pixels não é igual ao que a equação daria para a bacia toda (a razão é n elevado a 0,12). Toda a conversão de escala e de unidade fica no c, que é calibrado com a carga medida (seções 3.4.3 e 3.4.4)." Vale ter uma frase pronta: "o c é o que transforma o índice em toneladas".
- **Risco:** alto.

### P6. "Você usou a condição de umidade seca (AMC I) em eventos de verão chuvoso, e o evento 16 começa 13 horas depois do fim do evento 15. Faz sentido?"
- **O que motivou:** seção 3.4.1.3 ("condição única para o conjunto de eventos, escolhida pelo volume"); Tabela 2 (o evento 15 termina em 09/02/20 às 01h e o evento 16 começa em 09/02/20 às 14h).
- **Resposta sugerida:** "Fisicamente, não. A condição seca não foi escolhida por medida de umidade. Ela foi escolhida porque, junto com λ = 0,05, fez o volume total calculado ficar próximo do medido (viés de +3%). O texto diz isso com todas as letras (seções 3.4.1.3 e 4.1). Na prática, o CN-I funcionou como um ajuste para compensar o CN tabelado, que daria escoamento demais. O caso 15-16 mostra a limitação de usar uma condição única para todos os eventos." O texto não comenta especificamente os eventos 15 e 16 colados.
- **Risco:** alto.

### P7. "Com só 2 pluviômetros, um deles fora da bacia, você consegue dizer onde chove mais?"
- **O que motivou:** seções 3.4.1.4, 4.1 (Figura 6), 4.5 e 4.6 (segunda fonte de incerteza).
- **Resposta sugerida:** "Não com detalhe. Com dois postos, o IDW sempre gera um gradiente suave entre eles, sem núcleos de chuva. O texto reconhece isso e diz ainda que, em escala logarítmica, cerca de 63% da variação espacial do mapa vem do termo de escoamento (chuva e CN), que é 'a parcela menos confiável do mapa' (seção 4.5). A melhoria proposta é usar mais postos ou radar (seção 5)." Número útil, que o texto não traz: os postos ficam a cerca de 29 km um do outro (conta feita com as coordenadas da seção 3.4.1.4).
- **Risco:** alto.

### P8. "A vazão de base deu quase metade do volume do evento, e você usou BFImax = 0,70 quando a referência sugere 0,25 para aquífero em rocha fraturada. Se fosse 0,25, o que mudaria?"
- **O que motivou:** seção 3.2 (base de 34% a 55% do volume, 47% no conjunto); seção 4.6 (quarta fonte de incerteza).
- **Resposta sugerida:** "A série de vazão de base veio junto com os dados de monitoramento. Eu só a reproduzi com o filtro de Eckhardt, e quem a reproduz é BFImax = 0,70. O texto reconhece que esse valor é bem maior que o sugerido (0,25) e que a série pode estar atribuindo à vazão de base parte do que seria escoamento direto (seção 4.6). Com um BFImax menor, o escoamento direto medido seria maior. Isso mudaria o MFM, o modelo simples com o escoamento e também a escolha de CN-I e λ, que foi feita para bater esse volume. Esse teste não foi feito; está entre as sugestões (seção 5)." Não dá para dizer quanto mudaria: o texto não quantifica.
- **Risco:** alto.

### P9. "Por que reduzir a abstração inicial (λ de 0,20 para 0,05) faz a retenção S quase dobrar, de 256 para 490 mm? Isso não é girar dois botões até dar o volume?"
- **O que motivou:** seções 2.3 e 3.4.1.3 (S0,20 médio de 255,7 mm; S0,05 médio de 489,9 mm); seção 3.4.6.
- **Resposta sugerida:** "O CN tabelado vale para λ = 0,20. Com λ = 0,05, o escoamento começa mais cedo, então, para a curva continuar coerente com os dados de onde o CN saiu, a retenção precisa ser maior. A relação de Woodward et al. (2003) faz essa conversão; é uma regressão com dados de bacias americanas (seção 2.3). E sim, a escolha da combinação CN-I, λ = 0,05 e S convertido foi feita olhando o volume dos mesmos 17 eventos. Por isso o texto avisa que a validação cruzada fica um pouco otimista e que uma validação aninhada seria o correto (seção 3.4.6)."
- **Risco:** médio a alto.

### P10. "Você mediu só sedimento em suspensão. E a carga de fundo?"
- **O que motivou:** seções 2.5 e 3.2 (carga obtida da turbidez); seção 3.4.4 ("carga total medida").
- **Resposta sugerida:** O texto não responde. Ele chama SYobs de "carga total", mas no sentido de incluir a parcela levada durante a vazão de base, não no sentido de suspensão mais fundo. Resposta possível: "O modelo foi comparado só com a carga em suspensão, que é o que foi medido; a carga de fundo não foi medida nem estimada. Em geral, a MUSLE é comparada com a carga em suspensão, mas isso é uma limitação que eu deveria ter escrito." Convém evitar um número para a fração de fundo sem uma referência.
- **Risco:** médio a alto (pergunta típica de quem é de hidráulica fluvial).

### P11. "A carga medida inclui o sedimento levado pela vazão de base, mas o seu modelo só usa o escoamento direto. Você não está comparando coisas diferentes?"
- **O que motivou:** seções 3.2 e 3.4.4 ("SYobs ... incluindo a parcela transportada pela vazão de base"; "parte da carga pode vir do canal e das margens").
- **Resposta sugerida:** "Sim, e o texto assume isso: toda a carga medida é comparada com a erosão das encostas vezes c. A hipótese é que o sedimento do evento foi mobilizado pelo escoamento superficial. A parte que vem do canal, das margens ou da vazão de base acaba dentro do c, que por isso não deve ser lido como uma taxa de transferência física (seções 3.4.4 e 4.6)."
- **Risco:** médio.

### P12. "Errar por um fator 2 é aceitável? Em hidráulica, errar o dobro é muito."
- **O que motivou:** seções 2.8 e 3.4.7; Tabela 13.
- **Resposta sugerida:** "Em sedimentos, a própria medição tem incerteza grande. Aqui a concentração vem da turbidez por uma curva de calibração (seção 2.5), e a carga varia de 199 a 3.829 t entre os eventos. O critério de fator 2 foi usado porque não depende do tamanho do evento e não é dominado pelo maior evento. Ele não diz que errar o dobro está bom: só serve para comparar modelos entre si." O texto não traz uma referência que diga qual erro é aceitável em modelagem de sedimentos; é bom ter uma pronta ou admitir isso.
- **Risco:** médio.

### P13. "Explique de forma simples o que é essa validação cruzada leave-one-out. E por que o ajuste e a validação deram quase o mesmo resultado?"
- **O que motivou:** seções 2.8, 3.4.6 e 4.2.
- **Resposta sugerida:** "Tiro um evento, calibro o c com os outros 16 e prevejo o evento que tirei. Repito isso para os 17. Assim, nenhum evento ajuda a calibrar o número que depois o prevê. Como só um parâmetro é calibrado, o c muda pouco de uma rodada para outra, e os resultados ficam parecidos (seção 4.2). O ponto fraco é que as escolhas de CN-I e λ foram feitas antes, com todos os eventos, e não foram refeitas em cada rodada. Por isso a validação é um pouco otimista (seção 3.4.6)."
- **Risco:** médio.

### P14. "Por que calibrar em logaritmo? E a soma dos 17 eventos bate com o total medido?"
- **O que motivou:** seção 3.4.5 (o evento 15 responde por 48,7% da soma dos quadrados); Tabela 12.
- **Resposta sugerida:** "O logaritmo mede o erro relativo, então um evento grande e um pequeno pesam parecido. Em escala linear, o evento 15 sozinho comandaria o ajuste (seção 3.4.5)." O texto não informa a soma simulada. Pela Tabela 12 (ajuste), o MC soma cerca de 37.300 t contra 23.846 t medidas (+56%), e o MFM soma cerca de 22.960 t (-4%) (conta feita a partir da Tabela 12). Para quem pensa em assoreamento de reservatório, o total importa. Vale ter esses números prontos e explicar que o MC superestima os eventos grandes, principalmente o 15 (10.361 t contra 3.829 t).
- **Risco:** médio.

### P15. "Que número é esse, 1.403 t por evento? É muito ou pouco? Quanto dá por hectare?"
- **O que motivou:** seção 3.2; Apêndice A (40,1 kg em um pixel).
- **Resposta sugerida:** O texto não dá nenhuma referência de comparação. Contas que ajudam (feitas a partir da seção 3.2 e do Apêndice A): 23.846 t em cerca de 13.800 ha dão cerca de 1,7 t/ha somando os 17 eventos, ou cerca de 0,1 t/ha por evento em média. O pixel de exemplo (40,1 kg em 897 m²) equivale a cerca de 0,45 t/ha só no evento 11. Seria bom comparar com algum limite de tolerância de perda de solo ou com valores de outras bacias, mas é preciso deixar claro que o mapa mostra erosão local, não o que chega ao rio.
- **Risco:** médio.

### P16. "Na prática, quem usaria isso e para quê? Que medida você recomendaria, e onde?"
- **O que motivou:** seção 4.5 (último parágrafo antes da área urbana); seção 5.
- **Resposta sugerida:** "Para priorizar onde começar medidas de conservação, em termos relativos: manchas de lavoura temporária e silvicultura sobre Cambissolo em encostas de 20% a 45%, na porção central e oeste, entre cerca de 3 e 12 km do exutório, além dos poucos pixels de solo exposto e mineração (seção 4.5). Medidas possíveis: práticas conservacionistas, recomposição da cobertura do campo e controle de solo exposto." Gancho para saneamento, que o texto não explora: a turbidez foi medida na captação da ETA da SABESP (seção 3.2), então reduzir sedimento interessa ao tratamento de água. O texto não estima quanto a carga cairia com essas medidas.
- **Risco:** médio.

### P17. "Na introdução você diz que o modelo pode prever cenários futuros. Com o MC errando 81%, dá para usar em cenário?"
- **O que motivou:** seção 1.2 ("podendo gerar predições de cenários futuros"); seção 2.8.
- **Resposta sugerida:** O texto não volta a esse ponto nos resultados. Resposta honesta: "Para o valor absoluto da carga, ainda não. Para comparar, em termos relativos, o efeito de mudar o uso do solo (trocar o C de uma área), o modelo pode indicar a direção da mudança, mas isso não foi testado neste trabalho." Talvez seja melhor tirar ou suavizar essa frase da introdução.
- **Risco:** médio.

### P18. "Por que manter os coeficientes 11,8 e 0,56 de Williams, se você mesmo diz que eles não valem para o pixel? O expoente não é absorvido pelo c."
- **O que motivou:** seções 3.4.3 e 4.6 (sexta fonte: expoente efetivo de 1,12 contra 0,94 observado entre carga e volume).
- **Resposta sugerida:** "O 11,8 é absorvido pelo c, mas o expoente não: ele define como a erosão cresce com o escoamento, entre pixels e entre eventos (E proporcional a Q elevado a 1,12). O texto reconhece que 1,12 é maior que a relação observada na bacia (0,94) e que isso amplia um pouco o erro do escoamento (seções 4.2 e 4.6). Recalibrar o expoente com 17 eventos acrescentaria um parâmetro, com risco de ajuste demais." O texto não diz explicitamente por que o expoente não foi recalibrado.
- **Risco:** médio.

### P19. "Por que a área de contribuição do LS foi limitada a 200 m? Por que 200, e não 100 ou 500?"
- **O que motivou:** seção 3.4.1.2.
- **Resposta sugerida:** "Sem limite, nos pixels de canal a área de contribuição chega a milhões de metros, e ali a USLE, que é uma equação de encosta, perde o sentido." O texto não justifica o valor de 200 m nem testa outros valores. Como o LS ajuda a definir onde ficam as áreas críticas (declividade acima de 20% concentra 78% da erosão), é bom ter uma justificativa ou admitir que é um valor adotado.
- **Risco:** médio.

### P20. "A área urbana tem erosão zero, e ela fica perto do exutório. E as obras, os loteamentos, as ruas de terra?"
- **O que motivou:** seção 4.5 (parágrafo da área urbana); Tabelas 5 e 6.
- **Resposta sugerida:** "É uma hipótese do modelo: C = 0 e K = 0 nas áreas urbanas. O texto reconhece que obras e solo exposto urbano podem ser fontes importantes e que essa simplificação pode jogar para as áreas rurais parte do sedimento que vem da cidade (seção 4.5). Com um mapa de uso mais detalhado, seria possível separar parques, solo exposto e superfície impermeável."
- **Risco:** médio.

### P21. "Onde exatamente se mediu a turbidez e onde se mediu a vazão? É o mesmo ponto? E a curva turbidez-concentração aguenta os picos?"
- **O que motivou:** seção 3.2 (vazão do DAEE; turbidez na ETA da SABESP, em água bruta); seção 2.5 (curva por partes com quebra em 250 NTU, maior incerteza nos picos).
- **Resposta sugerida:** O texto não diz a distância entre o ponto de captação da ETA e a seção do DAEE. Quanto à curva: "ela tem a maior incerteza justamente nas turbidezes altas, quando a carga é maior, e essa incerteza não foi estimada neste trabalho (seções 2.5 e 4.6)." Também é bom saber explicar por que a turbidez é horária e a vazão tem medição a cada 10 minutos (o trabalho usou tudo em passo horário).
- **Risco:** médio.

### P22. "O que é o coeficiente c fisicamente? E por que ele é diferente no MC (0,0344) e no MFM (0,0222)?"
- **O que motivou:** seção 3.4.4; Tabela 9.
- **Resposta sugerida:** "A ideia é que ele faça o papel de uma taxa de transferência média: a fração do que é erodido nas encostas que chega ao exutório. Mas, por ser calibrado, ele também absorve a mudança de escala da equação de Williams para o pixel e parte do erro do escoamento. A diferença entre os dois valores mostra isso: só o escoamento muda entre as versões, e o c muda junto. Por isso o texto pede que o valor não seja lido como uma taxa física (seção 3.4.4)."
- **Risco:** baixo a médio.

### P23. "O evento 17 tem uma concentração muito acima dos outros. Por que você não tirou?"
- **O que motivou:** seção 4.3 (3.806 mg/L contra 1.085 a 2.088 mg/L nos outros eventos).
- **Resposta sugerida:** "Não há base para excluir. As explicações possíveis são uma fonte de sedimento que o modelo não representa (obra, deslizamento) ou a incerteza da curva de turbidez nas concentrações altas. Sem ele, o MFM melhora (15,3% e 100% no fator 2), mas as conclusões não mudam (seção 4.3)."
- **Risco:** baixo.

### P24. "A comparação com o seu trabalho anterior (Vivarelli et al., 2025) é justa? Um foi validado e o outro não."
- **O que motivou:** seções 3.4.8 e 4.3 (o concentrado foi ajustado nos 17 eventos, sem validação cruzada).
- **Resposta sugerida:** "Não é uma comparação perfeita, e o texto chama de 'só indicativa'. O concentrado foi ajustado nos próprios eventos, então os números dele tendem a ser otimistas. O que dá para dizer é que, com o escoamento medido, a versão espacializada chega a um erro da mesma ordem (21% contra 22%) e ainda fornece o mapa (seções 4.3 e 5)."
- **Risco:** baixo.

### P25. "O que quer dizer que 37% do padrão vem de K x LS x C e 63% do escoamento? E por que isso muda em escala linear?"
- **O que motivou:** seções 3.4.9 e 4.5.
- **Resposta sugerida:** "Como a erosão do pixel é o produto de dois termos, um fixo (K x LS x C) e outro que depende da chuva e do CN, em logaritmo ela vira uma soma, e dá para ver quanto da variação entre os pixels vem de cada termo. Em log, o escoamento pesa mais; em escala linear, K x LS x C sozinho explica 58%. Ou seja, a conclusão depende da escala (seção 4.5). A mensagem prática é que o mapa não é só um mapa de K x LS x C: o gradiente de chuva e o CN também pesam, e essa é a parte menos confiável."
- **Risco:** baixo.

---

## 2. O que ficou difícil de entender para quem é de fora da área

**Siglas e termos sem explicação suficiente:**
- **SY, SDR, TR, E_unit, MC, MFM, AMC I/II/III, BFImax, Vdir, Bt:** muitas siglas. TR aparece em "volume TR" (seção 3.2) antes de ser definido; só fica claro na Tabela 7.
- **Fatores K, C, LS e P:** o texto diz o nome, mas não diz o que significa fisicamente um K de 0,039 ou um LS de 7,8, nem se esses valores são altos ou baixos. As unidades de K (t h MJ⁻¹ mm⁻¹) aparecem sem explicação.
- **Número de curva (CN), retenção S, abstração inicial Ia e λ:** para quem não é da área, não fica claro o que é "retenção potencial máxima" nem por que S muda quando λ muda (seção 3.4.1.3).
- **Classes de solo (Cambissolo Háplico, Argissolo Vermelho-Amarelo, Neossolo Litólico):** não há uma frase sobre o que as distingue nem por que o Cambissolo erode mais (o texto só cita o K maior).
- **Köppen Cfa/Cfb, Grupo Tubarão, embasamento cristalino:** aparecem sem tradução prática.
- **"Área de contribuição específica", "potência do escoamento", Moore e Burch:** a equação do LS não tem explicação intuitiva.
- **Conectividade de sedimentos e taxa de transferência de sedimentos:** são explicadas, mas a diferença entre as duas não fica clara.
- **Histerese e "laço em oito" (seção 2.5):** a ligação com o resto do trabalho não é evidente. Dá para entender que a seção serve para justificar não usar uma curva-chave instantânea, mas depois o modelo de volume funciona bem.
- **Estatística:** NSE em log, Spearman, MedAPE, fator 2, bootstrap, Wilcoxon, viés de otimismo, validação aninhada. Estão definidos, mas em sequência densa; um leigo precisa de um exemplo simples para cada um.
- **"Curva-chave de sedimentos com o escoamento direto" (seção 3.4.8):** em hidráulica, curva-chave relaciona cota e vazão; o uso aqui é diferente e não foi explicado.
- **IDW, raster, UTM/SIRGAS, reamostragem por vizinho mais próximo, MapBiomas, BR_CN-2022:** termos de SIG explicados de forma breve.

**Passos que parecem mágica:**
- **Pesos 0,307 e 0,693 da lâmina R (seção 3.4.1.4):** vêm "da planilha de eventos", sem dizer como foram calculados (Thiessen? área?).
- **Série de vazão de base "fornecida com os dados":** não diz por quem nem como foi feita originalmente; o trabalho só a reproduz.
- **Partição do R² "pela média dos ganhos nas duas ordens de entrada" (seção 3.4.9):** é um método estatístico que não foi nomeado nem explicado de forma intuitiva.
- **Razão "n elevado a 0,12" entre a soma dos pixels e a bacia inteira (seção 3.4.3):** aparece sem a dedução.
- **Fator f_n do MFM com o limite Q ≤ P:** entende-se a ideia, mas não fica claro por que o SCS-CN pode servir para distribuir o volume no espaço se ele erra o volume de cada evento.
- **Delimitação manual dos eventos:** não há critério escrito (início e fim no hidrograma).

**Números sem referência de comparação:**
- **Carga de 199 a 3.829 t por evento (média de 1.403 t):** não há valor por hectare, por ano nem comparação com outras bacias ou com limites de tolerância de perda de solo.
- **Mapas de erosão em t/pixel:** não há valor típico em t/ha nem limite de tolerância.
- **Coluna "Erosão por área, MC" nas Tabelas 14 e 15 (19, 129, 530, 1.772...):** a unidade não é dita. Parece ser um índice com a média da bacia igual a 100, mas o texto não diz.
- **c = 0,0344 e c = 0,0222:** não se sabe se são valores "razoáveis".
- **LS médio de 7,80 e K médio de 0,039:** sem comparação.
- **Coeficiente de escoamento dos eventos:** o texto fala dele (correlação de -0,01 com a chuva), mas não mostra os valores. Pelas Tabelas 2 e 11, o escoamento direto medido é de cerca de 1,6 a 16 mm, ou seja, coeficientes da ordem de 5% a 16% (conta feita a partir das tabelas). Um hidráulico vai querer ver esse número.

---

## 3. Pontos fracos e dúvidas sobre a utilidade prática

1. **O modelo preditivo (MC) perde para a referência mais simples.** Com só a chuva como entrada, ele é pior que "chuva vezes coeficiente" (seção 4.3). Para quem quer um número de carga, o trabalho não entrega uma ferramenta melhor do que já existe.
2. **A versão que funciona (MFM) depende de medir o volume no próprio evento.** Ela não é previsão, e mesmo assim não se distingue de uma regressão carga x volume (seção 4.3). A fórmula de erosão não foi testada de forma independente.
3. **O produto principal, o mapa, não foi validado.** É relativo, depende de K e C de literatura, de dois pluviômetros e de um CN nacional sobre solos em escala 1:250.000 (pixel de 30 m com mapa de solos muito mais grosseiro). Cerca de 63% do padrão (em log) vem justamente das partes menos confiáveis (seção 4.5).
4. **O mapa mostra onde o solo é erodido, não onde o sedimento chega ao rio.** Sem conectividade nem roteamento, uma área crítica longe da drenagem pode contribuir pouco para o rio, a ETA ou um reservatório (seções 3.4.4 e 4.5).
5. **As escolhas hidrológicas foram ajustadas com os mesmos dados:** CN-I, λ = 0,05, conversão de Woodward, além da vazão de base com BFImax = 0,70, bem acima do valor sugerido. A condição seca em eventos de verão, inclusive em eventos colados (15 e 16), é difícil de defender fisicamente.
6. **O "pico local" e as unidades da equação no pixel são frágeis do ponto de vista hidráulico.** O pico não é uma vazão; E_unit não tem unidade física, e tudo vai para o c.
7. **O que se mede e o que se modela não são a mesma coisa:** carga só em suspensão (sem carga de fundo), estimada por turbidez, incluindo a parcela da vazão de base e possíveis fontes de canal e margem, comparada com a erosão de encosta.
8. **A área urbana com erosão zero** pode distorcer a distribuição justamente perto do exutório, onde ficam as obras e os loteamentos.
9. **A amostra é pequena (17 eventos, 2018 a 2020).** As próprias conclusões são qualitativas (seção 4.6). Há uma tendência no tempo não explicada (MFM superestima os primeiros eventos e subestima os últimos).
10. **A promessa de simular cenários (seção 1.2) não foi demonstrada.** Não há nenhum cenário de mudança de uso nem estimativa de quanto a carga cairia com as medidas recomendadas.
11. **Falta o "e daí" para a engenharia.** O texto não liga o resultado a uma decisão concreta: assoreamento de reservatório, custo de tratamento na ETA, dimensionamento de bacias de retenção de sedimento, ou um ranking de sub-bacias para investir. Também não há valores em t/ha nem comparação com limites de tolerância.
12. **O total dos eventos no MC fica bem acima do medido** (cerca de +56% pela Tabela 12) por causa dos eventos grandes, o que pesa para qualquer uso em balanço de sedimentos, e o texto não comenta isso.

**Pontos fortes para o aluno usar na defesa:** a honestidade do texto sobre as limitações, a comparação com modelos simples (que poucos trabalhos fazem), a separação clara entre o erro do escoamento e o da fórmula (MC contra MFM) e o exemplo numérico completo no Apêndice A, que permite seguir o cálculo pixel a pixel.
