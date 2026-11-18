# Banca simulada: professor de hidráulica, sem prática em erosão

**Persona:** professor de recursos hídricos que trabalha com hidráulica (canais, condutos, obras, saneamento). Conhece bacia, hidrograma, chuva e vazão, mas não conhece em detalhe a MUSLE, o SCS-CN, sedimentos nem validação cruzada ou NSE. Quer entender a lógica, as unidades, o motivo de cada escolha e para que o resultado serve.

**Base:** só os 36 slides e as falas do apresentador. O texto do TCC não foi lido. Os slides 2 a 8, 10 a 20 e 33 não têm fala escrita. Nesses slides, imaginei que o aluno fala só o que está escrito.

---

## 1. Perguntas prováveis (da mais provável para a menos provável)

### P1. "Se uma regra de três com a chuva acerta mais que a MUSLE, para que serve a MUSLE?"
- **Slide que motivou:** 21, 24, 26 e 30. A regra simples erra 42% e o MC erra 81%. Com o volume medido, a regra simples erra 16% e o MFM erra 21%.
- **Resposta sugerida:** "Para estimar a carga total no exutório, a MUSLE não ganhou da regra simples. Isso aparece nos slides 21 e 26, e eu não escondo. O ganho da MUSLE espacializada é o mapa. A regra simples dá só um número para a bacia inteira. A MUSLE diz em que parte da bacia a erosão é produzida (slides 27 a 30). O modelo concentrado também não dá isso. Mas o mapa é relativo e ainda não foi validado no campo (slide 32)."
- **Risco: alto.** Essa é a conclusão que mais chama atenção, e um leigo vai querer saber se o trabalho "deu certo".

### P2. "Que unidade é essa? No slide 4 o Q está em m³, mas no exemplo do slide 18 entra 13,0, que é em mm."
- **Slide que motivou:** 4, 17 e 18. No slide 17, o volume do pixel é 0,013 m × 897 m² = 11,67 m³. No slide 18, a conta usa 13,0 × 5,17·10⁻⁴ × 897, ou seja, Q em mm vezes A em m².
- **Resposta sugerida:** "Na conta do slide 18, Q·A está em mm·m², que equivale a litros. Isso é 1.000 vezes o volume em m³. Como 1.000 elevado a 0,56 é um fator constante (cerca de 48), e como o coeficiente c é calibrado depois, esse fator é absorvido por c. Por isso chamo E de índice relativo, e não de toneladas." **Atenção:** a apresentação não dá base para essa resposta. O aluno precisa conferir no texto e no código qual unidade foi usada de fato e corrigir o slide 18 ou o slide 4, para os dois ficarem iguais.
- **Risco: alto.** Um professor de hidráulica percebe esse tipo de coisa na hora, e o slide 4 mostra as unidades em destaque.

### P3. "O 11,8 tem unidade? A equação é dimensionalmente consistente?"
- **Slide que motivou:** 3 a 6. O slide diz "constantes de calibração, sem sentido físico" e "Y em t".
- **Resposta sugerida:** "Não é consistente. A MUSLE é uma equação empírica. O 11,8 e o 0,56 foram ajustados por Williams (1975) para um conjunto específico de unidades de Q, qp e K. Se outra unidade entra, o 11,8 muda. Aqui isso não altera o resultado final, porque o coeficiente c (slide 19) é recalibrado com a carga medida. O que importa é a proporção entre os pixels e entre os eventos." Falta dizer qual é a unidade de K usada.
- **Risco: alto.**

