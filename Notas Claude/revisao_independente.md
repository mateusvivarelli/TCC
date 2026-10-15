# Revisão técnica independente: MUSLE espacializada, Alto Jundiaí

Revisor independente (hidrologia, erosão e modelagem). Data: 15/10/2026. Escopo: dados, código, estatística, citações e
coerência entre documentos, antes da redação. As notas não foram tomadas como verdade: tudo o que aparece como
"recalculado" foi refeito a partir da série horária, das planilhas e dos rasters (17 eventos; Drive montado), com
scripts temporários em `C:\Users\sonek\AppData\Local\Temp\claude\revisor\` (r03 a r10). Nenhum arquivo do projeto
foi alterado.

---

## (a) Resumo executivo

1. A cadeia numérica está correta e é reprodutível. Refiz IDW, Q, pr, E_unit, SY, c, NSE, LOO, WIA e PBIAS para os 17 eventos e todos batem com o publicado (diferença máxima de 1e-5).
2. O problema está nas definições. `T_R_m3` não é escoamento direto: é o volume **total** (ΣQ·3600, incluindo a vazão de base). Pela coluna `Bt` da própria série horária, a vazão de base responde por 34–55% desse volume.
3. Assim, o par "CN-I + λ=0,05 com erro de +0,5%" foi calibrado contra a vazão total. Contra o volume direto, o PBIAS é de +96% e o NSE do volume é −6,1. O λ que zera o viés contra o volume direto é ≈0,18, ou seja, próximo do padrão 0,20.
4. Um modelo trivial, SY = c·T_R_m3 (1 parâmetro, sem MUSLE e sem mapa), dá NSE 0,809 e LOO 0,765, com erro absoluto de 19%. Isso empata com a versão "volume restrito" (0,805 e 0,776, erro de 27%).
5. A afirmação de que "com hidrologia boa a estrutura espacial atinge 0,78–0,81" não se sustenta. O desempenho vem do volume medido, que entra também no próprio SY observado (SYY_t = ΣQ·CSS).
6. A previsão pura (NSE 0,37, LOO 0,28) perde para SY = c·Chuva_evento (0,67 e 0,61) e até para SY = c·Vol_SCS (0,42 e 0,36). O ρ de Spearman é 0,55 e o log-NSE é −0,27.
7. A estatística é frágil. Só o evento 15 responde por 49% da variância: sem ele, o NSE da previsão pura cai para −0,21 (LOO −0,31). O intervalo de confiança de 95% do NSE por bootstrap vai de −1,63 a 0,80.
8. A linha 1B da planilha (um evento real) é descartada em todos os scripts sem justificativa escrita. Com ela, o NSE cai para 0,25 (LOO 0,16).
9. Ainda há afirmações exageradas não corrigidas: "supera Hao/Baert" no README, na seção 13 das notas e no `Relatorio_Resultados_TCC.pdf`, e "acima do teto de 0,66 de Baert". As justificativas de λ=0,05 (Brandão, Valle Junior) não se aplicam como estão escritas.
10. O mapa médio é, na prática, um mapa de K·C·LS (r=0,88; Spearman 0,92), e o r=0,994 decorre da construção. O TCC continua defensável como **produto de mapeamento com validação agregada fraca**, desde que o texto mude de tom e as limitações sejam declaradas com estes números.

---

## (b) Achados

Severidade: **C** = crítico (pode invalidar uma conclusão), **I** = importante (enfraquece, a banca ataca), **M** = menor.

### 1. [C] `T_R_m3` é o volume total do rio, não o escoamento direto

**Evidência (recalculada, r03):** para as 18 linhas de `eventos_processados_manuais.xlsx`:

- `T_R_m3` = Σ Q·3600 sobre [Inicio, Fim] na série horária, exatamente. Também é igual a Q_mean · N_horas · 3600. Exemplo, evento 15: 7,925669 × 150 × 3600 = 4.279.861 m³.
- `Ris_R_m3` e `Fall_R_m3` são apenas a divisão do hidrograma no pico: o ramo ascendente inclui a hora do pico, o descendente vem depois. Não há separação de vazão de base.
- A série horária tem a coluna `Bt_... (m3/s)`, que é a vazão de base.

Parcela de base no `T_R_m3`:

| Método de separação | Faixa entre eventos |
|---|---|
| Coluna `Bt` da série | 34% (ev. 2) a 55% (ev. 10) |
| `Qb_inicio` constante | 13% a 44% |

Os documentos dizem o contrário:

- `notas_qgis_calibracao_qp.md` l.16–17 e l.62–64: "volume total de escoamento direto, já separado de base".
- Apostila, tabela de dados do cap. 3: "Volume de escoamento direto do evento".
- `base_para_redacao_tcc.md` §1.1.
- `Resultados_Calibracao_TCC.xlsx`, aba "Volume (Q)", A1.

**Consequências (recalculadas com os rasters, r06 e r10):**

- **Contra o volume direto (T_R − base), CN-I com λ=0,05 erra muito.**

  | Métrica | Valor |
  |---|---|
  | PBIAS | +95,7% |
  | Erro médio | +92% |
  | Erro absoluto médio | 121% |
  | NSE do volume | −6,1 |

- **O λ adequado ao volume direto fica perto do padrão.** O λ que reproduz o volume direto evento a evento tem mediana ≈0,18 (14 eventos com solução). λ=0,20 dá PBIAS de −11% contra o volume direto.
- **O "+0,5%" esconde que o ajuste é fraco mesmo contra o volume total.** Contra `T_R_m3`, o NSE do volume com λ=0,05 é só 0,18.
- **Os "5 eventos impossíveis" (1, 2, 4, 7, 10) viram 3 (2, 4, 10)** quando o alvo é o volume direto.
- **O volume restrito força o Q direto do SCS-CN a igualar o volume total.** Os fatores f ficam cerca de 2× maiores do que seriam contra o escoamento direto. Exemplo, evento 10: f = 6,9 contra o total e 3,1 contra o direto.
- **Calibrar contra o volume direto piora o SY.** Com o λ que zera o viés contra o direto (0,18), a previsão pura de SY cai para NSE −0,03 (LOO −0,69); com λ=0,20, NSE −0,10. Logo, o NSE 0,37 depende de o λ compensar a vazão de base.

**Por que importa:** é a premissa da Fase 1 inteira e da versão restrita. Uma banca de hidrologia nota que o SCS-CN estima escoamento direto, e que Brandão (2025) e Valle Junior (2019) usam escoamento direto separado; Valle Junior usou o filtro de Eckhardt.

**Como corrigir:** escolher uma das duas saídas e declarar no texto.

- (a) Separar a base, com a coluna `Bt` ou outro filtro citado, recalibrar o volume e refazer a versão restrita com o volume direto. Pela aproximação f^1,12 (r04), a versão restrita contra o direto dá NSE 0,76 e LOO 0,71.
- (b) Manter como está, mas dizer explicitamente que o "Q" do modelo representa o volume total do evento. Nesse caso, λ=0,05 com CN-I é um ajuste empírico que absorve a vazão de base, não uma validação de λ. A palavra "escoamento direto" sai de todo o texto.

### 2. [C] Um modelo trivial empata com o volume restrito, e outros superam a previsão pura

**Evidência (r04).** Todos os modelos têm um parâmetro, ajustado pela origem, nos mesmos 17 eventos.

| Modelo | NSE | NSE LOO | Erro abs. médio | Spearman |
|---|---|---|---|---|
| Espacializada, previsão pura (adotada) | 0,371 | 0,282 | 44,4% | 0,55 |
| SY = c·Vol_CN1 (só volume do SCS-CN, sem MUSLE) | 0,416 | 0,361 | 42,6% | 0,65 |
| **SY = c·Chuva_evento_mm** | **0,671** | **0,605** | 55,8% | 0,69 |
| Espacializada, volume restrito | 0,805 | 0,776 | 26,7% | 0,79 |
| **SY = c·T_R_m3 (sem MUSLE, sem mapa)** | **0,809** | **0,765** | **19,1%** | **0,88** |
| Concentrada, (T_R·Q_pico)^0,56 | 0,848 | 0,799 | 28,6% | 0,93 |
| SY = a·T_R^b (log-log, 2 parâmetros) | — | 0,768 | — | — |

**Leitura:**

- O SY observado é Σ Q·CSS, que compartilha a vazão com `T_R_m3`: r(SY, T_R) = 0,906. É uma curva-chave de sedimento por evento.
- O volume restrito não acrescenta nada mensurável ao volume medido, e piora o erro absoluto (27% contra 19%).
- A previsão pura fica abaixo da chuva bruta: a estrutura MUSLE (pr, K, C, LS, expoente 0,56) reduz a capacidade preditiva no exutório.

**Afirmações que caem:**

- Notas §12.2, apostila p.~33, `base_para_redacao` §5.2 e `Relatorio_Resultados` §"Superam": "a estrutura espacial está correta — com hidrologia boa atinge 0,78–0,81".
- "a espacialização entrega o mapa de graça".
- "acima do teto de Baert".

**Como corrigir:**

- Incluir estes benchmarks na aba Resumo de `Comparacao_Modelos_TCC.xlsx` e no texto.
- Reescrever a conclusão: a validação no exutório **não discrimina** a estrutura espacial. O mapa é coerente por construção, não validado.
- Afirmação defensável: "no exutório, o SY por evento é explicado sobretudo pelo volume escoado; a MUSLE espacializada não supera índices simples de chuva/volume".

### 3. [C] A amostra é pequena e o NSE depende de um único evento

**Evidência (r04):**

- O evento 15 responde por **48,7%** de Σ(O − Ō)².
- Sem o evento 15, a previsão pura dá NSE **−0,21** (LOO −0,31); a versão restrita dá 0,62 (LOO 0,56).
- Bootstrap de eventos (2000 reamostragens, reajustando c), intervalo de confiança de 95% do NSE in-sample:
  - previsão pura: [−1,63; 0,80];
  - restrita: [0,22; 0,95].
- Log-NSE: previsão pura −0,27; restrita 0,84.

**O LOO é otimista.** A escolha do cenário AMC (CN-I entre 3), do λ (0,05) e a exclusão do 1B (achado 4) foram feitas olhando os mesmos 17 eventos. O LOO só reajusta c, então não é validação independente.

**Por que importa:** frases como "espacial 0,37 vs concentrado 0,44 → espacializar não degrada" não têm poder estatístico com n=17. O NSE 0,37 da previsão pura é essencialmente o acerto do evento 15. Pelos critérios de Moriasi et al. (2007), citados em Valle Junior (2019), NSE ≤ 0,50 é "insatisfatório".

**Como corrigir:** reportar junto com o NSE:

- o NSE sem o evento 15 (ou o log-NSE, que é a métrica de calibração de Hao, Eq. 11);
- o intervalo de bootstrap;
- o Spearman.

Declarar que λ e o cenário AMC foram escolhidos dentro da amostra.

### 4. [C/I] O evento 1B é descartado sem justificativa

**Evidência:**

- `eventos_processados_manuais.xlsx` tem 18 eventos: 1A, 1B e 2 a 17. A planilha `eventos_definidos_artigo_I4SDWI_corrigido.xlsx` também tem 18.
- **Todos** os scripts usam `iloc[0 if n == 1 else n]`, descartando a linha 1 (1B): `calcular_pr_pixel.py` l.32, `calcular_sy_final.py` l.38–42, `calcular_sy_volume_restrito.py` l.43–44, `excelReader.py` l.9–10 e diagnósticos. O mapeamento é coerente entre scripts e com os `ESTPLUV_n.csv` (verificado).
- A apostila só diz que "o evento 1 do trabalho é a linha 1A". Não há motivo escrito em lugar nenhum.

**Recalculei o 1B do zero (r09)**, com o mesmo IDW, S-Seco, λ, K, C e LS; o mesmo procedimento reproduz o 1A exatamente:

| Grandeza | Modelo | Observado | Erro |
|---|---|---|---|
| Volume | 267 mil m³ | `T_R` 1,39 milhão m³ | −81% |
| SY (com c) | ≈155 t | 1.349 t | −88% |

| Conjunto de eventos | NSE | NSE LOO |
|---|---|---|
| 17 eventos (atual) | 0,37 | 0,28 |
| 18 eventos (com 1B) | 0,254 | 0,158 |
| 17 eventos com 1B no lugar de 1A | 0,16 | 0,05 |
| SY = c·T_R, 18 eventos | 0,80 | 0,76 |

O modelo trivial é robusto à inclusão; a previsão pura não.

**Por que importa:** excluir sem critério um evento mal ajustado configura seleção de amostra.

**Como corrigir:** documentar o critério. Por exemplo, se 1B é continuação do 1A com base elevada (`Qb_inicio` de 2,15 m³/s), ou se o artigo da IC usou 17 eventos com esse critério. Ou incluir o 1B e reportar com 18.

### 5. [I] A justificativa de λ=0,05 e do CN-I fixo não se aplica como está escrita

**Evidência:**

- **CN de origem não documentada.** `CN TCC.tif` (CN-II) tem classes de 52 a 98, origem não registrada (a nota §14.7 admite).
- **Fórmulas de conversão confirmadas.** O CN-I veio de 4,2·CN/(10 − 0,058·CN) e o CN-III de 23·CN/(10 + 0,13·CN); ambos conferem com os rasters (diferença < 4e-6). S = 25400/CN − 254 também confere. Essas são as fórmulas do NEH-4 / Chow et al. (1988) e devem ser citadas.
- **Os CN tabelados pressupõem λ=0,20.** Brandão et al. (2025) mostram que, para λ=0,05, o CN tem de ser convertido para valores menores e fornecem equações de conversão. Valle Junior (2019) obteve CN de 17,7 a 44,3 com λ=0,05 calibrado na própria bacia, com escoamento direto separado por filtro de Eckhardt.
- **O que o TCC faz é outra coisa:** CN tabelado → CN-I → λ=0,05 sem conversão. É uma compensação empírica, não a aplicação de Brandão. A frase "Brandão valida diretamente nossa escolha" (notas §8.1) está exagerada.
- **Baert et al. (2026) dizem o oposto** sobre λ fixo baixo: "lower fixed values increased runoff-initiation frequency but strongly overestimated runoff volume. The difficulty was therefore not resolved by selecting a universally lower abstraction ratio" (§4.1).
- **Os documentos se contradizem sobre a origem de λ:**
  - apostila, FAQ 3: "λ = 0,05 veio da literatura e por coincidência zerou o viés";
  - `projeto_tcc_atualizacao_09-2026.md` l.28–30: "recalibradas de λ=0,2 para λ=0,05 a partir do ajuste aos 17 eventos";
  - comentário em `spatialRain.py` l.19–26: "calibrado".

**Como corrigir:**

- Declarar CN-I + λ=0,05 como **par escolhido empiricamente** nos 17 eventos, contra a vazão total (achado 1).
- Citar Brandão e Valle Junior só como contexto de que λ < 0,2 é comum, com a ressalva da conversão de CN.
- Citar a frase de Baert como limitação.
- Registrar a fonte do CN-II.

### 6. [I] Na razão RI/R, numerador e denominador vêm de bases diferentes

**Evidência (r03, r09):**

- `Intensidade_60min_mm/h` = max(i60_p1, i60_p2): é o máximo entre os dois postos (verificado nas 18 linhas).
- `Chuva_evento_mm` é a média ponderada (peso implícito do DBT5 = 0,3062 em 17 linhas; 0,318 no evento 16).
- RI/R passa de 1/h nos eventos 1 (1,010) e 12 (1,382; DBT5 = 0 mm), o que é fisicamente impossível para uma chuva só.
- Usando RI = máximo horário da série **ponderada** (coerente com R), a previsão pura vai de NSE 0,371 / LOO 0,282 para **0,368 / 0,244**.
- Hao et al. interpolam RI e R como rasters com IDW de 26 postos (p.4).

**Como corrigir:** usar RI e R da mesma série (ponderada ou IDW por pixel) e reportar a sensibilidade.

### 7. [I] O "SY por pixel" é erosão bruta escalonada, não produção de sedimentos

**Evidência:**

- Com c constante, SY_k = c·E_unit,k impõe uma razão de entrega espacialmente uniforme.
- Hao et al. (2022) mostram o contrário: em média 43,61% da área tem "mismatch" entre erosão e conectividade (§4.2).
- 18,8% da bacia tem E = 0 porque K = 0 (13,7%) ou C = 0 (14,3%); a sobreposição é parcial (K = 0 e C > 0 em 4,5%) (r09).
- O mapa médio correlaciona com K·C·LS com r = 0,883 (Spearman 0,922). 70,8% dos hot spots (top 5%) coincidem com o top 5% de K·C·LS sozinho (r06).
- O r = 0,994 e os 96,9% entre os mapas "previsão" e "restrito" são consequência da construção. A nota §14.6 já reconhece isso, mas o README (l.86) e o `Relatorio_Resultados` ainda apresentam como "resultado de robustez".

**Como corrigir:**

- Rotular o mapa como "erosão potencial local escalonada ao total medido".
- Declarar que o padrão espacial é dominado por K, C e LS, que a chuva de 2 postos contribui pouco, e que não há validação espacial.
- Retirar "robustez" como resultado.

### 8. [I] Afirmações sobre a literatura que continuam exageradas ou mal atribuídas

Documentos ainda não corrigidos (a correção de 02/10 só chegou a `base_para_redacao` e à apostila):

- `README.md` l.85: "Supera o patamar de Hao et al. (2022) (NSE > 0,70, WIA > 0,89)."
- `notas_musle_espacializada.md` §13, l.571–572: "atinge e supera esse patamar".
- `Relatorio_Resultados_TCC.pdf` (texto l.191–197): "a) Superam o artigo de referência… b) Superam o benchmark mais recente (Baert)".

Outros pontos:

- **"Teto" de Baert.** Notas §12.2 (l.496–497) e §8.2: "acima do teto de 0,66 de Baert". Baert não fala em teto. O 0,66 é validação cruzada 5-fold (calibração 0,72), em 46 eventos, numa bacia de 0,84 km², com MUSLE concentrada, α calibrado e β = 0,56 (Tabela 10). Além disso, o nosso 0,78 é igual ao do modelo trivial `T_R` (achado 2).
- **Espacialização em Baert.** Notas §8.2 (l.440–441): "eles nem tentam espacializar o pico, só o volume". O SCS-CN de Baert é concentrado ("lumped catchment-scale effective rainfall", §4.3): nada é espacializado.
- **"Precedente direto" de Baert para o volume restrito.** `calcular_sy_volume_restrito.py` l.15–17 ("exatamente essa configuração"), notas §12.5 e §13, `base_para_redacao` §3.4. Baert usa volume **e pico** observados numa MUSLE concentrada. Aqui entram o volume total observado e o pr modelado, por pixel. Dá para chamar de precedente conceitual, não de "exatamente".
- **Faixa de FCI₀ em Hao.** Notas §9, l.293–294: "FCI₀ entre −2,33 e −4,79". A Tabela 4 de Hao traz 2,33 / 4,79 / **2,02** (Xiangshui omitido; o sinal se perdeu na extração). A apostila está correta: |FCI₀| de 2,0 a 4,8.
- **Erros "consistentes com Baert".** `projeto_tcc_atualizacao_09-2026.md` l.53–55: "magnitudes de erro consistentes com… Baert". Baert não reporta erro percentual médio de volume e pico (reporta NSE, KGE, PBIAS e RRMSE); a afirmação não tem respaldo. O mesmo documento descreve FCI/DSC como o método aplicado (abandonado) e mantém "Simulação de cenários" no cronograma (l.78), embora tenha sido cortada.
- **"Faixa documentada" do fator de pico.** Notas_qgis §3.10 (l.555–562), `spatialPeakFlowHU_convolucao.py` l.59–68 e `Resultados_Calibracao_TCC.xlsx` (Resumo A7 e A20) citam "PRF 100–300 em alguns manuais" sem referência. Mais importante: no NRCS, PRF baixo vem com um hidrograma unitário redesenhado (recessão mais longa) que conserva o volume. Aqui o triângulo mantém Tb = 2,67·Tp com k = 1,1184, e o hidrograma perde 46% do volume (1,1184/2,08 = 0,538). A nota §14.5 já diz isso; os demais documentos não.

**Como corrigir:** harmonizar todos os documentos com a §14 das notas e com o achado 2.

### 9. [I] A escala de E_unit é arbitrária, mas o README a interpreta fisicamente

**Evidência:**

- Q (mm) × A (m²) = 1000 × volume (m³). Isso põe um fator 1000^0,56 ≈ 47,9 em relação às unidades de Williams (1975), que usa Q em m³ e qp em m³/s.
- Em unidades de Williams, ΣE_unit < SY_obs em todos os eventos (c ≈ 5,2).
- O README (l.154) diz que "E_unit sempre > sedimento medido… faz sentido fisicamente". Isso é artefato de unidade. A nota §14.3 reconhece o fator, mas o README não foi corrigido.
- Na mediana do evento 11, Q·pr·A vale 7,3 (mm·m³/s·m²); em unidades de Williams, 0,0073.

**Como corrigir:** retirar a frase do README e não interpretar c como razão de entrega. A apostila, FAQ 7, já faz isso corretamente.

### 10. [I] O pico da Fase 1 tem inconsistências internas

Pesa menos porque o pico não entra no mapa.

**Evidência (`spatialPeakFlowHU_convolucao.py`):**

- O SCS-CN é aplicado de forma **concentrada**, com S médio = 255,69 mm sobre a chuva ponderada (l.79–84, l.163–171). O volume é espacial. Pela não linearidade, as duas abordagens não geram o mesmo escoamento.
- O `Q_pico` medido inclui a vazão de base (`Qb_inicio` de 0,9 a 2,7 m³/s, isto é, 4–25% do pico), e o modelo não.
- O fator de pico foi ajustado minimizando o erro percentual absoluto nos mesmos 17 eventos. O viés resultante é de −38,4%.
- O tempo de resposta empírico (`tempo_resposta_empirico_por_evento.csv`) varia de 2 a 27 h (pico a pico), contra Tp = 6,89 h.

**Como corrigir:** declarar estas limitações. No texto, apresentar a Fase 1 do pico como "verificação de ordem de grandeza", não como calibração validada.

### 11. [M] Área do pixel, máscaras e grades não são uniformes

**Evidência (r05, r06):**

**Área do pixel**

- `spatialRain.py` (l.487–491) e `_calibrar_lambda_por_evento.py` (l.27) usam 900 m², o que dá volume +0,28%. Isso alimenta o "+0,5%" e o CSV de volumes.
- Os scripts da Fase 2 usam 897,49 m².

**Pixels válidos por camada**

| Camada | Pixels válidos |
|---|---|
| Q | 154.667 |
| K e C | 154.737 |
| LS | 154.759 |
| K·C·LS | 154.445 |
| E_unit e SY | 154.011 |

**Áreas da bacia que aparecem nos documentos**

| Origem | Área (km²) |
|---|---|
| Acumulação de fluxo corrigida | 137,80 |
| Área usada no HU-SCS | 138 |
| Máscara rasterizada | 138,86 |
| Máscara do E_unit | 138,22 |

**Grades**

- `S - Seco.tif` e `CN TCC.tif` estão numa grade de 973×362 pixels de 27,25×30,17 m (822 m²). São reamostrados por vizinho mais próximo para 884×365.

Efeito total < 1%, mas convém uniformizar e citar a área do pixel uma vez só.

### 12. [M] O IDW extrapola, e a ponderação dos postos tem pontos soltos

**Evidência (r06):**

- O IDW com potência 2 foi reproduzido exatamente (diferença 0).
- O peso médio do DBT5 dentro da bacia é **0,34** no IDW, contra 0,306 na `Chuva_evento_mm`. A média IDW na bacia difere de R (ev. 12: 22,58 contra 23,73 mm; ev. 15: 136,8 contra 139,4 mm).
- O peso "0,307 ajustado por mínimos quadrados" (notas_qgis §3.6, apostila) só recupera, por engenharia reversa, um peso que já estava na planilha original. A origem real desse peso (Thiessen do estudo de origem?) não é conhecida.
- O evento 16 usa um peso implícito diferente (0,318).
- O DBT5 fica cerca de 3 km fora da grade: parte da bacia é extrapolação.

### 13. [M] Os pixels limitados à chuva não se concentram só em dois eventos

**Evidência (r09):** o total de 12.619 pixels (0,48%) confere. Mas a notas §13 diz que estão "concentrados nos eventos 4 e 10". Na verdade aparecem em 7 eventos: 4 (5.478), 10 (5.716), 1, 2, 7 e 11 (293 cada) e 5 (253).

### 14. [M] Números divergentes entre documentos

| # | Onde | Divergência |
|---|---|---|
| a | notas §12.2 (tabela) × §13 | 0,8009 / 0,7703 / 28,2% × 0,8052 / 0,7759 / 27,8%. O primeiro par é a aproximação f^1,12 (reproduzi 0,8009 / 0,7703 / 28,2%); o segundo é o cálculo real. Usar só o segundo. |
| b | notas §9 l.285 | "NSE = 0,37/0,65": o 0,65 não é explicado; coincide com r² = 0,648 de uma regressão **com** intercepto. Remover ou explicar. |
| c | notas §12.3 / apostila × §14.9c | λ(chuva) usa 0,273 como base, contra 0,2816 no cálculo principal (já anotado). |
| d | notas_qgis §3.5 × notas §12.3 | Acerto da classificação AMC: 41% (7/17) × "12/17" (apostila Ap. D já sinaliza; não verificado). |
| e | notas_qgis §3.6 | Tp = 4,080 h e Tb = 10,893 h (versão Kirpich, obsoleta) × 6,89 h e 18,40 h (final, conferido). |
| f | `Resultados_Calibracao_TCC.xlsx`, aba Resumo | C13, C14, E13 e E14 ("depois") vazias. B14/D14 = 16,562 / 16,599 (é o +1.656% do Método Racional, não o "antes" do HU). Colunas de erro (G:I) da aba "Volume (Q)" sem valor em cache. |
| g | README l.129–132 × notas | Erro de volume "+0,5% / 47,4%" está correto, mas é contra a vazão total (achado 1). |
| h | Apostila × notas | 154.737 pixels (K/C) × "~154 mil" × 154.011 efetivamente somados. |
| i | Erro absoluto do baseline | 44,4% (in-sample) × 46,1% (LOO): ambos corretos, mas é preciso dizer qual é qual (notas §10 usa 44,4%; README usa 46,1%). |
| j | `projeto_tcc_atualizacao` l.78 × README l.111 | Simulação de cenários no cronograma × cortada do escopo. |

### 15. [M] Pontos metodológicos a declarar como limitação

Além dos achados acima, a banca deve atacar estes pontos:

- **C e P:** C fixo no tempo (Hao usou C mensal por NDVI) e P = 1 sem verificação de campo.
- **LS:** LS de Moore (1991) sobre MDE de 30 m reprojetado.
- **Áreas urbanas:** K = 0 e C = 0 nas áreas urbanas; a erosão urbana e de estradas é ignorada.
- **Sedimento observado:** SYY_t vem de turbidez convertida em CSS (Murillo-Bermúdez et al., 2021), e a incerteza não é propagada. A CSS máxima chega a 4.602 mg/L no evento 12.
- **Peso dos eventos em c:** c é ajustado em valores absolutos e é dominado pelos eventos grandes. Os eventos pequenos ficam com erros de −65% a −88% (eventos 1, 7 e 10).
- **Convenção do PBIAS:** o projeto usa Σ(S−O)/ΣO, sinal oposto ao de Moriasi. Já documentado; manter consistente no texto.
- **Projeto original:** atribuía a Hao "distribuir a vazão de pico observada por tempo de chegada". Hao não faz isso (pr é local, Eq. 4); a atualização já corrige.

---

## (c) O que verifiquei e está correto

**Dados (série horária × planilha, 18/18 linhas, r03)**

- `T_R_m3`, `Ris_R_m3`, `Fall_R_m3`, `Q_pico`, `Q_mean`, `CSS_max`, `chuva_p1_mm` e `chuva_p2_mm` foram reconstruídos exatamente.
- `SYY_t` = Σ Q·CSS·3600/10⁶ (t), exato, e coerente com a Eq. 10 de Hao (vazão total × concentração).
- `SYY_t` = `SSY_Ris_t` + `SSY_Fall_t`.
- `Q_pico` = máximo da série horária.

**Correspondência chuva–evento e índices**

- `ESTPLUV_n.csv` corresponde às linhas 1A, 2..17 (ex.: ESTPLUV_1 = 32,8/19,2 = 1A; ESTPLUV_12 = 0/34,2).
- O índice `0 if n == 1 else n` é usado de forma idêntica em todos os scripts.

**Cadeia espacial (17 eventos, rasters reais, r05 e r06)**

| Item | Resultado |
|---|---|
| IDW | reproduzido com diferença 0 |
| Q{n}_CN1 (λ=0,05, S-Seco) | diferença ≤ 1,3e-5 mm |
| pr | diferença ≤ 1e-10 |
| ΣE_unit | igual ao CSV (até 1e-3 t) |
| SY{n} | 0,109049·E em todos os eventos |
| Fator f do volume restrito | confere (ev. 11: 1,22492); faixa 0,55 (ev. 9) a 6,95 (ev. 10) confere |
| Pixels limitados | 12.619 de 2.618.187 (0,48%) confere |
| Conversões de CN | S = 25400/CN − 254; CN-I e CN-III pelas fórmulas NEH-4/Chow conferem |
| Volumes CN-1 do CSV (λ=0,05) | conferem; erro médio +0,46%, abs. 47,4% |

**Estatística (r04)**

- Previsão pura: c = 0,109049; NSE 0,3714; LOO 0,2816; WIA 0,8683; PBIAS −21,28%; erro absoluto 44,4% (in-sample) e 46,1% (LOO).
- Restrito: c = 0,140844; NSE 0,8052; LOO 0,7759; WIA 0,9462; PBIAS −0,99%; erro absoluto 26,7% / 27,8%.
- Concentrada: medidos 0,8476 / 0,7994; modelados 0,4412 / 0,4069 (r09).
- O LOO está implementado corretamente (c reajustado sem o evento testado). As fórmulas de NSE e WIA (Willmott) estão corretas.

**Mapas (r06)**

- r(SY médio, SY médio restrito) = 0,9941.
- C médio nos hot spots 0,2467; LS 0,7907.
- r(SY, C) = 0,696; r(SY, LS) = 0,188.
- Áreas das classes de C conferem com a tabela das notas (C = 0: 19,83 km² = 14,3%).
- K = 0 e C > 0: 4,5%, como na apostila.

**Hidrograma unitário**

- Tp = 0,5 + 0,6·10,652 = 6,89 h; Tb = 18,40 h.
- 2,08 é exatamente o pico de um triângulo com Tb = 2,67·Tp que conserva 1 cm.
- Com 1,1184, o triângulo contém 53,8% do volume (nota §14.5 correta).
- A tabela de Qp das notas confere com o CSV.

**Citações conferidas nos PDFs**

- **Hao et al. (2022):**
  - Eq. 1 com 11,8 e 0,56 fixos;
  - Eq. 2 com λ = 0,2 (o TCC desvia, e isso deve ser dito);
  - Eq. 4 sem /1000;
  - 26 postos; RI e R interpolados por IDW;
  - 58 eventos; bacias de 1.310, 8.973 e 1.749 km²;
  - Tabela 4: NSE 0,74 / 0,83 / 0,70; WIA 0,89 / 0,95 / 0,92; k 2,99 / 2,93 / 0,96;
  - validação NSE > 0,78; LOO na §3.3.2; Eq. 8 com k dividindo; objetivo log-NSE (Eq. 11).
- **Baert et al. (2026):**
  - 83,84 ha; 154 eventos (46 com sedimento);
  - melhor λ fixo: NSE 0,13;
  - volume 0,21 / 0,40 e pico −0,26 / 0,34 fora da amostra;
  - MUSLE: 0,72 (cal.) / 0,66 (CV) com dados observados; 0,46 com λ_opt; −0,03 / 0,01 nas formulações preditivas;
  - β = 0,56 fixo; lag do NRCS; menção ao HIDROPIXEL.
- **Brandão et al. (2025):** 3.578 bacias; λ = 0,05 melhor; lavoura, urbano e árido associados a 0,05; pastagem a 0,2.
- **Valle Junior et al. (2019):** λ mediano 0,045 (de 0,005 a 0,455), bacia do Guariroba.
- **Artigo da IC:** α = 0,277; β = 0,807; K = 0,031; LS = 0,536; C = 0,267; erro de −4,15% (de −60,01% a +37,14%); valores de K por classe com as fontes citadas na §14.7.
- **Revisões anteriores corretas:** a correção da Eq. 8 do DSC, a ressalva do fator 1000^0,56, a autoria de Valle Junior e a não comparabilidade do volume restrito com Hao (§14 das notas, `base_para_redacao` §6 e apostila cap. 7) estão corretas.

---

## (d) Itens que não consegui verificar

- **FCI/DSC:** não rodei `calcular_fci_por_evento.py` nem `calcular_dsc_calibrar_validar.py`. Os números NSE −0,60, −0,91, 0,21 e −2,63 e o FCI₀ = 3,17 não foram reproduzidos.
- **α/β livres:** o experimento (4,2237 / 0,2793; NSE 0,6121) não foi refeito.
- **Diagnósticos:** os de λ(chuva) (0,273 → 0,258), AMC por P5 (NSE_vol −2,97; NSE_SY −0,70; acerto 12/17 contra 41%) e oráculo (0,47 / 0,63) não foram refeitos.
- **MDE:** a correção de barreiras (137,80 km²), L = 37,587 km, Hm = 147,1 m e o próprio Tc de Giandotti não foram recalculados. A faixa de validade usual de Giandotti (bacias maiores, da ordem de centenas de km²) deve ser conferida numa fonte primária antes de ser citada.
- **Rasters de entrada:** não verifiquei a derivação do LS (Moore, SAGA), a reprojeção de WGS84, a atribuição de K e C por classe nos shapefiles, nem a origem do `CN TCC.tif`.
- **Vazão de base:** o método da coluna `Bt` (qual filtro, qual parâmetro) é desconhecido. A fração de base de 34–55% depende dele; com `Qb_inicio` constante, fica entre 13% e 44%.
- **Incertezas de medição:** não avaliei a curva-chave nem a calibração turbidez–CSS.
- **Por que o 1B foi excluído:** não há registro nos documentos nem nos scripts.
- **Material de apoio:** as planilhas do pacote `Evento11_Auditoria` (01, 02), as figuras da apostila e o `Projeto TCC.pdf` foram lidos só parcialmente.
