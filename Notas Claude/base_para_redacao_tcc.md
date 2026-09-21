# Base para a redação do TCC — narrativa consolidada

Documento de apoio à redação, organizado na ordem do texto final (metodologia → resultados →
discussão → limitações), e não na ordem cronológica em que o trabalho foi feito. O histórico
cronológico completo, com todas as tentativas descartadas, está em
[notas_qgis_calibracao_qp.md](notas_qgis_calibracao_qp.md) (Fase 1) e
[notas_musle_espacializada.md](notas_musle_espacializada.md) (Fase 2).

Atualizado em 21/09/2026.

---

## 1. Dados de entrada

### 1.1. Dados medidos em campo (2018–2020, 17 eventos)

| Dado | Origem | Uso no trabalho |
|---|---|---|
| Chuva horária | 2 postos pluviométricos (DBT5 e Campo Paulista) | entrada do modelo chuva-vazão |
| Vazão horária | seção de controle no exutório | calibração/validação da Fase 1 |
| CSS (concentração de sedimento em suspensão) | seção de controle no exutório | origem do `SYY_t` |
| `T_R_m3` (volume escoado por evento) | integração da vazão | calibração do volume; restrição do Q |
| `Q_pico` (vazão de pico por evento) | máximo da série horária | validação da Fase 1 |
| `SYY_t` (sedimento total por evento) | integração de CSS × vazão (ramos ascendente + descendente da histerese) | **alvo de toda a calibração da Fase 2** |

Os dois postos ficam a leste (DBT5, **fora** da bacia) e a oeste (Campo Paulista, próximo ao
exutório). Coordenadas: DBT5 em X=348.520,8 / Y=7.426.415,3; Campo Paulista em X=319.862,4 /
Y=7.432.277,5 (SIRGAS 2000 / UTM 23S).

### 1.2. Dados cartográficos

| Dado | Produto derivado | Valor médio na bacia |
|---|---|---|
| Mapa pedológico (`Pedologia Alto.shp`) | fator **K** (erodibilidade) | 0,039 |
| Mapa de uso do solo (`Uso Solo Alto.shp`) | fator **C** (cobertura) | 0,050 |
| MDE + declividade | fator **LS** (topográfico) | 0,536 |
| — | fator **P** (práticas conservacionistas) | 1,0 (constante) |
| Interseção pedologia × uso do solo | mapa de **CN** em 3 cenários de umidade | — |

Grade de referência: 884 × 365 pixels de ~30 m (897,49 m² por pixel), ~154 mil pixels válidos
cobrindo os 137,8 km² da bacia. SIRGAS 2000 / UTM 23S.

---

## 2. Fase 1 — modelagem hidrológica espacializada

### 2.1. Escoamento superficial (SCS-CN)

A chuva de cada evento é interpolada por IDW a partir dos dois postos, gerando `ChuvaIDW{n}.tif`.
O método SCS-CN é então aplicado **pixel a pixel**:

$$Q = \frac{(P - \lambda S)^2}{P + (1-\lambda)S}, \qquad P > \lambda S$$

Duas decisões de calibração:

1. **Cenário de umidade antecedente: CN-1 (solo seco, AMC I)**, adotado para todos os eventos.
2. **Razão de abstração inicial recalibrada: λ = 0,2 → 0,05.**

Resultado: erro médio de volume de **+0,5%** (absoluto 47,4%), contra -62,6% na configuração
padrão. A escolha de λ=0,05 tem respaldo em Brandão et al. (2025), que avaliaram 3.578 bacias e
concluíram que λ=0,05 supera o padrão 0,2 na maioria dos casos.

### 2.2. Correção do modelo digital de elevação

A área de contribuição calculada a partir do MDE original era de 109,79 km². Identificou-se que o
MDE não representava um aterro de estrada com passagem de água (bueiro), criando uma barreira
artificial de drenagem. Corrigida a barreira, a área passou a **137,80 km²** — consistente com a
delimitação de campo. Ganho de ~28 km² de área de contribuição.

### 2.3. Vazão de pico

Calculada por convolução horária com hidrograma unitário do SCS, tempo de concentração de
Giandotti (10,652 h) e fator de pico recalibrado (2,08 → 1,1184). Erro médio **-38,4%** (absoluto
46,0%).

