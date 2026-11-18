# Perguntas prováveis da banca: professor de hidráulica (não especialista em erosão nem em estatística)

Persona: professor de engenharia civil, recursos hídricos, do lado da hidráulica (canais, condutos, obras hidráulicas, saneamento). Conhece bacia, hidrograma, chuva e vazão. Não conhece MUSLE, SCS-CN em detalhe, sedimentos, validação cruzada nem NSE. Quer entender a lógica, as unidades, o motivo de cada escolha e para que o resultado serve.

Base: texto final do TCC (`TCC_texto_final.md`) e apresentação (`texto_e_falas.md` + slides 1 a 36; 35 e 36 são de apoio).

---

## 1. Perguntas prováveis (da mais provável para a menos provável)

### P1. "As unidades da fórmula no pixel não fecham. Williams usa volume em m³ e pico em m³/s. No seu slide aparece Q em mm vezes pico vezes área. Qual é a unidade do E_unit? E a do c?"
- **Motivação:** slide 4 diz "Q: volume escoado (m³)"; slide 18 usa "11,8 (Q · pr · Apix)^0,56" com Q = 13,0 (em mm). Quem é de hidráulica confere unidade antes de tudo.
- **Resposta sugerida:** "Q em mm vezes a área em m² dá litros (1 mm sobre 1 m² é 1 litro). Então o termo entre parênteses é o volume do pixel em litros vezes o pico em m³/s. Isso só muda a escala por uma constante (1000^0,56). Por isso eu não trato o E_unit como toneladas: é um índice relativo, e toda a constante de escala e de unidade fica no coeficiente c, que é calibrado com a carga medida. O c tem unidade de t por unidade de índice. Há um segundo motivo: Williams ajustou 11,8 e 0,56 para bacias inteiras; somar a fórmula em 150 mil pixels não dá o mesmo que aplicá-la na bacia (para n pixels iguais, a razão é n^0,12)." Base: seção 3.4.3 (parágrafo "E_unit,k é um índice relativo...") e 3.4.4; Tabela 7.
- **Risco: alto.** O slide 4 diz "m³" e o slide 18 usa mm sem comentar. A explicação dos "litros" não está no texto; é bom tê-la pronta.

### P2. "Se o modelo calculado erra mais do que uma regra de três com a chuva, qual é a vantagem de fazer tudo isso?"
- **Motivação:** slides 21 e 26 (MC 81% contra 42% da regra simples; pior em 14 de 17 eventos).
- **Resposta sugerida:** "Para prever a carga total do evento, nesta bacia e com estes dados, a regra simples é melhor. O ganho da espacialização não está no número da carga, está no mapa: ela diz onde a erosão acontece, o que nenhuma regra simples e nem o modelo concentrado dizem. E a comparação serviu para localizar o problema: o que estraga o MC é a conversão da chuva em escoamento pelo SCS-CN, não a fórmula de erosão." Base: seções 4.2, 4.3 e 5 (quarto parágrafo das conclusões).
- **Risco: alto.** É a pergunta mais natural de quem quer saber "para que serve".

### P3. "No modelo forçado ao medido você usa o volume medido no mesmo rio onde mede o sedimento. Não é óbvio que vai acertar? Isso não é circular?"
- **Motivação:** slides 23 e 24 (MFM 21%).
- **Resposta sugerida:** "É, e eu digo isso no slide: o MFM não é uma previsão. A carga é a vazão vezes a concentração, e entre os eventos o volume varia muito mais que a concentração; só o volume explica 88% da variação da carga (em log). Por isso qualquer modelo que recebe o volume medido acerta a ordem de grandeza. O MFM serve só para isolar o efeito do escoamento: muda só o volume e o erro cai de 81% para 21%. E, com o volume medido, a MUSLE não se distingue de uma regra simples com o volume (16%), então eu não digo que isso valida a fórmula de erosão." Base: seção 3.4.4 (último parágrafo), seção 4.3 (parágrafo "Esse resultado precisa, porém, ser lido com uma ressalva...") e Figura 11.
- **Risco: alto.**

