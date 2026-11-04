# Respostas às perguntas da banca e perguntas frequentes

Para estudar antes da defesa. Versão do texto: `TCC_Texto/TCC_versao_04-11.pdf`. Feito na nuvem em 04/11/2026, a partir de `1_revisao_texto.md`, `2_avaliador_A.md` e `3_avaliador_B.md`.

## Como usar este arquivo

As perguntas A e B se repetem muito. Por isso estão agrupadas por tema; cada tema diz quais perguntas responde (por exemplo, "A1, B4"). No fim há uma tabela com todas as 50 perguntas e o tema de cada uma.

Cada tema tem:
- **Resposta falada:** o que dizer, em poucas frases. Escrita em primeira pessoa, para você treinar em voz alta.
- **Evidência:** onde está o apoio (seção, tabela, arquivo ou conta).
- **Classificação:**
  - **sustentada:** o trabalho ou as contas já feitas dão a resposta.
  - **parcial:** há parte da resposta; o resto é limitação que você deve admitir.
  - **depende do orientador:** só o Luis (ou quem gerou os dados) sabe; não invente, diga que vai confirmar.
- **Se apertarem:** o que admitir e o que propor.

Regras para a defesa:
1. Não diga um número que não está no texto ou nas notas. Se não souber, diga "não calculei isso" e o que faria para calcular.
2. "Não recalculado" quer dizer que a conta depende dos rasters (.tif), que não estavam na nuvem. São contas para rodar no PC antes da banca, se der tempo.
3. Concordar com uma crítica justa conta a seu favor. O trabalho já é honesto; a defesa deve continuar assim.

## Parte 1. Três frases que vão ser atacadas (mudar antes da banca, se possível)

| Frase do texto | Onde | Problema | Troca sugerida |
|---|---|---|---|
| "O limite está, portanto, na conversão da chuva em escoamento." | Resumo | O volume medido está dos dois lados da comparação (tema 1). | "Os resultados indicam que o escoamento é a maior fonte de erro; como a carga medida também depende do volume, o ganho com o volume medido não valida a fórmula de erosão." |
| "A comparação demonstra que a espacialização não se mostrou pior" | Conclusões, p. 60 | A seção 4.3 diz que a comparação é só indicativa, e a IC tem outra lista de eventos (tema 9). | "A comparação é só indicativa: com o escoamento medido, a espacialização chega a um erro da mesma ordem da formulação concentrada." |
| "A diferença não se explica pelo acaso" | Seção 4.3, p. 49; Conclusões | Com 17 eventos escolhidos e p = 0,02, é forte demais (tema 10). | "Dificilmente se explica pelo acaso, com a ressalva de que são 17 eventos." |

Se o texto não puder mais ser mudado, abra a defesa dizendo você mesmo essas três ressalvas. Isso tira a força das perguntas A1, A5, B4 e B5.

## Parte 2. Respostas por tema

### Tema 1. O modelo forçado prova que o gargalo é o escoamento? (A1, B4)

**Resposta falada:** "Não prova sozinho, e eu concordo que a frase do resumo ficou forte. A carga medida é vazão vezes concentração, então quando eu dou ao modelo o volume medido, uma parte do ganho é aritmética. O argumento mais limpo é outro: a regra simples proporcional à chuva usa a mesma chuva que o MC e ganha dele em 14 de 17 eventos. Isso mostra que a passagem da chuva pelo SCS-CN, nesta configuração, piora a estimativa. O MFM mostra que o volume é necessário; não mostra que basta. Os 91% da variância explicada e os 88% da carga explicada pelo volume são o mesmo fato visto de lados diferentes, e não três provas."

**Evidência:**
- Seção 4.3 (p. 49 e 50): o próprio texto faz a ressalva "por construção".
- Tabela 13: MC 81% e 35%; regra da chuva 42% e 82%; teste pareado p = 0,02, 14 de 17 eventos. Em erro logarítmico o resultado é mais forte: p = 0,009 (conta do Avaliador B, refeita na nuvem com `Scripts/banca_04-11/calc1.py`).
- Regra com o volume direto: 15,9% e 94%, sem diferença do MFM (p = 0,52).

**Classificação:** parcial. A parte "o MC perde para a chuva" é sustentada; "o limite está no escoamento" é só indicada.

**Se apertarem:** proponha o teste sem autocorrelação que o Avaliador A sugeriu: prever a carga por volume (concentração média do evento) em vez da carga. Não foi feito.

### Tema 2. O teste no exutório diz alguma coisa sobre o mapa? Para que espacializar? (A2, B1, B2)

**Resposta falada:** "Não diz quase nada sobre o mapa, e o texto reconhece isso. K, C e LS são iguais em todos os eventos, então entram só na escala, que o coeficiente c absorve. O que muda de um evento para outro é a chuva, o volume e a intensidade. A validação no exutório é temporal, não espacial. O mapa é uma hipótese de onde a erosão se concentra, condicionada aos valores de K, C e CN adotados. Espacializar não serve, aqui, para prever melhor a carga; serve para gerar hipóteses de localização, que precisam ser verificadas em campo."

**Evidência:**
- Seção 4.2 (p. 47): os fatores são os mesmos em todos os eventos.
- Seção 4.3: "não é uma validação da fórmula de erosão nem do mapa".
- Conta do Avaliador B: uma fórmula sem pixel, ln[Vdir^1,12 * (RI/R)^0,56], reproduz o MFM com R² de 0,99 em log. Em validação cruzada, 22,3% de erro contra 20,6% do MFM.

**Classificação:** parcial. A limitação é admitida no texto; a demonstração (embaralhar K, C e LS) não foi feita: não recalculado.