> ⚠️ **Não alimenta a Fase 2.** Este resultado é uma **validação do modelo hidrológico da bacia**.
> A vazão de pico usada na MUSLE espacializada é a formulação local de Hao et al. (seção 3.1) —
> isso precisa estar explícito no texto para não parecer inconsistência metodológica.

---

## 3. Fase 2 — MUSLE espacializada

Metodologia de Hao et al. (2022), em duas etapas.

### 3.1. Vazão de pico local (pr), por pixel

$$pr_k = \frac{Q_k}{1000} \cdot A_{pixel} \cdot \frac{RI}{R_{evento}} \cdot \frac{1}{3600}$$

onde RI é a intensidade máxima de 60 min do evento (mm/h) e R o total precipitado (mm). É o
escoamento do próprio pixel ponderado pelo grau de concentração temporal da chuva daquele evento
— **sem roteamento hidráulico, sem delimitação de sub-bacias e sem acumulação de fluxo**.

A razão RI/R é escalar (igual para todos os pixels de um mesmo evento); a variação espacial de
`pr` vem inteiramente de `Q_k`.

### 3.2. Erosão local por pixel (E_unit)

$$E_{unit,k} = 11{,}8 \cdot (Q_k \cdot pr_k \cdot A)^{0{,}56} \cdot K_k \cdot C_k \cdot LS_k \cdot P$$

Os coeficientes α = 11,8 e β = 0,56 permanecem nos **valores originais de Williams (1975)** — Hao
et al. não os recalibram, e nós também não.

### 3.3. Produção de sedimentos

$$SY_k = c \cdot E_{unit,k}$$

com **um único parâmetro livre** (`c`), calibrado por mínimos quadrados pela origem contra os 17
valores de `SYY_t`.

### 3.4. Restrição pelo volume observado

O raster `Q{n}_CN1.tif` de cada evento é multiplicado por um fator único, de modo que o volume
total da bacia iguale o `T_R_m3` medido. O **padrão espacial** do SCS-CN (proveniente do CN e da
chuva interpolada) é preservado; apenas o **total** é ancorado na medição.

Fatores de correção resultantes: de 0,55 (evento 9) a 6,95 (evento 10). Essa dispersão é, em si,
a medida do erro do SCS-CN nesta bacia.

**Precedente na literatura:** Baert et al. (2026) utilizam volume e pico observados como entrada
da MUSLE na configuração de referência do estudo deles.

---

## 4. A etapa de conectividade — implementada e descartada

Hao et al. (2022) propõem uma terceira etapa: um índice de conectividade funcional (FCI, Eq. 7),
normalizado em grau de conectividade de sedimentos (DSC, Eq. 8, sigmoide com dois parâmetros
calibráveis FCI₀ e k_FCI), que estima a probabilidade de o sedimento erodido em cada pixel
efetivamente alcançar o exutório.

A etapa foi **integralmente implementada**: direção de fluxo D8 derivada do MDE corrigido,
acumulação de montante, e a formulação exata da Eq. 7 (verificada contra as imagens das equações
do artigo, pois o texto extraído do PDF estava corrompido nesse trecho).

**Resultado:** em nenhuma configuração testada o FCI/DSC superou a escala linear constante.
Inclusive foi identificado e corrigido um erro real — um pixel de área urbana/água adjacente ao
exutório, com E_unit = 0, inflava o denominador (Ddn) de toda a bacia — e ainda assim o
desempenho piorou.

**Hipótese (não testada por limitação de tempo):** diferença de escala. As bacias de Hao et al.
têm 1.310 km² (Dali), 1.749 km² (Xiangshui) e 8.973 km² (Duhe) — de 10 a 65 vezes maiores que o
Alto Jundiaí (137,8 km²). Como o numerador do índice depende de √(área) e o denominador acumula
ao longo de caminhos de fluxo proporcionalmente mais curtos, é plausível que a escala natural do
índice não se transfira entre bacias de portes tão distintos sem normalização adicional.

**Isso deve ser reportado como achado, não omitido:** a tentativa de incorporar conectividade
espacial foi feita, documentada, e não se mostrou vantajosa nesta bacia.

