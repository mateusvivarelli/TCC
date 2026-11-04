# Revisão do texto: versão de 04/11 (RELATÓRIO PARCIAL, em andamento)

**Situação:** versão provisória, gravada a pedido da coordenação, porque o notebook pode ser desligado. O que ainda não foi feito está em "Falta fazer", no fim. Páginas citadas: número impresso (a página do PDF é o número impresso + 1).

## (a) O que foi lido e o que não foi

- Lido por inteiro: o texto das 68 páginas (`Notas Claude/doc_texto_pdf_paginas_04-11.txt`) e `Notas Claude/entrega_tfc_regras.md`.
- Sumário conferido por script contra os títulos no PDF.
- Não feito ainda: ver figuras e equações no PDF (as páginas foram convertidas em imagem, mas ainda não examinadas); `Normas FECFAU/` no original; `leitura_referencias/`; revisão de 03/11.
- As contas abaixo são à mão, a partir das tabelas do próprio texto. O script de recálculo ainda não rodou (falta a biblioteca scipy; vou refazê-lo sem ela).

## (b) Achados até agora (preliminares)

### Crítico

1. **Sumário (p. 9 do PDF, sem número impresso).** Conferido por script: 31 das 43 entradas têm a página errada, de "2. FUNDAMENTAÇÃO TEÓRICA" em diante. Só estão certas as da seção 1 e as de 2.2, 2.4, 2.5 e 2.6. Exemplos (sumário / real): seção 2, 11 / 12; 2.3, 13 / 14; 3, 20 / 21; 3.4.2, 30 / 32; 3.4.8, 36 / 38; 4, 39 / 41; 4.3, 45 / 48; 5, 57 / 59; Referências, 59 / 61; Apêndice A, 63 / 65. Correção: atualizar o sumário depois da última edição.
2. **Pré-textuais (p. 3 a 5 do PDF).** A p. 3 do PDF está em branco, e Dedicatória e Agradecimentos só têm o título. A folha de aprovação, obrigatória no modelo da biblioteca (`entrega_tfc_regras.md`, seção 4), não aparece. Correção: incluir a folha de aprovação; preencher ou retirar as páginas opcionais.
3. **Conclusões, p. 60.** Trecho: "A comparação demonstra que a espacialização não se mostrou pior, e acrescenta o mapa". A seção 4.3 (p. 50) diz que "a comparação é só indicativa". O texto se contradiz. Sugestão: "A comparação indica apenas que, com o escoamento medido, a espacialização chega a um erro da mesma ordem; ela acrescenta o mapa de onde a erosão é produzida."

### Importante

