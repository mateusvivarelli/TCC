# Dados da área de estudo — extraídos do Plano de Bacias PCJ

Consulta feita em 16/10/2026 ao arquivo `RELAT_FINAL_E_ANEXOS.pdf` (1.342 páginas, ~183 MB),
para resolver as pendências de clima, geologia e população do capítulo de área de estudo.
**Objetivo deste arquivo:** não precisar reabrir o PDF depois. As páginas indicadas são as do
PDF, conferidas na extração.

## 1. A fonte

> CONSÓRCIO PROFILL-RHAMA. **Plano de Recursos Hídricos das Bacias Hidrográficas dos Rios
> Piracicaba, Capivari e Jundiaí, 2020 a 2035**: Relatório Final. Piracicaba: Comitês PCJ;
> Fundação Agência das Bacias PCJ, set. 2020.

- Autor-entidade: Consórcio Profill-Rhama (Profill Engenharia e Ambiente S.A. + Rhama
  Consultoria, Pesquisa e Treinamento)
- Publicação: Piracicaba/SP, setembro de 2020
- Aprovado pela Deliberação dos Comitês PCJ nº 332/2020

⚠️ **Divergência de paginação:** a referência da IC diz "712 p."; o arquivo completo
(relatório + anexos) tem **1.342 páginas**. Conferir qual versão está sendo citada antes de
fechar a lista de referências.

## 2. Clima (seção 3.1.5, p. 117–119 do PDF)

**Classificação de Köppen**, segundo Alvares et al. (2013), adaptada na Figura 3.6 (p. 119).
As Bacias PCJ são de clima subtropical úmido (C), repartido em quatro faixas:

| Tipo | % da área PCJ | Descrição | Onde |
|---|---|---|---|
| Cfa | 41% | sem estação seca (mês mais seco > 40 mm), verão quente (≥ 22 °C) | faixa sul das Bacias |
| Cfb | 36% | sem estação seca, verão ameno (< 22 °C) | porção central até as nascentes |
| Cwa | 19% | inverno seco (mês mais seco < 40 mm), verão quente | Corumbataí, norte da Piracicaba, oeste da Jaguari |
| Cwb | 4% | inverno seco, verão ameno | áreas mais altas, extremos leste e oeste |

⚠️ **O Plano não atribui uma classe específica ao Alto Jundiaí.** Pela posição (faixa sul) e
altitude (725–1.315 m), deve ser Cfa nas cotas baixas e Cfb nas altas — mas isso **precisa ser
lido no mapa da Figura 3.6** antes de ser afirmado no texto.

**Precipitação e temperatura:**

- Precipitação média anual nos municípios das Bacias PCJ: **1.195 a 1.609 mm** (p. 117)
- Chuvas concentradas de **outubro a março**; médias bem menores de abril a setembro
- Temperaturas mais altas de outubro a abril; mais baixas de maio a agosto
- Maiores precipitações no extremo leste (Serra da Mantiqueira); **menores na porção centro-sul,
  com destaque para os municípios a jusante das sub-bacias Capivari e Jundiaí** — ou seja, o
  **alto** Jundiaí (nossa área) está na porção mais chuvosa da sub-bacia
- Fonte primária: CEPAGRI (2017), normais climatológicas de 1961–1990
- **Jundiaí é um dos quatro municípios da Figura 3.3** (normais mensais de temperatura e
  precipitação), junto com Pedra Bela, Rio Claro e Santa Maria da Serra

## 3. Geologia (seção 3.1.1, Quadro 3.2, p. 103 do PDF)

O Quadro 3.2 traz a composição litológica **por sub-bacia**. Coluna do Jundiaí:

| Unidade geológica | Sub-bacia Jundiaí |
|---|---|
| **Cristalino Pré-Cambriano** | **86,06%** |
| Cenozóico | 9,90% |
| Grupo Tubarão | 4,08% |
| Serra Geral (basalto) | 0,00% |
| Guarani (SAG) | 0,00% |
| Passa Dois | 0,00% |

- Litologia do embasamento cristalino: granitoides ígneos a metamórficos, xistos e rochas
  metassedimentares; **aquífero do tipo fraturado**
- Texto do Plano (p. 103): as sub-bacias Atibaia, Camanducaia, Jaguari e Jundiaí têm cobertura
  de embasamento cristalino **maior que 70%**, "que confere respostas hidrológicas e
  hidrogeológicas análogas"
- Fonte: Mapa Geológico do Estado de São Paulo (DAEE; IPT; IG, 2005) e Mapa Geológico do Estado
  de Minas Gerais (CPRM, 2005)

### 3.1. Ligação com o achado da vazão de base (relevante para a discussão do TCC)