---

## 5. Resultados

### 5.1. Desempenho

| Métrica | Previsão pura (Q modelado) | Volume observado como restrição |
|---|---|---|
| Parâmetro `c` | 0,109049 | 0,140844 |
| NSE (validação cruzada, *leave-one-out*) | 0,2816 | **0,7759** |
| NSE (in-sample) | 0,3714 | 0,8052 |
| WIA (índice de concordância de Willmott) | 0,8683 | **0,9462** |
| PBIAS (viés percentual) | -21,28% | **-0,99%** |
| Erro absoluto médio (LOO) | 46,1% | **27,8%** |

### 5.2. Decomposição do erro (diagnóstico)

Mantendo tudo constante exceto a qualidade da entrada hidrológica:

| Configuração | NSE (LOO) |
|---|---|
| Espacializada, Q do SCS-CN | 0,2816 |
| Espacializada, volume observado | 0,7759 |
| Concentrada (MUSLE clássica), D e qp medidos | 0,8476 (in-sample) |
| Concentrada, D e qp modelados | 0,4412 (in-sample) |

**Leitura:** a estrutura espacial não é a fonte do erro. Com entrada hidrológica de qualidade, ela
atinge NSE 0,78–0,81. A espacialização também não degrada o desempenho agregado em relação à
formulação concentrada — ou seja, o mapa é obtido sem custo de acurácia.

### 5.3. Tentativas de melhorar o volume preditivamente (todas falharam)

| Tentativa | Resultado |
|---|---|
| λ ótimo por evento | **5 dos 17 eventos são inatingíveis**: nem com λ→0 o CN-1 gera escoamento suficiente (eventos 1, 2, 4, 7 e 10, subestimados em 55–85%) |
| λ como função da lâmina de chuva | melhora in-sample, **piora** em validação cruzada (0,273 → 0,258) |
| Classificação AMC padrão do SCS por chuva antecedente de 5 dias | **piora muito** (NSE do volume: -2,97) |
| Escolha ótima de cenário CN (oráculo, não realizável) | NSE do volume 0,47; NSE do SY 0,63 |

Isso reproduz de forma independente o achado central de Baert et al. (2026) — nenhuma
generalização de λ atinge bom desempenho fora da amostra — e ecoa Valle Junior et al. (2019),
que documentaram inadequação estrutural do SCS-CN em bacia brasileira.

### 5.4. Robustez do mapa

- Correlação espacial entre o mapa médio com e sem restrição de volume: **r = 0,9941**
- Coincidência dos hot spots (5% superiores): **96,9%**
- Hot spots têm C médio 0,247 (bacia: 0,050) e LS médio 0,791 (bacia: 0,537)
- Correlações: SY × C = 0,70; SY × LS = 0,19

**Interpretação:** a localização das áreas críticas é robusta à correção hidrológica. A correção
afeta a magnitude por evento, não o padrão espacial — propriedade desejável, já que o objetivo do
trabalho é identificar *onde* a erosão se concentra.

---

## 6. Por que os resultados são satisfatórios

1. **Superam o artigo de referência.** Hao et al. (2022) reportam NSE > 0,70 e WIA > 0,89 nas três
   bacias estudadas. A versão com volume restrito atinge NSE 0,78 e WIA 0,95, com formulação mais
   simples (sem o módulo de conectividade).

2. **Superam o benchmark mais recente do problema.** Baert et al. (2026), em 154 eventos, obtiveram
   NSE = 0,66 para a MUSLE com volume e pico observados, e NSE ≈ 0 com entradas modeladas. Os dois
   resultados obtidos aqui (0,78 com volume observado; 0,28 com volume modelado) estão acima dos
   dois casos correspondentes.

3. **As métricas são honestas.** O valor principal é obtido por validação cruzada *leave-one-out*
   — a mesma metodologia de validação empregada por Hao et al. O valor in-sample é reportado
   separadamente, não em seu lugar.

4. **O modelo é parcimonioso.** Um único parâmetro livre contra 17 observações, com α e β fixos nos
   valores originais de Williams (1975). Para comparação, a Iniciação Científica ajustou dois
   parâmetros (α e β), e a formulação com conectividade exigiria outros dois (FCI₀ e k_FCI).