**Se apertarem sobre "o que eu perderia usando só K * LS * C":** responda com honestidade. Pelas notas do PC (`resultados_analise_mapa_pc_02-11.md`), o R² linear entre o mapa e K * LS * C é 0,58 (MC) e 0,56 (MFM). Então o mapa é em boa parte K * LS * C, e a diferença vem da chuva e do CN, que são as entradas menos confiáveis. A sobreposição dos 5% críticos com o top 5% de K * LS * C não foi calculada (não recalculado). Diga que é a primeira conta que faria.

### Tema 3. O que o trabalho pode concluir? Os objetivos foram cumpridos? Qual a contribuição? (A5, B24)

**Resposta falada:** "O modelo não serve para prever a carga de um evento a partir só da chuva: o MC erra 81% e perde até para uma carga constante no erro mediano. A contribuição é um diagnóstico: comparei a MUSLE espacializada com referências simples que usam a mesma informação e mostrei onde o erro nasce. O objetivo de identificar áreas críticas foi cumprido em parte: o mapa existe e é estável entre as duas versões, mas não foi validado no espaço. O mapa indica onde verificar em campo antes de indicar onde investir."

**Evidência:**
- Tabela 13 e Conclusões.
- Notas: as áreas críticas coincidem 94% entre MC e MFM (texto, seção 4.5) e 95% e 91% entre as duas configurações testadas (`resumo_modelo_completo.md`, citado pelo Avaliador B em B3).
- Modelo constante: 38,5% de erro mediano (conta na nuvem).

**Classificação:** sustentada, desde que você não diga "demonstra" nem "validado".

**Se apertarem:** diga objetivo por objetivo. Objetivo 1 (montar o modelo): cumprido. Objetivo 2 (avaliar o escoamento): cumprido. Objetivo 3 (validar o modelo distribuído): só no exutório, que não valida o mapa. Objetivo geral (áreas críticas): sugeridas, não validadas.

### Tema 4. A escolha da configuração olhou para a carga? (A11, B3)

**Resposta falada:** "Escolhi CN-I e λ = 0,05 pelo volume, não pela carga. Mas a banca tem razão: como o volume explica 88% da carga, escolher pelo volume é em boa parte escolher pela carga. Essa atenuante da seção 3.4.6 é fraca, e eu retiraria. Testei poucas configurações (condição de umidade, λ e a conversão de Woodward), e a escolha foi feita olhando para os mesmos 17 eventos. Por isso o desempenho reportado é otimista. A validação aninhada seria o teste certo e não foi feita."

**Evidência:**
- Seção 3.4.6 (p. 36 e 37) contra seção 4.3 (p. 49).
- `resumo_modelo_completo.md`, seção 3: a configuração anterior dava MC 97,9% e MFM 38,7%; a atual, 81,1% e 20,6%.
- A favor: as áreas críticas coincidem 95% (MC) e 91% (MFM) entre as duas configurações (notas).

**Classificação:** parcial.

**Se apertarem sobre os 18 pontos entre 38,7% e 20,6% no MFM (B3):** não há explicação escrita nas notas consultadas. Diga que a mudança de configuração muda a distribuição do volume entre os eventos (o fator f muda), e por isso o MFM também muda, mas que não analisou a diferença em detalhe. Não invente outra causa.

### Tema 5. CN-I, λ = 0,05 e Woodward: física ou ajuste? (A3, A16, B16)

**Resposta falada:** "É ajuste. O CN-I não representa a umidade antes de cada evento; é uma condição única escolhida porque fazia o volume total bater, e o texto diz isso na seção 3.4.1.3. O evento 16, que começa 13 horas depois de 139 mm, mostra bem: fisicamente o solo estava úmido. Eu testei aplicar a umidade evento a evento e ficou muito pior: os eventos em condição úmida davam de 1,75 a 6,6 vezes o volume medido. Isso sugere que o problema está na estrutura do método nesta bacia, não só no valor do CN. No pixel do Apêndice, quase toda a mudança vem do CN-I, e não do λ."

**Evidência:**
- Seção 3.4.1.3 (p. 31 e 32).
- `resumo_modelo_completo.md`, passo 2: pelo critério do NEH-4, 13 dos 17 eventos cairiam em condição seca; o teste por evento foi rejeitado (viés de +85%). Essa informação não está no TCC.
- Conta do Avaliador A no pixel do Apêndice: com CN-I e λ = 0,20, Q seria cerca de 11,7 mm; com a conversão, 13,0 mm.
- Viés do volume: -12% com λ = 0,20 e +3% com a conversão (`resumo_modelo_completo.md`, passo 3).

**Classificação:** sustentada (desde que você chame de ajuste).

**Se apertarem sobre Brandão (clima úmido associado a λ maior):** concorde. O λ = 0,05 não foi provado nesta bacia; foi uma escolha que melhorou o volume total. Baert, citado no texto, teve NSE negativo com a mesma conversão.

### Tema 6. A falha é do SCS-CN ou da sua configuração? O SCS-CN distribui bem o volume entre os pixels? (A4, B8)

**Resposta falada:** "Só testei uma configuração no texto, então devo dizer 'nesta configuração'. Com uma retenção média de 490 mm e chuva média de 63 mm, a bacia fica na parte da curva em que o volume cresce com o quadrado da chuva. Nos dados, o volume calculado cresce com a chuva elevada a 2,6, e o medido, com a chuva elevada a cerca de 1,2. Um CN maior deixaria a curva mais reta, mas erraria o total. Quanto à distribuição entre pixels: não verifiquei. O padrão espacial do MFM é herdado do SCS-CN."

**Evidência:**
- Conta na nuvem (Tabelas 2 e 3, em log): inclinação de V_SCS contra R = 2,58 (R² 0,99); de Vdir contra R = 1,17 (R² 0,57).
- Coeficiente de escoamento sem relação com a chuva: correlação de -0,01 (seção 4.1).
- `teste_cn_calibrado.md`: formas calibradas viram quase um coeficiente de escoamento constante e não superaram a regressão simples com a chuva (versão anterior do modelo; não está no TCC).
- A favor: pixels com CN-I abaixo de 35 respondem por 0,1% da erosão (`resultados_analise_mapa_pc_02-11.md`).

