# Avaliador B: arguição do TCC (versão de 04/11/2026)

Papel: pesquisador de modelagem ambiental, geoprocessamento e estatística aplicada, cético quanto a modelos calibrados com poucos dados e atento à utilidade para a gestão da bacia.

**Estado:** as 25 perguntas estão prontas e as contas sobre tabelas e planilha foram feitas. O que ficou em aberto está na seção "Falta fazer", no fim.

## (a) O que foi lido e conferido

**TCC:** texto inteiro, p. 1 a 68 do PDF, em `Notas Claude/doc_texto_pdf_paginas_04-11.txt`. A primeira leitura foi feita só com o TCC. Todas as figuras (1 a 11, A1 e A2) foram vistas em 95 dpi, e o painel de CN da Figura 3 também em 220 dpi. As páginas citadas abaixo são as impressas no rodapé ou no topo do texto; o Resumo está na p. 7 do PDF.

**Não li**, como pedido: `1_revisao_texto.md`, `2_avaliador_A.md`, `revisao_processo_29-10.md`, `revisao_independente_03-11.md`.

**Notas consultadas depois da primeira leitura:**
- `resultados_analise_mapa_pc_02-11.md`
- `perguntas_para_o_luis_30-10.md`
- `relatorio_checagens_base_alvo_woodward_27-10.md` (até a seção c2)
- `resumo_modelo_completo.md` (trechos)
- `teste_cn_calibrado.md` (início)
- `leitura_referencias/`, lotes A, B, C e D (trechos)
- `alteracoes_doc_03-11.md` (só um trecho)
- `README.md` (início)
- `Scripts/revisao_29-10/r2_estatistica.py` (início) e busca em `Scripts/`

**Contas minhas:** feitas em Python, com scripts fora do repositório. Usam as Tabelas 2, 3, 11 e 12 (valores arredondados) e a planilha `Dados Iniciais/Dados_finais_histereses_corrigido.xlsx`. Ao longo do texto vêm marcadas como "(conta minha)". A soma de carga das 17 janelas na planilha deu 23.846 t, igual à do TCC. O MedAPE, o fator 2, o NSE log e o Spearman da Tabela 13 também foram reproduzidos, com diferença máxima de 0,1 ponto no erro mediano da regra da chuva (41,8 contra 41,9).

**Não recalculado:** nada que dependa dos rasters, que não estão no repositório. A literatura vem das notas de leitura do repositório, salvo onde digo "de memória, não conferido".

## (b) Impressão geral (parecer curto)

O trabalho é honesto, e isso é o seu maior mérito: mostra que o modelo calculado perde para uma regra proporcional à chuva e escreve que o MFM não valida a fórmula nem o mapa. As contas principais se reproduzem a partir das tabelas.

A fragilidade está no que sobra depois dessa honestidade. O título promete "identificação de áreas críticas", mas o único teste disponível, no exutório, praticamente não enxerga o espaço: uma fórmula de duas grandezas por evento, sem nenhum pixel e sem K, LS e C, reproduz o resultado do MFM com R² de 0,99 em log (B1). O mapa é, em boa parte, o produto de tabelas de K e C com fontes não confirmadas, de um gradiente entre dois postos que divergem muito entre si e de um mapa de CN com limites abruptos. O texto admite isso, mas não mede a sensibilidade do mapa a nenhuma dessas entradas.

Três frases vão além do que foi demonstrado:
- "A comparação demonstra que a espacialização não se mostrou pior";
- "não se explica pelo acaso";
- "O limite está, portanto, na conversão da chuva em escoamento".

A atenuante do viés de seleção na seção 3.4.6 é contrariada pela própria seção 4.3.

Eu aprovaria, com exigência de ajustes nesses pontos e de ao menos uma análise de sensibilidade do mapa. A resposta à pergunta "para que serve espacializar?" decide a qualidade da defesa.

## (c) Perguntas de banca

### B1. Um teste que não enxerga o mapa
**Pergunta:** "Se eu embaralhar K, LS e C entre os pixels e rodar de novo, o que acontece com o seu erro mediano? Fiz uma conta só com as suas tabelas: uma fórmula com volume medido e RI/R, sem pixel nenhum, reproduz o seu MFM quase exatamente. O que os 153.855 pixels acrescentam ao resultado no exutório?"
**Local:** seção 4.2, p. 47 ("Os fatores K, C e LS são os mesmos em todos os eventos"); seção 3.4.3, p. 32; seção 4.3, p. 49.
**Por que importa:** (conta minha) ln MFM contra ln[Vdir^1,12 * (RI/R)^0,56] tem R² = 0,9875, e o maior desvio é um fator de 1,27 (evento 1). Em LOO, essa fórmula dá 22,3% / 94% / NSE log 0,80 / Spearman 0,84, contra 20,6% / 94% / 0,84 / 0,83 do MFM. Para o MC, com V_SCS no lugar de Vdir, o R² é 0,9988. Isso mostra que o exutório quase não dá informação sobre K, LS e C, e que "validar no exutório" não diz nada sobre o mapa. O texto faz a ressalva, mas não a demonstra com um teste de placebo.
**Boa resposta:** explicar que os fatores fixos só entram na escala absorvida por c, que a validação é temporal e não espacial, e apresentar o teste de placebo (embaralhar os fatores; não recalculado aqui, depende dos rasters).
**Gravidade:** pode comprometer.

