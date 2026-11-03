# Revisão independente do TCC (texto de 03/11/2026)

Revisor: leitor externo, sem histórico do trabalho. Nada foi editado no Doc nem em outros arquivos; este é o único arquivo criado.

## (a) O que foi lido e o que não foi

Lido inteiro, em 5 blocos, linhas 1 a 977 de `C:\TCC\Notas Claude\doc_texto_completo_03-11.md`: capa e folha de rosto, Resumo, Abstract, capítulos 1 a 5, 5.1, Referências e Apêndice A.

Conferido contra fontes:
* `TCC_Texto\tabelas\tab_volumes.md`, `tab_mc_mfm_eventos.md`, `tab_resultados.md`, `tab_parametros.md`, `tab_qpico.md`, `tab_nse_linear.md`: Tabelas 3, 11, 12 e 9 batem com as fontes.
* `resultados_analise_mapa_pc_02-11.md`: Tabela 16, partição R2, limite Q<=P e CN-I<35 batem.
* `resumo_modelo_completo.md`, `Scripts\_ic_original.py` (valores originais da IC, recalculei as métricas à mão) e `proposta_cap4_30-10.md` (notas de conferência dos números de bootstrap, Wilcoxon, sensibilidade da base).
* Recalculei à mão: somas e médias das Tabelas 2, 3 e 11; durações da Tabela 2; R ponderado; erro percentual mediano e médio do volume (46% e 54%); "11 de 17 em fator 2"; contagem de superestimados/subestimados do MC; "14 de 17 pior que a regra da chuva"; sinal igual em 15 de 17; 0,5^1,12; somas das Tabelas 14 a 16; todo o exemplo numérico do Apêndice A (CN-I, S0,20, S0,05, Q, pr, E_unit, razão 1,55); K e C médios das Tabelas 5 e 6; carga por m3 de escoamento direto (evento 17 e faixa).

NÃO conferi (diga ao orientador que são "conforme notas do autor"):
* As figuras (não estão no texto) e as equações (aparecem como marcadores).
* Números que dependem dos rasters (áreas por classe, R2 do mapa, 94,2% de coincidência, 0,98 de correlação, 7.693 pixels, pixels com CN-I<35): só comparei com o arquivo de saída de 02/11.
* Bootstrap, Wilcoxon (p = 0,02 e 0,52), variâncias 0,66/0,08 e 88%, correlação -0,01 do coeficiente de escoamento com a chuva, correlação 0,96, sensibilidades da base (15,1 a 21,9%; 12,9%; 66%), "sem o evento 15/17": só encontrei registro nas notas do autor, não refiz.
* O conteúdo das obras citadas (Baert, Hao, Woodward, Brandão, Valle Junior, Avanzi, Hoppen, Reda, Azmeri, Sadeghi, Ochoa-Rodriguez, etc.): não li os originais.

---

## (b) Achados, por gravidade

### CRÍTICO

**C1. Resumo e Abstract não carregam a ressalva central do capítulo 4 (o MFM não valida a fórmula de erosão).**
* Local: Resumo, penúltima e última frases (e Abstract equivalente).
* Problema: o Resumo diz "Com o escoamento direto forçado ao valor medido, o acerto sobe a 94%... O limite está, portanto, na conversão da chuva em escoamento" e, em seguida, compara o MFM (21%) com a IC (22%) e diz que a espacialização "acrescenta um mapa". Falta dizer que, com o escoamento medido, a regra simples proporcional ao volume (16%; 94%) faz o mesmo que a MUSLE espacializada (seção 4.3: diferença +1,6 pontos, IC95% -5,5 a +10,4, p = 0,52) e que, portanto, o desempenho do MFM mostra o peso do volume medido e não valida a fórmula nem o mapa. Essa ressalva está bem tratada em 4.3 e na conclusão 4, mas o Resumo, que é a parte mais lida, deixa o leitor com a impressão de que o MFM valida o modelo. A frase "o limite está, portanto, na conversão" também é quase uma tautologia: qualquer modelo que dependa do volume sofre com o erro do volume.
* Correção sugerida: acrescentar ao Resumo e ao Abstract, antes da comparação com a IC: "Como a carga medida é essencialmente o volume escoado vezes uma concentração pouco variável, uma regra simples proporcional ao volume medido tem desempenho equivalente (erro mediano de 16%); o resultado do MFM mostra, portanto, o peso do volume medido, e não valida a fórmula de erosão."

