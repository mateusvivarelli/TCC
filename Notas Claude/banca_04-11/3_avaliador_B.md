# Avaliador B: arguição do TCC (versão de 04/11/2026)

**ESTADO: VERSÃO PARCIAL, gravada às pressas porque o notebook pode ser desligado.** As perguntas abaixo já valem, mas a parte estatística ainda não foi recalculada. Ver a seção "Falta fazer" no fim.

Papel: pesquisador de modelagem ambiental, geoprocessamento e estatística aplicada, cético quanto a modelos calibrados com poucos dados e atento à utilidade para a gestão da bacia.

## (a) O que foi lido

**Lido por inteiro:** o texto do TCC, páginas 1 a 68, em `Notas Claude/doc_texto_pdf_paginas_04-11.txt`. A primeira leitura foi feita só com o TCC.

**Figuras vistas no PDF até agora:** Figura 1 (p. 22), Figura 3 (p. 26), Figura 8 (p. 46), Figura 9 (p. 48) e Figura 11 (p. 52). Vi em resolução baixa, de 95 dpi.

**Figuras ainda não vistas:** Figura 2 (p. 25), Figura 4 (p. 28), Figura 5 (p. 42), Figuras 6 e 7 (p. 44 e 45), Figura 10 (p. 51), Figuras A1 e A2 (p. 67).

**Conferido depois da leitura, no repositório:**
- `resultados_analise_mapa_pc_02-11.md`
- `perguntas_para_o_luis_30-10.md`
- `relatorio_checagens_base_alvo_woodward_27-10.md` (até a seção c2)
- `resumo_modelo_completo.md` (trechos)
- `teste_cn_calibrado.md` (início)
- `leitura_referencias/`, lotes A, B, C e D (trechos)
- `README.md` (início)
- busca por caminhos fixos e por "bootstrap/wilcoxon" em `Scripts/*.py`

**Não li**, como pedido: `1_revisao_texto.md`, `2_avaliador_A.md`, `revisao_processo_29-10.md`, `revisao_independente_03-11.md`.

**Origem dos números:** cada número vem do TCC, de uma nota do repositório ou de conta manual minha sobre as tabelas do TCC, e isso está indicado. Nada que dependa dos rasters foi recalculado. A literatura citada vem das notas de leitura do repositório, salvo onde digo "de memória, não conferido".

## (b) Impressão geral (parecer curto)

O trabalho é honesto e isso é o seu maior mérito: mostra que o modelo calculado perde para uma regra proporcional à chuva e que o MFM não valida a fórmula nem o mapa. Poucos TCCs escrevem isso.

A fragilidade está no que sobra depois dessa honestidade. O título promete "identificação de áreas críticas", mas o único teste disponível, no exutório, não enxerga o padrão espacial. O mapa é, em boa parte, o produto de tabelas de K e C com fonte não confirmada, de um gradiente de chuva entre dois postos e de um mapa de CN com solos em 1:250.000. O texto reconhece isso, mas não mede a sensibilidade do mapa a nenhuma dessas entradas.

Há também três pontos em que a conclusão vai além do que foi demonstrado:
- "não se mostrou pior" em relação à IC;
- "não se explica pelo acaso";
- "o limite está na conversão da chuva em escoamento".

Eu aprovaria com exigência de ajustes nesses pontos.

## (c) Perguntas de banca

### B1. Teste que não enxerga o mapa
**Pergunta:** "Se eu embaralhar os valores de K, LS e C entre os pixels da bacia e rodar tudo de novo, o que acontece com o seu erro mediano e com o fator 2? Se quase nada mudar, o que a sua validação diz sobre o mapa?"
**Local:** seção 4.2, p. 47: "Os fatores K, C e LS são os mesmos em todos os eventos e não mudam de um evento para outro"; seção 4.3, p. 49.
**Por que importa:** esses fatores não variam entre eventos, então só entram na escala, que o c absorve (salvo a interação com o padrão de Q). O teste no exutório quase não tem poder sobre eles. O texto diz que não é validação, mas não demonstra isso com um teste de placebo.
**Boa resposta:** admitir que a validação é só temporal, explicar por que o c absorve os fatores, propor ou apresentar o teste de placebo e separar "acerto no exutório" de "acerto no espaço". Não recalculado (depende dos rasters).
**Gravidade:** pode comprometer.

