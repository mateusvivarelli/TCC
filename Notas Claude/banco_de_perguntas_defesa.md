# Banco de perguntas para a defesa (19/11, 15h)

Feito a partir de 6 leituras simuladas: 3 de especialistas em hidrologia e sedimentos (como o orientador ou um avaliador da área) e 3 de um professor de hidráulica que não conhece a MUSLE. Em cada grupo, um leu só o TCC, outro só a apresentação e o terceiro os dois. Os relatórios completos estão em `Notas Claude/banca_18-11/`.
Os números marcados com (*) não estão no TCC: foram calculados dos dados e conferidos.

---

## 0. As 12 que mais vão cair (decore estas)

**1. "Se uma regra de três com a chuva acerta mais que o seu modelo, para que serve a MUSLE espacializada?"** (todos os 6 levantaram)
> "Para prever a carga total no exutório, nesta bacia e com estes dados, a regra simples é melhor; eu não escondo isso. O ganho da espacialização não está no número da carga, está no mapa: onde a erosão acontece, o que nem a regra simples nem o modelo concentrado dizem. E a comparação serviu para localizar o problema: o que estraga o modelo calculado é a conversão da chuva em escoamento, não a fórmula de erosão."

**2. "Com o escoamento medido, a MUSLE empata com carga = c × volume. Então ela não acrescenta nada?"**
> "No exutório, não. K, LS e C são os mesmos em todos os eventos; a única coisa que muda entre eventos é o escoamento. Então nenhum teste no exutório consegue avaliar a fórmula e os fatores — o próprio trabalho conclui isso. O que a espacialização acrescenta é a distribuição dentro da bacia."

**3. "Como você sabe que as áreas críticas estão no lugar certo?"**
> "Não sei: o mapa não foi validado no espaço, porque só há medição no exutório. Ele é relativo, depende dos K e C adotados, e mostra onde a erosão é produzida, não onde o sedimento chega ao rio. Os 94% de coincidência entre MC e MFM não são validação, porque os dois usam o mesmo padrão. Ele serve para indicar onde verificar primeiro. Para validar: medir sedimento em sub-bacias e conferir as manchas em campo ou em imagens."

**4. "Condição seca (CN-I) em eventos de verão? O 16 começa 13 horas depois de um evento de 139 mm."**
> "Não tem sentido físico de umidade, e o TCC diz isso (3.4.1.3): foi uma condição única, escolhida porque, com λ = 0,05 e a conversão de Woodward, o volume total dos 17 eventos ficou a +3% do medido. Na prática é um CN efetivo da bacia. É coerente com o escoamento direto baixo desta bacia — cerca de 10% da chuva no conjunto (*) —, mas foi escolhido olhando os mesmos eventos, e acerta o total, não cada evento (46% de erro)."
Não tente defender que o solo estava seco.

**5. "Quais são as unidades? Williams usa volume em m³; você usa Q em mm vezes área em m²."**
> "Segui a forma de Hao et al. (2022). Q em mm vezes m² dá litros, 1.000 vezes o volume em m³. Como o expoente é fixo, isso vira uma constante (1.000^0,56, cerca de 48) que vai para dentro do c. Não muda nenhuma previsão nem o mapa relativo. Por isso o E é um índice, não toneladas."
Se insistirem que isso tira o sentido físico do c: "Sim. Com o volume em m³, o c ficaria perto de 1,6 no MC — maior que 1, sem sentido como taxa de transferência. Por isso o TCC diz que o c não deve ser lido como taxa física (3.4.4): ele junta a entrega de sedimento, a mudança de escala, as unidades e parte do erro do escoamento."

**6. "Pico local de um pixel de 30 m sem tempo de concentração nem propagação? Isso não é vazão de pico."** (o professor de hidráulica vai fazer)
> "Concordo, não é um pico hidráulico. Não há hidrograma no pixel; segui Hao et al. (2022): o volume do pixel vezes o índice de concentração da chuva (RI/R), dividido por 3.600. Como RI/R é um número por evento, o pico é proporcional ao escoamento: não traz informação espacial e só dá mais peso aos eventos de chuva concentrada. Por isso a erosão cresce com Q^1,12."
Se perguntarem se testou sem o pico ou com o pico medido: "Não testei."

