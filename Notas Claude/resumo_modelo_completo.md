# O modelo completo: dados, passos, métodos, referências e justificativas

Atualizado em 27/10/2026. Base para escrever a Metodologia. Cada passo traz **o que é feito**, **de onde vem** (referência ou dado) e **por que** (justificativa). Os detalhes e os testes estão em `notas_musle_espacializada.md`, nas seções indicadas.

> **Estado da decisão.** O modelo **adotado hoje** (script `calcular_sy_so_direto.py`) usa CN-I e λ = 0,20. O **candidato** (script `calcular_sy_lambda005_woodward.py`, sufixo `_l05w`) usa CN-I, λ = 0,05 e a retenção convertida pela relação de Woodward. O candidato é o que estamos considerando adotar; falta a aprovação do orientador. As figuras e tabelas do TCC ainda são do adotado.

---

## 1. Dados de entrada

| Dado | Fonte | Uso |
|---|---|---|
| Chuva horária em 2 postos: DBT5 (fora da bacia, a leste) e Rio Jundiaí em Campo Limpo Paulista (perto do exutório) | série de monitoramento (MURILLO-BERMÚDEZ; MARTIM, 2022) | entrada dos dois modelos |
| Vazão horária na seção de controle | DAEE / SAISP, telemetria a cada 10 min, usada em passo horário | volume, pico e vazão inicial medidos |
| Concentração de sedimentos em suspensão (CSS) | turbidez horária da ETA da SABESP convertida por curva de calibração (MURILLO-BERMÚDEZ et al., 2023) | carga medida |
| Vazão de base (Bt) | filtro de Eckhardt (2005), α = 0,995 e BFImax = 0,70, calibrado segundo Collischonn e Fan (2013), aplicado pelo orientador (§28) | separar o escoamento direto medido |
| 17 eventos (11/2018 a 02/2020) | definidos na base de dados (janelas de 23 a 149 h) | unidade de análise |
| MDE de 30 m | USGS, corrigido e em SIRGAS 2000 / UTM 23S (§24) | relevo e fator LS |
| Mapas de solo e de uso | Plano de Bacias PCJ (CONSÓRCIO PROFILL-RHAMA, 2020) | fatores K e C |
| Valores de K e C por classe | IC (VIVARELLI et al., 2025), com fonte por classe (Tabelas `tab_fator_K.md` e `tab_fator_C.md`) | erodibilidade e cobertura |
| Número de curva (CN-II) | ANA, BR_CN-2022, 30 m (ANA, 2024): uso do MapBiomas 2022, solo do IBGE e grupos hidrológicos de Sartori, Lombardi Neto e Genovez (2005) (§25.5) | escoamento |
| Fator P | constante igual a 1 | sem práticas conservacionistas mapeadas |

**Grandezas medidas por evento:**
- SY_obs = Σ Q · CSS · 3600 (carga **total**, em t);
- T_R = Σ Q · 3600 (volume **total**, que inclui a base);
- V_dir = Σ (Q − Bt) · 3600 (escoamento **direto** medido);
- vazão de pico, vazão no início do evento.

A base é 34% a 55% do volume de cada evento (§15).

**Grade:** 884 × 365 pixels de 897,49 m². O cálculo usa os 153.855 pixels (138,1 km²) que têm CN, K, C e LS ao mesmo tempo (§24, §25).

---

## 2. Passo a passo

### Passo 1 — Chuva do evento e chuva em cada pixel
- **Lâmina do evento:** R = 0,307 · P_DBT5 + 0,693 · P_CampoLimpo. Os pesos foram ajustados por mínimos quadrados nos 17 eventos.
- **Chuva no pixel:** inverso do quadrado da distância (IDW) entre os dois postos, P(x) = (P₁·d₂² + P₂·d₁²)/(d₁² + d₂²).
- **RI:** intensidade máxima de chuva em 60 min.
- *Por quê:* só há dois postos; o IDW é o interpolador mais simples e transparente. Com dois postos, o resultado é um gradiente suave entre eles.