### B2. Para que serve espacializar
**Pergunta:** "Seu modelo espacial não supera uma regra de uma linha, proporcional ao volume, e a chuva sozinha supera o seu modelo calculado. O mapa não tem validação. Então, para que espacializar? O que eu perderia se fizesse só o cruzamento de uso e declividade?"
**Local:** seção 4.3, p. 49 ("não melhora a estimativa do sedimento total"); Conclusões, p. 60; seção 4.5, p. 55.
**Por que importa:** é o argumento central do trabalho. A única justificativa restante é "acrescenta o mapa", e o texto não compara esse mapa com nenhuma alternativa barata, como K * LS * C sozinho, RUSLE ou cruzamento de uso e declividade.
**Boa resposta:** dizer que a espacialização não serve para prever a carga e sim para formular hipóteses de localização, informar a sobreposição entre os críticos e o top 5% de K * LS * C e encarar o dilema: se a sobreposição for alta, o evento acrescenta pouco; se for baixa, a diferença vem da parte menos confiável (chuva e CN).
**Gravidade:** pode comprometer.

### B3. O argumento atenuante que o próprio texto derruba
**Pergunta:** "Na seção 3.4.6 você diz que o viés de seleção é reduzido porque as escolhas seguiram o volume, e não a carga. Na 4.3 você diz que o volume explica 88% da variância da carga. Como as duas frases convivem?"
**Local:** seção 3.4.6, p. 36 ("as escolhas seguiram o volume de escoamento, e não a carga de sedimentos que é avaliada"); seção 4.3, p. 49.
**Por que importa:** se carga e volume são quase a mesma informação, escolher pelo volume é em boa parte escolher pela carga. Além disso, `resumo_modelo_completo.md` (seção 3) mostra as duas configurações comparadas também no sedimento: MC 97,9% contra 81,1% e MFM 38,7% contra 20,6%. Com a mesma lista de eventos, a segunda atenuante do texto também não reduz esse viés.
**Boa resposta:** retirar ou reformular a atenuante, declarar quantas configurações foram examinadas e o que se viu antes de decidir, e fazer a validação aninhada ao menos para λ e AMC, mesmo com 16 eventos.
**Gravidade:** pode comprometer.

### B4. Quantas configurações foram testadas
**Pergunta:** "Quantas combinações de CN, λ e conversão foram testadas antes desta? Por que nenhuma aparece no texto? Se eu trocasse λ = 0,05 por 0,20, o que aconteceria com o MFM, que recebe o mesmo volume medido?"
**Local:** seção 3.4.1.3, p. 31; seção 3.4.6, p. 36. O repositório tem dezenas de scripts de teste em `Scripts/` (por exemplo, `_teste_amc_por_evento.py`, `_teste_cn2_lambda005_convertido.py`).
**Por que importa:** segundo `resumo_modelo_completo.md`, o MFM com λ = 0,20 dá 38,7% e o com λ = 0,05 dá 20,6%, com o mesmo volume medido. São 18 pontos, enquanto o texto diz que 2 a 5 pontos não são interpretáveis. Logo, o resultado do MFM não vem só do volume: depende também de como o padrão espacial concentra o escoamento.
**Boa resposta:** mostrar uma tabela de sensibilidade com as configurações testadas, explicar a diferença de 18 pontos pela não linearidade de Q^1,12 e usar a favor o que está nas notas e não no texto: áreas críticas coincidem em 95% (MC) e 91% (MFM) entre as duas configurações.
**Gravidade:** importante.