### P4. "Por que condição seca (CN-I) em todos os eventos, se eles são do verão chuvoso? No evento 11 você mesmo diz que choveu de 12 a 14 mm nas 9 horas antes."
- **Motivação:** slide 16 (CN-I) e slide 31, item 2 (chuva antes da janela).
- **Resposta sugerida:** "A condição seca não foi escolhida como medida de umidade de cada evento. Ela é uma condição única, escolhida porque, com ela, λ = 0,05 e a conversão de Woodward, o volume total dos 17 eventos ficou próximo do medido (+3%). É um ajuste de volume, e eu reconheço que foi feito olhando os mesmos eventos. Ela acerta o total, mas não o evento a evento (46% de erro mediano)." Base: seção 3.4.1.3 (parágrafo "A combinação de CN-I..."), seção 3.4.6 e 4.6 (terceira fonte).
- **Risco: alto.** Para o hidráulico, "seco" no verão parece contraditório. O dado de 12 a 14 mm na véspera do evento 11 só aparece no slide 31; o texto (seção 4.6) diz que a delimitação dos eventos é tratada "sem estimativa quantitativa". Se perguntarem de onde vem o número, é preciso saber explicar.

### P5. "Esse mapa de áreas críticas é confiável? Como você sabe que a erosão está mesmo ali?"
- **Motivação:** slides 27, 29 e 30.
- **Resposta sugerida:** "Não foi validado no espaço: só existe medição de sedimento no exutório. O mapa é relativo, depende dos K e C adotados por classe, considera a área urbana sem erosão e mostra onde a erosão é produzida, não onde o sedimento chega ao rio. Os 94% de coincidência entre MC e MFM não validam nada, porque os dois usam o mesmo padrão espacial. Para validar seria preciso medir sedimento em sub-bacias ou conferir as manchas em campo ou em imagens." Base: seções 4.5 e 4.6 (sétima fonte) e conclusões (último parágrafo).
- **Risco: alto.**

### P6. "Você diz que 63% do padrão do mapa vem do escoamento, isto é, da chuva de dois postos e do CN. Então o mapa é mais um mapa de chuva interpolada do que de erosão?"
- **Motivação:** slide 27 ("37% dos fatores K, LS e C e 63% do escoamento") e fala do slide 27 ("a parte menos confiável do mapa").
- **Resposta sugerida:** "Em escala log, sim, mais da metade da variação vem do termo de escoamento. Em escala linear, o produto K·LS·C sozinho explica 58%, então a conclusão depende da escala. As manchas fortes ficam onde se juntam uso com C alto, Cambissolo e encosta íngreme, e o escoamento puxa a intensidade para oeste, onde chove mais e o CN é maior. Por isso eu digo que essa parte do padrão é a menos confiável." Base: seção 4.5 (parágrafo "Para medir quanto do padrão espacial...") e 3.4.9.
- **Risco: alto.** Ele mesmo chamou essa parte do mapa de "menos confiável" na fala; a banca vai explorar.

### P7. "Esse pico local no pixel: em hidráulica o pico depende de tempo de concentração, de roteamento. Como um pixel de 30 m tem pico? E por que não usou o pico medido no hidrograma?"
- **Motivação:** slide 17.
- **Resposta sugerida:** "Não há hidrograma no pixel nem roteamento. Segui Hao et al. (2022): o volume do pixel é distribuído no tempo pela concentração da chuva do evento, RI/R (intensidade máxima sobre a lâmina total). Como RI/R é um só número por evento, o pico local é proporcional ao escoamento do pixel; ele não acrescenta informação espacial e só dá mais peso a eventos de chuva concentrada. O pico medido no exutório não foi usado porque a ideia do MC é prever só com a chuva; no MFM forcei só o volume." Base: seção 3.4.3 e 2.6.
- **Risco: alto.** É a parte mais "anti-hidráulica" do método. O texto não discute se seria melhor usar o pico medido no MFM: não há resposta direta para isso.

### P8. "O que é esse coeficiente c? Ele tem significado físico ou é um botão de ajuste?"
- **Motivação:** slide 19 e Tabela 9 (c do MC = 0,0344, do MFM = 0,0222).
- **Resposta sugerida:** "Em princípio ele faz o papel de uma taxa de transferência de sedimento média da bacia: quanto do que erode chega ao exutório. Mas, como é calibrado, ele também absorve a diferença de escala da fórmula e parte do erro do escoamento; é por isso que o valor muda entre o MC e o MFM. Então não deve ser lido como uma taxa física. Hao et al. usam uma conectividade por pixel; eu usei um único c." Base: seção 3.4.4 (segundo parágrafo).
- **Risco: médio.**