**Classificação:** parcial.

**Se apertarem sobre os blocos de CN com limite reto na Figura 3 (B8):** diga que eles vêm dos polígonos dos mapas de solo e de uso, que são de escala grosseira (1:250.000). A origem exata de cada bloco não foi conferida no raster (não recalculado).

### Tema 7. Vazão de base e BFImax: de onde vem o seu "escoamento direto medido"? (A8, B17)

**Resposta falada:** "O escoamento direto não é medido; é estimado a partir da vazão medida, com o filtro de Eckhardt. A série que recebi se reproduz com a = 0,995 e BFImax = 0,70. O cabeçalho do arquivo diz 0,58, e isso ainda preciso confirmar com o orientador. A escolha pesa: com 0,58, o viés do volume calculado seria cerca de -11%; com 0,70, +3%; com 0,80, +21%; com 0,25, valor sugerido para aquífero em rocha dura, -36%. Então o +3% não é propriedade da bacia; depende da separação. O MFM, por outro lado, é estável à separação, porque o coeficiente c absorve um fator parecido entre os eventos."

**Evidência:**
- Seção 3.2 e seção 4.6.
- Conta na nuvem com a planilha: BFImax 0,70 dá soma de Vdir de 15.225 mil m³ (a coluna Bt dá 15.263, igual à Tabela 3); 0,25 dá 24.571 mil m³ (85% do volume total) e viés de V_SCS de -36%.
- `relatorio_checagens_base_alvo_woodward_27-10.md`: frações e estabilidade do MFM (erro de 15% a 22%).
- `perguntas_para_o_luis_30-10.md`, item 2.

**Classificação:** depende do orientador (qual BFImax e por quê); a sensibilidade é sustentada pelas contas.

**Se apertarem sobre "superficial":** concorde. O filtro não sabe se a água veio pela superfície; o certo é "escoamento direto" ou "escoamento rápido", que inclui fluxo subsuperficial raso.

### Tema 8. Como os 17 eventos foram escolhidos? E 24/11/2018? (A6, B10)

**Resposta falada:** "Os eventos vêm da lista de trabalhos anteriores do grupo, com pico de pelo menos 10 m³/s, delimitados à mão sobre o hidrograma. O critério precisa estar escrito na seção 3.2, e não está. O evento de 24/11/2018 existe na planilha, com pico de 12,48 m³/s, e estava na lista de partida como '1B'; ele saiu da lista do TCC. O motivo eu preciso confirmar com o orientador. Concordo que selecionar pela resposta da bacia pode distorcer a relação entre coeficiente de escoamento e chuva: uma chuva pequena só entra se respondeu muito. Isso pode explicar parte da subestimação dos eventos pequenos."

**Evidência:**
- Seção 2.5 (p. 17 e 18): critério de 10 m³/s, citado só como trabalho anterior.
- `Dados Iniciais/eventos_processados_manuais.xlsx`: "1B", de 24/11/2018 16h a 26/11/2018 21h, pico de 12,484 m³/s, volume de 1.391 mil m³.
- Conta do Avaliador B (planilha): entre 22/11/2018 e 22/02/2020, os 17 eventos têm 11,4% das horas, 32,3% do volume e 64,5% da carga. Há quatro picos acima de 10 m³/s depois do período (09/12/2020 a 07/03/2021), não usados.
- `perguntas_para_o_luis_30-10.md`, itens 3 e 6.

**Classificação:** depende do orientador (critério e motivo da troca).

**Se apertarem:** proponha testar as regras com volume nos quatro eventos de 2020 e 2021 como teste independente. Atenção: nesses quatro, o DBT5 marca 0,0 mm nas 48 h anteriores, então o teste do MC ficaria fraco.

### Tema 9. A comparação com a IC é justa? (B5; também C3 da revisão do texto)

**Resposta falada:** "É só lado a lado, não é pareada. A lista de eventos da IC não é igual à minha: tem 24/11/2018 no lugar de 17/12/2018, e as cargas medidas diferem em vários eventos. Por exemplo, em 20/02/2020 a IC usa 1.456 t e eu uso 1.710 t; os 37% de erro da IC no evento 17 são contra a carga dela. Contra 1.710 t, seriam 46%. A IC tem dois parâmetros ajustados nos próprios eventos, sem validação cruzada. Refeita em validação cruzada com as minhas tabelas, ela dá 16,3%, e não se distingue do MFM (p = 0,58). Por isso 'demonstra' é forte demais; o certo é 'não permite distinguir'. Decidi apresentar só os valores originais da IC para não misturar o meu trabalho com uma refação dela."

**Evidência:**
- `Scripts/_ic_original.py` (listas e cargas da IC).
- Figura 8 (p. 47): no painel da IC, o evento 12 aparece com carga medida de cerca de 130 t; nos outros painéis, 211 t. Ou seja, o eixo do painel da IC usa as cargas da IC (visto a 200 dpi na nuvem).
- Conta do Avaliador B: a * (TR * qp)^b em validação cruzada, 16,3%, 100% em fator 2; diferença para o MFM +6,2 pontos, p = 0,58.
- `perguntas_para_o_luis_30-10.md`, item 14 (decisão de usar só os valores originais).

**Classificação:** parcial (os fatos estão claros; o texto precisa declará-los).

**Se apertarem sobre a decisão de não mostrar a IC refeita:** defenda como escolha de escopo, mas admita que, com a IC refeita, a vantagem visual do MFM some.

### Tema 10. Qual é a referência nula? O p = 0,02 e o Wilcoxon (A21, B9, B12)