### P4. "Esse 'pico local' é vazão de pico de verdade? Cadê o tempo de concentração e o hidrograma?"
- **Slide que motivou:** 17.
- **Resposta sugerida:** "Não é um pico calculado com propagação. É a vazão média do pixel na hora de chuva mais forte. Pego o volume que escoa no pixel, multiplico pela fração da chuva que caiu naquela hora (RI/R) e divido por 3.600 s. Como RI/R é o mesmo número para todos os pixels de um evento, o pico fica proporcional a Q. Por isso ele não muda o padrão do mapa. Ele só dá mais peso aos eventos de chuva concentrada. Usei o método de Hao et al. (2022). Para um pixel de 900 m², o tempo de concentração é de minutos, então a média de 1 h subestima o pico instantâneo. Mas, de novo, c absorve esse fator."
- **Risco: alto.** O assunto é a especialidade do professor.

### P5. "Por que usou a condição seca (CN-I)? Pelo que você mostrou, choveu antes do evento."
- **Slide que motivou:** 16 (CN-I, "condição seca") e 31 (12 a 14 mm nas 9 h antes da janela do evento 11).
- **Resposta sugerida:** "A combinação de CN-I com λ = 0,05 não é uma descrição física da umidade de cada evento. É uma escolha que faz o volume total dos 17 eventos ficar próximo do medido (+3%). Com o CN-II, o modelo calcularia escoamento demais no total. O próprio slide 16 aponta a limitação: a escolha foi feita olhando os mesmos 17 eventos. E o slide 31 mostra que ela acerta o total, mas não o erro de cada evento." É preciso ter pronto quanto o escoamento total daria com o CN-II.
- **Risco: alto.** As duas informações aparecem na apresentação e parecem se contradizer.

### P6. "O que é esse λ, e de onde vêm o 0,05 e o 0,95 da fórmula?"
- **Slide que motivou:** 15 e 16.
- **Resposta sugerida:** "λ é a fração da retenção S que é perdida antes de começar o escoamento (a abstração inicial, Ia = λ·S). Na fórmula clássica, λ = 0,2. Usei λ = 0,05, que teve o melhor desempenho médio em 3.578 bacias (Brandão et al., 2025). A fórmula geral é Q = (P − λS)² / (P + (1 − λ)S). O 0,95 é 1 − 0,05. Quando o λ muda, o S também precisa ser convertido. Para isso usei a relação de Woodward et al. (2003)."
- **Risco: alto.** Nenhum slide define λ.

### P7. "Por que 40.885 dividido por 1.822 não dá o seu c?"
- **Slide que motivou:** 19. Lado a lado aparecem "40.885" (soma do índice) e "1.822 t" (carga medida), e c = 0,0344. Mas 1.822 / 40.885 = 0,0446.
- **Resposta sugerida:** "O c não é calibrado só com o evento 11. Ele é a média geométrica das razões entre carga medida e índice nos 17 eventos (slide 20). Com esse c, o evento 11 fica com 1.406 t, e não com 1.822 t."
- **Risco: médio a alto.** O slide convida a fazer essa conta.

### P8. "Esse c = 0,0344 quer dizer que só 3% do solo erodido chega ao rio?"
- **Slide que motivou:** 19 ("c faz o papel de uma taxa de transferência de sedimentos média").
- **Resposta sugerida:** "Não dá para ler o c assim. Ele junta três coisas: a fração do sedimento que chega ao exutório, a mudança de escala (a equação foi feita para bacias inteiras e aqui é aplicada a pixels) e as diferenças de unidade. Por isso ele é só um coeficiente de escala, sem sentido físico isolado."
- **Risco: médio.**

### P9. "No slide 24, 21% menos 16% dá 5 pontos. Por que a diferença é de 1,6 pontos? E o que são esses p e IC?"
- **Slide que motivou:** 24 e 26.
- **Resposta sugerida:** "Os 21% e os 16% são as medianas de cada modelo. Os 1,6 pontos são a mediana das diferenças evento a evento, que não é a mesma coisa que a diferença das medianas. O IC 95% (de −5,5 a +10,4) vem de bootstrap, que é sortear os eventos de novo muitas vezes. Como o intervalo inclui o zero e p = 0,52 (teste de Wilcoxon), não dá para dizer que um modelo é melhor que o outro com só 17 eventos."
- **Risco: médio a alto.** A conta de cabeça leva a 5, e os termos estatísticos não foram definidos.

