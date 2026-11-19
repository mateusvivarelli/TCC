# Fala da defesa em 20 minutos (rascunho de 18/11/2026)

Base: slides do arquivo `Apresentacao/slideTCC_18-11_sugestoes.pptx` (branch `claude/banca-04-11`, gerado pela sessão em nuvem), 36 slides; os números entre parênteses são o número do slide nesse arquivo. Ritmo de fala usado: 135 palavras por minuto. Números por extenso para facilitar a leitura em voz alta; confira a pronúncia de siglas.

Slides de apoio, fora do tempo (só se perguntarem): 8 (mapa grande), 26 (tabela de todos os modelos), 35 (histerese), 36 (critério de calibração).

| Slide | Parte | Alvo | Palavras | Tempo estimado |
|---|---|---|---|---|
| 1 | Capa | 0:20 | 49 | 0:21 |
| 2 | Título completo | 0:25 | 46 | 0:20 |
| 3 | MUSLE: equação e Williams (1975) | 0:30 | 52 | 0:23 |
| 4 | Q e Qp em destaque | 0:20 | 21 | 0:09 |
| 5 | K, LS, C e P em destaque | 0:35 | 73 | 0:32 |
| 6 | 11,8 e 0,56 em destaque | 0:25 | 30 | 0:13 |
| 7 | Área de estudo (mapa pequeno e depois grande) | 0:35 | 45 | 0:20 |
| 9 | Solo e uso | 0:25 | 43 | 0:19 |
| 10 | Espacialização | 0:40 | 96 | 0:42 |
| 11 | Objetivo | 0:20 | 45 | 0:20 |
| 12 | Dados e fontes | 0:50 | 114 | 0:50 |
| 13 | Evento 11 | 0:25 | 59 | 0:26 |
| 14 | Chuva em cada pixel (IDW) | 0:25 | 58 | 0:25 |
| 15 | Escoamento do pixel (SCS-CN) | 0:40 | 63 | 0:28 |
| 16 | Parêntese: CN-I e λ = 0,05 | 0:45 | 102 | 0:45 |
| 17 | Parêntese: vazão de pico local (Hao) | 0:50 | 106 | 0:47 |
| 18 | Erosão local (MUSLE no pixel) | 0:35 | 70 | 0:31 |
| 19 | Parêntese: o coeficiente c | 1:00 | 142 | 1:03 |
| 20 | Calibração e validação cruzada | 0:50 | 112 | 0:49 |
| 21 | Resultado: modelo calculado (MC) | 0:40 | 68 | 0:30 |
| 22 | O erro vem do escoamento | 0:40 | 80 | 0:35 |
| 23 | Modelo forçado ao medido (MFM) | 0:30 | 55 | 0:24 |
| 24 | Com o escoamento medido | 0:45 | 97 | 0:43 |
| 25 | Métricas | 0:25 | 40 | 0:17 |
| 27 | Áreas críticas | 0:45 | 107 | 0:47 |
| 28 | Sedimento por evento | 0:15 | 22 | 0:09 |
| 29 | Sedimento médio | 0:20 | 28 | 0:12 |
| 30 | Conclusões | 0:55 | 92 | 0:40 |
| 31 | Limitações: de onde vem o erro | 0:45 | 65 | 0:28 |
| 32 | Limitações: o que falta validar | 0:25 | 54 | 0:24 |
| 33 | Agradecimentos | 0:20 | 29 | 0:12 |
| 34 | Uso de inteligência artificial | 0:25 | 59 | 0:26 |

**Total: 2122 palavras, cerca de 15:43 de fala** (alvo somado: 18:05), de 20:00. Sobram cerca de 4:16 para pausas, troca de slide e imprevistos.

## Texto slide a slide

### Slide 1: Capa (alvo 0:20; 49 palavras)

Boa tarde a todos. Eu sou o Mateus Vivarelli e vou apresentar o meu trabalho, Espacialização da MUSLE para identificação de áreas críticas de erosão, com um estudo de caso na bacia do rio Jundiaí. Agradeço ao meu orientador, Luis Fernando Murillo-Bermúdez, e ao meu coorientador, professor André Martim.

