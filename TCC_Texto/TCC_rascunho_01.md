# Espacialização da Equação Universal Modificada de Perda de Solo (MUSLE) para Identificação de Áreas Críticas de Erosão: Estudo de Caso na Bacia do Rio Jundiaí

**Autor:** Mateus Vivarelli
**Orientador:** [PREENCHER]
**Rascunho 01 — 15/10/2026**

> **Como ler este rascunho.** Trechos marcados com **[PENDENTE: ...]** dependem de uma decisão com o orientador, de uma conferência ainda em andamento ou de um dado que falta. Referências marcadas com **[conferir]** não estão nos PDFs do projeto e precisam ter os dados bibliográficos checados antes da entrega. Os números dos resultados vêm de `Notas Claude/` e de `Comparacao_Modelos_TCC.xlsx`.

---

## RESUMO

A Equação Universal Modificada de Perda de Solo (MUSLE) estima a produção de sedimentos de eventos de chuva, mas, em sua forma concentrada, trata a bacia como uma unidade homogênea e não indica onde a erosão se origina. Este trabalho espacializa a MUSLE em pixels de cerca de 30 m na parte alta da bacia do rio Jundiaí (137,8 km², São Paulo), para 17 eventos de chuva monitorados entre novembro de 2018 e fevereiro de 2020. O escoamento foi calculado pelo método SCS-CN sobre chuva interpolada por IDW a partir de dois postos; a vazão de pico local e a erosão local seguiram Hao et al. (2022); e um único parâmetro de escala, calibrado contra a carga de sedimentos medida no exutório, converte a erosão local em produção de sedimentos. Com o escoamento calculado pelo modelo, o ajuste obteve NSE de 0,37 (0,28 em validação cruzada *leave-one-out*); com o volume escoado medido como restrição, o NSE foi de 0,81 (0,78 em validação cruzada). O erro vem, portanto, sobretudo da estimativa hidrológica e não da estrutura espacial. Uma etapa de conectividade de sedimentos foi implementada e não melhorou o resultado. Os mapas apontam áreas críticas associadas a usos do solo de maior fator C e maior declividade, com padrão espacial estável entre as duas versões. **[PENDENTE: revisar após a decisão sobre o volume observado, que inclui vazão de base.]**

**Palavras-chave:** MUSLE; produção de sedimentos; SCS-CN; modelagem distribuída; SIG; bacia do rio Jundiaí.

## ABSTRACT

The Modified Universal Soil Loss Equation (MUSLE) estimates event-scale sediment yield, but in its lumped form it treats the basin as a homogeneous unit and does not show where erosion originates. This work spatializes the MUSLE at a ~30 m pixel scale in the upper Jundiaí River basin (137.8 km², São Paulo, Brazil) for 17 rainfall events monitored between November 2018 and February 2020. Runoff was computed with the SCS-CN method over rainfall interpolated by IDW from two gauges; local peak discharge and local erosion followed Hao et al. (2022); and a single scale parameter, calibrated against the sediment load measured at the outlet, converts local erosion into sediment yield. With model-derived runoff, the fit reached an NSE of 0.37 (0.28 under leave-one-out cross-validation); with measured runoff volume as a constraint, the NSE was 0.81 (0.78 under cross-validation). The error therefore comes mainly from the hydrological estimate rather than from the spatial structure of the model. A sediment connectivity step was implemented and did not improve the results. The maps point to critical areas associated with land uses of higher C factor and steeper slopes, with a spatial pattern that is stable between the two versions.

**Keywords:** MUSLE; sediment yield; SCS-CN; distributed modelling; GIS; Jundiaí River basin.

## 1. INTRODUÇÃO

### 1.1 Contexto

O transporte de sedimentos fluviais é um problema ambiental, social e econômico: afeta a gestão dos recursos hídricos, a qualidade da água e a vida útil de reservatórios. A bacia hidrográfica do rio Jundiaí, no estado de São Paulo, reúne áreas de grande concentração urbana e atividades agrícolas intensivas, o que a torna vulnerável a processos erosivos e ao aumento da carga de sedimentos nos cursos d'água.