### B5. "O limite está na conversão da chuva em escoamento"
**Pergunta:** "Você substitui a saída de um modelo pelo volume medido no mesmo hidrograma em que a carga é medida, e o acerto sobe. Isso é um diagnóstico ou uma consequência aritmética? Conclui-se mesmo que, corrigindo o SCS-CN, o modelo passaria a prever?"
**Local:** Resumo, p. 7 ("O limite está, portanto, na conversão da chuva em escoamento"); seção 3.4.8, p. 38 ("isola o efeito"); seção 4.3, p. 49; Conclusões, p. 59 e 60.
**Por que importa:** o texto faz a ressalva da carga como volume vezes concentração, mas o Resumo mantém o "portanto" sem ressalva. Forçar o volume medido melhora qualquer modelo. Além disso, MC e MFM não diferem só no volume: o c muda de 0,0344 para 0,0222.
**Boa resposta:** distinguir "o volume é necessário" de "o volume é suficiente", reconhecer que o ganho é em parte por construção, dizer que o MFM é teto e não previsão, e citar que uma calibração melhor do volume não melhorou o sedimento nas notas (`teste_cn_calibrado.md`, feito em versão anterior do modelo).
**Gravidade:** pode comprometer.

### B6. O erro de 91% é explicação ou identidade?
**Pergunta:** "Você diz que o erro do escoamento explica 91% do erro do sedimento. Os dois erros usam o mesmo volume calculado e cargas que são quase volume medido. Que parte desse 91% é física e que parte é conta?"
**Local:** seção 4.2, p. 47; Conclusões, p. 59.
**Por que importa:** é correlação entre grandezas que têm termos em comum. Como E_unit é proporcional a Q^1,12 e a carga medida é volume vezes concentração, um valor alto é esperado por construção.
**Boa resposta:** reconhecer o termo comum, mostrar a dedução e tratar o 91% como consistência, não como descoberta.
**Gravidade:** importante.

### B7. Viés de 56% que não aparece
**Pergunta:** "Você destaca o viés de +3% no volume. Qual é o viés do MC na carga total dos 17 eventos? E o NSE linear dele? Por que a Tabela 13 só traz a escala log?"
**Local:** Tabela 12, p. 46; Tabela 13, p. 48; seção 3.4.5, p. 35; p. 50 (NSE linear só para a IC).
**Por que importa:** pela soma da Tabela 12 (conta manual), o MC no ajuste dá 37.294 t contra 23.846 t medidas, ou +56%; o MFM dá 22.964 t, ou -3,7%. `resumo_modelo_completo.md` registra NSE linear de -5,43 para o MC, número ausente do texto, enquanto o da IC (0,83) é citado. Para quem cuida de reservatório ou de captação, a massa total é o que importa, e a calibração em log não a preserva.
**Boa resposta:** explicar o efeito da calibração em log e do expoente 1,12, reportar viés de massa e NSE linear para todos os modelos e justificar a log sem esconder o custo dela.
**Gravidade:** importante.

### B8. Bootstrap e Wilcoxon
**Pergunta:** "Onde está descrito o Wilcoxon nos métodos? Ele foi aplicado a diferenças de erro percentual, uma métrica assimétrica. Sob que hipótese vale o p de 0,02? E o que quer dizer 'não se explica pelo acaso' quando os eventos não são sorteados e a configuração foi escolhida olhando para eles?"
**Local:** seção 3.4.7, p. 37 (só o bootstrap é descrito; a busca no texto acha "Wilcoxon" apenas na seção 4.3); seção 4.3, p. 48 e 49; Conclusões, p. 59.
**Por que importa:**
- `alteracoes_doc_03-11.md` registra "Wilcoxon definido", mas o PDF não o define.
- O teste supõe eventos trocáveis e diferenças simétricas.
- O intervalo de +3,1 a +117,5 é muito largo e o limite inferior está perto de zero.
- Bootstrap de mediana com 17 pontos é discreto e instável.
- O teste não leva em conta a escolha da configuração.
**Boa resposta:** definir o teste nos métodos, dizer qual é a população de referência, repetir em erro logarítmico e trocar "não se explica pelo acaso" por uma frase condicional à configuração e à amostra.
**Gravidade:** importante.

