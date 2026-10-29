# Plano de reestruturação do TCC a partir dos comentários do Luis (30/10/2026)

Escrito pela sessão na nuvem (noite de 29 para 30/10/2026), sem acesso ao usuário nem ao Google Doc. Base: `comentarios_luis_29-10.md` (C9 a C31, S9 a S31), `doc_texto_completo_29-10b.md` (texto do Doc), `pontos_discussao_e_reuniao_29-10.md` (orientações da reunião), `revisao_processo_29-10.md`, propostas de 29/10 (`proposta_secao4.md`, `proposta_secao5.md`, `proposta_secao6.md`) e `tarefa_nuvem_30-10.md`. **Nada foi aplicado no Doc.**

Arquivos que esta sessão produz (um por item):
- B: `ajustes_cap1_a_3_30-10.md` (pares "trecho atual -> trecho novo" no Resumo, Abstract e capítulos 1 a 3).
- C: `proposta_cap3_30-10.md` (capítulo 3 inteiro, Materiais e métodos).
- D: `proposta_cap4_30-10.md` (capítulo 4 inteiro, Resultados e discussão).
- E: `proposta_cap2_30-10.md` (capítulo 2 enxuto, só teoria).
- F: `proposta_cap5_30-10.md` (Conclusões e trabalhos futuros).
- G: `mapa_figuras_tabelas_30-10.md` e a planilha com a IC original.
- H: `leitura_referencias/loteE_medicao_e_validacao.md`.
- I: `perguntas_para_o_luis_30-10.md`.
- K: `roteiro_aplicacao_doc_30-10.md`.

---

## 1. Sumário novo do TCC

Legenda da coluna "Origem": de onde vem o conteúdo no Doc atual (seção e parágrafo). "Novo" = texto que não existe no Doc.