**7. "Vazão de base com BFImax = 0,70? Eckhardt sugere 0,25 para rocha cristalina."**
> "A série veio com os dados e eu reproduzi com o filtro de Eckhardt; quem a reproduz é 0,70. O TCC reconhece que é bem maior que o sugerido e que parte do que foi para a base pode ser escoamento direto (4.6). Não fiz sensibilidade. Isso pesa em cadeia: muda o escoamento direto 'medido', o MFM, a regra com o volume e até a escolha do CN-I, que foi feita para bater esse volume. A conclusão de que o escoamento é o gargalo deve se manter, mas os números mudariam."

**8. "O MFM usa o volume medido no mesmo rio em que se mede o sedimento. Não é óbvio que acerta?"**
> "É, e eu digo que não é previsão. A carga é o volume vezes a concentração, e entre os eventos o volume varia muito mais (variância do log 0,66 contra 0,08 da concentração). Por isso quem recebe o volume medido acerta a ordem de grandeza. O MFM serve só para isolar o efeito do escoamento: trocando só o volume, o erro cai de 81% para 21%."
Evite dizer "por construção": diga "em grande parte por causa do volume".

**9. "Você escolheu CN-I e λ olhando os 17 eventos; a validação cruzada só refaz o c. O que ela valida?"**
> "Ela tira o viés do ajuste do c, e só. As escolhas do SCS-CN foram feitas antes, com os mesmos eventos, então as métricas tendem a ser otimistas, em grau que não estimei; a validação aninhada não foi feita (3.4.6). Mas o MC vai mal mesmo com esse viés a favor dele, então a conclusão sobre o escoamento fica de pé."
Tenha pronta a lista de configurações testadas (CN-II com λ 0,20, CN-II com 0,05, CN-I com 0,20, CN-I com 0,05 e Woodward) e o critério (viés de volume).

**10. "O resultado 'MC pior que a regra com a chuva' depende do critério de calibração?"**
> "Depende. Com o critério em log, o do TCC, o MC erra 81% contra 42%. Em escala linear, 45% contra 39%. O log foi escolhido porque o evento 15 responde por 48,7% da variabilidade da carga e dominaria um ajuste linear, e porque equivale a maximizar o NSE em log, a função objetivo de Hao et al. O que não muda: o MC erra de 40 a 80%, e com o escoamento medido o MFM fica em cerca de 20% em qualquer critério." (slide de apoio)

**11. "O padrão do mapa não é só o gradiente da chuva de dois postos?"**
> "Em parte, sim: em log, 63% da variação espacial vem do termo de escoamento (chuva e CN), e eu digo que é a parte menos confiável. Mas: em escala linear, K·LS·C sozinho explica 58%; a ordem das classes de uso, solo e declive vem dos fatores fixos; e o termo de escoamento também carrega o CN, que depende do uso e do solo. As classes críticas são mais robustas que a posição exata das manchas. O teste seria refazer o mapa com chuva uniforme."

**12. "Por que não usou conectividade (índice de Borselli), como Hao et al.?"**
> "Com um único ponto de medição e 17 eventos, eu não teria como calibrar nem testar um índice por pixel; ele mudaria o mapa sem dado para conferir. Por isso usei um c único e trato o mapa como erosão produzida, relativa. É o terceiro dos próximos passos."
Não diga que o índice "não mudaria nada".

---

## 1. Banca especialista: outras perguntas, por tema

