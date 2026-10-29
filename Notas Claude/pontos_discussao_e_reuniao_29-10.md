# Pontos para a Discussão (5.7) e para a reunião com o Luis (anotado em 29/10/2026)

Pedido do usuário (ditado por voz, 29/10): na Discussão, listar as **fontes de erro desde o começo da cadeia**, incluindo:

1. **Delimitação manual dos eventos.** Os eventos foram delimitados à mão; isso pode fazer a chuva usada (R e RI) não coincidir exatamente com a chuva do evento (início e fim do evento, chuva que cai antes ou depois do recorte, evento 1 x 1B). Ligar a: origem da coluna `Chuva_evento_mm` (pesos 0,307/0,693 do IDW são ajuste por mínimos quadrados, resíduo de até 0,57 mm), RI/R > 1 nos eventos 1 e 12, exclusão do evento de 24/11/2018 (1B).
2. **Filtro de Eckhardt** para separar escoamento direto e vazão de base: escolha de α (0,995) e BFImax (0,70 reproduz a série do orientador; o cabeçalho da planilha dele diz 0,58), e a hipótese de que a base não carrega sedimento além da mesma concentração da mistura. Já existe um parágrafo curto na 5.7 ("Vazão de base e alvo"); ampliar.
3. **Apoiar cada fonte de erro nos artigos que o usuário passou** (ditado como "artísticas"; ele esclareceu: "os artigos"). Já lidos e aproveitáveis (lotes A a D):
   - Baert et al. (2026): o início do escoamento é incerteza central; erros de volume e pico são amplificados pelo termo (Q*qp)^0,56; um λ fixo mais baixo não resolve. Com volume e pico medidos a MUSLE chega a NSE 0,66 (apoia "o gargalo é a água").
   - Eckhardt (2005; forma lida em Eckhardt 2012): BFImax não é mensurável, é elemento subjetivo. Brandão et al. (2025) e Valle Junior et al. (2019) usam o filtro (Valle com BFImax 0,80 e parâmetro 0,98, diário), mas nenhum justifica o 0,70. Collischonn e Fan (2013) para a calibração.
   - Murillo-Bermúdez et al. (2023) e a Tabela 1 de 2022: turbidez convertida em CSS por curva; CSS máximo de 4.602 mg/L corresponde a ~9.000 NTU, acima dos 250 NTU em que a regressão por partes muda (extrapolação, incerteza da carga medida). CSSmax da planilha bate com o artigo em 15 de 17 eventos (diferem os eventos 6 e 15); durações diferem 1 a 2 h por evento (janelas definidas de outro modo).
   - Hao et al. (2022): SY_obs é a integral de Q*c; não discute delimitação de eventos nem separa a base.
   - Nenhum artigo lido trata especificamente da delimitação manual de eventos: esse ponto fica como limitação própria, sem citação.
   - Se houver outros artigos que ele passou e que não estão nos lotes A a D, ele deve indicar quais (a sessão ainda não os leu).

Já cobertas na proposta (`proposta_secao5.md`, 5.7): erro do volume do SCS-CN (91% da variância do MC), concentração por m³ (3,5 vezes) e contraste 2018/19 x 2019/20, evento 17, λ e conversão de Woodward, condição de umidade, escolhas avaliadas nos mesmos eventos, alvo, K e C, espaço.

Sugestão de forma: uma lista/tabela "fonte de erro, onde entra na cadeia, efeito conhecido, como foi tratado", da medição (turbidez-CSS, chuva) até o mapa, antes dos parágrafos atuais.

Para levar à reunião: pontos 1 e 2 acima, mais as 4 perguntas do fim de `instrucoes_sessao_desktop.md` e o achado crítico da revisão (o alvo contém o volume medido).

## IC publicada, calculada da planilha do Drive (29/10/2026)

Fonte: Drive, pasta do TCC, "Cópia de Tabela Resumo" (abas "CLP Eventos", "CLP Calibração", "CLP Resultados Calibrados", "J ..."). α 0,277 e β 0,807 sobre 17 eventos (Y_obs e Y_sim da própria planilha). Convenção da planilha: erro = (obs - sim)/obs, então -4,15% significa simulado acima do observado.

