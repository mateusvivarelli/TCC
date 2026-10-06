# Roteiro — refazer o Evento 11 à mão (só o caminho que leva aos resultados finais)

Objetivo: reproduzir, para o evento 11, os dois resultados finais da Fase 2 e conferir método e valores:

- **Simulado** (previsão pura, Q do CN-SCS) → `SY11.tif`
- **Forçado** (Q reescalado para o volume medido) → `SY11_obs.tif`

Planilha de apoio, já com as fórmulas e os valores de referência: **`Conferencia_Evento11.xlsx`** (raiz do repositório). Células amarelas = digitar; verdes = valores lidos do QGIS; o resto é fórmula.

## O que NÃO precisa ser feito (becos sem saída / não alimentam o resultado)

- Qp da Fase 1 (hidrograma unitário, Tc de Giandotti, fator de pico): validação do modelo hidrológico, **não** entra no mapa.
- IC / FCI / DSC (`calcular_ic_*`, `calcular_fci_*`, `calcular_dsc_*`, `calcular_indice_conectividade`): abandonados.
- α e β livres (`calibrar_alfa_beta_pixel.py`).
- CN-2 e CN-3, calibração de λ por evento, classificação AMC: só comparação. Fixos: **CN-1 (seco), λ = 0,05**.
- Correção de MDE / flowacc, `_diagnostico_*`, `_calibrar_*`, grade 2×2 da seção 11.
- Modelo concentrado (`SY = c·(D·qp)^0,56`): só aparece na planilha comparativa.

## 1. O que é RI/R e de onde vêm os números

`RI/R` (1/h) = **RI** (intensidade máxima de chuva em 60 min, mm/h) ÷ **R** (lâmina total da chuva do evento, mm).

- Intuição: é a fração da chuva total que cai na hora mais intensa. Chuva concentrada (RI/R alto) gera pico local maior; chuva espalhada em muitas horas (RI/R baixo) gera pico menor.
- Está na Eq. 4 de Hao et al. (2022) para a vazão de pico local `pr`. É **um número só por evento**, igual para todos os pixels; a variação espacial de `pr` vem só de Q.
- **R** = coluna `Chuva_evento_mm`: média dos dois postos com pesos 0,307 (DBT5) e 0,693 (Campo Paulista). Os pesos foram ajustados por mínimos quadrados sobre os 17 eventos, não são Thiessen. Evento 11: `0,307·62,8 + 0,693·79,0 = 74,03` (planilha: 74,0396; diferença só do arredondamento dos pesos).
- **RI** = coluna `Intensidade_60min_mm/h`: o **máximo** entre as duas colunas `i60_p1` (11,8) e `i60_p2` (9,4), vindas da série horária dos postos. Evento 11: 11,8 mm/h.
- **RI/R do evento 11** = 11,8 / 74,039628 = **0,159374 /h**.
- Ressalva (nota 14.4 das notas): RI vem de um posto e R é uma média ponderada; nos eventos 1 e 12 a razão passa de 1 /h, o que é fisicamente impossível para um posto só. No evento 11 não ocorre.

## 2. De onde vem cada dado