### B2. Para que serve espacializar
**Pergunta:** "Seu modelo espacial não supera uma regra de uma linha com o volume, e a chuva sozinha supera o modelo calculado. O mapa não tem validação. O que eu perderia se fizesse só o cruzamento de uso e declividade, ou o mapa de K * LS * C?"
**Local:** seção 4.3, p. 49 ("não melhora a estimativa do sedimento total"); Conclusões, p. 60; seção 4.5, p. 55.
**Por que importa:** é o argumento central. A única justificativa restante é "acrescenta o mapa", e o texto não compara esse mapa com nenhuma alternativa barata, nem informa a sobreposição entre os críticos e o top 5% de K * LS * C.
**Boa resposta:** dizer que espacializar não serve para prever a carga, e sim para gerar hipóteses de localização. Encarar o dilema: se a sobreposição com K * LS * C for alta, o modelo de evento acrescenta pouco; se for baixa, a diferença vem de chuva e CN, a parte que o próprio texto chama de menos confiável (p. 55).
**Gravidade:** pode comprometer.

### B3. Viés de seleção: a atenuante que o próprio texto derruba
**Pergunta:** "Na 3.4.6 o viés é reduzido porque as escolhas seguiram o volume, e não a carga. Na 4.3 o volume explica 88% da variância da carga. Como as duas frases convivem? Quantas configurações foram testadas, e o que se viu de sedimento antes de escolher?"
**Local:** seção 3.4.6, p. 36; seção 4.3, p. 49; seção 3.4.1.3, p. 31.
**Por que importa:** se carga e volume são quase a mesma informação, escolher pelo volume é em boa parte escolher pela carga. `resumo_modelo_completo.md` (seção 3) mostra as duas configurações comparadas também no sedimento (MC 97,9% contra 81,1%; MFM 38,7% contra 20,6%), e `Scripts/` tem vários testes de AMC, λ e CN. O TCC não mostra nenhuma alternativa. Os 18 pontos entre 38,7% e 20,6% surgem com o mesmo volume medido, enquanto o texto diz que 2 a 5 pontos não são interpretáveis; logo, o MFM não depende só do volume. A segunda atenuante do texto (mesma lista e mesma janela) não reduz viés de seleção.
**Boa resposta:** retirar ou reformular a atenuante, declarar o caminho percorrido numa tabela de sensibilidade, explicar os 18 pontos e fazer a validação aninhada ao menos para λ e AMC. A favor do aluno, e fora do texto: as áreas críticas coincidem 95% (MC) e 91% (MFM) entre as duas configurações, segundo as notas.
**Gravidade:** pode comprometer.

### B4. "O limite está na conversão da chuva em escoamento"
**Pergunta:** "Você troca a saída do modelo pelo volume medido no mesmo hidrograma em que mede a carga, e o acerto sobe. Isso é diagnóstico ou aritmética? E os 91% do erro do sedimento explicados pelo erro do escoamento: o que é física e o que é termo em comum?"
**Local:** Resumo, p. 7 ("O limite está, portanto..."); seção 3.4.8, p. 38 ("isola o efeito"); seção 4.2, p. 47; seção 4.3, p. 49; Conclusões, p. 59 e 60.
**Por que importa:** a 4.3 faz a ressalva da carga como volume vezes concentração, mas o Resumo mantém o "portanto" sem ela. Forçar o volume medido melhora qualquer modelo. MC e MFM também não diferem só no volume, porque c muda de 0,0344 para 0,0222. Os dois erros do 91% têm V_SCS e o volume medido em comum. Mostrar que o volume é necessário não mostra que basta: nas notas (`teste_cn_calibrado.md`, versão anterior do modelo), calibrar melhor o volume não melhorou o sedimento.
**Boa resposta:** distinguir necessário de suficiente, tratar o MFM como teto e o 91% como consistência, e ajustar o Resumo.
**Gravidade:** pode comprometer.

### B5. A comparação com a IC
**Pergunta:** "A IC tem 2 parâmetros ajustados nos próprios dados, usa volume total e pico. O MFM tem 1 parâmetro, validação cruzada e escoamento direto. Os 17 eventos são os mesmos? Refiz a IC em leave-one-out só com as suas Tabelas 2 e 3, em minutos, e deu 16,3%. Por que isso não está no texto? E como a comparação 'demonstra' que a espacialização não é pior?"
**Local:** seção 3.4.8, p. 38; Tabela 13 e Figura 9, p. 48; seção 4.3, p. 49 e 50 ("só indicativa"); Conclusões, p. 60 ("demonstra"); Resumo, p. 7.
**Por que importa:** (conta minha) a*(TR*qp)^b em LOO dá 16,3% / 100% / NSE log 0,87 / Spearman 0,93, igual ao registrado nas notas como "IC refeita". A diferença pareada para o MFM é +6,2 pontos, com intervalo de -8,6 a +8,0 e Wilcoxon p = 0,58: não se distinguem. Usar só o 22,5% original deixa o MFM visualmente empatado ou à frente, e as barras da Figura 9 reforçam isso. As notas registram que a lista da IC usa 24/11/2018 e a do TCC usa 17/12/2018, e que a carga difere (perguntas 3 e 14 ao orientador). "Não se mostrou pior" exigiria teste de equivalência e contradiz o "só indicativa" da 4.3. O uso só dos valores originais foi decisão registrada do aluno, e ele precisa saber defendê-la.
**Boa resposta:** declarar as diferenças de lista e de carga, mostrar também a forma da IC em validação cruzada e trocar "demonstra" por "não permite distinguir".
**Gravidade:** pode comprometer.