### Hidrologia e dados de entrada
- **"Woodward em cima do CN-I: a retenção média ficou em 490 mm, CN equivalente de 34 (*). Plausível?"** — "Como propriedade física do solo, não. Como CN efetivo, é coerente com o escoamento direto de cerca de 10% da chuva (*). O TCC reconhece que a conversão é extrapolada em 8,4% dos pixels e nos eventos 1 e 12, e que Baert et al. (2026) tiveram NSE de −0,87 com Woodward."
- **"Woodward converte o quê?"** — "Só o λ (de 0,20 para 0,05). O CN-I vem da fórmula de Chow, Maidment e Mays (1988). Combinar as duas foi escolha minha."
- **"Brandão et al. (2025) não associam clima úmido e pastagem a λ mais alto?"** — "Sim, e o TCC cita isso (4.6): o alto Jundiaí tem clima úmido e 29% de campo. O 0,05 não é consenso; foi escolhido pelo volume."
- **"O coeficiente de escoamento não cresceu com a chuva (r = −0,01). O que isso diz sobre como o escoamento é gerado?"** — "Sugere que boa parte do escoamento rápido não é por excesso de infiltração nas encostas, e sim de áreas saturadas perto dos canais e fluxo subsuperficial raso, comum em clima úmido com solo profundo. Por isso o SCS-CN não acompanha. Com a ressalva de que o coeficiente medido depende da separação da base e da chuva de dois postos." (boa pergunta para mostrar que entende o processo)
- **"De onde vêm os pesos 0,307 e 0,693 da chuva média?"** — O TCC não diz. **Confirmar com o Luis** (provavelmente Thiessen ou fração de área). Se não souber: "vieram da planilha de eventos do grupo; não recalculei".
- **"RI/R maior que 1 nos eventos 1 e 12?"** — "Não é físico: RI vem do posto mais intenso e R é a média dos dois. A chuva forte pegou praticamente um posto só (no 12, o DBT5 marcou 0). Num mesmo posto, daria 0,72 e 0,96. Por isso é tratado como índice." (slide de apoio)
- **"Como os 17 eventos foram escolhidos e delimitados? O 15 e o 16 estão colados."** — "São eventos do monitoramento do grupo, com pico acima de 10 m³/s (Murillo-Bermúdez e Martim, 2022), delimitados à mão sobre o hidrograma. É uma limitação: no evento 11, 12 a 14 mm caíram nas 9 h antes da janela. No 15 e 16, parte da recessão do 15 pode estar no 16." **Confirmar com o Luis** se são os mesmos 17 eventos do artigo de 2022.
- **"Dois postos, um fora da bacia. Não havia outros?"** — "Eram os dois com registro horário no período. É a primeira causa de erro que aponto. Os postos ficam a cerca de 29 km um do outro (*)."
- **"Na seção 3.1 você diz que a cabeceira é mais chuvosa, mas o mapa de chuva mostra o contrário."** — "O mapa vem só de dois postos; a cabeceira é comandada pelo DBT5, que registrou menos na maioria dos eventos. É mais um sinal de que o padrão leste–oeste da chuva não é confiável."

### Modelo e calibração
- **"O que é o c? Por que muda de 0,0344 para 0,0222?"** — "Um coeficiente de escala calibrado. Ocupa o lugar da taxa de transferência, mas absorve também a escala, as unidades e parte do erro do escoamento — por isso muda quando só o escoamento muda. Não deve ser lido como taxa física."
- **"40.885 dividido por 1.822 não dá o seu c."** — "O c não vem só do evento 11: é a média geométrica das razões medido/índice dos 17 eventos. Com ele, o evento 11 dá 1.406 t, não 1.822 t."
- **"Somar a fórmula em 150 mil pixels não dá o mesmo que aplicá-la na bacia."** — "Certo: para pixels iguais, a razão é n^0,12. O c absorve essa diferença, como em Hao et al. Por isso o mapa é relativo."
- **"Por que não calibrou o expoente 0,56?"** — "Para ter um só parâmetro com 17 eventos. Calibrar o expoente aproximaria o MFM da regra com o volume, mas continuaria sem testar K, LS e C. O TCC mostra que o expoente efetivo (1,12) é maior que a relação observada entre carga e volume (0,94), o que amplia um pouco o erro do escoamento."
- **"Os 91% (erro do escoamento explica o erro do sedimento) não são quase automáticos?"** — "São esperados pela estrutura: K, LS e C são fixos, então só o escoamento muda entre eventos. A evidência independente é o MFM: trocando só o volume, o erro cai de 81% para 21%."
- **"Por que mediana e fator 2, e não o NSE linear?"** — "O evento 15 responde por 48,7% da soma dos quadrados e dominaria o NSE linear. Com 17 eventos, métricas relativas são mais estáveis."
- **"p = 0,52 quer dizer que são iguais?"** — "Não: quer dizer que não há evidência de diferença com 17 eventos. O intervalo vai de −5,5 a +10,4 pontos."
- **"Somando os 17 eventos, o MC acerta o total?"** — Não está no TCC. "No ajuste, o MC soma cerca de 37.300 t contra 23.846 t medidas, +56% (*), porque superestima os eventos grandes (o 15: 10.361 t contra 3.829 t). O MFM soma 22.964 t, −4% (*)."

