# Banca simulada: parecer e perguntas do Avaliador A (hidrologia e hidrossedimentologia)

Versão analisada: `TCC_Texto/TCC_versao_04-11.pdf`. Estado deste arquivo: perguntas completas, com as contas incorporadas na retomada na nuvem (04/11). O que ficou em aberto está em "Falta fazer", no fim.

## (a) O que foi lido

- Lido inteiro, pelo texto marcado por página (`Notas Claude/doc_texto_pdf_paginas_04-11.txt`): resumo, capítulos 1 a 5, referências e Apêndice A (68 páginas). As páginas citadas abaixo são as do PDF.
- Não lidos, como pedido: `1_revisao_texto.md`, `3_avaliador_B.md`, `revisao_processo_29-10.md`, `revisao_independente_03-11.md`.
- Figuras: na primeira leitura só as legendas. Na retomada (nuvem, 04/11) foram vistas a 200 dpi as Figuras 7 e 8 (PDF p. 46 e 47). Nada abaixo depende de leitura visual das outras figuras.
- Conferido depois da primeira leitura, só para testar dúvidas: `Notas Claude/relatorio_checagens_base_alvo_woodward_27-10.md` (parte inicial), `Notas Claude/resumo_modelo_completo.md` (passos 2 e 3), `Notas Claude/teste_cn_calibrado.md` (parte inicial), `Notas Claude/perguntas_para_o_luis_30-10.md` (item 2), `Notas Claude/leitura_referencias/loteA_...md` (Hao e Baert) e `loteB_...md` (Moore e Burch).
- Contas à mão: feitas com as Tabelas 2, 3, 11 e 12 e os valores do texto. Cada uma está indicada como "conta minha".
- Literatura: os originais NÃO foram reabertos. O que digo de Hao e de Baert vem da nota do lote A. Onde cito algo de memória, está escrito "de memória, não conferido". Rasters: não recalculado.

## (b) Parecer curto

O trabalho é honesto, e isso é raro. O aluno mostra que o modelo calculado perde para uma regra proporcional à chuva e que o modelo forçado não se distingue de uma regra proporcional ao volume. Ele também escreve que o mapa não foi validado. A organização, o exemplo numérico e a clareza sobre o que é ajuste e o que é validação estão acima do esperado em um TCC.

O ponto fraco é que a conclusão central vai além do que o desenho permite. "O limite está, portanto, na conversão da chuva em escoamento" se apoia em uma comparação em que o volume entra dos dois lados. O próprio aluno reconhece isso na seção 4.3, mas o resumo mantém a frase. Além disso, várias falhas atribuídas "ao método SCS-CN" podem vir da configuração escolhida (S médio de 490 mm), da seleção dos eventos (pico de pelo menos 10 m³/s) ou das janelas de vários dias, e nada disso foi testado no texto. Por fim, a validação no exutório não tem poder nenhum sobre o padrão espacial, e o padrão espacial é o produto que dá título ao trabalho. Eu aprovaria com arguição dura, pedindo que resumo e conclusões sejam ajustados ao que os dados sustentam.

## (c) Perguntas, da mais importante para a menos importante

### A1. O MFM prova mesmo que o gargalo é o escoamento?
- **Pergunta:** "A carga medida é a soma de vazão vezes concentração. O MFM recebe o volume desse mesmo hidrograma. Então o volume está dos dois lados da comparação. Com que base o seu resumo diz 'o limite está, portanto, na conversão da chuva em escoamento'?"
- **Local:** Resumo (p. 7); seção 4.3 (p. 50 do PDF, "Como nada mais muda entre as duas versões"; e a ressalva logo depois, "por construção"); Conclusões (p. 60 e 61). Ver também seção 2.5 (p. 18): "a carga de um evento não pode ser estimada só pela vazão por uma relação fixa", enquanto a seção 4.3 mostra uma relação fixa com o volume com 15,9% de erro.
- **Por que importa:** é a principal conclusão. O 94%, os 91% da seção 4.2 e os 88% da seção 4.3 são o mesmo fato visto três vezes, e não três evidências. A conta do erro do MC se decompõe em 1,12 * ln(V_SCS/Vdir) mais o resíduo do MFM (conta minha), então os 91% decorrem do bom ajuste do MFM.
- **Boa resposta:** separar o que é autocorrelação do que é evidência. Dizer que o argumento mais limpo é outro: a regra com a chuva usa a mesma chuva e ganha do MC, o que isola a curva SCS-CN do erro de chuva. Propor um teste sem autocorrelação, como prever a concentração média (carga/volume) em vez da carga. Explicar a diferença entre relação instantânea C x Q (histerese, seção 2.5) e relação integrada no evento. Aceitar mudar a frase do resumo.
- **Gravidade:** pode comprometer.

### A2. O que a validação no exutório diz sobre o mapa?
- **Pergunta:** "Se eu embaralhar K, C e LS entre os pixels da bacia e recalibrar c, o que acontece com os seus 81% e 21%? Se quase nada muda, o que o objetivo específico 3, 'validar o modelo distribuído', validou?"
- **Local:** seção 1.3.2, objetivo 3 (p. 12); seção 4.3 (p. 50); seção 4.5 (p. 53 a 56). K, C e LS não mudam entre eventos (seção 4.2, p. 48).
- **Por que importa:** o c absorve a média de K * C * LS. O que resta entre eventos vem de chuva, volume e RI/R. O teste no exutório é praticamente cego ao padrão espacial, e o título promete identificar áreas críticas. Teste não recalculado, pois depende dos rasters.
- **Boa resposta:** admitir que o exutório não testa o padrão, rodar o teste de embaralhar como demonstração e separar "modelo de evento" de "mapa condicional às hipóteses". Propor validação espacial possível: seções em afluentes, feições erosivas por imagem, traçadores ou comparação com outro modelo, deixando claro que comparar modelos não é validar.
- **Gravidade:** pode comprometer.