### B6. K e C sem fonte confirmada
**Pergunta:** "O campo ocupa 29% da bacia e responde por 37% da erosão. De onde vem o C = 0,050? Você leu isso na fonte que cita? O K de 0,0475, aplicado a 68,6% da bacia, representa a classe?"
**Local:** Tabelas 5 e 6, p. 25 e 26; seção 4.5, p. 53; Resumo, p. 7.
**Por que importa:** segundo `leitura_referencias/loteD_fontes_K_C.md`:
- Silva et al. (2016) não trata de pastagem, e 0,05 não aparece como fator C no artigo, mas a Tabela 6 ainda diz "com base em Silva et al. (2016)".
- C = 0,212 é o valor da soja; o mesmo artigo dá 0,1418 para cultura anual.
- C = 0,121 é o do eucalipto jovem; o plantio mais velho deu 0,016.
- K = 0,0475 é uma amostra; a média dos Cambissolos no artigo é 0,036.
- K = 0,0351 não foi conferido.
A pergunta 17 ao orientador segue aberta. Mudar as tabelas muda diretamente as Tabelas 14 e 15.
**Boa resposta:** dizer o que foi e o que não foi confirmado, corrigir a coluna "Fonte" e mostrar quanto o mapa muda com os valores alternativos do lote D (não recalculado).
**Gravidade:** pode comprometer.

### B7. A cabeceira recebe menos chuva? Os postos são confiáveis?
**Pergunta:** "Na 3.1 a cabeceira tende a ser a parte mais chuvosa. Na 4.1 e na 4.4 ela recebe menos chuva e por isso produz pouca erosão. Qual vale? Sua planilha mostra abril de 2020 com 184 mm em um posto e 1 mm no outro. Que controle de qualidade foi feito nesses postos?"
**Local:** seção 3.1, p. 21; seção 4.1, p. 44; seção 4.4, p. 51; seção 4.5, p. 55; Tabela 2, p. 23; Figuras 1 e 6, p. 22 e 44.
**Por que importa:** (conta minha, planilha) do primeiro ao último evento, DBT5 soma 1.741 mm e Campo Limpo 2.332 mm (razão 0,75). Dentro dos eventos a razão é 0,62; fora deles, 0,89. A diferença se concentra em poucos meses (jan/2019: 131 contra 282; fev/2019: 164 contra 316; jan/2020: 141 contra 268); em outros, os postos se aproximam ou se invertem. Depois do período estudado, os desacordos são enormes nos dois sentidos: abr/2020, 184 contra 1 mm, com vazão máxima de 1,5 m³/s, o que combina melhor com o posto de 1 mm; jan/2021, 32 contra 165 mm. Isso não prova erro nos 17 eventos, mas exige verificação. O gradiente entra direto no mapa, e a partição atribui 63% da variação ao termo que o contém. "Não registrou chuva" no evento 12 pode ser falha do posto.
**Boa resposta:** apresentar dupla massa e comparação com outra fonte de chuva, rodar o mapa com chuva uniforme e informar a coincidência dos pixels críticos (não recalculado).
**Gravidade:** pode comprometer.

### B8. SCS-CN errado na bacia, certo no pixel?
**Pergunta:** "O SCS-CN erra o volume da bacia em até 10 vezes, com f chegando a 9,75. Por que acreditar que ele acerta como o volume se distribui entre os pixels? E o bloco de CN baixo com limite abrupto na cabeceira, na Figura 3: é a bacia ou é um polígono de mapa?"
**Local:** seção 3.4.4, p. 34 ("apenas distribui no espaço"); Tabela 11, p. 41; seção 4.1, p. 44; Figura 3, p. 26; Figura A1, p. 67.
**Por que importa:** o padrão do MFM é herdado do SCS-CN. A Figura 3 mostra um bloco azul escuro no extremo leste, a partir de cerca de E 340, e um bloco alaranjado junto ao exutório, ambos de limites nítidos (observação visual; não conferi a origem no raster). São justamente os extremos de escoamento descritos na p. 44. Em chuvas pequenas, a abstração inicial pesa: S0,20 = 558 mm dá S0,05 de cerca de 1.180 mm e abstração de cerca de 59 mm (conta minha), contra R de 23 a 36 mm em seis eventos.
**Boa resposta:** admitir que o padrão não foi verificado, identificar a origem dos blocos, mostrar a fração de pixels com Q > 0 nos eventos pequenos e testar um padrão alternativo, como coeficiente de escoamento uniforme. A favor: pelas notas, pixels com CN-I abaixo de 35 respondem por só 0,1% da erosão.
**Gravidade:** pode comprometer.