### Slide 2: Título completo (alvo 0:25; 46 palavras)

O título do trabalho é o roteiro desta apresentação. Vou explicar cada termo, nesta ordem: primeiro a MUSLE, depois a área de estudo, a bacia do rio Jundiaí, em seguida o que significa espacializar, e por fim o objetivo, que é identificar áreas críticas de erosão.

### Slide 3: MUSLE: equação e Williams (1975) (alvo 0:30; 52 palavras)

A MUSLE, descrita por Williams em 1975, estima o sedimento produzido por um evento de chuva. Em vez da energia da chuva, ela usa a energia do escoamento, o volume e a vazão de pico. É uma equação empírica: foi ajustada a medições de campo, e não deduzida das leis da física.

### Slide 4: Q e Qp em destaque (alvo 0:20; 21 palavras)

Esta parte é a física da equação: o volume escoado e a vazão de pico, que são grandezas medidas ou calculadas.

### Slide 5: K, LS, C e P em destaque (alvo 0:35; 73 palavras)

Estes quatro fatores são índices empíricos, relativos a uma parcela padrão, sem vegetação. É como um índice de preços: não é o preço de nada, só compara com uma referência. K é a erodibilidade do solo, LS é o relevo, C é a cobertura e o manejo, que diz quanto da erosão de um solo exposto ainda ocorre, e P são as práticas conservacionistas, que na nossa bacia não existem, então vale 1.

### Slide 6: 11,8 e 0,56 em destaque (alvo 0:25; 30 palavras)

E estes dois números são constantes de Williams, sem sentido físico. Como os fatores e as constantes são empíricos, o resultado precisa ser calibrado com sedimento medido na própria bacia.

### Slide 7: Área de estudo (mapa pequeno e depois grande) (alvo 0:35; 45 palavras)

A área de estudo é a parte alta da bacia do rio Jundiaí, com cento e trinta e oito quilômetros quadrados, nos municípios de Mairiporã, Atibaia, Jarinu e Campo Limpo Paulista, onde fica a seção de medição. Deixo o mapa grande para vocês enquanto continuo.

### Slide 9: Solo e uso (alvo 0:25; 43 palavras)

O solo é dominado pelos Cambissolos, em 69% da área, e pelos Argissolos, em 18%. No uso, predominam a mata nativa, com 40%, e o campo, com 29%, e há também áreas urbanizadas, 14%, silvicultura, 13%, e um pouco de lavoura temporária, 4%.

### Slide 10: Espacialização (alvo 0:40; 96 palavras)

Sem espacialização, só temos dados hidrossedimentológicos: quanto escoa e quanto sedimento sai. Com ela, os dados têm referência espacial, e sabemos também onde. A MUSLE costuma ser aplicada à bacia ou a sub-bacias, com um fator médio; na minha iniciação científica usei valores médios. Aqui aplico pixel a pixel, em pixels de trinta metros, cerca de cento e cinquenta e quatro mil. O principal guia foi Hao e colaboradores, de 2022, que fizeram esse procedimento, inclusive com a vazão de pico por pixel, que é o maior desafio, porque não há chuva medida em cada pixel.

### Slide 11: Objetivo (alvo 0:20; 45 palavras)

O objetivo é desenvolver e aplicar a espacialização da MUSLE, em escala de evento, para identificar áreas críticas de erosão. Como o cálculo é pixel a pixel, o resultado também é um mapa, que mostra onde a erosão é produzida e onde vale priorizar intervenções.

### Slide 12: Dados e fontes (alvo 0:50; 114 palavras)

Os dados vêm do monitoramento do grupo do Luis Murillo. A chuva é de dois postos, o DBT5, fora da bacia, e o Campo Limpo Paulista. A vazão é da estação telemétrica do DAEE na saída da bacia. O sedimento vem da turbidez medida de hora em hora pela SABESP e convertida em concentração por uma curva de calibração. Os dados espaciais são o modelo de elevação do USGS, os mapas de solo e uso do Plano de Bacias e o número de curva da base da ANA. São dezessete eventos, de novembro de 2018 a fevereiro de 2020, e o gráfico mostra a carga medida em cada um. Vou acompanhar o evento onze.

