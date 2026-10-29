# Ajustes no texto existente do Doc: Resumo, Abstract e capítulos 1 a 3 (30/10/2026)

Sessão na nuvem, sem acesso ao Doc. Base: `doc_texto_completo_29-10b.md` (exportação de 29/10, revisão AHj4eM...). **Nada foi aplicado no Doc.**

Como usar: cada item traz o **trecho atual** (cópia exata do texto exportado, para usar em "Localizar") e o **trecho novo**. Onde o trecho novo é "(apagar)", o trecho sai. Onde o trecho sai do capítulo 2 para o 3, o destino está indicado e o texto final está nas propostas `proposta_cap3_30-10.md` (C) e `proposta_cap2_30-10.md` (E).

Atenção na busca: o texto exportado traz as sugestões abertas do Luis já misturadas (por exemplo "foié", "geoespaciaiscartográficos"). Os itens 0.x dizem para **aceitar** essas sugestões no próprio Doc antes de buscar os outros trechos.

---

## 0. Aceitar no Doc as sugestões do Luis (S9 a S13)

- 0.1 (S9, S10) 3.2: aceitar as duas trocas "é" -> "foi" ("A vazão foi registrada...", "a turbidez foi medida...").
- 0.2 (S11) Título do capítulo 3: aceitar "3. MATERIAIS E MÉTODOS".
- 0.3 (S12) Título da 3.2: aceitar "3.2 Dados observados de vazão e descarga sólida de sedimentos em suspensão".
- 0.4 (S13) Título da 3.3: aceitar "3.3 Dados geoespaciais".
- 0.5 (S14 a S18) Títulos 3.4, 3.4.1, 3.4.1.1, 3.4.2, 3.4.3: aceitar; em seguida substituir o bloco inteiro "4. METODOLOGIA" até o fim de "4.9" pelo texto de `proposta_cap3_30-10.md` (3.4 em diante) e do Apêndice/Anexo.
- 0.6 (S19 a S31) Capítulo de resultados: aceitar e depois substituir pelo texto de `proposta_cap4_30-10.md`.

---

## 1. Resumo

1.1 (C30, "água")
- Atual: "Com a água medida, o erro mediano da espacialização (21%) é da mesma ordem que o da formulação concentrada da Iniciação Científica anterior (22%, ajustada sem validação cruzada)"
- Novo: "Com o escoamento superficial direto medido, o erro mediano da espacialização (21%) é da mesma ordem que o da formulação concentrada da Iniciação Científica anterior (22%, ajustada nos próprios eventos, sem validação cruzada, e com lista de eventos e carga medida que não coincidem inteiramente com as deste trabalho)"
- Observação: se ficar longo para o Resumo, usar só "(22%, ajustada nos próprios eventos, sem validação cruzada)". A ressalva das listas diferentes vai obrigatoriamente na 4.3.

1.2 (consistência com a 3.4.3, que agora explica o pico local)
- Sem mudança. Conferido: o Resumo não tem outras ocorrências de "água" no sentido de escoamento.

## 2. Abstract

2.1 (C30)
- Atual: "With measured water, the median error of the spatialized model (21%)"
- Novo: "With measured direct runoff, the median error of the spatialized model (21%)"

2.2 (paralelo ao 1.1)
- Atual: "(22%, fitted without cross-validation)"
- Novo: "(22%, fitted to its own events without cross-validation)"

---

## 3. Capítulo 1

3.1 (1.2, C30)
- Atual: "Um modelo em células também permite comparar o desempenho com a água calculada e com a água forçada ao valor medido, e assim verificar quanto a qualidade das estimativas depende da estimativa da água (chuva transformada em escoamento)."
- Novo: "Um modelo em células também permite comparar o desempenho com o escoamento superficial direto calculado a partir da chuva e com o escoamento direto forçado ao valor medido, e assim verificar quanto a qualidade das estimativas depende da transformação da chuva em escoamento."

3.2 (1.2, C30)
- Atual: "verificar quanto a estimativa da água limita a qualidade das estimativas. Como só há medição"
- Novo: "verificar quanto a estimativa do escoamento superficial direto limita a qualidade das estimativas. Como só há medição"

3.3 (1.3.1, C30)
- Atual: "e avaliar o quanto a estimativa da água limita a qualidade das estimativas."
- Novo: "e avaliar o quanto a estimativa do escoamento superficial direto limita a qualidade das estimativas."

