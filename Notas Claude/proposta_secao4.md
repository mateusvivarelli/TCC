# Proposta de texto: seção 4 (Metodologia), modelo oficial

Escrita na noite de 29/10/2026 por uma sessão na nuvem, sem acesso ao usuário. **Nada foi aplicado no Google Doc.** Os textos abaixo são propostas para o usuário ler, mudar e colar à mão.

Regras seguidas: caracteres de teclado (`*` e `-`, decimais com vírgula); equações em texto simples dentro de crase, marcadas `[EQUAÇÃO]` (criar no editor do Docs); nada de método ou parâmetro descartado; só cito referência lida, e o nível de leitura está na seção "Referências usadas" no fim.

Numeração: as Tabelas 1 a 6 e as Figuras 1 a 3 já estão no Doc (seções 2 e 3). A seção 4 usa as Tabelas 7 a 10 e as Figuras 4 e 5. As Tabelas 11 a 14 e as Figuras 6 em diante ficam para a seção 5 (ver `mapa_figuras_tabelas_secoes_4_a_6.md`).

Cada subseção traz: (a) o texto proposto, (b) as tabelas e figuras, (c) uma linha "O que muda no Doc".

---

## 4.1 Visão geral

**Texto proposto**

O trabalho estima, para cada um dos 17 eventos, quanta erosão cada pixel da bacia produz e quanto sedimento chega ao exutório, e compara o resultado com o sedimento medido. A Figura 4 resume o fluxo. Para cada evento:

1. a chuva medida nos dois postos é interpolada para todos os pixels (seção 4.2.4);
2. o método SCS-CN converte a chuva de cada pixel em escoamento direto, segundo o número de curva do pixel (seção 4.3);
3. a vazão de pico local e a erosão local de cada pixel são calculadas pela fórmula de Williams, aplicada pixel a pixel (seção 4.4);
4. as erosões dos pixels são somadas e multiplicadas por um coeficiente de escala c, o que dá o sedimento do evento (seção 4.5);
5. o coeficiente c é calibrado contra o sedimento medido no exutório, em escala logarítmica (seção 4.6);
6. o desempenho é avaliado por validação cruzada leave-one-out, com métricas pouco sensíveis ao evento dominante (seções 4.7 e 4.8).

O modelo foi aplicado de duas formas, que diferem só na origem da água de cada evento. No Modelo Calculado (MC), o escoamento vem da chuva pelo SCS-CN: é uma previsão. No Modelo Forçado ao Medido (MFM), o volume de escoamento direto é o medido, e o SCS-CN só o distribui no espaço: é uma referência, que mostra o desempenho possível quando a água é bem estimada. Separar as duas formas permite saber se o erro vem da água ou da fórmula de erosão.

(b) Figura 4: fluxograma. Arquivo: `TCC_Texto/figuras/mapas/fig_fluxograma.png` (regerada com o modelo oficial; trocar a imagem do Doc).
Legenda sugerida (acima da figura): "Figura 4. Fluxograma do método." Abaixo: "Fonte: elaborado pelo autor."

(c) O que muda no Doc: os itens 4 e 5 da lista (era "soma de dois termos" e "dois parâmetros c1 e c2"); some a menção a vazão de base como termo; o MFM passa a usar só o escoamento direto medido.

---

## 4.2 Preparação dos dados

### 4.2.1 Variáveis de cada evento e pixels de cálculo

**Texto proposto**

Todos os dados espaciais foram colocados na mesma grade, a do raster de chuva (884 * 365 pixels, SIRGAS 2000 / UTM 23S, pixel de 29,992 * 29,925 m = 897,49 m²). O raster de número de curva tinha outra grade (973 * 362) e foi reamostrado pelo vizinho mais próximo: cada pixel da grade de cálculo recebe o valor do pixel original que contém o seu centro. O cálculo da erosão só é feito nos pixels em que existem, ao mesmo tempo, número de curva, K, C e LS (153.855 pixels, 138,1 km²); os demais ficam sem valor. As variáveis usadas em cada evento estão na Tabela 7.

**Tabela 7. Variáveis usadas em cada evento** (colunas: Símbolo | Significado | Unidade). Proposta de conteúdo (conferir com a Tabela 7 que já existe no Doc, só trocando o que mudou):

