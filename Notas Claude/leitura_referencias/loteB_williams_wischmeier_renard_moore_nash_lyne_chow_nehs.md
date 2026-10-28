# Lote B: leitura das referências (MUSLE espacializada, Alto Jundiaí)

Escrito em 28/10/2026. Regras: nada foi alterado em C:\TCC. Onde não consegui o texto original, digo isso e nomeio a fonte secundária usada. Páginas do AH 537 são as impressas no livro (página do PDF menos 6).

Resumo rápido do nível de leitura:

| # | Referência | Nível de leitura |
|---|---|---|
| 1 | Williams (1975) | Não consegui acessar o original. Só fontes secundárias e o AH 537, que cita Williams. |
| 2 | Wischmeier e Smith (1978), AH 537 | Texto completo acessado (PDF escaneado com OCR, 67 páginas). Li os trechos relevantes, não o livro inteiro. |
| 2b | Wischmeier (1959) | Não consegui acessar. Só a referência bibliográfica e o que o AH 537 diz que ela contém. |
| 3 | Renard et al. (1997), AH 703 | Só resumo (registros de catálogo e do AGRIS). Texto não acessível. |
| 4 | Moore e Burch (1986) | Só resumo (via Crossref) mais fontes secundárias para a equação. |
| 5 | Nash e Sutcliffe (1970) | Não consegui acessar o texto. Só dados bibliográficos e fontes secundárias. |
| 6 | Lyne e Hollick (1979) | Não consegui acessar o original. Só fontes secundárias. |
| 7 | Chow, Maidment e Mays (1988) | Não consegui acessar o livro. Só fontes secundárias. |
| 8 | USDA-SCS (1972), NEH-4 | Não consegui acessar a edição de 1972. Li o capítulo 10 da edição de 2004 (NEH Parte 630, texto aberto) e uma fonte secundária que reproduz a tabela de AMC da edição antiga. |

---

## 1. WILLIAMS (1975), MUSLE

**Nível de leitura:** não consegui acessar o original (capítulo de anais, ARS-S-40, p. 244-252; não achei cópia aberta). Usei: (a) o AH 537 (Wischmeier e Smith, 1978), que cita Williams e eu li; (b) uma revisão de 2023 no arXiv (arXiv 2310.08430, lida em PDF); (c) o resumo de Smith, Williams, Menzel e Coleman (1984, J. Range Management 37(4):295-297, página de catálogo do Rangelands Gateway). Tudo o que está abaixo sobre a equação vem de (a), (b) e (c), não do original.

**O que é**
- Williams trocou o fator de erosividade da chuva (R) da USLE por um fator de energia do escoamento: o produto do volume escoado pelo pico de vazão. Isso permite estimar o sedimento de uma chuva só (evento) e, segundo o AH 537, dispensa a razão de entrega de sedimentos.
- Forma métrica: Y = 11,8 · (Q · qp)^0,56 · K · LS · C · P. Y é o sedimento do evento em toneladas métricas, Q é o volume escoado em m³ e qp é a vazão de pico em m³/s (Smith et al., 1984, no resumo do catálogo; a revisão do arXiv diz o mesmo).
- Segundo a revisão do arXiv (fonte secundária), os coeficientes foram ajustados com 778 eventos de 18 bacias pequenas, de 15 a 1.500 ha, com declividades de 0,9 a 5,9% e comprimentos de rampa de 78,64 a 173,74 m. Não consegui conferir isso no original.
- Existe também a forma em unidades americanas, com coeficiente 95, Q em acre-pé e qp em pés cúbicos por segundo. A diferença entre 11,8 e 95 é só o sistema de unidades.
- O AH 537 (p. 47) diz: "Williams (48) concluded that the need for a sediment delivery ratio could be eliminated by using the watershed runoff times peak rate as the storm R value in the USLE". Essa frase é uma confirmação direta, em texto que li, da ideia central de Williams. A referência 48 do AH 537 traz o título, ARS-S-40, p. 244-252.