Em uma Iniciação Científica anterior (VIVARELLI et al., 2025), a produção de sedimentos na bacia foi quantificada com a Equação Modificada de Perda de Solo (MUSLE; WILLIAMS, 1975), que estima a produção de sedimentos por evento. Essa aplicação foi **concentrada**: as características topográficas, de solo e de uso foram resumidas em valores médios para toda a bacia. A simplificação permite validar o modelo no exutório, mas impede identificar as áreas que mais geram sedimento e representar a heterogeneidade local.

### 1.2 Problema e justificativa

Passar de uma pesquisa de calibração técnica para um estudo útil à gestão da bacia exige resultados distribuídos no espaço. Coletar novos dados de vazão de sedimentos é difícil e caro, porque depende da coincidência entre eventos de chuva significativos e visitas a campo; dividir a bacia em seções com novos postos de medição é inviável no prazo de um TCC.

A premissa deste trabalho é aproveitar a base de dados já levantada, de escoamento e de descarga sólida em suspensão em 17 eventos, e substituir o modelo concentrado por um modelo **espacializado**, em células. Assim é possível verificar o modelo em escala de bacia e, além disso, mapear onde a erosão é gerada em cada evento, identificando *hot spots* erosivos.

### 1.3 Objetivos

**Objetivo geral.** Desenvolver e aplicar a espacialização da MUSLE em ambiente de Sistemas de Informação Geográfica (SIG) para identificar áreas críticas de erosão na parte alta da bacia do rio Jundiaí.

**Objetivos específicos.**

1. Espacializar o escoamento superficial (Q) de cada um dos 17 eventos pelo método SCS-CN e calcular a vazão de pico local (pr) por pixel, segundo Hao et al. (2022);
2. Mapear, em formato raster, os fatores físicos da MUSLE: erodibilidade do solo (K), fator topográfico (LS), cobertura e manejo (C) e práticas conservacionistas (P);
3. Implementar uma rotina computacional em Python/SIG que automatize o cálculo espacializado da MUSLE;
4. Validar o modelo distribuído comparando a soma da produção de sedimentos de todos os pixels com a carga de sedimentos medida na seção de controle em cada evento;
5. Avaliar a incorporação de um índice de conectividade de sedimentos (Hao et al., 2022) ao modelo.

> **Alterações em relação ao Projeto (TFC I).** (a) A simulação de cenários de conservação (alteração de C e P) foi retirada do escopo em 14/09/2026, por decisão do autor em função do prazo; ela fica como trabalho futuro. (b) A vazão de pico deixou de ser distribuída por um raster de tempo de resposta e passou a seguir a formulação local de Hao et al. (2022), que dispensa roteamento. (c) O objetivo 5 foi incluído porque a etapa de conectividade foi implementada e testada.

---

## 2. FUNDAMENTAÇÃO TEÓRICA

[PENDENTE: esta seção é um roteiro; cada item deve virar 1–2 páginas com citações. A Apostila (`Apostila_TCC_Do_dado_ao_mapa.pdf`) já tem o conteúdo técnico de cada item e pode ser usada como base.]

**2.1 Erosão hídrica e produção de sedimentos.** Processos de desagregação, transporte e deposição; produção de sedimentos em escala de evento e de bacia; razão de aporte de sedimentos.

**2.2 USLE e MUSLE.** A USLE (WISCHMEIER; SMITH, 1978) estima a perda média anual de solo com a energia da chuva. Williams (1975) substituiu o fator de erosividade da chuva por um fator de energia do escoamento, o que permite estimar a produção de sedimentos de **eventos isolados**:

> Y = 11,8 · (Q · qp)^0,56 · K · LS · C · P

em que Y é a produção de sedimentos do evento (t), Q é o volume de escoamento (m³), qp é a vazão de pico (m³/s) e K, LS, C e P são os fatores da USLE. Os coeficientes 11,8 e 0,56 foram ajustados por Williams em escala de bacia.