**C2. Contradição entre 4.4 e 4.5 sobre o que organiza o padrão espacial do mapa.**
* Local: 4.4, 1ª frase: "o padrão espacial é dado sobretudo pelos fatores fixos K, C e LS... Os pontos de maior erosão são os mesmos em todos os eventos e mudam de intensidade, mas não de lugar". 4.5 (parágrafo da partição): o termo de escoamento "responde por mais da metade da variação espacial em escala logarítmica" (62,9% no MC; 66,0% no MFM); K*LS*C sozinho 45,5% e 37,1% após a partição. Conclusões: "37% fatores fixos, 63% escoamento".
* Problema: duas seções adjacentes dão leituras opostas do mesmo mapa. Em escala linear (R2 = 0,58 para K*LS*C) a afirmação de 4.4 é defensável para as manchas mais intensas, mas o texto de 4.4 não diz isso, e "não de lugar" nunca foi quantificado (não há correlação entre os mapas de eventos diferentes). Também é preciso lembrar que o "termo de escoamento" inclui o CN, que vem do uso do solo e portanto não é independente de C.
* Correção sugerida: reescrever a 1ª frase de 4.4 para algo como "As manchas de maior erosão se repetem de um evento para outro, com intensidade proporcional à chuva e ao escoamento do evento; a seção 4.5 mostra quanto desse padrão vem dos fatores fixos e quanto do escoamento". Retirar "não de lugar" ou apoiar com a correlação entre mapas de eventos. Em 4.5, dizer explicitamente que a conclusão sobre "fatores fixos" depende da escala (log: 37%/63%; linear: R2 0,58 e r = 0,76).

### IMPORTANTE

**I1. IC: "47%" no evento 17 contradiz a faixa de erros da IC dada no parágrafo anterior.**
* Local: 4.3, parágrafo da IC ("erros de -37% a +60%") e parágrafo seguinte ("o MFM o subestima em 55%, a regra com o escoamento direto em 61% e a IC em 47%").
* Evidência: recalculei com `_ic_original.py`. Contra a carga medida da própria IC, o erro da IC no evento 17 é -37,1% (915 t simulado contra 1.456 t); é exatamente o extremo "-37%". Contra a carga deste trabalho (1.710 t) é -46,5%. O valor -47% também aparece como "IC" em `tab_resultados.md`, que é a IC refeita (nota do autor: "nada da IC refeita"). Os "47%" do texto são, portanto, ou resíduo da IC refeita, ou um erro calculado contra outra carga medida; em qualquer caso, estão em base diferente da faixa -37% a +60%.
* Correção sugerida: usar uma única base. Se a intenção é comparar os modelos no mesmo evento, dizer "a IC em 46% (915 t simulados contra 1.710 t medidos neste trabalho; 37% contra a carga da própria IC)". Conferir também se o "61%" da regra com o escoamento direto confere com o script.

**I2. Padrão entre estações chuvosas descrito de forma falsa na primeira frase.**
* Local: 4.3, último parágrafo antes do "Em resumo": "O MFM superestima todos os eventos de 2018/19 (eventos 1 a 6...) e subestima os de 2020 (eventos 14 a 17...)".
* Evidência (Tabela 12): os eventos 7 a 10 (jan a mar de 2019, mesma estação 2018/19) são subestimados (-30, -9, -21, -8) e o 11 (jul/2019) também (-24); o evento 13 (jan/2020) é +3%, o 12 (dez/2019) é +8%. "Todos os eventos de 2018/19" é incorreto; só os eventos 1 a 6 (nov/2018 a jan/2019) superestimam. O recorte 1-6 e 14-17 parece escolhido para formar o padrão. A média de ~1.480 mg/L para 2018/19 não pude reproduzir: com os eventos 1 a 6 obtenho ~1.350 mg/L; com 1 a 11, ~1.455 mg/L; para 12 a 16 sem o 17 obtenho ~1.680 mg/L (confere com "cerca de 1.700"). Deixar explícito qual conjunto entra em cada média.
* Correção sugerida: "O MFM superestima os eventos 1 a 6 (nov/2018 a jan/2019, de +18% a +84%) e subestima os eventos 14 a 17 (jan a fev/2020, de -10% a -55%); os eventos intermediários não seguem esse padrão". Se quiser manter a hipótese de mudança ao longo do tempo, mostrar a carga por m3 evento a evento (ou um gráfico) em vez de duas médias de conjuntos escolhidos.