3.4 (1.3.2, objetivo 1; precisão)
- Atual: "Espacializar o escoamento superficial de cada um dos 17 eventos"
- Novo: "Espacializar o escoamento superficial direto de cada um dos 17 eventos"

3.5 (1.3.2, objetivo 5, C30)
- Atual: "comparando o modelo com a água calculada e com a água forçada ao valor medido;"
- Novo: "comparando o modelo com o escoamento superficial direto calculado e com o escoamento direto forçado ao valor medido;"

3.6 (1.3.2, objetivo 4; honestidade do resultado, revisão de 29/10, achado 18)
- Atual: "para verificar se a espacialização custa precisão;"
- Novo: "para verificar se a espacialização perde precisão em relação a eles;"

As ocorrências "qualidade da água" e "cursos d'água" (1.1) ficam: não se referem ao escoamento.

---

## 4. Capítulo 2 (o que sai, o que muda; texto final do capítulo em E)

4.1 (2.2, último parágrafo; correção de fato e preparação da 3.4.8)
- Atual: "aplicou a forma concentrada da equação (volume e pico medidos, fatores médios da bacia) e ajustou os coeficientes aos dados de campo, obtendo um modelo capaz de reproduzir o sedimento de 17 eventos, mas que não indica onde a erosão ocorre."
- Novo: "aplicou a forma concentrada da equação (volume e pico medidos, fatores médios da bacia) e ajustou o coeficiente e o expoente por regressão aos dados de 17 eventos, obtendo um modelo capaz de reproduzir o sedimento desses eventos, mas que não indica onde a erosão ocorre."
- Fonte: IC publicada (α 0,277 e β 0,807 por regressão; lote C e `revisao_processo_29-10.md` R3.1). O relatório PIBIC diz que o ajuste da bacia inteira foi forçado ao intervalo da literatura; o artigo dá a regressão. Usei a forma do artigo, que é a que o TCC cita.

4.2 (2.3, C16: sai para 3.4.1.3)
- Atual: "Na bacia estudada, o CN em AMC II varia de 52 a 98 (média 71,6), resultando em valores de 31 a 95 em AMC I, cenário adotado neste trabalho."
- Novo: (apagar). Destino: 3.4.1.3.

4.3 (2.3, unidades da relação de Woodward: tirar o "foi aplicada", que é método)
- Atual: "No cálculo, com S em milímetros, a relação foi aplicada na forma:"
- Novo: "Com S em milímetros, a mesma relação se escreve:"

4.4 (2.3, C9: sai para 3.4.1.3; fica a teoria sobre a faixa de validade)
- Atual: "Neste trabalho adotou-se λ = 0,05 com S convertido por essa relação, porque com ela o volume calculado no conjunto dos eventos ficou próximo do escoamento direto medido (viés de +3%). A relação é uma regressão entre valores de S ajustados a bacias norte-americanas, para chuvas de pelo menos 25,4 mm. Na bacia estudada, 8,4% dos pixels têm CN em AMC I abaixo de 35, fora da faixa tabelada pelos autores, o que é extrapolação. A escolha foi feita observando os mesmos 17 eventos, e isso é discutido nas limitações."
- Novo: "A relação é uma regressão entre valores de S ajustados a bacias norte-americanas, com chuvas de pelo menos 25,4 mm, e a tabela dos autores cobre números de curva de 35 a 100; fora dessas faixas, o seu uso é extrapolação."
- Destino do restante: 3.4.1.3 (escolha e viés de +3%) e 4.6 (8,4% dos pixels; escolha nos mesmos eventos).
- Conferir no PC: a faixa "35 a 100" vem da proposta 5.7 de 29/10 ("faixa da Tabela 4 de Woodward et al., 2003"), que cita o manuscrito lido no lote A. Não reabri o PDF nesta sessão.

4.5 (2.4, título; C10: a medição de sedimentos vira a 2.5)
- Atual: "2.4 Escoamento direto, vazão de base e medição de sedimentos em suspensão"
- Novo: "2.4 Escoamento direto e vazão de base"