**O que usamos no TCC**
- Seção 2.2 do rascunho 04: "Williams (1975) propôs substituir o fator de erosividade por um fator de energia do escoamento ... permite estimar a produção de sedimentos de um evento isolado". Isto está sustentado (AH 537, p. 47, e fontes secundárias).
- Seção 2.2: Y = 11,8 (Q·qp)^0,56 K LS C P, com Q em m³ e qp em m³/s. Sustentado só por fontes secundárias, que concordam entre si.
- Seção 2.2: "Os coeficientes 11,8 e 0,56 foram ajustados empiricamente por Williams em escala de bacia". Sustentado por fonte secundária (bacias de 15 a 1.500 ha).
- Seção 4.4 / Passo 7: E_unit = 11,8 · (Q·pr·A_pix)^0,56 · K · LS · C · P, "coeficientes originais mantidos" (seguindo Hao et al., 2022).

**Atenção**
1. Não li o original. Se o TCC for afirmar o número de eventos, a faixa de áreas ou de declividades, é preciso dizer que vem de fonte secundária, ou obter o ARS-S-40 em biblioteca. Hoje o TCC não afirma esses números (só "escala de bacia"), então não há problema agora.
2. Unidades no uso por pixel. A seção 4.4 diz "Q em mm, pr em m³/s e A_pix em m²". Na equação de Williams, Q é volume em m³. Q em mm vezes A_pix em m² dá 1.000 vezes o volume em m³. Como (1.000)^0,56 é cerca de 48, o índice por pixel fica cerca de 48 vezes maior do que ficaria com o volume em m³. A constante c absorve isso, então o resultado final não muda, mas a frase "coeficientes originais mantidos" vale para 11,8 e 0,56, não para as unidades. Vale escrever isso com clareza. Isto vem da leitura do texto do rascunho; não conferi o script.
3. Faixa de validade. As bacias de Williams, segundo a fonte secundária, tinham declividade de 0,9 a 5,9%. O Alto Jundiaí tem encostas mais íngremes (LS médio 7,80, chegando a cerca de 25). O TCC já diz que o pixel de 897 m² está fora da faixa, mas pode acrescentar a declividade. Só vale se o dado do original for conferido.
4. Unidade do K. A revisão do arXiv escreve K em t·ha·h/(ha·MJ·mm), mas Smith et al. (1984) não dão a unidade de K no resumo que li. Não consegui confirmar qual K o 11,8 pressupõe. Os K da IC (cerca de 0,03 a 0,04) têm a ordem de grandeza do K métrico. Como c é recalibrado, não afeta o resultado, mas convém não afirmar uma unidade sem conferir.
5. Fatores LS e C no pixel. Williams usava fatores de bacia inteira. A aplicação por pixel é de Hao et al. (2022), não de Williams.

---

## 2. WISCHMEIER e SMITH (1978), Agriculture Handbook 537

**Nível de leitura:** texto completo acessado (PDF escaneado com OCR, 67 páginas, copiado do repositório r-geospatial no GitHub; é o mesmo AH 537). Li os trechos sobre a equação, os fatores R, K, LS, C e P, a precisão, a razão de entrega e o apêndice métrico. Não li o livro inteiro (tabelas de C e de P, por exemplo, só de relance).

**O que é**
- A USLE é "um modelo de erosão feito para calcular perdas médias de longo prazo de solo por erosão em lâmina e em sulcos" (resumo, p. 3 do PDF). Não prevê deposição e não calcula sedimento de voçorocas, margens e leito.
- A = R · K · L · S · C · P (p. 3 impressa). A é a perda por unidade de área (normalmente t/acre/ano). Os fatores:
  - R: índice de erosividade da chuva (EI), em geral anual. EI de uma chuva = energia total da chuva (centenas de pés-tonelada por acre) vezes a intensidade máxima em 30 min (p. 4 a 6).
  - K: perda de solo por unidade de EI numa "parcela unitária" de 72,6 pés (22,1 m) de comprimento, 9% de declive, em pousio limpo. Calculado pelo nomograma (p. 8 a 11).
  - L e S: razão entre a perda da encosta e a da parcela de 22,1 m e 9%.
  - C: razão entre a perda com a cobertura e o manejo considerados e a do pousio limpo.
  - P: razão entre a perda com prática de suporte (plantio em contorno, terraços) e a do plantio morro abaixo.