**I3. O expoente 1,12 é atribuído "à própria fórmula", mas decorre da simplificação pr proporcional a Q.**
* Local: 4.3 ("A MUSLE faz o sedimento crescer com a potência 1,12 do escoamento... O expoente 0,56 de Williams... é uma das razões pelas quais a MUSLE não supera a regra linear"); 4.6 "A sexta"; Conclusão 3.
* Problema: o expoente de Williams é 0,56 sobre o produto volume * pico. O 1,12 só aparece porque, na espacialização de Hao adotada em 3.4.3, o pico local é proporcional ao escoamento do pixel (RI/R é constante no evento). Na MUSLE concentrada original, o pico medido não é proporcional ao volume, e a potência efetiva é outra. O texto de 3.4.3 diz isso ("pr,k é proporcional a Q_k"), mas 4.3 e 4.6 transferem a limitação ao expoente de Williams, o que não é bem o que ocorre. Pela mesma razão, o "pico local" não acrescenta informação (dito em 3.4.3), e isso não aparece nem no Resumo nem nas Conclusões: o leitor fica sem saber que, na prática, a "vazão de pico" do modelo é um fator de escala por evento.
* Correção sugerida: em 4.3/4.6, "o expoente efetivo de 1,12 resulta do expoente de Williams combinado com a proporcionalidade entre o pico local e o escoamento"; e acrescentar nas Conclusões uma frase sobre o papel real do pico local.

**I4. Conclusão 2 apresenta o acerto de +3% no volume total como resultado, sem lembrar que foi o critério de escolha dos parâmetros.**
* Local: Conclusões, 2º parágrafo: "reproduziu o volume total... (viés de +3%)". Em 3.4.1.3 e 4.1 o texto diz o oposto: a combinação CN-I + λ 0,05 + S convertido "foi escolhida porque" aproximava o volume, e "não deve ser lido como bom desempenho".
* Correção sugerida: "o volume total ficou próximo do medido (viés de +3%), resultado já esperado porque a configuração foi escolhida com esse critério, mas não o de cada evento...".

**I5. Explicação causal forte demais: "porque a fração da chuva que escoa não cresce com a chuva".**
* Local: Conclusões, 2º parágrafo; 4.1 ("a fração da chuva que escoa não depende da lâmina... r = -0,01... a forma da curva do método não corresponde à resposta desta bacia").
* Problema: o "coeficiente de escoamento medido" é Vdir/(chuva), e Vdir depende da separação de vazão de base, que o próprio texto (4.6, "A quarta") diz ser incerta (BFImax = 0,70 contra 0,25 sugerido para a geologia) e que o autor não controla. Além disso, a chuva R vem de dois postos. Com 17 eventos, r = -0,01 mostra ausência de correlação linear, não prova que a forma da curva está errada.
* Correção sugerida: "indica que" em vez de "porque" nas Conclusões, e uma frase em 4.1 ligando esse resultado à incerteza da separação de base e da chuva.

**I6. Fatores médios da IC (K 0,031; LS 0,536; C 0,267) são muito diferentes dos deste trabalho (0,039; 7,80; 0,050) e a diferença não é explicada.**
* Local: 3.4.8 (modelo da IC) contra Tabela 4 e 3.4.1.2.
* Problema: o texto diz que os valores de K e C por classe são "os da IC", mas o C médio é 5 vezes menor e o LS médio, 14 vezes maior. Um leitor que compare vai perguntar por quê. As notas do autor dizem que o LS da IC estava errado e foi refeito, mas isso não está no texto. Também afeta a leitura da comparação com a IC (coeficientes α e β da IC absorvem esses fatores).
* Correção sugerida: uma frase em 3.4.8 (ou 3.3) explicando a origem de cada diferença (cálculo do LS, forma de tirar a média de C) e dizendo que a comparação com a IC não depende desses fatores, porque α e β os absorvem (se for o caso).

