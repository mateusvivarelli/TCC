# Mudanças a fazer no Google Doc — remoção da vazão de base (decisão de 26/10/2026)

Decisão: **λ = 0,20 e sem termo de vazão de base**. A MUSLE usa só o escoamento direto, nos dois modelos:

- **MC (calculado):** SY = c · ΣE_unit, com Q do SCS-CN (CN-I, λ = 0,20).
- **MFM (forçado):** SY = c · ΣE_unit, com Q reescalado para o escoamento direto **medido** (T_R − ΣBt).

O alvo continua sendo a carga total medida: todo o sedimento do evento é atribuído ao escoamento superficial, e a base só o transporta. A vazão de base (Bt) só serve para obter o escoamento direto medido.

Tudo abaixo já foi recalculado: dados, tabelas `.md`, figuras, mapas e planilha. Este arquivo lista **o que muda no texto**, seção por seção, na ordem do Doc. Os números vêm de `Scripts/calcular_sy_so_direto.py` (rodado em 26/10/2026).

---

## ⚠️ Antes de tudo: duas conclusões mudam

1. **O MC deixa de empatar com a regra da chuva e fica bem abaixo dela.**
   - MC: 98% de erro mediano e 24% dos eventos dentro de fator 2.
   - SY = c · chuva: 42% e 82%.
   - Sem o termo de base, fica exposto que o SCS-CN não gera o escoamento certo: erra o escoamento direto em 69% na mediana, com NSE do volume de −0,69.
2. **O MFM deixa de empatar com a IC na calibração em log.**
   - MFM: 39% / 94% / NSE em log 0,50.
   - IC: 16% / 100% / 0,87.
   - SY = c · volume direto medido: 16% / 94% / 0,85.
   - No **NSE linear**, os dois continuam empatados: 0,79 a 0,80 (calibração linear) contra 0,77 da IC. Mas a régua adotada no TCC é a calibração em log.
   - A frase "a espacialização mantém a qualidade da formulação concentrada" **não vale mais** como está. A leitura honesta passa a ser: *com a água medida, a MUSLE espacializada acerta a ordem de grandeza (94% em fator 2), mas não melhora a carga total em relação a regras simples ou à IC; o ganho dela é o mapa.*
   - **Sensibilidade que vale citar:** no MFM, λ só muda o padrão espacial, porque o volume é o medido. Com padrão λ = 0,05, o MFM chega a 18,5% / 94% / 0,81, perto da IC. Isso sugere que o padrão espacial do SCS-CN com λ = 0,20 concentra demais o escoamento. Mantivemos λ = 0,20 por decisão, e isso vai como sensibilidade.

Vale mostrar essas duas mudanças ao orientador antes de reescrever o resumo e as conclusões.

---

## Resumo (PT)

- **Trocar** "A erosão local seguiu Hao et al. (2022) e a vazão de base, que compõe parte da carga medida no exutório, entrou como um termo separado da bacia."
  → "A erosão local seguiu Hao et al. (2022), com a MUSLE alimentada apenas pelo escoamento direto, já que a vazão de base não produz erosão nas encostas."
- **Trocar** "Com apenas chuva e vazão inicial como entrada, o modelo acertou 71% dos eventos dentro de fator 2 (erro mediano de 33%), desempenho equivalente ao de uma regra simples com a chuva do evento."
  → "Com apenas a chuva como entrada, o modelo acertou 24% dos eventos dentro de fator 2 (erro mediano de 98%), abaixo de uma regra simples com a chuva do evento (82%; 42%), porque o SCS-CN erra o escoamento direto em 69% na mediana dos eventos."
- **Trocar** "Com a água forçada ao valor medido (escoamento direto e vazão de base), o acerto sobe a 94% dos eventos e o erro mediano cai a 14%."
  → "Com o escoamento direto forçado ao valor medido, o acerto sobe a 94% dos eventos e o erro mediano cai a 39%."
- **Trocar** "A espacialização mantém a qualidade da formulação concentrada e acrescenta o mapa de áreas críticas, que permite direcionar medidas de contenção."
  → "A espacialização não melhora a estimativa da carga total em relação a regras simples ou à formulação concentrada, mas acrescenta o mapa de áreas críticas, que permite direcionar medidas de contenção."
- A frase "recalibrar o método SCS-CN contra o escoamento direto não o resolveu" continua válida (Apêndice D).

