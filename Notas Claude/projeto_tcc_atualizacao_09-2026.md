# Sugestão de atualização — Projeto TCC (seções 5 e 6)

Preparado em 14/09/2026 pra envio no mesmo dia. Texto pronto pra colar no documento original
(`Projeto TCC.pdf`), substituindo o item 2 da seção 5 (Metodologia) e a tabela da seção 6
(Cronograma). Baseado no que de fato foi feito até agora (ver
[README.md](../README.md), [notas_qgis_calibracao_qp.md](notas_qgis_calibracao_qp.md) e
[notas_musle_espacializada.md](notas_musle_espacializada.md) pros detalhes completos).

---

## 5. METODOLOGIA — texto sugerido para o item 2 (substitui o parágrafo atual)

**Texto original (pra referência, será substituído):**

> 2. Modelagem Hidrológica Espacializada: O volume de escoamento superficial (fator D ou Q da
> MUSLE) será espacializado utilizando o método SCS-CN (Soil Conservation Service - Curve
> Number). O fator CN será mapeado com base na intersecção do mapa de uso do solo com o mapa
> pedológico, permitindo gerar um raster do volume de escoamento em m³. Para a vazão de pico
> (qp), será feita uma ponderação baseada em um mapa raster de tempo de chegada (tempo de
> concentração/propagação), distribuindo o valor da vazão de pico observada de acordo com as
> características morfométricas de cada pixel (HAO et al., 2022).

**Texto sugerido (atualizado com o método efetivamente aplicado):**

> 2. Modelagem Hidrológica Espacializada: O volume de escoamento superficial (fator D ou Q da
> MUSLE) foi espacializado utilizando o método SCS-CN (Soil Conservation Service - Curve Number),
> com o fator CN mapeado a partir da intersecção do mapa de uso do solo com o mapa pedológico. A
> condição de umidade antecedente do solo (AMC I, cenário seco) e a razão de abstração inicial
> foram recalibradas de λ=0,2 (padrão) para λ=0,05 a partir do ajuste aos 17 eventos observados,
> abordagem consistente com estudos recentes de grande amostra (BRANDÃO et al., 2025). A área de
> contribuição foi também corrigida a partir do reprocessamento do Modelo Digital de Elevação
> (MDE), identificando e corrigindo uma barreira de drenagem não capturada originalmente (aterro
> de estrada com passagem de água/bueiro), o que elevou a área de drenagem calculada de 109,79
> km² para 137,80 km², valor consistente com a delimitação da bacia em campo.
>
> Para a vazão de pico (qp), foi adotada a metodologia de dois estágios de Hao et al. (2022):
> primeiro, calcula-se uma vazão de pico local por pixel (pr), obtida a partir do volume de
> escoamento do próprio pixel ponderado pela razão entre a intensidade máxima de chuva e a lâmina
> total do evento — sem necessidade de roteamento hidráulico. A partir de pr, calcula-se a erosão
> local por pixel (E_unit) aplicando a formulação de Williams (1975) célula a célula, com os
> fatores K, C, P e LS espacializados. Em seguida, calcula-se um Índice de Conectividade de
> Sedimentos (FCI), baseado no arcabouço de Borselli et al. (2008) e adaptado por Hao et al.
> (2022), que pondera a contribuição de cada pixel para a exutória em função da distância de fluxo
> a montante (upslope) e da resistência ao escoamento ao longo do caminho de fluxo a jusante
> (downslope), determinados a partir da direção de fluxo D8 derivada do MDE corrigido. O FCI é
> normalizado em um índice de entrega de sedimentos (DSC, 0 a 1) por meio de uma função sigmoide
> calibrada contra os dados medidos, permitindo calcular o rendimento de sedimentos por pixel como
> SY = E_unit × DSC.
>
> Como etapa adicional de rigor metodológico, os componentes hidrológicos D e qp foram calibrados
> e validados individualmente contra os dados observados dos 17 eventos antes da aplicação da
> MUSLE espacializada completa, obtendo erro médio de +0,5% (absoluto 47,4%) para o volume de
> escoamento e -38,4% (absoluto 46,0%) para a vazão de pico — magnitudes de erro consistentes com
> as encontradas na literatura recente para modelos hidrossedimentológicos distribuídos aplicados
> a bacias de porte semelhante (BAERT et al., 2026).

*(Opcional: também acrescentar Borselli et al. 2008 e Baert et al. 2026 nas referências da seção
7, caso queira citá-los no texto acima — ver detalhes bibliográficos completos nas notas.)*

---

## 6. CRONOGRAMA — tabela atualizada

A tabela original (Maio–Novembro) não reflete mais o calendário real: a entrega final do TCC
precisa ocorrer em ~6 semanas a partir de 12/09/2026, ou seja, até aproximadamente **24/10/2026**.
Sugestão de tabela revisada, mantendo as etapas já cumpridas como referência histórica e
detalhando as semanas restantes:

| Tarefa | Status / Período |
|---|---|
| Revisão Bibliográfica | ✅ Concluída |
| Espacialização dos fatores D e qp (calibração SCS-CN, HU-SCS, correção do MDE) | ✅ Concluída |
| Entrega TFC I | ✅ Concluída |
| Processamento e automatização (E_unit, FCI — Hao et al. 2022) | 🔄 Em andamento (14–21/09) |
| Normalização DSC e cálculo de SY_sim por evento | 22–26/09 |
| Validação de resultados e ajustes (calibração FCI₀/k_FCI, métricas NSE/WIA/PBIAS) | 27/09–05/10 |
| Mapas finais de produção de sedimentos (hot spots erosivos) | 06–12/10 |
| Simulação de cenários de gestão (alteração de C/P — bioengenharia e engenharia civil) | 13–19/10 |
| Redação final, revisão e Entrega TFC II | 20–24/10 |