### B9. E o modelo nulo?
**Pergunta:** "Você compara tudo com regras simples, mas qual é o desempenho de prever a mesma carga para todos os eventos? Sua regra da chuva tem erro mediano menor que esse?"
**Local:** seção 3.4.7, p. 36 e 37; seção 3.4.8, p. 38; Tabela 13, p. 48.
**Por que importa:** (conta minha, LOO) a constante dá 38,5% de erro mediano e 71% (12 de 17) em fator 2, com NSE log de -0,13. Portanto:
- em erro mediano e em fator 2, o MC (81% e 35%) é claramente pior que não modelar nada;
- a regra da chuva (41,8% e 82%) não se distingue da constante em teste pareado (diferença de -12,1 pontos, intervalo de -31,8 a +16,2, p = 0,22), embora ganhe em NSE log (0,53);
- o fator 2 discrimina pouco: as cargas variam só 19 vezes, e 12 de 17 já é a linha de base.
Intervalos de 95% do fator 2: 6/17 de 14 a 62%; 12/17 de 44 a 90%; 14/17 de 57 a 96%; 16/17 de 71 a 100%. (O Spearman da constante em LOO é um artefato e não deve ser lido.)
**Boa resposta:** incluir o modelo nulo na Tabela 13, dizer que a regra da chuva é referência, não modelo útil, e dar intervalos às métricas.
**Gravidade:** importante.

### B10. O que 17 eventos permitem concluir, e por que só estes
**Pergunta:** "Esses 17 são todos os eventos acima do critério? O pico de 12,48 m³/s de 24/11/2018 ficou fora, e é maior que os dos eventos 1, 9 e 10. Sua planilha vai até março de 2021, com mais quatro picos acima de 10 m³/s: por que não usá-los como teste independente? Que parte da carga do período está nos seus eventos?"
**Local:** seção 3.2, p. 22 e 23; seção 2.5, p. 17 (critério de 10 m³/s em 2022); seção 4.6, p. 56.
**Por que importa:** (conta minha, planilha) conferi o pico de 12,48 m³/s em 24/11/2018 às 23h, como apontado no LEIAME, cerca de 24 h depois do fim do evento 1. Entre 22/11/2018 e 22/02/2020, os eventos têm 11,4% das horas, 32,3% do volume e 64,5% da carga (23.846 de 36.976 t): um terço da carga fica fora. Picos fora das janelas, com Q e CSS válidos: 09/12/2020 (12,54), 14/01/2021 (18,56), 16/01/2021 (12,11) e 07/03/2021 (15,32). Ressalva: nesses quatro, DBT5 registra 0,0 mm nas 48 h anteriores, então o teste do MC ficaria fraco, mas o das regras com volume é viável. O TCC não dá critério escrito de seleção (pergunta 6 ao orientador). São 15 meses, 1 evento no período seco e pico máximo de 30,4 m³/s.
**Boa resposta:** dar o critério, explicar as exclusões, testar nos eventos novos e limitar as conclusões a cheias dessa faixa.
**Gravidade:** importante.

### B11. Eventos não independentes e teste temporal
**Pergunta:** "O evento 16 começa 13 horas depois do fim do 15. Seu leave-one-out os trata como independentes? Se os resíduos do MFM têm tendência no tempo, por que não calibrar no início e prever o fim?"
**Local:** Tabela 2, p. 23; seção 4.2, p. 45 ("a perda de desempenho do MC não vem da calibração"); seção 4.3, p. 50.
**Por que importa:** (conta minha) o resíduo em log do MFM tem correlação de -0,68 com a ordem do evento (-0,59 sem o evento 17), mais forte do que a descrição do texto sugere. Calibrando em 1 a 11 e prevendo 12 a 17, e o inverso:
| Modelo | 1-11 para 12-17 (erro mediano; razão mediana) | 12-17 para 1-11 (erro mediano; razão mediana) |
|---|---|---|
| MFM | 16,9%; 0,83 | 37,7%; 1,38 |
| Regra com Vdir | 27,2%; 0,79 | 31,3%; 1,31 |
| Regra com chuva | 23,3%; 1,06 | 47,5%; 0,74 |
| MC | 165,2%; 2,65 | 66,6%; 0,44 |
O c obtido dos totais da Tabela 12 muda bastante conforme o período, ao contrário do que o leave-one-out sugere. Os grupos são pequenos, de 6 e 11 eventos.
**Boa resposta:** reconhecer a dependência e a não estacionariedade, apresentar a divisão temporal e dizer que "validação" em leave-one-out com 1 parâmetro é fraca.
**Gravidade:** importante.

