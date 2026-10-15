# Revisão independente, 2ª rodada: modelo "escoamento direto + vazão de base" (`calcular_sy_com_base.py`)

Revisor independente. Data: 15/10/2026. Drive montado. Não alterei nenhum arquivo do projeto. Os números abaixo foram
recalculados por uma reimplementação própria, que não grava nada no projeto (`...\Temp\claude\revisor\r11_base.py`,
`r12_vol.py`), usando os rasters e a série horária. Os achados do relatório anterior (`revisao_independente.md`) são
citados como "R1-n".

---

## Resumo executivo

1. **A implementação está correta.** Reproduzi todos os números do script e do CSV: kb 1,9286; c 0,132380; volume total
   com erro −7,7%, abs. 25,5%, NSE 0,582; SY com NSE in-sample 0,4975, PBIAS −16,5%, LOO aninhado 0,3746, abs. 30,2%.
   A diferença máxima é de 3e-5 t. As somas dos rasters `E_unit{11,15}_vb.tif` e a lâmina q_base também batem.
   Máscara (154.011 pixels, 138,22 km²), unidades, indexação de eventos e aninhamento do LOO para kb e c estão certos.
2. **Há vazamento de informação forte, e ele vem da `Duracao_horas`, não do λ.** A duração é a janela observada do
   hidrograma: corr(dur, T_R) = 0,87 e corr(dur, SY) = 0,82.
   - **Benchmarks com a duração.** SY = c·Duracao_horas sozinho dá LOO **0,602**, mais que o modelo (0,375). V_total = c·dur dá NSE-LOO **0,70** contra T_R, mais que o volume do modelo (0,582).
   - **Com duração fixa (sem vazamento).** A previsão da base contra Bt cai de NSE-LOO 0,664 para **−0,004**. O erro absoluto do volume volta a 45% (era 25,5%). O erro absoluto do SY sobe de 30% para **62%** em LOO.
   - **Conclusão.** O ganho de volume e de erro percentual vem de saber, depois do evento, quanto ele durou.
3. **O λ "a priori" não é um problema relevante.** Escolhendo λ dentro de cada dobra do LOO, o critério de SY sempre
   escolhe 0,05 (LOO 0,558) e o critério de volume sempre escolhe 0,20 (LOO 0,375). O autor ficou com a opção
   *menos* favorável ao SY. Isso deve ser dito, mas não invalida nada.
4. **Na prática, o modelo é um modelo de vazão de base.**
   - Mediana de 55% do volume e 49% do E_unit vêm da lâmina uniforme de base.
   - Nos eventos 1, 4, 7, 10 e 12, 92–99% da "erosão" vem da base.
   - Em média, 40% dos pixels têm Q_dir = 0 com λ=0,20 e mesmo assim erodem.
   - Fisicamente, isso é insustentável como erosão de encosta.
   - Uma alternativa mais honesta, com dois componentes separados (SY = c1·E_dir + c2·V_base, sem base nos pixels), dá LOO aninhado **0,415**, acima do modelo adotado.
5. **O ganho sobre o modelo anterior está dentro do ruído.**
   - NSE-LOO: 0,282 → 0,375.
   - Bootstrap pareado da diferença: mediana +0,10, IC 95% [−0,09; +0,78], P(diferença ≤ 0) = 0,20.
   - Wilcoxon pareado: p = 0,31 nos erros quadráticos; p = 0,045 nos erros percentuais (o efeito vem dos eventos pequenos, onde a duração vaza).
   - Sem o evento 15, os dois modelos ficam ≤ 0 (−0,03 contra −0,31).
   - O ganho real e robusto é em escala log (log-NSE LOO −0,29 → 0,54), isto é, nos eventos pequenos.
6. **Os benchmarks sem MUSLE continuam acima.** c·T_R: LOO 0,765. c·V_base observada: 0,657. c·Chuva: 0,605. c·Duração: 0,602.
   c·(V_dir SCS + V_base prevista), sem MUSLE: 0,383, igual ao modelo. A MUSLE espacial não acrescenta nada ao seu
   próprio volume de entrada.
7. **A versão honesta falha.** Comparar a carga do escoamento direto observado (SY − carga da base, cerca de 65% do SY)
   com a MUSLE só com escoamento direto dá LOO **−1,22** (λ=0,20) ou 0,12 (λ=0,05).
8. **O mapa fica ainda mais K·C·LS.** r = 0,886 e Spearman **0,966**. A base uniforme achata a hidrologia
   (CV espacial de Q 0,50, contra 2,15 de K·C·LS). O r = 0,996 com o mapa antigo é, de novo, consequência da construção.
