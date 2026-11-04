# Revisão do texto: versão de 04/11

Páginas citadas: número impresso no rodapé do texto (a página do PDF é o número impresso + 1). "PDF p. N" indica a página do arquivo.

## (a) O que foi lido e o que não foi

**Lido por inteiro:** o texto das 68 páginas (`Notas Claude/doc_texto_pdf_paginas_04-11.txt`), incluindo Resumo, Abstract, Referências e Apêndice A.

**Visto no PDF, como imagem:** Figuras 1 a 11, A1 e A2, as 24 áreas de equação, Tabelas 7, 12 e 13 e a primeira página das Referências. As Figuras 7 e 8 foram vistas em parte com ampliação (Figura 7: eventos 1 a 12; Figura 8: faixa superior). Nas demais, os rótulos menores foram lidos só no tamanho da página.

**Conferido por script ou contra fontes:**
- Sumário contra os títulos no PDF.
- Recálculo a partir das Tabelas 2, 3, 11 e 12 (resultado na seção c).
- Métricas da IC com `Scripts/_ic_original.py`.
- Evento de 24/11/2018 em `Dados Iniciais/Dados_finais_histereses_corrigido.xlsx` e nas listas de eventos.
- 23 DOIs da lista de referências, na base pública Crossref.
- Normas: `entrega_tfc_regras.md`, o modelo `Normalizacao_TFC_FEC_2017.doc` (texto extraído) e busca por termos no `Regulamento_TFC_2023.pdf`.

**Não feito ou não conferido:**
- As obras originais não foram abertas. O que digo sobre a literatura vem de `leitura_referencias/` (ver seção c). Avanzi, Hoppen, Reda, Azmeri e Sadeghi aparecem nas notas como lidos só pelo resumo (`instrucoes_sessao_desktop.md`), e não achei nas notas os números de Avanzi (14,96; 0,59; 286 ha) nem o NSE de 0,66 de Valle Junior.
- Referências sem DOI não foram conferidas na fonte.
- Não recalculado (depende dos rasters): áreas por classe, 94,2% e 0,98 entre mapas, R² da partição, perdas do limite Q <= P, somas de E_unit.
- `Diretrizes_TFC_LALT.pdf` não foi lido (não se aplica ao caso, segundo `entrega_tfc_regras.md`).
- As normas ABNT não estão no repositório. O que digo sobre elas é de memória e está marcado "(ABNT, de memória)".

**Correção de versões anteriores deste arquivo:** um relatório parcial dizia que os valores de 1.700 e 1.450 mg/L da seção 4.3 misturavam duas contas. Foi erro meu de soma à mão: a média simples dá 1.685 e 1.455 mg/L, e o texto está certo. Esse achado foi retirado. O parcial também dava 0,8189 como certo; o valor correto é 0,8187 (achado M1).

## (b) Achados por gravidade

### Crítico

**C1. Sumário com páginas erradas**
- Local: Sumário (PDF p. 9).
- Trecho: "2. FUNDAMENTAÇÃO TEÓRICA....11"; "5. CONCLUSÕES....57"; "REFERÊNCIAS BIBLIOGRÁFICAS....59"; "APÊNDICE A....63".
- Problema: 33 das 43 entradas estão erradas, de 1 a 3 páginas a menos. Só estão certas as seis entradas da seção 1 e as de 2.2, 2.4, 2.5 e 2.6. Valores reais: seção 2, p. 12; 2.3, p. 14; 3, p. 21; 3.4, p. 27; 3.4.2, p. 32; 3.4.8, p. 38; 4, p. 41; 4.2, p. 45; 4.3, p. 48; 4.6, p. 56; 5, p. 59; Referências, p. 61; Apêndice A, p. 65.
- Sugestão: atualizar o sumário depois da última edição e tirar os dois-pontos e o ponto depois dos números (M15).

**C2. Elementos pré-textuais incompletos**
- Local: PDF p. 3, 4 e 5.
- Trecho: p. 3 em branco; "DEDICATÓRIA" e "AGRADECIMENTOS" só com o título.
- Problema: a folha de aprovação é obrigatória no modelo da biblioteca (`Normalizacao_TFC_FEC_2017.doc`: título, aluno, "BANCA EXAMINADORA", linhas de assinatura, "Aprovado em") e não aparece. Dedicatória e agradecimentos são opcionais, mas vazios parecem esquecidos. A ficha catalográfica só é obrigatória para trabalhos selecionados para o acervo.
- Sugestão: incluir a folha de aprovação; preencher ou retirar as duas páginas opcionais; decidir o que fazer com a p. 3.