O Plano afirma que as sub-bacias com Sistema Aquífero Guarani (Corumbataí, Piracicaba) esperam
"maior regularização das vazões e **maiores contribuições de vazões de base**, geradas pelas
descargas subterrâneas". A sub-bacia do Jundiaí **não tem SAG** — é embasamento cristalino
fraturado, que armazena e regulariza menos.

Ainda assim, medimos **34–55% do volume total como vazão de base** (seção 15 de
`notas_musle_espacializada.md`). Vale um parágrafo na discussão: a contribuição de base é
expressiva mesmo num contexto geológico que, pela caracterização regional, não favoreceria isso.

## 4. População (seção 2, Quadro 2.3, p. ~55 do PDF)

- **Campo Limpo Paulista** (onde fica a seção de controle): **73.664 habitantes**, com 100% do
  município inserido nas Bacias PCJ
- Jundiaí (município): 369 mil habitantes (censo 2010), 6,4% da população das Bacias PCJ
- A **sub-bacia Jundiaí** responde por **16,55%** da população das Bacias PCJ

⚠️ **Limitação:** são totais municipais, não da área de 137,8 km² a montante da seção de
controle. Para a população do alto curso especificamente seria preciso cruzar a máscara da bacia
com a malha municipal do IBGE (passo rápido no QGIS, mas exige baixar o shapefile).

**Alternativa provavelmente melhor para um trabalho de erosão:** usar o indicador que já temos do
nosso próprio mapa de uso do solo — **14,07% da área é urbanizada**. Diz mais sobre pressão
antrópica no processo erosivo do que contagem populacional municipal.

## 5. Conferência dos números que já estavam no texto (16/10/2026)

Calculados diretamente dos dados do projeto (shapefiles e MDE corrigido), não do Plano:

| Item | Texto do rascunho | Calculado | Situação |
|---|---|---|---|
| Mata nativa | 39,6% | 39,61% | ✅ |
| Campo | 29,0% | 29,02% | ✅ |
| Área urbanizada | 14,1% | 14,07% | ✅ |
| Silvicultura | 12,7% | 12,65% | ✅ |
| Lavoura temporária | 3,9% | 3,92% | ✅ |
| Solo exposto | 0,5% | 0,46% | ✅ |
| Cambissolos Háplicos | 68,6% | 68,52% | ✅ |
| Argissolos Vermelho-Amarelos | 17,6% | 17,69% | ✅ |
| Área urbana sem classe de solo | 13,7% | 13,66% | ✅ |
| **Altitudes** | **740 a 1.320 m** | **723,5 a 1.314,1 m** (média 887) | ⚠️ ajustar para "≈725 a 1.315 m" |
| **Área** | **137,8 km²** | 138,84 km² (shapefiles) / 138,58 km² (máscara raster) | ⚠️ declarar a fonte do número |

**Classes faltando no texto** (somam 0,27%, convém nota de rodapé para fechar 100%): corpos
d'água 0,19%, mineração 0,05%, afloramento rochoso 0,03%.

**Sobre a área:** o 137,8 km² vem da acumulação de fluxo no exutório (MDE corrigido); os
shapefiles cobrem uma borda ligeiramente maior. Diferença de ~0,7%, mas o texto deve dizer de
onde veio o valor.

## 6. Correção factual importante sobre a cabeceira

O rio Jundiaí **nasce na Serra da Pedra Vermelha, em Mairiporã**, e percorre Atibaia, Campo
Limpo Paulista, Várzea Paulista, Jundiaí, Itupeva e Indaiatuba até o Tietê, em Salto. A **Serra
do Japi alimenta o ribeirão Piraí**, afluente bem a jusante da nossa área de estudo.

⚠️ **Não atribuir a cabeceira do Jundiaí à Serra do Japi** — erro fácil de cometer, já que o Japi
é o acidente geográfico mais conhecido da região.

## 7. Contraste de solos que vale mencionar

Nas Bacias PCJ como um todo, predominam Argissolos Vermelho-Amarelos (50,5%) e os Cambissolos
Háplicos representam menos de 2% da área (p. ~110 do PDF). Na **nossa** área de estudo a relação
se inverte: Cambissolos Háplicos 68,5% e Argissolos 17,7%. É coerente — o alto curso é a porção
íngreme de cabeceira, onde solos rasos e pouco desenvolvidos predominam. Bom argumento para
justificar por que a área de estudo não é representativa da média regional.

## 8. O que ficou pendente

- [ ] Ler a Figura 3.6 (p. 119) e fixar a classe de Köppen do Alto Jundiaí
- [ ] Se quiser população do alto curso: cruzar máscara da bacia com malha municipal do IBGE
- [ ] Confirmar a paginação correta da referência (712 p. vs 1.342 p.)

---