### B9. Eventos que não são independentes
**Pergunta:** "O evento 16 começa 13 horas depois do fim do evento 15. O seu leave-one-out e o seu bootstrap tratam os dois como independentes? E, se os resíduos do MFM têm tendência ao longo da série, por que não fez um teste de calibrar no início e prever o fim?"
**Local:** Tabela 2, p. 23 (evento 15 termina em 09/02/20 01h; evento 16 começa em 09/02/20 14h); seção 4.3, p. 50 (MFM superestima os eventos 1 a 6 e subestima os 14 a 17).
**Por que importa:** o próprio texto mostra indício de não estacionariedade, e essa é a situação em que o leave-one-out é mais otimista. Calibrar em 2018-2019 e prever 2020 seria um teste mais duro e ainda barato.
**Boa resposta:** reconhecer a dependência e apresentar a divisão temporal ou a validação em blocos.
**Gravidade:** importante.

### B10. O que 17 eventos permitem concluir
**Pergunta:** "São 17 eventos em 15 meses, com 1 no período seco e vazão de pico até cerca de 30 m³/s. Para que população de eventos valem as suas conclusões? Esses 17 são todos os eventos acima do critério no período? E o evento de 24/11/2018?"
**Local:** seção 3.2, p. 22 e 23; seção 2.5, p. 17 (critério de 10 m³/s em Murillo-Bermúdez e Martim, 2022); seção 4.6, p. 56.
**Por que importa:** o TCC não dá critério de seleção nem diz que parcela da carga do período está nos eventos. O LEIAME registra pico de 12,48 m³/s em 24/11/2018 na planilha (não conferi ainda), acima do critério de 2022 e fora da lista. A pergunta 6 de `perguntas_para_o_luis_30-10.md` mostra que não há critério escrito confirmado para a delimitação.
**Boa resposta:** dar o critério escrito, dizer quais eventos ficaram de fora e por quê, informar a fração da carga do período coberta e limitar as conclusões a eventos de cheia dessa faixa.
**Gravidade:** importante.

### B11. A comparação com a IC
**Pergunta:** "A IC tem 2 parâmetros ajustados nos próprios dados, usa volume total e pico, e o MFM tem 1 parâmetro, validação cruzada e só o escoamento direto. Os 17 eventos são os mesmos? Por que você não refez a IC com a mesma validação cruzada, se é uma regressão de minutos? E como a comparação 'demonstra' que a espacialização não é pior?"
**Local:** seção 3.4.8, p. 38; Tabela 13 e Figura 9, p. 48; seção 4.3, p. 49 e 50 ("só indicativa"); Conclusões, p. 60 ("A comparação demonstra que a espacialização não se mostrou pior"); Resumo, p. 7.
**Por que importa:**
- A Figura 9 põe as barras lado a lado como se fossem comparáveis.
- As notas registram que a lista da IC usa 24/11/2018 e o TCC usa 17/12/2018, e que a carga medida difere; o texto não diz isso de forma explícita.
- As notas têm uma IC refeita com validação cruzada, com 16,3%, 100% e NSE log de 0,87, que não entrou no texto (decisão registrada na pergunta 14 das notas ao orientador). Um avaliador pode refazê-la em minutos.
- "Não se mostrou pior" exigiria teste de equivalência, e a frase contradiz o "só indicativa" da 4.3.
**Boa resposta:** declarar as diferenças de lista e de carga, justificar a escolha pelos valores originais e, de preferência, mostrar também a IC em validação cruzada, trocando "demonstra" por "não permite distinguir".
**Gravidade:** pode comprometer.

### B12. K e C sem fonte confirmada
**Pergunta:** "O campo ocupa 29% da bacia e responde por 37% da erosão. De onde vem o C = 0,050? Você leu isso na fonte que cita? E o K de 0,0475 do Cambissolo, que responde por 93% da erosão, representa a classe?"
**Local:** Tabelas 5 e 6, p. 25 e 26; seção 4.5, p. 53; Resumo, p. 7 ("sob os valores de K e C adotados").
**Por que importa:** segundo o lote D (`leitura_referencias/loteD_fontes_K_C.md`):
- Silva et al. (2016) não trata de pastagem, e o C de 0,050 não aparece no artigo, mas a Tabela 6 ainda escreve "com base em Silva et al. (2016)".
- C = 0,212 é o valor da soja; o mesmo artigo dá 0,1418 para cultura anual.
- C = 0,121 é o do eucalipto jovem; o plantio mais velho deu 0,016.
- K = 0,0475 é uma amostra só; a média dos Cambissolos no artigo é 0,036.
- O K de 0,0351 não foi conferido.
A pergunta 17 ao orientador segue aberta.
**Boa resposta:** dizer o que foi e o que não foi confirmado, corrigir a coluna "Fonte" e mostrar quanto o mapa muda com os valores alternativos do próprio lote D. Não recalculado (depende dos rasters).
**Gravidade:** pode comprometer.