### B12. Bootstrap e Wilcoxon
**Pergunta:** "Onde o Wilcoxon está descrito nos métodos? Ele foi aplicado a diferenças de erro percentual, métrica que o seu próprio texto diz ser assimétrica. E o que quer dizer 'não se explica pelo acaso' quando os eventos não foram sorteados e a configuração foi escolhida olhando para eles?"
**Local:** seção 3.4.7, p. 36 e 37 (só o bootstrap é descrito; "Wilcoxon" só aparece na 4.3, p. 48 e 49, embora `alteracoes_doc_03-11.md` diga "Wilcoxon definido"); Conclusões, p. 59.
**Por que importa:** a seção 3.4.7 rejeita a média do APE pela assimetria (+100% contra -50% para o mesmo fator 2), mas a mediana do APE e o teste pareado continuam nessa escala, e a calibração é em log. O teste supõe eventos trocáveis e não leva em conta a seleção. Em favor do aluno (conta minha): reproduzi +32,6 [+3,1; +117,5] e p = 0,02, e em erro logarítmico o resultado fica mais forte (mediana +0,55, intervalo de +0,14 a +0,73, p = 0,009). Para MFM contra regra com Vdir, obtive +1,4 [-5,6; +10,4] e p = 0,52 (o texto traz +1,6 e -5,5; provável arredondamento das tabelas, a conferir). No MFM contra a constante, o Wilcoxon dá p = 0,027 e o intervalo inclui zero (-40,7 a +12,3), o que mostra a instabilidade do bootstrap de mediana com n = 17. Intervalos aproximados do Spearman: MC de 0,14 a 0,84; MFM de 0,57 a 0,94.
**Boa resposta:** definir o teste nos métodos, dizer qual é a população de referência, reportar também a escala log e escrever uma frase condicional à configuração e à amostra.
**Gravidade:** importante.

### B13. Viés de massa de 56%
**Pergunta:** "Você destaca +3% no volume. Qual é o viés do MC na carga total dos 17 eventos? E o NSE linear dele? Por que a Tabela 13 só traz a escala log, se o da IC você cita?"
**Local:** Tabela 12, p. 46; Tabela 13, p. 48; seção 3.4.5, p. 35; seção 4.3, p. 49 e 50.
**Por que importa:** (conta minha) no ajuste, o MC soma 37.294 t contra 23.846 t, ou +56% (+63% em LOO). O NSE linear é -4,35 no ajuste e -5,43 em LOO; o MFM soma -3,7% e tem NSE linear de 0,78. Quem cuida de captação ou de reservatório precisa da massa, e a calibração em log não a preserva. O NSE linear da IC (0,83) está no texto, e o do MC não.
**Boa resposta:** explicar o efeito da calibração em log e do expoente 1,12, reportar viés de massa e NSE linear de todos os modelos e justificar a escolha sem esconder o custo.
**Gravidade:** importante.

### B14. A Tabela 14 é a Tabela 6 disfarçada?
**Pergunta:** "A ordem das classes de uso em erosão por área é a ordem do C que você adotou. Esse resultado foi descoberto pelo modelo ou entrou pela tabela?"
**Local:** Tabela 6, p. 26; Tabela 14, p. 53; Conclusões, p. 60 ("46% da área", "83% da erosão").
**Por que importa:** (conta minha) nas seis classes com C e erosão positivos e dados completos, a correlação entre ln(erosão por área) e ln C é de 0,985. Usando só área vezes C, a parte de campo, silvicultura e lavoura já dá 77% (29,3 + 31,0 + 16,7), contra 83% no modelo. O principal resultado "por classe" vem em grande parte da entrada mais incerta (B6), e o mesmo vale para os 93% dos Cambissolos, que têm 68,6% da área.
**Boa resposta:** separar o efeito de C do efeito de LS e escoamento dentro de cada classe e apresentar o resultado como consequência das hipóteses.
**Gravidade:** importante.

### B15. O que resta da fórmula de Williams
**Pergunta:** "Se c absorve toda a escala, o 11,8 não tem efeito: por que a Tabela 9 diz 'mantido'? Se pr é proporcional a Q, o que o pico local acrescenta? O expoente efetivo é 1,12 e o observado é 0,94: por que não usar o observado?"
**Local:** seção 3.4.3, p. 32 e 33; Tabela 9, p. 35; seção 4.6, p. 57.
**Por que importa:** só c e o expoente têm efeito. (Conta minha) O termo RI/R não ajuda: Vdir^1,12 sozinho dá 17,3% / NSE log 0,82 / Spearman 0,90, e com (RI/R)^0,56 dá 22,3% / 0,80 / 0,84. Com a chuva, R^1,12 tem NSE log de 0,55 e, com RI/R, de 0,20, embora o erro mediano melhore de 44,9% para 37,6%. O ajuste de ln(carga) em ln(Vdir) dá expoente 0,935, próximo do 0,94 do texto. O RI vem do posto mais intenso, e o R, de uma média, o que faz RI/R passar de 1 nos eventos 1 e 12. Hao et al. calibraram em bacias de 1.310 a 8.973 km², com conectividade e vários postos, segundo a 2.6 do próprio TCC.
**Boa resposta:** dizer que, depois de c, a estrutura se reduz a expoente e padrão; que o RI/R foi mantido para seguir Hao, não porque melhora; e mostrar esse teste.
**Gravidade:** importante.