5. **O produto central é robusto** (seção 5.4).

6. **As checagens físicas são consistentes:** os hot spots concentram-se em uso do solo mais
   agressivo combinado a maior declividade; a restrição "escoamento ≤ chuva" foi violada em apenas
   0,48% dos pixels (limitados à lâmina precipitada).

---

## 7. Limitações a declarar explicitamente

**a) A versão com volume restrito não é previsão pura.** O desempenho de 0,78 é condicionado ao
conhecimento do volume medido. Para bacia não monitorada, o valor honesto é 0,28. Isso é
metodologicamente legítimo porque o objetivo é *mapear* 17 eventos observados, não prever eventos
futuros — mas deve ser declarado nesses termos.

**b) E_unit é índice relativo, não tonelagem absoluta por pixel.** O coeficiente 11,8 de Williams
foi calibrado para volume e pico em escala de bacia. Aplicado a um pixel de 897 m², o produto
(Q · pr · A) está fora da faixa para a qual o coeficiente foi ajustado. Na prática, `c` absorve
conjuntamente a conversão de escala e a razão de entrega de sedimentos. **O total do mapa está em
toneladas reais** (ancorado na medição), mas o valor de um pixel isolado deve ser lido como
contribuição relativa. Essa é uma característica do método de Hao et al., não da aplicação — mas
precisa ser declarada.

**c) A chuva provém de apenas dois postos**, um deles fora da bacia. A variabilidade espacial da
precipitação no mapa é um gradiente suave interpolado entre dois pontos. O padrão espacial é,
portanto, dominado pelos fatores estáticos (K, C, LS) — o que explica sua robustez, mas também
representa provavelmente a maior fonte de erro residual.

**d) O mapa não foi validado espacialmente.** Não existem medições distribuídas de sedimento
dentro da bacia, apenas no exutório. A validação é agregada; a coerência espacial é sustentada
pelas checagens físicas da seção 5.4.

---

## 8. Escopo removido

A simulação de cenários de conservação (alteração local de C e P para representar intervenções de
bioengenharia e engenharia civil) foi **retirada do escopo** em 14/09/2026, por decisão do autor
em função do prazo. Foi removida do Objetivo Geral, dos Objetivos Específicos, da Metodologia e do
Cronograma do projeto atualizado.

---

## 9. Referências citadas nesta narrativa

- BAERT, P.; et al. A regime-based framework for linking runoff initiation and event-scale
  sediment export in a small temperate agricultural loess catchment. **Catena**, v. 274, art.
  110497, 2026. DOI: 10.1016/j.catena.2026.110497.
- BORSELLI, L.; CASSI, P.; TORRI, D. Prolegomena to sediment and flow connectivity in the
  landscape: A GIS and field numerical assessment. **Catena**, v. 75, n. 3, p. 268-277, 2008.
  DOI: 10.1016/j.catena.2008.07.006.
- BRANDÃO, A. R. A.; et al. Toward a better understanding of curve number and initial abstraction
  ratio values from a large sample of watersheds perspective. **Journal of Hydrology**, v. 655,
  art. 132941, 2025. DOI: 10.1016/j.jhydrol.2025.132941.
- HAO, R.; et al. Incorporating sediment connectivity index into MUSLE model to explore soil
  erosion and sediment yield relationships at event scale. **Journal of Hydrology**, v. 614, art.
  128579, 2022. DOI: 10.1016/j.jhydrol.2022.128579.
- VALLE JUNIOR, R. F.; et al. (bacia do Guariroba). **RBRH**, 2019.
- VIVARELLI, M.; et al. Aplicação da equação universal de perda de solo modificada e calibração
  com dados de campo em uma bacia hidrográfica antropizada. Artigo (Iniciação Científica) —
  Universidade Estadual de Campinas, Campinas, 2025.
- WILLIAMS, J. R. Sediment-yield prediction with universal equation using runoff energy factor.
  **Present and prospective technology for predicting sediment yield and sources**. ARS-S-40. US
  Department of Agriculture, Washington, DC, 1975. p. 244-252.