- Erro médio com sinal: 4,15% (sim acima do obs); erro médio absoluto 22,3%; **erro mediano absoluto 22,5%**; faixa de -37,1% a +60,0% (sim contra obs).
- Fator 2: 17 de 17. NSE linear 0,83; NSE em log 0,91. Ajuste e avaliação nos mesmos 17 eventos (sem validação cruzada).
- **Atenção para comparar com o MFM (20,6%):** os SY_obs da planilha da IC diferem dos do TCC (`comparacao_SY_lambda005_woodward.csv`) em vários eventos (ex.: evento 12: 129,3 contra 210,7 t; 17: 1.455,7 contra 1.709,6 t; 15: 3.972,9 contra 3.828,8 t). O alvo e a lista de eventos não são os mesmos. Alinhar pelas datas antes de afirmar qualquer comparação direta. IC: evento 2 = 24/11/2018 (TCC usa 17/12/2018).
- A IC usa volume de escoamento "superficial" total do evento e pico medidos (ex.: evento 1: 409.024,8 m3, pico 10,3 m3/s).

## Decisões do usuário em 29/10/2026 (aplicar no Doc antes das seções 4 a 6)

D: cortar as duas frases da 2.3, manter só o viés de +3%. A: Resumo/Abstract citam apenas a IC publicada. B: trocar "permite direcionar" por "indica, em termos relativos, onde priorizar medidas de contenção, sob os valores de K e C adotados" (Resumo e 1.2). C: ajustar 1.2 e 1.3 já (a água limita; a parte da erosão não foi isolada). E/F: versão provisória (frase na 3.3 com as duas áreas; Tabela 2 sem "Q inicial" e "T chuva"). J: manter as citações diretas; acrescentar NRCS (2004) à lista. G, H, I: aplicar. K, L: aplicar (Fonte em Tabelas 5 e 6, "razão de abstração inicial", "Fonte:" nas legendas, padrão ABNT das chamadas, referências corrigidas); M (divisão de parágrafos): não aplicar.

## Aplicado no Google Doc em 29/10/2026 (revisão do Doc depois da revisão independente)

Resumo/Abstract (comparação com a IC publicada, erro mediano 22%, "razão" de abstração inicial, mapa relativo), 1.2 e 1.3 (objetivo geral e 5: a água, não "o fator"), 2.3 (cortadas as frases de método descartado, Valle Junior com três autores, USDA-SCS como UNITED STATES), 2.5 (frase da razão de entrega), Tabela 1 (Bt: série fornecida, reproduzida pelo filtro), Tabela 2 (sem Q inicial e T chuva; larguras refeitas), Tabela 4 (LS: área de contribuição específica limitada a 200 m), 3.3 (frase da área 138,1 contra 137,8 km² e frase de K e C adotados da IC), Tabelas 5 e 6 (coluna Fonte "com base em"), "Fonte:" abaixo das Figuras 1 a 3 e das Tabelas 1 a 6, legenda da Tabela 6 sem negrito, 9 referências novas (Castro, Chagas, Corrêa, Demarchi, Martins, Rocha Lima, Silva A. M., Silva B. P. C., Silva L. C. N., Silva T. S.) e USDA-SCS pela jurisdição.

Pendente: origem da `Chuva_evento_mm` (Tabela 2, R); explicação real da diferença de áreas (conferir no PC); NRCS (2004) entra na lista quando as seções 4 a 6 citarem; Vivarelli et al. (2025) sem indicação de onde está disponível; Silva T. S. (2016) sem "Acesso em" porque a dissertação não abriu; notação com índice k e demais ajustes da seção 4 em diante vão com a reescrita das seções 4 a 6; comparação 21% x 22%: alvo e lista de eventos da IC diferem dos do TCC (ver acima).

## Orientações do Luis, ditadas pelo usuário (29/10/2026) para a Discussão e a seção do mapa