9. **Dos 5 achados graves de R1:**
   - R1-1 (vazão de base): reconhecido e tratado no **diagnóstico**, mas não resolvido no modelo (a base entra como erosão).
   - R1-2 (benchmarks): persiste.
   - R1-3 (fragilidade): persiste.
   - R1-4 (evento 1B): melhora (o modelo novo prevê 563 t contra 1.349 t; com 18 eventos, NSE 0,447 / LOO 0,339), mas a exclusão segue sem justificativa.
   - R1-5 (λ=0,05 sem respaldo): resolvido, porque λ=0,20 é o padrão.
   - Novo: vazamento pela duração.
10. **Recomendação.** O modelo pode entrar no TCC como **análise diagnóstica** ("quanto do erro é vazão de base"), não
    como "previsão pura melhorada". A previsão pura honesta, sem `Duracao_horas` observada, fica entre NSE-LOO
    0,23 (duração da chuva) e 0,46 (duração fixa), com erro absoluto de 40% a 62%: não melhor que o modelo anterior.

---

## 1. Implementação: verificada, sem erros que mudem resultados

| Item | Verificação | Resultado |
|---|---|---|
| Máscara | S-Seco (vizinho mais próximo) ∩ K ∩ C ∩ LS | 154.011 pixels; A_bacia = 154.011 × 897,49 = 138,22 km² (= máscara de E_unit de R1) |
| q_base | V_base/A_bacia·1000, uniforme, inclusive em pixels com K=0 ou C=0 | Conserva V_base na soma. Nesses pixels não gera E (K·C=0). Correto. |
| Unidades | Q mm; pr m³/s; E = 11,8·(Q·pr·A)^0,56·K·C·LS | Idênticas ao pipeline anterior (verificado em R1) |
| Q_dir | SCS-CN λ=0,20 com S-Seco | Meu cálculo com IDW e S independentes reproduz ΣE (diferença ≤ 1e-3 t) |
| Indexação | `iloc[0 if n==1 else n]`; janelas da série horária | Igual a R1; 1B ainda excluído |
| kb | MQ pela origem: Qb_inicio·Duracao_horas·3600 contra ΣBt·3600 | kb = 1,9286; faixa no LOO 1,768–2,004 |
| LOO aninhado | Para cada i: kb sem i; E de todos com esse kb; c sem i | Correto. O λ não é reescolhido (ver item 2.3). |
| Rasters `_vb` | ΣE11 = 4.396,65; ΣE15 = 33.307,33; Q mínimo = q_base (4,318 / 9,191 mm) | Batem |

**Observações menores:**

- **Duração usada em `xb`.** `Duracao_horas` = N − 1 horas, mas `BTV` soma N leituras. kb absorve a diferença, então não há efeito material.
- **Bootstrap e "sem evento 15".** No script, os dois fixam kb em toda a amostra (só c é refeito). Refiz o "sem ev. 15" com kb e c aninhados: LOO −0,032 (o script reporta −0,01 nas notas §17). A diferença é desprezível.
- **Comparação com `SY_medio_eventos.tif` antigo.** Usa a máscara nova (o mapa antigo é do λ=0,05 sem base). Ok.

---

## 2. Vazamento de informação

### 2.1 [Crítico] `Duracao_horas` é informação posterior ao evento e carrega quase todo o ganho

`Inicio` e `Fim` definem a janela do hidrograma observado. A duração só é conhecida depois que a vazão volta ao normal
e é, na prática, um indicador do volume observado:

| Correlação | r |
|---|---|
| dur × T_R | 0,874 |
| dur × SY | 0,821 |
| dur × chuva | 0,817 |

**Testes (todos LOO, 1 parâmetro):**

| Preditor | Alvo | NSE-LOO | Erro abs. LOO |
|---|---|---|---|
| c·Duracao_horas | SY | **0,602** | 50,3% |
| c·Duracao_horas | T_R | **0,700** | — |
| Modelo novo (V_dir + base) | T_R | 0,582 | 25,5% |
| Modelo novo | SY | 0,375 | 30,2% |

**O mesmo modelo, trocando só a duração por informação disponível antes do evento:**

| Duração usada em V_base | Base prevista × Bt (NSE-LOO) | Volume total × T_R | SY: NSE-LOO / erro abs. LOO |
|---|---|---|---|
| Observada (adotado) | 0,664 | NSE 0,582; abs. 25,5% | 0,375 / 30,2% |
| Fixa (mediana) | **−0,004** | NSE 0,625; abs. **45,0%** | 0,458 / **62,3%** |
| Duração da chuva (máx. dos postos) | — | — | **0,227 / 40,3%** |