### A3. CN seco logo depois de 139 mm de chuva?
- **Pergunta:** "O evento 15 termina em 09/02/2020 às 01h, depois de 139 mm. O evento 16 começa 13 horas depois. Você usa nele a condição seca, CN-I. Que hipótese física sustenta isso? E por que o evento 16 ainda é superestimado (razão 1,21) mesmo assim?"
- **Local:** Tabela 2 (p. 24), Tabela 11 (p. 42), seção 3.4.1.3 (p. 32): "uma condição única [...] escolhida pelo volume, e não uma medida da umidade antecedente".
- **Por que importa:** AMC I é um conceito físico sobre chuva antecedente, e aqui virou parâmetro de ajuste. O texto não apresenta a análise da chuva antecedente. Nas notas existe: pelo critério do NEH-4, 13 dos 17 eventos cairiam em AMC I, e aplicar a umidade evento a evento foi testado e rejeitado, com eventos em AMC III dando de 1,75 a 6,6 vezes o medido (`resumo_modelo_completo.md`, passo 2). Isso é informação útil que ficou fora do texto.
- **Boa resposta:** dizer sem rodeio que CN-I funciona como fator de calibração de S, e não como estado da bacia. Mostrar a classificação AMC evento a evento e o teste rejeitado. Explicar que, se até o estado "certo" piora o volume, a própria estrutura do método está em questão nesta bacia.
- **Gravidade:** pode comprometer.

### A4. A falha é do método ou da sua configuração?
- **Pergunta:** "S médio de 490 mm para chuva média de 63 mm. Nessa faixa, Q é quase P²/S. Foi o SCS-CN que errou a forma da curva, ou foi você quem colocou a bacia na parte mais curva da equação para acertar o total?"
- **Local:** seção 3.4.1.3 (p. 31 e 32), seção 4.1 (p. 43 e 44: "A forma da curva do método não parece corresponder"), seção 4.2 (p. 48), Conclusões (p. 60).
- **Por que importa:** o trabalho generaliza para o método ("a passagem pelo SCS-CN piora a estimativa", p. 50), mas só uma configuração foi avaliada no texto. Um CN maior deixa a curva mais próxima de uma reta na faixa de chuva. O total só bate porque erros de sinais opostos se compensam, como o próprio texto diz. As notas indicam que formas calibradas viram quase um coeficiente de escoamento constante (`teste_cn_calibrado.md`, item 3), mas isso não está no TCC.
- **Conta minha (Tabelas 2 e 3, em log contra R):** a inclinação de V_SCS é 2,58 (R² 0,99), e a de Vdir é 1,17 (R² 0,57). Ou seja, o modelo faz o volume crescer com a chuva elevada a 2,6, e a bacia, com a chuva elevada a cerca de 1,2. É a forma P²/S aparecendo nos números.
- **Boa resposta:** separar três coisas: equação, CN tabelado e configuração. Mostrar a inclinação de V_SCS contra R em escala log comparada à de Vdir contra R. Trazer o teste de CN calibrado, com a ressalva de que, nas notas, ele não superou a regressão simples com a chuva. Restringir a frase a "nesta configuração e com estes dados".
- **Gravidade:** pode comprometer.

### A5. O que suas conclusões podem e não podem afirmar?
- **Pergunta:** "Em uma frase, sem ressalvas: o modelo que você construiu serve para prever o sedimento de um evento nesta bacia? E com que direito o texto indica onde colocar prática conservacionista?"
- **Local:** Conclusões (p. 60 e 61): "A comparação demonstra que a espacialização não se mostrou pior"; seção 4.5 (p. 56): "candidatas a práticas conservacionistas"; seção 4.2 (p. 48): "não indica [...] que a fórmula de erosão ou a espacialização sejam inadequadas"; seção 4.3 (p. 51): "não permite dizer que um seja melhor que o outro".
- **Por que importa:** a única versão preditiva (MC) erra 81% e perde para a regra simples. O "não se mostrou pior" só vale para a versão que recebe o volume medido, em que a espacialização quase não atua. Não distinguir com n = 17 não demonstra equivalência. E dizer que o resultado "não indica inadequação" é pouco falseável, porque também não indica adequação.
- **Boa resposta:** dizer "não serve para previsão". Listar o que fica de pé: a hierarquia chuva x volume medido, o mapa como hipótese de trabalho e a base de dados. Trocar "demonstra" por um verbo mais fraco. Dizer que o mapa orienta onde verificar em campo antes de orientar onde investir.
- **Gravidade:** pode comprometer.