### Passo 2 — Condição de umidade antecedente: CN-I
- **O que:** o CN-II da ANA é convertido para a condição seca (AMC I) pela fórmula de Chow, Maidment e Mays (1988): CN_I = 4,2·CN_II / (10 − 0,058·CN_II). O raster confere exatamente com essa fórmula (§25).
- **Por quê (§31):** pelo critério do NEH-4 (USDA-SCS, 1972), a chuva dos 5 dias anteriores coloca **13 dos 17 eventos em AMC I**. Usamos os limites da estação de crescimento, porque o período chuvoso é de vegetação ativa. O CN-I é usado como **condição representativa do conjunto**.
- **Testado e rejeitado:** aplicar a umidade evento a evento, como o NEH-4 manda. Os eventos AMC III ficam com volume de 1,75 a 6,6 vezes o medido (viés de +85%).

### Passo 3 — Retenção e abstração inicial
- S = 25,4 · (1000/CN − 10) (mm).
- **Adotado hoje:** λ = 0,20, o valor padrão do método.
- **Candidato:** λ = 0,05, com a retenção convertida, S₀,₀₅ = 1,33 · S₀,₂₀^1,15 (S em polegadas; WOODWARD et al., 2003).
- **Por que o candidato (§30):**
  1. A literatura sustenta λ baixo: Woodward et al. (2003) propõem 0,05; Valle Junior, Rodrigues e Oliveira (2019) acharam mediana de 0,045 numa bacia brasileira; Brandão et al. (2025), em 3.578 bacias, ficaram perto de 0.
  2. O CN tabelado vale para λ = 0,20; usar 0,05 exige converter S, senão o escoamento infla (+94%).
  3. Com a conversão, é a configuração em que o volume calculado mais se aproxima do escoamento direto medido: viés de +3% e NSE do volume de −0,39, contra −12% e −0,69 com λ = 0,20.
  4. Corrige o defeito do λ = 0,20 nas chuvas pequenas, em que o escoamento ficava concentrado nas áreas urbanas, onde C = 0 (§29).
- ⚠️ Conferir a fórmula de conversão no original (citada de memória; metadados conferidos no Crossref).

### Passo 4 — Escoamento direto em cada pixel (SCS-CN)
- Q = (P − λS)² / (P + (1 − λ)S) se P > λS; senão Q = 0 (USDA-SCS, 1972; CHOW; MAIDMENT; MAYS, 1988).

### Passo 5 — Origem da água: dois modelos
- **MC (calculado):** Q do passo 4, só a partir da chuva. É a previsão.
- **MFM (forçado ao medido):** o SCS-CN só distribui no espaço o escoamento direto **medido**. Todos os pixels são multiplicados por f = V_dir / V_SCS, com Q ≤ P. Não é previsão: mostra o desempenho possível com a água certa.
- *Por quê:* separar a qualidade da água da qualidade da fórmula de erosão. É daí que vem o diagnóstico do gargalo.

### Passo 6 — Vazão de pico local
- pr = (Q/1000) · A_pix · (RI/R) / 3600 (m³/s), sem propagação (HAO et al., 2022).
- **Testado (§29):** forçar o pico medido no MFM não melhora o resultado, porque c absorve a escala e a razão pico/volume da chuva já acompanha a medida.

### Passo 7 — Erosão local (MUSLE no pixel)
- E_unit = 11,8 · (Q · pr · A_pix)^0,56 · K · C · LS · P (WILLIAMS, 1975; HAO et al., 2022). Os coeficientes de Williams são mantidos.
- **LS:** Moore e Burch (1986), sobre o MDE corrigido em UTM, com a área de contribuição limitada a 200 m (§24). O LS herdado da IC estava errado e foi refeito.
- E_unit é um **índice relativo**: o coeficiente de Williams foi ajustado em escala de bacia, não de pixel.

### Passo 8 — Sedimento do evento: só escoamento direto
- SY = c · Σ E_unit. **Não há termo de vazão de base.**
- **Por quê (decisão com o orientador, 26/10; §27):** a MUSLE descreve erosão por escoamento superficial, e a base não erode encostas. O termo empírico de base carregava 91% do sedimento sem significado físico. O trabalho em que a IC se baseou também não considera a base.
- **Alvo:** a carga total medida. Todo o sedimento do evento é atribuído ao escoamento superficial, que o mobiliza; a base só o transporta.

### Passo 9 — Calibração de c
- Mínimos quadrados em escala log: ln c = média(ln SY_obs − ln Σ E). Equivale a maximizar o NSE em log.
- *Por quê (§18):* o evento 15 responde por 49% da variância linear. A calibração em log pesa os eventos pelo erro relativo. A calibração linear entra só como sensibilidade.