## Abstract (EN)

Fazer as mesmas quatro trocas. Sugestões:
- "Local erosion followed Hao et al. (2022), with MUSLE driven by direct runoff only, since baseflow does not cause hillslope erosion."
- "With rainfall as the only input, the model placed 24% of the events within a factor of 2 (median error of 98%), below a simple rule based on event rainfall (82%; 42%), because SCS-CN misestimates direct runoff by 69% in the median event."
- "With direct runoff forced to measured values, the hit rate rises to 94% and the median error drops to 39%."
- "Spatialization does not improve the estimate of the total load relative to simple rules or the lumped formulation, but it adds the map of critical areas, which allows erosion control measures to be targeted."

## 1.3.2 Objetivos específicos

- "Identificar o fator que mais limita a qualidade das estimativas (a vazão de base, o escoamento ou a erosão)" → tirar "a vazão de base": "(o escoamento ou a erosão)".

## 3.2 Dados observados

- Parágrafo "O volume e a carga medidos incluem a vazão de base…": **trocar as duas últimas frases** ("Do mesmo modo, SYobs é a carga total… (seção 4.5).") por:
  "SYobs é a carga total. Neste trabalho, todo o sedimento do evento é atribuído ao escoamento superficial, que o mobiliza nas encostas; a vazão de base é tratada apenas como água que o transporta e serve para obter o escoamento direto medido (seção 4.5)."
- A Tabela 1 (linha Bt, "Separação do escoamento direto") e a Tabela 3 continuam certas.

## 4.1 Visão geral

- Item "a erosão dos pixels é somada, e o sedimento do evento é escrito como a soma de dois termos…" → "a erosão dos pixels é somada e multiplicada por um coeficiente de escala c, que converte o índice de erosão em toneladas (seção 4.5);"
- Item "os dois parâmetros de escala do modelo são calibrados…" → "o coeficiente c é calibrado contra o sedimento medido no exutório, em escala logarítmica (seção 4.6);"
- Item "validação cruzada leave-one-out aninhada" → "validação cruzada leave-one-out" (com um único coeficiente, não há mais etapa aninhada).
- Parágrafo do MC e do MFM: trocar "em que o volume de escoamento direto e a vazão de base são os medidos" → "em que o volume de escoamento direto é o medido".
- **Figura 4 (fluxograma):** substituir pela nova `TCC_Texto/figuras/mapas/fig_fluxograma.png`. O termo de base saiu e a equação agora é SY = c · ΣE_unit.

## 4.2.x Tabela 6 (variáveis)

- **Tirar** as linhas Qbinicio e Tchuva: só eram usadas no termo de base. Elas continuam na Tabela 2, que é descritiva.
- Manter Vbase: é usado para obter Vdir = TR − Vbase.

## 4.4 Vazão de pico local e erosão local

- Última frase: "O fator c₁ da seção seguinte converte esse índice em toneladas." → "O coeficiente c da seção seguinte converte esse índice em toneladas."

## 4.5 Sedimento do evento — reescrever a seção inteira

Novo título: **"4.5 Sedimento do evento"**. Texto sugerido:

> O sedimento de cada evento é a soma do índice de erosão de todos os pixels de cálculo, multiplicada por um coeficiente de escala:
>
> SY = c · Σₖ E_unit,k
>
> A MUSLE é alimentada somente pelo escoamento direto. A vazão de base, água subterrânea que já alimentava o rio, não produz erosão nas encostas, e por isso não entra no cálculo. Todo o sedimento medido no exutório é atribuído ao escoamento superficial, que o mobiliza; a vazão de base apenas o transporta. O coeficiente c converte o índice em toneladas e absorve também a diferença de escala entre o coeficiente de Williams e o pixel; não deve ser lido como razão de entrega de sedimentos. O mapa de áreas críticas mostra c · E_unit,k em cada pixel.
>
> As duas versões do modelo diferem apenas na origem da água (Tabela 7):
>
> **Modelo Calculado (MC):** Q vem do SCS-CN a partir da chuva interpolada; só usa a chuva dos postos.
>
> **Modelo Forçado ao Medido (MFM):** o volume de escoamento direto é forçado ao valor medido, Vdir = TR − Σ Bt · 3600. O SCS-CN apenas distribui esse volume no espaço: todos os pixels são multiplicados pelo mesmo fator f = Vdir / VSCS, em que VSCS é o volume que o SCS-CN calcularia, e o escoamento do pixel é limitado à chuva do pixel, Q = min(f · QSCS, P). Não é previsão: mostra o desempenho que o modelo atingiria se a água fosse bem estimada.