### Dados de sedimento
- **"Como a turbidez virou concentração? Quantas amostras, qual faixa, qual R²? O pico de 2.700 mg/L está dentro da curva?"** — "A curva é de Murillo-Bermúdez et al. (2023), por partes com quebra em 250 NTU; a incerteza é maior nos picos, e eu não a estimei." **Antes da defesa: reler o artigo de 2023 para ter número de amostras, faixa e R², ou dizer que usou a série de CSS pronta.**
- **"A captação da SABESP fica no mesmo ponto da estação do DAEE?"** — O TCC não diz. **Confirmar com o Luis.**
- **"E a carga de fundo?"** — "Não foi medida; o alvo é a carga em suspensão, e o c absorve a diferença."
- **"Você calibra com a carga total, que inclui sedimento do canal e o período de vazão de base."** — "É uma hipótese assumida no TCC (3.4.4). No evento 11, cerca de 72% da carga está na parcela do escoamento direto, supondo a mesma concentração na base. O c absorve o resto; muda o valor do c, não o padrão do mapa."
- **"Histerese: o pico de CSS vem antes da vazão. E o modelo?"** — "O pico de concentração chega cerca de 25 h antes no evento 11, o que costuma indicar sedimento disponível perto do canal que se esgota. O modelo trabalha com o total do evento e não representa isso. A histerese entra no trabalho para justificar somar vazão × CSS hora a hora, em vez de usar uma curva-chave instantânea."
  **Cuidado:** o TCC (2.5) cita Murillo-Bermúdez e Martim (2022): laços em forma de oito em 13 eventos e horários em 4. Não diga "13 de 17 eventos com laço horário" (o slide de apoio foi corrigido para "pico de CSS antes do pico de vazão em 13 de 17 eventos", que é uma conta direta dos dados). O Luis é o autor do artigo.
- **"Evento 17?"** — "3.806 mg/L de carga por m³ de escoamento direto, contra 1.085 a 2.088 nos outros. Pode ser obra, deslizamento ou a curva de turbidez nas concentrações altas. Mantive porque não há base para excluir; sem ele, o MFM vai a 15,3% e nada muda." (Atenção: 3.806 mg/L é carga dividida pelo escoamento direto, não uma concentração medida.)
- **"Os erros do MFM mudam ao longo da série."** — "Os primeiros eventos são superestimados e os últimos, subestimados. Não identifiquei a causa: pode ser o sensor, a curva, a disponibilidade de sedimento ou obras. Um c único não representa isso."

### Mapa
- **"K e C de outras regiões; silvicultura com C = 0,121, mais que o campo."** — "Adotados de Vivarelli et al. (2025), sem recalibração; não dá para calibrá-los no exutório. A ordem entre lavoura, silvicultura e campo depende diretamente desses valores. O 0,121 vale para plantio com manejo variável; talhão formado teria C menor."
- **"Área urbana com erosão zero?"** — "Hipótese do modelo (C = 0, K = 0). Obras e loteamentos podem ser fontes importantes, e a área urbana fica perto do exutório; isso pode jogar para a área rural parte do sedimento."
- **"Por que limitar a área de contribuição do LS a 200 m?"** — "Sem limite, ela chega a milhões de m² nos pixels de canal, onde a USLE, que é de encosta, não vale. O 200 é uma escolha; não testei outros. Afeta a intensidade do mapa, não as métricas no exutório."
- **"Por que 5% para área crítica?"** — "É um corte para destacar as manchas principais; não testei outros limiares."
- **"Os 78% da erosão nas encostas acima de 20% não são automáticos pelo LS?"** — "São esperados pela formulação; descrevem o modelo, não confirmam o campo."
- **"Escalas diferentes: pixel de 30 m e solos em 1:250.000."** — "As manchas devem ser lidas como regiões, não como pixels."
- **"Onde, concretamente, agir?"** — "Nos pixels críticos, a combinação mais comum é lavoura temporária sobre Cambissolo com declive de 20 a 45% (26,7%), depois silvicultura na mesma situação (19,2%) e lavoura com 8 a 20% (13,8%), na porção central e oeste, entre 3 e 12 km do exutório."