**Resposta falada:** "Não incluí no texto o modelo que prevê sempre a mesma carga, e deveria. Calculei depois: ele dá 38,5% de erro mediano e 71% dentro de fator 2. Isso mostra que o fator 2 é um critério folgado aqui, porque as cargas variam só cerca de 19 vezes. O MC é pior que a constante. A regra da chuva ganha da constante em fator 2 e em NSE log, mas não se distingue dela em teste pareado. O MFM e a regra do volume ganham da constante. O Wilcoxon foi aplicado às diferenças de erro percentual, pareado por evento; o método precisa estar na seção 3.4.7. Com 17 eventos escolhidos, o p = 0,02 é indicativo, não prova."

**Evidência:**
- Conta na nuvem (`calc1.py`, leave-one-out): constante 38,5%; 70,6%; NSE log -0,13. Regra da chuva contra constante: p = 0,22. MFM contra constante: p = 0,03. Regra do volume contra constante: p = 0,005.
- MC contra regra da chuva: +32,6 pontos, intervalo +3,1 a +117,5, p = 0,02; em erro log, p = 0,009.
- Intervalos de confiança do fator 2 (Clopper-Pearson): 6 de 17, de 14% a 62%; 14 de 17, de 57% a 96%; 16 de 17, de 71% a 100%.
- Script do Wilcoxon: `Scripts/revisao_29-10/r2_estatistica.py`, com semente fixa.

**Classificação:** parcial (as contas existem; o texto não as tem, e o método do Wilcoxon não está escrito).

**Se perguntarem por que o texto traz +1,6 e o avaliador achou +1,4:** é arredondamento. A conta com as tabelas impressas (arredondadas) dá +1,4; o texto usou os valores sem arredondar.

### Tema 11. Os eventos são independentes? Há tendência no tempo? (A14, B11)

**Resposta falada:** "Não são totalmente independentes, e há tendência: o MFM superestima os primeiros eventos e subestima os últimos. O erro do MFM tem correlação de -0,68 com a ordem dos eventos. Calibrando nos eventos 1 a 11 e prevendo 12 a 17, o MFM erra 16,9%, com o simulado em média abaixo do medido; no sentido inverso, 37,7%. A carga por volume parece subir de 1.455 para 1.685 mg/L, mas com tão poucos eventos essa diferença entre grupos não é distinguível. O leave-one-out com um único parâmetro é uma verificação fraca, e eu digo isso."

**Evidência:** conta na nuvem (`calc1.py`): Spearman -0,68 (p = 0,002); divisão temporal como acima; teste entre grupos p = 0,30 (t) e 0,18 (Mann-Whitney). Seção 4.3 (p. 51) descreve a tendência sem testá-la. Seção 4.2: o próprio texto diz que o coeficiente muda pouco entre rodadas.

**Classificação:** parcial.

**Se perguntarem a causa:** não sabemos. As candidatas são sensor ou curva de turbidez, mudança na bacia (obras, uso) ou início da estação chuvosa. A troca ou manutenção do turbidímetro só o orientador ou a SABESP podem confirmar (depende do orientador).

### Tema 12. Quanto o MC erra na soma? (A20, B13)

**Resposta falada:** "Na soma dos 17 eventos, o MC dá cerca de 37 mil toneladas contra 23,8 mil medidas, ou +56% no ajuste e +63% em validação cruzada. O MFM erra -4%. Isso acontece porque calibrei em log, o que dá o mesmo peso a erros relativos, e porque a erosão cresce com o volume elevado a 1,12, enquanto os eventos grandes são superestimados pelo SCS-CN. Para estimar massa total, por exemplo para assoreamento de reservatório, o MC não serve. Eu deveria ter reportado esse número e o NSE linear."

**Evidência:** soma da Tabela 12: MC 37.294 t; MFM 22.964 t; medido 23.846 t. NSE linear: MC -4,35 (ajuste) e -5,43 (validação cruzada); MFM 0,78 (conta na nuvem). No MC, o evento 15 pesa 27,8% da soma.

**Classificação:** sustentada (os números estão nas tabelas; só não estão escritos).

### Tema 13. O que é o coeficiente c? (A7, B18)

**Resposta falada:** "c é um coeficiente de escala empírico, sem sentido físico isolado. Ele absorve a unidade (o volume está em outra unidade que a de Williams), o tamanho do pixel, a compensação do erro do escoamento e, talvez, a entrega de sedimento. Por isso muda de 0,0344 no MC para 0,0222 no MFM: a diferença compensa o escoamento. Não pode ser usado em outra bacia nem em outra grade. Retiraria a palavra 'conectividade'. Pelo mesmo motivo, o valor em kg por pixel do mapa não é erosão bruta: a soma do mapa bate com a carga no exutório por construção. O mapa deve ser lido como índice relativo."

**Evidência:** seções 3.4.3 e 3.4.4 (p. 33 a 35); o texto já diz que c não deve ser lido como razão de entrega. Conta do Avaliador A: com volume em m³, c seria cerca de 1,65 e 1,06. Nota do lote A: a fórmula impressa em Hao não tem o /1000.

**Classificação:** sustentada (se você chamar de coeficiente de escala).

### Tema 14. O que sobra da fórmula de Williams? O que é pr? Por que RI/R? (A17, B15)

**Resposta falada:** "Depois que c absorve a escala, sobram o expoente 1,12 e o padrão no espaço. O pico local pr é proporcional a Q no pixel, então não traz informação espacial nova; entre eventos, ele só multiplica pelo termo de intensidade. Mantive 11,8 e 0,56 e o termo RI/R para seguir Hao, não porque melhoram: sem o RI/R, a regra com o volume elevado a 1,12 erra 17,3%; com ele, 22,3%. A correlação entre a carga por volume e RI/R é fraca (0,28). O RI vem do posto mais intenso e o R de uma média, por isso RI/R passa de 1 em dois eventos."