- O livro avisa (p. 3, em tradução minha, não literal) que as equações atuais são bem menos precisas para prever eventos específicos do que médias de longo prazo. Na p. 47 repete: perdas de uma tempestade ou de um ano podem diferir muito da média de longo prazo. Diz também que a USLE é mais exata para encostas de menos de 400 pés (cerca de 122 m) e declives de 3 a 18%.
- O apêndice (p. 51 a 57) dá a conversão para unidades métricas, com K_métrico = 1,292 · K.
- As referências do livro incluem Wischmeier (1959), A rainfall erosion index..., SSSA Proceedings 23:246-249 (ref. 49), citada na p. 4 para a ideia de que a perda de uma tempestade em campo cultivado é proporcional ao EI.

**O que usamos no TCC**
- Seção 2.2: "A USLE (WISCHMEIER; SMITH, 1978) estima a perda média anual de solo pelo produto de seis fatores: erosividade, erodibilidade (K), comprimento e declividade (LS), cobertura e manejo (C) e práticas conservacionistas (P)". Sustentado pelo AH 537 (os seis fatores são R, K, L, S, C, P; o TCC os lista agrupando L e S em LS).
- Seção 4.2.2 e Tabela 5: K e C por classe (valores vindos da IC), P = 1,0 "porque não há práticas conservacionistas ativas". P = 1 é coerente com a definição do AH 537 (a razão fica em 1 quando não há prática de suporte).
- Seção 4.2.2: o LS "limitado a A_s de 200 m, o maior comprimento de rampa admitido pela equação". Ver Atenção 2.

**Atenção**
1. O AH 537 não traz os valores de K da IC nem os de C do TCC. K e C vêm da IC (Vivarelli et al., 2025), que tem sua própria fonte por classe. O AH 537 só define os fatores e dá métodos de cálculo (nomograma de K, tabelas de C). Para C = 0 na área urbana, C = 1 na mineração e K = 0 na área urbana (pendência 4 do resumo), o AH 537 não é a fonte: pelo texto que li, C é razão contra pousio limpo, e valores 0 ou 1 para urbano e mineração não são tabelados lá. Eu não procurei esses valores em todas as tabelas do livro, então só posso dizer que não os vi.
2. O limite de 200 m. Não achei no AH 537 nada que fixe 200 m como máximo da equação. O livro diz que a precisão é melhor abaixo de 400 pés (cerca de 122 m) e que a extrapolação aumenta o erro. O 200 m parece escolha do TCC (ou vem de outra fonte, como a RUSLE, que não li). Sugiro escrever como "adotamos 200 m", sem atribuir ao AH 537 ou à "equação".
3. Média anual. O AH 537 diz que a USLE é menos exata para eventos. Isso apoia o argumento do TCC de que a MUSLE (Williams) é a escolha para eventos. Pode ser citado na introdução.
4. A IC cita Wischmeier (1959) para a equação A = R·K·LS·C·P. Pelo que o AH 537 diz, o artigo de 1959 trata do índice de erosividade EI, não da equação de seis fatores. Eu não li o artigo de 1959. Para a equação completa, a referência certa é o AH 282 (1965) ou o AH 537 (1978). O rascunho 04 do TCC não cita Wischmeier (1959), só a IC e o arquivo `referencias_consolidadas.md`. Se for citar, use para o EI.
5. Unidade do K. O AH 537 dá K em unidades americanas (o exemplo do livro usa K = 0,32). Os K da IC, de 0,03 a 0,04, estão na faixa do K métrico (t·ha·h/(ha·MJ·mm)). O TCC não afirma unidade para K. Se afirmar, conferir.

### 2b. WISCHMEIER (1959), SSSA Proceedings 23(3):246-249

**Nível de leitura:** não consegui acessar o artigo. Só a referência bibliográfica (conferida no AH 537, ref. 49, que a cita como "A rainfall erosion index for a universal soil-loss equation") e o que o AH 537 diz que ela mostra.