### Escopo e texto
- **"Na introdução você diz que o modelo pode prever cenários futuros."** — "Em valor absoluto, ainda não, com estes dados. Em termos relativos (trocar o C de uma classe), o mapa indicaria a tendência, sem validação. A frase é uma possibilidade futura."
- **"O objetivo era validar o modelo distribuído."** — "A validação foi feita no exutório, para a soma da bacia; o mapa não pôde ser validado no espaço."
- **"A comparação com o seu trabalho anterior é justa?"** — "Não totalmente, por isso a chamo de indicativa: o concentrado foi ajustado nos próprios eventos, sem validação cruzada, e usa o volume total e o pico medidos. Dá para dizer que, com o volume medido, a espacialização chega a um erro da mesma ordem e acrescenta o mapa."
- **"Qual é a área da bacia?"** — "137,8 km² pela acumulação de fluxo; a área de cálculo tem 138,1 km² e a literatura cita 139,3 km²." (O mapa grande dos slides 7 e 8 mostra 138,8 km² na legenda: é engano do mapa.)

---

## 2. Professor de hidráulica (não conhece a MUSLE)

- **"O que é MUSLE, em uma frase?"** — "Uma equação empírica que estima o sedimento de uma chuva a partir do volume escoado e da vazão de pico, multiplicados por fatores de solo (K), relevo (LS), cobertura (C) e práticas (P). Diferente da USLE, que é média anual, ela é por evento."
- **"O 11,8 tem unidade? A equação é dimensionalmente consistente?"** — "Não é consistente: é empírica, ajustada por Williams para um conjunto de unidades. Aqui não importa para o resultado, porque o c é calibrado com a carga medida."
- **"O que é o número de curva e o λ?"** — "O CN, de 0 a 100, diz quanto o terreno deixa escoar (mata e solo profundo baixo, asfalto perto de 100). λ é a fração da retenção perdida antes de começar a escoar; o clássico é 0,20, usei 0,05. O 0,95 da fórmula é 1 − 0,05."
- **"O que é fator 2? Errar o dobro é aceitável? Em hidráulica é muito."** — "Fator 2 é o simulado entre a metade e o dobro do medido, ou seja, a ordem de grandeza certa. Em sedimentos a própria medição tem incerteza grande (a carga vem da turbidez). Não digo que errar o dobro está bom; uso para comparar modelos entre si."
- **"O que é validação cruzada?"** — "Tiro um evento, calibro o c com os outros 16 e prevejo o que tirei, como se fosse novo. Repito 17 vezes. Assim o erro mostrado é de previsão, não de ajuste."
- **"O que é NSE?"** — "Compara o modelo com o palpite de prever sempre a média: 1 é perfeito, 0 é igual à média, negativo é pior. Em log, um erro de 50% pesa igual num evento pequeno e num grande."
- **"No slide, 21% menos 16% dá 5. Por que a diferença é 1,6?"** — "Os 21% e 16% são as medianas de cada modelo; os 1,6 pontos são a mediana das diferenças evento a evento, que é outra conta."
- **"Por que IDW e não Thiessen?"** — "Com dois postos, qualquer método dá um gradiente; Thiessen cortaria a bacia em duas metades constantes. Usei IDW de potência 2, padrão do QGIS."
- **"1,48 milhão de m³ para 74 mm em 138 km² é razoável?"** — "Dá cerca de 10,7 mm de escoamento direto, uns 14% da chuva (*). Na bacia, o escoamento direto medido vai de cerca de 3% a 22% da chuva, 10% no conjunto (*). O SCS-CN calculou 7,2 mm."
- **"Quanto é isso por hectare?"** — Não está no TCC. "Somando os 17 eventos, cerca de 1,7 t/ha; em média, 0,1 t/ha por evento (*). O pixel de exemplo, 40,1 kg em 897 m², equivale a uns 0,45 t/ha só no evento 11 (*). Mas o mapa é relativo."
- **"Para que serve isso na prática? Quem usaria?"** — "Para priorizar onde fazer conservação do solo: práticas conservacionistas, recompor cobertura no campo, controlar solo exposto. Isso reduz o sedimento que assoreia reservatórios e chega à captação — a turbidez usada no trabalho é justamente a da água bruta da SABESP. O mapa ordena onde agir; não dimensiona toneladas nem obras."
- **"Por que P = 1?"** — "Não havia mapa de práticas conservacionistas; P = 1 é o caso sem prática, o mais desfavorável."
- **"Por que o evento 11 como exemplo?"** — Prepare uma frase. Sugestão: "é o mesmo do Apêndice A: um evento médio e longo (74 mm em 91 h), com chuva nos dois postos, em que dá para seguir todas as etapas."
- **"O mapa muda se o pixel for maior?"** — "O LS depende da resolução; com pixels maiores a declividade é suavizada. A carga total se ajusta pelo c, mas a posição das manchas pode mudar. Não testei."