**2.3 Método SCS-CN.** O escoamento direto é obtido da chuva P e da retenção potencial máxima S (mm), que depende do número de curva CN (USDA-SCS, 1972; CHOW; MAIDMENT; MAYS, 1988):

> S = 25,4 · (1000 / CN − 10)
> Q = (P − λS)² / (P + (1 − λ)S), para P > λS; Q = 0 caso contrário

A razão de abstração inicial λ vale 0,2 no método original. Brandão et al. (2025) analisaram 3.578 bacias e concluíram que λ = 0,05 supera o valor 0,2 na maioria dos casos; Valle Junior, Rodrigues e Oliveira (2019) estimaram λ mediano de 0,045 em bacia brasileira (Guariroba, MS). As condições de umidade antecedente (AMC I, II, III) deslocam o CN; a conversão do CN de AMC II para AMC I seguiu CN_I = 4,2·CN_II / (10 − 0,058·CN_II) (CHOW; MAIDMENT; MAYS, 1988) [conferir].

**2.4 MUSLE espacializada e conectividade.** Hao et al. (2022) aplicam a MUSLE por pixel, com uma vazão de pico local derivada do escoamento do pixel e da concentração temporal da chuva, e ponderam a contribuição de cada pixel por um índice de conectividade funcional (FCI), adaptado de Borselli, Cassi e Torri (2008), normalizado por uma sigmoide (DSC).

**2.5 Limites de predição da MUSLE em escala de evento.** Baert et al. (2026), em 154 eventos de uma bacia agrícola pequena, mostram que a MUSLE tem desempenho de validação cruzada razoável (NSE 0,66) quando alimentada por volume e pico *observados*, e desempenho próximo de zero (NSE ≈ 0) em formulações realmente preditivas.

**2.6 Métricas de desempenho.** Eficiência de Nash-Sutcliffe (NSE; NASH; SUTCLIFFE, 1970), índice de concordância de Willmott (WIA; WILLMOTT, 1981), viés percentual (PBIAS) e validação cruzada *leave-one-out*.

---

## 3. ÁREA DE ESTUDO E DADOS

### 3.1 Área de estudo

A área de estudo é a parte alta da bacia do rio Jundiaí, a montante da seção de controle (Rio Jundiaí em Campo Limpo Paulista), com **137,8 km²** de área de contribuição. [PENDENTE: mapa de localização, clima, geologia, população; a fonte é o Plano de Bacias (CONSÓRCIO PROFILL-RHAMA, 2020) e a IC.]

> Nota técnica: a área de contribuição obtida do MDE original era de 109,79 km²; o MDE não representava a passagem de água (bueiro) sob um aterro de estrada, criando uma barreira artificial de drenagem. Corrigida a barreira, a área passou a 137,80 km², consistente com a delimitação de campo (a máscara da bacia tem 138,9 km²).

### 3.2 Dados observados

| Dado | Origem | Uso |
|---|---|---|
| Chuva horária | 2 postos: Desemboque do Túnel 5 (DBT5, fora da bacia, a leste) e Rio Jundiaí em Campo Limpo Paulista (próximo ao exutório) | entrada do modelo |
| Vazão horária (Q) | seção de controle no exutório | validação |
| Concentração de sedimentos em suspensão (CSS) | seção de controle, a partir de turbidez (MURILLO-BERMÚDEZ et al., 2021 [conferir]) | carga de sedimentos observada |
| Eventos | 17 eventos, de 11/2018 a 02/2020, janelas de 23 a 149 h | unidade de análise |

Da série horária obtêm-se, para cada evento: o volume escoado total `T_R_m3 = Σ Q·3600` (m³), a vazão de pico `Q_pico` (m³/s) e a carga de sedimentos observada

> SY_obs = Σ (Q · CSS · 3600 / 10⁶)  (t)

somada sobre as leituras horárias da janela do evento (coluna `SYY_t` da planilha de eventos).

