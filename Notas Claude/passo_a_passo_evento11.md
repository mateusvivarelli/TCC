# Passo a passo manual — Evento 11 (simulado e forçado)

Para fazer sozinho, com QGIS + Google Sheets. Cada passo diz **onde** (QGIS ou Sheets), **de onde vem o dado**, **qual ferramenta** e **qual fórmula**. O resultado final do evento 11 deve bater com a seção 9.

Convenções: fórmulas do Sheets em sintaxe **pt-BR** (`;` separa argumentos, vírgula decimal). Se a planilha estiver em inglês, troque `;` por `,`, `RAIZ` por `SQRT`, `SE` por `IF`, `MÁXIMO` por `MAX`, `MÍNIMO` por `MIN`, `E`/`OU` por `AND`/`OR`, e use ponto decimal. Camadas do QGIS aparecem entre aspas na Calculadora Raster como `"nome@1"`.

---

## 0. Preparação

**0.1 Arquivos (Drive → `C:\TCC`)**: `Dados Iniciais/` com `eventos_processados_manuais.xlsx`, `S - Seco.tif`, `K_raster.tif`, `C_raster.tif`, `LS_raster.tif`, `CN TCC.tif`; e `Evento 11/EstPluv11.shp` (já no git). Os rasters pesados vêm do Drive (ver README, junctions).

**0.2 Projeto QGIS**: novo projeto, CRS do projeto = **EPSG:31983 (SIRGAS 2000 / UTM 23S)**. Adicione `CN TCC.tif`, `S - Seco.tif`, `K_raster.tif`, `C_raster.tif`, `LS_raster.tif`.

**0.3 Grade de referência**: abra *Propriedades → Informação* de `CN TCC.tif` e anote tamanho (884 × 365), resolução (30 m) e origem (canto superior esquerdo, ~X=318.646,35 / Y=7.435.057,59). Todos os rasters seguintes têm de ter essa grade.

**0.4 Google Sheets**: crie uma planilha com 4 abas: `Evento11`, `Pixels`, `Totais`, `Calibracao17` (preenchidas nos passos abaixo).

---

## 1. Entradas do evento (SHEETS, aba `Evento11`)

Abra `eventos_processados_manuais.xlsx` (aba `Sheet1`). **A linha do evento 11 é a de índice 11**, coluna A (`Unnamed: 0`) = 11; só o evento 1 usa índice 0. Digite na aba `Evento11` (coluna A = nome, coluna B = valor):

| Célula | Nome | Valor | Coluna da planilha de origem |
|---|---|---|---|
| B2 | P DBT5 (mm) | 62,800003 | `chuva_p1_mm` |
| B3 | P Campo Paulista (mm) | 79,000002 | `chuva_p2_mm` |
| B4 | R (mm) | 74,039628 | `Chuva_evento_mm` |
| B5 | RI (mm/h) | 11,8 | `Intensidade_60min_mm/h` |
| B6 | V medido (m³) | 2436681,6 | `T_R_m3` |
| B7 | SY medido (t) | 1821,753506 | `SYY_t` |
| B8 | Área do pixel (m²) | 900 | 30 m × 30 m |
| B9 | λ | 0,05 | calibrado na Fase 1 |
| B10 | α | 11,8 | Williams (1975) / Hao et al. (2022) |
| B11 | β | 0,56 | idem |
| B12 | P (MUSLE) | 1 | constante |
| B13 | c simulado | 0,10904894 | calibração nos 17 eventos (passo 8) |
| B14 | c forçado | 0,14084438 | idem |
| B15 | X0 (m) | 318646,35 | origem da grade (passo 0.3) |
| B16 | Y0 (m) | 7435057,59 | idem |
| B17 | resolução (m) | 30 | idem |
| B18 | X DBT5 (m) | 348520,849 | `EstPluv11.shp`, UTM 23S |
| B19 | Y DBT5 (m) | 7426415,273 | idem |
| B20 | X Campo (m) | 319862,370 | idem |
| B21 | Y Campo (m) | 7432277,543 | idem |

(Coordenadas dos postos: abra a tabela de atributos de `EstPluv11.shp`, ou rode a calculadora de campo com `$x`/`$y`; o posto de cima em lon −46,4809 é DBT5.)

Fórmulas escalares (na mesma aba):

| Célula | O que é | Fórmula |
|---|---|---|
| B24 | **RI/R (1/h)** | `=B5/B4`  → 0,159374 |
| B25 | R conferido | `=0,307*B2+0,693*B3`  → 74,03 (confere com B4; pesos 0,307/0,693 arredondados) |
| B26 | RI conferido | `=MÁXIMO(11,8; 9,4)`  (colunas `i60_p1_mm/h` e `i60_p2_mm/h`) → 11,8 |