### A6. A seleção dos eventos cria o resultado sobre o coeficiente de escoamento?
- **Pergunta:** "Seus eventos foram escolhidos por terem pico de pelo menos 10 m³/s, certo? Então uma chuva pequena só entra na amostra se tiver respondido muito. Isso não explica, ao menos em parte, a correlação de -0,01 e a subestimação dos eventos pequenos?"
- **Local:** seção 2.5 (p. 18, critério de 10 m³/s, citado só como trabalho anterior); seção 3.2 (p. 23, sem critério de seleção); seção 4.1 (p. 43 e 44); Conclusões (p. 60). Ver também o ponto do LEIAME: pico de 12,48 m³/s em 24/11/2018, que fica fora da lista, depois do fim do evento 1.
- **Por que importa:** selecionar pela resposta trunca a amostra. Em uma amostra assim, a relação entre coeficiente de escoamento e chuva fica distorcida. A conclusão "a fração da chuva que escoa não cresce com a chuva" pode ser, em parte, artefato. Os eventos 1, 4, 7 e 10, os mais subestimados, são justamente os candidatos a esse efeito.
- **Conferido na planilha:** `eventos_processados_manuais.xlsx` e `eventos_definidos_artigo_I4SDWI_corrigido.xlsx` listam um evento "1B", de 24/11/2018 16h a 26/11/2018 21h, com pico de 12,484 m³/s e volume total de 1.391 mil m³, maior que o do evento 1 ("1A", 409 mil m³). Ele está na lista de partida e foi tirado depois. O motivo não está nas notas consultadas.
- **Boa resposta:** declarar o critério e a lista de eventos excluídos na seção 3.2. Levantar as chuvas grandes do período que não passaram do limite e ver o volume delas. Reconhecer o viés e explicar por que 24/11/2018 ficou de fora.
- **Gravidade:** pode comprometer.

### A7. O que c é de verdade?
- **Pergunta:** "Você diz que c representa uma conectividade média da bacia e, na mesma frase, que não deve ser lido como razão de entrega. Se a bacia é a mesma, por que c é 0,0344 em um modelo e 0,0222 no outro? E, escrevendo o volume em m³, como fez Williams, c vira cerca de 1,65 e 1,06. Conectividade maior que 1?"
- **Local:** seção 3.4.4 (p. 34 e 35), seção 3.4.3 (p. 34), Tabela 9 (p. 36), seção 4.6 (p. 58).
- **Por que importa:** c tem um fator de unidade (1000^0,56, cerca de 48; conta minha), um fator de grade (o texto mostra n^0,12), a compensação do viés do escoamento (razão de 1,55 entre os dois c) e, talvez, entrega. Ele depende do tamanho do pixel e não pode ser transferido. A palavra "conectividade" dá um sentido físico que o número não sustenta. A nota do lote A registra que a fórmula impressa em Hao não tem o /1000.
- **Boa resposta:** chamar c de coeficiente de escala empírico, sem significado físico isolado. Listar o que ele absorve. Explicar que a diferença entre MC e MFM é compensação da hidrologia. Dizer que não pode ser usado em outra bacia ou grade. Retirar "conectividade média" ou qualificá-la.
- **Gravidade:** pode comprometer.

### A8. "Medido" e "superficial": de onde vem o seu Vdir?
- **Pergunta:** "Você escreve 'escoamento superficial direto medido'. Ele não é medido, sai de um filtro, e o filtro não sabe se a água veio pela superfície. Quem gerou a coluna Bt? Com que critério? E se BFImax não for 0,70, o seu +3% continua existindo?"
- **Local:** seção 3.2 (p. 24), Tabela 1 (p. 23), Tabela 3 ("estimado", p. 25) contra Tabela 7 ("medido", p. 30), seção 3.4.1.3 (p. 32), seção 4.6 (p. 58).
- **Por que importa:** a separação é o alvo do critério que escolheu CN-I e λ, portanto o erro se propaga para toda a hidrologia. Usando as frações ΣVdir/ΣTR de `relatorio_checagens...27-10.md`, conta minha sobre V_SCS = 15.702 mil m³: viés de cerca de -11% com BFImax 0,58, de +3% com 0,70, de +21% com 0,80. O texto não traz essa sensibilidade, embora o MFM tenha se mostrado estável nela. Nas notas consultadas, 0,25 não foi testado, e é o valor que a seção 4.6 aponta como mais próximo da geologia. Conta minha, nesta revisão (filtro de Eckhardt com a = 0,995 sobre a vazão da planilha, nas 17 janelas): com BFImax 0,70 a soma de Vdir dá 15.225 mil m³ (a coluna Bt dá 15.263, igual à Tabela 3), e com 0,25 dá 24.571 mil m³, 85% do volume total; o viés de V_SCS passaria de +3% para -36%. `perguntas_para_o_luis_30-10.md` registra que o cabeçalho do arquivo do orientador diz 0,58, enquanto a série se reproduz com 0,70. Além disso, a = 0,995 por hora equivale a 0,887 por dia, ou tempo característico de cerca de 8 dias (conta minha): é rápido para água subterrânea, e o texto não mostra análise de recessão.
- **Boa resposta:** dizer "estimado" e usar "escoamento rápido" ou "direto", sem "superficial". Informar a origem de Bt e a dúvida entre 0,58 e 0,70. Mostrar a tabela de sensibilidade, incluindo 0,25. Explicar que o MFM é estável porque c absorve um fator parecido entre eventos, mas que a escolha do CN não é estável. Mencionar fluxo subsuperficial em solos de encosta sobre embasamento cristalino.
- **Gravidade:** pode comprometer.

