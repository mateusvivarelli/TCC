# Checagens de sensibilidade e verificação — MUSLE espacializada, Alto Jundiaí (27/10/2026)

Pasta de trabalho: `C:\Users\sonek\AppData\Local\Temp\claude\checagens_27-10\`. Nada foi gravado em `C:\TCC`. Só foram lidos arquivos (rasters, planilhas, `tab_eventos.md`) e o conteúdo de `origin/main` (notas e scripts de referência, copiados para a pasta de trabalho como `ref_*.py` e `notas.md`).
Scripts: `common.py` (módulo), `repro.py`, `check1.py`, `check1b_repro_bt.py`, `check2.py`, `check2c_cbase_const.py`, `check_pareados.py`, `check4_pdf.py`, `check4_raster.py`, `check4_pcrit.py`. Saídas: `*.txt` e `check*.csv`.

---

## (a) Conclusão

1. **Reprodução:** os números de referência foram reproduzidos (diferença máxima 0,1 ponto, só em "SY = c·chuva"), sem nenhum ajuste.
2. **Checagem 1 (separação da base):** trocar a separação (Eckhardt com BFImax 0,58/0,70/0,80, α 0,98, Lyne-Hollick) muda o V_dir por evento por fatores de 0,69 a 1,27, mas em geral parecidos entre eventos (o que o c, calibrado em log, absorve). O MFM candidato fica entre 15,1% e 21,9% de erro mediano, fator 2 = 94% e NSE-log entre 0,81 e 0,85 em todos os cenários. O MFM adotado fica entre 31,1% e 41,6%, NSE-log 0,45 a 0,61. A ordem (candidato ≈ SY = c·V_dir, adotado pior) não muda. A vantagem do candidato sobre o adotado tem IC95% pareado que exclui zero em 4 dos 6 cenários, e inclui zero em dois: BFImax 0,80 e α 0,98.
3. **Checagem 2 (alvo = carga direta):** com o alvo direto o MFM candidato vai a 12,9% / 94% / 0,83, o MFM adotado a 36,7% / 88% / 0,53, e o MC candidato a 80,2% / 35% / −0,68. O ranking é o mesmo; só os pares MFM candidato × c·V_dir (12,9 contra 17,8) e MFM adotado × c·chuva (36,7 contra 32,8) se invertem, ambos dentro do ruído (IC95% da diferença pareada inclui 0). O NSE-log praticamente não muda, e o ganho em MedAPE do MFM candidato (20,6 → 12,9) não é robusto com 17 eventos.
4. A parcela da carga atribuída à base (34% no total; 24% a 45% por evento) depende da hipótese de que a água de base tem a mesma concentração da mistura no instante. Essa hipótese é provavelmente alta demais: com a base a 119 mg/L (mediana do CSS nas horas em que Q ≈ Bt), a base cai para 6,8% da carga, e os resultados ficam próximos dos do alvo total e do direto (MFM candidato 18,4%, adotado 41,4%). A conclusão sobre a robustez do método candidato não depende de qual alvo se usa.
5. **Checagem 4 (Woodward):** a fórmula S₀,₀₅ = 1,33·S₀,₂₀^1,15 (S em polegadas) foi confirmada no texto original (PDF do artigo, equação 8), com coeficiente e expoente conferidos. É um arredondamento de dois ajustes (1,344·S^1,149 e 1,316·S^1,164) em 307 bacias/parcelas dos EUA. Nos rasters, S₀,₀₅ é **maior** que S₀,₂₀ em 100% dos pixels (razão 1,19 a 2,11, mediana 1,79); o "S₀,₀₅ < S₀,₂₀" esperado não ocorre, e isso é o comportamento correto da relação: o CN equivalente é que diminui. 8,4% dos pixels têm CN-I < 35, abaixo da faixa da Tabela 4 do artigo (extrapolação).
6. **Robustez do candidato:** a escolha λ = 0,05 com S convertido é consistente em separação de base, alvo (total ou direto) e fórmula de conversão (verificada). Limitações permanentes: 17 eventos, parâmetros escolhidos sobre os mesmos eventos, o MC continua ruim (NSE-log < 0) porque o gargalo é a conversão chuva → escoamento, e o candidato não se distingue de SY = c·V_dir nem da IC.

---

## (b) Reprodução dos números de referência

Alvo = carga total, LOO, c em escala log, pixels = 153.855, A_pix = 897,49 m², R e RI de `tab_eventos.md`, janelas de `tab_eventos.md` (início e fim inclusivos). SY_obs e T_R por evento conferem com `eventos_processados_manuais.xlsx` (diferença 0,0%). Totais: SY_obs = 23.846 t; carga de base = 8.094 t (33,9%).

| Modelo | MedAPE (%) | Fator 2 (%) | NSE-log | Spearman | Referência dada | Confere? |
|---|---|---|---|---|---|---|
| ADOTADA MC | 97,9 | 24 | −3,95 | 0,57 | 97,9 / 24 / −3,95 | sim |
| ADOTADA MFM | 38,7 | 94 | 0,50 | 0,86 | 38,7 / 94 / 0,50 | sim |
| CANDIDATA MC | 81,1 | 35 | −0,69 | 0,59 | 81,1 / 35 / −0,69 | sim |
| CANDIDATA MFM | 20,6 | 94 | 0,84 | 0,83 | 20,6 / 94 / 0,84 | sim |
| SY = c·chuva (R) | 41,8 | 82 | 0,53 | 0,63 | 41,9 / 82 / 0,53 | sim (0,1 ponto; R da tabela vem com 1 casa decimal) |
| SY = c·V_dir | 15,9 | 94 | 0,85 | 0,90 | 15,9 / 94 / 0,85 | sim |
| SY = c·T_R | 17,6 | 94 | 0,86 | 0,88 | 17,6 / 94 / 0,86 | sim |

Conferências adicionais: V_SCS/V_dir da candidata, mediana 0,86 (0,10 a 2,15), igual à nota §32. Nenhum ajuste foi necessário (cap Q ≤ P, máscara de pixels e janelas estavam corretos).

---

## (c1) Checagem 1 — Sensibilidade à separação da vazão de base

**Reprodução do Bt fornecido.** Filtro de Eckhardt contínuo desde o primeiro ponto válido (14/11/2018 18h, b0 = Bt), α = 0,995 e BFImax = 0,70, sobre a coluna Q de `Dados_finais_histereses_corrigido.xlsx`:

| Teste | mediana |dif| (m³/s) | máx |dif| (m³/s) | r com Bt |
|---|---|---|---|
| α 0,995 / BFImax 0,70 | 1,6e-3 | 4,0e-2 | 0,999995 |
| α 0,995 / BFImax 0,58 | 1,1e-1 | 2,1 | 0,9828 |
| α 0,995 / BFImax 0,80 | 8,5e-2 | 2,9 | 0,9815 |
| α 0,98 / BFImax 0,70 | 7,6e-2 | 7,0 | 0,9102 |
| Lyne-Hollick 0,925 (3 passadas) | 1,7e-1 | — | 0,9395 |

Confirmado que **só 0,70 reproduz**. A diferença mediana que encontrei (1,6e-3 m³/s) é maior que a "~2e-4" informada: a coluna Bt da planilha `Dados_finais` não é exatamente igual à saída do filtro. Diagnóstico (`check1b_repro_bt.py`): a série do orientador (`serie_Q_Qb_Qquick_Eckhardt_orientador.xlsx`) tem Q idêntico ao da planilha (diferença 4e-16) e é reproduzida pelo filtro com erro de 9e-16; já a coluna Bt de `Dados_finais` difere dessa série em 1,6e-3 (mediana) e 0,040 (máx) m³/s. Isso muda V_dir em apenas 0,2% (cenário (i) contra (0)). O valor inicial de b0 (Bt, Q₀ ou 0,7·Q₀) não altera nada na prática.

**Separação alternativa: V_dir e MFM** (alvo = carga total; as colunas MFM mudam só porque V_dir muda; o MC não depende de V_dir e não muda). Medidas: MedAPE % / fator 2 % / NSE-log / Spearman.

| Cenário | ΣV_dir/ΣT_R | razão V_dir cenário/Bt (mediana; mín–máx) | MFM CANDIDATA | MFM ADOTADA | SY = c·V_dir |
|---|---|---|---|---|---|
| (0) Bt fornecido | 0,528 | 1,000 | 20,6 / 94 / 0,84 / 0,83 | 38,7 / 94 / 0,50 / 0,86 | 15,9 / 94 / 0,85 / 0,90 |
| (i) Eckhardt 0,995 / 0,70 | 0,526 | 0,998 (0,995–0,999) | 20,6 / 94 / 0,84 / 0,83 | 38,8 / 94 / 0,50 / 0,86 | 15,9 / 94 / 0,85 / 0,90 |
| (ii) Eckhardt 0,995 / 0,58 | 0,612 | 1,152 (1,06–1,27) | 15,1 / 94 / 0,85 / 0,82 | 41,6 / 82 / 0,45 / 0,86 | 17,2 / 94 / 0,85 / 0,90 |
| (iii) Eckhardt 0,995 / 0,80 | 0,447 | 0,851 (0,77–0,94) | 21,9 / 94 / 0,83 / 0,87 | 40,3 / 94 / 0,54 / 0,90 | 16,0 / 94 / 0,84 / 0,90 |
| (iv) Eckhardt 0,98 / 0,70 | 0,384 | 0,730 (0,69–0,94) | 17,7 / 94 / 0,81 / 0,83 | 31,1 / 94 / 0,61 / 0,88 | 14,5 / 94 / 0,84 / 0,89 |
| (v) Lyne-Hollick 0,925 | 0,470 | 0,914 (0,74–0,95) | 21,9 / 94 / 0,84 / 0,87 | 36,8 / 94 / 0,51 / 0,89 | 13,9 / 94 / 0,85 / 0,90 |

Para comparação, IC concentrada: 16,3 / 100 / 0,87 (não recalculada). ΣV_dir/ΣT_R é a fração do volume total nos 17 eventos (a fração mediana por evento fica cerca de 2 pontos abaixo; ver `check1_resultado.csv`).

**Comparações pareadas** (diferença do erro % por evento, mediana; bootstrap de eventos, 4.000 reamostragens, IC95%):

| Cenário | MFM candidata − MFM adotada | MFM candidata − c·V_dir |
|---|---|---|
| (0) Bt fornecido | −15,9 pt [−34,3; −4,2], melhor em 13/17 | +1,4 [−5,6; +10,3] |
| (i) | −15,8 [−34,2; −4,2], 13/17 | +1,5 [−5,6; +10,4] |
| (ii) BFImax 0,58 | −23,3 [−38,5; −7,6], 14/17 | +0,3 [−6,1; +6,9] |
| (iii) BFImax 0,80 | −14,3 [−33,4; +10,9], 12/17 | +2,9 [−5,4; +9,8] |
| (iv) α 0,98 | −6,3 [−26,6; +15,1], 11/17 | +3,8 [−4,9; +8,2] |
| (v) Lyne-Hollick | −19,8 [−34,8; −3,0], 13/17 | +2,5 [−6,7; +11,7] |

**Leitura.**
- A separação desloca V_dir por um fator em geral parecido entre eventos (por isso c, calibrado em log, o absorve). O que importa para a qualidade é a variação *relativa* entre eventos: ela só muda de forma relevante em (iv) e (v).
- Candidato ≈ SY = c·V_dir em todos os cenários (diferença mediana +0,3 a +3,8 pontos, IC95% sempre incluindo 0). Candidato ≈ IC como na referência (não recalculado). O MFM adotado é pior em todos os cenários em MedAPE (de 13,4 a 26,5 pontos acima do candidato, NSE-log 0,45–0,61 contra 0,81–0,85). A significância da vantagem do candidato sobre o adotado muda: o IC exclui zero em (0), (i), (ii) e (v) e inclui zero em (iii) e (iv). (iv) é um teste de estresse: α = 0,98 não reproduz a série fornecida (r = 0,91).
- **As conclusões não mudam.** O que varia é o tamanho da diferença, não a ordem. A única ressalva: o MFM adotado perde fator 2 (94 → 82%) com BFImax 0,58.

---

## (c2) Checagem 2 — Alvo = carga só do escoamento direto

SY_dir_obs = Σ (Q − Bt)·CSS·3,6/1000 por evento. Total: 15.752 t (contra 23.846 t do alvo total). Parcela da carga atribuída à base:

| Evento | SY total (t) | Base (t) | Direta (t) | Base % da carga | Base % do volume | Base % (Eck. 0,58) | Base % (Lyne-Hollick) |
|---|---|---|---|---|---|---|---|
| 1 | 266,4 | 73,6 | 192,8 | 27,6 | 45,3 | 23,5 | 32,2 |
| 2 | 2039,9 | 529,3 | 1510,6 | 25,9 | 34,2 | 20,2 | 32,2 |
| 3 | 927,8 | 335,4 | 592,4 | 36,1 | 45,3 | 27,9 | 46,6 |
| 4 | 1379,9 | 464,7 | 915,1 | 33,7 | 42,0 | 27,0 | 42,0 |
| 5 | 1371,7 | 482,2 | 889,5 | 35,2 | 54,8 | 27,9 | 45,1 |
| 6 | 198,6 | 70,5 | 128,1 | 35,5 | 43,7 | 30,2 | 43,2 |
| 7 | 1316,6 | 506,0 | 810,5 | 38,4 | 50,0 | 29,8 | 45,9 |
| 8 | 2108,5 | 669,9 | 1438,6 | 31,8 | 51,6 | 24,3 | 43,0 |
| 9 | 1154,6 | 513,9 | 640,6 | 44,5 | 53,9 | 36,6 | 53,8 |
| 10 | 847,3 | 380,9 | 466,4 | 45,0 | 55,3 | 35,2 | 57,8 |
| 11 | 1821,8 | 504,9 | 1316,9 | 27,7 | 39,3 | 21,0 | 36,8 |
| 12 | 210,7 | 67,5 | 143,2 | 32,0 | 46,2 | 30,1 | 34,8 |
| 13 | 1196,5 | 282,1 | 914,4 | 23,6 | 38,7 | 17,8 | 27,8 |
| 14 | 1731,2 | 640,1 | 1091,1 | 37,0 | 48,9 | 30,0 | 41,3 |
| 15 | 3828,8 | 1434,1 | 2394,8 | 37,5 | 49,1 | 29,5 | 48,0 |
| 16 | 1736,1 | 666,7 | 1069,4 | 38,4 | 51,6 | 33,1 | 45,2 |
| 17 | 1709,6 | 472,5 | 1237,0 | 27,6 | 49,1 | 23,8 | 31,5 |
| **Total** | 23.846 | 8.094 | 15.752 | **33,9** | 47,2 | 27,1 | 42,1 |

Mediana por evento da parcela de base na carga: 35,2% (mín 23,6%, máx 45,0%), confirmando os valores informados (35%; 24% a 45%; 34% no total). A base tem 47% do volume nas janelas e 34% da carga, porque se concentra nas horas de CSS baixo.

**Métricas LOO, alvo total contra alvo direto** (Bt fornecido; V_dir do MFM é o mesmo; MedAPE % / fator 2 % / NSE-log / Spearman):

| Modelo | Alvo TOTAL | Alvo DIRETO |
|---|---|---|
| MC CANDIDATA | 81,1 / 35 / −0,69 / 0,59 | 80,2 / 35 / −0,68 / 0,58 |
| MFM CANDIDATA | 20,6 / 94 / 0,84 / 0,83 | **12,9 / 94 / 0,83 / 0,78** |
| MC ADOTADA | 97,9 / 24 / −3,95 / 0,57 | 97,5 / 18 / −3,90 / 0,54 |
| MFM ADOTADA | 38,7 / 94 / 0,50 / 0,86 | 36,7 / 88 / 0,53 / 0,82 |
| SY = c·chuva (R) | 41,8 / 82 / 0,53 / 0,63 | 32,8 / 76 / 0,52 / 0,61 |
| SY = c·V_dir | 15,9 / 94 / 0,85 / 0,90 | 17,8 / 94 / 0,83 / 0,85 |
| SY = c·T_R (extra) | 17,6 / 94 / 0,86 / 0,88 | 14,1 / 94 / 0,81 / 0,80 |

Razão mediana LOO simulado/observado no alvo direto: MFM candidata 0,97; MFM adotada 1,24; MC candidata 1,50; MC adotada 1,71; c·chuva 0,88; c·V_dir 1,03.

**Ordem dos modelos (por MedAPE).**
- Alvo total: c·V_dir (15,9) < MFM cand (20,6) < MFM adot (38,7) < c·chuva (41,8) < MC cand (81,1) < MC adot (97,9).
- Alvo direto: MFM cand (12,9) < c·V_dir (17,8) < c·chuva (32,8) < MFM adot (36,7) < MC cand (80,2) < MC adot (97,5).
- Duas inversões, ambas dentro do ruído: MFM cand × c·V_dir (pareado: +0,5 pt, IC95% [−13,2; +13,3], melhor em 8/17) e MFM adot × c·chuva (−3,5 pt, [−24,5; +17,2]). No NSE-log, o MFM cand permanece em 0,83 e o c·V_dir em 0,83; e o MC candidato continua pior que c·chuva (+35,0 pt, IC95% [+6,1; +113,2], pior em 14 dos 17 eventos). O MFM cand é melhor que o MFM adot em 14/17 eventos (−25,9 pt, IC95% [−33,5; −9,7]).
- A queda do Spearman (0,83 → 0,78 no candidato; 0,86 → 0,82 no adotado) e do fator 2 do MFM adotado (94 → 88) pode indicar que o alvo direto é um pouco mais ruidoso (não testado). O ganho de MedAPE do MFM cand (20,6 → 12,9) não vem com ganho de NSE-log e não aparece nos demais modelos; não deve ser vendido como melhora.

**Candidata com separação e alvo consistentes** (alvo e V_dir calculados pela mesma separação; MedAPE % / fator 2 % / NSE-log / Spearman):

| Separação (carga de base) | MFM CANDIDATA | MFM ADOTADA | SY = c·V_dir | SY = c·chuva | MC CANDIDATA |
|---|---|---|---|---|---|
| Bt fornecido (33,9%) | 12,9 / 94 / 0,83 / 0,78 | 36,7 / 88 / 0,53 / 0,82 | 17,8 / 94 / 0,83 / 0,85 | 32,8 / 76 / 0,52 / 0,61 | 80,2 / 35 / −0,68 / 0,58 |
| Eckhardt 0,58 (27,1%) | 14,5 / 94 / 0,84 / 0,80 | 39,5 / 82 / 0,50 / 0,84 | 17,7 / 94 / 0,84 / 0,85 | 34,7 / 76 / 0,52 / 0,60 | 80,9 / 35 / −0,65 / 0,57 |
| Lyne-Hollick (42,1%) | 11,9 / 94 / 0,84 / 0,82 | 39,2 / 88 / 0,55 / 0,85 | 18,8 / 94 / 0,82 / 0,82 | 37,9 / 71 / 0,52 / 0,62 | 80,1 / 35 / −0,71 / 0,60 |

O resultado do candidato com alvo direto é estável entre separações (MedAPE 11,9 a 14,5, NSE-log 0,83 a 0,84, fator 2 = 94%). MFM cand melhor que MFM adot em 14/17 eventos nos três casos (−25,9, −30,1 e −29,1 pt; ICs que excluem 0). O MFM cand é melhor que c·chuva com IC95% que exclui 0 apenas no Lyne-Hollick (−18,1 pt, [−30,7; −0,4]).

**Ressalva fisicamente relevante: (Q − Bt)·CSS.** Esse alvo supõe que, em cada hora, a água de base e a água direta têm a **mesma concentração**, a da mistura medida. Implica:
- A água de base carregaria, durante os eventos, a concentração de enchente (a concentração média ponderada pela vazão dos eventos é de 527 a 1.936 mg/L), o que é improvável: a base vem de reservatórios subsuperficiais/subterrâneos, tipicamente com CSS muito menor. O "alvo direto" assim definido é, portanto, um **limite inferior** da carga do escoamento direto, e o alvo total o limite superior.
- A coluna CSS_Bt da planilha (911 h) não é uma medida independente da água de base: coincide com o CSS da mistura em 95,7% dessas horas (horas em que Q ≈ Bt, mediana 119 mg/L, quartis 63 a 193). Serve apenas como ordem de grandeza da concentração em horas de recessão.
- O filtro de Eckhardt é matemático: não distingue água subterrânea de recessão do escoamento direto. A parcela "base" de 47% do volume dos eventos inclui água de recessão que provavelmente carrega sedimento.
- Sensibilidades exploratórias (`check2c_cbase_const.py`, `check2.py`), base com concentração fixa: 119 mg/L (mediana do CSS_Bt) → base = 6,8% da carga total; MFM cand 18,4 / 94 / 0,83 / 0,79; MFM adot 41,4 / 94 / 0,51 / 0,82; c·V_dir 16,7 / 94 / 0,83 / 0,84; c·chuva 40,1 / 82 / 0,53 / 0,60. Com 63 e 193 mg/L (quartis do CSS_Bt): base 3,6% e 11,1%, MFM cand 19,6 e 16,8%. Com a concentração pré-evento (mediana das 48 h antes do início; contaminada pela recessão de eventos anteriores nos eventos 10, 14 e 16): base = 9,9% da carga, MFM cand 29,4 / 94 / 0,81 / 0,75 (ruído maior). Ou seja, o MFM candidato fica entre 12,9 e 20,6% de erro mediano nos alvos total, direto por (Q − Bt)·CSS e base a 63–193 mg/L (16,8 a 19,6% nos três últimos), e em 29,4% com a concentração pré-evento; o NSE-log fica em 0,81 a 0,84 e o fator 2 em 94%. A qualidade relativa dos modelos (candidato ≈ c·V_dir, adotado e MC piores) é a mesma.
- Em resumo: a escolha do alvo (total ou direto) muda os números absolutos da carga e o valor de c (candidata: 0,0222 para o total e 0,0146 para o direto, t por unidade de E), mas não as conclusões. Se a base carregar sedimento relevante, cabe definir em texto o alvo como "carga total, mobilizada pelo escoamento superficial" (como já está no §8 do resumo).

---

## (d) Checagem 4 — Fórmula de conversão de Woodward et al. (2003)

**Original localizado e lido.** O PDF do trabalho (103 KB, 10 páginas, metadados: autores Hawkins, Hjelmfelt, Quan, Van Mullem, Woodward) foi baixado de `http://ruby.fgcu.edu/courses/twimberley/EnviroPol/CurveNumber.pdf` (a cópia em `ponce.sdsu.edu`/`uon.sdsu.edu` não abriu: conexão recusada) e lido com pymupdf (`woodward_texto.txt`). O texto é um manuscrito do artigo de 2003: título e resumo conferem com os da ASCE/Crossref, mas o PDF não declara o local de publicação e não pude comparar com a versão editorial (a numeração de páginas e equações é a do manuscrito).