| Símbolo | Significado | Unidade |
|---|---|---|
| P1, P2 | chuva total do evento nos postos DBT5 e Campo Limpo | mm |
| R | lâmina de chuva do evento, R = 0,307 * P1 + 0,693 * P2 | mm |
| RI | intensidade máxima da chuva (maior chuva em 60 minutos) | mm/h |
| T_R | volume total escoado no exutório, soma de Q * 3.600 | m³ |
| Bt | vazão de base separada pelo filtro de Eckhardt (seção 2.4) | m³/s |
| V_dir | volume de escoamento direto medido, T_R - soma(Bt * 3.600) | m³ |
| SY_obs | carga total de sedimentos medida, soma de Q * CSS * 3.600 | t |
| P(x) | chuva interpolada no pixel | mm |
| CN, S | número de curva e retenção potencial do pixel | -, mm |
| Q | escoamento direto no pixel | mm |
| pr | vazão de pico local no pixel | m³/s |
| E_unit | índice de erosão local do pixel | adimensional (índice relativo) |
| c | coeficiente de escala do modelo | t por unidade de E_unit |

(c) O que muda no Doc: sai a linha da duração da chuva usada no termo de base (T_chuva) e a vazão inicial como variável do modelo; entra V_dir e a definição de SY_obs como carga total. As variáveis dos eventos (valores) estão na Tabela 2 (3.2), que já está no Doc.

**Suposição:** a definição "RI = maior chuva em 60 minutos" vem do resumo do modelo (RI, intensidade máxima em 60 min). Conferir com o usuário se é assim que a Tabela 7 atual define.

### 4.2.2 Fatores K, C, LS e P

**Texto proposto**

Os fatores K e C foram atribuídos por classe (Tabelas 5 e 6): cada pixel recebe o valor da classe de solo ou de uso do polígono que contém o seu centro. Essa regra reproduz exatamente os rasters de K e de C usados no trabalho (verificado pixel a pixel). O fator LS vem do modelo digital de elevação em UTM, pela formulação de Moore e Burch (1986): LS = (As/22,13)^0,4 * (sen β/0,0896)^1,3, em que As é a área de contribuição específica (área a montante dividida pela largura da célula, em m) e β é a declividade. Adotou-se As máxima de 200 m, que equivale a limitar o comprimento da encosta a 200 m e evita que os pixels de canal recebam valores muito altos de LS. O LS médio é 7,80. O fator P é igual a 1,0 em toda a bacia, porque não há práticas conservacionistas mapeadas.

[EQUAÇÃO] `LS = (As / 22,13)^0,4 * (sen β / 0,0896)^1,3`

(b) Tabelas 5 e 6 já estão no Doc (3.3).

(c) O que muda no Doc: troca "(SAGA)" por cálculo sobre o MDE em UTM; o texto atual do Doc pode já ter isso (a 3.3 foi corrigida em 17/10). Só conferir.

**Pontos de atenção (não vão para o Doc)**
- A fórmula do LS com expoentes 0,4 e 1,3 é de uso corrente, mas só li o resumo de Moore e Burch (1986). Fontes secundárias atribuem esses expoentes a Moore e Wilson (1992). Sugiro conferir no artigo antes de manter a atribuição só a Moore e Burch.
- O limite de 200 m é escolha do TCC. O AH 537 não fixa 200 m (diz que a USLE é mais exata abaixo de ~122 m). Por isso o texto diz "adotou-se", sem atribuir a ninguém.
- Os valores de K e C por classe têm fonte na Iniciação Científica; as fontes originais estão sendo lidas no item B (`leitura_referencias/loteD_fontes_K_C.md`).

### 4.2.3 Número de curva e retenção S

**Texto proposto**

O número de curva CN (de 0 a 100) mede quanto um pixel tende a gerar escoamento: valores altos, como os de áreas urbanizadas, indicam pouca infiltração; valores baixos, como os de mata, indicam muita infiltração. O CN vem do raster BR_CN-2022 da Agência Nacional de Águas e Saneamento Básico (ANA, 2024), na condição de umidade média (CN-II), com média de 71,6 na bacia. Como condição representativa dos 17 eventos, adotou-se a condição seca (CN-I), obtida pela conversão de Chow, Maidment e Mays (1988):

[EQUAÇÃO] `CN_I = 4,2 * CN_II / (10 - 0,058 * CN_II)`

Essa conversão reproduz os valores dos rasters de CN seco usados no trabalho. O CN médio passa de 71,6 (CN-II) para 52,5 (CN-I). A escolha tem apoio no critério histórico do manual do Serviço de Conservação do Solo dos EUA (USDA-SCS, 1972), que classifica a condição antecedente pela chuva dos 5 dias anteriores: com os limites da estação de crescimento (condição seca abaixo de 35,6 mm), 13 dos 17 eventos ficam na condição seca. O manual atual do NRCS (NEH Parte 630, 2004) já não usa esse critério, e nesta bacia a chuva dos 5 dias anteriores tem correlação baixa com o coeficiente de escoamento medido (r = 0,37). Por isso o CN-I é tratado como uma condição única para o conjunto, escolhida porque reproduz o escoamento direto medido, e não como uma medida da umidade de cada evento.