**Tabela 7** (nova) — "Origem da água em cada versão do modelo":

| Versão | Escoamento direto |
|---|---|
| Modelo calculado (MC) | SCS-CN, a partir da chuva |
| Modelo forçado ao medido (MFM) | volume medido (TR − Σ Bt), distribuído pelo padrão do SCS-CN |

## 4.6 Calibração dos parâmetros

- **Trocar** "Os parâmetros c₁ e c₂ foram ajustados aos 17 sedimentos medidos minimizando o erro em escala logarítmica:" → "O coeficiente c foi ajustado aos 17 sedimentos medidos minimizando o erro em escala logarítmica:"
- **Trocar a equação** por: min_c Σₙ [ln SYobs,n − ln(c · ΣE_n)]², cuja solução é **ln c = média(ln SYobs,n − ln ΣE_n)**, ou seja, c é a média geométrica da razão entre o sedimento medido e o índice de erosão.
- **Trocar** "em que Vref,n é o volume de referência do termo de base. Esse critério pesa… O problema foi resolvido por mínimos quadrados não lineares com limites (algoritmo de região de confiança), a partir de três pontos de partida, e a melhor solução foi mantida."
  → "Esse critério pesa os eventos pelo erro relativo e evita que um único evento muito grande (o evento 15 responde por 48,7% da variância linear da carga medida e por 49% do peso na calibração por mínimos quadrados lineares) comande o ajuste. Com um único coeficiente, a solução é direta."
- **Tabela 8:** tirar as 4 linhas de c₁/c₂ e pôr (fonte: `tab_parametros.md`):
  - MC: c (t por unidade de E_unit) | **0,0784** | calibrado em log, 17 eventos
  - MFM: c (t por unidade de E_unit) | **0,0302** | calibrado em log, 17 eventos

## 4.7 Validação cruzada

- Trocar "(ii) ajustam-se c₁ e c₂ (e, nos modelos de comparação, os parâmetros de cada um)" → "(ii) ajusta-se c (e, nos modelos de comparação, os parâmetros de cada um)".
- Se mudar o título de "aninhada", mudar também no 4.1. A frase "qualquer etapa que dependa de ajuste é refeita dentro de cada rodada" continua certa.

## 4.9 Exemplo numérico — Tabela 9 (evento 11)

Mudam só as linhas finais:

| Antes | Depois |
|---|---|
| sedimento do pixel c₁ · Eunit = 0,00352 · 1,038 = 0,0037 t (3,7 kg) | sedimento do pixel c · Eunit = 0,0784 · 1,038 = 0,0814 t (81 kg) |
| soma de Eunit sobre os pixels = 30.003 | (igual) 30.003 |
| termo das encostas c₁ · ΣE = 106 t | sedimento do evento c · ΣE = 0,0784 · 30.003 = 2.353 t |
| volume de referência da base … = 78.226 m³ | **apagar a linha** |
| termo de base c₂ · volume = 1.025 t | **apagar a linha** |
| MC: validação cruzada 1.098 t (−40%) | MC: validação cruzada **2.391 t (+31%)** |
| MFM: validação cruzada 1.711 t (−6%) | MFM: validação cruzada **1.931 t (+6%)** |

- Figura 5 (`mapa_08_evento11.png`): substituir pela nova (painel de sedimento com c · E_unit e os valores novos).

## 5.2 Resultados do Modelo Calculado (MC) — reescrever

Texto sugerido:

> O MC (só chuva) obteve c = 0,0784 t por unidade de E_unit (Tabela 8). Na validação cruzada, o erro percentual mediano foi de 98%, e só 24% dos eventos (4 de 17) ficaram dentro de fator 2; o NSE em escala logarítmica foi −3,95 e a correlação de Spearman, 0,57. O erro tem sinal sistemático: o MC subestima muito os eventos de chuva pequena (1, 4, 7, 10 e 12, de −73% a −98%), em que o SCS-CN quase não gera escoamento, e superestima os de chuva grande (3, 8, 9, 13 a 16, de +211% a +655%) (Tabela 10). A Figura 6 compara o sedimento simulado, na validação cruzada, com o medido em cada evento.