### A9. Toda a carga vem da encosta?
- **Pergunta:** "Você tira a vazão de base da água, mas deixa na carga o que ela transporta, e compara tudo com a erosão de encosta. Você também cita laços de histerese, 13 em oito e 4 horários, e não volta a eles. O que um laço horário diz sobre a fonte do sedimento? Isso combina com a sua hipótese?"
- **Local:** Resumo (p. 7); seção 3.2 (p. 24); seção 3.4.4 (p. 35): "a vazão de base atua apenas como meio de transporte"; seção 2.5 (p. 18); seção 4.6 (p. 58).
- **Por que importa:** é uma assimetria entre entrada e alvo, e o canal é uma fonte sem nenhum termo no modelo. Se a carga de canal é relevante, c e o mapa atribuem às encostas o que não veio delas. As notas mostram o quanto a parcela da base é incerta: 34% da carga se a base tiver a concentração da mistura, 6,8% com 119 mg/L (`relatorio_checagens...27-10.md`, conclusão 4). Esses números não estão no TCC.
- **Boa resposta:** explicar a decisão e a hipótese, separando a água de base (sem erosão de encosta) da carga de fundo e da remobilização do canal. Citar o teste com o alvo direto, em que a ordem dos modelos não mudou. Relacionar o tipo de laço de cada evento aos resíduos. Dizer que a parcela do canal não foi estimada.
- **Gravidade:** pode comprometer.

### A10. Dois postos: o gradiente de chuva é real?
- **Pergunta:** "Em média, DBT5 tem 44 mm por evento e Campo Limpo, 72 mm. Na seção 3.1 você diz que a cabeceira tende a estar na parte mais chuvosa, e nas seções 4.1 e 4.4 diz que a cabeceira recebe menos chuva. Qual das duas? Você fez consistência desses postos? O zero do DBT5 no evento 12 é chuva zero ou falha?"
- **Local:** seção 3.1 (p. 22), Tabela 2 (p. 24), seção 4.1 (p. 45), seção 4.4 (p. 52), seção 4.5 (p. 55 e 56), seção 3.4.1.4 (p. 32 e 33).
- **Por que importa:** o texto atribui cerca de 63% da variação espacial (em log) ao termo de escoamento, que inclui esse gradiente. A leste, fora da bacia, um posto que mede sistematicamente menos deixa a cabeceira sem áreas críticas. Os postos ficam a cerca de 29 km um do outro (conta minha), com altitudes de 724 a 1.314 m na bacia, e a interpolação não usa o relevo. A escala do Plano (sub-bacia inteira) é diferente da escala do alto curso, e por isso as frases podem não ser contraditórias, mas o aluno precisa saber explicar. A chuva da cabeceira não é medida.
- **Boa resposta:** apresentar curva de dupla massa ou comparação com outro posto ou produto de chuva. Refazer o mapa com chuva uniforme (MC sem gradiente) e medir quantos pixels críticos permanecem. Explicar por que R tem pesos 0,307 e 0,693 e por que difere da média por IDW.
- **Gravidade:** importante, podendo comprometer o mapa.

### A11. Escolher pelo volume protege a avaliação da carga?
- **Pergunta:** "Na seção 3.4.6, você diz que o viés é reduzido porque escolheu pelo volume, e não pela carga. Na seção 4.3, você mostra que o volume explica 88% da carga. Como as duas frases ficam de pé juntas? E por que 16 eventos em cada rodada seriam um impedimento para o aninhamento?"
- **Local:** seção 3.4.6 (p. 37), seção 4.3 (p. 50), seção 3.4.1.3 (p. 32), seção 2.8 (p. 20 e 21).
- **Por que importa:** a defesa contra o viés de otimismo enfraquece. Também o texto não informa quantas configurações foram testadas nem traz a tabela delas. Um parâmetro único recalibrado em leave-one-out muda muito pouco, como a seção 4.2 admite. Ou seja, a validação cruzada pouco testa aqui. Aliás, 16 de 17 é quase toda a amostra; o argumento em si não justifica a omissão.
- **Boa resposta:** informar quantas configurações foram testadas e mostrar a tabela. Rodar o aninhado, que é barato (as notas têm um exercício desse tipo para versão anterior). Admitir que o leave-one-out aqui é verificação fraca e que o teste real seria com eventos fora do período.
- **Gravidade:** importante.

### A12. Qual a incerteza da carga "medida"?
- **Pergunta:** "Qual foi a maior turbidez usada na curva? Que fração da carga de cada evento vem de leituras acima dela? Com a turbidez de uma leitura por hora, em uma estação de tratamento e não na seção, qual é o erro da sua carga? Ele é menor que os 21% que você comemora?"
- **Local:** seção 2.5 (p. 17 e 18), seção 3.2 (p. 23), Tabela 1, seção 4.6 (p. 58): "muito acima"; seção 4.3 (p. 51).
- **Por que importa:** SYobs é tratado como verdade, sem barra de erro. O texto não informa número de amostras, R², faixa de ajuste nem o valor máximo de turbidez. Se a incerteza da carga for da ordem de 20% a 30%, diferenças entre modelos ficam abaixo do ruído da medição. A coleta em um ponto, a defasagem entre o rio e a estação, a matéria orgânica de esgoto na turbidez e a falta de arraste de fundo e areia também pesam: a MUSLE estima sedimento total, e a turbidez vê sobretudo os finos.
- **Conferido na planilha:** a planilha tem a concentração (CSS), e não a turbidez, por isso a faixa de turbidez não pôde ser conferida. A maior CSS da série é 4.844 mg/L (19/03/2021); dentro dos eventos, 4.602 mg/L (evento 12) e 4.227 mg/L (evento 17). Nos 17 eventos não há hora sem CSS.
- **Boa resposta:** citar os números da curva de Murillo-Bermúdez et al. (2023). Calcular a parcela da carga fora da faixa em cada evento. Propagar a incerteza da curva até a carga. Dizer onde fica a captação em relação à estação de vazão. Chamar o dado de "carga estimada".
- **Gravidade:** importante.