A retenção potencial máxima S (mm) é a quantidade de chuva que o solo pode absorver depois que o escoamento começa. Para o CN-I, e para a razão de abstração inicial λ = 0,20 com que os CN tabelados são definidos, ela vale:

[EQUAÇÃO] `S0,20 = 25,4 * (1000 / CN - 10)`

e tem média de 255,7 mm na bacia (de 12 a 558 mm entre os pixels).

A razão de abstração inicial λ é a fração de S que a chuva precisa preencher antes de gerar escoamento (a abstração inicial é λ * S). Adotou-se λ = 0,05, valor proposto por Woodward et al. (2003) a partir de 307 bacias e parcelas dos EUA, e valores baixos de λ aparecem também em bacias brasileiras (Valle Junior; Rodrigues; Oliveira, 2019). Como o CN tabelado vale para λ = 0,20, usar λ = 0,05 exige converter a retenção. Foi usada a relação de Woodward et al. (2003), escrita em polegadas:

[EQUAÇÃO] `S0,05 = 1,33 * S0,20^1,15` (S em polegadas)

Em milímetros, que é a unidade do cálculo:

[EQUAÇÃO] `S0,05 = 25,4 * 1,33 * (S0,20 / 25,4)^1,15`

A retenção convertida tem média de 489,9 mm na bacia (Tabela 10, evento 11). Ela é maior que S0,20 em todos os pixels, como é de esperar: com abstração inicial menor, a retenção depois do início do escoamento precisa ser maior para dar um escoamento da mesma ordem.

(b) Sem tabela nova. A origem do CN e da conversão já está na Tabela 4 (3.3).

(c) O que muda no Doc: o Doc atual dá S com λ = 0,20 e média de 255,7 mm; passa a ter duas retenções e λ = 0,05. Sai a frase do "CN seco herdado da fase em que o modelo foi calibrado contra o volume total".

**Limites a declarar (ver 5.7)** e **pontos de atenção (não vão para o Doc)**
- **Frase com "λ = 0,20" no texto proposto:** ela aparece só como o valor para o qual o CN tabelado é definido, o que é necessário para explicar a conversão. Não é apresentada como alternativa testada. Se o usuário preferir cortar até essa menção, a conversão ainda se explica chamando S0,20 de "retenção obtida do CN tabelado".
- O número 489,9 mm é a média de S0,05 informada em `tab_evento11_passo_a_passo.md`; é média da bacia (igual em todos os eventos, pois S não depende da chuva).
- **Fora da faixa tabelada:** 8,4% dos pixels (12.933) têm CN-I abaixo de 35 (S0,20 acima de 472 mm), abaixo da faixa da Tabela 4 de Woodward et al. (2003), de modo que neles a conversão é extrapolação. Essa frase vai na 5.7. Opcional também aqui, em uma linha.
- **Justificativa de λ = 0,05:** o argumento que se sustenta é a água. Com CN-I e λ = 0,05 convertido, o volume do SCS-CN dá viés total de +2,9% e NSE do volume de -0,39 contra o escoamento direto medido (Tabela 3). Os 17 eventos foram usados para escolher e para avaliar; isso é limitação (5.7). **Não incluí no texto** que, sem a conversão, o escoamento inflaria 94%, porque isso é resultado de configuração descartada pela regra 3. Se o usuário quiser a frase, ela está em `notas_musle_espacializada.md` §30.
- **Contrapontos** (Baert et al., 2026; Brandão et al., 2025; Valle Junior et al., 2019) vão na 5.7, não aqui.
- **Fonte de "13 de 17":** cálculo do TCC (`notas_musle_espacializada.md` §31) com os limites de Burke e Gray, fonte secundária; o NEH-4 de 1972 não foi lido. Por isso o texto fala "critério histórico" e cita USDA-SCS (1972) só para o critério em si, com a ressalva na lista de referências abaixo.

### 4.2.4 Chuva espacializada

**Texto proposto**

Os dois postos medem a chuva em pontos. Para estimar a chuva em cada pixel, usa-se o inverso do quadrado da distância (IDW, potência 2): quanto mais perto de um posto, maior o peso dele.

[EQUAÇÃO] `P(x) = (P1 * d2^2 + P2 * d1^2) / (d1^2 + d2^2)`

