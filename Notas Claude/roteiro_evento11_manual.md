# Roteiro — refazer o Evento 11 à mão (só o caminho que leva aos resultados finais)

Objetivo: reproduzir, para o evento 11, os dois resultados finais da Fase 2 e conferir método e valores:

- **Simulado** (previsão pura, Q do CN-SCS) → `SY11.tif`
- **Forçado** (Q reescalado para o volume medido) → `SY11_obs.tif`

Valores de referência do evento 11 (para conferir no fim) estão na seção 6.

## O que NÃO precisa ser feito (becos sem saída / não alimentam o resultado)

- Qp da Fase 1 (hidrograma unitário, Tc de Giandotti, fator de pico): validação do modelo hidrológico, **não** entra no mapa.
- IC / FCI / DSC (`calcular_ic_*`, `calcular_fci_*`, `calcular_dsc_*`, `calcular_indice_conectividade`): abandonados.
- α e β livres (`calibrar_alfa_beta_pixel.py`).
- CN-2 e CN-3, e a calibração de λ por evento / AMC: só comparação. Fixos: **CN-1 (seco), λ = 0,05**.
- Correção de MDE / flowacc, `_diagnostico_*`, `_calibrar_*`, grade 2×2 da seção 11.
- Modelo concentrado (`SY = c·(D·qp)^0,56`) só aparece na planilha comparativa, não é parte do mapa.

## 1. Entradas

Fixas (já prontas, iguais para todos os eventos; vêm do Drive em `Dados Iniciais/`):

| Insumo | Arquivo | Observação |
|---|---|---|
| S do cenário seco (CN-1) | `S - Seco.tif` | S em mm |
| K | `K_raster.tif` | solo (`Pedologia Alto.shp`), média 0,039 |
| C | `C_raster.tif` | uso do solo (`Uso Solo Alto.shp`), média 0,05 |
| LS | `LS_raster.tif` | Moore et al. (1991), média 0,536 |
| P | constante 1,0 | |
| Grade | 884×365, 30 m (900 m²), SIRGAS 2000 / UTM 23S | |

Do evento 11 (planilha `eventos_processados_manuais.xlsx`, aba `Sheet1`, **linha de índice 11**; só o evento 1 usa índice 0):

| Campo | Valor |
|---|---|
| `chuva_p1_mm` (posto DBT5) | 62,800003 |
| `chuva_p2_mm` (posto Campo Paulista) | 79,000002 |
| `Chuva_evento_mm` (R) | 74,039628 |
| `Intensidade_60min_mm/h` (RI) | 11,8 |
| `T_R_m3` (volume medido) | 2.436.681,6 m³ |
| `SYY_t` (sedimento medido) | 1821,7535 t |

## 2. Chuva espacializada (`spatialRain.py`)

1. CSV `ESTPLUV_11.csv`: dois pontos (DBT5 lon −46,4809 / lat −23,2646, P=62,8; Campo Paulista lon −46,760284 / lat −23,208778, P=79,0).
2. Reprojetar os pontos para o CRS do raster (UTM 23S, EPSG:31983).
3. IDW (`qgis:idwinterpolation`), expoente 2, pixel 30 m, extensão do `CN TCC.tif` → `ChuvaIDW11.tif` (P em mm por pixel).

Conferência: com só dois postos, P em cada pixel fica entre 62,8 e 79,0 mm (IDW não extrapola). Dá para checar um pixel à mão: `P = (62,8/d1² + 79,0/d2²) / (1/d1² + 1/d2²)`.

## 3. Escoamento Q por pixel — **simulado**

Alinhar `S - Seco.tif` à grade da chuva (vizinho mais próximo) e, em cada pixel:

```
Ia = 0,05 · S
Q (mm) = 0                          se P ≤ Ia
Q (mm) = (P − Ia)² / (P + 0,95·S)   se P > Ia
```

Saída: `Q11_CN1.tif`. Volume da bacia: `V_calc = Σ Q/1000 · 900` (m³), comparar com `T_R_m3`.

## 4. Do Q ao sedimento — **simulado** (`calcular_pr_pixel.py` → `calcular_e_unit.py` → `calcular_sy_final.py`)

Para cada pixel válido (Q, K, C, LS todos com dado):

```
pr (m³/s) = [Q/1000 · 900] · (RI / R) / 3600        com RI/R = 11,8 / 74,039628 = 0,15937 /h
E_unit (t) = 11,8 · (Q · pr · 900)^0,56 · K · C · P · LS      (Q em mm, pr em m³/s, 900 em m²)
SY_sim (t) = c · Σ E_unit                                   c = 0,109049
```

Observações para a conferência: `RI` e `R` são escalares por evento (iguais em todos os pixels); o 11,8 do expoente de Williams é o coeficiente do artigo de Hao et al. (2022), usado em escala de bacia (ver seção 14.3 das notas). O raster `SY11.tif` é `c · E_unit11` por pixel.

## 5. Q **forçado** ao volume medido (`calcular_sy_volume_restrito.py`)

1. Fator do evento: `f = T_R_m3 / V_calc`.
2. `Q_obs = Q · f` em cada pixel.
3. Limite físico: se `Q_obs > P` (chuva do pixel em `ChuvaIDW11.tif`), `Q_obs = P`.
4. Refazer o passo 4 com `Q_obs` no lugar de `Q`:
   ```
   pr_obs = [Q_obs/1000 · 900] · (RI/R) / 3600
   E_obs  = 11,8 · (Q_obs · pr_obs · 900)^0,56 · K · C · P · LS
   SY_forçado = c_obs · Σ E_obs                              c_obs = 0,140844
   ```

Saídas: `Q11_CN1_obs.tif`, `pr11_obs.tif`, `E_unit11_obs.tif`, `SY11_obs.tif`.

## 6. Valores esperados (do `comparacao_SY_previsao_vs_restrito.csv`)

| Grandeza | Simulado | Forçado |
|---|---|---|
| Σ E_unit (t) | 6.881,90 | 8.634,27 |
| c | 0,109049 | 0,140844 |
| SY do modelo (t) | 750,46 | 1.216,09 |
| SY medido (t) | 1.821,75 | 1.821,75 |
| Erro | −58,8% | −33,2% |

Checagens intermediárias (para achar onde diverge, se divergir):
- `Σ E_unit_obs / Σ E_unit_sim = 1,2547`. Como `E ∝ Q^(2·0,56) = Q^1,12`, isso implica `f` por volta de 1,2 (estimativa; o teto Q ≤ P e a não linearidade pixel a pixel mexem um pouco). Logo `V_calc` deve ficar na casa de 2,0 milhões de m³, abaixo dos 2,44 milhões medidos.
- Os rasters não estão no git; os números acima de Q, f e V_calc dependem de rodar o passo 3 e **ainda não foram registrados** em nenhum arquivo do repositório. Anote os seus.

## 7. Atenção ao comparar à mão

- **`c` não se recalcula só com o evento 11**: vem de uma regressão pela origem nos 17 eventos (`c = Σ(ΣE·SY_obs) / Σ(ΣE²)`). Para a conferência, usar os `c` finais acima. Para reproduzir o `c`, é preciso rodar o passo 4 (ou 5) nos 17 eventos e as somas Σ E_unit de cada um estão na mesma tabela do CSV.
- O evento 11 é, nos dois casos, **subestimado**: simulado por causa do volume do CN-SCS; forçado porque o volume já bate e o resto do erro vem do `c` global e da estrutura espacial. Ver seção 12 das notas.
- O Q do evento 11 usa CN-1 para todos os eventos; nenhuma escolha de AMC por evento.