**Evidência:** seções 2.6 e 3.4.3; conta na nuvem (`calc1.py`); `perguntas_para_o_luis_30-10.md`, item 7 (origem do RI, a confirmar). Expoente carga contra volume observado: 0,94.

**Classificação:** sustentada (a parte da origem do RI depende do orientador).

### Tema 15. Toda a carga vem da encosta? E a histerese? (A9)

**Resposta falada:** "O modelo supõe que sim, e isso é uma simplificação. Tiro a vazão de base do volume, mas a carga medida inclui o que a base transporta e o que vem do canal e das margens. A parcela da base é incerta: nas minhas checagens, ela vai de cerca de 7% a 34% da carga, conforme a concentração que se supõe para a base. A ordem dos modelos não mudou com o alvo só do escoamento direto. A parcela do canal não foi estimada. Não relacionei o tipo de laço de histerese aos resíduos; seria um próximo passo."

**Evidência:** seção 3.4.4 (p. 35); `relatorio_checagens_base_alvo_woodward_27-10.md`, conclusão 4 (34% e 6,8%). Planilha (conta na nuvem): o pico de concentração vem antes do pico de vazão em 12 dos 17 eventos.

**Classificação:** parcial.

### Tema 16. Dois postos: o gradiente de chuva é real? (A10, B7; também I2 da revisão do texto)

**Resposta falada:** "As duas frases não falam da mesma coisa. A seção 3.1 fala da média anual do Plano, na escala da sub-bacia inteira. As seções 4.1 e 4.4 falam dos dois postos nos 17 eventos, em que o DBT5, a leste, registra em média 44 mm e Campo Limpo, 72 mm. Mas eu deveria ter explicado a diferença no texto. Não fiz curva de dupla massa nem comparei com outra fonte de chuva. A diferença entre os postos é grande em alguns meses e às vezes se inverte, então ela precisa ser verificada. Como o gradiente entra direto no mapa, a falta de chuva na cabeceira pode ser em parte efeito do posto."

**Evidência:**
- Tabela 2; seção 3.1 (p. 21); seções 4.1 e 4.4.
- Conta do Avaliador B (planilha): dentro dos eventos, DBT5/Campo Limpo = 0,62; fora deles, 0,89. Em abril de 2020, 184 mm contra 1 mm, com vazão máxima de 1,5 m³/s, o que combina mais com 1 mm.
- R é reproduzida por 0,307 * DBT5 + 0,693 * Campo Limpo, pesos ajustados aos 17 eventos (`tabelas/tab_parametros.md`); a origem da coluna é pergunta 5 ao orientador.

**Classificação:** parcial (a origem de R depende do orientador).

**Se perguntarem sobre o zero do DBT5 no evento 12:** não sei se é chuva zero ou falha; não verifiquei.

**Proposta:** rodar o mapa com chuva uniforme e ver quantos pixels críticos permanecem (não recalculado).

### Tema 17. Qual é o erro da carga "medida"? (A12, B23)

**Resposta falada:** "A carga vem da turbidez convertida em concentração por uma curva de calibração, e o texto não dá a incerteza dela. Preciso confirmar com o orientador qual curva foi usada (a de potência de 2022 ou a por partes de 2023) e a faixa das amostras. Se a curva for a de potência, quase 90% da carga do período está em horas com concentração acima do equivalente a 250 NTU, o trecho mais incerto. Por isso eu deveria chamar o dado de 'carga estimada' e não comparar modelos com diferenças de poucos pontos."

**Evidência:**
- `perguntas_para_o_luis_30-10.md`, itens 4 e 16.
- Conta do Avaliador B, condicional à curva de potência: 17,7% das horas e 89,1% da carga acima de cerca de 267 mg/L.
- Planilha (conta na nuvem): a planilha só tem a concentração, não a turbidez. Maior concentração da série: 4.844 mg/L (março de 2021); nos eventos, 4.602 (evento 12) e 4.227 mg/L (evento 17). Nenhuma hora sem dado nos 17 eventos.

**Classificação:** depende do orientador.

**Se apertarem:** não diga um valor de incerteza. Diga que a incerteza não foi estimada e que, sem ela, diferenças de 2 a 5 pontos entre modelos não são interpretáveis (o próprio texto diz isso).

### Tema 18. O que aconteceu no evento 17? (A13)

**Resposta falada:** "Não sei com certeza. A carga por volume direto é 3.806 mg/L, cerca de 2,5 vezes a média dos outros eventos; essa não é uma concentração física, é carga total dividida pelo volume direto. Olhando hora a hora, a concentração sobe para 4.227 mg/L uma hora antes de a vazão começar a subir e fica num patamar de cerca de 3.700 a 4.200 mg/L por seis horas. Isso pode ser sedimento de uma fonte perto do ponto de coleta, como área urbana, obra ou margem, ou um problema de horário ou do sensor. Nenhuma das duas hipóteses foi testada. Mantive o evento e mostrei os resultados com e sem ele."

**Evidência:**
- Planilha, 20/02/2020: chuva entre 16h e 18h (DBT5 18,8 + 43,0 + 2,0 mm; Campo Limpo 7,0 + 34,8 + 18,4 mm); concentração de 705 mg/L às 18h e 4.227 mg/L às 19h, com vazão de 2,0 m³/s; vazão de 4,6 às 20h e pico de 21,4 m³/s às 21h.
- Nos outros eventos, o pico de concentração também costuma vir antes do de vazão (12 de 17); o que é único no evento 17 é o patamar alto.
- Sem o evento 17, o MFM tem 15,3% e 100% (seção 4.3).

**Classificação:** parcial.

**Se apertarem:** proponha procurar registros de obra ou deslizamento em fevereiro de 2020 e confirmar a sincronia dos relógios das duas séries.