em que P1 e P2 são as chuvas medidas nos postos, e d1 e d2 são as distâncias (m) do centro do pixel a cada posto, em coordenadas UTM. Os postos foram projetados de latitude e longitude (EPSG:4326) para SIRGAS 2000 / UTM 23S: DBT5 em E 348.520,8 m e N 7.426.415,3 m; Campo Limpo em E 319.862,4 m e N 7.432.277,5 m. Com apenas dois postos, um deles fora da bacia, o resultado é um gradiente suave entre os pontos, que muda de evento para evento conforme a chuva medida em cada posto. Esse cálculo reproduz o raster de chuva do QGIS com diferença menor que 10^-5 mm.

A lâmina de chuva do evento, usada na razão entre a intensidade máxima e a chuva total (seção 4.4), é a média ponderada dos dois postos, R = 0,307 * P1 + 0,693 * P2. Os pesos foram ajustados por mínimos quadrados nos 17 eventos.

(c) O que muda no Doc: a equação já está escrita na forma de fração única (a que o usuário digita no Docs); só acrescenta-se a frase da lâmina R.

**Dúvida registrada (suposição):** as notas dizem que os pesos 0,307 e 0,693 foram "ajustados por mínimos quadrados nos 17 eventos", mas não dizem **contra qual grandeza** (provavelmente a lâmina média da bacia pelo raster IDW). O texto proposto repete só o que as notas dizem. O usuário deve completar "contra o quê" antes de manter esta frase.

---

## 4.3 Escoamento direto por pixel (SCS-CN)

**Texto proposto**

Para cada pixel, o escoamento direto Q (mm) depende da chuva P do pixel e da retenção S0,05 do pixel:

[EQUAÇÃO] `Q = (P - 0,05 * S)^2 / (P + 0,95 * S)`, se P > 0,05 * S

[EQUAÇÃO] `Q = 0`, se P <= 0,05 * S

com S = S0,05 (seção 4.2.3). O termo 0,05 * S é a abstração inicial, a chuva que o solo absorve antes de qualquer escoamento (USDA-SCS, 1972; Chow; Maidment; Mays, 1988). O escoamento calculado é só o direto; a vazão de base não entra no modelo. No evento 11, por exemplo, todos os pixels geram algum escoamento.

(b) Sem tabela nova.

(c) O que muda no Doc: λ = 0,05 e S convertido no lugar de λ = 0,20; some a frase "10% dos pixels sem escoamento" e a frase sobre a condição seca herdada; some "não inclui a vazão de base" como justificativa de termo extra (fica só a constatação).

**Atenção:** a forma geral Q = (P - λS)²/(P + (1 - λ)S) vem de substituir Ia = λS em Q = (P - Ia)²/(P - Ia + S). O NEH-630 (2004) mostra a equação com λ = 0,2 e Ia genérica (lido); a substituição é álgebra do TCC. A fração de pixels sem escoamento, no evento 11, é 0% (`tab_evento11_passo_a_passo.md`); na seção 5 vale citar que em geral é de 14,0% (todos os pixels-evento) segundo a checagem de 27/10 (`relatorio_checagens_base_alvo_woodward_27-10.md`, item d).

---

## 4.4 Vazão de pico local e erosão local

**Texto proposto**

A fórmula de Williams (seção 2.2) usa o volume e a vazão de pico do escoamento. Seguindo Hao et al. (2022), cada pixel tem a sua própria vazão de pico, calculada sem roteamento hidráulico: o escoamento do pixel, em volume por segundo, é ponderado pela concentração temporal da chuva do evento, isto é, pela razão entre a intensidade máxima (RI) e a lâmina total (R):

[EQUAÇÃO] `pr = (Q / 1000) * A_pix * (RI / R) / 3600`

Em palavras: Q/1000 é a lâmina em metros; multiplicada pela área do pixel A_pix (897,49 m²), dá o volume escoado no pixel (m³); a razão RI/R (por hora) indica a fração da chuva que cai na hora mais intensa; a divisão por 3.600 converte horas em segundos. Eventos em que a chuva se concentra em poucas horas têm picos locais maiores. A razão RI/R é um número único por evento; a variação de pr entre pixels vem só de Q. O fator 1/1000 converte a lâmina de mm para m; a fórmula impressa em Hao et al. (2022) não o traz, e aqui ele é uma correção de unidade que só muda a escala, absorvida por c.

A erosão local é a fórmula de Williams (1975) aplicada ao pixel, com os coeficientes originais (11,8 e 0,56):