### Slide 13: Evento 11 (alvo 0:25; 59 palavras)

O evento onze, de quatro a oito de julho de 2019, teve setenta e quatro milímetros de chuva, intensidade máxima de onze vírgula oito milímetros por hora, um milhão e quatrocentos e setenta e nove mil metros cúbicos de escoamento direto e mil oitocentas e vinte e duas toneladas de sedimento. É esse valor que o modelo tenta reproduzir.

### Slide 14: Chuva em cada pixel (IDW) (alvo 0:25; 58 palavras)

Primeiro, a chuva em cada pixel, interpolada pelo inverso do quadrado da distância a partir dos dois postos, que registraram sessenta e dois vírgula oito e setenta e nove milímetros. Os pixels vão de sessenta e três a setenta e nove. O pixel de exemplo, de lavoura temporária sobre Argissolo, em Atibaia, recebeu setenta e cinco vírgula quatro.

### Slide 15: Escoamento do pixel (SCS-CN) (alvo 0:40; 63 palavras)

Segundo, o escoamento do pixel pelo método do número de curva. Com a chuva do pixel e a retenção do solo, o escoamento do pixel de exemplo é treze milímetros. Somando a bacia inteira, o modelo calcula novecentos e noventa e sete mil metros cúbicos, contra um milhão e quatrocentos e setenta e nove mil medidos, cerca de dois terços do volume medido.

### Slide 16: Parêntese: CN-I e λ = 0,05 (alvo 0:45; 102 palavras)

Um parêntese sobre duas escolhas. Usei o número de curva da condição seca, o CN-I, que passa de oitenta e um para sessenta e quatro, e a razão de abstração de zero vírgula zero cinco, com a retenção convertida pela relação de Woodward, de cento e quarenta e dois para duzentos e quarenta e quatro milímetros. Essa combinação aproxima o volume total dos dezessete eventos, com viés de mais três por cento, e é apoiada por Brandão e colaboradores, em três mil quinhentas e setenta e oito bacias. A limitação é que foi escolhida olhando os mesmos eventos que uso na avaliação.

### Slide 17: Parêntese: vazão de pico local (Hao) (alvo 0:50; 106 palavras)

Terceiro, a vazão de pico local. Não existe hidrograma em cada pixel, então, seguindo Hao, o volume do pixel, onze vírgula sessenta e sete metros cúbicos, é distribuído no tempo conforme a concentração da chuva, medida pela razão entre a intensidade máxima e a lâmina do evento: zero vírgula cento e cinquenta e nove por hora. Isso dá um pico de cinco vírgula dezessete vezes dez elevado a menos quatro metros cúbicos por segundo. Atenção: essa razão é um único número por evento, então o pico local é proporcional ao escoamento. Ele não traz informação espacial nova, só dá mais peso aos eventos de chuva concentrada.

### Slide 18: Erosão local (MUSLE no pixel) (alvo 0:35; 70 palavras)

Quarto, a erosão local, que é a equação de Williams aplicada ao pixel. Com K de zero vírgula zero trezentos e cinquenta e um, para o Argissolo, LS de quatro vírgula oitocentos e sessenta e nove, C de zero vírgula duzentos e doze e P igual a um, o resultado é um vírgula cento e sessenta e sete. Esse valor é um índice relativo, e não uma massa em toneladas.

### Slide 19: Parêntese: o coeficiente c (alvo 1:00; 142 palavras)

Para chegar ao sedimento, somo esse índice nos cento e cinquenta e três mil pixels: no evento onze, quarenta mil oitocentos e oitenta e cinco. Se isso fossem toneladas, seria vinte e duas vezes a carga medida de mil oitocentas e vinte e duas. Isso acontece porque Williams ajustou a equação para bacias inteiras, com volume e pico em metros cúbicos, e aqui ela é aplicada a pixels de oitocentos e noventa e sete metros quadrados. O coeficiente c converte o índice em toneladas: zero vírgula zero trezentos e quarenta e quatro. Ele faz o papel de uma taxa de transferência de sedimentos média da bacia e também absorve a diferença de escala e parte do erro do escoamento. Atenção: c minúsculo é este coeficiente, C maiúsculo é a cobertura. No pixel de exemplo, c vezes E dá cerca de quarenta quilos.