### P9. "Por que calibrar em logaritmo? E o que é essa 'validação cruzada'? Com um parâmetro só, precisa?"
- **Motivação:** slide 20.
- **Resposta sugerida:** "Em log, o ajuste olha o erro relativo; em escala linear, o evento 15 (o maior) responde por quase metade da variabilidade e mandaria no ajuste. Com um parâmetro só, o ajuste em log tem solução direta: a média geométrica das razões medido/índice. A validação cruzada é tirar um evento, ajustar c nos outros 16, prever o que ficou de fora e repetir 17 vezes. Com um parâmetro, o ganho é pequeno (ajuste e validação dão quase o mesmo: 1.406 t e 1.383 t no evento 11), mas é o jeito honesto de medir o erro em um evento que o modelo não viu. Ressalva: a escolha de CN-I e λ foi feita antes, olhando todos os eventos, e não foi refeita em cada rodada." Base: seções 3.4.5, 3.4.6 e 2.8; seção 4.2 (primeiro parágrafo).
- **Risco: médio.**

### P10. "E se calibrar de outro jeito, o resultado muda? O MC continua pior que a regra simples?"
- **Motivação:** slide de apoio 36 (se for mostrado) ou pergunta natural depois do slide 20.
- **Resposta sugerida:** "Muda para o MC: em linear ou com erro relativo, ele cai para 40 a 45%, perto da regra com a chuva (39 a 52%). O que não muda: o MC tem erro alto em qualquer critério, e com o volume medido o MFM fica em cerca de 20% em qualquer critério." Base: só o slide 36. **O texto não traz essa análise de sensibilidade**; ela cita um script de 18/11.
- **Risco: médio.** A frase "o MC foi pior que a regra simples (p = 0,02)" vale para o critério em log; com outros critérios a diferença quase some. Melhor dizer isso antes de ser perguntado.

### P11. "Como separou a vazão de base? Esse escoamento direto 'medido' é medido mesmo?"
- **Motivação:** slide 13 (linha tracejada "vazão de base"), slide 22 (rodapé) e slide 31, item 4.
- **Resposta sugerida:** "Não é medido diretamente. A série de vazão de base veio com os dados e eu reproduzi com o filtro de Eckhardt (a = 0,995, BFImax = 0,70). O BFImax é escolhido, não medido, e 0,70 é bem maior que o valor que Eckhardt sugere para rio perene em rocha cristalina (0,25), que é o caso da bacia. Então parte do que foi para a base pode ser escoamento direto. A base é 34% a 55% do volume de cada evento." Base: seções 2.4, 3.2 (Tabela 3) e 4.6 (quarta fonte).
- **Risco: médio.** Na apresentação a vazão de base só aparece como linha no gráfico e como limitação; não é explicada no método.

### P12. "A carga medida inclui o que passa durante a vazão de base, mas o modelo só usa o escoamento direto. Não está comparando coisas diferentes?"
- **Motivação:** slide 13 (área azul = escoamento direto; carga total de 1.822 t).
- **Resposta sugerida:** "A carga medida é a total do evento. O modelo admite que o sedimento do evento foi mobilizado pelo escoamento superficial, e o c absorve a diferença. No evento 11, supondo a mesma concentração na base, cerca de 72% da carga estaria na parcela do escoamento direto." Base: seção 3.4.4 (terceiro parágrafo) e 3.2. O número de 72% está só no slide de apoio 35, não no texto.
- **Risco: médio.**

### P13. "Para que serve isso na prática? Quem usaria esse mapa? A ETA da SABESP, o comitê de bacia?"
- **Motivação:** slides 27 e 30; objetivo do slide 11. A apresentação não fala da motivação prática.
- **Resposta sugerida:** "Para priorizar onde fazer conservação do solo: práticas conservacionistas, recompor cobertura no campo, controlar solo exposto e mineração. Isso reduz sedimento que assoreia reservatórios e chega à captação. O mapa é relativo e serve para ordenar onde agir, não para dimensionar quantas toneladas." Base: seção 1.1 (reservatórios, qualidade da água) e 4.5 (parágrafo "O mapa serve, assim..."). O texto não fala de uso pela ETA ou de dimensionamento de obra hidráulica (desarenador, volume morto de reservatório): para isso não há resposta.
- **Risco: médio.**