[EQUAÇÃO] `E_unit = 11,8 * (Q * pr * A_pix)^0,56 * K * C * LS * P`

com Q em mm, pr em m³/s e A_pix em m², como em Hao et al. (2022). Como pr é proporcional a Q, E_unit é proporcional a Q^1,12. E_unit é um índice relativo de erosão, não uma massa em toneladas: os coeficientes de Williams foram ajustados em escala de bacia, e o produto Q * pr * A em um pixel de 897 m² está fora da faixa para a qual eles foram ajustados. O coeficiente c da seção seguinte converte esse índice em toneladas. Os coeficientes 11,8 e 0,56 foram mantidos; Q em mm (no lugar de m³) apenas muda a escala de E_unit e também é absorvida por c.

(c) O que muda no Doc: quase nada. Acrescentar a frase sobre o fator 1/1000 e sobre Q em mm; a frase "c1 da seção seguinte" vira "c".

**Pontos de atenção (não vão para o Doc)**
- Hao et al. (2022): texto completo lido. A MUSLE por pixel e o pico local sem roteamento são de lá; a fórmula impressa não tem o 1/1000 e a Eq. 3 do artigo tem um erro de digitação (100/CN no lugar de 1000/CN). Hao não cita Williams (1975); a origem de 11,8 e 0,56 é Williams.
- Williams (1975): original **não lido**; a equação e os coeficientes vêm de fontes secundárias e do AH 537 (p. 47), onde só a ideia central está confirmada. O texto não afirma número de bacias, eventos nem faixa de declividade de Williams.
- No pixel a declividade média é muito maior que a das bacias de Williams (fonte secundária: 0,9 a 5,9%). Isso é limitação possível para 5.7, **só se** o dado for conferido no original.

---

## 4.5 Sedimento do evento

(Título novo. No Doc era "Sedimento do evento: modelo de dois componentes".)

**Texto proposto**

O sedimento do evento é proporcional à soma da erosão local de todos os pixels:

[EQUAÇÃO] `SY = c * soma(E_unit)`

em que a soma é feita sobre os 153.855 pixels de cálculo, e c (t por unidade de E_unit) converte o índice em toneladas. Esse coeficiente absorve, além da diferença de escala entre o coeficiente de Williams e o pixel, a razão de entrega de sedimentos, e por isso não deve ser lido como uma razão de entrega. Não há termo de vazão de base: a MUSLE descreve a erosão causada pelo escoamento superficial, e a água de base transporta o sedimento mas não o produz nas encostas.

O sedimento medido que serve de alvo (SY_obs) é a carga total do evento, soma de Q * CSS * 3.600 sobre as horas do evento. Admite-se que todo o sedimento do evento foi mobilizado pelo escoamento superficial e que a água de base apenas o transporta. O mapa de áreas críticas mostra c * E_unit de cada pixel.

As duas versões do modelo diferem na origem da água (Tabela 8):

- **Modelo Calculado (MC):** Q vem do SCS-CN, a partir da chuva interpolada. Usa só a chuva dos postos. É uma previsão.
- **Modelo Forçado ao Medido (MFM):** o volume de escoamento direto é forçado ao valor medido, V_dir = T_R - soma(Bt * 3.600). O SCS-CN apenas distribui esse volume no espaço: todos os pixels são multiplicados pelo mesmo fator f = V_dir / V_SCS, em que V_SCS é o volume que o SCS-CN calcularia, e o escoamento do pixel é limitado à chuva do pixel, Q = min(f * Q_SCS, P), porque o escoamento não pode superar a chuva. Não é previsão: mostra o desempenho que o modelo atingiria se a água fosse bem estimada.

**Tabela 8. Origem da água em cada versão do modelo.**

| Versão | Escoamento direto | Coeficiente c (t por unidade de E_unit) |
|---|---|---|
| Modelo Calculado (MC) | calculado pelo SCS-CN (CN-I, λ = 0,05 com S convertido) a partir da chuva | 0,0344 |
| Modelo Forçado ao Medido (MFM) | volume medido, V_dir = T_R - soma(Bt * 3.600), distribuído no espaço pelo padrão do SCS-CN | 0,0222 |

(O valor de c entra aqui porque a Tabela 9 também os traz; se o usuário preferir, deixar c só na Tabela 9.)

(c) O que muda no Doc: seção reescrita; saem "modelo de dois componentes", os dois termos, Vref e o parágrafo da duração da chuva. A Tabela 8 perde a coluna da vazão de base e fica com duas colunas de conteúdo.