**O que é (pelo AH 537):** é o artigo que propôs o EI (energia da chuva vezes intensidade máxima em 30 min) como medida da erosividade da chuva. Não li o conteúdo, então não afirmo detalhes dele.

**O que usamos no TCC:** nada no rascunho 04. A IC cita para a equação A = R·K·LS·C·P (ver Atenção 4 acima).

**Atenção:** a citação da IC parece desencontrada com o tema do artigo (EI). Confirme antes de reaproveitar.

---

## 3. RENARD et al. (1997), Agriculture Handbook 703 (RUSLE)

**Nível de leitura:** só resumo. Não achei o texto aberto. O PDF do site da ARS não carregou (erro de DNS) e o texto no archive.org exige login. Usei registros de catálogo (bibliotecas, AGRIS) e um resumo de base bibliográfica.

**O que é**
- É a revisão da USLE. Os registros dizem: o modelo estima a perda média anual de solo (A) causada por salpico de gota e escoamento em encostas de campo, em sistemas de cultivo e manejo definidos, e em pastagem. Mantém os seis fatores do AH 537; as mudanças são principalmente na forma de calcular os fatores e no uso de computador (bancos de dados de clima, culturas e operações agrícolas).
- É de janeiro de 1997, 384 páginas, e "substitui" o AH 537 (informação de catálogo).
- Autores listados: Renard, Foster, Weesies, McCool e Yoder.

**O que usamos no TCC:** nada no rascunho 04. Está no `referencias_consolidadas.md` e na IC (Relatório Final PIBIC, p. 2: "a equação RUSLE se baseia em perdas de solo anuais (Renard et al., 1997), a versão modificada estuda as perdas em eventos específicos de chuva (Williams, 1975)"). Na introdução do TCC, a frase é sustentada pelo resumo: a RUSLE estima perda média anual, não de evento. Isto está sustentado só no nível do resumo.

**Atenção**
1. Não li o texto: não posso afirmar detalhes (equações de L e S da RUSLE, valores de C, limites de comprimento de rampa). Se alguém quiser atribuir o limite de 200 m do LS à RUSLE, isso não está confirmado por mim.
2. A diferença USLE/RUSLE/MUSLE na IC é correta em termos gerais (anual versus evento), mas "MUSLE é versão da USLE" é uma simplificação: Williams não faz parte da família RUSLE. A RUSLE é a revisão do USDA-ARS de 1997, a MUSLE é de Williams (1975) e usa escoamento no lugar da erosividade.
3. Na prática, o AH 537 já basta para sustentar "USLE estima média anual e é pior para eventos". Citar Renard só se quiser nomear a RUSLE.

---

## 4. MOORE e BURCH (1986), SSSAJ 50(5):1294-1298

**Nível de leitura:** só resumo (obtido pelo Crossref; a página da Wiley deu 403). A equação em si não está no resumo. Para ela usei fontes secundárias (descrito abaixo).

**O que é**
- Os autores derivaram um fator comprimento-declividade fisicamente baseado, usando a teoria de potência de fluxo unitária (unit stream power) para o escoamento em lâmina e em sulcos, e mostraram que ele é equivalente ao fator empírico da USLE.
- Concluem que o fator da USLE mede a capacidade de transporte de sedimento do escoamento, mas não captura bem os processos hidrológicos. A versão física inclui convergência da bacia e formação de sulcos.
- (Resumo conforme a descrição do Crossref; a fonte é um resumo parafraseado, não o texto do artigo.)

**O que usamos no TCC**
- Seção 4.2.2 e Passo 7: LS = (A_s/22,13)^0,4 · (sen β/0,0896)^1,3, com A_s = área de contribuição específica (área a montante dividida pela largura da célula, em m) e β a declividade, sobre MDE em UTM, com A_s limitada a 200 m.
- Seção 2.4: "fator LS ... pela formulação de Moore e Burch (1986)".