> **[PENDENTE — decisão com o orientador] Volume observado.** `T_R_m3` é o volume **total** escoado no exutório e **inclui a vazão de base**: nos 17 eventos a vazão de base (coluna Bt da série) soma de 34% a 55% desse volume (evento 11: 0,96 de 2,44 milhões de m³). O SCS-CN calcula escoamento **direto**. Do mesmo modo, `SY_obs` é a carga total medida (inclui sedimento carreado pela vazão de base). Ver 5.1 e a Seção 15 de `notas_musle_espacializada.md`.

### 3.3 Dados cartográficos

| Fator | Fonte | Valor médio |
|---|---|---|
| K | mapa pedológico (Plano de Bacias 2020), valor de K por classe de solo da IC | 0,039 |
| C | mapa de uso do solo (Plano de Bacias 2020), valor de C por classe de uso da IC | 0,050 |
| LS | MDE (USGS) pelo método de Moore et al. (1991) no SAGA [conferir] | 0,536 |
| P | constante | 1,0 |
| CN | interseção uso × solo, em 3 cenários de umidade | — |

Todos os rasters usam a grade de 884 × 365 pixels de ~30 m (29,992 × 29,925 m; área do pixel de 897,49 m²), SIRGAS 2000 / UTM 23S. Cerca de 154,7 mil pixels cobrem a bacia.

> [PENDENTE: origem dos valores de CN por combinação uso × solo (tabela e fonte).]

---

## 4. METODOLOGIA

### 4.1 Visão geral

A Figura 1 [PENDENTE: fluxograma] resume o modelo. Para cada evento *n* (n = 1…17): (i) a chuva dos dois postos é interpolada por IDW; (ii) o SCS-CN gera o raster de escoamento Q; (iii) a vazão de pico local pr e (iv) a erosão local E_unit são calculadas pixel a pixel; (v) um fator único de escala *c* converte E_unit em produção de sedimentos, e a soma dos pixels é comparada com SY_obs. Todas as etapas foram automatizadas em Python (GDAL/QGIS).

### 4.2 Chuva espacializada

As chuvas totais dos dois postos em cada evento foram interpoladas pelo inverso do quadrado da distância (IDW, potência 2):

> P(x) = Σ (Pᵢ / dᵢ²) / Σ (1 / dᵢ²),  i = 1, 2

com resolução de 30 m, na grade de referência. Com apenas dois postos, um deles fora da bacia, a interpolação produz um gradiente suave entre os pontos. Para a lâmina do evento (R, mm) usada em 4.4 adotou-se a média ponderada dos postos, com peso de 0,307 para o DBT5 e 0,693 para Campo Limpo, estimados por mínimos quadrados nos 17 eventos para reproduzir a lâmina de evento da planilha (R = w₁p₁ + (1 − w₁)p₂).

### 4.3 Escoamento superficial (SCS-CN)

O escoamento Q (mm) em cada pixel segue as equações da seção 2.3, com duas decisões de calibração: **(a)** cenário de umidade antecedente seco (AMC I) para todos os eventos; **(b)** razão de abstração inicial **λ = 0,05**, em vez de 0,2 (Brandão et al., 2025; Valle Junior et al., 2019). Com λ = 0,2 e AMC I, o volume total ficou 62,6% abaixo do medido; com λ = 0,05, o erro médio passou a +0,5% (erro absoluto médio de 47,4%) em relação ao volume total medido (5.1).

### 4.4 Vazão de pico local (pr) e erosão local (E_unit)

Seguindo Hao et al. (2022), a vazão de pico local do pixel *k* é o escoamento do próprio pixel ponderado pela concentração temporal da chuva, **sem roteamento**:

> pr_k = (Q_k / 1000) · A_pix · (RI / R) / 3600   (m³/s)

em que A_pix é a área do pixel (m²), RI é a intensidade máxima de chuva em 60 min (mm/h) e R é a lâmina do evento (mm). RI/R é um escalar por evento; a variação espacial de pr vem de Q_k. A erosão local é a MUSLE aplicada ao pixel, com os coeficientes originais de Williams:

> E_unit,k = 11,8 · (Q_k · pr_k · A_pix)^0,56 · K_k · LS_k · C_k · P_k