### A13. O que aconteceu no evento 17?
- **Pergunta:** "No evento 17, os dois postos concordam (68 e 65 mm), o que é raro na sua série, a intensidade é alta, a bacia vem de duas semanas muito chuvosas, e mesmo assim o coeficiente de escoamento é de cerca de 5%, um dos menores. A concentração média é de cerca de 1.940 mg/L, mais que o dobro da média geral de 824 mg/L. Como você explica isso, e que dado fecharia a dúvida?"
- **Local:** seção 4.3 (p. 51), seção 4.6 (p. 58), Tabelas 2, 3 e 11. Os valores 1.940 e 824 mg/L e o coeficiente são conta minha, com carga/TR e Vdir/(R * A).
- **Por que importa:** o texto usa 3.806 mg/L, que é carga dividida por Vdir: não é concentração física e exagera o contraste. As duas explicações dadas (curva fora da faixa, obra ou deslizamento) são hipóteses sem teste. O volume baixo também merece suspeita, pois chuva, vazão e janela podem ter problema no evento.
- **Conferido hora a hora na planilha (20 a 22/02/2020):** a chuva cai entre 16h e 18h de 20/02 (DBT5 18,8 + 43,0 + 2,0 mm; Campo Limpo 7,0 + 34,8 + 18,4 mm). A CSS sobe de 83 para 705 mg/L às 18h e para 4.227 mg/L às 19h, com a vazão ainda em 2,0 m³/s. A vazão só sobe às 20h (4,6) e chega ao pico às 21h (21,4 m³/s). A CSS fica entre 3.742 e 4.227 mg/L por seis horas seguidas, como um patamar. Duas leituras possíveis, nenhuma testada: (1) sedimento de uma fonte perto do ponto de coleta (área urbana, obra, margem) chegando antes da onda de cheia; (2) defasagem de relógio entre a série de turbidez e a de vazão, ou limite do sensor. Nos outros eventos o pico de CSS também vem antes do de vazão (12 de 17, quase sempre 2 h no caso dos picos rápidos), então a antecipação não é exclusiva do evento 17; o patamar alto é. Chuva nos 14 dias antes: 96 mm (DBT5) e 150 mm (Campo Limpo).
- **Boa resposta:** olhar hora a hora turbidez, vazão e chuva. Verificar se a turbidez saturou. Procurar imagens, notícias e registros de obra ou deslizamento em fevereiro de 2020. Usar "carga por volume direto", e não "concentração". Manter o evento e mostrar os resultados com e sem ele, como já fez.
- **Gravidade:** importante.

### A14. A mudança entre as estações invalida um c único?
- **Pergunta:** "O MFM superestima os eventos 1 a 6 e subestima os eventos 14 a 17. Isso é um sinal no tempo. Por que então você usou leave-one-out, que supõe eventos trocáveis, em vez de calibrar em 2018-2019 e prever 2020?"
- **Local:** seção 4.3 (p. 51), seção 3.4.6 (p. 36 e 37). Entre os eventos 10 e 12 há nove meses, com um único evento, o 11, em julho.
- **Por que importa:** uma deriva quebra a hipótese da validação. A causa pode estar no sensor, na curva, na bacia (uso, obras) ou no início de estação chuvosa. O contraste de 1.450 para 1.700 mg/L é dado sem teste de significância e sem o evento 17, e com poucos eventos pode ser ruído. O CN de 2022 e o C de 2020 também não acompanham essas mudanças.
- **Conta minha (Tabelas 2, 3 e 12):** o erro em log do MFM tem Spearman de -0,68 com a ordem dos eventos (p = 0,002). Calibrando c nos eventos 1 a 11 e prevendo os eventos 12 a 17: MFM com erro mediano de 16,9% e razão mediana simulado/medido de 0,83; regra com Vdir, 27,2% e 0,79. No sentido inverso (12 a 17 para 1 a 11), o MFM erra 37,7% (razão 1,38). Carga por Vdir: 1.455 mg/L nos eventos 1 a 11 contra 1.685 mg/L nos eventos 12 a 16, com p = 0,30 (t) e 0,18 (Mann-Whitney). Ou seja, a tendência é clara, mas a diferença entre os dois grupos não é distinguível com tão poucos eventos.
- **Boa resposta:** fazer o teste de divisão temporal. Testar a diferença entre grupos. Verificar datas de manutenção e troca do turbidímetro. Comparar a relação turbidez x CSS por período. Dizer o que um c por estação custaria em graus de liberdade.
- **Gravidade:** importante.

### A15. SCS-CN em evento de seis dias?
- **Pergunta:** "Sua janela vai até 149 horas, e 14 dos 17 eventos passam de 48 horas. O SCS-CN trata isso como uma única chuva, sem recuperação de abstração entre os pulsos. A superestimativa dos eventos grandes não vem daí?"
- **Local:** Tabela 2 (p. 24), seção 3.4.2 (p. 33), seção 4.1 (p. 43), seção 4.6 (p. 57). Contagem é conta minha.
- **Por que importa:** o texto trata a delimitação como limitação sem estimativa, e explica o erro pela forma da curva. Há uma explicação alternativa testável. O inverso também ocorre: uma janela que começa na recessão de evento anterior atribui ao evento um volume sem chuva correspondente, o que pode inflar Vdir nos eventos pequenos, como o evento 10 (1.236 mil m³ com 25,8 mm, contra 409 mil m³ com 23,4 mm no evento 1).
- **Conferido na planilha (vazão no início de cada janela, menos a base Bt):** em 13 eventos a vazão inicial está a menos de 0,7 m³/s da base. Nos eventos 5 e 10 a janela começa na recessão do evento anterior: 2,0 e 1,2 m³/s acima da base; no evento 10, a vazão inicial é 35% do pico. Conta minha a favor do aluno: a razão V_SCS/Vdir tem correlação de 0,79 com ln R e só 0,37 com a duração, então a duração da janela não é a explicação principal do erro de volume.
- **Boa resposta:** rodar o SCS-CN por pulso de chuva nas janelas longas. Relacionar a razão calculado/medido com a duração. Quantificar a vazão no início da janela. Ter um critério objetivo de início e fim, e medir a sensibilidade a ele.
- **Gravidade:** importante.