**Fórmula exata (Eq. 6 a 9 do artigo).** Transcrição:
- Eq. (6), dados "naturais": S₀,₀₅ = 1,344·S₀,₂₀^1,149, r² = 99,38%.
- Eq. (7), dados "ordenados": S₀,₀₅ = 1,316·S₀,₂₀^1,164, r² = 99,44%.
- "where S₀,₀₅ and S₀,₂ are in inches." Valores "consenso" arredondados, Eq. (8): **S₀,₀₅ = 1,33·S₀,₂₀^1,15**.
- Eq. (9), preservando CN = 1000/(10 + S): CN₀,₀₅ = 100 / (1,879·[100/CN₀,₂₀ − 1]^1,15 + 1).
- Nas Conclusões: "S₀,₀₅ = 1,33 S₀,₂₀^1,15 (where S is in inches) ... It was determined from data from 307 watersheds."

**Conferência com o seu uso:** coeficiente 1,33 e expoente 1,15 conferem; unidades: polegadas (a conversão `25,4·1,33·(S/25,4)^1,15` do script é correta; equivale a S₀,₀₅(mm) = 0,8189·S₀,₂₀(mm)^1,15, valor que Brandão et al. (2025) citam como 0,8187). Relação inversa: **não é apresentada** no artigo; basta inverter, S₀,₂₀ = (S₀,₀₅/1,33)^(1/1,15) (inversão minha, não do artigo).