**O que é RI/R:** fração da chuva total que cai na hora mais intensa (RI = intensidade máx. de 60 min; R = lâmina total do evento). É um número por evento, igual para todos os pixels; entra em `pr`.

---

## 2. Chuva espacializada P (QGIS)

Ferramenta: **Caixa de Ferramentas de Processamento → Interpolação → Interpolação IDW** (`qgis:idwinterpolation`).

1. Camada de entrada: `EstPluv11` (campo **`P`**, atributo de interpolação).
2. Coeficiente de distância: **2**.
3. Extensão: `CN TCC.tif`. Tamanho do pixel: **30**.
4. Saída: `Evento 11/ChuvaIDW11.tif`.

Conferência: P em qualquer pixel fica entre 62,8 e 79,0 mm; próximo ao exutório (perto do posto Campo Paulista) fica em ~79.

Se o `EstPluv11.shp` não estiver no CRS UTM, reprojete (ferramenta **Reprojetar camada**, EPSG:31983) antes.

---

## 3. S na grade da chuva (QGIS, só se as grades diferirem)

`S - Seco.tif` (S em mm, cenário CN-1 seco). Se a grade não for idêntica à de `ChuvaIDW11`:
**Ferramenta:** *Raster → Projeções → Deformar (reprojetar)* (GDAL Warp), reamostragem **vizinho mais próximo**, CRS 31983, resolução 30, extensão de `ChuvaIDW11`. Saída: `S_alinhado.tif`. Repita para `K`, `C`, `LS` se alguma não tiver 884×365.

(O valor de S vem do CN do projeto: `S = 25400/CN − 254`. A origem dos valores de CN ainda não está documentada nas notas.)

---

## 4. Q simulado (QGIS)

**Ferramenta:** *Raster → Calculadora Raster*.

```
("ChuvaIDW11@1" > 0.05*"S - Seco@1") * (("ChuvaIDW11@1" - 0.05*"S - Seco@1")^2 / ("ChuvaIDW11@1" + 0.95*"S - Seco@1"))
```

Fórmula física: `Ia = λ·S`; `Q = 0` se `P ≤ Ia`; senão `Q = (P − Ia)² / (P + (1−λ)·S)`. Unidade: mm. Saída: `Q11_CN1.tif`.

### 4.1 Máscara de pixels válidos (QGIS)

Só são usados os pixels onde Q, K, C e LS têm dado (como nos scripts). Na Calculadora Raster:

```
"Q11_CN1@1" + 0*"K_raster@1" + 0*"C_raster@1" + 0*"LS_raster@1"
```

Saída: `Q11_CN1_m.tif`. **Use este raster nos próximos passos.** (Pixels de água/urbano têm C = 0, mas continuam válidos.)

---

## 5. Totais do volume e fator f (QGIS → SHEETS)

**5.1 QGIS** — **Estatísticas da camada raster** (`native:rasterlayerstatistics`) sobre `Q11_CN1_m.tif`: anote **SOMA** e **CONTAGEM**.

**5.2 SHEETS, aba `Totais`** (col. A nome, col. B valor):

| Célula | O que é | Valor / fórmula |
|---|---|---|
| B2 | N pixels válidos | contagem do QGIS |
| B3 | ΣQ (mm·pixel) | soma do QGIS |
| B4 | **V_calc (m³)** | `=B3/1000*Evento11!B8` |
| B5 | V medido (m³) | `=Evento11!B6` |
| B6 | Erro do volume (%) | `=100*(B4-B5)/B5` |
| B7 | **Fator f** | `=B5/B4` |

Referência: `f` ≈ 1,2 (estimativa; **anote o seu**, o repositório ainda não tem `V_calc` nem `f` do evento 11).

---

## 6. Simulado: pr, E_unit, SY (QGIS → SHEETS)

**6.1 pr simulado (QGIS)**, Calculadora Raster, com o RI/R da célula `Evento11!B24` (0,159374):

```
"Q11_CN1_m@1" / 1000 * 900 * 0.159374 / 3600
```

Saída `pr11.tif` (m³/s; é o pico **local** do pixel, não uma vazão de bacia).

**6.2 E_unit simulado (QGIS)**:

```
11.8 * ("Q11_CN1_m@1" * "pr11@1" * 900)^0.56 * "K_raster@1" * "C_raster@1" * 1 * "LS_raster@1"
```

Saída `E_unit11.tif`. Unidades como em Hao et al.: Q em mm, pr em m³/s, área em m².

**6.3 Soma de E (QGIS)**: Estatísticas da camada raster sobre `E_unit11.tif` → **SOMA** (esperado ≈ **6.881,90**).

**6.4 SY simulado por pixel (QGIS)**: `0.109049 * "E_unit11@1"` → `SY11.tif`.