4.6 (2.4, o que é dado do trabalho vai para 3.2)
- Atual: "Neste trabalho, a série de vazão de base foi fornecida junto com os dados de monitoramento. Ela é reproduzida pelo filtro de Eckhardt com a = 0,995 (passo horário) e BFImax = 0,70, com diferença mediana de 0,002 m³/s; outros valores de BFImax e o filtro de Lyne e Hollick não a reproduzem. A série serve para obter o escoamento direto medido, usado no modelo forçado ao medido."
- Novo: "Como o BFImax não é mensurável, a vazão de base obtida por filtro é uma estimativa, e o escoamento direto obtido pela diferença entre a vazão total e a de base herda essa incerteza."
- Destino do restante: 3.2.
- Leitura: "BFImax não é mensurável, elemento subjetivo" é de Eckhardt (2012, texto completo; lote A); Eckhardt (2005) só pelo resumo. A frase nova não leva citação (é consequência direta da frase anterior do Doc); se quiser citação, usar "(ECKHARDT, 2005)" com a ressalva de leitura, ou acrescentar Eckhardt (2012) à lista.

4.7 (2.4, 2º parágrafo; C10: vai para a nova 2.5)
- Atual: "A carga de sedimentos em suspensão é estimada, em estações automatizadas, a partir da turbidez, convertida em concentração de sedimentos em suspensão (CSS) por curvas de calibração (MURILLO-BERMÚDEZ et al., 2023). A CSS é, portanto, uma estimativa, e não uma medida direta. Integrando o produto Q * CSS sobre o tempo, obtém-se a carga do evento, que inclui o sedimento carreado pela vazão de base. Neste trabalho, a carga total medida é atribuída ao escoamento superficial, que mobiliza o sedimento nas encostas; a vazão de base é tratada apenas como a água que o transporta."
- Novo: (apagar daqui). As três primeiras frases entram, reescritas, na 2.5 nova (E). A última frase vai para 3.4.4 (C), sem "água": "a vazão de base é tratada apenas como meio de transporte".

4.8 (2.5 vira 2.6; C11: 2º parágrafo sai)
- Atual (título): "2.5 MUSLE espacializada" -> Novo: "2.6 MUSLE espacializada"
- Atual: "Neste trabalho, a formulação de Hao et al. (2022) é usada sem a conectividade: a soma da erosão dos pixels é multiplicada por um único coeficiente de escala, calibrado contra o sedimento medido no exutório. Na escala da bacia, a MUSLE dispensa a razão de entrega (seção 2.2); aplicada ao pixel, estima a erosão local, e a parte que chega ao exutório precisa de um fator, aqui o coeficiente c. Esse coeficiente faz o papel de uma conectividade média da bacia e absorve também a diferença de escala entre a equação de Williams, ajustada em bacias, e o pixel."
- Novo: (apagar). Destino: 3.4.4.

4.9 (2.6 vira 2.7; C12: o parágrafo inteiro é substituído pela versão teórica de E)
- Atual (título): "2.6 Dados espaciais em SIG" -> Novo: "2.7 Dados espaciais e interpolação da chuva"
- Atual (parágrafo inteiro, começa em): "Os fatores da MUSLE são espacializados em formato raster, com a mesma grade da chuva e do CN." e termina em "O mapa de solos usado pela ANA tem escala 1:250.000, mais grosseira que a grade de 30 m."
- Novo: texto da 2.7 em `proposta_cap2_30-10.md`. O que é escolha do trabalho (Moore e Burch, limite de 200 m, ANA, CN-I, mapa de 1:250.000) vai para 3.3 e 3.4.1.2.

4.10 (2.7 vira 2.8; C13, C14, C15)
- Atual (título): "2.7 Avaliação e validação de modelos" -> Novo: "2.8 Avaliação e validação de modelos"
- Atual: "Parâmetros ajustados aos mesmos dados que se usam para avaliar o modelo levam a desempenho otimista. A validação cruzada leave-one-out corrige em parte esse problema: cada evento é previsto com parâmetros ajustados sem ele. A validação cruzada não corrige, porém, o otimismo das escolhas feitas observando os mesmos dados, como a da razão de abstração inicial (seção 2.3)."
- Novo: texto do 3º parágrafo da 2.8 em `proposta_cap2_30-10.md` (com "viés de otimismo" definido e referências lidas). A parte aplicada (escolha do λ nos mesmos eventos) vai para 3.4.6.

---

## 5. Capítulo 3 (3.1 a 3.3)