**I7. Origem de R, dos pesos 0,307/0,693 e da lista de eventos não está descrita no método.**
* Local: 3.4.1.4 ("é a da planilha de eventos"), 3.4.8 ("o evento de 24/11/2018 no lugar do de 17/12/2018"), 4.6 ("um evento da lista original (24/11/2018) não foi usado").
* Problema: (i) "planilha de eventos" não foi apresentada na seção 3.2 de dados; R e RI são entradas centrais e não se diz quem as calculou; os pesos 0,307 e 0,693 foram ajustados por mínimos quadrados aos 17 R (segundo `tab_parametros.md`), o que o texto apresenta só como "corresponde, com diferença de até 0,6 mm". (ii) R não é a média espacial do raster IDW (apêndice: média 73,5 mm no evento 11, contra R = 74,0), então o volume de chuva do raster e o R usado em RI/R não coincidem; o texto não discute o efeito (pequeno, mas é preciso dizer). (iii) Nunca se explica por que o evento de 24/11/2018 foi trocado pelo de 17/12/2018.
* Correção sugerida: em 3.2, acrescentar quem forneceu/ calculou R e RI e como; em 3.4.1.4 dizer que R é uma média ponderada ajustada aos eventos e comentar a diferença de ~0,5 mm em relação à média do raster; em 3.2 ou 4.6, justificar a troca do evento.

**I8. Teste de Wilcoxon usado em 4.3 não está no método (3.4.7).**
* Local: 3.4.7 só descreve o bootstrap; 4.3 reporta "Wilcoxon pareado p = 0,02" e "p = 0,52".
* Correção sugerida: acrescentar a 3.4.7 uma frase definindo o teste de postos sinalizados de Wilcoxon pareado sobre os erros percentuais absolutos por evento. Aproveitar para dizer que, com 17 eventos e vários testes, os p valores são indicativos.

**I9. O Apêndice A nunca é citado no corpo do texto.**
* Local: busca por "Apêndice" só encontra o próprio apêndice. 3.4 ou 4.2 deveria dizer "um exemplo numérico completo é dado no Apêndice A".

**I10. Afirmações de uso do mapa sem sustentação nos dados.**
* Local: 4.5, penúltimo parágrafo: "alvos naturais de práticas conservacionistas, de recomposição da cobertura em áreas de campo degradado e de controle da erosão em áreas de solo exposto"; "Em uma bacia de abastecimento..."; Conclusão 6: "o mapa indica onde priorizar".
* Problemas: (i) nada nos dados indica "campo degradado"; C = 0,050 é um valor genérico por classe (e o próprio texto diz que não foi confirmado nas obras). (ii) "bacia de abastecimento" não é estabelecido em 3.1 (só aparece a ETA da SABESP em 3.2). (iii) Mineração (1,8% da erosão) e solo exposto (8,2%) têm C = 1 "adotado"; o destaque dessas classes é consequência direta desse valor adotado, não um resultado independente, e o texto as lista como "alvos". (iv) A atribuição de 92,9% da erosão aos Cambissolos "que têm o maior K" é enganosa: o K do Cambissolo (0,0475) é só 35% maior que o do Argissolo (0,0351); a razão de 135 contra 40 na Tabela 15 vem de uso e declividade que se concentram nos Cambissolos. (v) Conclusão 6 mantém "o mapa indica onde priorizar" mesmo com as classes dominantes (campo, lavoura temporária, Cambissolo) justamente as de K e C não confirmados.
* Correção sugerida: trocar "campo degradado" por "áreas de campo"; justificar "bacia de abastecimento" em 3.1 ou tirar; dizer que mineração e solo exposto aparecem por C = 1 adotado; reescrever a frase dos Cambissolos como "porque concentram os usos e as declividades de maior erosão, além de terem o maior K"; trocar "indica" por "sugere" em 4.5 e na Conclusão 6. Considerar uma análise de sensibilidade simples (por exemplo, trocar C do campo e da lavoura por valores alternativos da literatura e verificar se as mesmas manchas continuam entre as críticas), que é a primeira coisa que um orientador vai pedir, já que o texto admite que esses valores não foram confirmados.

**I11. Lista de eventos "de maior lâmina" errada.**
* Local: 4.4, "nos eventos 9, 14, 15 e 16, os de maior lâmina".
* Evidência (Tabela 2): maiores R = 139,4 (evento 15), 97,7 (16), 92,9 (9), 82,5 (8), 82,2 (14). Os quatro maiores são 8, 9, 15 e 16.
* Correção: "nos eventos 8, 9, 15 e 16" (ou "8, 9, 14, 15 e 16" como os cinco maiores).