### P14. "Por que a área urbana tem erosão zero? Obra, loteamento, rua de terra produzem muito sedimento, e ela fica perto do exutório."
- **Motivação:** slides 27 e 32 ("área urbana sem erosão").
- **Resposta sugerida:** "É uma hipótese do modelo: o mapa de uso classifica toda a mancha urbana como superfície impermeável (C = 0), e o mapa de solos não tem classe nela (K = 0). Sei que isso subestima a contribuição urbana e pode jogar para as áreas rurais parte do sedimento que o c atribui. Com um mapa de uso mais detalhado daria para separar obras, solo exposto urbano e áreas verdes." Base: seção 4.5 (último parágrafo).
- **Risco: médio.**

### P15. "Por que dois postos, um fora da bacia? E por que IDW? Com dois postos não daria na mesma usar Thiessen?"
- **Motivação:** slide 14 e slide 31, item 1.
- **Resposta sugerida:** "Eram os postos com registro horário disponíveis. Com dois postos, qualquer interpolação vira um gradiente suave e não mostra núcleo de chuva entre eles; é a primeira limitação que listo. Usei IDW de potência 2 por ser o padrão do QGIS e estar entre as melhores no teste de Moeletsi et al.; outras potências não foram testadas." Base: seções 2.7 e 3.4.1.4.
- **Risco: médio.** Ponto fraco ligado: a lâmina R usada no pico local vem da planilha, com pesos fixos 0,307/0,693 (74,0 mm no evento 11), e não da média do IDW (73,5 mm). O texto não diz de onde vêm esses pesos (seção 3.4.1.4). Se perguntarem "por que duas chuvas médias diferentes?", não há resposta no texto.

### P16. "O SCS-CN supõe que, quanto maior a chuva, maior a fração que escoa. Você diz que aqui isso não aconteceu. Isso não é o mais interessante do trabalho?"
- **Motivação:** slide 22 e slide 31, item 3 (r = −0,01).
- **Resposta sugerida:** "É um dos resultados centrais. Nos eventos medidos, o coeficiente de escoamento não cresceu com a chuva. Por isso o SCS-CN subestima as chuvas pequenas e superestima as grandes, e os erros se cancelam no total. Mas o coeficiente medido depende da separação da base e da chuva de dois postos, então é uma leitura com ressalva." Base: seção 4.1 (parágrafo "No método SCS-CN, a fração...").
- **Risco: baixo** (é uma pergunta favorável, desde que ele cite a ressalva).

### P17. "O que é esse expoente 1,12? De onde saiu?"
- **Motivação:** slide 22 ("A erosão cresce com Q^1,12"); a explicação está só nas notas.
- **Resposta sugerida:** "Williams eleva (volume vezes pico) a 0,56. Como o pico local é proporcional ao escoamento, fica (Q vezes Q)^0,56, ou Q^1,12. Por isso um erro no escoamento chega ao sedimento um pouco ampliado: metade do escoamento dá cerca de 46% do sedimento." Base: seção 3.4.3 e 4.2 (parágrafo "Esse resultado tem uma explicação direta...").
- **Risco: baixo**, se ele disser a frase que está nas notas.

### P18. "O que é NSE, fator 2, Spearman? Por que tantas métricas, e por que mediana?"
- **Motivação:** slides 21 a 26. O slide 25, das métricas, vem **depois** dos slides que já usam "fator 2" e "erro mediano".
- **Resposta sugerida:** "Erro mediano: quanto o modelo erra num evento típico; a mediana evita que dois ou três eventos muito errados dominem. Fator 2: em quantos eventos o simulado fica entre a metade e o dobro do medido, ou seja, acerta a ordem de grandeza. NSE: compara o modelo com 'chutar sempre a média'; 1 é perfeito, 0 é igual à média, negativo é pior. Spearman: se o modelo coloca os eventos na ordem certa do menor para o maior." Base: seções 2.8 e 3.4.7.
- **Risco: baixo** (é simples de responder), mas a ordem dos slides pode gerar a pergunta.