### B16. Sentido físico do CN-I e de S
**Pergunta:** "O evento 16 vem 13 horas depois de um evento de 139 mm: é solo seco? Uma retenção média de 490 mm, passando de 1 m, é física? O CN-I é condição de umidade ou parâmetro de ajuste?"
**Local:** seção 3.4.1.3, p. 30 e 31; Figura A1, p. 67; seção 4.1, p. 42.
**Por que importa:** o texto admite a escolha pelo volume. Notas registram um critério do NEH-4 (13 de 17 em AMC I) e o teste rejeitado de AMC por evento (viés de +85%); nenhum dos dois está no TCC. (Conta minha) a chuva de 5 dias em Campo Limpo passa de 53 mm nos eventos 4, 14 e 16, e o coeficiente de escoamento tem Spearman de +0,45 com essa chuva e também com a vazão inicial, o que é fraco, mas é sinal que o texto não explora. CN-I, λ = 0,05 e conversão de Woodward se empilham fora do contexto em que cada um foi obtido, e o +3% é compensação de erros.
**Boa resposta:** assumir o caráter de ajuste e levar ao texto o teste de umidade por evento.
**Gravidade:** importante.

### B17. O +3% depende da vazão de base
**Pergunta:** "Seu critério foi bater o volume direto, que depende de BFImax = 0,70. O texto diz que a sugestão para rocha dura é 0,25, e o cabeçalho do arquivo diz 0,58. Com outro BFImax, a escolha de CN-I e λ seria a mesma?"
**Local:** seção 3.2, p. 23; seção 4.6, p. 57; pergunta 2 ao orientador.
**Por que importa:** no relatório de checagens, a fração direta do volume vai de 0,384 a 0,612 conforme o cenário; com V_SCS fixo, o viés iria de cerca de -11% a +41% (conta minha). A escolha da configuração é condicional a essa série. A série é "fornecida" e foi reconstruída depois. O MFM é robusto à separação (15% a 22% nas notas), o que é bom para o aluno e não está no texto, mas 0,25 não foi testado. O alvo também mistura: carga total contra energia só do escoamento direto.
**Boa resposta:** trazer a sensibilidade, incluir 0,25, explicar a origem da série e dizer que o +3% não é propriedade da bacia.
**Gravidade:** importante.

### B18. Unidade e significado do mapa
**Pergunta:** "No Apêndice A, aquele pixel produz 40,1 kg. Mas c foi calibrado para a soma bater com o exutório. Isso é erosão local ou carga que chegou ao exutório? Se c é conectividade média, por que muda de 0,0344 para 0,0222?"
**Local:** Apêndice A, p. 65; seção 3.4.3, p. 33; seção 3.4.4, p. 33 e 34; seção 3.4.9, p. 39; Figuras 10, 11 e A2.
**Por que importa:** a soma do mapa é a carga no exutório por construção; a erosão bruta deveria ser maior. O texto chama o valor de erosão, as Figuras 10 e 11 de "sedimento" e a Figura A2 rotula E_unit como "kg por pixel, sem calibrar", enquanto a 3.4.3 diz que não é massa. A 3.4.4 diz que c "representa" conectividade e, em seguida, que não deve ser lido como razão de entrega.
**Boa resposta:** apresentar o mapa como índice relativo ou quantis, abandonar "kg por pixel" e tratar c só como fator de escala.
**Gravidade:** importante.

### B19. Limite de 200 m e fator LS
**Pergunta:** "Por que 200 m, e não 100 ou 300? Se a USLE não vale no canal, por que os pixels de canal continuam no mapa? Quantos pixels batem no limite? A fórmula vale nas suas declividades? Os expoentes são mesmo de Moore e Burch?"
**Local:** seção 3.4.1.2, p. 30; seção 4.5, p. 54; Tabela 16, p. 54.
**Por que importa:** com pixel de 30 m, As = 200 m equivale a cerca de 6.000 m², ou 6,7 pixels a montante (conta minha). O limite corta o valor, mas não remove o canal. Não há sensibilidade, embora Hoppen et al. (2019), citados na 2.2, indiquem que o método de LS importa. O lote B diz que os expoentes 0,4 e 1,3 não foram conferidos no original (só resumo lido) e que fonte secundária os atribui a Moore e Wilson (1992). De memória, não conferido: essa forma costuma ser restrita a encostas mais curtas e menos íngremes; 65% da área está acima de 20%.
**Boa resposta:** justificar o valor, informar a fração limitada, mostrar o mapa com 100 e 300 m, mascarar a drenagem e confirmar a citação.
**Gravidade:** importante.