### P10. "Qual é a diferença entre o MC e o MFM? Se o MFM usa o volume medido, não é trapaça?"
- **Slide que motivou:** 21 e 23.
- **Resposta sugerida:** "O MC (modelo calculado) só sabe a chuva. O MFM (modelo forçado ao medido) é igual ao MC, mas o volume de escoamento de cada evento é corrigido para o volume medido. Para isso, todos os pixels são multiplicados por um mesmo fator f. O MFM não serve para prever. Ele é um teste: se o erro cai de 81% para 21% quando só o volume é corrigido, então o problema estava no escoamento, e não na fórmula de erosão."
- **Risco: médio.** O próprio slide 23 deixa claro que o MFM não é previsão.

### P11. "O que é validação cruzada e por que precisa dela?"
- **Slide que motivou:** 20 e 25.
- **Resposta sugerida:** "É uma prova honesta. Tiro um evento, calibro o c com os outros 16 e prevejo o evento que tirei, como se ele fosse novo. Repito isso 17 vezes. Assim, o erro mostrado é o de previsão, e não o de ajuste. Sem isso, o modelo seria avaliado nos mesmos dados usados para calibrá-lo."
- **Risco: médio.**

### P12. "Como você mede o sedimento? Turbidez de água bruta da Sabesp? E a carga de fundo?"
- **Slide que motivou:** 12 e 32.
- **Resposta sugerida:** "A turbidez horária da água bruta foi convertida em concentração de sedimentos em suspensão (CSS) por uma curva de calibração. Depois, a concentração vezes a vazão dá a carga. A incerteza dessa curva não foi estimada (slide 32). Só medi sedimento em suspensão. A carga de fundo não entra." **Atenção:** a apresentação não diz onde fica a captação em relação ao exutório nem fala em carga de fundo. Vale ter isso pronto.
- **Risco: médio.**

### P13. "Como interpolar chuva com só dois postos, um deles fora da bacia? Por que não usou Thiessen?"
- **Slide que motivou:** 14 e 31.
- **Resposta sugerida:** "Com dois postos, qualquer método dá só um gradiente entre eles. Com o IDW (inverso do quadrado da distância), a chuva muda de forma suave de oeste para leste. Com Thiessen, a bacia seria cortada em duas metades com valores constantes. Reconheço que essa é a primeira causa de erro (slide 31). Mais postos ou radar seriam o próximo passo."
- **Risco: médio.**

### P14. "Como o escoamento direto foi 'medido'? Que filtro é esse com BFImax?"
- **Slide que motivou:** 13, 22 e 31.
- **Resposta sugerida:** "O escoamento direto é a vazão total menos a vazão de base. A vazão de base foi separada com um filtro digital, que tem um parâmetro BFImax (a fração máxima da vazão que pode ser de base), adotado como 0,70. Então o 'medido' também depende de uma escolha." **Atenção:** os slides não dão o nome do filtro.
- **Risco: médio.**

### P15. "Para que serve o mapa na prática? Um gestor faz o quê com ele?"
- **Slide que motivou:** 27, 29 e 30.
- **Resposta sugerida:** "O mapa mostra onde priorizar o controle de erosão, como práticas conservacionistas no campo, na silvicultura e na lavoura sobre Cambissolos em encostas íngremes, e onde fazer a verificação de campo. Ele não diz quanto sedimento chega a um reservatório ou a uma captação, porque não considera a conectividade (slide 32)."
- **Risco: médio.**