- **Tabela 10:** substituir pela nova `TCC_Texto/tabelas/tab_mc_mfm_eventos.md`. Ela traz, por evento: medido, MC (ajuste e validação cruzada), MFM (ajuste e validação cruzada) e a razão SCS-CN/medido do escoamento direto. Novo título: "Tabela 10. Sedimento por evento (t): medido e simulado pelo MC e pelo MFM, e razão entre o escoamento direto do SCS-CN e o medido."
- **Figura 6** (`fig_dispersao.png`): agora tem 4 painéis. Nova legenda: "Sedimento simulado e medido nos 17 eventos, validação leave-one-out, para a referência simples (SY = c · chuva), o MC, o MFM e a IC. A faixa clara indica fator 2."
- **Parágrafo "Nas previsões do MC, a vazão de base carrega a maior parte…" e Figura 7:** apagar os dois. A figura antiga (`fig_decomposicao.png`) foi removida. No lugar, sugestão:
  > O erro do MC vem do escoamento. O escoamento direto calculado pelo SCS-CN fica entre 0,02 e 1,95 vezes o medido, com erro mediano de 69% e NSE do volume de −0,69 (Figura 7). Ele é quase nulo nos eventos de chuva pequena e excessivo nos de chuva grande, e como a erosão cresce com Q^1,12, o erro do volume é amplificado no sedimento.
  >
  > Figura 7. Escoamento direto por evento: calculado pelo SCS-CN (λ = 0,20) x medido (TR − Σ Bt). (`TCC_Texto/figuras/fig_volume_direto.png`)

## 5.3 O gargalo — atualizar os números

Texto sugerido:

> Forçando o escoamento direto ao valor medido, a fração de eventos dentro de fator 2 sobe de 24% para 94% e o erro mediano cai de 98% para 39%; o NSE em log passa de −3,95 a 0,50 e o Spearman de 0,57 a 0,86. O que muda entre as duas versões é só a água: a fórmula de erosão e os fatores do solo, do uso e do relevo são os mesmos. A qualidade do sedimento estimado depende, portanto, da qualidade da estimativa do escoamento.

- Apagar a última frase ("O erro mediano de 14% exige, porém, que tanto a água das encostas quanto a vazão de base sejam as medidas.").
- Opcional, como sensibilidade: "No MFM, λ só altera a distribuição espacial do volume medido; com o padrão de λ = 0,05, o erro mediano cai a 18,5% (94% em fator 2; NSE em log de 0,81), o que indica que o padrão do SCS-CN com λ = 0,20 concentra o escoamento em poucos pixels."

## 5.4 Testes simples — reescrever

Novo título: **"5.4 A MUSLE espacializada e os testes simples"**. Texto sugerido:

> Com os mesmos insumos, a MUSLE espacializada fica abaixo das regras simples de um coeficiente. Só com a chuva, o MC tem erro mediano de 98% e 24% dos eventos em fator 2, contra 42% e 82% de SY = c · chuva. Com o escoamento direto medido, o MFM tem 39% e 94%, contra 16% e 94% de SY = c · volume direto medido. Para a carga total no exutório, a distribuição espacial do escoamento e dos fatores K, C e LS não acrescenta informação além do volume do evento; o ganho da espacialização é saber onde a erosão ocorre.

## 5.5 Comparação com a IC

**Tabela 11** — trocar as linhas do MC e do MFM e acrescentar a de volume direto:

| Modelo | Informação medida usada | Erro mediano | Dentro de fator 2 | NSE em log | Spearman |
|---|---|---|---|---|---|
| SY = c · chuva do evento | chuva | 41,9% | 82% | 0,53 | 0,63 |
| MC | chuva | **97,9%** | **24%** | **−3,95** | **0,57** |
| SY = c · volume direto medido | volume direto | 15,9% | 94% | 0,85 | 0,90 |
| SY = c · volume total medido | volume total | 17,6% | 94% | 0,86 | 0,88 |
| MFM | volume direto | **38,7%** | **94%** | **0,50** | **0,86** |
| IC | volume total e pico | 16,3% | 100% | 0,87 | 0,93 |

**Texto** — trocar o parágrafo por:

> Como mostra a Tabela 11, a formulação concentrada da IC, com volume e pico medidos do próprio hidrograma, tem o melhor desempenho (16,3% de erro mediano; 100% dos eventos dentro de fator 2). O MFM, que recebe o escoamento direto medido, acerta a ordem de grandeza de 94% dos eventos, mas tem erro mediano maior (38,7%). No NSE linear, os dois são equivalentes (0,77 na IC; 0,79 no MFM com calibração linear), porque o NSE linear é dominado pelos eventos grandes, que o MFM acerta bem. A IC, no entanto, não prevê (precisa do hidrograma do evento, que gera também o sedimento medido), não gera mapa e seus coeficientes foram ajustados nos mesmos 17 eventos. A espacialização não melhora a estimativa da carga total, mas acrescenta o mapa de áreas críticas.

## 5.6 Mapas

- Figuras 8, 9 e 10: substituir pelas novas (`mapa_04`, `mapa_05` e `mapa_06`). O padrão espacial é o mesmo; muda só a escala do sedimento.
- §5.6.2: "correlação de 0,97; 90,9% das áreas críticas coincidem" e "0,69 com K · LS · C" **continuam valendo**: o padrão dos dois mapas não mudou, só a escala. A Figura 11 (`mapa_07`) deve ser substituída.
- **Tabelas 12 e 13:** as **porcentagens não mudam**; mudam as colunas de kg/pixel. Copiar de `tab_classes_uso.md` e `tab_classes_solo.md`. Por exemplo, Campo: MC 37,43 e MFM 14,48 kg/pixel (antes 1,68 e 4,73). O kg/pixel do MC ficou alto porque o MC superestima muito os eventos grandes; vale uma frase dizendo que o mapa deve ser lido em termos relativos.
- Frase final do 5.6.2 ("A coincidência dos mapas entre o MC e o MFM não constitui validação independente…"): continua certa.

## 6. Conclusões

- **1ª:** "…não é comparável a eles sem uma separação ou um termo de base." → "…não é comparável a eles sem separar a vazão de base."
- **2ª:** continua certa.
- **3ª — trocar inteira:**
  > Alimentada só pelo escoamento direto, que é a parcela que causa erosão nas encostas, a MUSLE espacializada calculada a partir da chuva tem desempenho inferior ao de uma regra simples com a chuva do evento (erro mediano de 98% contra 42%; 24% contra 82% dos eventos dentro de fator 2).
- **4ª — trocar inteira:**
  > O gargalo está em transformar chuva em escoamento: com o escoamento direto forçado ao valor medido, 94% dos eventos ficam dentro de fator 2 e o erro mediano cai de 98% para 39%.
- **5ª — trocar inteira:**
  > Para a carga total no exutório, a espacialização não supera regras simples nem a formulação concentrada da IC quando recebe informação equivalente; sua contribuição é o mapa de áreas críticas, que indica onde a erosão ocorre e permite direcionar medidas de contenção.

## Apêndice B (se for incluir)

- Tabela de NSE linear atualizada: `TCC_Texto/tabelas/tab_nse_linear.md`. As linhas "não adotado" registram os modelos com termo de base, para comparação.

## Arquivos novos ou atualizados (para copiar para o Doc)

| O quê | Arquivo |
|---|---|
| Tabela 8 (parâmetros) | `TCC_Texto/tabelas/tab_parametros.md` |
| Tabela 10 (por evento, nova) | `TCC_Texto/tabelas/tab_mc_mfm_eventos.md` |
| Tabela de resultados (c · chuva, MC, MFM, IC) | `TCC_Texto/tabelas/tab_resultados.md` |
| Tabelas 12 e 13 | `TCC_Texto/tabelas/tab_classes_uso.md`, `tab_classes_solo.md` |
| Apêndice B | `TCC_Texto/tabelas/tab_nse_linear.md` |
| Figura 4 (fluxograma) | `TCC_Texto/figuras/mapas/fig_fluxograma.png` |
| Figura 5 (evento 11) | `TCC_Texto/figuras/mapas/mapa_08_evento11.png` |
| Figura 6 (dispersão, 4 painéis) | `TCC_Texto/figuras/fig_dispersao.png` |
| Figura 7 (nova: escoamento SCS-CN × medido) | `TCC_Texto/figuras/fig_volume_direto.png` |
| Figuras 8–11 | `TCC_Texto/figuras/mapas/mapa_04` a `mapa_07` |
| Escada do gargalo (se usar) | `TCC_Texto/figuras/escada_gargalo.png` |