com Q em mm, pr em m³/s e A_pix em m², como em Hao et al. (2022). Como pr ∝ Q, E_unit ∝ Q^1,12.

### 4.5 Produção de sedimentos e calibração de *c*

> SY_k = c · E_unit,k

O parâmetro *c*, único e comum aos 17 eventos, é o de mínimos quadrados pela origem:

> c = Σ (Eₙ · SY_obs,n) / Σ (Eₙ²),  Eₙ = Σₖ E_unit,k do evento n

*c* é um fator empírico de calibração: absorve a diferença de escala entre o coeficiente de Williams (ajustado para a bacia) e o pixel de 897 m², e a fração do material erodido que de fato chega ao exutório. **Não deve ser lido como razão de entrega de sedimentos.** E_unit é, portanto, um índice relativo; o total da bacia é ancorado na medição, e o valor de um pixel isolado deve ser lido como contribuição relativa.

### 4.6 Variante com volume restrito

Para separar o erro da estrutura espacial do erro de entrada hidrológica, Q de cada evento foi reescalado por um fator único *f = V_med / V_calc*, de modo que o volume total sobre os pixels válidos iguale `T_R_m3`, limitando Q à lâmina de chuva do pixel (0,48% dos pixels); pr, E_unit e *c* foram recalculados (Baert et al., 2026, usam volume observado como entrada de referência). O padrão espacial do SCS-CN é preservado; só o total é restringido. Esta variante **não é previsão**: usa o volume medido. [PENDENTE: como `T_R_m3` inclui vazão de base, *f* reescala Q para um alvo que contém vazão de base; ver 3.2 e 5.1.]

### 4.7 Validação da vazão de pico (Fase 1)

A vazão de pico foi validada à parte: o hietograma horário de bacia (média ponderada dos postos) foi convertido em chuva efetiva pelo SCS-CN com S médio da bacia (255,7 mm) e convolvido com o hidrograma unitário triangular do SCS (D = 1 h), com Tc de Giandotti = 10,652 h, Tp = D/2 + 0,6·Tc = 6,89 h, Tb = 2,67·Tp = 18,40 h e fator de pico 2,08 × 0,5377 = 1,118 (reduzido de 2,08 por calibração nos 17 eventos). Esse fator reduz o volume do triângulo a ~54% do volume unitário, de modo que ele deve ser lido como fator empírico de escala. **O Qp não alimenta o mapa de sedimentos**; é uma validação da hidrologia da bacia.

### 4.8 Conectividade (implementada e descartada)

A etapa de conectividade de Hao et al. (2022) (FCI, direção de fluxo D8 do MDE corrigido, e DSC, sigmoide com dois parâmetros FCI₀ e k) foi integralmente implementada e calibrada. Em nenhuma configuração testada superou a escala linear constante (por exemplo, NSE 0,21 contra 0,37 com a Eq. 8 exata). Por isso o modelo adotado é SY = c · E_unit. O resultado é reportado em 5.5.

### 4.9 Métricas

NSE, WIA, PBIAS (sinal adotado: Σ(Sim − Obs)/ΣObs × 100; negativo = subestimativa, oposto ao uso comum em hidrologia), erro percentual por evento e validação cruzada *leave-one-out* (o *c* de cada evento é recalculado sem esse evento). As métricas in-sample e *leave-one-out* são reportadas separadamente.

---

## 5. RESULTADOS E DISCUSSÃO

> **[PENDENTE]** Os números desta seção vêm das notas de 21/09 e 02/10/2026. Devem ser revistos depois (i) da revisão independente em andamento, (ii) da conferência do evento 11 e (iii) da decisão sobre o volume observado (3.2).

### 5.1 Escoamento e vazão de pico

| Grandeza | Erro médio | Erro absoluto médio |
|---|---|---|
| Volume total (SCS-CN, AMC I, λ = 0,05) vs. `T_R_m3` | +0,5% | 47,4% |
| Vazão de pico (convolução HU-SCS) vs. `Q_pico` | −38,4% | 46,0% |