### P16. "Se 65% da bacia tem encosta acima de 20%, isso é critério para área crítica?"
- **Slide que motivou:** 27 e 30. As encostas acima de 20% são 65% da área e dão 78% da erosão. Os Cambissolos são 69% da área e dão 93% da erosão.
- **Resposta sugerida:** "Sozinho, não. Esses números mostram quais fatores pesam na erosão. As áreas críticas são os 5% de pixels com maior erosão média, que aparecem no mapa do slide 30. Nos slides 27 e 30, o '46% da área → 83% da erosão' se refere só aos três usos (campo, silvicultura e lavoura). Os outros critérios não entram nessa conta."
- **Risco: médio.** Do jeito que está escrito, a conclusão do slide 30 mistura critérios diferentes com um número só.

### P17. "Por que P = 1? Não existe nenhuma prática conservacionista na bacia?"
- **Slide que motivou:** 5 e 18.
- **Resposta sugerida:** "Não havia mapa de práticas, então adotei P = 1, que é o caso sem prática, o mais desfavorável. Isso pode superestimar a erosão em áreas que já têm terraço ou plantio em nível." A apresentação não dá base para essa resposta, só mostra P = 1.
- **Risco: médio a baixo.**

### P18. "Área urbana com erosão zero? E os loteamentos e as obras?"
- **Slide que motivou:** 27 e 32.
- **Resposta sugerida:** "Isso é uma hipótese do modelo. A área urbana foi tratada como impermeável e sem solo exposto. Obras e loteamentos podem ser fontes importantes de sedimento, e o modelo não as representa. Junto com o pico de CSS antes do pico de vazão (slide 35), isso indica fontes perto do canal que o modelo não vê."
- **Risco: médio a baixo.**

### P19. "Por que o evento 11 foi o exemplo? E como os 17 eventos foram escolhidos?"
- **Slide que motivou:** 12 e 13. O evento 11 é o único de julho (estação seca), segundo os títulos do slide 28.
- **Resposta sugerida:** a apresentação não dá base. É preciso preparar uma frase como "os eventos vêm do monitoramento de Murillo-Bermúdez e Martim (2022), separados manualmente, entre nov/2018 e fev/2020; o evento 11 foi usado como exemplo porque [critério]".
- **Risco: médio a baixo.**

### P20. "O que é NSE e por que calcular em log?"
- **Slide que motivou:** 20, 22 e 25. O NSE aparece no slide 20 e só é definido no slide 25.
- **Resposta sugerida:** "O NSE compara o modelo com o palpite de prever sempre a média. 1 é perfeito, 0 é igual à média e um valor negativo é pior que a média. Calculo em log para que um erro de 50% pese o mesmo num evento pequeno e num grande. Sem o log, o evento 15, que responde por quase metade da variabilidade, dominaria o resultado."
- **Risco: médio a baixo.**

### P21. "O resultado do MC depende de como você calibrou o c?"
- **Slide que motivou:** 20 (e o slide de apoio 36).
- **Resposta sugerida:** "Depende. Com os outros critérios, o erro do MC cai para 40 a 45%, perto da regra com a chuva. O MFM fica em cerca de 20% com qualquer critério. Escolhi o log para que o evento 15 não comande o ajuste." Mostrar o slide 36.
- **Risco: baixo a médio.** É mais provável vir de um especialista, mas uma pessoa curiosa pode perguntar.

### P22. "Por que a concentração chega antes da vazão? Isso afeta o modelo?"
- **Slide que motivou:** 13 (o hidrograma mostra a CSS com pico bem antes da vazão).
- **Resposta sugerida:** usar o slide 35. "É um laço horário: o sedimento disponível perto do canal sai primeiro e se esgota. O modelo trabalha com o total do evento e não representa isso. Mesmo assim, no total, o volume explica 88% da variação da carga."
- **Risco: baixo a médio.** Quem é de hidráulica e olha o hidrograma do slide 13 nota isso.

### P23. "O mapa muda se o pixel for maior ou menor?"
- **Slide que motivou:** 10 e 18 (o LS vem do MDE de 30 m).
- **Resposta sugerida:** a apresentação não dá base. Resposta geral: "o fator LS depende da resolução do MDE. Com pixels maiores, a declividade é suavizada e o LS cai. Como o c é recalibrado, a carga total se ajusta, mas a posição relativa das manchas pode mudar. Não testei isso."
- **Risco: baixo.**