| Dado | Valor (ev. 11) | Origem |
|---|---|---|
| Chuva dos 2 postos | 62,8 mm (DBT5), 79,0 mm (Campo Paulista) | `eventos_processados_manuais.xlsx` (Sheet1, linha de índice 11), colunas `chuva_p1_mm`, `chuva_p2_mm`; `excelReader.py` gera `ESTPLUV_11.csv` |
| Localização dos postos | DBT5 (−46,4809; −23,2646), Campo Paulista (−46,760284; −23,208778) | fixa em `excelReader.py`; reprojetada para UTM 23S em `Evento 11/EstPluv11.shp` (DBT5 = 348.520,85 / 7.426.415,27; Campo = 319.862,37 / 7.432.277,54) |
| R, RI | 74,0396 mm, 11,8 mm/h | colunas `Chuva_evento_mm`, `Intensidade_60min_mm/h` |
| Volume medido V_med | 2.436.681,6 m³ | coluna `T_R_m3` = `Ris_R_m3` + `Fall_R_m3`: escoamento direto medido no exutório (vazão com separação do fluxo de base) |
| Sedimento medido SY_obs | 1821,7535 t | coluna `SYY_t` = `SSY_Ris_t` + `SSY_Fall_t` (turbidez → concentração de sedimento × vazão) |
| S do CN-1 (seco), em mm | raster | `Dados Iniciais/S - Seco.tif`. **A origem dos valores de CN ainda não está registrada nas notas** (ponto aberto na nota 14.7); S médio da bacia = 255,69 mm |
| K (erodibilidade) | raster, média 0,039 | `Pedologia Alto.shp` (campo `Valor`), classes de solo com K da literatura; mapa do Plano de Bacias (Profill-Rhama, 2020) |
| C (uso do solo) | raster, média 0,05 | `Uso Solo Alto.shp` (campo `Valor`), mesma fonte; urbano/água = 0, solo exposto/mineração = 1 |
| LS (topográfico) | raster, média 0,536 | `LS Alto.tif` (Moore et al., 1991, SAGA, MDE do USGS), reprojetado para a grade de 30 m |
| P (práticas) | 1,0 | constante, sem áreas de conservação |
| λ | 0,05 | calibrado na Fase 1 (padrão SCS = 0,2) |
| α, β | 11,8 e 0,56 | Williams (1975), usados como em Hao et al. (2022) |
| c simulado / forçado | 0,109049 / 0,140844 | regressão pela origem nos 17 eventos (planilha, aba 5) |
| Grade | 884×365, 30 m (900 m²), UTM 23S (SIRGAS 2000), origem X=318.646,35 / Y=7.435.057,59 | `CN TCC.tif` / `ChuvaIDW*.tif` |

## 3. Divisão do trabalho: QGIS × planilha

**Regra prática:** tudo que tem **um valor por pixel** é QGIS; tudo que é **um número por evento** (entrada ou total) é planilha. A ponte entre os dois são (a) alguns pixels de amostra e (b) quatro totais da bacia lidos no QGIS.

### 3.1 No QGIS (raster, pixel a pixel)

Camadas: `ChuvaIDW11` (P), `S - Seco`, `K_raster`, `C_raster`, `LS_raster`. Os rasters precisam estar na **mesma grade** (884×365, 30 m). `S - Seco.tif` pode ter outra grade: alinhar com *Warp* ou *Align rasters* (vizinho mais próximo, extensão e resolução de `ChuvaIDW11`), como faz `spatialRain.py`.

1. **Chuva P (mm):** camada de pontos `EstPluv11.shp` (campo `P`) → *IDW interpolation* (`qgis:idwinterpolation`), coeficiente de distância 2, pixel 30 m, extensão de `CN TCC.tif` → `ChuvaIDW11.tif`.
2. **Q simulado (mm)** — Calculadora Raster (λ = 0,05):
   ```
   ("P@1" > 0.05*"S@1") * ( ("P@1" - 0.05*"S@1")^2 / ("P@1" + 0.95*"S@1") )
   ```
   (se `P ≤ 0,05·S`, o produto dá 0). Salvar como `Q11_CN1.tif`.
3. **Máscara de pixels válidos:** o cálculo só vale onde K, C e LS têm dado. Para forçar o mesmo conjunto em todos os totais, somar zero dos três fatores:
   ```
   "Q11_CN1@1" + 0*"K_raster@1" + 0*"C_raster@1" + 0*"LS_raster@1"
   ```
   O resultado é o `Q` mascarado; use-o nos passos seguintes. Isso importa porque o script do forçado calcula `V_calc` **só sobre essa máscara**.
4. **pr simulado (m³/s):** `"Q@1" / 1000 * 900 * 0.159374 / 3600`
5. **E_unit simulado (t):** `11.8 * ("Q@1" * "pr@1" * 900)^0.56 * "K@1" * "C@1" * 1 * "LS@1"` → `E_unit11.tif`.
6. **SY simulado por pixel (t):** `0.109049 * "E_unit11@1"` → `SY11.tif`.
7. **Totais para a planilha** — *Raster layer statistics* (`native:rasterlayerstatistics`) lê SUM e COUNT:
   - COUNT e SUM do `Q` mascarado (passo 3);
   - SUM de `E_unit11`.