**C3. O texto não diz que a IC usa outra lista de eventos e outras cargas**
- Local: seção 2.2 (p. 14), 3.4.8 (p. 38), Tabela 13 (p. 48), Figura 8 (p. 46), seção 4.3 (p. 49 a 51), seção 4.6 (p. 57 e 58), Resumo.
- Trecho: "O evento 17 (20/02/2020) é o mais difícil para todos os modelos que usam o escoamento medido: o MFM o subestima em 55%, a regra com o escoamento direto em 61% e a IC em 37%."
- Problema, conferido em `Scripts/_ic_original.py`:
  - A lista da IC tem o evento de 24/11/2018 e não tem o de 17/12/2018.
  - As cargas medidas diferem: 1.455,7 t contra 1.710 t em 20/02/2020; 129,3 t contra 211 t em 30/12/2019; soma de 24.023 t contra 23.846 t.
  - Os 55% e 61% são contra 1.710 t, e os 37% contra 1.456 t. Contra 1.710 t, a IC erraria 46% (915 t simulados).
  - O texto de 03/11 avisava da diferença de lista ("a lista de eventos da IC tem o evento de 24/11/2018 no lugar do de 17/12/2018"). A versão de 04/11 não tem mais o aviso, e o leitor entende que são os mesmos 17 eventos.
  - Também não houve teste pareado com a IC, mas a p. 51 ("nenhuma diferença mensurável entre as formulações que recebem o escoamento medido") e a p. 58 ("não se distinguem entre si") a incluem no conjunto.
- Evento de 24/11/2018 (ponto do LEIAME): ele existe. A planilha tem 12,484 m³/s às 23h de 24/11/2018, e `eventos_processados_manuais.xlsx` o lista como "1B" (24/11 16h a 26/11 21h). A palavra "inexistente" não aparece no PDF de 04/11, então esse erro não está no texto enviado, mas a explicação correta também não. O motivo da troca não está nas notas que consultei (`loteC`, item "Lista de eventos diferente", diz o mesmo).
- Sugestão, em 3.4.8: "A lista de eventos da IC não é igual à deste trabalho: tem o evento de 24/11/2018 no lugar do de 17/12/2018 [autor: dizer o motivo], e as cargas medidas diferem em vários eventos. Por isso, a comparação não é pareada." Em 4.3: "o MFM o subestima em 55% e a regra com o escoamento direto em 61% (carga de 1.710 t); a IC o subestima em 37% contra a sua própria carga de 1.456 t (46% contra 1.710 t)." Na p. 51 e na p. 58, trocar por "entre o MFM e a regra simples com o volume". Na Figura 8, confirmar qual numeração o painel da IC usa e dizê-lo na legenda.

**C4. Conclusão mais forte que a discussão**
- Local: Conclusões, p. 60; seção 4.3, p. 50.
- Trecho: "A comparação demonstra que a espacialização não se mostrou pior, e acrescenta o mapa de onde a erosão é produzida."
- Problema: a seção 4.3 diz que "a comparação é só indicativa". Além disso, "demonstra" não combina com o motivo de C3, e o sujeito de "acrescenta" fica ambíguo.
- Sugestão: "A comparação é só indicativa: com o escoamento medido, a espacialização chega a um erro da mesma ordem que a formulação concentrada e acrescenta o mapa de onde a erosão é produzida."

**C5. Resumo e Abstract deixam de fora os resultados que as Conclusões tratam como centrais**
- Local: PDF p. 7 e 8.
- Trecho: "Com o escoamento direto forçado ao valor medido, o acerto sobe a 94% dos eventos e o erro mediano cai a 21%. O limite está, portanto, na conversão da chuva em escoamento."
- Problema: faltam dois resultados das p. 59 e 60: o MC é pior que a regra simples com a chuva (42%; 82%), e o MFM não se distingue da regra com o volume medido (16%; 94%), o que "não permite avaliar separadamente a fórmula de erosão". Quem lê só o Resumo entende que o MFM valida o modelo. `alteracoes_doc_03-11.md` registra essa correção como aplicada, mas ela não está no PDF de 04/11. O texto de 03/11 tinha a regra da chuva e a frase "não pôde ser validado no espaço", e ambas saíram.
- Sugestão em português (fica dentro do limite de 500 palavras; hoje são cerca de 252): "Com a chuva como única entrada, 35% dos eventos ficaram dentro de fator 2 (erro mediano de 81%), resultado pior que o de uma regra simples proporcional à chuva (82%; 42%). Com o escoamento direto forçado ao valor medido, o acerto sobe a 94% dos eventos e o erro mediano cai a 21%, desempenho que não se distingue do de uma regra proporcional ao volume medido (94%; 16%): o ganho mostra o peso do volume medido e não valida a fórmula de erosão." E, no fim: "..., sob os valores de K e C adotados, sem validação espacial."
- Sugestão em inglês: "With rainfall as the only input, 35% of the events fell within a factor of 2 (median error of 81%), worse than a simple rule proportional to rainfall (82%; 42%). With direct runoff forced to measured values, the share rises to 94% and the median error drops to 21%, which cannot be distinguished from a rule proportional to measured volume (94%; 16%): the gain shows the weight of the measured volume and does not validate the erosion formula." E, no fim: "..., under the adopted K and C values and without spatial validation."

### Importante

**I1. Teste de Wilcoxon sem método**
- Local: seção 3.4.7 (p. 37) contra seção 4.3 (p. 48 e 49).
- Trecho: "o teste de Wilcoxon pareado dá p = 0,02".
- Problema: a seção 3.4.7 só descreve o bootstrap. `alteracoes_doc_03-11.md` diz "3.4.7 (Wilcoxon definido)", mas a frase não está no PDF. "NSE linear" e "erro médio com sinal" (p. 49 e 50) também não são definidos ali.
- Sugestão: acrescentar à seção 3.4.7: "A mesma diferença foi avaliada pelo teste de postos sinalizados de Wilcoxon, pareado por evento. Com 17 eventos, os valores de p são indicativos."