### A16. Woodward em cima de CN-I: é legítimo? Quem faz o trabalho, λ ou CN-I?
- **Pergunta:** "A relação de Woodward foi ajustada com S de bacias americanas. Você a aplica sobre um S que já passou pela conversão para condição seca. No seu pixel de exemplo, com CN-I e λ = 0,20, eu calculo cerca de 11,7 mm, e com a sua conversão dá 13,0 mm. Então o que muda de fato é o CN-I, não o λ. Por que dizer que adotou λ = 0,05 por causa da literatura, se Brandão associa clima úmido a λ maior?"
- **Local:** seção 2.3 (p. 15 a 17), seção 3.4.1.3 (p. 31 e 32), Apêndice A (p. 66), seção 4.6 (p. 57). Conta minha com P = 75,4 mm e S0,20 = 141,9 mm. As notas (`resumo_modelo_completo.md`, passo 3) indicam viés de -12% com λ = 0,20 e +3% com a conversão.
- **Por que importa:** são duas transformações em sequência que aumentam S, e a segunda é uma regressão usada fora do seu contexto (8,4% dos pixels e dois eventos em extrapolação). Baert obteve NSE negativo com a mesma conversão, como o texto registra. Literatura citada conforme o próprio TCC e a nota do lote A.
- **Boa resposta:** assumir que CN-I com S convertido equivale a um ajuste de S, e dizer qual é o CN efetivo. Explicar o efeito de λ nas chuvas pequenas, o que sobra de ganho e a falta de prova do valor de λ nesta bacia. Considerar calibrar diretamente um multiplicador de S, com aninhamento.
- **Gravidade:** importante.

### A17. Williams no pixel: qual é o significado de pr?
- **Pergunta:** "Um pixel de 30 m tem tempo de concentração de minutos, e sua intensidade é de uma hora, de um único valor para a bacia, tirada do posto mais intenso. No evento 12, RI/R dá 1,38. O que é pr? Se o único papel dele é multiplicar cada evento por (RI/R)^0,56, ele melhorou alguma coisa em relação a SY = c * Vdir?"
- **Local:** seções 2.6 e 3.4.3 (p. 18, 33 e 34), seção 4.3 (p. 50), seção 4.6 (p. 58).
- **Por que importa:** o texto já diz que pr não traz informação espacial. Entre eventos, a diferença entre MFM e regra com o volume é o expoente 1,12 e o termo RI/R, e o MFM não ganhou. O expoente 1,12 é maior que o observado (0,94), e os coeficientes de Williams são mantidos fora da faixa de ajuste só para dar um índice.
- **Conta minha:** ln(carga/Vdir) contra ln(RI/R) tem r = 0,28 (p = 0,28): o termo de intensidade quase não explica a carga por volume. Mesmo assim, ele pode mudar um evento em até 3,35 vezes. Em validação cruzada, c * Vdir^1,12 dá 17,3% de erro mediano, e c * Vdir^1,12 * (RI/R)^0,56 dá 22,3%: o termo de intensidade piora um pouco.
- **Boa resposta:** chamar pr de índice de concentração temporal. Testar se o resíduo de carga/volume se relaciona com RI/R. Corrigir R e RI para mesma base (mesmo posto ou mesma média). Dizer que a escolha de manter 11,8 e 0,56 é consequência de seguir Hao, e o que mudaria com expoente calibrado.
- **Gravidade:** importante.

### A18. Por que seguir Hao sem a conectividade? E a deposição?
- **Pergunta:** "O artigo que você segue tem a conectividade no título. Você tira justamente isso. O índice de Borselli sai do MDE e do C, que você já tem. Por que não calculá-lo, mesmo sem calibrar, para ver quanto o mapa muda? Um pixel de lavoura no topo do morro, longe do rio, vale tanto quanto um na margem?"
- **Local:** seções 2.1 e 2.6 (p. 13, 18 e 19), seção 3.4.4 (p. 34 e 35), seção 4.5 (p. 56), seção 4.6 (p. 58).
- **Por que importa:** Hao encontrou conectividade abaixo de 0,5 em cerca de 80% da área. Sem conectividade, a prioridade pode cair em lugares que não entregam nada ao rio. Há também inconsistência: LS usa a área a montante, mas Q é só do próprio pixel, sem escoamento vindo de cima, sem deposição em sopé e sem filtro de mata ciliar. Os mapas em "t por pixel" não são erosão bruta nem entrega, e por isso não podem ser comparados com tolerância de perda de solo.
- **Boa resposta:** explicar que calibrar conectividade em 17 eventos seria arriscado, mas que calcular o índice como análise de sensibilidade é viável. Mostrar a sobreposição entre críticos e conectados como próximo passo. Admitir que o mapa é de "potencial local". Tratar a unidade do mapa com cuidado.
- **Gravidade:** importante.