### Tema 19. Eventos de seis dias são um problema para o SCS-CN? (A15)

**Resposta falada:** "É uma hipótese razoável, mas os dados não a apoiam muito. A razão entre o volume calculado e o medido tem correlação de 0,79 com a chuva e só 0,37 com a duração. Então a chuva explica o erro bem melhor que o tamanho da janela. Duas janelas, as dos eventos 5 e 10, começam na recessão do evento anterior, o que pode inflar o volume medido nelas. Não rodei o SCS-CN por pulso de chuva."

**Evidência:** conta na nuvem (`calc1.py`): 0,79 e 0,37. Planilha: no evento 10 a vazão inicial está 1,2 m³/s acima da base e é 35% do pico; no evento 5, 2,0 m³/s acima da base; nos outros, até 0,9 m³/s.

**Classificação:** sustentada (para a parte "a duração não é a causa principal"); parcial para o resto.

### Tema 20. Por que tirar a conectividade de Hao? E a deposição? (A18)

**Resposta falada:** "Com 17 eventos, calibrar um termo de conectividade seria arriscado, e eu preferi deixar um único coeficiente. Mas calcular o índice de conectividade sem calibrar, só para ver quanto o mapa muda, seria viável e não fiz. Sem conectividade, o mapa é de potencial local de erosão: um pixel no topo do morro, longe do rio, vale tanto quanto um na margem. O modelo também não leva escoamento de um pixel para o de baixo nem deposição. Isso está na seção 4.6."

**Evidência:** seções 2.6, 3.4.4, 4.5 e 4.6. Hao: conectividade abaixo de 0,5 em cerca de 80% da área (nota do lote A).

**Classificação:** parcial.

### Tema 21. K e C: de onde vêm? A Tabela 14 é só a Tabela 6? (A19, B6, B14)

**Resposta falada:** "Os valores de K e C vêm das tabelas usadas na IC, e eu não consegui confirmar todos nas obras citadas. Pelas minhas notas, o C de 0,05 do campo não aparece como fator C em Silva et al. (2016), o C de 0,212 é o da soja, o de 0,121 é o do eucalipto jovem, e o K de 0,0475 é de uma amostra. A origem está perguntada ao orientador. A banca tem razão em que a ordem das classes na Tabela 14 segue a ordem do C: a correlação entre erosão por área e C é quase 1. Então o resultado por classe é consequência das hipóteses, e não uma descoberta do modelo. O C também é anual, sem variação de estação."

**Evidência:**
- `leitura_referencias/loteD_fontes_K_C.md`; `perguntas_para_o_luis_30-10.md`, item 17.
- Conta do Avaliador B: correlação 0,985 entre ln(erosão por área) e ln C; só com área * C, campo, silvicultura e lavoura já dão 77%, contra 83% no modelo.

**Classificação:** depende do orientador (fontes); parcial para o resto.

**Se apertarem:** corrigir a coluna "Fonte" das Tabelas 5 e 6 e rodar o mapa com os valores alternativos do lote D (não recalculado).

### Tema 22. A área urbana gera água, mas não gera sedimento? (A22)

**Resposta falada:** "No modelo, sim: a área urbana tem K e C iguais a zero, então gera volume e nenhuma erosão. É uma simplificação: na realidade, a água urbana desce e pode erodir margens e canais, e há sedimento de ruas e obras. K = 0 marca ausência de dado, não uma propriedade do solo. Não calculei a parcela do volume gerada em pixels urbanos nem testei um C urbano pequeno."

**Evidência:** seção 3.3 (p. 27 e 28); seção 4.5. Área urbana de 14,1% (seção 3.1).

**Classificação:** parcial. As contas pedidas: não recalculado.

### Tema 23. Fator LS e limite de 200 m (A23, B19)

**Resposta falada:** "O limite existe porque a fórmula da USLE não vale no canal, onde a área a montante fica enorme. O valor de 200 m foi uma escolha; não testei 100 ou 300 m. Com pixel de 30 m, ele equivale a cerca de 7 pixels a montante. Os pixels de canal ficaram no mapa, só limitados. Sobre os expoentes 0,4 e 1,3: a atribuição a Moore e Burch (1986) precisa ser conferida no original; uma fonte secundária os atribui a Moore e Wilson (1992)."

**Evidência:** seção 3.4.1.2; nota do lote B (só resumo lido). A faixa de validade da fórmula foi citada pelos avaliadores de memória, sem conferência: não use número nenhum sobre ela na defesa.

**Classificação:** parcial.

### Tema 24. Escala e resolução: pixel de 30 m sobre mapa de 1:250.000? (A24, B20)

**Resposta falada:** "A grade de 30 m não é a resolução da informação. O solo vem de um mapa de 1:250.000, e o uso, de 2022, enquanto os eventos são de 2018 a 2020. O mapa deve ser lido por manchas e por classes, e não pixel a pixel. Os 5% críticos são um limite escolhido; não testei 1% ou 10%. A soma de E_unit depende do tamanho do pixel, e não testei outra resolução."

**Evidência:** seções 3.3 e 3.4.1.1; Tabela 4; seção 3.4.3 (efeito n^0,12).

**Classificação:** parcial.

### Tema 25. Barramentos, captações e esgoto (A25)

**Resposta falada:** "Não verifiquei. O texto descreve uso e geologia, mas não açudes, captações nem lançamentos a montante. Isso afetaria a vazão de base, a turbidez e a retenção de sedimento. Seria preciso levantar outorgas e imagens."

**Classificação:** depende do orientador (ou de levantamento que não foi feito). Não afirme que existem nem que não existem.

### Tema 26. A partição do R² do mapa (B21)