**Atenção**
1. Não consegui conferir no original os expoentes 0,4 e 1,3. Uma fonte secundária que li (artigo de 2024 sobre Meghalaya, Índia, em Springer) escreve a mesma equação com m = 0,4 e n = 1,3, mas a atribui a Moore e Wilson (1992), que seria uma versão aprimorada da fórmula de Moore e Burch. Uma busca na web também aponta que Moore e Wilson (1992, J. Soil Water Conserv. 47(5):423-428) usam m = 0,4 e n = 1,3 e que outros trabalhos usam m = 0,6 (para transporte limitado). Há também formas com o fator multiplicador (m+1). Ou seja: a forma e os expoentes que o TCC usa são os de uso corrente em SIG, mas atribuí-los a "Moore e Burch (1986)" sem conferir pode estar impreciso. Sugestão: conferir o artigo de 1986 e, se os expoentes estiverem em Moore e Wilson (1992), citar os dois.
2. As constantes 22,13 m e 0,0896 são o comprimento e a declividade da parcela unitária da USLE (22,1 m e 9%; sen de 5,14° = 0,0896). Isso confere com o AH 537 (parcela unitária de 22,1 m e 9%, p. 3).
3. O LS do TCC é só da encosta (A_s limitada a 200 m). O artigo de Moore e Burch trata de convergência, que é justamente o que o limite de 200 m desliga nos pixels de canal. É uma decisão do TCC, bem justificada na seção 4.2.2, mas não é de Moore e Burch.

---

## 5. NASH e SUTCLIFFE (1970), J. Hydrology 10(3):282-290

**Nível de leitura:** não consegui acessar o texto. Conferi só os dados bibliográficos (Crossref: título "River flow forecasting through conceptual models Part I: A discussion of principles", autores J.E. Nash e J.V. Sutcliffe, vol. 10, n. 3, p. 282-290, abril de 1970, DOI 10.1016/0022-1694(70)90255-6; sem resumo). A definição abaixo vem da Wikipédia (fonte secundária).

**O que é (por fonte secundária)**
- NSE = 1 − [soma dos quadrados dos erros do modelo] / [soma dos quadrados dos desvios das observações em relação à média]. Vale 1 para ajuste perfeito, 0 quando o modelo é tão bom quanto a média das observações e negativo quando é pior.
- Por usar quadrados, é sensível a valores extremos. A Wikipédia cita Legates e McCabe (1999) como quem propôs uma versão com valores absolutos, e diz que muita gente aplica o logaritmo antes de calcular o NSE (para dar mais peso às vazões baixas).

**O que usamos no TCC**
- Seção 2.5 e Passo 10: definição do NSE (1 perfeito, 0 igual à média, negativo pior), a observação de que é dominado pelos eventos maiores, o NSE linear no Apêndice B (com e sem o evento 15) e o NSE em log como medida de apoio.

**Atenção**
1. O NSE em escala logarítmica não é de Nash e Sutcliffe (1970): é uma adaptação comum (fonte secundária). O TCC usa o NSE em log como medida de apoio e o descreve com palavras próprias. Não cite N&S como origem do log.
2. A frase "o NSE é dominado pelos eventos de maior magnitude" não está confirmada no original (não li). Em fonte secundária aparece como sensibilidade a extremos e é atribuída a trabalhos posteriores (Legates e McCabe, 1999). O TCC cita N&S logo depois de definir o NSE, o que é correto para a definição, mas a observação sobre sensibilidade pode pedir outra citação. Não verifiquei Legates e McCabe, só sei dele pela Wikipédia.
3. O artigo de 1970 trata de previsão de vazão em rios, e o TCC aplica o índice à carga de sedimentos por evento. É uma extensão comum, mas é extensão.

---

## 6. LYNE e HOLLICK (1979), filtro digital de vazão de base

**Nível de leitura:** não consegui acessar o original (anais de simpósio de Perth, p. 89-93, sem versão aberta). Só fontes secundárias: documentação do pacote R hydroTSM, documentação do pacote Python baseflowx e do pacote grwat (todas lidas por resultado de busca, e a baseflowx por leitura da página). As páginas de pacotes não são texto científico; servem para a forma da equação e para quem recomendou cada parâmetro.