| Seção nova | Título | Origem no Doc atual | Arquivo da proposta |
|---|---|---|---|
| Resumo / Abstract | (mesmos) | Resumo e Abstract; trocar "água" e "taxa/razão"; ajustar remissões | B |
| 1 | INTRODUÇÃO | 1 | B |
| 1.1 | Contexto | 1.1 (sem mudança de conteúdo; só remissão "seção 3.1" e "seção 2.2") | B |
| 1.2 | Problema e justificativa | 1.2 (troca de "água" por "escoamento superficial direto") | B |
| 1.3 | Objetivos (1.3.1 geral; 1.3.2 específicos) | 1.3 (troca de "água"; objetivo 5 reescrito, ver F) | B e F |
| 2 | FUNDAMENTAÇÃO TEÓRICA | 2 | E |
| 2.1 | Erosão hídrica em escala de evento | 2.1 (igual) | E |
| 2.2 | USLE e MUSLE | 2.2 (último parágrafo, sobre a IC, sai daqui e vai para 3.4.8) | E |
| 2.3 | Método SCS-CN | 2.3, parágrafos 1 a 5 e 7 (teoria: equações gerais, AMC, debate do λ, relação de Woodward como teoria, limites do método). Saem: frase "Na bacia estudada, o CN em AMC II varia..." (C16) e o parágrafo "Neste trabalho adotou-se λ = 0,05..." (C9) -> 3.4.1.3 | E |
| 2.4 | Escoamento direto e vazão de base | 2.4, 1º parágrafo, só a teoria (o que é cada componente, filtros, BFImax subjetivo). Sai "Neste trabalho, a série..." -> 3.2 | E |
| 2.5 | Medição de sedimentos em suspensão | Novo (C10), mais o 2º parágrafo da 2.4 (turbidez -> CSS). A frase "Neste trabalho, a carga total medida é atribuída..." vai para 3.4.4 | E (referências do item H) |
| 2.6 | MUSLE espacializada | 2.5, 1º parágrafo (Hao et al., 2022). O 2º parágrafo ("Neste trabalho, a formulação... coeficiente c") vai para 3.4.4 (C11) | E |
| 2.7 | Dados espaciais e interpolação da chuva | 2.6, só a teoria (raster, IDW, K e C por classe, LS a partir do MDE, CN de base nacional). O que é escolha do trabalho (Moore e Burch, limite de 200 m, ANA, CN-I) vai para 3.3 e 3.4.1 (C12) | E |
| 2.8 | Avaliação e validação de modelos | 2.7, sem equações (vão para 3.4.7, C13) e com "viés de otimismo" no lugar de "otimista" (C14). O 3º parágrafo, na parte aplicada ao trabalho (escolha do λ nos mesmos eventos), vai para 3.4.6 (C15); fica a teoria (viés de otimismo, LOO, validação cruzada aninhada) | E |
| 3 | MATERIAIS E MÉTODOS | 3 (título trocado, S11) | C |
| 3.1 | Área de estudo | 3.1 (igual) | B/C |
| 3.2 | Dados observados de vazão e descarga sólida de sedimentos em suspensão | 3.2 ("foi", S9 e S10) + a série de vazão de base (vinda da 2.4) + carga total. Tabela 3 perde as duas colunas do SCS-CN (resultado, vão para a 4.1) | B/C |
| 3.3 | Dados geoespaciais | 3.3 (S13) + K, C, LS (Moore e Burch, 200 m) e CN da ANA vindos da 2.6 | B/C |
| 3.4 | Espacialização da MUSLE | 4.1 (Visão geral, S14), com o fluxograma (Figura 4) | C |
| 3.4.1 | Preparação dos dados | 4.2 (S15) | C |
| 3.4.1.1 | Variáveis de cada evento e pixels de cálculo | 4.2.1 (S16) | C |
| 3.4.1.2 | Fatores K, C, LS e P | 4.2.2 | C |
| 3.4.1.3 | Número de curva, razão de abstração inicial e retenção S | 4.2.3 + 2.3 (C9, C16: CN da bacia, escolha de λ = 0,05 e conversão de Woodward) | C |
| 3.4.1.4 | Chuva espacializada | 4.2.4 + 2.6 (IDW) | C |
| 3.4.2 | Escoamento direto por pixel (SCS-CN) | 4.3 (S17) | C |
| 3.4.3 | Vazão de pico local e erosão local | 4.4 (S18), com o pico local e o E_unit explicados (pedido do Luis na reunião) | C |
| 3.4.4 | Sedimento do evento e versões do modelo (MC e MFM) | 4.5 (reescrita: SY = c * soma(E_unit,k), C17) + 2.5, 2º parágrafo (C11) + 2.4, frase da carga total | C |
| 3.4.5 | Calibração do coeficiente c | 4.6 | C |
| 3.4.6 | Validação cruzada | 4.7 + 2.7, 3º parágrafo (C15), com referência (C19) | C |
| 3.4.7 | Métricas de desempenho | 4.8 + 2.7 com as equações (C13) | C |
| 3.4.8 | Comparação com outros modelos de erosão | Novo (S19): modelo forçado (MFM), modelos simples, modelo concentrado da IC (2.2, último parágrafo); mesmas métricas | C |
| 3.4.9 | Mapas de erosão e áreas críticas | Novo (S19): sedimento médio, áreas críticas (5% dos pixels), contribuição por classe de uso, solo e declividade, R² com K*LS*C (C31) | C |
| 4 | RESULTADOS E DISCUSSÃO | 5 (S23) | D |
| 4.1 | Escoamento superficial direto | 5.1 (S20; C24: resultados do SCS-CN e gráfico calculado x medido) + 5.6.1 (chuva e escoamento por evento, C26) + colunas do SCS-CN da Tabela 3 | D |
| 4.2 | Resultados do Modelo Calculado de Erosão (MC) | 5.2 (S21, C23, C25) | D |
| 4.3 | Comparação do modelo calculado de erosão com outros modelos | 5.3 + 5.4 + 5.5, sem subitens (S22, C28, C29, S31), com as fontes de incerteza | D |
| 4.4 | Mapas de erosão por evento de chuva | 5.6 (S24 a S27); só o sedimento por evento (chuva e escoamento foram para 4.1) | D |
| 4.5 | Erosão média da bacia hidrográfica e áreas críticas | 5.6.2 (S28 a S30) + análise por declividade e R² (C31) + limitação da área urbana | D |
| 4.6 | Fontes de incerteza e limitações | Novo (proposta 5.7 de 29/10, reescrita com a reunião: defasagem do modelo) | D (decisão 1 abaixo) |
| 5 | CONCLUSÕES | 6 | F |
| - | REFERÊNCIAS | lista atual + novas lidas (item H) | H e K |
| Anexo 1 | Exemplo numérico: o evento 11 | 4.9 (C20), passo a passo em texto corrido; tabela só com resultados; imagens maiores | C (no fim do arquivo) |