### B13. A Tabela 14 é a Tabela 6 disfarçada?
**Pergunta:** "A ordem das classes de uso na erosão por área é a mesma ordem do fator C que você adotou. Esse resultado foi descoberto pelo modelo ou entrou pela tabela?"
**Local:** Tabela 6, p. 26; Tabela 14, p. 53; Conclusões, p. 60 ("46% da área e 83% da erosão").
**Por que importa:** mata (C 0,015; 19), campo (0,05; 129), silvicultura (0,121; 191), lavoura (0,212; 530), solo exposto (1; 1.772), mineração (1; 3.784). A ordem é monótona, salvo o empate em C = 1. O principal resultado "por classe" vem em boa parte da entrada, que é a mais incerta (B12). O mesmo vale para os Cambissolos, que têm 68,6% da área.
**Boa resposta:** separar o efeito de C do efeito de LS e de escoamento dentro de cada classe e apresentar o resultado como consequência das hipóteses.
**Gravidade:** importante.

### B14. A cabeceira recebe menos chuva?
**Pergunta:** "Na seção 3.1 a cabeceira tende a ser a parte mais chuvosa. Na 4.1 e na 4.4 ela recebe menos chuva e por isso produz pouca erosão. Qual das duas vale? E um posto que mede em média 44 mm contra 71,5 mm do outro, com zero no evento 12, foi avaliado quanto à consistência?"
**Local:** seção 3.1, p. 21; seção 4.1, p. 44; seção 4.4, p. 51; seção 4.5, p. 55; Tabela 2, p. 23; Figura 1, p. 22.
**Por que importa:** o gradiente leste-oeste entra direto no mapa, e a partição atribui 63% da variação ao termo de escoamento. Com dois postos nas pontas e nenhum no interior, e relevo de 724 a 1.314 m, o padrão pode ser artefato de um posto. Nenhum teste de consistência dos postos é apresentado, e "não registrou chuva" no evento 12 pode ser falha do posto.
**Boa resposta:** mostrar dupla massa ou comparação com outra fonte de chuva, rodar o mapa com chuva uniforme e informar a coincidência dos pixels críticos. Não recalculado (depende dos rasters).
**Gravidade:** pode comprometer.

### B15. SCS-CN errado na bacia, certo no pixel?
**Pergunta:** "O SCS-CN erra o volume da bacia em até 10 vezes, e o f chega a 9,75. Por que eu deveria acreditar que o mesmo método acerta como esse volume se distribui entre os pixels?"
**Local:** seção 3.4.4, p. 34 ("apenas distribui no espaço"); Tabela 11, p. 41; seção 4.1, p. 44; seção 4.5, p. 52.
**Por que importa:** o padrão do MFM é herdado do SCS-CN. Em chuvas pequenas, a abstração inicial pode ser grande: pela fórmula do texto, S0,20 = 558 mm leva a S0,05 de cerca de 1.180 mm e abstração de cerca de 59 mm (conta manual), enquanto vários eventos têm R de 23 a 36 mm. Nesses eventos o padrão vira quase ligado ou desligado.
**Boa resposta:** admitir que o padrão não foi verificado, mostrar a fração de pixels com Q > 0 nos eventos pequenos e testar outro padrão, como coeficiente de escoamento uniforme.
**Gravidade:** pode comprometer.