**I2. Afirmações opostas sobre a chuva na cabeceira**
- Local: seção 3.1 (p. 21) contra seções 4.1 (p. 44) e 4.4 (p. 51).
- Trecho: "a cabeceira tende a estar na porção mais chuvosa da sub-bacia" contra "a cabeceira, a leste, que recebe menos chuva na maioria dos eventos".
- Problema: as duas frases se chocam, e o texto não explica. Na Tabela 2, DBT5 (leste) tem média de 44,2 mm e Campo Limpo, de 71,5 mm. `loteC` marca a frase da seção 3.1 como inferência do TCC, não como frase do Plano.
- Sugestão, na seção 4.1: "Esse gradiente é o oposto do que a média anual regional sugere (seção 3.1) e vem só dos dois postos, um deles fora da bacia."

**I3. "Medido" e "estimado" para a mesma grandeza**
- Local: seção 3.2 e Tabela 3 (p. 23 e 24), Tabelas 7 e 11, seção 4.1 (p. 43), título "Modelo Forçado ao Medido".
- Trecho: "o escoamento direto estimado, Vdir" (p. 23); "Vdir: escoamento direto medido" (Tabela 7); "Escoamento estimado" (Tabela 3).
- Problema: o mesmo Vdir tem os dois nomes, e a seção 4.1 diz que ele "também é uma estimativa". Um avaliador pode perguntar qual vale.
- Sugestão, na seção 3.2: "Neste trabalho, 'escoamento direto medido' é o volume obtido do hidrograma medido, menos a vazão de base da série; a parcela da base é uma estimativa." Depois disso, usar só "medido", inclusive na Tabela 3.

**I4. Figuras chamam de massa o que o texto chama de índice**
- Local: Figura A2 (p. 67); Figuras 10 e 11 (p. 51 e 52); seções 3.4.3 e 3.4.9.
- Trecho: eixo da Figura A2, "kg por pixel, sem calibrar", com escala até 3.000; texto: "E_unit,k é um índice relativo de erosão, e não uma massa"; Apêndice: E_unit = 1,167.
- Problema: (a) o painel contradiz o texto e está em outra escala (1,167 viraria 1.167); (b) as figuras dizem "Sedimento estimado" e "Sedimento médio", e as legendas e o texto dizem "erosão", embora a seção 3.4.4 avise que o mapa não mostra o sedimento que chega à rede; (c) a seção 3.4.9 diz "t por pixel", e as figuras e o Apêndice dizem kg.
- Sugestão: refazer a Figura A2 com "índice E_unit (adimensional)" e a escala do texto; usar "erosão local" nas Figuras 10, 11 e A2; escrever "kg por pixel" na seção 3.4.9.

**I5. Frase sobre Baert sem apoio nas notas de leitura**
- Local: seção 2.2, p. 13.
- Trecho: "(-0,03 e 0,01), mesmo com o volume e o pico melhorados."
- Problema: `loteA`, ponto de atenção 2 sobre Baert, já apontou: nessa previsão fora da amostra, o volume tem NSE de 0,21 e 0,40 e o pico, de -0,26 e 0,34. "Melhorado" não vale para o pico por regimes. Não abri o original.
- Sugestão: "(-0,03 e 0,01); com o volume e o pico medidos, o NSE chegou a 0,66."

**I6. Coluna sem unidade**
- Local: Tabelas 14 e 15, p. 53.
- Trecho: "Erosão por área, MC" (19; 129; 191; 530; 1.772; 3.784).
- Problema: o leitor não sabe o que é. Pelos valores, 100 é a média da bacia (129 = 37,4 / 29,0 * 100).
- Sugestão: "Erosão por área, MC (média da bacia = 100)".

**I7. Fontes de dados sem referência**
- Local: Tabela 4 e fonte (p. 25), Figura 1, seção 3.3 (p. 27).
- Trecho: "MDE de 30 m (USGS)"; "do USGS"; "MapBiomas (coleção 2023, ano de 2022)"; "mapa pedológico do IBGE".
- Problema: é a única citação sem entrada na lista (USGS), e a sigla não é explicada. MapBiomas e IBGE aparecem como bases da ANA, sem entrada própria.
- Sugestão: incluir a entrada do MDE (produto, ano de acesso) e explicar a sigla. Para MapBiomas e IBGE, deixar claro que a citação é via ANA (2024) ou incluir entradas.

**I8. Símbolo TR sem definição no primeiro uso, e T_R nas figuras**
- Local: seção 3.2, p. 23; Tabela 3; Figuras 4 e 5.
- Trecho: "o volume TR é exatamente a soma das vazões horárias".
- Problema: TR só é definido na Tabela 7 (p. 29). As Figuras 4 e 5 escrevem "T_R".
- Sugestão: "o volume total escoado (TR)" e o mesmo símbolo nas figuras.

**I9. Referência da IC incompleta**
- Local: seção 3.4.8 (p. 38) e Referências (p. 64).
- Trecho: "coeficientes e cargas simuladas publicados"; "VIVARELLI, M. G. et al. [...] Artigo (Iniciação Científica) - Universidade Estadual de Campinas, Campinas, 2025."
- Problema: a entrada não diz onde foi publicado, e o leitor não consegue achar os números. `_ic_original.py` registra que as cargas simuladas vêm de uma planilha do Drive, não do artigo.
- Sugestão: dar o veículo e, se os valores vieram da planilha, escrever "valores originais da IC, fornecidos pelo autor" em vez de "publicados".