**Atenção**
- O texto diz "a água de base apenas o transporta" como **hipótese de trabalho**, não como fato medido. A checagem de 27/10 mostra que, com a hipótese alternativa (alvo = só a carga do escoamento direto, com concentração igual à da mistura), o MFM iria a 12,9% de erro mediano, sem mudar as conclusões. Isso vai na 5.7 (limitações), não aqui.
- Nome dos modelos (MC/MFM, ou "preditivo/diagnóstico"): decisão pendente do usuário (`notas_musle_espacializada.md` §34). Usei MC e MFM, que são os do Doc.

---

## 4.6 Calibração do coeficiente c

**Texto proposto**

O coeficiente c foi ajustado aos 17 sedimentos medidos em escala logarítmica, isto é, minimizando a soma dos quadrados de ln(SY_obs) - ln(c * soma(E_unit)). A solução tem forma fechada:

[EQUAÇÃO] `ln c = média[ ln(SY_obs,n) - ln(soma E_unit,n) ]`, média sobre os 17 eventos

Esse critério pesa os eventos pelo erro relativo e evita que um único evento muito grande comande o ajuste: o evento 15 responde por 48,7% da variância linear da carga medida. É equivalente a maximizar o NSE em escala logarítmica. A calibração é feita separadamente para o MC e para o MFM, porque a soma de E_unit é diferente nos dois. A Tabela 9 reúne os parâmetros fixos e o calibrado.

**Tabela 9. Parâmetros fixos e calibrados.** Fonte: `TCC_Texto/tabelas/tab_parametros.md`.

| Parâmetro | Valor | Origem |
|---|---|---|
| Coeficiente de Williams e expoente | 11,8 e 0,56 | Williams (1975), mantidos |
| Número de curva | CN-II da ANA convertido para CN-I | ANA (2024); conversão de Chow, Maidment e Mays (1988) |
| λ (razão de abstração inicial) | 0,05 | Woodward et al. (2003) |
| Retenção S com λ = 0,05 | S0,05 = 25,4 * 1,33 * (S0,20 / 25,4)^1,15 (mm) | Woodward et al. (2003), S0,20 do CN-I |
| Peso dos postos DBT5 / Campo Limpo na lâmina do evento | 0,307 / 0,693 | mínimos quadrados nos 17 eventos |
| P (práticas conservacionistas) | 1,0 | sem práticas na bacia |
| MC: c (t por unidade de E_unit) | 0,0344 | calibrado em log, 17 eventos |
| MFM: c (t por unidade de E_unit) | 0,0222 | calibrado em log, 17 eventos |

(A linha "IC refeita: α e β" de `tab_parametros.md` (0,978 e 0,733) pertence à seção 5.5; sugiro **tirar** da Tabela 9 e citar na 5.5, porque a seção 4 não descreve a IC. Se o usuário quiser descrevê-la na 4.7, mantém.)

(c) O que muda no Doc: dois parâmetros (c1, c2) viram um (c); sai a otimização não linear em três pontos de partida (agora há fórmula fechada).

---

## 4.7 Validação cruzada

**Texto proposto**

Um coeficiente ajustado aos mesmos dados usados para avaliar o modelo leva a resultados otimistas. Para evitar isso, cada evento foi previsto com um c ajustado sem ele (validação cruzada leave-one-out): (i) retira-se um evento; (ii) ajusta-se c aos 16 eventos restantes; (iii) prevê-se o sedimento do evento retirado; (iv) repete-se para os 17 eventos. As métricas são calculadas sobre as 17 previsões. Os resultados "no ajuste" (sem validação cruzada) são mostrados à parte e só têm valor diagnóstico.

(c) O que muda no Doc: sai "aninhada" (com um único parâmetro não há etapa aninhada) e a menção a c1 e c2. Os modelos de comparação (seção 4.8) passam pelo mesmo procedimento: o parâmetro de cada um é refeito dentro de cada rodada.

---

## 4.8 Modelos de comparação e métricas de desempenho

(Título sugerido: "4.8 Modelos de comparação e métricas". No Doc era só "Métricas".)

**Texto proposto**

Para saber se o modelo espacializado acrescenta algo, ele foi comparado a regras simples que usam a mesma informação. O MC foi comparado a SY = c * R (sedimento proporcional à lâmina de chuva do evento), que usa só a chuva. O MFM foi comparado a SY = c * V_dir (sedimento proporcional ao volume de escoamento direto medido) e à formulação concentrada da Iniciação Científica (IC) refeita: Y = α * (V * qp)^β * K * LS * C * P, com o volume V e a vazão de pico qp medidos no hidrograma e K, LS e C médios da bacia, com α e β recalibrados em escala logarítmica nos 17 eventos (Vivarelli et al., 2025). Todos passam pela mesma validação cruzada.