**6.5 SHEETS, aba `Totais`**:

| Célula | O que é | Fórmula |
|---|---|---|
| B9 | ΣE_unit simulado (t) | soma do QGIS |
| B10 | **SY simulado (t)** | `=Evento11!B13*B9` → ≈ 750,46 |
| B11 | Erro (%) | `=100*(B10-Evento11!B7)/Evento11!B7` → ≈ −58,8% |

---

## 7. Forçado: Q·f, pr, E_unit, SY (QGIS → SHEETS)

**7.1 Q forçado (QGIS)**, com `f` da célula `Totais!B7` (troque `1.2183` pelo seu f):

```
( "Q11_CN1_m@1" * 1.2183 > "ChuvaIDW11@1" ) * "ChuvaIDW11@1" + ( "Q11_CN1_m@1" * 1.2183 <= "ChuvaIDW11@1" ) * "Q11_CN1_m@1" * 1.2183
```

Isto é `Q_obs = mín(Q·f, P)`: escoamento nunca passa da chuva do pixel. Saída: `Q11_CN1_obs.tif`.

**7.2 Pixels limitados à chuva (QGIS)**: Estatísticas da camada raster sobre `("Q11_CN1_m@1"*1.2183 > "ChuvaIDW11@1")` (salve esse raster booleano) → **SOMA** = nº de pixels limitados. (No evento 11 deve ser pequeno; o valor 0,48% é do conjunto dos 17 eventos, concentrado nos eventos 4 e 10.)

**7.3 pr forçado (QGIS)**: `"Q11_CN1_obs@1" / 1000 * 900 * 0.159374 / 3600` → `pr11_obs.tif`.

**7.4 E_unit forçado (QGIS)**:

```
11.8 * ("Q11_CN1_obs@1" * "pr11_obs@1" * 900)^0.56 * "K_raster@1" * "C_raster@1" * 1 * "LS_raster@1"
```

→ `E_unit11_obs.tif`. **Estatísticas**: SOMA (esperado ≈ **8.634,27**).

**7.5 SY forçado por pixel (QGIS)**: `0.140844 * "E_unit11_obs@1"` → `SY11_obs.tif`.

**7.6 SHEETS, aba `Totais`**:

| Célula | O que é | Fórmula |
|---|---|---|
| B13 | N pixels limitados | soma do QGIS (7.2) |
| B14 | ΣE_unit forçado (t) | soma do QGIS (7.4) |
| B15 | **SY forçado (t)** | `=Evento11!B14*B14` → ≈ 1216,09 |
| B16 | Erro (%) | `=100*(B15-Evento11!B7)/Evento11!B7` → ≈ −33,2% |
| B17 | ΣE forç. / ΣE sim. | `=B14/B9` → ≈ 1,2547 |

---

## 8. Recalcular c nos 17 eventos (SHEETS, aba `Calibracao17`)

`c` não vem do evento 11 sozinho. Dados (do `Dados Iniciais/comparacao_SY_previsao_vs_restrito.csv`; importe com *Arquivo → Importar*, ou copie as colunas):

| Coluna | Conteúdo |
|---|---|
| A | evento (1 a 17) |
| B | `SY_obs_t` |
| C | `soma_E_unit_previsao_t` (ΣE simulado) |
| D | `soma_E_unit_restrito_t` (ΣE forçado) |

Linhas 2 a 18 (17 eventos). Em células soltas:

| Célula | O que é | Fórmula |
|---|---|---|
| F1 | c simulado | `=SOMARPRODUTO(C2:C18; B2:B18)/SOMAQUAD(C2:C18)` → 0,109049 |
| F2 | c forçado | `=SOMARPRODUTO(D2:D18; B2:B18)/SOMAQUAD(D2:D18)` → 0,140844 |
| E2:E18 | SY sim. | `=$F$1*C2` |
| G2:G18 | SY forçado | `=$F$2*D2` |
| F3 | NSE sim. | `=1-SOMAXMY2(B2:B18; E2:E18)/DESVQ(B2:B18)` → 0,3714 |
| F4 | NSE forçado | `=1-SOMAXMY2(B2:B18; G2:G18)/DESVQ(B2:B18)` → 0,8052 |
| F5 | PBIAS sim. (%) | `=100*(SOMA(E2:E18)-SOMA(B2:B18))/SOMA(B2:B18)` → −21,28 |
| F6 | PBIAS forç. (%) | `=100*(SOMA(G2:G18)-SOMA(B2:B18))/SOMA(B2:B18)` → −0,99 |

(Em inglês: `SUMPRODUCT`, `SUMSQ`, `SUMXMY2`, `DEVSQ`, `SUM`.) O evento 11 está na linha 12: `E12` ≈ 750,46 e `G12` ≈ 1216,09.