### B16. Sentido físico do CN-I e de S
**Pergunta:** "Evento 16 a 13 horas do fim de um evento de 139 mm, em solo seco? Uma retenção média de 490 mm, chegando a mais de 1 m, é física? O CN-I é uma condição de umidade ou um parâmetro de ajuste?"
**Local:** seção 3.4.1.3, p. 30 e 31; Tabela 2, p. 23.
**Por que importa:** o texto admite que foi escolhido pelo volume. As notas registram um critério do NEH-4 (13 de 17 eventos em AMC I) e o teste rejeitado de AMC por evento (viés de +85%), e o TCC não traz nenhum dos dois. CN-I, λ = 0,05 e a conversão de Woodward se empilham fora do contexto de obtenção de cada um, e o erro por faixa de chuva pode ser compensação.
**Boa resposta:** assumir o caráter de ajuste, levar ao texto o teste de AMC por evento e explicar que o +3% decorre da compensação.
**Gravidade:** importante.

### B17. O +3% depende da vazão de base
**Pergunta:** "Seu critério foi bater o volume direto, que depende de BFImax = 0,70. O próprio texto diz que, para rocha dura, a sugestão é 0,25. O cabeçalho do arquivo diz 0,58. Com outro BFImax, a escolha de CN-I e λ continuaria a mesma?"
**Local:** seção 3.2, p. 23; seção 4.6, p. 57; `perguntas_para_o_luis_30-10.md`, pergunta 2.
**Por que importa:** o relatório de checagens dá a fração direta do volume entre 0,384 e 0,612 conforme o cenário. Com V_SCS fixo, o viés iria de cerca de -11% a +41% (conta manual). O MFM é robusto (15% a 22%), mas essa robustez não está no texto, e BFImax de 0,25 não foi testado. A origem da série é "fornecida" e foi reconstruída depois.
**Boa resposta:** apresentar a análise de sensibilidade, incluir 0,25 e dizer que a seleção da configuração é condicional à base.
**Gravidade:** importante.

### B18. Unidade do mapa
**Pergunta:** "No Apêndice A você diz que aquele pixel produz 40,1 kg de sedimento. Mas o c foi calibrado para a soma bater com o exutório. Isso é erosão local ou carga que chegou ao exutório? Se o c é conectividade média, por que muda de 0,0344 para 0,0222 entre MC e MFM?"
**Local:** Apêndice A, p. 65; seção 3.4.4, p. 33 e 34; seção 3.4.9, p. 39; Figura 11, p. 52.
**Por que importa:** a soma do mapa é a carga no exutório por construção, não a erosão local. Rotular o valor em kg ou t por pixel dá aparência de medida a um índice, e a erosão bruta deveria ser maior. O texto diz que c "representa" conectividade e, logo depois, que não deve ser lido como razão de entrega.
**Boa resposta:** apresentar o mapa como índice relativo ou quantis e abandonar "kg por pixel", explicando que c é só um fator de escala.
**Gravidade:** importante.

### B19. Limite de 200 m e fator LS
**Pergunta:** "Por que 200 m, e não 100 ou 300? Se a USLE não vale no canal, por que os pixels de canal continuam no mapa? Quantos pixels batem no limite? A fórmula vale em declividades como as suas?"
**Local:** seção 3.4.1.2, p. 30; seção 4.5, p. 54; Tabela 16, p. 54; Figura 3, p. 26 (a nota da figura limita só a escala de cores).
**Por que importa:**
- Com pixel de 30 m, As = 200 m equivale a cerca de 6.000 m², ou 6,7 pixels a montante (conta manual).
- O limite corta o valor, mas não remove o canal do mapa.
- O texto não mostra sensibilidade, e Hoppen et al. (2019), citados na 2.2, indicam que o método de LS importa.
- O lote B diz que os expoentes 0,4 e 1,3 não foram conferidos em Moore e Burch (1986), só por fonte secundária, que os atribui a Moore e Wilson (1992).
- De memória, não conferido: a literatura de LS restringe essa forma a encostas curtas e menos íngremes, e 65% da área está acima de 20%.
**Boa resposta:** justificar o valor, informar a fração limitada, mostrar o mapa com 100 e 300 m, mascarar a rede de drenagem e confirmar a citação.
**Gravidade:** importante.