### P24. "Uma vazão de 1.479 mil m³ para 74 mm de chuva em 139 km² é razoável?"
- **Slide que motivou:** 13.
- **Resposta sugerida:** "Isso dá cerca de 10,7 mm de escoamento direto, ou seja, cerca de 14% da chuva. É coerente com uma bacia com 40% de mata. O SCS-CN calculou 7,2 mm (slide 15), cerca de 67% do medido."
- **Risco: baixo.**

---

## 2. Onde essa pessoa se perderia, slide por slide

| Slide | Problema para um ouvinte de hidráulica |
|---|---|
| 1–2 | Tudo certo. O slide 2 repete o título. |
| 3–6 | Não há fala escrita. As unidades estão incompletas: K, LS, C e P não têm unidade, e o "sem sentido físico" do 11,8 abre a pergunta de consistência dimensional. "Parcela padrão" não é explicada. Não se diz que a MUSLE é **por evento**, ao contrário da USLE, que é anual. Essa é a ideia-chave para quem não é da área. |
| 7–8 | São dois slides para o mesmo mapa. A área estudada (138,8 km²) e o exutório (Campo Limpo Paulista) aparecem só na legenda, em letra pequena. Falta dizer isso em voz alta. |
| 9 | K = 0,0475 sem unidade. Os percentuais de solo e uso são muitos números ditos rápido. |
| 10 | A frase "obtenção de dados espaciais além de hidrossedimentológicos" é confusa. "Cerca de 30 × 30 m" e depois "897 m²" podem parecer números diferentes, mas 897 m² ≈ 29,95 m × 29,95 m. "Hao et al. (2022)" aparece sem dizer o que o método faz. |
| 11 | Tudo certo. |
| 12 | Siglas sem definição: DBT5, DAEE, SAISP, CSS (escrito só "concentração (CSS)"), MDE, USGS, BR_CN-2022. O gráfico usa separador americano (4,500). O gráfico de carga entra antes de se explicar como a carga é calculada. |
| 13 | O hidrograma com dois eixos é bom, mas carregado. "1.479 mil m³" é difícil de ler, e "1,48 milhão de m³" seria melhor. O pico de CSS bem antes do pico de vazão salta aos olhos e não é comentado. O evento dura cerca de 4 dias, o que também não é comentado. |
| 14 | A fórmula do IDW usa wi, di e Pk sem dizer o que são. A sigla IDW só aparece no título do gráfico. Não há fala escrita. |
| 15 | O 0,05 e o 0,95 aparecem sem λ e sem a fórmula geral. S e CN ainda não foram apresentados, e só aparecem no slide seguinte, então a ordem está invertida. O mapa de escoamento é quase todo branco. |
| 16 | CN-II, CN-I, S0,20, S0,05, λ e "Woodward": nenhum é definido. Não se diz o que é o CN nem por que usar a condição seca. O mapa mostra S acima de 1.000 mm, o que choca quem pensa em "retenção" física. A frase "viés de +3%" chega antes de se explicar o que é viés. |
| 17 | pr,k, Qk, Apix, RI e R não são definidos no slide. "Pico local" é um termo que um hidráulico vai contestar. Este é o slide mais importante para a persona e não tem fala escrita. |
| 18 | O Q entra em mm (13,0), em conflito com o "m³" do slide 4. O LS = 4,869 não é explicado. "E_unit" é uma notação nova. |
| 19 | SYn e Σk aparecem sem explicação. Mostrar 40.885 e 1.822 t lado a lado induz a dividir um pelo outro, e a conta não bate com o c. "Taxa de transferência de sedimentos" é jargão. |
| 20 | O NSE aparece antes de ser definido (só no slide 25). Os números 1.406 e 1.383 não são explicados, e é preciso dizer que um é ajuste e o outro é previsão. A régua de 1 a 17 é boa. |
| 21 | "MC" aparece no título sem ter sido apresentado antes. O gráfico de dispersão não tem rótulo no eixo x (observado), está em escala log, e a faixa cinza do fator 2 não é explicada. "Leave-one-out" está em inglês. "Wilcoxon, p = 0,02" não é explicado. O "fator 2" só é definido na fala e no slide 25. |
| 22 | O expoente Q^1,12 só é explicado na fala. "NSE ≈ 0" não é explicado. O gráfico de barras é fácil de ler. Este é um bom slide. |
| 23 | "Chuva IDW" de novo, e "Williams e c" é um rótulo enigmático. "1,48 elevado a 1,12" exige que o ouvinte se lembre do slide 22. |
| 24 | O gráfico **não mostra** a "regra com o volume medido" (16%), que é a comparação principal das caixas de baixo. "IC 95%", "pontos" e "p" não são explicados. A conta 21 − 16 = 5 não bate com 1,6. A cor laranja (concentrado) só aparece no grupo da direita. |
| 25 | As definições são boas, mas chegam **depois** de quatro slides que já usaram esses termos. A caixa de R² ("volume: 88%") cita um número que não aparece em outro lugar da sequência principal (só no slide 35, de apoio). |
| 26 | A tabela é clara. Falta destacar as duas comparações que importam, por exemplo com cor ou caixas. |
| 27 | Há números demais: seis indicadores e três observações. "r = 0,98" não diz qual correlação é. "37% / 63% em escala log" não diz como foi calculado. Os dois mapas são pequenos. |
| 28 | São 17 mapas ilegíveis na tela. A escala de cores em raiz quadrada, saturada no percentil 99,5, é explicada só em letra minúscula. Serve como imagem de "padrão que se repete", e não para ser lido. |
| 29 | Repete o mapa de cima do slide 27. |
| 30 | A conclusão 4 junta "campo, silvicultura, lavoura + Cambissolos + encostas > 20%" e atribui tudo a "46% da área, 83% da erosão", mas esse número é só dos usos. |
| 31 | BFImax não é definido. "r = −0,01" não é explicado: é a correlação entre a fração escoada e a chuva. A conta "3/4 do erro" (81 → 21) é feita de cabeça. O item 2 (chuva antes da janela) conflita com a escolha do CN-I do slide 16, e isso não é comentado. |
| 32 | "Conectividade" é jargão. O resto está claro. |
| 33 | O marcador "[e-mail de contato]" ficou no slide. Não há fala escrita além da indicação de tempo. |
| 34 | O marcador "[Opcional: confirme...]" ficou visível no slide. |
| 35 (apoio) | "Laço horário" é jargão (histerese no sentido horário). Os números 88% e 0% são bons. |
| 36 (apoio) | A fonte mostra o caminho de um script (`Scripts/_sensibilidade_...py`). A regra com a chuva aparece com 41,8% aqui e 41,9% no slide 26. |