---

## 3. Plateia (família, amigos)

- **"O que você fez, em uma frase?"** — "Fiz um mapa de onde a terra é mais levada pela chuva numa bacia que abastece a região de Jundiaí e testei o quanto esse tipo de modelo consegue prever o sedimento que chega ao rio."
- **"Deu certo?"** — "Em parte. O mapa saiu e mostra onde a erosão se concentra. Para prever a quantidade de sedimento a partir da chuva, o modelo errou bastante, e descobri por quê: a parte que transforma chuva em água escorrendo é a que mais erra. Saber onde está o erro também é um resultado."
- **"Por que isso importa?"** — "A terra que a chuva arrasta vai para o rio: suja a água que a SABESP trata e enche os reservatórios. Saber de onde ela vem ajuda a decidir onde proteger o solo."
- **"O que é um pixel aqui?"** — "Um quadradinho de 30 por 30 metros. Dividi a bacia em uns 154 mil quadradinhos e fiz a conta em cada um."
- **"Onde estão as áreas mais críticas?"** — "Na parte do meio e do oeste da bacia, em pasto, eucalipto e lavoura em morros mais inclinados. A parte de mata, a leste, quase não erode."
- **"Por que a parte da mata erode menos?"** — "As folhas e as raízes seguram o solo e a chuva infiltra mais."
- **"Por que o Jundiaí?"** — "O grupo do meu orientador monitora o rio lá desde 2018, com medição de chuva, vazão e turbidez. Sem esses dados não daria para testar o modelo."
- **"Quanto tempo levou?"** — Sua resposta (iniciação científica + TCC).
- **"Usou inteligência artificial?"** — Sua resposta, alinhada com o slide de IA.
- **"E agora, o que vem depois?"** — "Medir sedimento em rios menores dentro da bacia para conferir o mapa, ter mais pluviômetros ou radar, e incluir quanto da terra realmente chega ao rio."

---

## 4. Pontos fortes (para usar nas respostas)
1. **Honestidade:** o trabalho diz claramente o que funcionou e o que não funcionou; as limitações estão escritas.
2. **Comparação com modelos simples:** poucos trabalhos com MUSLE fazem isso. É ela que mostra onde está o erro.
3. **MC contra MFM:** separa o erro do escoamento do erro da fórmula — o diagnóstico é o resultado mais sólido.
4. **Validação cruzada e métricas robustas** (mediana, fator 2, NSE em log), com testes pareados.
5. **Exemplo numérico completo** (Apêndice A, evento 11): dá para seguir a conta pixel a pixel.
6. **Mapa com leitura por classe** (uso, solo e declive), útil para priorizar conservação.