**Resposta falada:** "A partição é uma descrição do mapa, não uma validação, e vale por construção: o E_unit é o produto exato de K * LS * C e do termo de escoamento. Em log, o escoamento fica com cerca de 63% e os fatores fixos com 37%. Em escala linear, o R² do mapa com K * LS * C é 0,58. Para priorizar os 5% de cima, o que importa é a cauda, e não calculei a partição na cauda. Além disso, CN e C vêm ambos do uso do solo, então os dois termos não são independentes."

**Evidência:** seção 3.4.9; `resultados_analise_mapa_pc_02-11.md`, item 1.

**Classificação:** sustentada (como descrição).

### Tema 27. Uso prático: o comitê tem verba para 500 ha; onde investir? (B22)

**Resposta falada:** "O mapa serve como triagem para vistoria, e não para decidir investimento direto. Os pixels críticos estão sobretudo em lavoura temporária e silvicultura sobre Cambissolos, com declividade de 20% a 45%. Não calculei que fração da erosão está nos 5% críticos nem que redução de carga uma prática daria na captação. O mapa também é a média de 17 eventos, não erosão anual; no MC, o evento 15 sozinho pesa 28% do total. O próximo passo barato seria verificar as manchas críticas em imagens de alta resolução e em campo."

**Evidência:** `resultados_analise_mapa_pc_02-11.md`, item 2; conta na nuvem (peso dos eventos: MC 27,8% e MFM 14,9% para o evento 15). 5% são 7.693 pixels, cerca de 6,9 km² (conta do Avaliador B).

**Classificação:** parcial.

**Sobre "não pôde ser validado":** diga "não foi validado". Uma verificação qualitativa (imagens, campo) era possível e não foi feita.

### Tema 28. Reprodutibilidade (B25)

**Resposta falada:** "O código e os dados estão num repositório no GitHub, com scripts em Python. Ainda não estão prontos para outra pessoa rodar: vários scripts têm caminhos fixos do meu computador, e os rasters estão no meu Drive. O Wilcoxon e o bootstrap estão no script de estatística, com semente fixa. A vazão de base, a chuva por evento e os fatores K e C foram recebidos prontos e reconstruídos por mim depois; quem os gerou foi o grupo de pesquisa."

**Evidência:** `README.md`; `Scripts/revisao_29-10/r2_estatistica.py`.

**Classificação:** parcial. Confirme antes da banca se o repositório é público ou privado: a busca da nuvem mostrou `mateusvivarelli/TCC` como público, enquanto o `README.md`, segundo o Avaliador B, diz privado.

### Pontos menores do Avaliador B

- **0,8189 contra 0,8187 (seção 2.3):** a conta dá 0,8187; o modelo usa a forma certa. Sustentada; corrigir o número.
- **Afloramento rochoso com C = 1:** "Foi tratado como solo exposto por falta de outra classe; rocha não erode como solo. A área é pequena." Parcial.
- **Duas estimativas de chuva (R por pesos e P_k por IDW):** "R serve para o volume total e as regras simples; P_k, para o mapa. A diferença entre as duas não foi tabelada; no evento 11, é de 0,5 mm (74,0 contra 73,5)." Parcial; origem de R depende do orientador.
- **Três áreas (137,8; 138,1; 139,3 km²):** diga de onde vem cada uma (área do polígono, pixels de cálculo, outra base). Se não souber, diga que vai uniformizar. Depende de conferência.
- **Figura 9 sem barras de incerteza:** concorde; os intervalos do bootstrap existem para as diferenças.

## Parte 3. Outras perguntas frequentes

**P1. Por que a MUSLE, e não a USLE ou um modelo físico?**
"A USLE é anual e usa a erosividade da chuva; a MUSLE troca a erosividade pelo escoamento do evento, o que serve para eventos. Um modelo físico exigiria dados de solo e de canal que não temos. Segui Hao et al., que espacializaram a MUSLE por pixel." Sustentada (seções 2.1 e 2.6).

**P2. O que é validação cruzada leave-one-out, e por que usar?**
"Calibro o coeficiente com 16 eventos e prevejo o 17º; repito para cada evento. Assim, cada previsão é feita sem ver aquele evento. Com um só parâmetro, ela muda pouco o resultado, por isso é uma verificação fraca." Sustentada (seção 3.4.6).

**P3. Por que calibrar em log?**
"Porque as cargas variam cerca de 19 vezes, e em escala linear os eventos grandes dominariam. Em log, um erro de duas vezes pesa igual para cima e para baixo. O custo é que o total não fica preservado: o MC erra +56% na soma." Sustentada (seção 3.4.5; tema 12).

**P4. O que é "dentro de fator 2"?**
"O simulado está entre a metade e o dobro do medido. Aqui o critério é folgado: prever sempre a mesma carga já acerta 12 de 17." Sustentada (tema 10).

**P5. Por que o erro mediano, e não o médio?**
"Com 17 eventos, um evento ruim puxa a média. A mediana é mais estável." Sustentada (seção 3.4.7). Se perguntarem sobre a assimetria do erro percentual, ver tema 10.

**P6. O que é o MFM, se não é previsão?**
"É o mesmo modelo com o escoamento direto forçado ao valor estimado do hidrograma medido. Serve de teto: mostra quanto o modelo melhoraria se o escoamento fosse perfeito." Sustentada (seção 3.4.8).

**P7. O que é o SCS-CN, em uma frase?**
"Um método que calcula quanto da chuva vira escoamento a partir de um número de curva, que depende do solo, do uso e da umidade antes do evento." Sustentada (seção 2.3).

**P8. O que é o filtro de Eckhardt?**
"Um filtro que separa a vazão medida em vazão de base e escoamento direto, com dois parâmetros: a constante de recessão (a) e o máximo índice de vazão de base (BFImax)." Sustentada (seção 3.2); o valor de BFImax, ver tema 7.