**O que é (por fontes secundárias)**
- Filtro digital recursivo, vindo do processamento de sinais, que separa o escoamento rápido do escoamento de base. Forma original (em escoamento rápido f): f(t) = α·f(t−1) + [(1+α)/2]·[Q(t) − Q(t−1)]; a vazão de base é b = Q − f. Em termos da base: b(t) = α·b(t−1) + [(1−α)/2]·[Q(t) + Q(t−1)]. As duas formas são equivalentes (conferi a álgebra).
- Passa-se o filtro em vários sentidos (ida, volta, ida). Os parâmetros 0,925 e 3 passadas são recomendação de Nathan e McMahon (1990), não de Lyne e Hollick (1979). A documentação do baseflowx cita Zhang et al. (2017), que acharam duas passadas melhor.
- A documentação do hydroTSM diz que o 0,925 foi obtido por Nathan e McMahon (1990) e Arnold et al.; um artigo da HESS de 2025 mostra que α costuma ser recalibrado por bacia.
- O filtro de Eckhardt é outro tipo (parâmetros a e BFImax, baseado em reservatório linear), mais ligado à recessão. Segundo a baseflowx, Lyne-Hollick e Eckhardt pertencem a famílias diferentes, e o LH tem só um parâmetro de suavização sem ligação direta com a recessão.

**O que usamos no TCC**
- Seção 3.2 / 2.4 (rascunho 04, linhas 69 e 112): citam "os filtros digitais recursivos de Lyne e Hollick (1979) e de Eckhardt (2005)" como os mais usados. Na linha 112: o filtro de Lyne e Hollick (α = 0,925; três passadas) dá 47% de escoamento direto contra 53% de Bt, com correlação de 0,996 entre Bt e o filtro de LH por evento.
- Referência listada no TCC (p. 89-93, conferida em fonte secundária como proceedings do Inst. Eng. Aust.).

**Atenção**
1. A afirmação de que "o filtro de Lyne e Hollick com α 0,925 não reproduz a série de base do orientador, e só Eckhardt BFImax 0,70 reproduz" é um teste do TCC, não conteúdo de Lyne e Hollick. A citação de 1979 só sustenta que o filtro existe e como funciona. Ela não sustenta "α = 0,925" nem "3 passadas": isso é de Nathan e McMahon (1990), que o TCC não cita. Para os parâmetros usados no teste (0,925, 3 passadas), é preciso citar Nathan e McMahon (1990), ou dizer que são os valores padrão da literatura.
2. Como o TCC diz que o método de Bt "não está documentado na fonte" (linha 69) e depois mostra que Eckhardt com a = 0,995 e BFImax = 0,698 reproduz (linha 112), o parágrafo ainda tem o PENDENTE do rascunho. Isso é questão do TCC, não de LH.
3. A forma da equação vem de documentação de pacotes de software, não do artigo. Se o TCC escrever a equação do LH, é preciso conferir em Nathan e McMahon (1990) ou em livro (ex.: Brutsaert), que não li.

---

## 7. CHOW, MAIDMENT e MAYS (1988), Applied Hydrology

**Nível de leitura:** não consegui acessar o livro (nem trecho do Google Books). Fontes secundárias: um resultado de busca de exercício de hidrologia em italiano (skuola.net) e um slide de aula (Scribd), ambos vistos só como trechos de resultado de busca, que dão CN(I) = 4,2·CN(II)/(10 − 0,058·CN(II)) e CN(III) = 23·CN(II)/(10 + 0,13·CN(II)); e o artigo de Mishra et al. (2008, Water Resources Management 22:1409-1420, DOI 10.1007/s11269-007-9233-5), que compara fórmulas de conversão de AMC e inclui a de Chow et al. (1988) (só vi o resumo; o texto exigiu login de biblioteca, e não segui esse link). Não sei o capítulo e a equação em que aparece no livro (a busca sugere Cap. 5, Infiltração, mas não confirmei o número).
- Verificação numérica que eu mesmo fiz: comparei a fórmula com a Tabela 10-1 do NEH-630 cap. 10 (2004, texto aberto, que li). Para CN II = 90, a tabela dá CN I = 78 e CN III = 96, e a fórmula de Chow dá 79,1 e 95,4. Para CN II = 72, a tabela dá 53 e 86, e a fórmula dá 51,9 e 85,5. Para CN II = 52, a tabela dá 32 e 71, e a fórmula dá 31,3 e 71,4. Ou seja, nos três casos que conferi a fórmula concorda com a tabela do NRCS com diferença de cerca de 1 ponto de CN ou menos.