### A19. C anual em modelo de evento, e valores vindos de outros lugares?
- **Pergunta:** "O fator C da USLE é uma média anual ponderada pela erosividade. Você o usa igual em janeiro e em julho. Hao usou C do mês do evento. Por que a silvicultura tem C de 0,121, mais que o dobro do campo, com valor do Rio Grande do Sul? Se eu inverter esses dois valores, quantos pixels críticos sobram?"
- **Local:** Tabelas 5 e 6 (p. 26 e 27), seção 4.2 (p. 48), seção 4.5 (p. 54 e 55), Conclusões (p. 61). Sobre Hao, nota do lote A (C por NDVI do mês do evento).
- **Por que importa:** a lista de áreas críticas é em grande parte um reflexo das classes (lavoura mais silvicultura sobre Cambissolo são boa parte dos pixels críticos), e o texto não traz sensibilidade a K e C, só a ressalva "sob os valores adotados". Baert destaca a proteção da cultura como controle de evento, como o próprio texto cita na seção 2.1. Teste não recalculado.
- **Boa resposta:** apresentar faixas de C e K da literatura. Rodar os críticos com os limites da faixa e reportar o que é robusto. Explicar o que "campo" representa no mapa do Plano. Dizer que variação sazonal foi ignorada e como NDVI resolveria isso.
- **Gravidade:** importante.

### A20. Quanto o MC erra na soma?
- **Pergunta:** "Somando sua Tabela 12, o MC no ajuste dá cerca de 37 mil toneladas contra 23,8 mil medidas. Isso é +56%. Por que esse número não aparece no texto, se a sua introdução fala de vida útil de reservatórios, que depende do total?"
- **Local:** Tabela 12 (p. 47), seção 3.4.5 (p. 35 e 36), seção 1.1 (p. 10). Conta minha: MC 37.294 t (+56%); MFM 22.964 t (-4%).
- **Por que importa:** a calibração em log é defensável, mas prioriza erro relativo e pode deixar viés no total. O texto apresenta o viés de volume de +3%, mas não o de sedimento. O contraste é um alerta: quase sem viés no volume total e +56% no sedimento total, porque E cresce com Q^1,12 e os eventos grandes são superestimados.
- **Boa resposta:** reportar o viés total nos modelos. Explicar por que escala log e o que ela sacrifica. Dizer para que uso o modelo não serve.
- **Gravidade:** importante.

### A21. Qual é a sua referência nula? E a linguagem estatística?
- **Pergunta:** "Quanto acerta um modelo que prevê sempre a mesma carga? Sem esse número, 82% dentro de fator 2 é bom ou é fácil? E 'não se explica pelo acaso', com p = 0,02 e 17 eventos, em uma comparação escolhida depois de ver os dados, é uma frase que você sustenta?"
- **Local:** Tabela 13 (p. 49), seção 4.3 (p. 49 e 50), seção 3.4.7 (p. 37 e 38), Conclusões (p. 60).
- **Por que importa:** a amplitude de carga é de cerca de 19 vezes, e um fator 2 é um critério folgado (cobre uma faixa de 4 vezes). Sem referência nula, as métricas não têm escala. O limite inferior do intervalo (+3,1 pontos) é pouco acima de zero, e várias comparações foram feitas.
- **Conta minha (leave-one-out, Tabela 12):** prever sempre a mesma carga (média geométrica dos outros 16) dá erro mediano de 38,5%, 70,6% dentro de fator 2 (12 de 17) e NSE log de -0,13. O erro mediano da constante é menor que o da regra da chuva (41,9%), que ganha em fator 2 (82%) e em NSE log (0,53); no teste pareado, regra da chuva e constante não se distinguem (p = 0,22). O MC (81%; 35%) é pior que a constante. O MFM e a regra com Vdir ganham da constante (p = 0,03 e 0,005).
- **Boa resposta:** incluir o modelo constante na Tabela 13, com leave-one-out. Mostrar o ganho em relação a ele. Relatar as comparações feitas e trocar a frase por "o intervalo e o teste indicam diferença, com n = 17".
- **Gravidade:** importante.

### A22. A área urbana gera água, mas não gera sedimento?
- **Pergunta:** "Os 14% urbanos têm os maiores CN, entram no seu volume, e têm erosão zero por K = 0 e C = 0. No modelo, essa água some sem erodir nada. Na realidade, ela desce e encontra margens, ruas e canais. E, se K e C urbanos fossem outros, quanto o c mudaria?"
- **Local:** seção 3.3 (p. 27 e 28), seção 4.1 (p. 45), seção 4.5 (p. 56), Tabelas 5 e 6.
- **Por que importa:** o texto reconhece a simplificação, mas não aponta que o volume urbano entra no ajuste do CN e no MFM. Como Q é proporcional ao fator f em todos os pixels, a água que a mancha urbana gera conta no volume sem contar na erosão. K = 0 é uma marcação de ausência de dado, e não uma propriedade do solo.
- **Boa resposta:** quantificar a parcela do volume gerada em pixels urbanos. Rodar sensibilidade com C urbano pequeno, diferente de zero. Relacionar isso com o evento 17 e a hipótese de obra.
- **Gravidade:** importante.