Numeração de tabelas e figuras: ver item G (`mapa_figuras_tabelas_30-10.md`). Resumo: capítulo 3 com Tabelas 1 a 10 e Figuras 1 a 4; capítulo 4 com Tabelas 11 a 16 e Figuras 5 a 11; Anexo 1 com Tabela A1 e Figura A1 (ou Tabela 17 e Figura 12, se o Doc numerar em sequência).

---

## 2. Comentários e sugestões do Luis, um a um

| Nº | O que o Luis pediu | Como interpreto | Ação planejada | Onde |
|---|---|---|---|---|
| C9 | 2.3: o parágrafo da escolha de λ = 0,05 é material e métodos; na fundamentação só se expõe como funciona e quais os problemas | Tudo o que diz "neste trabalho" sai do capítulo 2 | Mover "Neste trabalho adotou-se λ = 0,05..." para 3.4.1.3; na 2.3 fica a teoria (relação de Woodward, faixa de validade, limites) sem dizer o que foi adotado | B (par de corte), C 3.4.1.3, E 2.3 |
| C10 | "Medição de sedimentos em suspensão" pode ser item separado, com teoria de medição e mais artigos de alta resolução temporal em eventos | Criar seção própria no capítulo 2 | Nova 2.5 "Medição de sedimentos em suspensão" (turbidez como substituto da CSS, curvas de calibração, incerteza, histerese, séries de alta frequência em eventos) com referências lidas no item H | E 2.5; H |
| C11 | 2.5, parágrafo "Neste trabalho, a formulação de Hao... coeficiente c" é materiais e métodos | Idem C9 | Mover para 3.4.4 (sedimento do evento), com a explicação do c como conectividade média | B, C 3.4.4, E 2.6 |
| C12 | 2.6 Dados espaciais em SIG: materiais e métodos | O que é escolha do trabalho vai para o 3; a teoria do raster/IDW/LS pode ficar curta no 2 | Mover IDW (3.4.1.4), K e C (3.3/3.4.1.2), LS de Moore e Burch com limite de 200 m (3.4.1.2), CN da ANA e CN-I (3.3/3.4.1.3). Deixar na 2.7 só teoria curta | B, C, E 2.7 |
| C13 | Colocar as equações dos estatísticos; resposta: a seção pode ficar em "métricas de desempenho", em materiais e métodos | Equações das métricas no capítulo 3 | 3.4.7 com equações de NSE, NSE em log, erro percentual absoluto mediano, fator 2, Spearman e viés de volume; no 2.8 só a teoria sem equações | C 3.4.7; E 2.8 |
| C14 | 2.7: trocar "otimista" por palavra mais técnica | "viés de otimismo" (optimism bias) é o termo da literatura de validação | Usar "estimativa enviesada para cima do desempenho (viés de otimismo)", com definição e referência lida (item H) | B, E 2.8 |
| C15 | 2.7, parágrafo do LOO e das escolhas feitas nos mesmos dados: pode ir para materiais e métodos | A aplicação ao trabalho vai para 3.4.6 | 3.4.6 explica o LOO aplicado e o que ele não corrige (escolhas de λ, CN-I e pesos dos postos feitas nos mesmos 17 eventos) | C 3.4.6 |
| C16 | 2.3: "Na bacia estudada, o CN em AMC II varia de 52 a 98..." é materiais e métodos | Idem | Mover para 3.3/3.4.1.3 | B, C |
| C17 | Equação SY = c1*soma + c2*(Qb*Tchuva*3600) mudou com os últimos ajustes? | Sim, é do modelo antigo | Trocar por SY = c * Σk E_unit,k e revisar toda a notação (índice k nos pixels, como no Doc) | C 3.4.4 |
| C18 | Corrigir as outras numerações em relação a "4.5" (visão geral) | Remissões internas com a numeração nova | Todas as remissões das propostas já usam a numeração nova; lista de troca no roteiro K | C, D, K |
| C19 | Procurar referência sobre a validação cruzada aninhada | Precisa de referência lida | Ler e citar (item H). No modelo oficial, com um só parâmetro, o LOO não é aninhado; a referência entra para explicar o que a validação aninhada faria (avaliar também as escolhas de λ, CN-I) e por que não foi feita (17 eventos) | H, C 3.4.6, E 2.8 |
| C20 | 4.9 (exemplo do evento 11) vira Anexo 1, imagens maiores, cálculo passo a passo em texto corrido, tabela só com resultados | Aceitar | Anexo 1 no fim de `proposta_cap3_30-10.md`; Tabela A1 só com resultados; Figura A1 em página inteira (ou dividida em duas) | C (Anexo 1), G |
| C21 | Capítulo 5 "com estrutura de IA"; melhorar de acordo com a reunião | Prosa corrida de relatório técnico, sem rótulos em negrito e listas | Capítulo 4 inteiro reescrito em parágrafos, com a discussão da reunião (defasagem do modelo, uso do mapa, área urbana) | D |
| C22 | Partes da tabela se sobrepõem; corrigir com o estado atual e com os termos de materiais e métodos | O comentário não mostra o trecho (vazio). Pela ordem dos comentários (entre C20, 14:15, e C23, 14:21), deve ser a Tabela 11 do Doc (sedimento por evento do MC, 7 colunas, com "Encostas" e "Base" do modelo antigo) ou a Tabela 10 (evento 11) | Refazer as duas: Tabela 12 nova (sedimento por evento, MC e MFM, sem "encostas/base", colunas estreitas, termos MC, MFM, validação cruzada) e Tabela A1 (evento 11 só com resultados). Também separar a Tabela 3 (tirar as colunas do SCS-CN) | D, G; pergunta no I |
| C23 | Explicar melhor os resultados do MC | Mais texto interpretativo: o que o número significa, por que o MC erra, em quais eventos | 4.2 com a leitura evento a evento, a ligação com o erro do escoamento (91% da variância), sinal do erro em 15 de 17 eventos, efeito do expoente | D 4.2 |
| C24 | 5.1: colocar o gráfico de vazão calculada x medida da reunião; "fala dos resultados do modelo SCS-CN" | 4.1 trata do SCS-CN | Figura 5 = `TCC_Texto/figuras/fig_volume_direto.png` (escoamento direto do SCS-CN contra o medido, por evento; é o único gráfico "calculado x medido" do modelo oficial no repositório). Suposição registrada; pergunta no I | D 4.1, G, I |
| C25 | Título "Resultados do Modelo Calculado de Erosão (MC)" | Aceitar | 4.2 com esse título | D |
| C26 | 5.6.1 (chuva e escoamento por evento) poderia ir para os resultados de escoamento direto | Concordo: a chuva e o escoamento por evento são resultado hidrológico; o sedimento por evento fica na 4.4 | Figuras de chuva e escoamento por evento na 4.1; sedimento por evento na 4.4 | D |
| C27 | Corrigir numerações (5.1) | Idem C18 | Numeração nova em tudo | D, K |
| C28 | 5.4 "O modelo de dois componentes e os testes simples": sem subtítulos | Aceitar; e o modelo de dois componentes não existe mais | 4.3 sem subitens | D |
| C29 | 5.5 "Comparação com a IC": sem subtítulos | Aceitar | Dentro da 4.3 | D |
| C30 | Trocar "água" por vazão ou escoamento superficial direto | Em todo o texto, quando "água" quer dizer o escoamento | Pares de troca no Resumo, Abstract ("water" -> "runoff"), 1.2, 1.3; nenhum "água" com esse sentido nas propostas novas. Ficam nomes próprios ("Agência Nacional de Águas", "estação de tratamento de água", "água bruta", "qualidade da água", "corpos d'água", "água subterrânea") | B; J confere |
| C31 | Explorar a correlação do mapa com K*LS*C; avaliar com R² para dizer que porcentagem se relaciona com K*LS*C e que porcentagem com outros fatores | Medir a parte da variação espacial do sedimento médio explicada pelos fatores fixos e a parte explicada pelo escoamento (chuva e CN) | Método em 3.4.9: R² entre ln(sedimento médio do pixel) e ln(K*LS*C); R² incremental ao acrescentar ln(Q médio do pixel); como, em log, ln(c*E) = constante + ln(K*LS*C) + 1,12*ln(Q) + termo do evento, a decomposição é quase exata em log; também em escala linear. Texto na 4.5 com "[a calcular no PC]" | C 3.4.9, D 4.5, K |
| S9, S10 | 3.2: "é" -> "foi" (duas vezes) | Aceitar | Já está no Doc como sugestão; aceitar no Doc | B |
| S11 | "ÁREA DE ESTUDO E DADOS" -> "MATERIAIS E MÉTODOS"; adicionar as partes da fundamentação | Aceitar | Título do capítulo 3; conteúdo movido conforme C9, C11, C12, C15, C16 | B, C |
| S12 | Título 3.2 com "de vazão e descarga sólida de sedimentos em suspensão" | Aceitar | Título já aparece assim no texto exportado; aceitar no Doc | B |
| S13 | "cartográficos" -> "geoespaciais" | Aceitar, também no texto da 3.3 ("Os dados cartográficos são...") e no título da Tabela 4 | B |
| S14 | "4. METODOLOGIA 4.1 Visão geral" -> "3.4. Espacialização da MUSLE" | Aceitar; o texto da visão geral fica como abertura da 3.4 | C 3.4 |
| S15 | 4.2 -> 3.4.1 | Aceitar | C |
| S16 | 4.2.1 -> 3.4.1.1; corrigir as outras numerações desta seção | Aceitar; 4.2.2 a 4.2.4 viram 3.4.1.2 a 3.4.1.4 | C |
| S17 | 4.3 -> 3.4.2 | Aceitar | C |
| S18 | 4.4 -> 3.4.3 | Aceitar | C |
| S19 | Novo item 3.4.x "Validação/Comparação de resultados com outros modelos de erosão" (modelo forçado, modelo simples, modelo da IC, mesmas métricas) e 3.4.x "Mapas de erosão e áreas críticas" | Aceitar | 3.4.8 e 3.4.9 | C |
| S20 | Título 5.1 -> "Escoamento superficial direto" | Aceitar | 4.1 | D |
| S21 | "de Erosão" no título do MC | Aceitar | 4.2 | D |
| S22 | 5.3 -> 4.x "Comparação do modelo calculado de erosão com outros modelos"; sem subitens; falar de cada modelo, gráficos, achados, fontes de incerteza | Aceitar | 4.3 | D |
| S23 | 5 -> 4 (RESULTADOS E DISCUSSÃO) | Aceitar | D |
| S24 a S27 | 5.6 -> 4.x "Mapas de erosão por evento de chuva"; excluir "5.6.1 Da chuva ao sedimento, evento a evento" | Aceitar | 4.4 | D |
| S28 a S30 | 5.6.2 -> 4.x "Erosão média da bacia hidrográfica e áreas críticas" | Aceitar | 4.5 | D |
| S31 | Excluir "5.4 O modelo de dois componentes e os testes simples" | Aceitar; nenhuma menção ao modelo de dois componentes | D |