*(Se preferir manter o formato de tabela Gantt mês-a-mês do original, dá pra adaptar essa mesma
sequência em semanas de Setembro/Outubro em vez de meses — me avisa se quiser nesse formato.)*

---

## Referências adicionadas (formato ABNT — seguindo o padrão já usado na seção 7 do projeto)

> BRANDÃO, A. R. A.; et al. Toward a better understanding of curve number and initial abstraction
> ratio values from a large sample of watersheds perspective. **Journal of Hydrology**, v. 655,
> art. 132941, 2025. DOI: 10.1016/j.jhydrol.2025.132941. Disponível em:
> https://doi.org/10.1016/j.jhydrol.2025.132941.

> BAERT, P.; et al. A regime-based framework for linking runoff initiation and event-scale
> sediment export in a small temperate agricultural loess catchment. **Catena**, v. 274, art.
> 110497, 2026. DOI: 10.1016/j.catena.2026.110497. Disponível em:
> https://doi.org/10.1016/j.catena.2026.110497.

> BORSELLI, L.; CASSI, P.; TORRI, D. Prolegomena to sediment and flow connectivity in the
> landscape: A GIS and field numerical assessment. **Catena**, v. 75, n. 3, p. 268-277, 2008. DOI:
> 10.1016/j.catena.2008.07.006. Disponível em: https://doi.org/10.1016/j.catena.2008.07.006.
> *(citação opcional — só necessária se decidir mencionar o arcabouço geral do Índice de
> Conectividade (IC) de Borselli, do qual o FCI de Hao et al. deriva.)*

Nomes completos dos autores (caso prefira grafar por extenso em vez de "et al."):

- Brandão et al. (2025): Abderraman R. Amorim Brandão, Dimaghi Schwamback, André Simões Ballarin,
  John J. Ramirez-Avila, José Goes Vasconcelos Neto, Paulo Tarso S. Oliveira.
- Baert et al. (2026): Pierre Baert, Matthieu Herpoel, Jeroen Meersmans, Charles Bielders, Aurore
  Degré.

---

## Glossário de siglas não explicadas no texto

Siglas que aparecem no texto atualizado da seção 5 e não estavam explicadas por extenso:

| Sigla | Nome completo (original) | Tradução / significado |
|---|---|---|
| **AMC** | Antecedent Moisture Condition | Condição de Umidade Antecedente (do solo) — classificação SCS-CN do quanto o solo já está úmido antes do evento de chuva (I=seco, II=médio, III=úmido); usamos AMC I (cenário seco), consistente com a calibração via CN-1. |
| **D8** | *(não é sigla — nome do método "eight-direction")* | Algoritmo de direção de fluxo que atribui, para cada célula do MDE, o escoamento inteiramente para 1 das 8 células vizinhas (a de maior declive), usado aqui pra determinar os caminhos de fluxo a montante/jusante no cálculo do FCI. |
| **FCI** | Functional Connectivity Index | Índice de Conectividade Funcional — mede o quanto cada célula está conectada (capaz de entregar sedimento) até a exutória da bacia, combinando a distância/resistência do caminho de fluxo a montante e a jusante (Hao et al., 2022, adaptado de Borselli et al., 2008). |
| **DSC** | Degree of Sediment Connectivity | Grau de Conectividade de Sedimentos — normalização do FCI numa escala de 0 a 1 (via função sigmoide), interpretada como a probabilidade de o sedimento erodido numa célula efetivamente chegar até a exutória. |

Outras siglas usadas no projeto/TCC de forma mais ampla (não aparecem no trecho atualizado, mas
podem aparecer em outras partes do texto ou seriam úteis num glossário do TCC):

| Sigla | Nome completo (original) | Tradução / significado |
|---|---|---|
| **MUSLE** | Modified Universal Soil Loss Equation | Equação Universal de Perda de Solo Modificada — já é o próprio título do TCC, mas fica registrado. |
| **SCS-CN** (ou NRCS-CN) | (Natural Resources) Soil Conservation Service – Curve Number | Método do Número de Curva do Serviço de Conservação do Solo (EUA) — estima o volume de escoamento superficial a partir da chuva e do tipo de solo/uso do solo. |
| **CN** | Curve Number | Número de Curva — parâmetro adimensional (0–100) do método SCS-CN que representa o potencial de escoamento de uma célula/bacia. |
| **HU-SCS** | *(SCS Unit Hydrograph)* | Hidrograma Unitário do SCS — método usado pra transformar a chuva efetiva incremental em vazão ao longo do tempo (usado na calibração de qp, Fase 1). |
| **IC** | Index of Connectivity | Índice de Conectividade — versão genérica original de Borselli et al. (2008), da qual o FCI (específico da MUSLE) é uma adaptação. |
| **NSE** | Nash–Sutcliffe Efficiency | Coeficiente de Eficiência de Nash-Sutcliffe — métrica de desempenho de modelos hidrológicos (1 = perfeito; pode ser negativo). |
| **WIA** | Willmott's Index of Agreement | Índice de Concordância de Willmott (Willmott, 1981) — outra métrica de desempenho de modelo, entre 0 e 1. |
| **PBIAS** | Percent Bias | Viés Percentual — mede a tendência média do modelo superestimar (+) ou subestimar (−) os valores observados. |
| **MDE** | *(português)* Modelo Digital de Elevação | Já em português — raster de altitude do terreno, base para o cálculo de direção de fluxo, declividade e área de contribuição. |