### P19. "O que é esse p = 0,02, Wilcoxon, intervalo de 95%? Com 17 eventos dá para concluir alguma coisa?"
- **Motivação:** slides 21 e 24.
- **Resposta sugerida:** "Comparei os dois modelos evento a evento, pela diferença dos erros. O bootstrap sorteia os eventos com reposição 4.000 vezes para ver quanto essa diferença poderia variar; se o intervalo inclui zero, os modelos não se distinguem. Com 17 eventos, os valores de p são só indícios e as conclusões são qualitativas." Base: seção 3.4.7 (último parágrafo) e 4.6 (último parágrafo).
- **Risco: baixo a médio.**

### P20. "E o evento 17? Por que ele fica fora em todos os modelos com volume medido?"
- **Motivação:** Tabela 12 / slide 24 (o MFM tem 94%, não 100%).
- **Resposta sugerida:** "A carga por m³ de escoamento direto dele foi 3.806 mg/L, contra 1.085 a 2.088 mg/L nos outros 16. Pode ser uma fonte que o modelo não representa (obra, deslizamento) ou a incerteza da curva de turbidez nas concentrações altas. Mantive o evento porque não há base para excluí-lo; sem ele as conclusões não mudam." Base: seção 4.3 (parágrafo do modelo concentrado).
- **Risco: baixo.**

### P21. "A carga é estimada pela turbidez da água bruta da ETA. Qual é o erro dessa medição? A turbidez não depende do tipo de partícula?"
- **Motivação:** slide 12 ("convertida em concentração (CSS) por curva de calibração") e slide 32.
- **Resposta sugerida:** "A curva turbidez–CSS foi ajustada por Murillo-Bermúdez et al. (2023), linear por partes com quebra em 250 NTU. A incerteza é maior justamente nos picos, onde está a maior carga, e eu não a estimei. É uma limitação." Base: seções 2.5 e 4.6 (quinta fonte).
- **Risco: baixo a médio.**

### P22. "Por que o erro do MFM vai de superestimar nos primeiros eventos a subestimar nos últimos?"
- **Motivação:** Tabela 12 (eventos 1 a 6 positivos, 14 a 17 negativos). Não está na apresentação; só quem leu o texto pergunta.
- **Resposta sugerida:** "Não identifiquei a causa. Pode ser uma mudança na bacia ou na medição (curva de turbidez) ao longo da série. Um c único para todos os eventos não representa essa variação." Base: seção 4.3 (penúltimo parágrafo) e 4.6 (quinta fonte).
- **Risco: baixo.**

### P23. "O concentrado do seu trabalho anterior acerta 100% em fator 2. Por que ele é 'só indicativo'?"
- **Motivação:** slides 24 e 26.
- **Resposta sugerida:** "Os valores dele foram ajustados nos próprios 17 eventos, com dois parâmetros (coeficiente e expoente) e sem validação cruzada, então o erro está otimista. Além disso, ele usa o volume total e o pico medidos, não só o escoamento direto. Dá para dizer que é da mesma ordem, não que é melhor ou pior." Base: seção 3.4.8 (terceiro modelo) e 4.3.
- **Risco: baixo.**

### P24. "Por que 5% para definir área crítica? E por que limitar a área de contribuição do LS em 200 m?"
- **Motivação:** slide 27 (rodapé) e Tabela 4 / seção 3.4.1.2.
- **Resposta sugerida:** "Sobre o LS: sem limite, a área de contribuição chega a milhões de metros nos pixels de canal, onde a USLE, que é de encosta, não faz sentido físico. Sobre os 5%: é um corte para destacar as manchas principais." Base: seção 3.4.1.2 (LS). **O texto não justifica os 5%** (seção 3.4.9 só define): não há resposta escrita.
- **Risco: baixo.**

---

## 2. Onde a apresentação e o texto diferem