5.1 (3.1) Sem mudança de texto. Conferido: "água" não aparece no sentido de escoamento.

5.2 (3.2, Tabela 1; remissão)
- Atual: "Série fornecida com os dados, reproduzida pelo filtro de Eckhardt (2005) (seção 2.4)"
- Novo: "Série fornecida com os dados, reproduzida pelo filtro de Eckhardt (2005) (ver texto)"

5.3 (3.2, frase nova sobre a série de base, vinda da 2.4; inserir **depois** do parágrafo "Da série horária obtêm-se...")
- Atual: "O volume medido inclui a vazão de base. Em todos os 17 eventos, o volume TR é exatamente a soma das vazões horárias na janela do evento, ou seja, o volume total escoado no exutório. A vazão de base (coluna Bt da série), separada pelo filtro de Eckhardt (seção 2.4), corresponde a 34% a 55% desse volume por evento (47% no conjunto), e o escoamento direto restante soma 15,3 de 28,9 milhões de m³ (Tabela 3). O SCS-CN calcula só o escoamento direto. SYobs é a carga total do evento."
- Novo: "O volume medido inclui a vazão de base. Em todos os 17 eventos, o volume TR é exatamente a soma das vazões horárias na janela do evento, ou seja, o volume total escoado no exutório. A série de vazão de base (coluna Bt) foi fornecida junto com os dados de monitoramento. Ela é reproduzida pelo filtro de Eckhardt (2005) com constante de recessão a = 0,995 (passo horário) e BFImax = 0,70, com diferença mediana de 0,002 m³/s; outros valores de BFImax e o filtro de Lyne e Hollick (1979) não a reproduzem. A vazão de base corresponde a 34% a 55% do volume total por evento (47% no conjunto), e o escoamento direto medido, Vdir = TR - Σ Bt * 3.600, soma 15,3 de 28,9 milhões de m³ (Tabela 3). A carga de sedimentos medida, SYobs, é a carga total do evento, incluindo a parcela transportada pela vazão de base."
- Observação: "diferença mediana de 0,002 m³/s" e "a = 0,995, BFImax = 0,70" são da 2.4 atual, conferidos na revisão de 29/10 (achado 5). O cabeçalho do arquivo do orientador diz BFImax 0,58 (pergunta no item I).

5.4 (3.2, Tabela 3: tirar as colunas do SCS-CN, que são resultado e vão para a Tabela 11 da 4.1)
- Atual (título): "Tabela 3. Volume total, vazão de base e escoamento direto medidos; escoamento direto calculado pelo SCS-CN; sedimento medido."
- Novo (título): "Tabela 3. Volume total, vazão de base, escoamento direto e sedimento medidos por evento."
- Nova tabela (6 colunas; colar no lugar da atual):

| Evento | Volume total TR (10³ m³) | Vazão de base Σ Bt (10³ m³) | Base (% do total) | Escoamento direto Vdir (10³ m³) | Sedimento SYobs (t) |
|---|---|---|---|---|---|
| 1 | 409 | 185 | 45 | 224 | 266 |
| 2 | 2.630 | 899 | 34 | 1.731 | 2.040 |
| 3 | 1.070 | 485 | 45 | 585 | 928 |
| 4 | 1.704 | 716 | 42 | 987 | 1.380 |
| 5 | 1.840 | 1.008 | 55 | 832 | 1.372 |
| 6 | 325 | 142 | 44 | 183 | 199 |
| 7 | 1.301 | 651 | 50 | 650 | 1.317 |
| 8 | 2.581 | 1.331 | 52 | 1.250 | 2.109 |
| 9 | 1.737 | 936 | 54 | 801 | 1.155 |
| 10 | 1.236 | 684 | 55 | 552 | 847 |
| 11 | 2.437 | 958 | 39 | 1.479 | 1.822 |
| 12 | 187 | 87 | 46 | 101 | 211 |
| 13 | 1.198 | 464 | 39 | 735 | 1.196 |
| 14 | 1.822 | 891 | 49 | 931 | 1.731 |
| 15 | 4.280 | 2.103 | 49 | 2.177 | 3.829 |
| 16 | 3.293 | 1.699 | 52 | 1.595 | 1.736 |
| 17 | 883 | 434 | 49 | 449 | 1.710 |
| Total | 28.934 | 13.671 | 47 | 15.263 | 23.846 |