Para refazer um dos 17 ΣE do zero, repita os passos 2 a 7 para aquele evento (o CSV do projeto serve de gabarito).

---

## 9. Conferência pixel a pixel (QGIS → SHEETS, aba `Pixels`)

Valida a fórmula em alguns pixels, sem depender dos totais.

**9.1 QGIS — escolher 6 pixels.** Escolha índices de coluna `j` (0 a 883) e linha `i` (0 a 364). Pixel central: `X = X0 + 30·(j + 0,5)`, `Y = Y0 − 30·(i + 0,5)` (a planilha calcula). Crie uma camada de pontos (*Camada → Nova camada temporária de pontos*) com esses 6 pontos nas coordenadas calculadas. Ferramenta: **Amostrar valores do raster** (`native:rastersampling`), uma vez por raster: `ChuvaIDW11`, `S - Seco`, `K_raster`, `C_raster`, `LS_raster`, `Q11_CN1`, `E_unit11`, `Q11_CN1_obs`, `E_unit11_obs`. Abra a tabela de atributos.

**9.2 SHEETS, aba `Pixels`** (linhas 2 a 7). Colunas:

| Col. | Conteúdo | Fórmula (linha 2) |
|---|---|---|
| A | id | 1, 2, … |
| B | j (coluna) | digitar |
| C | i (linha) | digitar |
| D | X (m) | `=Evento11!$B$15+Evento11!$B$17*(B2+0,5)` |
| E | Y (m) | `=Evento11!$B$16-Evento11!$B$17*(C2+0,5)` |
| F | dist. a DBT5 (m) | `=RAIZ((D2-Evento11!$B$18)^2+(E2-Evento11!$B$19)^2)` |
| G | dist. a Campo (m) | `=RAIZ((D2-Evento11!$B$20)^2+(E2-Evento11!$B$21)^2)` |
| H | P IDW (mm) | `=(Evento11!$B$2/F2^2+Evento11!$B$3/G2^2)/(1/F2^2+1/G2^2)` |
| I | S (mm) | amostrado de `S - Seco` |
| J | K | amostrado |
| K | C | amostrado |
| L | LS | amostrado |
| M | Q sim (mm) | `=SE(H2<=Evento11!$B$9*I2; 0; (H2-Evento11!$B$9*I2)^2/(H2+(1-Evento11!$B$9)*I2))` |
| N | pr sim (m³/s) | `=M2/1000*Evento11!$B$8*Evento11!$B$24/3600` |
| O | E_unit sim (t) | `=Evento11!$B$10*MÁXIMO(M2*N2*Evento11!$B$8; 0)^Evento11!$B$11*J2*K2*Evento11!$B$12*L2` |
| P | Q forçado (mm) | `=MÍNIMO(M2*Totais!$B$7; H2)` |
| Q | pr forçado | `=P2/1000*Evento11!$B$8*Evento11!$B$24/3600` |
| R | E_unit forçado | `=Evento11!$B$10*MÁXIMO(P2*Q2*Evento11!$B$8; 0)^Evento11!$B$11*J2*K2*Evento11!$B$12*L2` |
| S–W | valores do QGIS | `ChuvaIDW11`, `Q11_CN1`, `E_unit11`, `Q11_CN1_obs`, `E_unit11_obs` |
| X–AB | diferenças | `=H2-S2`, `=M2-T2`, `=O2-U2`, `=P2-V2`, `=R2-W2` (devem ser ≈ 0, até a precisão float32) |

Diferença de P (coluna X) maior que ~0,1 mm sugere que a interpolação usou outra configuração (expoente, extensão, CRS dos postos). Diferença em Q com P igual sugere S desalinhado (passo 3).

---

## 10. Resultado final e o que anotar

| Grandeza | Simulado | Forçado |
|---|---|---|
| Σ E_unit (t) | 6.881,90 | 8.634,27 |
| c | 0,109049 | 0,140844 |
| SY do modelo (t) | 750,46 | 1.216,09 |
| SY medido (t) | 1.821,75 | 1.821,75 |
| Erro | −58,8% | −33,2% |

**Anote e traga de volta** (ainda não estão no repositório): `V_calc`, `f`, pixels limitados à chuva, os 6 pixels de amostra (j, i, P, S, K, C, LS, Q, E). Se algum valor diferir da tabela, as diferenças da seção 9 apontam onde.

## 11. O que ficou de fora (de propósito)

Qp/hidrograma unitário (Fase 1), IC/FCI/DSC, α e β livres, CN-2/CN-3, calibração de λ por evento, correção do MDE, modelo concentrado, diagnósticos. Nenhum alimenta os mapas finais; ver `roteiro_evento11_manual.md`.