### Slide 20: Calibração e validação cruzada (alvo 0:50; 112 palavras)

O coeficiente c é calibrado em escala logarítmica, com a média geométrica das razões entre o sedimento medido e o índice. Assim, nenhum evento grande domina: o evento quinze responderia por quase metade da variabilidade da carga em escala linear. Isso equivale a maximizar o NSE em log, a função objetivo de Hao. O modelo final usa os dezessete eventos, mas para saber se ele funciona faço a validação cruzada: tiro um evento, ajusto o c nos outros dezesseis e prevejo o evento retirado. No evento onze, o ajuste dá mil quatrocentas e seis toneladas, e a validação, mil trezentas e oitenta e três, contra mil oitocentas e vinte e duas medidas.

### Slide 21: Resultado: modelo calculado (MC) (alvo 0:40; 68 palavras)

Agora olho os dezessete eventos. O modelo calculado, que usa só a chuva, teve erro mediano de oitenta e um por cento, e só trinta e cinco por cento dos eventos ficaram dentro de um fator dois. Uma regra simples, com a carga proporcional à chuva do evento, tem a mesma informação e erra quarenta e dois por cento. O modelo foi pior em catorze dos dezessete eventos.

### Slide 22: O erro vem do escoamento (alvo 0:40; 80 palavras)

De onde vem esse erro? O SCS-CN acerta o volume total dos dezessete eventos, com três por cento de diferença, mas erra quarenta e seis por cento na mediana de cada evento: superestima as chuvas grandes e subestima as pequenas. Esse erro passa para o sedimento, ainda ampliado, porque a erosão cresce com a potência um vírgula doze do escoamento. O erro do escoamento explica noventa e um por cento do erro do sedimento. Baert e colaboradores encontraram algo parecido.

### Slide 23: Modelo forçado ao medido (MFM) (alvo 0:30; 55 palavras)

Para testar isso, criei o modelo forçado ao medido: troco só o volume do escoamento pelo medido, multiplicando todos os pixels pelo mesmo fator, que no evento onze é um vírgula quarenta e oito. O resto é igual, e o c é recalibrado. Ele não é uma previsão, serve para isolar o efeito do escoamento.

### Slide 24: Com o escoamento medido (alvo 0:45; 97 palavras)

Com o escoamento medido, o erro mediano cai de oitenta e um para vinte e um por cento, e noventa e quatro por cento dos eventos ficam dentro de um fator dois. Mas uma regra simples com o volume medido erra dezesseis por cento, e os dois não se distinguem, com p igual a zero vírgula cinquenta e dois. Então o trabalho mostra o peso do escoamento, mas não isola a contribuição da fórmula de erosão. A iniciação científica erra vinte e dois por cento, mas foi ajustada nos próprios eventos, então a comparação é só indicativa.

### Slide 25: Métricas (alvo 0:25; 40 palavras)

Todas as métricas desta comparação vêm da validação cruzada: o erro mediano, a fração de eventos em fator dois, o NSE em log e a correlação de Spearman, que diz se o modelo ordena os eventos do menor ao maior.

### Slide 27: Áreas críticas (alvo 0:45; 107 palavras)

Agora o que a espacialização acrescenta: onde a erosão é produzida. Campo, silvicultura e lavoura temporária ocupam quarenta e seis por cento da área e respondem por oitenta e três por cento da erosão. Noventa e três por cento vem dos Cambissolos, e as encostas acima de vinte por cento respondem por setenta e oito. As áreas críticas dos modelos calculado e forçado coincidem em noventa e quatro por cento, o que é esperado, pois usam o mesmo padrão espacial. O mapa é relativo, depende dos valores de K e C adotados e mostra onde a erosão é produzida, e não onde o sedimento chega ao rio.

### Slide 28: Sedimento por evento (alvo 0:15; 22 palavras)

Aqui, o sedimento em cada pixel nos dezessete eventos: as mesmas manchas se repetem, e muda a intensidade, que acompanha a chuva.