---

## 3. Sugestões para este público, dentro de 20 minutos

**Tempo:** são 34 slides principais em 20 minutos, cerca de 35 s por slide. Dá para ganhar de 1,5 a 2 minutos assim:
- Juntar os slides 2 a 6 numa sequência rápida, porque já são animação do mesmo título, e falar no máximo 1 minuto no total.
- Cortar o slide 7 e ficar só com o 8, ou o contrário.
- Cortar o slide 29, que repete o mapa do 27, ou trocar o mapa de cima do 27 pelo mapa de áreas críticas.
- Ocultar o slide 34 ou resolvê-lo numa frase. Tirar os marcadores dos slides 33 e 34.

**Use o tempo ganho em:**

1. **Um slide "mapa do caminho" logo depois dos Objetivos (slide 11).** Ele mostraria a cadeia **chuva (IDW) → escoamento (SCS-CN) → pico local → índice de erosão (Williams) → coeficiente c → carga no exutório**, marcando o que é medido e o que é calculado. Reaproveitar o mesmo diagrama no slide 23 (MFM), destacando só a caixa que muda. Para quem é de hidráulica, essa é a forma mais rápida de entender o trabalho.

2. **Uma frase sobre unidades e o caráter relativo do índice, no slide 18 ou 19.** Por exemplo: "A equação não é dimensionalmente consistente. As unidades e a escala são absorvidas pelo c, então E é um índice relativo." E corrigir a inconsistência mm × m³ entre os slides 4, 17 e 18 (ver a pergunta P2).