**I12. Símbolos usados com mais de um significado.**
* Q: volume de escoamento em m3 (2.2), lâmina de escoamento em mm (2.3, 3.4.2, Tabela 7), vazão (Q pico, 3.2, Tabela 1). P: chuva (P_k, P1, P2) e fator de práticas conservacionistas (na mesma equação de E_unit). S: retenção (3.4.1.3) e carga simulada S_n (3.4.7). R: lâmina de chuva do evento (aqui) e erosividade (nome do fator USLE). c (coeficiente de escala) e C (fator de cobertura) e "c_R", "c_V". Y (2.2, 3.4.8) e SY. Para o leitor, essa sobrecarga é a causa mais provável de confusão no capítulo 3.
* Correção sugerida: trocar pelo menos S_n por SY_sim,n (ou "Ŷ_n") em 3.4.7, usar V (m3) ou D para volume em 2.2 e manter Q só para a lâmina em mm; indicar "Q_vaz" ou "Qpico" para vazão; adotar "p" minúsculo ou "Pr" para o fator de práticas ou escrever "P (práticas)". Incluir uma lista de símbolos.

**I13. Unidades da fórmula de erosão local.**
* Local: 3.4.3: "com Q_k em mm, pr,k em m3/s e Apix em m2, como em Hao et al. (2022)". O produto Q (mm) * pr * Apix (m2) não é dimensionalmente o produto volume * pico da equação de Williams (mm * m2 = 1.000 vezes menos que m3 nominal), mas o texto não diz que a diferença é um fator constante absorvido por c.
* Correção sugerida: acrescentar "(mm * m2 = 10^-3 m3; esse fator constante é absorvido por c)" ou escrever a equação em m3.

**I14. A frase "as métricas principais não dependem da variância dos dados" é inexata.**
* Local: 3.4.7, 1ª frase. O NSE em log (uma das métricas principais) tem no denominador a variância dos logaritmos. O que as métricas escolhidas evitam é o domínio de um único evento grande, não a dependência da variância.
* Correção: "As métricas principais pouco dependem da magnitude absoluta dos eventos e, por isso, não são dominadas por um único evento".

**I15. Lacunas que o orientador provavelmente cobrará (não estão tratadas no texto ou estão só de passagem).**
1. Sensibilidade do mapa a K e C (ver I10).
2. Por que CN-I (seca) para todos os eventos: a justificativa do texto é só o volume total. As notas do autor mencionam o critério de umidade antecedente (NEH-4: 13 dos 17 eventos em AMC I) que daria uma base física independente; se for método final, vale colocar em 3.4.1.3.
3. Ausência de teste de uma geração de escoamento alternativa e simples (por exemplo, escoamento proporcional à chuva, Q = phi*P), sugerida pelo próprio texto: Valle Junior (2019) é citado como tendo achado Q = C*P melhor e a seção 4.1 mostra que o coeficiente de escoamento desta bacia não depende da chuva. O orientador pode perguntar por que o texto diagnostica o problema e não testa a saída óbvia; no mínimo, citar isso em 5.1 de forma explícita.
4. Descasamento temporal: CN vem do uso da terra de 2022 (MapBiomas) e os eventos são de 2018 a 2020; K e C vêm do mapa de uso do Plano de Bacias (2020). O texto reconhece a diferença de fontes (3.3), mas não o intervalo de tempo.
5. A origem dos dados de chuva: não se diz qual instituição opera os postos DBT5 e Campo Limpo (Tabela 1 e 3.2 só dão os nomes).
6. Disponibilidade do código e dos dados (a rotina Python é citada três vezes, mas não há onde obtê-la).
7. As classes de declividade (0-3, 3-8, 8-20, 20-45, 45-75, >75%) não têm fonte citada (são as classes de relevo da Embrapa).
8. A geologia (3.1) é descrita para a "sub-bacia do Jundiaí" inteira (86,1% de embasamento cristalino) e depois usada em 4.6 como se valesse para o alto Jundiaí ("situação mais próxima da sub-bacia, dominada pelo embasamento cristalino com aquífero fraturado"). Dizer que é extrapolação ou mostrar o dado da área de estudo.
9. Apenas uma bacia, 17 eventos e dois postos: está em 4.6, mas a Conclusão não menciona o limite de generalização.