### B20. Resolução, reamostragem, escala e defasagem
**Pergunta:** "Um mapa de solos 1:250.000 tem unidade mínima de que tamanho? O que significa um resultado por pixel de 30 m sobre isso? O que muda a 90 m? O MDE, o uso de 2020, o MapBiomas de 2022 e os eventos de 2018 a 2020 conversam entre si?"
**Local:** seção 3.3, p. 24 e 27; seção 3.4.1.1, p. 28 e 29; seção 3.4.3, p. 33 (n^0,12); Tabela 4, p. 25.
**Por que importa:** cada polígono de solo cobre muitos pixels, e a precisão visual é maior que a real. K tem na prática dois valores, com diferença de 35% (o texto diz "pouco acima"). CN e C saem de mapas de uso diferentes, com datas diferentes, e C é fixo o ano inteiro, apesar de lavoura temporária e de 16 eventos fora do inverno. O texto não nomeia o produto do MDE, o algoritmo de direção de fluxo nem a "correção". E_unit somado depende do tamanho do pixel, e nenhuma outra resolução foi testada.
**Boa resposta:** calcular a unidade mínima mapeável, agregar a uma escala defensável (mancha ou sub-bacia), testar 90 m e declarar as fontes completas.
**Gravidade:** importante.

### B21. Partição do R²
**Pergunta:** "Em log, o escoamento fica com 63%; em linear, K * LS * C tem R² de 0,58. Qual é a resposta para quem vai priorizar os 5% de cima? E essa partição separa causas, se CN e C vêm ambos do uso do solo?"
**Local:** seção 3.4.9, p. 39 e 40; seção 4.5, p. 54 e 55; Conclusões, p. 60.
**Por que importa:** a escala log dá o mesmo peso a pixels irrelevantes e aos críticos, mas a decisão está na cauda superior. Os dois termos não são independentes. O texto reconhece que a partição vale por construção, mas mesmo assim a leva às Conclusões, e o termo que ganha é justamente o que o texto chama de menos confiável. A conta (média dos ganhos) está certa: 37,1% e 62,9% saem de 45,5% e 71,2%.
**Boa resposta:** calcular a partição na cauda ou a sobreposição do top 5% e apresentar o resultado como descrição.
**Gravidade:** importante.

### B22. Uso prático do mapa
**Pergunta:** "Sou do comitê PCJ e tenho verba para 500 hectares. Seu mapa me diz onde? Que redução de carga eu teria na captação? Que fração da erosão está nos 5% críticos? Por que 5%? E 'não pôde ser validado': não pôde, ou não foi? Uma visita a campo ou imagens de alta resolução não dariam uma verificação parcial?"
**Local:** seção 3.4.9, p. 39; seção 4.5, p. 53 e 55; Figura 11, p. 52; Conclusões, p. 60.
**Por que importa:** os 5% são 7.693 pixels, cerca de 6,9 km² (conta minha), e o texto não diz que fração da erosão concentram. Sem conectividade, um pixel crítico longe da drenagem pode não afetar a carga. Não há cenário, custo nem incerteza. A média de 17 eventos não é erosão anual; no MC, o evento 15 pesa 27,8% do total (no MFM, 14,9%). A área urbana, nula por hipótese, fica fora. Verificar as manchas de solo exposto e mineração, como a do sul na Figura 11, é barato.
**Boa resposta:** dizer que o mapa é triagem para vistoria, informar a concentração da erosão, testar 5% e 10%, simular um cenário com P < 1, combinar com distância à drenagem e separar validação quantitativa de verificação qualitativa.
**Gravidade:** importante.

### B23. Qual é o erro da observação?
**Pergunta:** "Qual é o erro da sua carga 'medida'? Um erro de 16% a 21% está acima ou abaixo da incerteza da curva de turbidez? Qual curva foi usada? O evento 17 está fora da faixa de calibração, ou só acima da quebra de 250 NTU?"
**Local:** seção 2.5, p. 16 e 17; seção 4.3, p. 50; seção 4.6, p. 57.
**Por que importa:** o texto nunca dá faixa de incerteza, e quebra de trecho não é limite de calibração. As perguntas 4 e 16 ao orientador mostram que não está confirmada a curva (potência de 2022 ou por partes de 2023) nem a faixa das amostras. Se a lei de potência das notas for a usada (conta minha, condicional): 250 NTU equivalem a cerca de 267 mg/L; as horas acima disso são 17,7% do período e 89,1% da carga; acima de 1.000 mg/L, 3,8% e 46,5%; os 4.227 mg/L do evento 17 equivalem a cerca de 8.000 NTU. Quase toda a carga, portanto, está no trecho mais incerto. "3.806 mg/L" é carga total dividida por volume direto, não uma concentração. Testei a hipótese de lavagem depois de período seco para o evento 17: a associação com a chuva de 5 dias é fraca (Spearman -0,20), então não serve de apoio.
**Boa resposta:** dizer qual curva e qual faixa, estimar a incerteza da carga e não comparar modelos abaixo desse piso.
**Gravidade:** importante.

### B24. Contribuição original e objetivos
**Pergunta:** "Em uma frase, qual é a contribuição original deste trabalho? O objetivo 3 fala em validar o modelo: ele foi validado? O objetivo geral fala em identificar áreas críticas: foram identificadas, ou só sugeridas?"
**Local:** Objetivos, p. 11; seção 1.2, p. 10; Conclusões, p. 59 e 60; título.
**Por que importa:** o leave-one-out refaz um coeficiente, e o próprio texto diz que quase não muda o resultado (p. 45). O MC falha nas regras simples e o MFM não é previsão. O texto passa de "identificar" no título a "sugere" na conclusão, sem dizer que o objetivo foi cumprido em parte.
**Boa resposta:** formular com sobriedade: um diagnóstico comparativo com referências simples e um mapa relativo não validado. Dizer objetivo a objetivo o que foi cumprido e o que foi só em parte; e defender o valor do resultado negativo.
**Gravidade:** importante.