**Base empírica.** 307 bacias ou parcelas (USDA-ARS 134 bacias, USLE-ARS 137 parcelas, USFS 26 bacias, Jornada/NMSU 6 parcelas, USGS 4 bacias), 23 estados dos EUA, majoritariamente leste, centro-oeste e sul; a parte noroeste dos EUA não tem dados. Eventos com 20 ou mais por unidade. Houve dois tipos de dado: "natural" (pares P–Q por evento) e "ordenado" (classificação por postos). O artigo cita 28.301 eventos no texto e 28.031 na Tabela 3 (inconsistência interna do original). Para cada unidade, ajustou-se o CN por mínimos quadrados com λ = 0,05 e com λ = 0,20 e relacionaram-se os S obtidos.
**Faixa de validade:** o artigo não declara uma faixa formal. A Tabela 4 mostra valores conjugados para CN₀,₂₀ de 35 a 100 (S₀,₂₀ até 18,6 pol = 472 mm). Os autores dizem que as duas relações se cruzam em S = 0,148 pol (≈ 3,8 mm, CN₀,₂₀ ≈ 98,5) e em S = 0, e sugerem tratá-las como iguais nesses níveis raros. Para P < P_crit (tabelado) λ = 0,05 gera mais escoamento; para P > P_crit, menos. O artigo recomenda construir novas tabelas de CN para λ = 0,05 a partir da relação.
**Ressalvas:** a relação é uma regressão entre S's ajustados a dados (não uma identidade matemática do SCS-CN). Foi derivada de bacias e parcelas dos EUA com regime próprio. Os próprios autores indicam que o efeito é maior em CN baixos e chuvas pequenas.