**I10. Localização da área urbana**
- Local: seção 4.1 (p. 44) contra seção 4.5 (p. 55).
- Trecho: "na mancha urbana da porção centro-sul" contra "a área urbanizada [...] está concentrada perto do exutório".
- Problema: as Figuras 2 e 3 mostram manchas no extremo oeste e também uma grande no centro-sul. A frase da seção 4.5 sustenta o argumento sobre deslocar sedimento para as áreas rurais.
- Sugestão: "está no extremo oeste, perto do exutório, e na porção centro-sul".

**I11. "Quase o dobro" e "concentração por metro cúbico"**
- Local: seção 4.6, p. 57.
- Trecho: "O evento 17, com concentração média por metro cúbico de escoamento direto quase o dobro da dos demais".
- Problema: 3.806 mg/L é cerca de 1,8 vez o maior dos outros (2.088 mg/L) e cerca de 2,5 vezes a média deles (1.527 mg/L). A seção 4.3 chama a mesma grandeza de "carga por metro cúbico".
- Sugestão: "com carga por metro cúbico de escoamento direto cerca de 2,5 vezes a média dos demais".

**I12. Origem de R e dos pesos**
- Local: seção 3.4.1.4, p. 31 e 32; Figura 1 (rodapé).
- Trecho: "é a da planilha de eventos (Tabela 2). Ela corresponde à média ponderada dos dois postos com pesos de 0,307 (DBT5) e 0,693 (Campo Limpo)".
- Problema: a "planilha de eventos" não foi apresentada na seção 3.2. Os pesos foram ajustados aos 17 eventos (`tabelas/tab_parametros.md`), e o texto não diz isso. A correspondência não é exata: no evento 16, a conta dá 98,2 mm e a tabela, 97,7 mm; nos outros 16, a diferença é de até 0,08 mm. O texto de 03/11 dizia "diferença de até 0,6 mm", e isso saiu.
- Sugestão: "R é a chuva por evento da planilha de dados (coluna [autor: nome]); ela é reproduzida por uma média ponderada dos dois postos, com pesos ajustados por mínimos quadrados aos 17 eventos (0,307 e 0,693), com diferença de até 0,6 mm."

**I13. Afirmação sobre a turbidez sem valor mostrado**
- Local: seção 4.3 (p. 50) e 4.6 (p. 57).
- Trecho: "as maiores concentrações da série correspondem a turbidez muito acima de 250 NTU".
- Problema: nenhum valor de turbidez aparece no texto. `loteC` registra que só o resumo de Murillo-Bermúdez et al. (2023) foi lido, e que a equação escrita em 2022 é outra (potência, sem quebra); a curva usada nos dados não está esclarecida nas notas. Não recalculado.
- Sugestão: dar o valor máximo de turbidez da série ou suavizar: "podem corresponder a turbidez acima da faixa das amostras de calibração".

**I14. Figura 9 agrupa modelos sob rótulos que não valem para eles**
- Local: Figura 9, p. 48.
- Trecho: grupos "Escoamento calculado a partir da chuva" (MC e regra simples) e "Escoamento direto forçado ao medido" (MFM e IC).
- Problema: a regra simples não calcula escoamento, e a IC usa o volume total, com a base. A figura é apresentada como "a comparação mais importante", mas deixa de fora a regra com o volume (16%; 94%), justamente o que a seção 4.3 usa para fazer a ressalva sobre o MFM.
- Sugestão: rótulos "Só chuva" e "Volume medido" e uma terceira barra para a regra com o volume.

**I15. Siglas sem definição na primeira ocorrência do corpo do texto**
- Local: SCS-CN (objetivo 1, p. 11; explicada na p. 14); IDW (p. 18: nome em português, sigla em inglês sem expansão); PCJ (p. 21); USGS (p. 25); IBGE, EPSG e UTM (p. 25 a 31).
- Sugestão: expandir na primeira ocorrência, por exemplo "Bacias dos Rios Piracicaba, Capivari e Jundiaí (PCJ)". Para SCS-CN no objetivo, "método do número de curva (SCS-CN)". Considerar uma lista de siglas e símbolos, que o modelo permite como opcional.

**I16. Símbolos com formato e sentido variáveis**
- Local: em todo o texto; ver Tabela 7 (p. 29), seção 4.2 (p. 45), equações das p. 15 e 30.
- Problema:
  - O mesmo tipo de símbolo aparece com sublinhado (P_k, Q_k, E_unit, V_SCS, c_R, f_n, O_n), com índice real (Apix, Vdir, SYobs nas tabelas) e sem índice (P1, P2, pr,k). Potências aparecem como Q_k^1,12 e 10^-5. Em um trabalho final, o sublinhado parece nota de programação.
  - "CN - I_k" (equações da p. 30) sai no PDF como uma subtração. A seção 2.3 escreve CN com índice I, e o texto, CN-I.
  - Na equação da p. 32, RI sai como R com índice I; no texto é RI. Pico aparece como Qpico, Q pico e qp.
  - Q é vazão (Tabela 1), lâmina (mm) e volume (m³, seção 2.2). S é retenção e carga simulada (S_n, seção 3.4.7). P sem índice é fator de práticas (p. 29), mas o Apêndice escreve "P = 75,4 mm" (p. 65 e Tabela A1).