3. **Definir os termos na primeira vez que aparecem:**
   - **Slide 15 ou 16:** "λ = fração de S perdida antes de escoar. Na fórmula clássica é 0,2. Usei 0,05." "CN-II = umidade normal; CN-I = solo seco." Inverter a ordem dos slides 15 e 16, para que CN e S venham antes da fórmula que os usa.
   - **Slide 17:** pôr os nomes das variáveis embaixo da fórmula (RI = maior chuva em 1 h; R = chuva do evento) e dizer: "não é um pico propagado, é a vazão média do pixel na hora mais intensa".
   - **Slide 21:** "MC = modelo calculado, que só usa a chuva" e "fator 2 = entre a metade e o dobro do medido". Rotular o eixo x do gráfico de dispersão como "carga medida (t)" e trocar "leave-one-out" por "validação cruzada".

4. **Levar o slide 25 (métricas) para antes do 21**, ou para logo depois do 20. Ou cortá-lo e definir cada métrica na primeira vez que ela aparece. Do jeito que está, o ouvinte ouve "fator 2", "NSE" e "Wilcoxon" por quatro slides antes da definição.

5. **Slide 19:** tirar o "1.822 t" do lado do "40.885", ou acrescentar "c vem dos 17 eventos (próximo slide), não só do evento 11".

6. **Slide 24:** acrescentar no gráfico a barra da "regra com o volume" (16%), que é a comparação central. Trocar "+1,6 pontos (IC 95%: −5,5 a +10,4; p = 0,52)" por "a diferença evento a evento é pequena e pode ser zero". Os números ficam para a resposta oral.

7. **Slide 27:** ficar com dois números grandes ("46% da área → 83% da erosão" e "94% das áreas críticas coincidem no MC e no MFM") e mandar o resto para a fala ou para um slide de apoio. No slide 30, separar "usos: 46% → 83%" das outras características.

8. **Frases de transição que faltam:**
   - Do slide 9 para o 10: "Para ter o mapa, a bacia foi dividida em cerca de 154 mil quadradinhos de 30 m, e a equação foi aplicada em cada um."
   - Do slide 13 para o 14: "Agora vou seguir um pixel do evento 11 por todas as etapas."
   - Do slide 20 para o 21: "Até aqui foi o método com um evento. Agora vem a pergunta: o modelo acerta os 17?"
   - Do slide 22 para o 23: "Se o problema é o escoamento, e se eu der ao modelo o escoamento certo?"
   - Do slide 26 para o 27: "Para a carga total, a MUSLE não ganha da regra simples. O que ela traz de novo é o mapa."

9. **Antecipar a pergunta P1 na conclusão (slide 30):** dizer de forma clara que o valor do trabalho está no mapa e no diagnóstico de onde vem o erro, e não em prever melhor a carga total.

10. **Ter pronto um slide de apoio de "unidades e conversões"** (K em t·h/(MJ·mm), Q em mm ou m³, pr em m³/s, como c absorve a escala) e uma frase sobre a escolha do evento 11 e dos 17 eventos. Essas são as perguntas em que a apresentação não dá base.

11. **Detalhes:** usar vírgula decimal e ponto de milhar nos gráficos do Excel (slides 12 e 22), tirar o caminho do script do slide 36 e deixar 41,8% e 41,9% iguais nos slides 26 e 36.