> **[PENDENTE — crítico]** O erro de +0,5% é contra o volume **total** (com vazão de base). Contra o escoamento direto (`T_R_m3` − Σ Bt·3600) o mesmo cálculo tem erro médio de +92%, e o NSE do volume passa de 0,18 (total) para −6,1 (direto). Ou seja, CN seco e λ baixo podem estar compensando a vazão de base que o SCS-CN não modela. Opções: (a) manter o volume total como alvo e declarar essa limitação; (b) recalibrar CN/λ contra o escoamento direto. Decidir com o orientador.

### 5.2 Produção de sedimentos no exutório

| Métrica | Previsão pura (Q do SCS-CN) | Volume restrito |
|---|---|---|
| c | 0,109049 | 0,140844 |
| NSE (in-sample) | 0,371 | 0,805 |
| NSE (*leave-one-out*) | 0,282 | 0,776 |
| WIA (in-sample) | 0,868 | 0,946 |
| PBIAS | −21,3% | −1,0% |
| Erro absoluto médio (LOO) | 46,1% | 27,8% |

{{TABELA_SY}}

A carga de sedimentos observada média por evento é de {{SY_MEDIA}} t (mín. {{SY_MIN}} t; máx. {{SY_MAX}} t).

### 5.3 De onde vem o erro

Mantendo tudo constante, exceto a qualidade da entrada hidrológica, o NSE (*leave-one-out*) vai de 0,28 (Q do SCS-CN) a 0,78 (volume observado): o erro do modelo espacializado vem sobretudo da hidrologia, não da estrutura espacial. A formulação concentrada tem desempenho parecido com os mesmos graus de liberdade (NSE 0,85 com volume e pico medidos, in-sample; 0,44 com os do modelo), logo a espacialização produz o mapa sem perda de acurácia agregada.

Tentativas de melhorar o volume sem usar dado observado não tiveram sucesso: λ ótimo por evento (5 eventos inatingíveis, 55–85% de subestimativa), λ em função da lâmina de chuva (piora na validação cruzada), classificação AMC padrão por chuva antecedente (NSE do volume −2,97).

### 5.4 Mapas e áreas críticas

O mapa médio dos 17 eventos (`SY_medio_eventos.tif`) apresenta *hot spots* concentrados em usos de maior C (C médio 0,247 nos 5% superiores, contra 0,050 na bacia) e maior declividade (LS 0,791 contra 0,537). O padrão espacial é robusto à correção do volume (r = 0,994; 96,9% de coincidência dos *hot spots*), mas isso é em grande parte garantido pela construção (f uniforme por evento), e as correlações SY × C (0,70) e SY × LS (0,19) refletem a própria fórmula: são consistência interna, **não** validação espacial independente. [PENDENTE: figuras dos mapas (evento 11 e média) e análise por classe de uso/solo.]

### 5.5 Conectividade

[PENDENTE: resumir 4.8 com tabela de configurações testadas, NSE 0,21–0,37 e a hipótese de escala (bacias de Hao: 1.310–8.973 km²; Jundiaí: 137,8 km²), declarada como não testada.]

### 5.6 Conferência detalhada de um evento (evento 11)

[PENDENTE: pacote `Evento11_Auditoria/`: planilhas com fórmulas, shapefiles e rasters; resumir como Apêndice A.] No evento 11 (04–08/07/2019; 74,0 mm; Q_pico 20,95 m³/s; 2,44 milhões de m³; SY_obs 1.821,75 t), a previsão pura simula 750,5 t (−58,8%) e a variante restrita 1.216,1 t (−33,2%).

---

## 6. LIMITAÇÕES

a) **O volume restrito não é previsão pura** (NSE 0,78 depende do volume medido; o valor honesto para bacia não monitorada é 0,28).
b) **E_unit é índice relativo**, não tonelagem por pixel; *c* absorve escala e entrega de sedimentos.
c) **Chuva de apenas dois postos**, um deles fora da bacia; o padrão espacial é dominado pelos fatores estáticos (K, C, LS).
d) **Sem validação espacial**: só há medição no exutório.
e) **Volume observado com vazão de base** (3.2 e 5.1).
f) RI é o máximo entre os dois postos e R é a lâmina ponderada, então RI/R passa de 1/h nos eventos 1 e 12 (fisicamente impossível para um posto só).
g) 17 eventos e 1 parâmetro calibrado: métricas in-sample são otimistas; usar *leave-one-out*.
h) A origem dos valores de CN ainda precisa ser documentada [PENDENTE].