**Referência completa.** Woodward, D. E.; Hawkins, R. H.; Jiang, R.; Hjelmfelt, A. T., Jr.; Van Mullem, J. A.; Quan, Q. D. (2003). *Runoff Curve Number Method: Examination of the Initial Abstraction Ratio*. In: World Water & Environmental Resources Congress 2003, Philadelphia, Pennsylvania. American Society of Civil Engineers, p. 1–10. DOI: [10.1061/40685(2003)308](https://ascelibrary.org/doi/10.1061/40685(2003)308). Conferência dos metadados no Crossref (autores, título, evento, ano, páginas e DOI conferem; data de publicação 17/06/2003). A página da ASCE devolveu HTTP 403, então não abri a versão editorial.
A autoria no registro Crossref tem Woodward primeiro e Quan por último; os metadados do PDF listam os cinco autores em ordem alfabética (Hawkins, Hjelmfelt, Quan, Van Mullem, Woodward), sem Jiang. A ordem usada acima é a do Crossref.

**Fontes que citam o original.**
- Brandão et al. (2025), *J. Hydrology* 655:132941, DOI 10.1016/j.jhydrol.2025.132941 (`C:\TCC\1-s2.0-S0022169425002793-main.pdf`, lido): seção 4.4 cita "Jiang (2001), Woodward et al. (2003) proposed S₀,₀₅ = 1,33 S₀,₂₀^1,15 (inches)". Registra também Hawkins et al. (2020) com S₀,₀₅ = 1,32·S₀,₂₀^1,089 (polegadas) e S₀,₀₅ = 0,8187·S₀,₂₀^1,15 (mm); a primeira é citada de Brandão, não a confirmei na fonte (o relatório de Hawkins et al. 2020, *Updating the Curve Number: Task Group Report*, DOI 10.1061/9780784483060.012, não foi aberto). Os resultados do próprio Brandão, em mm: S₀,₀₅ = 0,919·S₀,₂₀^1,174 (n = 3.398) e S₀,₀₅ = 0,917·S₀,₂₀^1,170 (n = 3.578), com R² ≈ 90%. Brandão calcula o S de cada evento pelas suas Eq. 3 e 4, atribuídas a Hawkins (1973) e Woodward et al. (2003) (não transcritas aqui: o texto extraído do PDF vem truncado). A referência de Jiang (2001) nesse artigo aparece como tese de doutorado (University of Arizona); o próprio Woodward et al. cita como MS thesis. Não verifiquei qual está certa.
- Elhakeem & Papanicolaou (2009), Hawkins et al. (2009) e outros: não abertos nem verificados.
- Resultados de busca na web (resumo ASCE, páginas da SDSU) confirmaram título e resumo, sem acrescentar a fórmula além do PDF que li.

**Verificação numérica.**
1. Minha implementação reproduz a Tabela 4 do artigo: CN₀,₂₀ = 95/90/80/70/60/50/35 dá S₀,₀₅ = 0,635/1,501/3,815/7,091/11,786/18,787/38,284 pol (tabela: 0,636/1,501/3,815/7,091/11,785/18,787/38,285), e CN₀,₀₅ = 94,02/86,95/72,39/58,51/45,90/34,74/20,71, igual ao da tabela e à Eq. 9.
2. Rasters da bacia (153.855 pixels):

| Grandeza | mín | p5 | mediana | p95 | máx |
|---|---|---|---|---|---|
| S₀,₂₀ (mm) (= CN-I) | 12,3 | 106,7 | 180,6 | 558,2 | 558,2 |
| S₀,₀₅ convertido (mm) | 14,7 | 176,0 | 322,5 | 1.180,2 | 1.180,2 |
| CN equivalente λ 0,20 | 31,3 | — | 58,4 | — | 95,4 |
| CN equivalente λ 0,05 | 17,7 | — | 44,1 | — | 94,5 |

- A razão S₀,₀₅/S₀,₂₀ vai de 1,19 a 2,11 (mediana 1,79): **S₀,₀₅ > S₀,₂₀ em 100% dos pixels**, nenhum com S₀,₀₅ < S₀,₂₀. É o esperado pela relação, pois o ponto de cruzamento é S = 3,8 mm e o menor S da bacia é 12,3 mm. Não é um defeito: com λ menor, a abstração λS é menor, e o S (retenção após o início do escoamento) precisa ser maior para dar um escoamento parecido.
- O percentual de pixels com CN-I < 35 (S₀,₂₀ > 472 mm, fora da Tabela 4 do artigo) é 8,4% (12.933 pixels): extrapolação do ajuste (que usa CN mínimo 35 na tabela). O CN equivalente de λ 0,05 chega a 17,7, valor muito abaixo do que se tabula (o próprio artigo chega a 20,7 no CN 35).
- Plausibilidade no escoamento: para o S mediano (180,6 mm / 322,5 mm), P = 50 mm dá Q = 0,99 mm (adotada) e 3,22 mm (candidata); P = 100 mm dá 16,7 e 17,3 mm. P_crit (onde as duas curvas se cruzam) é 107 mm para o S mediano (77 mm para o p5 e 241 mm para o p95), em linha com o comportamento descrito no artigo (λ = 0,05 gera mais escoamento em chuvas pequenas). A fração de pixel-evento sem escoamento (P ≤ λS) cai de 39,8% (adotada) para 14,0% (candidata).
- As fórmulas de Brandão (2025) (em mm) dão S₀,₀₅ 24 a 27% (mediana) maior que a de Woodward na bacia (razão 1,18 a 1,31), então a incerteza na própria conversão é grande.

---

## (e) Limitações e dúvidas

- **Reprodução do Bt:** a coluna Bt de `Dados_finais` difere da série do orientador (reproduzida a 9e-16 pelo filtro) em até 0,04 m³/s (mediana 1,6e-3), diferente dos "~2e-4" informados. Efeito em V_dir: 0,2%. Vale perguntar de qual versão vem a coluna Bt; o cabeçalho BFImax = 0,58 continua sem reproduzir nenhuma das séries.
- **Lyne-Hollick:** implementei q_t = α·q_{t−1} + (1+α)/2·(Q_t − Q_{t−1}) com q em [0, entrada] e três passadas, cada uma aplicada à base da passada anterior (frente sobre Q, trás sobre a base 1, frente sobre a base 2), q₀ = 0. Outras convenções de passada (filtrar sempre Q) podem dar frações diferentes. O LH com α = 0,925 dá BFI global 0,77 (maior que 0,66 do Eckhardt 0,70), o que não é um parâmetro calibrado para a bacia. Todas as alternativas são aplicadas sem calibração própria; α = 0,98 é um teste de estresse (não reproduz a série).
- **Amostra:** n = 17 eventos, MedAPE de 17 valores é instável (diferenças de 2 a 4 pontos não são interpretáveis; os ICs pareados são largos). Nenhum cenário foi avaliado fora da amostra além do LOO; λ, CN-I e a conversão foram escolhidos olhando os mesmos eventos (já declarado em §4 do resumo).
- **Alvo direto:** a hipótese de mesma concentração é provavelmente alta; as sensibilidades com concentração fixa são exploratórias (CSS_Bt de 911 horas; concentração pré-evento contaminada por eventos anteriores, especialmente em 10, 14 e 16). Não há medida independente do sedimento do escoamento direto.
- **Uso do R da tabela:** R e RI vêm de `tab_eventos.md` (1 casa decimal); isso explica o 41,8 contra 41,9 da referência para c·chuva.
- **Checagem 4:** li o manuscrito do PDF encontrado em um site de curso (FGCU); não consegui abrir a página editorial da ASCE (403) nem o relatório Hawkins et al. (2020). Conferi os metadados no Crossref. Elhakeem & Papanicolaou (2009) não foi consultado. Não há relação inversa publicada; a inversa é matemática. O artigo é de 2003 (EUA); a relação não foi validada em bacias tropicais brasileiras, e na bacia 8,4% dos pixels ficam além da faixa tabelada.
- **Dúvida aberta para o orientador:** quais BFImax e quais versões da série usar; se o alvo no TCC deve ser a carga total (todo o sedimento atribuído ao escoamento que o mobiliza) ou a direta com a ressalva acima.