---

### MENOR

**Numérico**
* M1. 3.1: "os 0,3% restantes são corpos d'água, mineração e afloramento rochoso". Pela Tabela 6, esses três somam 0,2% (0,2 + 0,0 + 0,0). A soma dos demais usos (39,6 + 29,0 + 14,1 + 12,7 + 3,9 + 0,5) é 99,8%, então o resto é 0,2%.
* M2. 4.2 e Conclusão 3: "o erro do escoamento explica 91% da variância do erro do sedimento", com r = 0,96. 0,96^2 = 0,92. Se r for 0,955, 91% fecha; informar r com três casas ou usar 92%. Não conferi o r original.
* M3. 4.3: o intervalo "1.085 a 2.088 mg/L" nos outros 16 eventos. Pela Tabela 3, o mínimo é 199/183 = 1.087 mg/L (evento 6) e 1.736/1.595 = 1.088 (evento 16); diferença de rounding, mas confira o mínimo.
* M4. 1.1: "usos como campo e silvicultura (no alto curso, 14,1% e cerca de 42% da área, respectivamente...)". "Respectivamente" aponta 14,1% para o campo e 42% para a silvicultura, o que é falso: 14,1% é área urbanizada e ~42% é campo + silvicultura (29,0 + 12,7). Sugestão: "reúne áreas urbanizadas (14,1% da área do alto curso) e usos como campo e silvicultura (juntos, cerca de 42%; seção 3.1)".
* M5. 4.1: "Em todos os eventos, os maiores valores [de escoamento] aparecem no extremo oeste... e os menores na cabeceira, a leste, que recebe menos chuva na maioria dos eventos". Nos eventos 1, 2, 4 e 17 a chuva é maior a leste (DBT5). "Todos os eventos" pode não valer para esses quatro; conferir os mapas.
* M6. 3.4.1.4 diz R "corresponde, com diferença de até 0,6 mm" à média ponderada; o apêndice mostra média do raster 73,5 contra R = 74,0 (0,5 mm). Coerente, mas a diferença merece ser dita (ver I7).
* M7. 4.3 (IC): "22,5%" na Tabela 13 e no texto, "22%" no Resumo, Abstract e Conclusão. Correto (22,46), só vale padronizar para evitar a pergunta.
* M8. "Seção 4.1, 'abaixo de poucos milímetros'": redação confusa, ver Escrita.

**Escrita e clareza (trecho -> sugestão)**
* "abaixo de poucos milímetros em quase toda a bacia" (4.1) -> "da ordem de poucos milímetros ou menos em quase toda a bacia".
* "Por essa razão, a MUSLE é a formulação de produção de sedimentos do modelo SWAT" (1.1) -> o "por essa razão" não decorre da frase anterior; "A MUSLE é também a formulação de produção de sedimentos do modelo SWAT...".
* "(CAWLEY; TALBOT, 2010; VARMA; SIMON, 2006).. Com 17 eventos" (3.4.6) -> ponto duplicado.
* "Resumo: 'o modelo acertou 35% dos eventos'" -> linguagem coloquial; "35% dos eventos ficaram dentro de fator 2".
* Resumo: "Este trabalho visa reproduzir a MUSLE de maneira espacializada" é mais fraco que o objetivo da seção 1.3.1 (identificar áreas críticas e avaliar o quanto o escoamento limita as estimativas). Alinhar.
* "Nenhum dos trabalhos consultados trata da incerteza da delimitação manual de eventos" (4.6): afirmação de ausência na literatura; trocar por "não encontrei, nos trabalhos consultados, tratamento da incerteza...".
* "a série fornecida... o método e os parâmetros com que ela foi gerada não estão documentados na fonte" (4.6): se a série veio do próprio orientador, o tom soa como crítica a ele. Sugestão: "o método e os parâmetros com que a série foi gerada não constam do material recebido; foram inferidos por reprodução com o filtro de Eckhardt".
* "Modelo Forçado ao Medido" (sem "de Erosão") contra "Modelo Calculado de Erosão": nomes não paralelos; considerar "Modelo Forçado ao Medido de Erosão" ou renomear ambos de forma simétrica. O título de 4.3 usa "modelo calculado de erosão" em minúsculas, enquanto o resto usa "MC".
* "carga", "sedimento", "produção de sedimentos", "descarga sólida" são usados alternadamente (título de 3.2 usa "descarga sólida"; o resto, "carga"). Padronizar: "carga de sedimentos em suspensão" para o medido, "produção de sedimentos" para o conceito.
* "escoamento" aparece como vazão (1.2, "base de dados de escoamento"), lâmina, volume direto e volume total. Em 4.3, "volume medido" é ora volume total (variância 0,66 e 88%, que valem para TR), ora direto (MFM). Dizer sempre qual.
* 1.2 repete três vezes a ideia de "verificar quanto a estimativa do escoamento limita a qualidade", e 1.3.2 itens 4 e 5 se sobrepõem (ambos comparam com modelos simples). Condensar.
* Repetições longas: Baert et al. (2026) com "154 eventos... 0,84 km2" aparece em 2.2, 2.3, 4.1 e 4.2; "os dados de Hao: poucos eventos respondem por mais da metade" em 1.1 e 2.1; a explicação do relato de IC em 3.4.8 e 4.3 (129 t contra 211 t; 1.456 t contra 1.710 t) é quase idêntica. Manter uma vez e remeter.
* A Conclusão tem 6 parágrafos densos de números; o 6º tem ~12 números. Considerar mover os números de classe para 4.5 e deixar na conclusão só o essencial.