Fonte: elaborado pelo autor.

(Valores copiados da Tabela 3 atual do Doc, sem recálculo; as duas colunas retiradas estão na Tabela 11 da proposta do capítulo 4.)
- Se o usuário preferir não mexer na Tabela 3 (decisão 4 do plano), manter a atual e, na 4.1, só remeter a ela.

5.5 (3.3, S13 no texto)
- Atual: "Os dados cartográficos são os mapas temáticos de solo e de uso do Plano de Bacias"
- Novo: "Os dados geoespaciais são os mapas temáticos de solo e de uso do Plano de Bacias"

5.6 (3.3, título da Tabela 4)
- Atual: "Tabela 4. Dados cartográficos."
- Novo: "Tabela 4. Dados geoespaciais."

5.7 (3.3, frase sobre CN vinda da 2.3 (C16); inserir no parágrafo "Os valores de CN não foram calculados neste trabalho...")
- Atual: "O raster corresponde à condição de umidade média (CN-II) e, na área de estudo, assume valores entre 52 e 98, com média de 71,6 nos pixels de cálculo. A condição seca (CN-I), usada no modelo, foi obtida do CN-II pela conversão empírica de Chow, Maidment e Mays (1988) e tem média de 52,5."
- Novo: "O raster corresponde à condição de umidade média (CN-II) e, na área de estudo, assume valores entre 52 e 98, com média de 71,6 nos pixels de cálculo. A condição seca (CN-I), usada no modelo (seção 3.4.1.3), foi obtida do CN-II pela conversão empírica de Chow, Maidment e Mays (1988) e varia de 31 a 95, com média de 52,5."
- Leitura: Chow, Maidment e Mays (1988) não foi acessado (lote B); a fórmula foi conferida em fonte secundária e contra a tabela do NEH-630. Já está citado assim no Doc; recomendo "CHOW; MAIDMENT; MAYS, 1988 apud NRCS, 2004" **se** a tabela do cap. 10 do NEH-630 trouxer as conversões (não verificado nesta sessão). Decisão do usuário, listada no roteiro K.

5.8 (3.3, LS; vindo da 2.6, C12; inserir como linha nova no fim do 1º parágrafo da 3.3, depois de "...não foram recalibrados neste trabalho.")
- Novo (inserir): "O fator LS foi calculado sobre o MDE corrigido, em projeção UTM, pela formulação de Moore e Burch (1986), baseada na potência do escoamento, com a área de contribuição específica limitada a 200 m (seção 3.4.1.2). O mapa de solos usado pela ANA na base de CN tem escala 1:250.000, mais grosseira que a grade de 30 m."
- Leitura: Moore e Burch (1986) só pelo resumo (lote B); a atribuição dos expoentes 0,4 e 1,3 está pendente (Moore e Burch, 1986, ou Moore e Wilson, 1992). Já é citado assim no Doc (2.6 e Tabela 4).

5.9 (3.3, remissões) Nenhuma remissão a "seção 4.x" na 3.3. As remissões "seção 2.4" da Tabela 1 e da 3.2 foram tratadas em 5.2 e 5.3.

---

## 6. Remissões a trocar no capítulo 2 e no 3 (depois de mover os textos)

| Onde | Atual | Novo |
|---|---|---|
| 2.6 (ex-2.5), se sobrar a frase | "(seção 2.2)" | "(seção 2.2)" (igual) |
| 2.8 (ex-2.7) | "(seção 2.3)" | "(seção 2.3)" (igual; e a parte aplicada vai para 3.4.6) |
| Tabela 1 | "(seção 2.4)" | "(ver texto)" (item 5.2) |
| 3.2 | "(seção 2.4)" | sai (item 5.3) |
| 1.1 | "seção 3.1"; "seção 2.2" | iguais |

## 7. O que não mudei (e por quê)

- Epígrafe, capa, folha de rosto: fora do pedido.
- Resumo, números: são os oficiais (conferidos em 29/10). Não recalculei nada.
- "água subterrânea" (2.4), "qualidade da água" (1.1), "cursos d'água" (1.1, 2.1), "corpos d'água" (3.1, 3.3), "estação de tratamento de água" e "água bruta" (3.2), "Agência Nacional de Águas" (3.3): não se referem ao escoamento; ficam.