- Sugestão: passar tudo para índice e expoente reais; escrever CN com índice nas equações; trocar S_n por SY_n na seção 3.4.7; escrever P_k no Apêndice.

### Menor

**M1.** Seção 2.3, p. 15. "S0,05 = 0,8189 * S0,20^1,15": a conta dá 1,33 * 25,4^(-0,15) = 0,8187, valor que `loteA` também registra como o citado por Brandão et al. A forma da seção 3.4.1.3 está certa. Trocar por 0,8187.

**M2.** Figura 2 (p. 25) contra seção 3.1 e Tabelas 5 e 6. A legenda da figura traz Cambissolos 68,5%, Argissolos 17,7% e Silvicultura 12,6%; o texto, que remete à figura, traz 68,6%, 17,6% e 12,7%. Provavelmente a figura usa a área da bacia e as tabelas, os pixels de cálculo. Dizer qual base vale ou igualar.

**M3.** Tabela 13 (p. 48). O cabeçalho quebra em "Spearma / n". Alargar a coluna ou usar "r_s".

**M4.** Seção 2.2, p. 13. "eficiência de Nash-Sutcliffe (NSE) de validação cruzada próximo de zero": concordância. Escrever "próxima de zero".

**M5.** Seção 3.4.7, p. 36. "Absolute Percentual Error": o termo é "Absolute Percentage Error". MedAPE é definido e não volta a ser usado; o texto e as figuras dizem "erro mediano" e "erro percentual mediano". Fixar uma forma.

**M6.** Conclusões, p. 59.
- "não cresce com a chuva, como a curva do método supõe" pode ser lido ao contrário. Escrever "não cresce com a chuva, ao contrário do que a curva do método supõe".
- A incerteza da vazão de base e a chuva de dois postos aparecem em duas frases seguidas. Sugestão: "...com a ressalva da incerteza da separação da vazão de base e da chuva de apenas dois postos. A delimitação manual dos eventos também pesa."

**M7.** Tabela 9 (p. 35) contra seção 3.4.1.2 (p. 30). "sem práticas na bacia" contra "não há práticas conservacionistas mapeadas": são afirmações diferentes. Usar a segunda.

**M8.** Seção 4.1, p. 44.
- "Em todos os eventos, os maiores valores aparecem no extremo oeste": nos eventos 1 e 4 da Figura 7, o oeste não se destaca. Nos eventos 1, 2, 4 e 17, chove mais a leste. Escrever "Na maioria dos eventos".
- "fica abaixo de poucos milímetros": escrever "fica em poucos milímetros ou menos".

**M9.** Seção 4.5, p. 53. "o maior K (0,0475, pouco acima dos 0,0351 dos Argissolos)": a diferença é de 35%. Retirar "pouco".

**M10.** Seção 3.2, p. 22. "duas fontes: os dois postos pluviométricos e a seção de controle", e a turbidez vem da estação de tratamento da SABESP. A Tabela 1 diz "Seção de controle, a partir de turbidez". Sugestão: "três fontes", ou explicar que a estação capta água no mesmo trecho, se for o caso.

**M11.** Seção 1.3.1, p. 11. "a estimativa do escoamento superficial direto limita a qualidade das estimativas": repete a palavra e não diz estimativas de quê. Escrever "a qualidade das estimativas de sedimento". O mesmo vale para a seção 1.2 (p. 10), que também repete "verificar".

**M12.** Frases longas. Exemplos e cortes:
- p. 16 e 17: a definição de NTU, dentro de um parêntese no meio da frase da regressão: passar para uma frase própria ("NTU é a unidade nefelométrica de turbidez...").
- p. 18: "o método é simples [...] entre eles": dividir depois de "cada posto".
- p. 50: "mas a comparação é só indicativa: o que a comparação permite dizer é que": escrever "mas a comparação é só indicativa: permite dizer que".

**M13.** Repetições.
- Seção 3.1: "14,1%" duas vezes no mesmo parágrafo (p. 21).
- Seções 3.3 e 3.4.1.1 a 3.4.1.3: a grade, K e C não recalibrados, a erosão nula e a faixa de CN são ditos duas vezes.
- Seções 1.1 e 2.1: a frase sobre abordagens anuais é quase igual.
- "154 eventos... 0,84 km²" aparece nas seções 2.2, 2.3 e 4.1.
- Sugestão: deixar uma vez e remeter.

**M14.** Pontuação e espaços.
- "Para avaliar a erosão em bacias existem" (p. 9): vírgula depois de "bacias".
- Espaços duplos em "corresponde  à média" (p. 31) e em "calibrado   c" (p. 45).
- "dá p = 0,02. A diferença não se explica pelo acaso" (p. 49) e o mesmo nas Conclusões (p. 59): com p = 0,02 e 17 eventos, "dificilmente se explica pelo acaso" é mais justo.