1. **Falar bastante da defasagem do modelo (por que erra).** Dificuldades de transformar chuva em vazão: (a) a delimitação dos eventos foi manual (o Luis olhou o hidrograma e recortou início e fim), o que já gera erro grande; (b) só dois postos de chuva; (c) a incerteza do próprio método SCS-CN, que já tem erro grande. "Forçar bastante nesse ponto." (Ligar às fontes de erro da seção acima: Baert et al. 2026, Eckhardt, curva turbidez-CSS, RI/R, `Chuva_evento_mm`.)
2. **Explorar bastante a espacialização do mapa:** onde houve mais erosão e onde não houve, por tipo de solo, por inclinação do terreno e por uso do solo. Isso recupera o sentido do mapa ("para que serve?": atacar as áreas de maior erosão). Já existem Tabelas 13 e 14 (uso e solo) na proposta da 5.6; **falta a análise por declividade/LS** (precisa dos rasters, no PC) e a leitura conjunta (solo x uso x declividade nas manchas críticas).
3. **Limitações do projeto a declarar:** a área urbana tem erosão nula (K = 0, C = 0), mas existe erosão urbana (obras, vias de terra, solo exposto). O mapa de uso classificou toda a mancha urbana como superfície impermeável; com um mapa de maior resolução seria possível separar, por exemplo, parques (que seriam como silvicultura ou mata nativa), rios e solo exposto urbano. Pode entrar no texto (5.7 "Espaço" e/ou 3.3) como sugestão de trabalho futuro (6).
4. O usuário ainda pode lembrar de mais pontos: acrescentar aqui.

Obs.: o Resumo e a 1.2 já dizem que o mapa é relativo e não validado no espaço; a pergunta do Luis ("para que serve o mapa?") responde-se na 5.6 com a priorização de áreas e classes.

## Luis pediu: explicar melhor o Qpico (pr) e por que o E_unit não vem em toneladas (29/10/2026)

Resposta preparada (para a 4.4 e a 4.5; ainda não aplicada no Doc):
- pr = (Q/1000)*A_pix*(RI/R)/3600 em m3/s. RI/R é um número único por evento, e não há roteamento; logo pr é proporcional a Q em todos os pixels, e E_unit = 11,8*(Q*pr*A)^0,56*K*C*LS é proporcional a Q^1,12. O "pico local" não acrescenta informação espacial além do escoamento Q; só altera o expoente e o efeito do evento (RI/R).
- E_unit não é massa porque a fórmula de Williams foi ajustada para bacias inteiras (volume em m3, pico em m3/s, resultado em t) e aqui é aplicada a pixels de 897 m2, com Q em mm. A fórmula é côncava (expoente 0,56): a soma dos valores dos pixels não é igual ao valor da bacia (para n pixels iguais a razão é n^0,12). Constantes de escala e unidade ficam todas no coeficiente c (t por unidade de E_unit).
- O que compensa a falta do índice de conectividade de Hao et al. (2022) é o coeficiente c (minúsculo, de escala), não o fator C do uso do solo. Mas c é um número único para toda a bacia: representa uma conectividade média, não a variação entre pixels. O mapa mostra, portanto, onde se produz erosão local, não onde o sedimento realmente chega ao rio.

## IC: só valores originais (29/10/2026, pedido do usuário)
Figuras `fig_dispersao.png` (painel da IC) e `escada_gargalo.png` (N3: MFM contra IC original) regeneradas com `Scripts/_ic_original.py`. Falta trocar a "IC refeita" em: `Scripts/gerar_tabelas_tcc.py` (coluna IC de tab_resultados, linha "IC refeita" de tab_parametros), `proposta_secao5.md` (5.5, Tabela 12, Spearman 0,93 da IC refeita), `mapa_figuras_tabelas_secoes_4_a_6.md`, `Planilhas/planilha_calculos_concentrados.xlsx` (aba ic) e `resumo_modelo_completo.md`. Métricas originais: MedAPE 22,5%; fator 2 100%; NSE log 0,91; NSE linear 0,83; Spearman 0,93; erro médio com sinal +4,2% (simulado acima), faixa -37% a +60%.

## Comentários do Luis no Doc (29/10/2026, 13:58 a 14:08 UTC): 9 comentários e 9 sugestões de edição
Não aplicar nada no Doc enquanto ele estiver revisando. Quando ele terminar: ler com `commentsIncluded`, listar um a um e propor. Temas já vistos: levar definições e equações das métricas estatísticas para "Materiais e métodos"; usar palavra mais técnica em um trecho; item separado com teoria; conferir se a equação mudou com os últimos ajustes.