# Parte 2 — Origem dos dados hidrossedimentológicos (Murillo-Bermúdez e Martim, 2022)

Investigação de 16/10/2026, motivada pela dúvida: a separação da vazão de base (coluna `Bt`)
usou Eckhardt/Lyne-Hollick, ou isso é suposição nossa?

## 9. Resposta: é suposição nossa

Três verificações independentes:

1. **Planilha** (`Dados_finais_histereses_corrigido.xlsx`): a coluna `Bt` tem **valores colados,
   sem fórmula**. Não há aba de metadados nem anotação sobre o método. Só existem três fórmulas
   soltas, de médias (Qmédia, CSSmedio, CSSmédiobt).
2. **Artigo de 2022** (o que descreve exatamente estes 17 eventos): **nenhuma menção** a
   separação de vazão de base, escoamento de base, filtro digital, recessão, Eckhardt ou
   Lyne-Hollick. A metodologia cobre apenas estação, turbidez→CSS, seleção de eventos e
   classificação das histereses.
3. **Teste numérico**: nenhum filtro padrão reproduz a série `Bt`. Melhor caso, Lyne-Hollick
   α=0,95 com 3 passadas: NSE 0,87, mas só **1,7% das horas batem** — se fosse esse filtro,
   deveria bater praticamente 100%. Eckhardt (α de 0,90 a 0,98; BFImax de 0,5 a 0,8) fica pior
   ainda (máx. 1,4% das horas).

**Conclusão:** a procedência do `Bt` é desconhecida. Como a vazão de base virou **componente
estrutural do modelo adotado** (Q = escoamento direto + base), isso precisa ser declarado como
limitação. **Ação recomendada: perguntar diretamente ao Murillo-Bermúdez**, que é o orientador.

⚠️ **No texto do TCC:** citar Lyne e Hollick (1979) e Eckhardt (2005) como *métodos existentes na
literatura* é correto, mas **não pode dar a entender que foram usados aqui**.

**Dados da série (conferidos):** 20.838 horas com Q e Bt; BFI global = **0,658**; `Bt = Q` em 4,4%
das horas; `Bt < Q` em 95,6%; nunca `Bt > Q`.

## 10. O que o artigo de 2022 fornece (e que resolve outras pendências)

Referência:
> MURILLO-BERMÚDEZ, L. F.; MARTIM, A. L. S. S. Avaliação qualitativa do efeito de histereses
> entre vazão e concentração de sedimentos em suspensão no rio Jundiaí, SP. In: INTERNATIONAL
> WORKSHOP FOR INNOVATION IN SAFE DRINKING WATER, 2022. p. 56-60.
> DOI: 10.20396/iwisdw.n1.2022.4793.

- **Municípios da área de captação: Mairiporã, Atibaia, Jarinu e Campo Limpo Paulista**
  → resolve a pendência de população (seção 4 acima): são esses os municípios a citar.
- **Área da parte alta: 139,3 km²** (o artigo escreve "139,3 m²", erro de digitação evidente).
  Comparar com nossos 137,8 km² (acumulação de fluxo) e 138,8 km² (shapefiles).
- **Estação fluviométrica:** rede telemétrica do DAEE / SAISP (Sistema de Alerta a Inundações de
  São Paulo), dados a cada **10 minutos**, coordenadas **-23,208833 / -46,760167**.
- **Turbidez:** medida dentro da ETA da SABESP, em amostras horárias de água bruta do rio.
- **Equação de calibração turbidez → CSS:**
  $$CSS = 3{,}264 \cdot Turbidez^{0{,}7974}$$
  Amostragem para calibração com amostrador manual DH-48 e automático ISCO; CSS determinada por
  **filtração**.
- **Critério de seleção dos eventos:** vazão ≥ 10 m³/s, o que corresponde a **menos de 1,5% do
  tempo monitorado**.
- **Resultado do artigo:** predomínio de histereses em forma de oito, associadas a múltiplos picos
  de vazão conectando diferentes fontes de sedimento a montante.

## 11. Discrepância encontrada: exutório x estação

Convertendo o exutório que derivamos do MDE (X=318.980,77 / Y=7.432.307,08, SIRGAS 2000 / UTM 23S)
para coordenadas geográficas: **-23,208415 / -46,768892**. A estação do artigo está em
**-23,208833 / -46,760167**.

Distância: **894 m**, com o nosso exutório a **jusante** da estação (o rio corre para oeste).

Ou seja, a bacia delineada inclui ~894 m de rio além do ponto de medição. O efeito na área é
pequeno, mas **a rigor a bacia deveria ser delineada na estação**. Vale conferir se a máscara
(`Máscara Jundiaí.shp`, herdada da IC) foi delineada em outro ponto, e declarar isso.