**Leitura:**

- Toda a capacidade de prever a vazão de base vem da duração observada.
- A queda do erro absoluto (46% → 30%) vem dela: é exatamente nos eventos pequenos (1, 6, 10) que o erro percentual despenca (−66 → +24%, +74 → +15%, −88 → −8%).
- O NSE do SY quase não depende dela (com duração fixa ele até sobe, mas o erro absoluto dobra). Isso mostra de novo que o NSE é governado pelo evento 15.

`Qb_inicio` em si é legítimo: é o estado antecedente, conhecido no início do evento.

**Correção:** substituir `Duracao_horas` por uma grandeza conhecida *a priori*. Por exemplo, uma janela fixa, a duração da
chuva mais um tempo de recessão fixo, ou um volume de base = Qb_inicio × janela padrão. Reportar o resultado
honestamente. Se a duração observada for mantida, rotular a versão como "diagnóstica (usa a duração observada)", na
mesma categoria do volume restrito.

### 2.2 [Importante] kb é ajustado contra `Bt`, que vem da própria série observada

- O aninhamento retira o evento i, o que é correto para LOO. Mas `Bt` é produto de um filtro aplicado à vazão
  observada (método ainda a confirmar) e embute a resposta do próprio evento: o kb de 1,93 indica que a "base" média
  durante o evento é quase o dobro de Qb_inicio.
- Isso é aceitável em LOO.
- Porém a base prevista só funciona por causa da duração (2.1). Sozinha, a base prevista é ruim contra o volume total: NSE −0,29.

### 2.3 [Menor] λ = 0,20 "fixado a priori" depois de ver vários λ

**Teste:** escolhi λ ∈ {0,05; 0,10; 0,15; 0,20} *dentro* de cada dobra do LOO.

| Critério de escolha do λ | λ escolhido (todas as dobras) | NSE-LOO de SY |
|---|---|---|
| NSE do SY | 0,05 | 0,558 |
| NSE do volume total | 0,20 | 0,375 |

**Conclusão:** a escolha de 0,20 é coerente com um critério declarável ("coerência do volume") e é a pior para o SY.
Não há indício de seleção oportunista. Mesmo assim, é preciso declarar que 0,20 foi escolhido depois de ver a
sensibilidade, e que a escolha é ancorada no valor padrão do SCS.

**Atenção à frase "λ = 0,05 dá LOO 0,558".** Com λ=0,05, o volume total tem NSE −0,76. Esse NSE de SY é obtido com a
hidrologia errada, outro sinal de que o NSE do SY não discrimina a qualidade física.

### 2.4 O LOO pode ser lido como validação preditiva?

**Não**, enquanto V_base usar `Duracao_horas` observada. O LOO aninhado protege contra o reajuste de kb e c, mas não
contra um preditor que só existe depois do evento. Com informação a priori, o LOO honesto fica entre 0,23 e 0,46, com
erro absoluto de 40–62%. Na prática, isso equivale ao modelo anterior (0,282 / 46%).

---

## 3. Somar uma lâmina de base uniforme a cada pixel é defensável?

### 3.1 [Crítico] Fisicamente, não

A vazão de base é água subterrânea que chega ao canal. Ela não escoa sobre as encostas e não desagrega solo. Ao
somá-la ao Q de cada pixel antes do termo (Q·pr·A)^0,56, o modelo trata a base como escoamento superficial erosivo
espalhado por toda a bacia.

| Indicador | Valor |
|---|---|
| Fração do volume previsto que é base | 23% (ev. 15) a 99% (ev. 10); mediana 55% |
| Fração de ΣE_unit gerada só pela base | mediana 49%; ≥ 92% nos eventos 1, 4, 7, 10 e 12 |
| Pixels sem escoamento direto (Q_dir=0, λ=0,20) que erodem só pela base | 40% em média |
| pr da base | pr = Q·RI/R é proporcional à intensidade da chuva, mas a base não responde a ela: a base vira "pico" |

**Estatisticamente**, a lâmina uniforme funciona como um termo aditivo de nível por evento, que reduz o contraste entre
eventos pequenos e grandes (por isso o log-NSE melhora). É um artifício de ajuste. As próprias notas (§16.7 e §17)
reconhecem isso.

### 3.2 Alternativas mais honestas (testadas)

Todas foram testadas com LOO aninhado e com a mesma base prevista com duração observada, para isolar só a forma de
combinar:

| Formulação | O que compara | NSE-LOO |
|---|---|---|
| (A) Adotada: base uniforme dentro da MUSLE | SY total | 0,375 |
| **(B) Dois componentes: SY = c1·ΣE_unit(Q_dir) + c2·V_base_prev** (c ≥ 0, NNLS) | SY total | **0,415** |
| (C) Carga só do escoamento direto: SY_dir,obs = Σ(Q − Bt)⁺·CSS contra c·ΣE_unit(Q_dir), λ=0,20 | SY direto (≈65% do SY) | **−1,22** |
| (C') Idem com λ=0,05 | SY direto | 0,12 |
| (D) Só a carga da base: (SY − SY_dir) contra c·V_base_prev | SY da base (≈35%) | 0,27 |

**Recomendação:** adotar (B) ou apresentar (C).

- (B) é fisicamente honesto (a erosão de encosta vem só do escoamento direto; a carga da base é um termo de canal/fundo, não espacializado) e tem desempenho igual ou melhor. O mapa sairia só de c1·E_unit(Q_dir).
- (C) é o teste mais limpo da MUSLE-SCS: e ela **falha**. Esse resultado precisa constar no TCC, porque é o que a banca vai perguntar.
- Nota: a separação da carga usa Bt × CSS horária, que é aproximada (a CSS da base não é medida separadamente).

---

## 4. O modelo melhora de fato a previsão pura? (comparação pareada, LOO de cada modelo)

| Métrica | Anterior (λ=0,05, sem base) | Novo (λ=0,20 + base) |
|---|---|---|
| NSE-LOO | 0,282 | 0,375 |
| NSE-LOO sem o evento 15 (kb e c aninhados) | −0,310 | −0,032 |
| log-NSE LOO | −0,290 | **0,539** |
| Spearman LOO | 0,551 | 0,586 |
| Erro abs. LOO | 46,1% | 30,2% |
| Eventos em que o novo erra menos (LOO) | — | 11 de 17 |

**Testes de diferença:**

- **Bootstrap pareado (5.000) da diferença de NSE-LOO:** mediana +0,103; IC 95% [−0,091; +0,778]; P(diferença ≤ 0) = 0,196. Não é significativo.
- **Wilcoxon pareado:** erros quadráticos p = 0,31; |erro %| p = 0,045. Esse último é marginal, vem dos eventos pequenos e depende da duração observada (2.1).

**Conclusão:** em NSE, a diferença está dentro do ruído (n=17, evento 15 com 49% da variância). Há uma melhora real em
escala log e em erro percentual nos eventos pequenos, mas ela é atribuível ao uso da duração observada. Com duração a
priori, o erro absoluto volta a 40–62%.

---

## 5. O que o autor pode e não pode afirmar

**Pode afirmar:**

- `T_R_m3` e SY_obs incluem a vazão de base (34–55% do volume; cerca de 35% da carga, pela separação Bt).
- A calibração anterior (CN-I, λ=0,05) compensava implicitamente essa base.
- Com λ padrão (0,20) e a base estimada a partir do estado antecedente e da duração do evento, o volume total é
  reproduzido com NSE 0,58 e o SY com NSE-LOO 0,38. É uma configuração **diagnóstica**, que usa a duração observada.
- O padrão espacial dos hot spots é insensível a essas escolhas (r ≥ 0,99), porque é dominado por K·C·LS (Spearman 0,97).
- A carga ligada ao escoamento direto não é reproduzida pela MUSLE com SCS-CN (NSE-LOO negativo).

**Não pode afirmar:**

- que o modelo novo é uma "previsão pura" ou que "melhora a previsão" (vazamento pela duração; diferença de NSE não significativa);
- que a vazão de base gera erosão nas encostas, ou que o mapa `_vb` representa erosão causada pela base;
- que a MUSLE espacial supera índices simples (c·T_R, c·chuva e c·duração ficam acima);
- que o mapa foi validado espacialmente, ou que sua estabilidade (r = 0,996) é evidência de robustez;
- que λ=0,20 foi "fixado a priori" sem mencionar que a escolha veio depois da análise de sensibilidade.

**Redação sugerida, parágrafo de resultados:**

> "A reconstrução das variáveis observadas mostrou que o volume (T_R) e a carga de sedimentos medidos no exutório
> incluem a vazão de base, responsável por 34 a 55% do volume dos eventos, componente que o SCS-CN não representa. Com
> o valor padrão λ = 0,20 e uma vazão de base estimada a partir da vazão no início do evento e da duração observada do
> hidrograma, o volume total foi reproduzido com NSE = 0,58 e a produção de sedimentos com NSE = 0,50 na calibração e
> 0,38 em validação cruzada leave-one-out aninhada (erro absoluto médio de 30%). Essa melhora em relação à
> configuração anterior (NSE-LOO = 0,28) não é estatisticamente distinguível com 17 eventos (IC 95% da diferença:
> −0,09 a +0,78) e depende do uso da duração observada do evento; índices simples, como o volume medido ou a chuva do
> evento, apresentaram desempenho igual ou superior no exutório."

**Redação sugerida, limitações:**

> "A configuração com vazão de base é diagnóstica, e não preditiva: a duração do evento só é conhecida após a
> passagem do hidrograma e, quando substituída por uma duração fixa, o erro absoluto do sedimento sobe para cerca de
> 60%. A adição de uma lâmina de base uniforme a cada pixel é um artifício estatístico, pois a vazão de base não
> produz erosão nas encostas; por isso, a parcela do sedimento associada ao escoamento direto não foi reproduzida pelo
> modelo (NSE negativo). A validação é apenas agregada, em 17 eventos, com um evento respondendo por cerca de metade
> da variância, e o padrão espacial do mapa é determinado essencialmente pelos fatores K, C e LS (correlação de
> postos de 0,97), sem verificação independente no interior da bacia."

---

## 6. Reavaliação dos 5 achados graves de R1

| R1 | Situação com o modelo novo | Evidência |
|---|---|---|
| 1. T_R_m3 é volume total | **Diagnóstico resolvido; modelagem não.** A definição foi corrigida nas notas (§15) e a base é explicitada. Mas no modelo ela entra como escoamento erosivo em todos os pixels (§3.1). | 49% de ΣE vem da base; formulação (C) com LOO −1,22 |
| 2. Benchmarks triviais superam | **Persiste.** c·T_R 0,765; c·V_base obs 0,657; c·Chuva 0,605; c·Duração 0,602 > 0,375. A MUSLE não acrescenta ao seu volume de entrada (c·V_total previsto: 0,383). | r11, seção 3 |
| 3. Fragilidade estatística | **Persiste.** Sem o evento 15: −0,03. Bootstrap do NSE in-sample [−0,96; 0,88] (script). Diferença entre modelos não significativa. | §4 |
| 4. Evento 1B excluído | **Atenuado, não resolvido.** O modelo novo prevê 563 t para o 1B (obs. 1.349 t; −58%, contra −88% antes). Com 18 eventos: NSE 0,447 / LOO(c) 0,339. A exclusão continua sem justificativa escrita. | r11, seção 8 |
| 5. λ=0,05 sem respaldo | **Resolvido.** λ=0,20 é o padrão do SCS e de Hao (Eq. 2). Basta declarar a ordem das decisões (§2.3). | — |
| Novo | **Vazamento pela `Duracao_horas`** (§2.1). Crítico para qualquer leitura preditiva. | c·dur LOO 0,602; base × Bt com duração fixa: NSE −0,004 |
| R1 (6), RI/R | **Persiste.** Com RI coerente (máximo horário da chuva ponderada): NSE in 0,494, LOO aninhado **0,314** (contra 0,375). | r11, seção 7 |
| R1 (7), mapa = K·C·LS | **Piorou.** Spearman(mapa, K·C·LS) 0,922 → 0,966; 72,5% dos hot spots coincidem com o top 5% de K·C·LS. A base uniforme reduz a contribuição espacial da hidrologia. | r11, seção 9 |

---

## 7. Não verificado

- Os scripts de diagnóstico `_diagnostico_escoamento_direto.py`, `_diagnostico_vazao_base_antecedente.py` e
  `_diagnostico_previsao_com_base.py` não foram executados linha a linha. Conferi os números finais que eles alimentam
  (§17 das notas) pela minha reimplementação. Os números da §16 (Lyne-Hollick, r do fator f com chuva, regressões em
  log) não foram refeitos.
- O método da coluna `Bt` (filtro e parâmetros) continua desconhecido. Toda a separação base/direto, inclusive kb e a
  formulação (C), depende dele. As notas registram correlação de 0,996 com Lyne-Hollick, o que dá alguma robustez.
- Não verifiquei Q > P nos rasters `_vb` (q_base de até 13,9 mm; possível só em pixels de chuva muito baixa no evento 12).
- Não verifiquei o critério de definição de `Inicio`/`Fim` dos eventos na fonte original (I4SDWI). Ele determina o
  quanto `Duracao_horas` é informação do hidrograma.