### B20. Resolução, escala e defasagem
**Pergunta:** "Um mapa de solos 1:250.000 tem unidade mínima de que tamanho? O que quer dizer um resultado por pixel de 30 m sobre isso? Na Figura 3 há um bloco de CN baixo com limite abrupto na cabeceira: isso é a bacia ou é o polígono do mapa? O MDE, o uso de 2020, o MapBiomas de 2022 e os eventos de 2018 a 2020 conversam?"
**Local:** seção 3.3, p. 24 e 27; seção 3.4.1.1, p. 28 e 29; Figura 3, p. 26 (observação visual em baixa resolução, a confirmar).
**Por que importa:** cada polígono do mapa de solos cobre muito mais do que um pixel; a precisão visual é maior que a real. A cabeceira com pouca erosão pode decorrer em parte desse limite. CN e C vêm de mapas de uso diferentes, e o produto do MDE não é nomeado no texto, assim como o algoritmo de direção de fluxo e o que é a "correção". Sem teste em outra resolução, e o texto mostra que a soma dos pixels depende de n^0,12.
**Boa resposta:** calcular a unidade mínima mapeável, agregar o resultado para uma escala defensável (por exemplo, sub-bacia ou mancha), testar 90 m e declarar as fontes completas.
**Gravidade:** importante.

### B21. Partição do R²
**Pergunta:** "Se em log o escoamento fica com 63%, e em escala linear K * LS * C tem R² de 0,58, qual é a resposta certa para quem vai priorizar os 5% de cima? Essa partição separa causas, se o CN e o C vêm ambos do uso do solo?"
**Local:** seção 3.4.9, p. 39 e 40; seção 4.5, p. 54 e 55; Conclusões, p. 60.
**Por que importa:** a escala log dá o mesmo peso a pixels irrelevantes e aos críticos, mas a decisão está na cauda superior. Os dois termos não são independentes, porque CN e C dependem do uso. O texto reconhece que a partição vale por construção, mas a leva às Conclusões.
**Boa resposta:** calcular a partição só na cauda ou a sobreposição do top 5%, explicar o método (média dos ganhos nas duas ordens) e tratar o resultado como descrição.
**Gravidade:** importante.

### B22. Uso prático do mapa
**Pergunta:** "Sou gestor do comitê PCJ e tenho verba para intervir em 500 hectares. Seu mapa me diz onde? Que redução de carga na captação eu teria? Que fração da erosão está nos 5% críticos? Por que 5%?"
**Local:** seção 3.4.9, p. 39; seção 4.5, p. 55; Figura 11, p. 52; Conclusões, p. 60.
**Por que importa:** os 5% são 7.693 pixels, cerca de 6,9 km² (conta manual), e o texto não diz que fração da erosão eles concentram. O modelo não tem conectividade, então um pixel crítico longe da drenagem pode não afetar a carga. Não há cenário, custo nem faixa de incerteza. A média de 17 eventos não é erosão anual. A área urbana, com erosão nula por hipótese, fica fora, apesar de obras e vias sem pavimento.
**Boa resposta:** dizer que o mapa só faz triagem para vistoria de campo, informar a concentração da erosão, testar 5% e 10%, simular um cenário com P < 1 e combinar com distância à drenagem.
**Gravidade:** importante.

### B23. "Não pôde ser validado"
**Pergunta:** "Não pôde ou não foi? Uma visita a campo, imagens de alta resolução nas manchas críticas ou o sedimento medido em algum afluente não dariam uma verificação parcial?"
**Local:** seção 4.5, p. 55; seção 1.2, p. 10.
**Por que importa:** sem medição de sedimento interna, ainda há verificações parciais de baixo custo, como conferir se o solo exposto e a mineração de maior peso existem de fato. A mancha ao sul na Figura 11 é um alvo óbvio.
**Boa resposta:** separar validação quantitativa, impossível aqui, de verificação qualitativa, possível, e fazer ao menos uma amostra.
**Gravidade:** importante.

### B24. Erro da observação
**Pergunta:** "Qual é o erro da sua carga medida? Um erro mediano de 16% a 21% está acima ou abaixo da incerteza da curva de turbidez e da curva-chave? O evento 17 está fora da faixa de calibração, ou só acima da quebra de 250 NTU?"
**Local:** seção 2.5, p. 16 e 17; seção 4.3, p. 50; seção 4.6, p. 57.
**Por que importa:** o texto usa "medido" e nunca dá faixa de incerteza. Quebra de trecho não é limite de calibração. As perguntas 4 e 16 ao orientador mostram que não está confirmada a curva usada (potência de 2022 ou por partes de 2023) nem a faixa das amostras. "3.806 mg/L" é carga total dividida por volume direto, portanto não é concentração.
**Boa resposta:** dizer qual curva foi usada e a faixa das amostras, estimar a incerteza da carga e não comparar modelos abaixo desse piso.
**Gravidade:** importante.