### A apresentação explica pior que o texto
- **Por que estudar erosão.** Os slides 2 a 10 montam o título e a fórmula, mas não dizem por que o sedimento importa (assoreamento de reservatório, qualidade da água para a captação). O texto faz isso na seção 1.1. Para um público de hidráulica e saneamento, essa é a ponte mais fácil.
- **Objetivos.** O slide 11 mostra só o objetivo geral (mapa). Os objetivos específicos que organizam os resultados (comparar com modelos simples e medir quanto o escoamento limita o resultado; seção 1.3.2) não aparecem. Por isso os slides 21 a 26 parecem uma mudança de assunto.
- **SCS-CN.** Os slides 15 e 16 mostram a fórmula e quatro números (CN-II, CN-I, S0,20, S0,05) sem dizer em uma frase o que é CN, S e λ. A seção 2.3 do texto explica melhor.
- **Vazão de base.** Aparece como linha tracejada no slide 13, como rodapé no 22 e como limitação no 31, mas nunca é explicada no método. O texto tem a seção 2.4 e a Tabela 3.
- **Ordem das métricas.** "Fator 2", "erro mediano" e "Wilcoxon" já aparecem nos slides 21 a 24, mas só são definidos no slide 25. No texto, as métricas (3.4.7) vêm antes dos resultados.
- **Unidades.** O slide 4 define Q em m³, e o slide 18 usa Q em mm sem comentar. O texto (3.4.3) explica por que o E_unit é um índice.

### A apresentação explica melhor que o texto
- O MFM, com o fluxograma do slide 23 e o aviso "não é previsão".
- A motivação da calibração em log (slide 20) e o exemplo numérico do evento 11 contado passo a passo (slides 13 a 19). No texto, ele fica no Apêndice A.
- O resumo das causas de erro em ordem de importância (slide 31).

### Onde os dois não batem (corrigir ou saber explicar)
1. **Histerese.** O slide 35 diz "13 de 17 eventos com laço horário". O texto (seção 2.5) diz que Murillo-Bermúdez e Martim (2022) acharam "laços em forma de oito em 13 e laços no sentido horário em 4". **É uma contradição direta.** O slide cita "planilha de eventos"; se a fonte for outra, ela tem que ser explicada.
2. **Conclusão das áreas críticas.** O slide 30 diz "campo, silvicultura e lavoura temporária sobre Cambissolos, em encostas acima de 20% (46% da área, 83% da erosão)". No texto, 46% → 83% vale **só para as três classes de uso**; Cambissolos (93%) e declividade acima de 20% (65% → 78%) são recortes separados. Do jeito que está, o slide junta três números diferentes.
3. **Área da bacia.** O mapa dos slides 7 e 8 mostra "138,8 km²"; o texto usa 137,8 km² (área de contribuição) e 138,1 km² (área de cálculo).
4. **Porcentagens de solo e uso.** Na legenda do slide 9 aparecem Cambissolos 68,5%, Argissolos 17,7% e silvicultura 12,6%. O texto (Tabelas 5 e 6) traz 68,6%, 17,6% e 12,7%. A diferença é pequena, mas é visível.
5. **Conteúdo que só existe nos slides.** Estes pontos não estão no texto: a chuva de 12 a 14 mm nas 9 h antes do evento 11 (slide 31; o texto diz que a delimitação ficou "sem estimativa quantitativa"); o "cerca de 3/4 do erro vem da hidrologia" (slide 31); o pico de CSS 25 h antes do pico de vazão, os 68% e 72% da carga, os "0%" explicados pela intensidade e o Spearman de 0,49 (slide 35); e a sensibilidade ao critério de calibração (slide 36). Se a banca pedir no texto, não vai encontrar.
6. **Sensibilidade ao critério de calibração (slide 36).** Ela enfraquece uma frase do texto e do slide 21: "MC pior que a regra simples (p = 0,02)" só vale firme no critério em log. Com os outros critérios, o MC (40 a 45%) fica perto da regra com a chuva. Além disso, a regra com a chuva aparece com 41,8% no slide 36 e com 41,9% na Tabela 13 e no slide 26.
7. **Gráfico do slide 24.** A comparação central do slide (MFM × regra com o volume, 21% × 16%) não está no gráfico. O gráfico mostra o modelo concentrado no grupo "escoamento direto forçado ao medido", mas o concentrado usa o volume **total** (com vazão de base) e o pico medidos, não o escoamento direto.
8. **Slide 16, "CN-II tabelado (uso × solo)".** O CN não foi tabelado pelo autor: veio pronto do raster BR_CN-2022 da ANA (seção 3.3). O slide também cita Brandão et al. (2025) só a favor de λ = 0,05. O texto (seção 4.6) lembra que os mesmos autores associam clima úmido e pastagem a λ mais alto, que é o caso da bacia.
9. **Slide 21.** O eixo horizontal (carga medida) dos gráficos de dispersão aparece sem rótulo e sem números legíveis.