**Termos, siglas e inglês**
* Siglas não definidas na primeira ocorrência: SCS-CN no Resumo (só é definido em 2.3); WEPP e LISEM (1.1); SWAT (1.1); NSE usado em 2.2 e 2.3 antes da definição em 2.8; SABESP (2.5, 3.2, nunca por extenso); DAEE aparece em 2.5 e só é definido em 3.2; PCJ (3.1); USGS (Tabela 4); AMC (2.3); SIG nas palavras-chave (definido só em 1.3.1).
* Termos em inglês sem necessidade: "leave-one-out" (Resumo, 3.4.6 e outros; manter definido uma vez e usar "validação cruzada deixando um evento de fora"); "bootstrap" (manter, está definido).
* Equações de IC em 3.4.8 usam D_n para volume e qp para pico; em 2.2 Q e qp. Padronizar.

**Referências e citações**
* Todas as citações do texto têm entrada na lista, e todas as entradas da lista são citadas (conferi uma a uma, incluindo as das Tabelas 5 e 6). Nada falta nem sobra.
* Ordem alfabética: CASTRO deve vir antes de CAWLEY (está depois).
* AZMERI et al.: sem iniciais do primeiro autor (padrão ABNT: SOBRENOME, N. et al.). O mesmo vale se algum outro "et al." não tiver iniciais.
* Formato de DOI não uniforme: alguns com "https://doi.org/", outros "DOI: 10.1029/..." (Gray e Gartner, Ochoa-Rodriguez, Varma e Simon).
* "Silva (2016)", "Silva et al. (2016)" e "Silva e Luchiari (2016)" são três obras diferentes no mesmo ano, citadas nas Tabelas 5 e 6; para evitar confusão, considerar sufixos a, b, c ou citar sempre com as iniciais.
* Fontes da Tabela 6 para Campo ("com base em Silva et al., 2016", obra sobre eucalipto e mata nativa) e Lavoura Temporária: o próprio texto admite que não foram confirmadas; confirmar que a Tabela 6 deixa isso claro (hoje só diz "com base em").
* A frase sobre a regressão por partes de Murillo-Bermúdez et al. (2023) com mudança em 250 NTU é usada em 2.5, 4.3 e 4.6. As notas do autor (proposta_cap4, nota 6) registram que só o resumo dessa obra foi lido e que não se sabe qual curva foi usada nos dados. Além disso, a afirmação de que as maiores concentrações correspondem a "turbidez muito acima de 250 NTU" não é demonstrada no texto (nenhum valor de turbidez é mostrado). Ou dar o valor de turbidez, ou suavizar.