### A23. LS médio de 7,80 e As limitada a 200 m: de onde veio isso?
- **Pergunta:** "Por que 200 m e não 100 m? Esse limite equivale a uns 7 pixels de área a montante. E 65% da sua bacia está acima de 20% de declividade: a fórmula de LS que você usa foi pensada para esses declives?"
- **Local:** seção 3.4.1.2 (p. 31), Tabela 4 (p. 26), Tabela 16 (p. 55). Sete pixels é conta minha (200 m * 30 m / 897 m²).
- **Por que importa:** o texto dá o motivo para existir um limite, mas não para o valor, e não traz sensibilidade. De memória, não conferido: há um limite de validade da forma de potência do escoamento em torno de 100 m de comprimento e 14 graus, atribuído a Moore e Wilson; precisa ser verificado antes de ser usado. A nota do lote B também registra dúvida sobre os expoentes serem de Moore e Burch (1986) ou de Moore e Wilson (1992), sem conferência no original.
- **Boa resposta:** conferir a origem dos expoentes e a faixa de validade. Testar limites de 100 e 400 m. Dizer se os pixels de canal foram excluídos ou só limitados.
- **Gravidade:** importante, sobretudo pela citação.

### A24. Um pixel de 30 m sobre mapa 1:250.000 tem resolução de 30 m?
- **Pergunta:** "Seu CN vem de solos 1:250.000 e uso de 2022. K e C vêm do Plano de 2020. Os eventos são de 2018 a 2020. Em que escala o seu mapa de áreas críticas pode ser lido de fato? Eu posso ir a campo com ele e procurar um pixel?"
- **Local:** seção 3.3 (p. 25 e 28), seção 3.4.1.1 (p. 29 e 30), seção 4.6 (p. 57 e 58). Apêndice A cita um pixel específico.
- **Por que importa:** a grade não é a resolução da informação. Os 5% críticos são uma regra arbitrária, sem análise de sensibilidade ao limite. Parte do mapa é uma classe grosseira sobre um relevo fino.
- **Boa resposta:** dizer que a leitura vale por manchas e por classes, e não por pixel. Dar uma ideia de escala mínima. Testar 1%, 5% e 10%. Agregar por sub-bacia.
- **Gravidade:** detalhe, com peso na aplicação.

### A25. A bacia é natural? Barramentos, captação e esgoto.
- **Pergunta:** "É uma bacia antropizada, com 14% urbanos e uma estação de tratamento na seção. Há barramentos, açudes, captações ou lançamentos de esgoto a montante? Como isso entra na vazão de base, na turbidez e na retenção de sedimento?"
- **Local:** seção 3.1 (p. 22), seção 3.2 (p. 23): o texto não trata desses itens.
- **Por que importa:** açude retém sedimento e amortece picos. Lançamento e captação alteram a vazão de base e a turbidez. O texto só descreve uso e geologia. Não afirmo que existam, é pergunta a ser verificada, e o aluno deve saber responder.
- **Boa resposta:** apresentar o levantamento (outorgas, imagens, Plano de Bacias). Dizer se há influência no período. Se não souber, dizer que não verificou.
- **Gravidade:** detalhe, ou importante se houver barramentos.

## (d) As 5 perguntas mais difíceis

1. **A1:** exige que o aluno refaça, em voz alta, a frase principal do próprio resumo.
2. **A2:** o teste do embaralhamento mostra que a validação nada diz sobre o mapa, e o título promete o mapa.
3. **A6:** o viés de seleção é sutil, e o aluno provavelmente nunca o considerou.
4. **A7:** o c maior que 1 com as unidades de Williams desmonta a leitura como conectividade.
5. **A4:** obriga a separar método de configuração, o que muda o tom das conclusões sobre o SCS-CN.

## (e) O que eu elogiaria

- Comparar o modelo com regras simples que usam a mesma informação, e relatar que ele perde. Poucos trabalhos de MUSLE fazem isso.
- A separação entre MC (previsão) e MFM (referência), com a ressalva de que o MFM não é previsão.
- A seção 4.3 admitir que o bom desempenho do MFM vem do volume e "não é uma validação da fórmula de erosão nem do mapa".
- Declarar que a escolha de CN-I e λ foi feita olhando os mesmos eventos, e citar a literatura de viés de seleção.
- O uso de métricas robustas e a justificativa para calibrar em log.
- O Apêndice A, que permite refazer o cálculo à mão. Conferi o pixel de exemplo (Q de 13,0 mm e E_unit próximo de 1,17) e bate, dentro do arredondamento.
- Manter o evento 17 e mostrar os resultados com e sem ele.
- A seção 4.6, que organiza as incertezas em ordem na cadeia do modelo.

## Falta fazer

Atualizado na retomada na nuvem (04/11, tarde).

**Feito na retomada:**
- Contas incorporadas às perguntas A4, A6, A14, A17 e A21 (scripts `Scripts/banca_04-11/calc1.py`, rodado de novo na nuvem com os mesmos resultados).
- Conferido na planilha: CSS máxima e ausência de falhas nos eventos (A12), evento 17 hora a hora (A13), vazão no início das janelas (A15), BFImax = 0,25 (A8).
- Figuras 7 e 8 vistas a 200 dpi.

**Continua em aberto:**
- Faixa de turbidez (NTU) da curva: a planilha só tem CSS. Depende do orientador (curva e amostras de Murillo-Bermúdez et al., 2023).
- Demais figuras (1 a 6, 9 a 11, A1 e A2) não abertas por este avaliador; foram vistas pelo revisor do texto e pelo Avaliador B.
- Conferir nos originais o que vem só das notas (Hao, Baert) ou da memória (limite de validade de LS, A23).
- Páginas citadas: tiradas do texto marcado por página (numeração do PDF), sem conferência uma a uma.
- Não recalculado (depende dos rasters): embaralhamento de K, C e LS (A2), mapa com chuva uniforme (A10), sensibilidade de C e K (A19), parcela do volume gerada em pixels urbanos (A22), limites de 100 e 400 m (A23), 1%, 5% e 10% (A24).