---

## 3. Contribuição e fragilidade, na visão dessa pessoa

**Qual é a contribuição.** Na leitura de um professor de hidráulica, o trabalho dá duas coisas:
1. **Um diagnóstico.** Usando a MUSLE para estimar o sedimento de um evento a partir da chuva, o gargalo é a hidrologia (chuva de dois postos + SCS-CN), não a fórmula de erosão. Trocando só o volume pelo medido, o erro cai de 81% para 21%. É um resultado "negativo" bem feito e honesto.
2. **Um mapa relativo de onde a erosão se concentra:** campo, silvicultura e lavoura temporária sobre Cambissolos, em encostas íngremes, na porção central e oeste. Ele serve para priorizar conservação.

**A contribuição fica clara?** Fica clara no texto (resumo e conclusões). Na apresentação, só aparece no fim. O título e o objetivo prometem "identificar áreas críticas", mas metade dos resultados trata de "o modelo não prevê bem a carga". Sem uma frase no começo dizendo que o trabalho tem duas perguntas (onde erode e quanto o escoamento limita a previsão), o ouvinte pode sair achando que "o modelo não funcionou". Também falta dizer cedo por que isso importa para quem cuida de reservatório e captação.

**O que ele acharia mais frágil:**
- **O mapa, que é o produto principal, não foi validado,** e 63% do padrão (em log) vem justamente da parte em que o próprio autor menos confia: chuva de dois postos e CN de base nacional. A coincidência de 94% entre MC e MFM não conta como validação.
- **As unidades e o significado físico.** A fórmula de Williams é aplicada fora da escala em que foi ajustada, com mm × m² × m³/s, e tudo é empurrado para um c calibrado que muda de 0,0344 para 0,0222 conforme o escoamento. Para um hidráulico, isso parece "ajuste de caixa-preta".
- **O pico local sem roteamento,** proporcional ao volume, que não traz informação nova.
- **As escolhas hidrológicas (CN-I no verão, λ, BFImax = 0,70) feitas olhando os mesmos 17 eventos,** e um "escoamento direto medido" que depende de um filtro com parâmetro escolhido.
- **Só 17 eventos;** a conclusão "MC pior que a regra simples" depende do critério de calibração (slide 36).

---

## 4. Frases de transição e explicações curtas para um público não especialista

1. **Antes do slide 3 (por que o assunto importa):** "Todo sedimento que sai das encostas acaba no rio: suja a água que a SABESP capta aqui no exutório e assoreia os reservatórios. Medir isso é caro, então a pergunta é: dá para estimar quanto sai em cada chuva e de onde sai?"
2. **No slide 11 (as duas perguntas do trabalho):** "O trabalho responde duas perguntas: primeiro, onde, dentro da bacia, a erosão se concentra; segundo, quanto a estimativa da chuva que vira escoamento limita a previsão do sedimento. Os primeiros resultados respondem a segunda, e os mapas no final respondem a primeira."
3. **No slide 15 (SCS-CN em uma frase):** "O SCS-CN é uma conta simples: parte da chuva fica no solo e o resto escoa. O número de curva, de 0 a 100, diz o quanto o terreno deixa escoar: mata e solo arenoso têm CN baixo, asfalto tem CN perto de 100."
4. **No slide 18 ou 19 (o que é o índice e o c):** "O número que sai da fórmula em cada pixel não é tonelada: é um índice para comparar pixels entre si. Para virar tonelada, multiplico a soma de todos os pixels por um único fator, ajustado com o que foi medido no rio."
5. **Na passagem do slide 20 para o 21 (antes dos resultados):** "Para julgar o modelo, vou usar uma pergunta simples: em quantos eventos ele acerta entre a metade e o dobro do que foi medido? E vou compará-lo com uma regra de três que qualquer um faria só com a chuva. Se o modelo complicado não ganha da regra de três, quero entender por quê."

Também ajudaria levar a definição de métricas (slide 25) para antes do slide 21 e, no slide 30, separar o 46% → 83% (uso) do 93% (Cambissolos) e do 65% → 78% (declividade).