4. **Seção 4.3, p. 50.** Trecho: "em média, maior nos eventos 12 a 16 (cerca de 1.700 mg/L, sem o evento 17) do que nos eventos 1 a 11 (cerca de 1.450 mg/L)". Pela Tabela 3: média simples de cerca de 1.684 e 1.364 mg/L; razão entre as somas de cerca de 1.571 e 1.449 mg/L. Os valores do texto parecem misturar as duas contas. Sugestão: usar uma só conta nos dois grupos e dizer qual é. Confirmar qual foi a usada.
5. **Seção 4.6, p. 57.** Trecho: "quase o dobro da dos demais". A seção 4.3 dá 3.806 mg/L contra 1.085 a 2.088 mg/L: cerca de 1,8 vez o maior valor e cerca de 2,5 vezes a média simples dos outros 16. Sugestão: "cerca de 1,8 vez a maior entre os demais eventos".
6. **Seção 4.3, p. 48 e 49, contra a seção 3.4.7.** O teste de Wilcoxon pareado é usado nos resultados, mas o método só descreve o bootstrap. Sugestão: acrescentar à seção 3.4.7: "A diferença foi avaliada também pelo teste de Wilcoxon pareado." Na mesma linha, "NSE linear" e "erro médio com sinal" (p. 49 e 50) aparecem sem definição na seção 3.4.7.
7. **Seção 3.1, p. 21, contra as seções 4.1 (p. 44) e 4.4 (p. 51).** A seção 3.1 diz que "a cabeceira tende a estar na porção mais chuvosa da sub-bacia"; as outras dizem que a cabeceira "recebe menos chuva" na maioria dos eventos. Pela Tabela 2, DBT5 registra menos que Campo Limpo em 13 de 17 eventos. Sugestão: dizer que a seção 3.1 trata da média anual regional e que, nos 17 eventos, os postos mostram o contrário.
8. **Termo "medido": seção 3.2 (p. 23), Tabelas 3, 7 e 11, seções 4.1 e 4.6.** O mesmo Vdir aparece como "estimado" (seção 3.2, Tabela 3) e "medido" (Tabelas 7 e 11), e a seção 4.1 diz que ele "também é uma estimativa". Sugestão: dizer uma vez que "medido" é o obtido do hidrograma medido, com a base separada por filtro, e manter um só termo.
9. **Tabela 14, p. 53, e Tabela 15.** A coluna "Erosão por área, MC" não tem unidade. Pelos valores (129 = 37,4 / 29,0 * 100), é um índice com a média da bacia = 100. Sugestão: "Erosão por área, MC (média da bacia = 100)".
10. **Tabela 4 e fonte, p. 25.** "USGS" é citado como fonte do MDE, mas não há entrada nas referências, e a sigla não é explicada. MapBiomas e IBGE (p. 27) também não têm entrada própria; aparecem como dados de base da ANA.
11. **Símbolo TR, seção 3.2, p. 23.** Aparece em "o volume TR" sem definição; só é definido na Tabela 7 (p. 29). Sugestão: "o volume total escoado (TR)".
12. **Resumo e Abstract, p. 7 e 8 do PDF, contra as Conclusões.** Ficam de fora dois resultados que as Conclusões tratam como centrais: o MC é pior que a regra simples com a chuva (42% e 82%), e o MFM não se distingue da regra simples com o volume (16%). O Resumo termina no MFM e no mapa. Sugestão: acrescentar uma frase com esses dois resultados.
13. **Referência VIVARELLI et al. (2025), p. 64.** A seção 3.4.8 (p. 38) fala em "coeficientes e cargas simuladas publicados", mas a entrada só diz "Artigo (Iniciação Científica)", sem veículo de publicação. Sugestão: dar o periódico ou evento, ou trocar "publicados" por "originais".
14. **Siglas sem definição na primeira ocorrência no corpo do texto.** SCS-CN (objetivo 1, p. 11; só é explicada na p. 14); PCJ (p. 21); UTM, EPSG, IBGE, USGS.

### Menor

15. **Seção 2.2, p. 13.** "eficiência de Nash-Sutcliffe (NSE) de validação cruzada próximo de zero": concordância. Sugestão: "próxima de zero".
16. **Seção 3.4.7, p. 36.** "Absolute Percentual Error": o termo em inglês é "Absolute Percentage Error". A sigla MedAPE é definida e não volta a ser usada; o texto usa "erro mediano".
17. **Apêndice A, p. 65, e Tabela A1.** "recebe P = 75,4 mm" contraria a seção 3.4.1.1 (p. 29), em que P sem índice é o fator de práticas. Sugestão: "P_k = 75,4 mm".
18. **Conclusões, p. 59.** A incerteza da separação da vazão de base e a chuva de dois postos aparecem em duas frases seguidas. Sugestão: juntar as duas. Na mesma passagem, "não cresce com a chuva, como a curva do método supõe" pode ser lido ao contrário. Sugestão: "não cresce com a chuva, ao contrário do que a curva do método supõe".
19. **Folha de rosto, p. 2 do PDF.** "título de Engenheiro Civil"; o modelo da biblioteca diz "título de Bacharel em Engenharia Civil".
20. **Títulos.** "1.3.1 Objetivo geral:" e "1.3.2 Objetivos específicos:" têm dois-pontos. "REFERÊNCIAS BIBLIOGRÁFICAS": a ABNT e o modelo usam "REFERÊNCIAS".
21. **Símbolos com sublinhado e circunflexo no texto corrido:** Q_k, P_k, E_unit, V_SCS, c_R, f_n, Q_k^1,12, 10^-5 convivem com índices reais nas equações. Falta ver no PDF. O mesmo símbolo varia: Qpico, Q pico e qp; CNI e CN-I; multiplicação com ponto e com asterisco. Q também é usado para vazão (Tabela 1), lâmina e volume.
22. **Objetivo geral, p. 11.** "a estimativa do escoamento superficial direto limita a qualidade das estimativas": repete a palavra e não diz estimativas de quê. Sugestão: "limita a qualidade das estimativas de sedimento". Mesmo problema na seção 1.2 (p. 10), que também repete "verificar".
23. **Repetições.** Seção 3.1: "14,1%" de área urbanizada duas vezes no mesmo parágrafo (p. 21). Seções 3.3 e 3.4.1.1 a 3.4.1.3: grade, K e C não recalibrados, erosão nula e faixa de CN são ditos duas vezes. Seções 1.1 e 2.1: a frase sobre abordagens anuais é quase igual.
24. **Seção 4.5, p. 53.** "o maior K (0,0475, pouco acima dos 0,0351 dos Argissolos)": a diferença é de 35%. Sugestão: retirar "pouco".
25. **Seção 3.2, p. 22.** "duas fontes: os dois postos pluviométricos e a seção de controle", e logo depois a turbidez vem da estação de tratamento da SABESP. Sugestão: citar a estação como terceira fonte.
26. **Pontuação e espaços.** "Para avaliar a erosão em bacias existem" (p. 9): falta vírgula depois de "bacias". Espaço duplo em "corresponde  à média" (p. 31). "abaixo de poucos milímetros" (p. 44): sugestão, "fica em poucos milímetros".
27. **Abstract, p. 8 do PDF.** "Local erosion followed Hao et al." pede "was computed following"; "hit rate" é informal; "calibrated on a logarithmic scale" repete "scale" logo depois de "scale coefficient"; "modelling" (britânico) convive com "watersheds" e "baseflow". Sugestão: revisar esses pontos.
28. **Referências, formato.** Autores listados por inteiro em SADEGHI et al. e MURILLO-BERMÚDEZ et al. (2023), e com "et al." nas demais de muitos autores: uniformizar. SILVA, T. S. tem endereço sem "Acesso em". Espaço entre entradas irregular nas p. 63 e 64. A citação (ANA, 2024) não coincide com a entrada, que começa por "AGÊNCIA NACIONAL": acrescentar a sigla à entrada.