Achados da revisão de 29/10 que entram junto (não são do Luis, mas mudam o texto): o alvo contém o volume medido (o bom desempenho do MFM mostra o peso do volume, não valida a fórmula de erosão); "não se distingue" no lugar de "equivalente"; RI/R descrito como "concentração temporal da chuva" e não como fração (passa de 1 nos eventos 1 e 12); o limite Q <= P no MFM; sensibilidade sem os eventos 15 e 17; eventos 1 e 12 abaixo de 25,4 mm.

---

## 3. Decisões que dependem do usuário ou do Luis

1. **Seção 4.6 "Fontes de incerteza e limitações".** O Luis pediu para lembrar das incertezas dentro da discussão (S22) e "falar bastante da defasagem do modelo". Proponho as duas coisas: incertezas citadas na 4.3 onde explicam um resultado, e uma 4.6 curta que reúne a cadeia de erros (da medição ao mapa). Se o Luis preferir sem 4.6, o texto da 4.6 se reparte entre 4.1 (chuva, eventos, SCS-CN, separação da base), 4.3 (alvo, IC) e 4.5 (K, C, área urbana).
2. **Anexo ou Apêndice.** O Luis escreveu "Anexo 1". Pela NBR 14724, material elaborado pelo próprio autor é "Apêndice"; "Anexo" é material de terceiros. Proponho "APÊNDICE A - Exemplo numérico: o evento 11" e deixo a pergunta no item I. O conteúdo é o mesmo.
3. **IC no texto.** A IC entra só com os valores originais (α 0,277; β 0,807; erro mediano absoluto 22,5%; 100% em fator 2; NSE log 0,91; NSE linear 0,83; Spearman 0,93; erro médio com sinal +4,2%; faixa -37% a +60%), ajustada nos próprios 17 eventos, sem validação cruzada, e com a ressalva de que a lista de eventos e o SY medido diferem. Consequência: não há comparação pareada (bootstrap, Wilcoxon) entre MFM e IC; a comparação é só lado a lado. Decisão já tomada pelo usuário; registrada aqui porque muda frases das propostas de 29/10 ("diferença de +6,1 pontos, IC95%..." sai).
4. **Tabela 3 dividida.** Proponho que a Tabela 3 (3.2) fique só com o medido e que as colunas do SCS-CN passem para uma tabela da 4.1 (é resultado). Alternativa: manter a Tabela 3 como está e só citá-la na 4.1.
5. **Qual gráfico de vazão calculada x medida** (C24): escolhi `fig_volume_direto.png`. Confirmar com o Luis.
6. **Qual tabela tem sobreposição** (C22): interpretei como a Tabela 11 do Doc (e, por precaução, a 10). Confirmar.
7. **Objetivo específico 5** (avaliar o quanto a estimativa do escoamento limita): proposta de redação nova em F, porque a parte "fórmula de erosão" não foi isolada (revisão de 29/10, achado 8).
8. **Padrão das chamadas ABNT** (maiúsculas dentro dos parênteses, como no Doc): mantive o padrão do Doc nas propostas.
9. **Números que só o PC calcula** (sem rasters na nuvem): R² do mapa com K*LS*C e incremental com o escoamento; contribuição por classe de declividade; volume perdido pelo limite Q <= P no MFM; fração do sedimento nos pixels com CN-I < 35. Ficam como "[a calcular no PC: ...]" nas propostas e listados no roteiro K.