**Estrutura**
* Níveis de título: no arquivo, 3.4.1 a 3.4.9 aparecem como "##" (mesmo nível de 3.4) e 3.4.1.x como "###". Se isso espelha o Doc, o sumário vai listar 3.4.1 a 3.4.9 como irmãs de 3.4. Ajustar para 3.4.1... em nível 3 e 3.4.1.x em nível 4 (ou renumerar).
* Método nos resultados e resultado no método (pequenos): (i) 3.4.4 traz as perdas do limite Q <= P por evento (10,3%, 7,6%, 3,7%), que são resultados; (ii) 3.4.1.3 e 3.4.4 citam o viés de +3%; (iii) 3.4.1.1 a 3.4.1.4 e 3.3 trazem frases de verificação interna ("reproduz exatamente os rasters... verificado pixel a pixel"; "reproduz o raster de chuva do QGIS com diferença menor que 10^-5 mm"; "reproduz o raster de CN seco... diferença menor que 10^-5") que soam como notas de conferência do autor e não como método. Sugestão: cortar ou transformar em "validado contra o cálculo no QGIS" numa frase só.
* 4.6 contém dois resultados novos de sensibilidade (15,1 a 21,9% e 12,9%) que não aparecem em outro lugar e não têm método descrito; se ficarem, dizer em 3.4 (ou em nota de rodapé do método) como foram calculados.
* 3.2 (último parágrafo): "outros valores de BFImax e o filtro de Lyne e Hollick (1979) não a reproduzem" menciona método testado e descartado, contra a regra do autor de só trazer o método final. Pode ficar só "reproduzida pelo filtro de Eckhardt com a = 0,995 e BFImax = 0,70".
* A seção 2.8 e a 3.4.6 repetem o mesmo argumento (viés de otimismo, validação cruzada aninhada). Aceitável (teoria e método), mas reduzir a duplicação em 2.8.
* Apêndice A: o pixel de exemplo é de lavoura temporária sobre Argissolo, enquanto a combinação crítica dominante (4.5) é lavoura sobre Cambissolo. Não é erro; vale uma frase dizendo por que foi escolhido.

**Elementos pré-textuais (não estavam na lista de itens conhecidos)**
* Dedicatória e Agradecimentos estão vazios (títulos sem texto).
* "co-orientação" (grafia anterior ao Acordo; hoje "coorientação").
* Epígrafe de John Flanagan (Halt em Perigo): decisão de gosto; a obra não está na lista de referências, o que é aceitável para epígrafe, mas confirmar se o orientador aceita.

---

## (c) O que está bom

* A coerência numérica geral é alta: Resumo, Abstract, Tabela 13, 4.2, 4.3 e Conclusões trazem os mesmos números principais (81%/35%, 42%/82%, 21%/94%, 46%, +3%, 22%, 94% de coincidência, 37%/63%), e as Tabelas 3, 11, 12 e 16 batem com as fontes. O Apêndice A reproduz corretamente todo o cálculo do evento 11.
* O tratamento das limitações é honesto e específico: o viés de otimismo da validação cruzada (3.4.6), a escolha de parâmetros feita sobre os mesmos eventos, os eventos 1 e 12 fora da faixa da relação de Woodward, a base de IC apenas indicativa, o evento 17 e o evento 15 como sensibilidade, e a seção 4.6 inteira organizada pela cadeia do modelo.
* A ressalva sobre o MFM (volume explica 88% da variância da carga; regra simples com o volume equivale ao MFM; "não é validação da fórmula nem do mapa") está claramente escrita em 4.3 e na Conclusão 4.
* A comparação com a IC é feita só com valores originais, com o motivo de não haver teste pareado declarado, e eu consegui reproduzir os 22,5%, 100%, +4,2% e a faixa -37% a +60% a partir dos valores originais.
* A estrutura de capítulos é lógica (teoria -> dados -> método -> resultados em escada: escoamento, MC, comparação, mapas, incertezas); o fluxo "o que o MC faz de errado -> o que acontece com a água medida -> o que o mapa mostra" é fácil de seguir. As referências estão completas (nada citado sem entrada, nada na lista sem citação).
* Os objetivos da seção 1.3.2 são respondidos nas Conclusões: espacializar o escoamento e o pico (parágrafos 1 e 2), rotina em Python (1), validação cruzada (3), comparação com modelos simples e IC (3, 4, 5), limite do escoamento (4) e mapeamento com contribuição por classe (6). Só o objetivo 4 ("verificar se a espacialização perde precisão") merece uma resposta mais direta: o MC perde para a regra da chuva; o MFM não perde para a regra do volume nem para a IC.