## (c) O que está bom (conferido à mão até agora)

- Citações e lista: pela leitura, todas as obras citadas têm entrada, salvo USGS, e todas as entradas são citadas. Falta conferir por busca automática.
- Remissões a seções, tabelas e figuras apontam para o lugar certo.
- Somas de área e de contribuição das Tabelas 14 a 16 fecham em 100%, e as frases da seção 4.5 batem com elas.
- A partição 37,1 e 62,9 (34,0 e 66,0) confere com os R² informados.
- As métricas do volume na seção 4.1 (46%, 54%, 11 de 17) e os erros do MC e do MFM (81%, 21%, 6 e 16 eventos em fator 2, 10 e 7 eventos por sentido) batem com as Tabelas 11 e 12.
- A conversão de Woodward para milímetros (0,8189), as faixas de CN-I e S e as contas principais do Apêndice A estão coerentes.
- Resumo em parágrafo único, abaixo do limite de 500 palavras (cerca de 260 palavras na página).

## (d) Resumo

Será escrito no relatório final.

## Falta fazer

1. Recalcular por script, a partir das Tabelas 2, 3, 11 e 12: NSE, Spearman, modelos simples, Wilcoxon, bootstrap, correlações (0,96; 91%; -0,01), variâncias (0,66; 0,08; 88%), expoente 0,94, 48,7% do evento 15, e os casos "sem o evento 17" e "sem o evento 15".
2. Conferir a linha da IC na Tabela 13 (22,5%; 100%; 0,91; 0,93) e o arredondamento 22,5% para 22% no Resumo, usando `Planilhas/`.
3. Examinar figuras e equações no PDF (legibilidade, coerência com o texto; localização da mancha urbana: "centro-sul" na seção 4.1 e "perto do exutório" na seção 4.5).
4. Ler o original de `Normas FECFAU/` (regulamento e normalização).
5. Conferir afirmações sobre a literatura contra `leitura_referencias/` e dizer o que não pôde ser conferido.
6. Verificar o ponto do evento de 24/11/2018 (pico de 12,48 m³/s) na planilha e no texto.
7. Ler `revisao_independente_03-11.md` e `alteracoes_doc_03-11.md` e dizer quais achados continuam abertos.
8. Escrever o resumo de 10 linhas e tirar a marca de relatório parcial.