## 5. Pontos fracos (assuma, com a frase pronta)
| Ponto fraco | Frase |
|---|---|
| Mapa sem validação espacial | "É relativo e não validado; serve para indicar onde verificar primeiro." |
| MUSLE não testável no exutório | "K, LS e C não mudam entre eventos, então o exutório não consegue testá-los." |
| Hidrologia escolhida com os mesmos dados | "CN-I e λ são um ajuste de volume, não umidade real; a validação aninhada não foi feita." |
| Vazão de base com BFImax 0,70 | "Não testei a sensibilidade; o escoamento direto 'medido' depende dela." |
| Chuva de 2 postos | "É a principal fonte de erro, e o padrão leste–oeste do mapa é a parte menos confiável." |
| c único, sem conectividade | "O mapa mostra onde a erosão é produzida, não onde chega ao rio." |
| Unidades na fórmula | "Segui Hao et al.; a constante de unidade vai para o c, por isso E é índice." |
| Turbidez e curva sem incerteza | "A incerteza é maior nos picos e não foi estimada." |
| 17 eventos | "As conclusões são qualitativas." |
| Resultado do MC depende do critério | "Em log, 81%; em outros critérios, 40 a 45%. Em todos, erro alto; o MFM fica em ~20% sempre." |

## 6. Armadilhas de números (para não ser pego)
- **c ≠ 1.822 / 40.885** (0,0446): o c vem dos 17 eventos (média geométrica).
- **21% − 16% ≠ 1,6**: 1,6 é a mediana das diferenças evento a evento.
- **"3/4 do erro"**: não use. Diga "a maior parte do erro vem da hidrologia" e cite os 91%.
- **Histerese**: TCC = 13 em oito e 4 horários (artigo de 2022). Não diga "13 laços horários".
- **46% → 83%** vale só para as três classes de uso (campo, silvicultura, lavoura). Cambissolos (69% → 93%) e declive > 20% (65% → 78%) são outras contas.
- **"Com o volume medido"**: quem chega a 21%, perto do concentrado (22%), é o MFM, não o MC.
- **Volume**: "regra com o volume" usa o escoamento direto; os "88% explicados pelo volume" usam o volume total.
- **41,8% × 41,9%**: use 41,9% (Tabela 13).
- **Área**: 137,8 km² (o mapa grande diz 138,8).
- **Evento 16, Tabela 2**: R = 97,7 mm, mas 0,307 × 63,6 + 0,693 × 113,6 = 98,2 mm (*). Diferença pequena; se perguntarem, "vou conferir a planilha".
- **f do evento 10**: o texto diz 9,75; pela Tabela 11 arredondada, 552/57 = 9,68. É arredondamento.

## 7. Confirmar com o Luis antes da defesa
1. De onde vêm os pesos 0,307 e 0,693 da chuva média (Thiessen?).
2. Se os 17 eventos são os mesmos do artigo de 2022 e qual foi o critério de seleção.
3. Onde fica a captação da SABESP (turbidez) em relação à estação do DAEE.
4. Número de amostras, faixa e R² da curva turbidez × CSS (artigo de 2023).
5. Quem gerou a série de vazão de base e por que BFImax = 0,70.
6. A chuva antes da janela do evento 11 (12 a 14 mm, das 3h às 11h de 04/07): foi intencional começar a janela na subida do hidrograma?

## 8. Ajustes nos slides
**Já feitos no meu exemplo** (`Apresentacao/slideTCC_18-11_sugestoes.pptx`): slide de apoio da histerese sem "laço horário"; conclusão das áreas críticas separando uso de solo e declive; conclusão do concentrado com "com o volume medido"; "3/4" trocado por "a maior parte"; rótulo do c no slide do MFM; métricas antes dos resultados; marcadores "[e-mail]" e "[Opcional]" removidos; caminho do script removido do slide de apoio; 41,9%; nota de unidade no slide da MUSLE; c "calibrado nos 17 eventos" no slide do coeficiente.

**Nos seus slides (pontuais, se quiser):**
1. **Mapa grande (slides 7 e 8):** a legenda diz 138,8 km²; o TCC diz 137,8. Se não der para refazer, não leia o número em voz alta.
2. **Slide do evento 11:** "1.479 mil m³" pode virar "1,48 milhão de m³".
3. **Gráfico de barras do slide 11:** separador de milhar em inglês (4,500) aparece na renderização; no PowerPoint em português deve sair 4.500 — confira.