**O que é**
- Livro-texto de hidrologia aplicada. Traz o método SCS-CN (Q = (P − Ia)²/(P − Ia + S), com Ia = 0,2 S) e as fórmulas de conversão do CN entre as condições de umidade antecedente.

**O que usamos no TCC**
- Seção 2.3 e 4.2.3: CN_I = 4,2·CN_II/(10 − 0,058·CN_II). O TCC verificou que o raster da ANA, em AMC I e III, bate exatamente com essas fórmulas (o rascunho 04 diz que o resultado reproduz o raster em menos de 10⁻⁵). Essa verificação é do próprio TCC e é forte.
- Seção 2.3 e Passo 4: a equação SCS-CN, citada junto de USDA-SCS (1972).
- CN médio de 71,6 (AMC II) para 52,5 (AMC I).

**Atenção**
1. Não vi a página do livro. A fórmula está certa (concorda com fontes secundárias e com a tabela do NRCS 2004), mas o TCC deveria indicar o capítulo/equação conferindo no livro.
2. O CN_I do TCC vem da fórmula de conversão, e o TCC mesmo observa que o CN III fica "forte demais". O trabalho de Mishra et al. (2008), pelo que li do resumo, compara fórmulas e não aponta a de Chow como a melhor, mas não vi a classificação completa. Se o TCC quiser dizer que a conversão é aproximada, pode citar esse artigo, mas só depois de lê-lo.
3. A equação com λ geral (Q = (P − λS)²/(P + (1−λ)S)) do TCC é a mesma da NEH com Ia = λS: substituindo Ia = λS em (P−Ia)²/(P−Ia+S) dá exatamente a forma do TCC. Está correta.

---

## 8. USDA-SCS (1972), National Engineering Handbook, Section 4 (NEH-4)

**Nível de leitura:** a edição de 1972 não está acessível. Li (texto aberto, 79 páginas) o capítulo 10 da edição atual, NEH Parte 630 "Estimation of Direct Runoff from Storm Rainfall", de julho de 2004 (cópia no irrigationtoolbox.com), que é a versão revista do capítulo que Mockus escreveu em 1972. Para os limites de chuva de 5 dias do NEH-4 original, usei uma fonte secundária: Burke e Gray, "Antecedent Moisture Condition Probabilities for Selected Indiana Stations", Proceedings of the Indiana Academy of Science (li o PDF; o ano não consegui confirmar na cópia, mas as referências vão até 1982). Esse trabalho cita a tabela como "Mockus, V.J., 1972. Estimation of Direct Runoff from Storm Rainfall. Chapter 10 of SCS National Engineering Handbook, Section 4 — Hydrology".

**O que é**
- O NEH-4 é o manual do SCS (hoje NRCS) em que o método do número de curva foi publicado. O que o TCC usa dele está no capítulo 10 (não no capítulo 4, como a mensagem do pedido dizia; "Section 4" é o volume de Hidrologia, e a tabela de AMC, segundo Burke e Gray, está no Cap. 10).
- Equação (NEH-630 cap. 10, 2004, figura 10-2 e texto): Q = (P − Ia)²/(P − Ia + S), e, com Ia = 0,2 S, Q = (P − 0,2 S)²/(P + 0,8 S), com CN = 1000/(10 + S) em polegadas. Confere com o TCC: S = 25,4 · (1000/CN − 10) em mm.
- Condições de umidade antecedente (AMC, hoje chamadas ARC): I (seca), II (média) e III (úmida), pela chuva total dos 5 dias anteriores. Tabela de Burke e Gray (fonte secundária, atribuída ao SCS):