### B25. Reprodutibilidade
**Pergunta:** "Onde baixo o seu código e os seus dados? Em outro computador, roda? Qual script gera o Wilcoxon da Tabela 13? Quem produziu os rasters que você diz 'reproduzir'?"
**Local:** seção 3.4, p. 28; seção 3.4.1.2, p. 29; seção 3.4.1.4, p. 31; Tabela 1, p. 22.
**Por que importa:** o TCC não informa repositório nem disponibilidade de dados (a busca por "github" e "repositório" no texto não acha nada). Segundo `README.md`, o repositório é privado, os rasters ficam em Google Drive pessoal e os caminhos são fixos; 61 dos 64 scripts em `Scripts/*.py` têm caminho `C:`, e não há arquivo de dependências. O Wilcoxon está em `Scripts/revisao_29-10/r2_estatistica.py`, com semente fixa, o que é bom, mas ele lê um CSV de um caminho temporário (`/tmp/...`). As frases "reproduz o raster" e "reproduzida pelo filtro" indicam que entradas (K, C, chuva, base) foram reconstruídas depois, não produzidas no trabalho; falta dizer quem as produziu.
**Boa resposta:** indicar script principal, versões e o que é público, depositar tabelas e código, e explicar a origem de cada raster.
**Gravidade:** importante.

### Pontos menores (detalhe; não numerados)
- Coeficiente 0,8189 na seção 2.3: a conta dá 0,8187; o modelo não o usa (conta minha).
- Afloramento Rochoso recebe K = 0,0087 e C = 1, "como solo exposto": rocha não erode como solo.
- R (média com pesos 0,307 e 0,693) e P_k (IDW) são duas estimativas de chuva no mesmo modelo.
- Três áreas diferentes: 137,8, 138,1 e 139,3 km².
- Figura 9 sem barras de incerteza.

## (d) As 5 perguntas mais difíceis

1. **B1:** a fórmula sem pixel que reproduz o MFM com R² de 0,99.
2. **B2:** para que espacializar; o dilema não tem saída fácil.
3. **B3:** a atenuante da 3.4.6 contra os 88% da 4.3, e o caminho das configurações.
4. **B5:** a IC em validação cruzada dá 16,3% com as próprias tabelas do aluno, e o texto diz "demonstra".
5. **B7:** a contradição sobre a cabeceira e os desacordos entre os postos, porque atinge o termo que domina o mapa.

## (e) O que eu elogiaria

- A coragem de relatar que o MC perde para uma regra simples e de usar referências simples como critério (seção 3.4.8).
- A frase "não é uma validação da fórmula de erosão nem do mapa" (seção 4.3).
- A discussão de validação aninhada e a admissão de que não foi feita (seção 3.4.6).
- A calibração com um único coeficiente e solução direta, sem excesso de parâmetros.
- As métricas robustas e o teste de retirar os eventos 15 e 17.
- O Apêndice A, cujos passos II a V conferi à mão e bateram.
- A seção 4.6, organizada na ordem da cadeia de cálculo.
- A reprodutibilidade numérica das tabelas: refiz a Tabela 13 e os testes a partir delas.

### Conferências que favorecem o aluno
- MC pior que a regra da chuva é robusto: em erro logarítmico, p = 0,009.
- A associação do erro de volume com a duração da janela é fraca (r = 0,37, contra 0,79 com a chuva): a hipótese de que as janelas longas explicam o erro não se sustenta.
- CN-I abaixo de 35 pesa só 0,1% da erosão, e o MFM é robusto à separação da base (segundo as notas).
- A coincidência de 94% entre MC e MFM ocorre apesar dos pesos bem diferentes dos eventos.

## Falta fazer

**Já feito:** leitura do texto inteiro; todas as figuras vistas; contas sobre tabelas e planilha; as 25 perguntas, as 5 mais difíceis e os elogios.

**Ficou em aberto:**
1. Confirmar nos rasters a origem dos blocos de CN (B8) e tudo que está marcado "não recalculado": placebo, chuva uniforme, sobreposição com K * LS * C, fração da erosão nos 5% críticos, fração de pixels no limite de 200 m e valores alternativos de K e C.
2. Conferir no original a afirmação "de memória" da B19 e os expoentes de Moore e Burch (1986).
3. Conferir por que o texto traz +1,6 [-5,5; +10,4] para MFM contra Vdir e eu obtive +1,4 [-5,6; +10,4]; provável arredondamento das tabelas.
4. Não fiz validação aninhada; não testei os quatro eventos de 2020-2021 (só os localizei) e não li o resto do relatório de checagens depois da seção c2.
5. Os intervalos de Spearman da B12 são aproximados (transformação de Fisher com fator 1,06).
6. Revisão final de ortografia e de citações de página deste arquivo, que foi fechado às pressas porque o notebook ia ser desligado.