8. **Q forçado:** com `f` calculado na planilha (aba 4, célula B12):
   ```
   ( "Q@1"*f > "P@1" ) * "P@1" + ( "Q@1"*f <= "P@1" ) * "Q@1" * f
   ```
   → `Q11_CN1_obs.tif`. Contar pixels limitados: SUM de `("Q@1"*f > "P@1")`.
9. Repetir os passos 4 e 5 com `Q11_CN1_obs` (→ `pr11_obs`, `E_unit11_obs.tif`) e o passo 6 com `0.140844` (→ `SY11_obs.tif`). Anotar SUM de `E_unit11_obs`.

### 3.2 Na planilha (`Conferencia_Evento11.xlsx`)

| Aba | Conteúdo |
|---|---|
| `1_Entradas` | todas as entradas do evento e a origem de cada uma |
| `2_Escalares` | RI/R, conferência de R, fator de conversão de pr |
| `3_Pixels_amostra` | ponte com o QGIS: 6 pixels onde você digita X, Y, S, K, C, LS (lidos com *Identify*) e os valores dos rasters; a planilha recalcula P (IDW por distância), Q, pr, E_unit e a versão forçada, e mostra as diferenças contra o QGIS |
| `4_Totais_QGIS` | digita ΣQ, N pixels, ΣE sim, ΣE forçado, N limitados; calcula V_calc, erro de volume, fator f, SY dos dois modelos e erros contra a referência |
| `5_Calibracao_17` | os 17 eventos do CSV do projeto; recalcula c, NSE, PBIAS e o SY do evento 11 pelas fórmulas |

Fluxo: ΣQ do QGIS → `4_Totais_QGIS` calcula `f` → `f` volta ao QGIS (passo 8) e à aba 3 → ΣE do QGIS → SY final.

**Ordem sugerida:** (1) preencher/ler a aba 1 e conferir a 2; (2) QGIS passos 1–7; (3) aba 4 com ΣQ e N pixels → `f`; (4) QGIS passos 8–9; (5) aba 4 com os ΣE; (6) aba 3 com 6 pixels para validar a fórmula pixel a pixel; (7) aba 5 para ver de onde vêm `c`, NSE e PBIAS.

## 4. Valores de referência (evento 11)

| Grandeza | Simulado | Forçado |
|---|---|---|
| Σ E_unit (t) | 6.881,90 | 8.634,27 |
| c | 0,109049 | 0,140844 |
| SY do modelo (t) | 750,46 | 1.216,09 |
| SY medido (t) | 1.821,75 | 1.821,75 |
| Erro | −58,8% | −33,2% |

- `ΣE_forçado / ΣE_simulado = 1,2547`. Como `E ∝ Q^(2·0,56) = Q^1,12`, `f` fica por volta de 1,2 (estimativa, ainda não registrada: o teto Q ≤ P e a não linearidade pixel a pixel mexem um pouco), portanto `V_calc` ≈ 2,0 milhões de m³, abaixo dos 2,44 milhões medidos. **Anote os seus `V_calc` e `f` reais**; são os dois números que o repositório ainda não tem.
- O que **a planilha não consegue** fazer sozinha: ΣE (a soma de E sobre ~260 mil pixels não se obtém de ΣQ, porque E é não linear em Q e depende de K, C e LS pixel a pixel). Por isso ΣE vem do QGIS.

## 5. Atenção ao comparar

- `c` não se recalcula só com o evento 11; vem dos 17 eventos (aba 5 reproduz: 0,109049 e 0,140844, NSE 0,3714 e 0,8052).
- O 11,8 de Williams entra em escala de bacia, com Q em mm e A em m² (nota 14.3): `c` **não** é razão de entrega de sedimentos.
- O evento 11 é subestimado nos dois casos. Simulado: o volume do CN-SCS sai baixo. Forçado: o volume já bate; o erro restante vem do `c` global e da estrutura espacial.
- O índice da planilha é 11 para o evento 11 (só o evento 1 usa 0).