As métricas principais não dependem da variância dos dados e, por isso, não são dominadas por um único evento:

- **Erro percentual mediano:** a mediana de |simulado - medido| / medido * 100 sobre os 17 eventos. A mediana evita que erros muito grandes em poucos eventos dominem. Não se usa a média do erro absoluto percentual, porque ela favorece a subestimativa.
- **Fração de eventos dentro de fator 2:** o percentual de eventos em que o simulado está entre 0,5 e 2 vezes o medido.
- **Correlação de Spearman:** correlação entre as posições (ordens) do simulado e do medido; indica se o modelo ordena os eventos corretamente, sem depender da magnitude.
- **NSE em escala logarítmica:** o NSE (Nash; Sutcliffe, 1970) calculado sobre ln(SY) em vez de SY. O NSE compara o erro do modelo com a variação dos próprios dados: vale 1 quando o modelo acerta tudo, 0 quando erra tanto quanto errar prevendo sempre a média dos eventos, e é negativo quando erra mais que isso. O NSE em escala linear é mostrado como medida secundária (Apêndice), com e sem o evento 15, porque é dominado pelos eventos grandes.

Para comparar dois modelos, calculou-se a diferença do erro por evento e o intervalo de confiança de 95% da mediana dessa diferença, por reamostragem dos eventos (bootstrap, 4.000 reamostragens).

(c) O que muda no Doc: entram os modelos de comparação (era só uma frase na 5.5) e o bootstrap; o NSE linear vira secundário.

**Atenção**
- **Bootstrap:** usei a descrição das checagens de 27/10 (4.000 reamostragens de eventos, IC95% da diferença pareada). Se o usuário não quiser descrever o bootstrap, a frase final pode sair e os ICs da 5.5 ficam sem a explicação do método.
- **Nash e Sutcliffe (1970): não lido.** A definição verbal do NSE é de fonte secundária. O NSE em log não é de Nash e Sutcliffe: é uma adaptação comum; o texto proposto o descreve com palavras próprias. A frase "dominado pelos eventos grandes" é afirmação do TCC (a variância linear do evento 15, 48,7%), não de Nash e Sutcliffe.
- A IC refeita usa o volume **total** e o pico **total** medidos (só assim os erros publicados se reproduzem), e K = 0,031, LS = 0,536, C = 0,267 da IC. Isso entra na 5.5 em detalhe; aqui basta a definição.
- O "erro de 16,3%" é da IC refeita pelo TCC, não da IC publicada.

---

## 4.9 Exemplo numérico: o evento 11

**Texto proposto**

Para acompanhar o cálculo, a Tabela 10 e a Figura 5 mostram o evento 11 (04 a 08/07/2019) do início ao fim, com um pixel de exemplo escolhido entre os de lavoura temporária sobre Argissolo, com erosão alta (E 330,18 km; N 7.432,86 km). O pixel recebe 75,4 mm de chuva. Seu CN-II é 81,0; convertido, vira CN-I 64,2. A retenção passa de 141,9 mm (S0,20) para 244,2 mm (S0,05), e a abstração inicial é 12,2 mm. O escoamento é 13,00 mm e, com K = 0,0351, C = 0,212 e LS = 4,869, o índice de erosão é E_unit = 1,167, que vale 40,1 kg de sedimento (c * E_unit = 0,0344 * 1,167). Somando E_unit nos 153.855 pixels (40.885), o MC estima 1.406 t no ajuste (1.383 t na validação cruzada), contra 1.822 t medidas: erro de -23% (-24%). O MFM estima 1.410 t (1.387 t na validação cruzada), erro de -23% (-24%).

**Tabela 10. O evento 11 passo a passo, com um pixel exemplificado.** Arquivo: `TCC_Texto/tabelas/tab_evento11_passo_a_passo.md` (colunas Etapa | Grandeza | Valor). Colar o conteúdo do arquivo. Trocar a tabela do Doc.

**Figura 5. Etapas espaciais do modelo no evento 11.** Arquivo: `TCC_Texto/figuras/mapas/mapa_08_evento11.png` (regerado; trocar a imagem). Legenda sugerida: "Figura 5. Etapas espaciais do modelo no evento 11: chuva interpolada, retenção S, escoamento direto, índice de erosão E_unit e sedimento do pixel (MC)." Abaixo: "Fonte: elaborado pelo autor."