### Slide 29: Sedimento médio (alvo 0:20; 28 palavras)

E esta é a média dos dezessete eventos: as manchas mais escuras estão na porção central e oeste, em campo, silvicultura e lavoura sobre Cambissolos, em encostas íngremes.

### Slide 30: Conclusões (alvo 0:55; 92 palavras)

Em conclusão: primeiro, a conversão da chuva em escoamento é o principal limite: o modelo erra oitenta e um por cento com a chuva e vinte e um com o volume medido. Segundo, com o volume medido, a MUSLE espacializada não se distingue de uma regra simples com o volume, então não isolamos a contribuição da fórmula. Terceiro, ela chega a um erro da mesma ordem do modelo concentrado e acrescenta o mapa. E quarto, as áreas críticas estão no campo, na silvicultura e na lavoura sobre Cambissolos, nas encostas mais íngremes.

### Slide 31: Limitações: de onde vem o erro (alvo 0:45; 65 palavras)

Sobre as limitações: cerca de três quartos do erro vêm da hidrologia, e não da fórmula de erosão. Em ordem provável: a chuva de só dois postos, um fora da bacia; a delimitação manual dos eventos; a forma do SCS-CN, em que a fração que escoa não cresceu com a chuva; e a vazão de base estimada, que torna o escoamento direto medido também incerto.

### Slide 32: Limitações: o que falta validar (alvo 0:25; 54 palavras)

E o que falta validar: o mapa não tem validação espacial, porque só medimos sedimento na saída; K e C foram adotados da iniciação científica, sem recalibração; o coeficiente c é único, sem conectividade; e são só dezessete eventos. Os próximos passos são medir sedimento em sub-bacias e verificar as áreas críticas em campo.

### Slide 33: Agradecimentos (alvo 0:20; 29 palavras)

Agradeço ao Luis, pela orientação e pelos dados, ao professor André, pela coorientação, à banca, a quem me apoiou durante a graduação, e a todos que estão aqui. Obrigado.

### Slide 34: Uso de inteligência artificial (alvo 0:25; 59 palavras)

Uma última nota, sobre transparência. Usei um assistente de inteligência artificial como ferramenta: para escrever e organizar a rotina em Python, gerar figuras e tabelas, redigir e reestruturar o texto a partir das orientações do Luis e conferir referências e números. As decisões de método, a interpretação dos resultados e a revisão do texto foram minhas, com o orientador.

## Se precisar cortar (ordem)
1. Slide 25 (métricas): dizer em uma frase dentro do 24.
2. Slides 28 e 29: falar só o 29.
3. Slide 34 (IA): falar em uma frase nos agradecimentos.
4. Juntar 13 e 14.

## Pontos a conferir antes de usar
* **Slide 33 (agradecimentos):** o arquivo da nuvem cita nomes da banca, CNPq/PIBIC, "Larissa" e família. Não encontrei a origem desses nomes no repositório; confirme antes. A fala acima é genérica de propósito.
* **Slide 34 (IA):** o rascunho da nuvem diz "apoio na escrita e revisão das rotinas" e "revisão de redação"; isso subestima o que foi feito (a rotina em Python, as figuras e os rascunhos do texto foram em grande parte feitos com a IA). A fala acima descreve o que de fato ocorreu; ajuste ao que você quiser dizer e à norma da FECFAU.
* **Slide 31 e notas:** a chuva de 12 a 14 mm antes da janela do evento 11 (cerca de 16% do total) vem de uma análise da sessão em nuvem; não conferi. Verifique na série horária antes de citar. "Cerca de três quartos do erro" é uma forma simples de dizer (81% para 21%); os erros medianos não somam.
* **Slide 13 (Shepard 1968):** está nas referências do Doc, ao contrário do que eu tinha anotado (a pendência de 18/11 deve ser desconsiderada).
* **Sensibilidade do critério de calibração:** o slide de apoio 36 tem a resposta (o MC depende do critério; o MFM não).
* Números de desempenho (81%, 35%, 21%, 94%, 16%, 22%) são da validação cruzada, exceto o da IC (ajuste).