---

## 7. CONCLUSÕES

[PENDENTE: escrever depois de fechar a seção 5 e a decisão do volume.]

---

## REFERÊNCIAS

Presentes nos PDFs do projeto (dados já conferidos):

BAERT, P.; et al. A regime-based framework for linking runoff initiation and event-scale sediment export in a small temperate agricultural loess catchment. **Catena**, v. 274, art. 110497, 2026. DOI: 10.1016/j.catena.2026.110497.

BORSELLI, L.; CASSI, P.; TORRI, D. Prolegomena to sediment and flow connectivity in the landscape: A GIS and field numerical assessment. **Catena**, v. 75, n. 3, p. 268-277, 2008. DOI: 10.1016/j.catena.2008.07.006.

BRANDÃO, A. R. A.; et al. Toward a better understanding of curve number and initial abstraction ratio values from a large sample of watersheds perspective. **Journal of Hydrology**, v. 655, art. 132941, 2025. DOI: 10.1016/j.jhydrol.2025.132941.

HAO, R.; et al. Incorporating sediment connectivity index into MUSLE model to explore soil erosion and sediment yield relationships at event scale. **Journal of Hydrology**, v. 614, art. 128579, 2022. DOI: 10.1016/j.jhydrol.2022.128579.

VALLE JUNIOR, L. C. G.; RODRIGUES, D. B. B.; OLIVEIRA, P. T. S. Initial abstraction ratio and Curve Number estimation using rainfall and runoff data from a tropical watershed. **RBRH**, Porto Alegre, v. 24, e5, 2019. DOI: 10.1590/2318-0331.241920170199.

VIVARELLI, M.; et al. Aplicação da equação universal de perda de solo modificada e calibração com dados de campo em uma bacia hidrográfica antropizada. Artigo (Iniciação Científica) — Universidade Estadual de Campinas, Campinas, 2025.

WILLIAMS, J. R. Sediment-yield prediction with universal equation using runoff energy factor. In: **Present and prospective technology for predicting sediment yield and sources**. ARS-S-40. Washington, DC: USDA, 1975. p. 244-252.

Citadas neste rascunho e **[conferir]** (dados bibliográficos completos antes da entrega):

CHOW, V. T.; MAIDMENT, D. R.; MAYS, L. W. **Applied hydrology**. New York: McGraw-Hill, 1988.

CONSÓRCIO PROFILL-RHAMA. **Plano de Bacias** [conferir título e órgão contratante], 2020.

MOORE, I. D.; GRAYSON, R. B.; LADSON, A. R. Digital terrain modelling: a review of hydrological, geomorphological, and biological applications. **Hydrological Processes**, v. 5, n. 1, p. 3-30, 1991. [conferir se é esta a obra citada na IC]

MURILLO-BERMÚDEZ, et al. (2021). [completar a referência conforme a IC]

NASH, J. E.; SUTCLIFFE, J. V. River flow forecasting through conceptual models part I: a discussion of principles. **Journal of Hydrology**, v. 10, n. 3, p. 282-290, 1970.

USDA-SCS. **National Engineering Handbook, Section 4: Hydrology**. Washington, DC: USDA Soil Conservation Service, 1972.

WILLMOTT, C. J. On the validation of models. **Physical Geography**, v. 2, n. 2, p. 184-194, 1981.

WISCHMEIER, W. H.; SMITH, D. D. **Predicting rainfall erosion losses: a guide to conservation planning**. Agriculture Handbook n. 537. Washington, DC: USDA, 1978.

---

## APÊNDICE A — Conferência do evento 11

[PENDENTE: preencher com o relatório da auditoria do evento 11 (cadeia completa, com as fórmulas e as planilhas).]