(c) O que muda no Doc: todos os números do exemplo (pixel e evento) e a tabela inteira; o painel da retenção na Figura 5 mostra S0,05 (convertido); o último painel era "sedimento das encostas" e passa a ser "sedimento do pixel". Conferir o rótulo dentro da imagem (ver `relatorio_regeneracao_oficial_28-10.md`: os rótulos "Sedimento das encostas" foram mantidos).

**Conferência feita nesta noite:** recalculei o pixel de exemplo a partir dos números da tabela: Q = (75,4 - 12,2)^2 / (75,4 + 0,95 * 244,2) = 12,99 mm (a tabela diz 13,00; diferença de arredondamento); c * E_unit = 0,0344 * 1,167 = 0,0401 t.

---

## Referências usadas na seção 4 e nível de leitura

Níveis tirados dos relatórios `Notas Claude/leitura_referencias/` (lotes A, B, C) e de `relatorio_checagens_base_alvo_woodward_27-10.md`. **Eu não reabri nenhum original esta noite**; repito o que os relatórios declaram.

| Referência | Nível de leitura declarado | Uso na seção 4 |
|---|---|---|
| Hao et al. (2022) | texto completo | MUSLE por pixel, pico local, E_unit, calibração em log, leave-one-out |
| Woodward et al. (2003) | texto completo do manuscrito (PDF de site de curso); página editorial da ASCE não aberta; Eq. 8 conferida | λ = 0,05 e conversão de S; base de 307 bacias/parcelas |
| Valle Junior, Rodrigues e Oliveira (2019) | texto completo | valores baixos de λ em bacia brasileira |
| Chow, Maidment e Mays (1988) | **livro não acessado**; fórmula conferida em fontes secundárias e contra a tabela do NEH-630 | CN-I = 4,2 CN-II / (10 - 0,058 CN-II) |
| USDA-SCS (1972), NEH-4 | **original de 1972 não acessado**; lido o cap. 10 do NEH-630 (2004) e fonte secundária (Burke e Gray) para os limites de 5 dias | equação do SCS-CN; critério histórico dos 5 dias |
| NEH Parte 630, cap. 10 (2004) | texto completo do capítulo | equação do SCS-CN; critério dos 5 dias abandonado (**ainda não está na lista de referências do TCC**; precisaria ser acrescentada se for citado) |
| ANA (2024) | ficha de metadados, planilha e Nota Técnica 9/2025 lidas | origem do CN-II (CN2) |
| Williams (1975) | **original não acessado**; AH 537 (p. 47) e fontes secundárias | MUSLE e coeficientes 11,8 e 0,56 |
| Moore e Burch (1986) | **só resumo** (Crossref); equação por fontes secundárias | LS |
| Nash e Sutcliffe (1970) | **não acessado**; só dados bibliográficos e fonte secundária | definição do NSE |
| Vivarelli et al. (2025), IC | texto completo (artigo e relatório PIBIC) | IC refeita |
| Wischmeier e Smith (1978), AH 537 | texto completo acessado, trechos relevantes lidos | P = 1; limite de 200 m **não** vem dele |
| Murillo-Bermúdez et al. (2023) / Murillo-Bermúdez e Martim (2022) | 2023: só resumo; 2022: texto completo | CSS por turbidez (descrita na seção 3.2, não na 4) |
| Eckhardt (2005) | só resumo (mais Eckhardt 2012 completo) | Bt (descrito na 2.4 e 3.2; aqui só citado em T_R, V_dir) |

**Para a lista de referências do TCC:** nenhuma nova é obrigatória para a seção 4 além do NEH-630 (se o usuário citar o abandono do critério dos 5 dias) e de Burke e Gray (se quiser citar a fonte dos limites). Sugestão: citar só USDA-SCS (1972) para o critério e o NEH-630 (2004) para o abandono, ambos com a nota de leitura acima.

## Resumo das dúvidas que ficam para o usuário

1. Contra o quê foram ajustados os pesos 0,307 e 0,693 da lâmina do evento (4.2.4)?
2. Manter "λ = 0,20" no texto da 4.2.3 como valor de definição do CN tabelado (necessário para a conversão)? Ou chamar S0,20 apenas de "retenção obtida do CN"?
3. Descrever o bootstrap (4.8)?
4. Tirar "IC refeita: α e β" da Tabela 9 e levar para 5.5?
5. Nomes MC e MFM mantidos ou trocar por "preditivo/diagnóstico"?
6. Expoentes do LS: atribuir a Moore e Burch (1986) ou a Moore e Wilson (1992)? Conferir no artigo.