**M15.** Títulos.
- "1.3.1 Objetivo geral:" e "1.3.2 Objetivos específicos:" têm dois-pontos.
- "1. INTRODUÇÃO" tem ponto depois do número; o modelo usa "1 INTRODUÇÃO".
- "REFERÊNCIAS BIBLIOGRÁFICAS": o modelo usa "Referências".
- A seção 4.3 diz "modelo calculado de erosão" em minúsculas, e as Conclusões, "Modelo Calculado (MC) de erosão"; a seção 3.4 define "Modelo Calculado de Erosão (MC)".

**M16.** Capa e folha de rosto (PDF p. 1 e 2), contra o modelo de 2017.
- Texto do modelo: "título de Bacharel em Engenharia Civil"; PDF: "título de Engenheiro Civil". Modelo: "como requisito parcial".
- O modelo pede "Orientador(a): Nome" em linha própria, à direita.
- Fontes: o modelo pede Arial 14 no nome e na instituição e Arial 16 negrito no título; o PDF usa 12 e 14.
- Confirmar com a coordenação se o modelo de 2017 ainda vale.

**M17.** Referências.
- Autores por extenso em SADEGHI et al. e MURILLO-BERMÚDEZ et al. (2023), e "et al." nas demais obras de muitos autores: uniformizar.
- SILVA, T. S. tem endereço sem "Acesso em".
- Espaço entre entradas irregular nas p. 63 e 64.
- A citação (ANA, 2024) não coincide com o início da entrada ("AGÊNCIA NACIONAL..."): acrescentar a sigla à entrada, por exemplo "AGÊNCIA NACIONAL DE ÁGUAS E SANEAMENTO BÁSICO (Brasil) - ANA" (ABNT, de memória).
- Silva (2016), Silva et al. (2016) e Silva e Luchiari (2016) nas Tabelas 5 e 6 são obras diferentes: cuidado ao citar.

**M18.** Figuras.
- Título dentro da imagem repete a legenda (Figuras 1, 3, 5, 6, 7, 8, 10, 11, A1, A2).
- O texto menor dentro das imagens é muito pequeno na página impressa, embora a resolução seja boa (300 dpi ou mais nas sete figuras medidas): rótulos dos eventos nas Figuras 6, 7 e 10; rodapés das Figuras 1, 3 e 11; números dos eventos na Figura 8, que se sobrepõem no grupo central. Aumentar a fonte.
- Na Figura 11, as legendas inferiores ficam sobre o contorno da bacia, e MC e MFM têm escalas de cores diferentes (até cerca de 175 e 100), o que atrapalha comparar os dois mapas. Usar a mesma escala ou avisar na legenda.
- A Figura 4 traz "pr = Q*(RI/R)", forma mais curta que a equação da p. 32, e o quadro do MFM não cita o limite Q <= P.
- A fonte da Figura 9 está à esquerda; nas outras, centrada.

**M19.** Legendas e equações (ABNT, de memória; conferir na norma).
- A NBR 14724 pede a identificação de ilustrações na parte superior; aqui as figuras têm legenda embaixo.
- As equações não têm número, e o texto remete a elas por seção ("pela equação da seção 3.4.5"). Numerar facilita a remissão, a defesa e a arguição.

**M20.** Tabela 3 (p. 24) e Tabela 11. Os totais são das somas sem arredondar: as colunas somam 28.933, 13.673, 15.262 e 23.848 contra 28.934, 13.671, 15.263 e 23.846. Acrescentar à fonte: "Totais calculados antes do arredondamento."

**M21.** Notas de conferência dentro do método: "verificado pixel a pixel" (p. 29), "diferença menor que 10^-5" (p. 30), "diferença menor que 10^-5 mm" (p. 31). Reduzir a uma frase. Na seção 3.4.4 (p. 34), as perdas do limite Q <= P (10,3%; 7,6%; 3,7%) são resultado e caberiam na seção 4.

**M22.** Abstract (PDF p. 8). Os números conferem com o Resumo, e o inglês é compreensível. Ajustes:
- "aims to spatialize MUSLE": "applies MUSLE in spatially distributed form".
- "Local erosion followed Hao et al.": "Local erosion was computed following Hao et al.".
- "scale coefficient was calibrated on a logarithmic scale": "scaling coefficient was calibrated in log space".
- "hit rate": ver a sugestão de C5.
- "modelling" (britânico) convive com "baseflow" e "watersheds": escolher uma grafia, por exemplo "modeling".
- "the relation of Woodward": "the relation proposed by Woodward".

**M23.** Resumo. "visa reproduzir a MUSLE de maneira espacializada" é mais fraco que o objetivo geral da seção 1.3.1. Escrever "aplica a MUSLE de forma espacializada para identificar áreas críticas e avaliar quanto o escoamento limita as estimativas". "calibrado em escala logarítmica" vem logo depois de "coeficiente de escala": escrever "coeficiente foi calibrado em logaritmos".

## (c) O que está bom

**Ortografia e gramática:** o texto está limpo. Achei só um erro de concordância (M4) e pontuação de detalhe. A redação é clara na maior parte.

**Coerência numérica:** Resumo, Abstract, Tabela 13, seções 4.1 a 4.5 e Conclusões trazem os mesmos números principais.

Recálculo feito por script, a partir das tabelas do próprio texto:

| Item | Texto | Recalculado |
|---|---|---|
| Durações, médias e somas (Tabelas 2 e 3) | conferem | iguais, salvo arredondamento (M20) |
| Viés de volume | +2,9% | +2,88% |
| Volume: erro mediano, médio, fator 2, NSE | 46%, 54%, 65%, -0,39 | 46,4%, 53,9%, 64,7%, -0,39 |
| MC, validação cruzada | 81,1%, 35%, -0,69, 0,59 | 81,1%, 35,3%, -0,69, 0,59 |
| MFM, validação cruzada | 20,6%, 94%, 0,84, 0,83 | 20,6%, 94,1%, 0,84, 0,83 |
| Regra com a chuva | 41,9%, 82%, 0,53, 0,63 | 41,8%, 82,4%, 0,53, 0,63 |
| Regra com o volume direto | 15,9%, 94%, 0,85, 0,90 | 15,9%, 94,1%, 0,85, 0,90 |
| IC, valores originais | 22,5%, 100%, 0,91, 0,83, 0,93, +4,2%, -37 a +60 | 22,46%, 100%, 0,91, 0,83, 0,93, +4,15%, -37,1 a +60,0 |
| MC contra regra da chuva | 14 de 17; +32,6; +3,1 a +117,5; p = 0,02 | 14 de 17; +32,6; +3,1 a +117,5; p = 0,02 |
| MFM contra regra do volume | +1,6; -5,5 a +10,4; p = 0,52; 6 de 17 | +1,4; -5,6 a +10,4; p = 0,52; 6 de 17 (entrada arredondada) |
| Sem o evento 17 (MFM) | 15,3%, 100% | 15,3%, 100% (c refeito) |
| Sem o evento 15 (MFM) | 20,6%, 94% | 20,7%, 93,8% |
| Correlação dos erros; variância explicada | 0,96; 91% | 0,956; 91,4% |
| Coeficiente de escoamento contra chuva | -0,01 | -0,01 |
| Variâncias do log; explicada pelo volume | 0,66; 0,08; 88% | 0,66; 0,08; 88% (variância populacional) |
| Expoente carga contra volume | 0,94 | 0,93 (volume total), 0,94 (direto) |
| Evento 15 na soma dos quadrados | 48,7% | 48,7% |
| Regra da chuva no evento 6; regra do volume no evento 17 | 3,7 vezes; -61% | 3,69 vezes; -60,7% |
| Carga por m³ | 3.806; 1.085 a 2.088; 1.700; 1.450 | 3.808; 1.087 a 2.089; 1.685; 1.455 (entrada arredondada) |
| Apêndice A | 64,2; 141,9; 244,2; 12,2; 13,00; 5,17 * 10^-4; 1,167 | 64,16; 141,9; 244,2; 12,2; 12,99; 5,16 * 10^-4; 1,168 |
| Partição do R² | 37,1 e 62,9; 34,0 e 66,0 | iguais, a partir dos R² informados |
| Tabelas 14 a 16 | somam 100%; frases da seção 4.5 | conferem |

**Estrutura:** capítulos em ordem lógica, objetivos respondidos nas Conclusões, seção 4.6 bem organizada pela cadeia do modelo e limitações tratadas com clareza.

**Remissões:** todas as remissões a seções, tabelas, figuras e ao Apêndice A que conferi apontam para o lugar certo. As tabelas e figuras estão em ordem.

**Citações:** por busca no texto, todas as obras da lista são citadas, e toda obra citada tem entrada, salvo USGS. Os 23 DOIs da lista existem no Crossref, e o primeiro autor, o periódico, o volume e as páginas batem com a entrada. As diferenças são de metadados: ano online em Eckhardt, Sadeghi e Murillo-Bermúdez (2023), e ordem de autores em Sartori e em Murillo-Bermúdez e Martim (2022).

**Literatura, conferida só contra `leitura_referencias/`, sem abrir os originais:**
- Hao: 1.314 bacias, 80%, 58 eventos, 1.310 a 8.973 km², NSE de 0,70 a 0,83 no ajuste.
- Baert: 154 e 46 eventos, 0,84 km², NSE de 0,13, -0,87, 0,21, 0,40, -0,03, 0,01 e 0,66.
- Woodward: 252 de 307, equação, tabela de CN de 35 a 100.
- Brandão: 3.578 bacias, menos de 15%.
- Valle Junior: 0,045 e a conclusão sobre o SCS-CN.
- Eckhardt: 0,80, 0,50 e 0,25.
- Minella: 1,19 km², 17 de 19.
- Murillo-Bermúdez e Martim: 13 e 4.
- Plano de Bacias: 1.195 a 1.609 mm; 86,1%, 9,9% e 4,1%. A classe Cfb e Cfa é leitura de mapa de baixa resolução (`notas_musle_espacializada.md`), e o texto a apresenta como leitura do mapa, o que está correto.

**Formato:** A4, margens de 3 e 2 cm, Arial 12, número de página no alto à direita, contagem a partir da folha de rosto. Resumo em parágrafo único, com cerca de 252 palavras, e Abstract, com cerca de 233 (limite de 500). Figuras com boa resolução. Equações legíveis, salvo a nota sobre CN-I (I16) e a fração pequena da p. 32.

## (d) Resumo: o que corrigir primeiro