| Condição | Estação de crescimento (abr-out, no estudo de Indiana) | Estação dormente (nov-mar) |
|---|---|---|
| AMC I | menos de 1,4 pol | menos de 0,5 pol |
| AMC II | 1,4 a 2,1 pol | 0,5 a 1,1 pol |
| AMC III | mais de 2,1 pol | mais de 1,1 pol |

  Em milímetros: 1,4 pol = 35,6 mm; 2,1 pol = 53,3 mm; 0,5 pol = 12,7 mm; 1,1 pol = 27,9 mm. Os limites da estação de crescimento batem com os que o TCC usa (35,6 e 53,3 mm). Os de estação dormente, no TCC, produzem 3 eventos AMC I, 6 AMC II e 8 AMC III; não recalculei.

**O que usamos no TCC**
- Passo 4 e seção 2.3: a equação SCS-CN (USDA-SCS, 1972; CHOW; MAIDMENT; MAYS, 1988). Sustentado (NEH-630 cap. 10 mostra a mesma equação).
- Passo 2 e §31: "pelo critério da chuva antecedente de 5 dias do NEH-4, 13 dos 17 eventos se enquadram em AMC I" (estação de crescimento, AMC I abaixo de 35,6 mm). Os limites numéricos conferem com a tabela da fonte secundária. Não conferi no original de 1972.

**Atenção (o mais importante deste lote)**
1. O próprio NRCS deixou de usar o critério dos 5 dias. O NEH-630 cap. 10 (2004), p. 10-5 a 10-7, explica que a variação do CN é atribuída à condição antecedente, que antes era medida pela chuva dos 5 dias anteriores, e que isso foi usado nas primeiras edições do NEH Seção 4. Mostra uma bacia (Treynor, Iowa) em que não aparece relação entre a chuva antecedente e S, diz que isso é típico de bacias onde predomina escoamento superficial e cita vários estudos (Cronshey 1983; Hjelmfelt et al. 1982, 1987, 1991; Van Mullem 1992) que chegam à mesma conclusão: não há relação aparente entre chuva antecedente e número de curva. A alternativa que o manual atual apresenta é tratar o CN como variável aleatória. Isso confirma o alerta que já estava em §31 (versões posteriores reinterpretam a condição antecedente: conferir antes de citar). Está conferido: o manual atual do NRCS não usa mais a regra dos 5 dias como método. Isso combina com o dado do TCC (P5 e coeficiente de escoamento têm correlação de só 0,37, §31). Recomendo no texto dizer "critério histórico do NEH-4" e não "o método manda", e dizer que o NEH-630 (2004) abandonou esse critério. O argumento que fica de pé é o de que o CN-I reproduz melhor o volume medido (§31, viés +3%), com o NEH-4 como apoio histórico e não como prova.
2. Estação dormente e de crescimento no Brasil. Os limites vêm de um critério por estação de vegetação ativa. Não confirmei na edição de 1972 como as estações são definidas. A fonte secundária usa datas de Indiana (abr-out e nov-mar) como definição operacional dos autores. O TCC considera todo o período chuvoso (nov-mar) como estação de crescimento, o que é razoável, mas não está sustentado por uma definição no NEH-4 que eu tenha lido. Se usasse os limites de estação dormente, daria 3 / 6 / 8 eventos (o próprio §31 mostra), o que mudaria a conclusão "13 de 17 em AMC I".
3. A tabela vem de dados de um local dos EUA. Fonte secundária (artigo do J. Hydrologic Eng.) diz que os dados da tabela AMC do NEH-4 vêm de local não especificado nos EUA e valeriam originalmente como exemplo de parcela. Não confirmei no original.
4. No NEH-630 (2004), o CN para AMC I e III está tabelado (Tabela 10-1) como envoltórias de 10% e 90%, não como "umidade" medida. Isso reforça que "AMC I" é uma condição estatística de CN baixo e não necessariamente de solo seco.
5. A citação no texto está certa em indicar "NEH-4", mas a página/capítulo (Cap. 10) deve ser indicada. A referência completa pode ser: MOCKUS, V. J. Estimation of direct runoff from storm rainfall. In: USDA-SCS. National Engineering Handbook, Section 4: Hydrology. Washington, DC: USDA-SCS, 1972. cap. 10. (A fonte secundária cita o capítulo assim; não pude conferir no original.)