**P9. O que é histerese?**
"Para a mesma vazão, a concentração é diferente na subida e na descida da cheia. Isso mostra que a carga não é função fixa da vazão instantânea. Para o evento inteiro, porém, a carga se relaciona bem com o volume." Sustentada (seção 2.5); ver tema 1.

**P10. Por que só 17 eventos?**
Ver tema 8. Depende do orientador quanto ao critério.

**P11. O que você faria com mais seis meses?**
Em ordem, sem prometer resultado:
1. Teste de embaralhar K, C e LS e mapa com chuva uniforme (temas 2 e 16).
2. Validação aninhada da configuração (tema 4).
3. Teste nos quatro eventos de 2020 e 2021 (tema 8).
4. Índice de conectividade como sensibilidade (tema 20).
5. Verificação das manchas críticas em imagens e em campo (tema 27).
6. Estimar a incerteza da curva de turbidez (tema 17).

**P12. Seu trabalho é um resultado negativo. Isso tem valor?**
"Tem. Mostra que, nesta bacia e com estes dados, a MUSLE espacializada com SCS-CN não supera regras simples, e onde o erro aparece. Isso evita que alguém use o mapa como se fosse validado. Comparar com regras simples que usam a mesma informação é pouco comum em trabalhos com a MUSLE." Sustentada (os dois avaliadores elogiam isso).

**P13. Qual foi a sua parte e o que veio pronto?**
Diga com clareza: a série de vazão, concentração e vazão de base, as chuvas dos postos, a lista de eventos e as tabelas de K e C vieram do grupo (trabalhos anteriores e a IC). O modelo espacializado, a calibração, a validação cruzada, as comparações e os mapas são seus. Confirme os detalhes com o orientador. Depende do orientador quanto ao que exatamente foi recebido.

**P14. Por que λ = 0,05?**
Ver tema 5. "Porque a literatura indica valores menores que 0,20 para muitas bacias e porque melhorou o volume total aqui. Não foi provado nesta bacia."

**P15. Os mapas mostram erosão ou sedimento?**
"Erosão local, como índice relativo. A soma bate com a carga no exutório por construção do c. As figuras que dizem 'sedimento' deveriam dizer 'erosão local'." Sustentada (tema 13; I4 da revisão do texto).

## Parte 4. Tabela de todas as perguntas

| Pergunta | Tema | Classificação |
|---|---|---|
| A1 | 1 | parcial |
| A2 | 2 | parcial |
| A3 | 5 | sustentada |
| A4 | 6 | parcial |
| A5 | 3 | sustentada |
| A6 | 8 | depende do orientador |
| A7 | 13 | sustentada |
| A8 | 7 | depende do orientador |
| A9 | 15 | parcial |
| A10 | 16 | parcial |
| A11 | 4 | parcial |
| A12 | 17 | depende do orientador |
| A13 | 18 | parcial |
| A14 | 11 | parcial |
| A15 | 19 | sustentada |
| A16 | 5 | sustentada |
| A17 | 14 | sustentada |
| A18 | 20 | parcial |
| A19 | 21 | depende do orientador |
| A20 | 12 | sustentada |
| A21 | 10 | parcial |
| A22 | 22 | parcial |
| A23 | 23 | parcial |
| A24 | 24 | parcial |
| A25 | 25 | depende do orientador |
| B1 | 2 | parcial |
| B2 | 2 | parcial |
| B3 | 4 | parcial |
| B4 | 1 | parcial |
| B5 | 9 | parcial |
| B6 | 21 | depende do orientador |
| B7 | 16 | parcial |
| B8 | 6 | parcial |
| B9 | 10 | parcial |
| B10 | 8 | depende do orientador |
| B11 | 11 | parcial |
| B12 | 10 | parcial |
| B13 | 12 | sustentada |
| B14 | 21 | parcial |
| B15 | 14 | sustentada |
| B16 | 5 | sustentada |
| B17 | 7 | depende do orientador |
| B18 | 13 | sustentada |
| B19 | 23 | parcial |
| B20 | 24 | parcial |
| B21 | 26 | sustentada |
| B22 | 27 | parcial |
| B23 | 17 | depende do orientador |
| B24 | 3 | sustentada |
| B25 | 28 | parcial |

Contagem: 13 sustentadas, 28 parciais e 9 que dependem do orientador.

## Parte 5. O que levar ao orientador antes da banca

São as respostas que só ele pode dar (já estão em `perguntas_para_o_luis_30-10.md`):
1. BFImax: 0,58 ou 0,70, e por quê (item 2; tema 7).
2. Por que 24/11/2018 saiu e 17/12/2018 entrou (item 3; temas 8 e 9).
3. Qual curva turbidez-concentração e qual a faixa das amostras (itens 4 e 16; tema 17).
4. Origem da chuva R por evento e do RI (itens 5 e 7; temas 14 e 16).
5. Critério escrito de delimitação dos eventos (item 6; tema 8).
6. Fonte de K e C (item 17; tema 21).
7. Novo: houve troca ou manutenção do turbidímetro entre 2019 e 2020? (tema 11). Há açudes ou captações a montante? (tema 25).

## Parte 6. Contas para rodar no PC, se der tempo (dependem dos rasters)

Em ordem de utilidade para a defesa:
1. Sobreposição dos 5% críticos com o top 5% de K * LS * C, e fração da erosão nos 5% críticos (temas 2 e 27).
2. Mapa com chuva uniforme: quantos pixels críticos permanecem (tema 16).
3. Embaralhar K, C e LS e recalibrar c: quanto muda o erro no exutório (tema 2).
4. Mapa com os valores alternativos de K e C do lote D (tema 21).
5. Limites de 100 e 300 m para As; 1% e 10% como corte de críticos (temas 23 e 24).
6. Parcela do volume gerada em pixels urbanos (tema 22).