1. Dizer em 3.4.8 e 4.3 que a IC tem outra lista de eventos e outras cargas; corrigir a frase do evento 17 e não incluir a IC em "não se distinguem" (C3).
2. Trocar "A comparação demonstra" nas Conclusões por redação coerente com a seção 4.3 (C4).
3. Acrescentar ao Resumo e ao Abstract que o MC perde para a regra da chuva e que o MFM não se distingue da regra do volume (C5).
4. Incluir a folha de aprovação; preencher ou retirar Dedicatória e Agradecimentos (C2).
5. Atualizar o sumário no fim: 33 de 43 entradas estão erradas (C1).
6. Refazer a Figura A2 e usar "erosão local" e "kg por pixel" nas Figuras 10, 11 e A2 e na seção 3.4.9 (I4).
7. Definir o Wilcoxon na seção 3.4.7 e corrigir a frase sobre Baert na seção 2.2 (I1, I5).
8. Resolver as contradições de texto: chuva na cabeceira, área urbana, "quase o dobro", "medido" e "estimado" (I2, I10, I11, I3).
9. Completar o que falta: unidade da Tabela 14, referência do USGS, veículo da IC, origem de R, TR e siglas (I6, I7, I9, I12, I8, I15).
10. Por último: símbolos com índice real, 0,8187, "Spearman" na Tabela 13, fontes das figuras e detalhes do Abstract (I16, M1, M3, M18, M22).

## Anexo: situação dos achados de `revisao_independente_03-11.md`

Li essa revisão e `alteracoes_doc_03-11.md` depois da minha primeira leitura.

**Continuam abertos:**
- C1 (Resumo e Abstract): aberto e pior que em 03/11. Ver C5 acima. As alterações o dão como aplicado, mas o PDF não o tem.
- I1 (IC no evento 17): o valor virou 37%, mas a base continua sem ser dita. Ver C3.
- I7 (origem de R e motivo da troca do evento): aberto. Ver I12 e C3. A frase sobre 24/11/2018 saiu do texto.
- I8 (Wilcoxon): aberto. As alterações o dão como aplicado, mas o PDF não o tem. Ver I1.
- I12 (símbolos): aberto, com uma frase de explicação na seção 3.4.1.1. Ver I16.
- Siglas: em parte resolvido; restam as de I15.
- 250 NTU sem valor mostrado: aberto. Ver I13.
- M5 ("Em todos os eventos"): aberto. Ver M8.
- "abaixo de poucos milímetros": aberto. Ver M8.
- Dedicatória e Agradecimentos vazios: aberto. Ver C2.
- Notas de conferência e resultados no método: aberto. Ver M21.
- Parte de I3: o papel real do pico local segue sem aparecer nas Conclusões.
- Parte de I15 ainda sem resposta no texto: quem opera os postos; fonte das classes de declividade; geologia da sub-bacia inteira usada para o alto Jundiaí (seção 4.6). Disponibilidade do código e dos dados também não aparece. Esses pontos cabem mais aos avaliadores; aponto só que continuam sem resposta.
- Nomes não paralelos (MC e MFM) e alternância de "carga", "sedimento" e "descarga sólida": aberto.

**Resolvidos no PDF de 04/11:**
- C2 (seções 4.4 e 4.5).
- I2 (eventos 1 a 6 e 14 a 17).
- I4 (+3% como critério).
- I5 ("indica que").
- I6 (os fatores médios da IC saíram do texto; sem esses números, a pergunta não surge).
- I9 (Apêndice A citado na seção 3.4.3).
- I10 ("campo degradado" e "bacia de abastecimento" saíram; "sugere").
- I11 (eventos 8, 9, 15 e 16).
- I13 (a seção 3.4.3 explica que as unidades ficam em c).
- I14 (frase da variância).
- M1 (0,2%), M4 (14,1% e 42%).
- DOI uniforme, ordem CASTRO e CAWLEY, "coorientação".
- AZMERI: a entrada "et al." está certa, segundo as alterações, e o Crossref traz o nome único.
- I3, quanto ao expoente de 1,12.
- 4.6: as sensibilidades sem método (15,1 a 21,9%; 12,9%) saíram.

## Falta fazer

Atualizado na retomada na nuvem (04/11, tarde).

**Feito na retomada:**
1. Figura 7, eventos 13 a 17, vista a 200 dpi (PDF p. 46): o padrão confere com o texto (oeste mais escuro; evento 15 o mais intenso). Nada a acrescentar a M8 e M18.
2. Metade inferior da Figura 8 (PDF p. 47), a 200 dpi: no painel da IC, o evento 12 aparece com carga medida de cerca de 130 t, e nos outros três painéis, em 211 t. Ou seja, o eixo "Sedimento medido" do painel da IC usa as cargas da IC, e não as do TCC. Isso reforça C3: a legenda deve dizer que o painel da IC tem outra lista de eventos e outras cargas.
3. NSE de 0,66 de Valle Junior: está em `leitura_referencias/loteA...md` (linha sobre Q = C * P, com C médio de 0,025, R² 0,71 e NSE 0,66). Conferido só na nota, não no original.

**Continua em aberto:**
- Páginas 2 a 4 das Referências como imagem (negrito e alinhamento; o texto delas foi lido).
- Referências sem DOI, na fonte; números de Avanzi (14,96; 0,59; 286 ha): não achados nas notas.
- Pontos marcados "(ABNT, de memória)": conferir na norma, que não está no repositório.
- Regulamento de 2023: só busca por termos.