### B25. Reprodutibilidade e contribuição original
**Pergunta:** "Onde eu baixo o seu código e os seus dados? Em outro computador, roda? Qual é, numa frase, a contribuição original deste trabalho, e todos os objetivos foram cumpridos, inclusive 'validar o modelo'?"
**Local:** seção 3.4, p. 28; Conclusões, p. 59; Objetivos 3 e 6, p. 11.
**Por que importa:**
- O TCC não informa repositório nem disponibilidade dos dados (a busca por "github" e "repositório" não acha nada no texto).
- `README.md` descreve repositório privado, rasters em Google Drive pessoal e caminhos fixos; 61 dos 64 scripts em `Scripts/*.py` têm caminho fixo `C:`.
- Não há arquivo de dependências na raiz.
- Não encontrei "wilcoxon" em `Scripts/*.py` (busca só nesse nível; falta olhar as subpastas).
- O objetivo 3 fala em validar, mas o leave-one-out refaz só um coeficiente, e o próprio texto diz que os resultados quase não mudam.
**Boa resposta:** indicar script principal, versão e dados, dizer o que é público, e formular a contribuição com sobriedade: um diagnóstico comparativo com referências simples, mais um mapa relativo, e não um modelo validado.
**Gravidade:** importante.

## (d) As 5 perguntas mais difíceis

1. **B1:** teste de placebo do mapa. Mostra que a validação é cega para o espaço.
2. **B2:** para que espacializar. O dilema não tem saída fácil.
3. **B3:** a atenuante da 3.4.6 contra os 88% da 4.3. É contradição interna do texto.
4. **B5:** "o limite está na conversão". Pergunta se a conclusão central é em parte aritmética.
5. **B12:** K e C com fonte não confirmada, junto com a B13, porque o resultado por classe depende diretamente deles.

## (e) O que eu elogiaria

- A coragem de relatar que o MC perde para uma regra simples e de usar referências simples como critério de comparação (seção 3.4.8).
- A frase "não é uma validação da fórmula de erosão nem do mapa" (seção 4.3).
- A discussão de validação aninhada e a admissão de que ela não foi feita (seção 3.4.6).
- A calibração simples de um único coeficiente, com solução direta e sem excesso de parâmetros.
- A preocupação com métricas robustas e o teste de retirar os eventos 15 e 17.
- O Apêndice A, cujas contas conferi à mão nos passos II a V; bateram.
- A seção 4.6, organizada na ordem da cadeia de cálculo.

## Falta fazer

1. **Recalcular a estatística a partir das Tabelas 2, 3, 11 e 12** (o script falhou e nada foi rodado ainda): Wilcoxon e bootstrap em APE e em erro logarítmico; modelo nulo constante, com fator 2 e erro mediano; IC em validação cruzada; intervalos do fator 2; divisão temporal; correlação do erro do volume com a duração da janela; papel de RI/R.
2. **Conferir na planilha `Dados Iniciais/Dados_finais_histereses_corrigido.xlsx`:** pico de 24/11/2018, outros picos acima de 10 m³/s fora da lista, fração da carga do período nos eventos e faixa de turbidez.
3. **Ver as figuras que faltam** (Figuras 2, 4, 5, 6, 7, 10, A1 e A2) e confirmar em resolução maior o limite abrupto do CN na Figura 3.
4. **Olhar as subpastas de `Scripts/`** antes de afirmar que falta o código do Wilcoxon e do bootstrap final.
5. **Revisar a ordem e o texto das perguntas**, acrescentar à B8, B9, B10 e B11 os números recalculados e tirar o aviso de versão parcial.
6. **Verificar a afirmação "de memória" da B19** ou mantê-la marcada como não conferida.