### Passo 10 — Validação cruzada e métricas
- Leave-one-out: c é refeito sem o evento avaliado, nas 17 rodadas.
- **Métricas principais:** erro percentual mediano, fração dentro de fator 2, Spearman, NSE em log.
- **Secundária:** NSE linear (NASH; SUTCLIFFE, 1970), com e sem o evento 15.

### Passo 11 — Comparações justas (mesma informação)
- MC × **SY = c · chuva** (só chuva).
- MFM × **SY = c · volume direto medido** e × **IC concentrada** (VIVARELLI et al., 2025).
- A IC usa o volume **total** e o pico total medidos, apesar de o texto dela dizer "escoamento superficial". Só com o total os erros publicados se reproduzem.

### Passo 12 — Mapa de áreas críticas
- Média de c · E_unit nos 17 eventos. Áreas críticas: os 5% de pixels de maior contribuição.
- Contribuição por classe de uso e de solo. Leitura relativa: não há validação espacial, porque só há medição no exutório.

---

## 3. Resultados (validação cruzada, calibração em log, carga total)

| Modelo | Erro mediano | Fator 2 | NSE em log | NSE linear |
|---|---|---|---|---|
| **MC candidato** (λ 0,05, S convertido) | 81,1% | 35% | −0,69 | −5,43 |
| MC adotado hoje (λ 0,20) | 97,9% | 24% | −3,95 | −65,3 |
| SY = c · chuva | 41,9% | 82% | 0,53 | 0,58 |
| **MFM candidato** | **20,6%** | **94%** | **0,84** | **0,78** |
| MFM adotado hoje | 38,7% | 94% | 0,50 | 0,50 |
| SY = c · volume direto medido | 15,9% | 94% | 0,85 | 0,74 |
| IC concentrada | 16,3% | 100% | 0,87 | 0,77 |

- **MFM candidato × IC:** diferença no erro por evento de +6,1 pontos, com IC95% de [−8,6; +7,9]. Não se distingue do ruído. O resultado é estável na calibração linear (20,4% / 94% / NSE 0,77).
- **Mapa:** o candidato coincide com o adotado em 95% das áreas críticas no MC e 91% no MFM. MC × MFM no candidato: 94%.
- **Volume do SCS-CN (candidato):** mediana de 0,86 vezes o medido (de 0,10 a 2,15), erro mediano de 46%.

**Conclusões com o candidato:**
1. O gargalo é a conversão chuva → escoamento: o MC fica abaixo da regra da chuva.
2. Com a água medida, a MUSLE espacializada empata com a IC e com a regra do volume, e acrescenta o mapa.
3. As áreas críticas são robustas à configuração.

---

## 4. Decisões e pendências

1. **Levar ao orientador:** adotar o candidato (λ 0,05 + Woodward) nos dois modelos? Se sim, migrar tabelas, figuras e mapas do TCC e refazer a lista de mudanças do Doc.
2. **BFImax:** 0,70 (o que reproduz a série) ou 0,58 (o que diz o cabeçalho da planilha)?
3. **Conferir no original:** a fórmula de Woodward et al. (2003); a frase de Bedient e Huber (1992) no Koskelo et al. (2012); os valores-guia de BFImax em Eckhardt (2005).
4. **Fontes que faltam na IC:** C = 0 da área urbanizada, C = 1 da mineração e do afloramento, K = 0 da área urbana.
5. **Limitação a declarar:** λ, CN-I e a calibração foram escolhidos olhando os mesmos 17 eventos. A justificativa deve vir da água, e o sedimento entra como consequência.

## Figuras ilustrativas (não são do TCC) — `Figuras/ilustrativas_27-10/`

- **A_configuracoes_testadas.png:** as 5 configurações (viés da água, MC, MFM).
- **B_volume_scs_x_medido.png:** escoamento direto do SCS-CN × medido, adotado × candidato.
- **C_sedimento_candidato.png:** sedimento simulado × medido, candidato contra as referências.
- **D_agua_em_pixels_sem_erosao.png:** por que λ 0,20 falha nas chuvas pequenas.
- **E_mapas_forcado_adotado_x_candidato.png:** mapas e coincidência das áreas críticas.
