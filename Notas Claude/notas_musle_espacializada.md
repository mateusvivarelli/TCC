# Notas de trabalho — Espacialização da MUSLE

Registro da fase 2 do TCC: espacializar a MUSLE (Modified Universal Soil Loss Equation) para
identificar áreas críticas de erosão na bacia do Alto Jundiaí, seguindo o projeto de TCC
aprovado e a metodologia de Hao et al. (2022). Continuação de
[notas_qgis_calibracao_qp.md](notas_qgis_calibracao_qp.md) (calibração de Q e Qp).

## 1. Contexto e objetivo

Na Iniciação Científica (Vivarelli et al., 2025), a MUSLE foi aplicada de forma **concentrada**:
$Y = \alpha \cdot (D \cdot q_p)^\beta \cdot K \cdot LS \cdot C \cdot P$, usando um único valor de
D (volume de escoamento) e qp (vazão de pico) por evento para a bacia inteira, e K/LS/C/P como
**médias únicas** da bacia (Tabela 3 da IC: K=0,031, LS=0,536, C=0,267, P=1,0). Resultado:
α=0,277, β=0,807 (calibrados), erro médio de -4,15% (faixa -60,01% a +37,14%) nos 17 eventos.

**Objetivo do TCC:** espacializar esse cálculo — gerar um mapa de produção de sedimentos, não um
valor único por evento, para identificar "hot spots" erosivos.

> **Atualização de escopo (14/09/2026):** a simulação de cenários de conservação (alterar C/P
> localmente pra representar bioengenharia/gabiões) foi **cortada do escopo do TCC**, decisão
> consciente do usuário dado o prazo de 6 semanas. Removida do projeto atualizado (Objetivo Geral,
> Objetivos Específicos, Metodologia e Cronograma). Não é mais um item pendente — não perder tempo
> nisso nas próximas etapas.

## 2. Metodologia adotada: Hao et al. (2022)

O projeto de TCC cita especificamente Hao et al. (2022, *Journal of Hydrology* 614:128579),
"Incorporating sediment connectivity index into MUSLE model...". Consegui o PDF completo do
artigo (`1-s2.0-S0022169422011490-main.pdf`) e extraí a metodologia exata. Ela tem **duas etapas
separadas**, o que resolve os problemas conceituais discutidos antes de eu ler o artigo (ver
seção 3 abaixo para esse histórico de discussão):

### 2.1. Etapa 1 — Erosão local por unidade/pixel (E_unit)

$$E_{unit} = 11{,}8 \cdot (Q \cdot pr \cdot Area_{unit})^{0{,}56} \cdot K \cdot C \cdot P \cdot LS$$

- **α=11,8 e β=0,56 ficam FIXOS** nos valores originais de Williams (1975) — Hao et al. não
  recalibram esses dois parâmetros; a calibração acontece só na Etapa 2.
- **Q**: escoamento local (mm), via SCS-CN — já temos isso (raster `Q{n}_CN1.tif`, CN-1, λ=0,05,
  calibrado nas notas de Q/Qp).
- **pr** (chamado de "qp" no resto do nosso projeto): vazão de pico **local**, calculada de forma
  simples, **sem flow accumulation nem roteamento**:
  $$pr_{pixel} = \frac{Q_{pixel}}{1000} \cdot Area_{pixel} \cdot \frac{RI}{R_{evento}} \cdot \frac{1}{3600}$$
  onde RI é a intensidade máxima de chuva do evento (mm/h) e R_evento é a lâmina total do evento
  (mm) — uma razão escalar, igual pra todo pixel do mesmo evento. Isso é muito mais simples do
  que eu esperava inicialmente (cheguei a propor sub-bacias com Método Racional/Giandotti
  recalculado — não é necessário, ver seção 3).
- **K, C, LS, P**: rasters espaciais (ver seção 4).

### 2.2. Etapa 2 — Conectividade de sedimentos (IC → FCI → DSC)

Estima a probabilidade de o sedimento produzido em cada unidade **realmente chegar** ao
exutório (não fica retido/depositado no caminho). Parte do Índice de Conectividade genérico (IC,
Borselli et al. 2008, Eq. 5 do artigo):

$$IC_k = \log_{10}\left(\frac{D_{up,k}}{D_{dn,k}}\right) = \log_{10}\left(\frac{\bar{W}_k\bar{S}_k\sqrt{A_k}}{\sum_{i=k}^n \frac{d_i}{W_i S_i}}\right)$$

Hao et al. adaptam isso especificamente para a MUSLE (**FCI**, Eq. 7 — a versão realmente usada,
confirmada com as imagens das equações do artigo, mais precisa que minha primeira leitura do
texto extraído em PDF, que estava corrompido nessa parte):

$$FCI_k = \log_{10}\left(\frac{11{,}8\cdot(\bar{Q}\cdot\bar{pr})^{0{,}56}\cdot\bar{K}\cdot\bar{C}\cdot\bar{P}\cdot\bar{S}\cdot\sqrt{A_k}}{\sum_{i=k}^n \frac{d_i}{W_i S_i}}\right)$$

Pontos-chave (que exigiram corrigir a primeira implementação, ver seção 6):

- **Numerador (Dup específico da MUSLE)**: Q̄, p̄r, K̄, C̄, P̄, S̄ são médias **separadas**, cada
  uma sobre toda a área de contribuição do pixel (via flow accumulation) — **não** é a média do
  E_unit já calculado/combinado. A ordem importa: primeiro tira a média de Q e de pr
  separadamente, depois multiplica e eleva a 0,56.
- **Sem o fator LS** no numerador — LS só entra em E_unit, usado no denominador via $W_i$.
- **Denominador ($D_{dn}$) não muda**: soma, ao longo do fluxo D8 até o exutório, de
  $d_i/(W_i \cdot S_i)$, com $W_i = E_{unit,i}$ **local** (não média) em cada célula do caminho —
  isso é o mesmo da Eq. 6 (peso/impedância = energia erosiva local).
- **Hao et al. usam o exutório da bacia como alvo** do caminho de fluxo (não o canal mais
  próximo, como na formulação original de Borselli) — bate com o que já temos (exutório único,
  localizado e validado nas notas de Q/Qp).
- **K̄ e S̄ são fixos** (não mudam por evento, já que K e a declividade não variam); só
  **Q̄ e p̄r precisam ser recalculados por evento**.

A conectividade funcional (FCI) e sua normalização em DSC (0 a 1, sigmoide) têm **2 parâmetros
calibráveis** (FCI₀ e k_FCI), ajustados contra o sedimento medido total via otimização numérica
(o artigo usa *simulated annealing*; podemos usar `scipy.optimize`, já usado várias vezes nesta
sessão).

### 2.3. Produção de sedimentos final

$$SY_{sim} = \sum_{pixels} E_{unit} \times DSC_{unit}$$

Como $E_{unit}$ é local (sem sobreposição) e $DSC$ é uma probabilidade (não uma vazão), a soma
**não tem o problema de dupla contagem** que discutimos antes (ver seção 3) — resolvido pela
própria estrutura do método.

## 3. Histórico da discussão (por que não fizemos diferente)

Antes de ler o artigo, discutimos várias abordagens e por que cada uma tinha problema:

1. **MUSLE pixel a pixel com qp = Método Racional local** (cada pixel usa sua própria área de
   contribuição): rejeitado por dois motivos — (a) sobreposição: a área de contribuição de um
   pixel a jusante contém a de todos os pixels a montante, então somar Y por pixel contaria a
   mesma área várias vezes; (b) Método Racional só é válido em áreas pequenas (já vimos isso
   custar 1.000%+ de erro na calibração do Qp da bacia inteira) — pixels perto do exutório
   teriam área grande demais pro método.
2. **qp constante em todo pixel** (usar o Qp já calibrado da bacia inteira, igual em todo canto):
   evita os dois problemas acima, mas descarta a variação real de qp ao longo da bacia.
3. **Sub-bacias com Tc/Giandotti recalculado por sub-bacia**: mais rigoroso que Método Racional,
   mas exigia bastante trabalho extra (delimitar sub-bacias, recalcular L/Hm por sub-bacia).
4. **A solução real (Hao et al.)**: nenhuma das anteriores — pr é **local e trivial** (Q local ×
   razão de intensidade), e a variação espacial "de verdade" entra pela **conectividade** (IC),
   que é uma probabilidade relativa (0 a 1), não uma vazão — por isso não sofre nem de
   sobreposição nem do problema de escala do Método Racional.

## 4. Preparação dos dados espaciais (K, LS, C, P)

Rasters gerados, todos alinhados à grade de referência (mesma do `ChuvaIDW1.tif`: 884×365
pixels, ~30m, origem X=318646,35/Y=7435057,59, SIRGAS 2000/UTM 23S):

| Fator | Arquivo | Fonte | Média obtida | Média na Tabela 3 da IC |
|---|---|---|---|---|
| K | `Dados Iniciais/K_raster.tif` | `Pedologia Alto.shp` (campo `Valor`) | 0,039 | 0,031 |
| LS | `Dados Iniciais/LS_raster.tif` | `LS Alto.tif` (reprojetado de WGS84) | 0,536 | 0,536 (bate exato) | **DEFEITUOSO — substituído em 16/10/2026 por `LS_moore.tif` (média 7,80); ver seção 24** |
| C | `Dados Iniciais/C_raster.tif` | `Uso Solo Alto.shp` (campo `Valor`) | 0,050 | 0,267 |
| P | (constante = 1,0 em toda a bacia) | — | 1,0 | 1,0 |

**Nota sobre os shapefiles:** `Pedologia Alto.shp` e `Uso Solo Alto.shp` vieram inicialmente sem
`.dbf` (tabela de atributos) — precisei pedir esse arquivo separadamente. Também vieram sem
`.prj`; assumi SIRGAS 2000/UTM 23S (EPSG:31983) com confiança alta, já que a extensão das
geometrias bate exatamente com a da `Máscara Jundiaí.shp` (já confirmada nessa projeção).

**Divergência do fator C, investigada e resolvida:** a média ponderada por área real (calculada
a partir da geometria, não do campo de atributo `Area_km2` que estava desatualizado/errado)
deu C≈0,05 — bem abaixo dos 0,267 da Tabela 3. Investigando a distribuição de classes por área
geométrica real:

| Classe de uso do solo | Área (km²) | Valor de C |
|---|---|---|
| Mata Nativa | 55,0 | 0,015 |
| Campo | 40,3 | 0,05 |
| Área Urbanizada | 19,5 | 0,0 |
| Silvicultura | 17,6 | 0,121 |
| Lavoura Temporária | 5,4 | 0,2116 |
| Solo exposto | 0,63 | 1,0 |
| Corpos D'Água | 0,26 | 0,0 |
| Mineração | 0,06 | 1,0 |
| Afloramento Rochoso | 0,05 | 1,0 |

**Confirmado com o usuário: C≈0,05 é o valor correto** — a Tabela 3 do relatório da IC
provavelmente usou uma fonte diferente (possivelmente o mapa mais genérico do Plano de Bacias
Profill-Rhama, 2020, em vez deste shapefile de uso do solo detalhado). O fator K (0,039 vs 0,031)
tem divergência pequena, dentro do esperado por diferenças de método de cálculo; o fator LS bate
exatamente (0,536), o que reforça que o processo de rasterização está correto e a divergência do
C é uma questão de fonte de dado, não erro de processamento.

## 5. pr_pixel (vazão de pico local) — calculado

Script: [Scripts/calcular_pr_pixel.py](Scripts/calcular_pr_pixel.py). Usa RI =
`Intensidade_60min_mm/h` e R_evento = `Chuva_evento_mm` (colunas já existentes na planilha de
eventos). Gera `pr{n}.tif` em cada pasta `Evento {n}`, usando o raster `Q{n}_CN1.tif` (CN-1,
λ=0,05) já calibrado.

| Evento | RI (mm/h) | R_evento (mm) | razão RI/R_evento (/h) | Σpr (m³/s, todos os pixels) |
|---|---|---|---|---|
| 1 | 23,60 | 23,36 | 1,010 | 34,61 |
| 2 | 19,00 | 57,34 | 0,331 | 107,45 |
| 3 | 53,20 | 65,43 | 0,813 | 352,41 |
| 4 | 35,20 | 36,19 | 0,973 | 114,01 |
| 5 | 36,60 | 60,91 | 0,601 | 237,93 |
| 6 | 29,40 | 34,45 | 0,853 | 97,37 |
| 7 | 15,40 | 35,52 | 0,434 | 46,90 |
| 8 | 30,60 | 82,54 | 0,371 | 260,46 |
| 9 | 23,00 | 92,94 | 0,247 | 217,33 |
| 10 | 12,60 | 25,78 | 0,489 | 24,29 |
| 11 | 11,80 | 74,04 | 0,159 | 88,47 |
| 12 | 32,80 | 23,73 | 1,382 | 70,62 |
| 13 | 36,60 | 74,88 | 0,489 | 284,00 |
| 14 | 37,40 | 82,20 | 0,455 | 322,49 |
| 15 | 47,80 | 139,42 | 0,343 | 623,14 |
| 16 | 15,80 | 97,68 | 0,162 | 157,26 |
| 17 | 43,00 | 65,64 | 0,655 | 282,90 |

Nota: essa soma de pr por pixel **não é** uma vazão de pico real da bacia (não pode ser somada
fisicamente como se fosse) — é só a soma dos valores locais, útil como checagem de ordem de
grandeza, não como validação.

## 6. Índice de Conectividade (IC) e FCI

**Atenção — correção:** a primeira versão funcional
([Scripts/calcular_ic_por_evento.py](Scripts/calcular_ic_por_evento.py)) usava a Eq. 5 genérica
do IC (Dup = W̄·S̄·√A, com W̄ = média do **E_unit já calculado/combinado**), porque o texto da
Eq. 7 extraído do PDF estava corrompido. O usuário enviou as imagens das equações 5 e 7
diretamente do artigo, revelando que a Eq. 7 (a que Hao et al. realmente usam, específica pra
MUSLE) é diferente — ver seção 2.2 acima para a fórmula exata. **Script corrigido:**
[Scripts/calcular_fci_por_evento.py](Scripts/calcular_fci_por_evento.py), que produz `FCI{n}.tif`
(não mais `IC{n}.tif`) em cada pasta de evento. Os arquivos `IC{n}.tif` da primeira versão foram
mantidos como registro do que foi tentado, mas **não devem ser usados na etapa de calibração** —
usar sempre `FCI{n}.tif`.

Script base (ainda útil como referência da lógica do IC genérico):
[Scripts/calcular_indice_conectividade.py](Scripts/calcular_indice_conectividade.py)
(versão placeholder, W=1 uniforme — mantida como registro/teste inicial).

Implementado do zero em Python (SAGA/QGIS não têm uma ferramenta pronta pra IC — por isso existe
o software separado SedInConnect, de Crema & Cavalli 2018, citado no artigo):

1. Direção de fluxo D8 calculada diretamente da elevação (maior declive entre os 8 vizinhos),
   em vez de decodificar a convenção interna do SAGA.
2. $D_{dn}$: acumula d/(W·S) ao longo do fluxo D8 até o exutório, via **propagação vetorizada em
   ondas** (não busca em largura/BFS com listas em Python puro — essa primeira versão travou,
   consumindo 500+ segundos de CPU sem terminar; a versão vetorizada com numpy processa tudo em
   menos de 2 segundos).
3. $D_{up}$: W̄ e S̄ médios por célula sobre toda a área de contribuição, via
   `sagang:catchmentarea` (parâmetro `VAL_MEAN`) — a mesma ferramenta já usada para calcular a
   altitude média da bacia (Hm) na calibração do Tc de Giandotti.
4. **Importante: o IC é recalculado por evento**, não uma vez só — porque
   $W_i = E_{unit,i}$ (Hao et al., Eq. 6) varia por evento (E_unit depende de Q e pr, que são
   específicos de cada evento). O `calcular_ic_por_evento.py` reprojeta o `E_unit{n}.tif` de cada
   evento (grade 884×365) para a grade do MDE (2722×1097), roda o SAGA pra obter W̄ e S̄
   a montante, recalcula Ddn com esse W variável, e salva `IC{n}.tif` em cada pasta `Evento {n}`.

### E_unit (erosão local) — calculado

Script: [Scripts/calcular_e_unit.py](Scripts/calcular_e_unit.py). Fórmula (Hao et al., Eq. 1,
com α=11,8 e β=0,56 fixos — não recalibrados nesta etapa):

$$E_{unit} = 11{,}8 \cdot (Q \cdot pr \cdot Area_{unit})^{0{,}56} \cdot K \cdot C \cdot P \cdot LS$$

| Evento | Soma de E_unit (t) | Evento | Soma de E_unit (t) |
|---|---|---|---|
| 1 | 842,91 | 10 | 916,94 |
| 2 | 5.580,65 | 11 | 6.881,90 |
| 3 | 13.120,27 | 12 | 1.702,20 |
| 4 | 3.151,76 | 13 | 13.851,64 |
| 5 | 10.290,75 | 14 | 16.718,94 |
| 6 | 3.165,93 | 15 | 39.972,69 |
| 7 | 1.989,17 | 16 | 13.110,52 |
| 8 | 14.634,44 | 17 | 11.307,75 |
| 9 | 14.906,42 | | |

Nota: essa soma é só a erosão potencial local somada — **ainda não é** a produção de sedimentos
final (falta multiplicar por DSC, a probabilidade de conectividade, na próxima etapa).

*(resultados do IC por evento a preencher assim que o cálculo terminar)*

## 6.1. Dados de sedimento medido (SY_obs) — já disponíveis

Não precisou digitalizar nada das figuras do relatório de IC: a planilha
`eventos_processados_manuais.xlsx` já tem a coluna **`SYY_t`** (sedimento suspenso total medido
no evento, em toneladas) = `SSY_Ris_t + SSY_Fall_t` (confirmado: soma bate exatamente, mesma
lógica de separação ascendente/descendente já usada para o volume `T_R_m3`).

| Evento | SY_obs (t) | Evento | SY_obs (t) |
|---|---|---|---|
| 1 | 266,36 | 10 | 847,32 |
| 2 | 2.039,89 | 11 | 1.821,75 |
| 3 | 927,78 | 12 | 210,70 |
| 4 | 1.379,86 | 13 | 1.196,49 |
| 5 | 1.371,70 | 14 | 1.731,23 |
| 6 | 198,56 | 15 | 3.828,83 |
| 7 | 1.316,56 | 16 | 1.736,07 |
| 8 | 2.108,50 | 17 | 1.709,56 |
| 9 | 1.154,55 | | |

Isso é o alvo (SY_obs) para calibrar FCI₀ e k_FCI (seção 7 do roadmap).

## 7. Status e próximos passos

- [x] Entendida e documentada a metodologia de Hao et al. (2022).
- [x] Rasters de K, LS, C gerados e conferidos (C confirmado com o usuário = 0,05).
- [x] pr_pixel calculado para os 17 eventos.
- [x] IC placeholder (W=1) testado e validado (< 2s por versão vetorizada).
- [x] E_unit calculado por pixel/evento (K, C, LS, Q, pr).
- [x] FCI final por evento (Eq. 7 exata, W = E_unit) — 17/17 rodados com sucesso, checagem visual
      confirmou padrão espacial coerente (baixa conectividade nas zonas de baixa declividade).
- [x] Normalizar FCI em DSC (sigmoide, Eq. 8) e calibrar FCI₀/k_FCI — **abandonado, ver seção 9**.
- [x] Validar: comparar SY_sim com SY_obs (NSE, WIA, PBIAS, erro %) — feito via o baseline (seção 9).
- [x] Mapas finais de produção de sedimentos (hot spots) — `Scripts/calcular_sy_final.py`,
      ver seção 9.
- [x] ~~Simulação de cenários (alterar C/P localmente)~~ — **cortado do escopo do TCC em
      14/09/2026** (decisão do usuário, dado o prazo de 6 semanas). Não é mais um item pendente.

## 9. Decisão final (17/09/2026): FCI/DSC abandonado, adotado baseline de escala linear

**Contexto:** retomando o trabalho pausado em 14/09 (ver README.md), a tentativa de recalibrar
FCI₀/k_FCI trocando o objetivo de log-NSE para NSE bruto **não resolveu** o problema original —
NSE continuou negativo (-0,60), pior que o baseline trivial (escala constante de E_unit,
NSE=0,37/0,65).

**Bug real encontrado e corrigido (mas que não resolveu o problema todo):** o pixel imediatamente
a montante do exutório tinha `E_unit=0` exato nos 17 eventos (é área de água/urbana, `C=0` — 14,3%
da bacia tem `C=0`). Como esse valor é usado como peso de impedância `W_i` no denominador `Ddn`
(soma de `d_i/(W_i·S_i)` ao longo do caminho de fluxo D8), e **praticamente todo caminho de fluxo
da bacia passa perto desse ponto antes de sair**, um piso de W próximo de zero (1e-6, valor
original do script) inflava o `Ddn` — e por consequência achatava o `FCI` — da bacia inteira em
dezenas de ordens de grandeza (FCI variando de -59 a -7, muito mais largo que a Tabela 4 do
artigo: FCI₀ entre -2,33 e -4,79, k_FCI entre 0,96 e 2,99 nas três bacias de Hao et al.).
Corrigido em `Scripts/calcular_fci_por_evento.py`: o piso de W passou a ser a **mediana** da
própria distribuição de E_unit do evento (não um valor arbitrário), já que testar o percentil 5
não resolveu (ainda caía dentro da cauda contaminada por pixels de água/urbano). Isso melhorou a
extremidade bem-conectada do FCI (máximo de -7 para -1,8, mais perto da escala do artigo), mas
**não resolveu a calibração — na verdade piorou** (NSE=-0,91 após a correção, contra -0,60 antes).

**Nota lateral (sem impacto direto, registrado para referência futura):** durante a investigação,
notou-se que a Eq. 6 do artigo define `W_i` **sem** o fator LS, enquanto o código usava
`E_unit` (que **inclui** LS) como `W_i`. Não foi a causa raiz (testado isoladamente: `Ddn` variou
menos de 2% removendo o LS), mas é uma divergência real em relação ao artigo que ficaria pendente
se a abordagem FCI/DSC fosse retomada no futuro.

**Hipótese não testada (falta de tempo):** a área da bacia do Alto Jundiaí (137,8 km²) é **10 a
65× menor** que as três bacias do artigo (Dali 1.310 km², Duhe 8.973 km², Xiangshui 1.749 km²).
Como o numerador do FCI (`Dup`) usa `sqrt(A_k)` e o denominador (`Ddn`) acumula ao longo de
caminhos de fluxo proporcionalmente mais curtos numa bacia pequena, é plausível que a escala
natural do índice não se transfira diretamente entre bacias de tamanhos tão diferentes sem um
ajuste adicional (ex.: normalização por área da bacia). Não foi investigado a fundo — ver seção
7/8 se decidir retomar essa linha no futuro.

**Decisão do usuário (17/09/2026):** abandonar a calibração FCI/DSC e adotar o **baseline de
escala linear constante** como resultado final da Fase 2 espacializada:

$$SY_{sim,k} = c \cdot E_{unit,k}, \quad c = 0{,}109049 \text{ (mínimos quadrados pela origem)}$$

- **NSE = 0,3714** (através da origem) contra os 17 eventos observados.
- Fisicamente, isso equivale a assumir que a fração de erosão local que efetivamente chega ao
  exutório é aproximadamente **constante entre pixels** (sem modelar a conectividade espacial
  como um fator adicional que varia por posição na bacia) — uma simplificação, mas consistente
  com o teto de precisão baixo que a literatura recente já reporta para MUSLE espacializada
  mesmo com dados de entrada observados perfeitos (Baert et al., 2026: NSE≈0,66 nesse cenário
  ideal, caindo a ~0 com entradas modeladas como as nossas).
- Isso deve ser reportado no texto do TCC como um **achado legítimo**, não como uma limitação
  escondida: a tentativa de incorporar conectividade espacial (Hao et al., 2022) foi feita e
  documentada, mas não superou uma escala linear simples nesta bacia — possivelmente por causa
  da diferença de escala espacial em relação às bacias originais do artigo (ver hipótese acima).

**Mapas finais gerados:** `Scripts/calcular_sy_final.py` — `Evento {n}/SY{n}.tif` (produção de
sedimentos por pixel, por evento) e `Dados Iniciais/SY_medio_eventos.tif` (média dos 17 eventos,
mapa principal de hot spots erosivos). Checagem física: os hot spots (top 5% da bacia) têm C
médio 0,247 (bacia: 0,050) e LS médio 0,791 (bacia: 0,537) — coerente (erosão concentrada em
áreas de uso do solo mais agressivo combinado com declividade mais alta). Correlação SY×C=0,70,
SY×LS=0,19.

**Fase 2 considerada concluída** com essa abordagem. Próximo passo é redação/figuras finais do
TCC (ver README.md).

## 10. Experimento (17/09/2026): recalibrar alfa/beta direto na fórmula por pixel

Usuário perguntou se dava pra usar o alfa/beta da própria IC (0,277/0,807) em vez dos fixos de
Williams/Hao (11,8/0,56). Resposta técnica: não dá pra simplesmente substituir — os parâmetros da
IC foram calibrados contra `D` e `qp` **agregados da bacia inteira** (um valor por evento), não
contra valores **locais por pixel**; além disso, por causa do expoente não-linear,
`Σx_k^β ≠ (Σx_k)^β`, então nem ajustando a escala o mesmo beta reproduziria o resultado agregado
aplicado pixel a pixel. Testamos mesmo assim, como experimento controlado (recalibrando alfa E
beta livremente na fórmula por pixel, via `differential_evolution` contra os 17 SY_obs — mesmo
método usado na tentativa de FCI0/kFCI). Script:
[Scripts/calibrar_alfa_beta_pixel.py](Scripts/calibrar_alfa_beta_pixel.py).

**Resultado:** alfa=4,2237, beta=0,2793 (bem diferente tanto do 11,8/0,56 de Hao quanto do
0,277/0,807 da IC — não bate com nenhuma referência física).

| Métrica | Baseline adotado (alfa/beta fixos, só escala `c`) | Este experimento (alfa/beta livres) |
|---|---|---|
| NSE | 0,3714 | **0,6121** (melhor) |
| PBIAS | — | -1,36% (bom) |
| Erro médio | -19,2% | +29,2% (pior) |
| Erro absoluto médio | 44,4% | **57,9%** (pior) |

**Por que o NSE melhora mas o erro médio piora:** NSE pesa por magnitude (eventos grandes como
13/14/15/9 dominam), enquanto erro médio trata todo evento igual. O ajuste livre acerta bem os
eventos grandes mas gera outliers extremos em eventos pequenos (evento 6: +302%, evento 12:
+154%, evento 3: +91%) — sintoma clássico de mal-condicionamento (2 parâmetros livres, só 17
observações de nível bacia, sem dado de validação por pixel). Ao contrário da tentativa de
FCI0/kFCI (que bateu no limite superior de kFCI, um sinal claro de degenerescência), aqui o
otimizador convergiu num ponto interior dos limites (`beta` entre 0,1 e 2,0, `alfa` entre 1e-6 e
1000) — ou seja, é um ótimo genuíno dos dados, só que **estatisticamente frágil e sem ancoragem
física** (beta=0,28 não corresponde a nenhuma referência da literatura de erosão).

**Decisão:** não adotado como resultado final (o baseline com alfa/beta fixos de Williams/Hao
continua sendo a escolha mais defensável cientificamente), mas vale documentar no texto do TCC
como um experimento que mostra o teto de ajuste estatístico possível, em contraste com a
abordagem fisicamente fundamentada.

## 11. Pendência para a próxima sessão (17/09/2026)

Usuário pediu para deixar anotado, sem executar agora:

1. **Testar SY_total com o "outro Qp"**: a Fase 1 (seção 3.10 de
   [notas_qgis_calibracao_qp.md](notas_qgis_calibracao_qp.md)) deixou pendente a escolha entre o
   fator de pico calibrado para **menor erro absoluto** (o atual, viés -38,4%, erro absoluto
   46,0%) ou recalibrado para **viés ~0%** (erro absoluto sobe pra ~55-65%). Gerar o `pr{n}.tif` /
   `Qp` alternativo (viés zero) e reprocessar `E_unit`, `SY` com ele.
2. **Testar SY com "minha calibração"**: gerar o mapa espacial completo (não só a comparação
   agregada da seção 10) usando alfa=4,2237/beta=0,2793 (o experimento acima) em vez dos valores
   fixos de Hao.
3. **Ver os gráficos de SY e E_unit (MUSLE) na bacia nos 4 casos** (desenho 2×2): {Qp atual, Qp
   alternativo (viés zero)} × {alfa/beta fixos de Hao, alfa/beta livres calibrados}. Isso dá 4
   combinações de mapas (SY e E_unit cada) para comparar visualmente.

Nenhum desses itens foi executado ainda — fica para quando o usuário retomar.

## 8. Artigos sugeridos pelo orientador (14/09/2026) — comparação com nosso plano

O orientador comentou ter em mente "uma forma de distribuir o valor de qp sem ter que aplicar
métodos, usando o dado observado" e indicou 4 artigos pra ajudar a "resolver a questão do Q".
Conseguimos 3 dos 4 (falta o artigo ASCE, doi/10.1061/JHYEFF.HEENG-6756). Leitura completa dos 3:

### 8.1. Brandão et al. (2025, *Journal of Hydrology*) — 3.578 bacias, validação global de λ

Estudo em grande escala (calibração de CN por mínimos quadrados, LS) comparando λ=0,2 (padrão)
vs λ=0,05 (revisado) em milhares de bacias no mundo todo.

- **Valida diretamente nossa escolha de λ=0,05**: o método LS com λ=0,05 supera λ=0,2 na maioria
  das bacias, com equações de conversão CN₀,₂→CN₀,₀₅.
- Achado extra: **o tipo de uso do solo prediz qual λ funciona melhor** — lavoura/urbano/árido
  tendem a λ=0,05; pastagem tende a λ=0,2. O Alto Jundiaí tem uso misto (mata, pastagem, lavoura,
  urbano — ver `C_raster.tif`), o que pode explicar parte do erro residual evento a evento que
  observamos mesmo após fixar λ=0,05: eventos com chuva concentrada em área de pastagem podem se
  comportar mais como λ=0,2.

### 8.2. Baert et al. (2026, *Catena*) — bacia do Chastre (Bélgica), o mais diretamente relevante

Mesmo problema que o nosso: SCS-CN + MUSLE, variabilidade de λ evento a evento, mas numa bacia
pequena e com monitoramento muito mais denso (83,84 ha, 154 eventos, dados a cada 1 min).

- **λ fixo (mesmo testando vários valores) tem desempenho ruim** — melhor NSE de volume obtido foi
  só 0,13. Confirma que o viés residual que vemos mesmo com λ=0,05 é esperado pra esse tipo de
  método, não sinal de erro nosso.
- Tentaram algo mais sofisticado: λ ótimo por evento (igual ao que já testamos em
  `_calibrar_lambda_por_evento.py`), generalizado por clusterização em regimes ou regressão
  contínua (chuva, retenção potencial, energia cinética, intensidade). Mesmo assim, fora da
  amostra: NSE = 0,21–0,40 pro volume e **-0,26 a 0,34 pro pico** — ou seja, um método bem mais
  elaborado que o nosso, com muito mais dado, ainda tem dificuldade real com o pico de vazão.
- **Achado mais importante pra calibrar expectativa**: a MUSLE, mesmo usando volume e pico
  **observados** (dado de entrada perfeito), só chega a NSE=0,66 na produção de sedimentos. Com
  entradas modeladas (situação real), cai pra perto de zero (NSE=-0,03 a 0,01). Ou seja, existe um
  teto de precisão da própria equação MUSLE, independente da qualidade da nossa estimativa de
  chuva/vazão.
- Usam hidrograma unitário **sintético** (USDA-NRCS lag, análogo ao nosso Giandotti), não um
  método baseado em dado observado puro. Na discussão, citam roteamento distribuído por
  pixel/isócronas (tipo HIDROPIXEL) como direção futura pouco explorada.
- **Sobre o comentário do orientador** ("distribuir qp sem método, usando o dado observado"):
  nenhum dos 3 artigos mostra exatamente essa técnica. O mais próximo é o teste que já fizemos
  nesta sessão (`_teste_qp_final_com_Q_medido.py`, isolando o mecanismo usando Q medido). Nossa
  abordagem (Hao et al. 2022, conectividade espacial) já vai além do que este artigo de 2026 faz
  pro pico — eles nem tentam espacializar o pico, só o volume.

### 8.3. Valle Junior et al. (2019, *RBRH*) — bacia do Guariroba (Brasil), alerta sobre solo arenoso

- Em solos muito arenosos (Neossolo Quartzarênico, alta infiltração), o **CN-SCS falhou
  completamente** (NSE negativo) porque o escoamento ali é dominado por fluxo subsuperficial, não
  pelo mecanismo de excesso de infiltração que o CN-SCS assume. Precisaram trocar pro método mais
  simples Q=C·P.
- **Verificação de adequação pra nossa bacia**: o Alto Jundiaí tem Cambissolos e Argissolos (mais
  argilosos, menos permeáveis que Neossolo arenoso — coerente com nosso `K_raster.tif`), então é
  bem mais provável que o mecanismo de infiltração-excesso do CN-SCS seja adequado ali. Vale
  mencionar essa verificação no texto do TCC como justificativa de adequação do método.

### 8.4. Síntese — o que muda no nosso plano

- **Nada muda estruturalmente**: λ=0,05 continua a escolha certa (reforçada pelo artigo 1); nossa
  abordagem espacial via Hao et al. continua mais avançada que o que a literatura recente (2026)
  usa pra vazão de pico.
- **Nível de erro esperado**: os benchmarks do artigo 2 (NSE≈0,66 mesmo com dado observado
  perfeito, caindo a ~0 com dado modelado) servem de referência pra avaliar nosso NSE final da
  MUSLE espacializada quando calibrarmos FCI₀/k_FCI — não esperar um NSE alto, isso é consistente
  com o estado da arte, não um sinal de erro metodológico.
- **A pendência real**: nenhum dos 3 artigos mostra a técnica específica que o orientador mencionou
  de cabeça ("distribuir qp sem método, usando dado observado"). Pode estar no 4º artigo (ASCE,
  ainda não obtido) ou em algo que ele vai esclarecer separadamente ("vou tentar ver amanhã").
- Ação recomendada: seguir rodando o FCI (Hao et al.) como planejado; se o orientador confirmar
  amanhã uma técnica de distribuição por dado observado, avaliar se é complementar (ex.: usar
  como cross-check do pr_pixel) ou alternativa ao que já foi feito.

## 12. Diagnóstico de fontes de erro (21/09/2026) — onde o erro realmente está

Antes de partir pra redação, foi feita uma decomposição do erro do modelo adotado
(`SY = c·E_unit`, NSE=0,37). Scripts: `Scripts/_diagnostico_limites_modelo.py`,
`_diagnostico_parte2.py`, `_diagnostico_parte3_lambda_variavel.py`, `_diagnostico_parte4_amc.py`.
**Todos são diagnósticos, não resultado final.**

### 12.1. Métricas honestas (leave-one-out)

O NSE=0,3714 é **in-sample** (o `c` foi ajustado nos mesmos 17 eventos). Em validação cruzada
leave-one-out (metodologia do próprio Hao et al., seção 3.3), o valor honesto é **NSE=0,2816**
(erro absoluto médio 46,1%). É esse par que deve ser reportado no TCC.

### 12.2. O achado central: o erro é hidrológico, não do modelo de erosão

Reescalando o Q de cada evento para bater o volume **medido** (`T_R_m3`) — o que equivale a
multiplicar Σ E_unit por f^1,12, já que E_unit ∝ Q^1,12 na nossa formulação:

| Configuração | NSE (in-sample) | NSE (leave-one-out) | erro abs. médio |
|---|---|---|---|
| Q do modelo CN-SCS (atual) | 0,3714 | 0,2816 | 46,1% |
| **Q com volume medido** | **0,8009** | **0,7703** | **28,2%** |
| MUSLE concentrada, D e qp medidos (só escala calibrada) | 0,8476 | — | 28,6% |
| MUSLE concentrada, D e qp do modelo | 0,4412 | — | 44,5% |

**Interpretação:** a estrutura espacial (E_unit + fatores K/C/LS) está correta — com hidrologia
boa ela atinge NSE 0,77-0,80, acima do teto de 0,66 que Baert et al. (2026) reportam para MUSLE
com entradas observadas. Todo o déficit vem do volume de escoamento da Fase 1 (erro abs. 47%).
A espacialização não degrada o desempenho agregado (0,37 espacial vs 0,44 concentrada, mesma
qualidade de entrada) — ou seja, ela entrega o mapa "de graça".

### 12.3. Tentativas de melhorar o volume — todas falharam (com evidência)

| Tentativa | Resultado | Conclusão |
|---|---|---|
| λ ótimo por evento | **5 dos 17 eventos são impossíveis**: nem com λ→0 o CN-1 gera escoamento suficiente (eventos 1, 2, 4, 7, 10, todos com subestimação de 55-85%) | não é problema de λ, é do próprio CN (S alto demais) |
| λ(chuva) = a·P^b, com LOO | volume melhora pouco (NSE_vol 0,21→0,34), mas SY **piora** em LOO (0,273→0,258) | sobreajuste com 17 pontos |
| Classificação AMC por P5 (limiares clássicos do SCS) | **piora muito** (NSE_vol -2,97; NSE_SY -0,70) — concorda com o melhor cenário em 12/17, mas os 5 erros são catastróficos (eventos 14 e 16 saltam para +292% e +176%) | a classificação padrão de umidade antecedente não funciona nesta bacia |
| Oráculo de cenário (escolher CN-1/2/3 sabendo a resposta) | NSE_vol 0,47, NSE_SY 0,63 | teto do que a escolha de cenário poderia dar — e não é realizável |

Isso reproduz de forma independente o achado central de Baert et al. (2026) (nenhuma
generalização de λ atinge bom desempenho fora da amostra) e ecoa Valle Junior et al. (2019)
(CN-SCS estruturalmente inadequado em certas bacias brasileiras). **É um resultado do TCC, não
uma falha** — mas significa que não há ganho barato restante pelo lado do CN-SCS.

### 12.4. A pendência da seção 11 é inócua (não executar)

- **Item 1 ("outro Qp", fator de pico com viés zero): não muda nada, por dois motivos
  independentes.** (a) O `pr_pixel` da Fase 2 **não usa** o Qp da Fase 1 — ele é calculado só a
  partir de `Q{n}_CN1.tif` e da razão `Intensidade_60min / Chuva_evento` da planilha (ver
  `calcular_pr_pixel.py`); o HU-SCS da Fase 1 não entra no pipeline espacial. (b) Mesmo que
  entrasse: `FATOR_PICO` é um escalar global, então pr escalaria por k em todos os eventos,
  Σ E_unit por k^0,56, e o `c` recalibrado absorveria isso **exatamente** — NSE, PBIAS e os mapas
  seriam idênticos.
- **Itens 2 e 3 (mapas com α/β livres, grade 2×2):** só o β muda o padrão espacial. E o
  diagnóstico mostra que baixar o β é um curativo estatístico para o viés do volume: com β=0,2793
  o erro absoluto piora de 46% para 66% (LOO), e com o volume corrigido o β=0,56 original funciona
  bem (NSE 0,80). Gerar os mapas só se for para figura ilustrativa de sensibilidade.

### 12.5. Recomendação

Usar o **volume medido como restrição** do raster de Q (reescalar `Q{n}_CN1.tif` por evento para
que o total bata `T_R_m3`), mantendo o padrão espacial do CN-SCS + interpolação de chuva. Isso
leva o NSE de 0,28 para 0,77 (LOO) e é metodologicamente defensável — Baert et al. (2026) usam
exatamente essa configuração (volume e pico observados como entrada da MUSLE) como caso de
referência. Deve ser descrito com transparência como "volume observado usado como restrição", não
como previsão pura, e o TCC pode apresentar os dois mapas (previsão pura × restrito pelo
observado) — a comparação entre eles **é** um resultado, pois quantifica quanto do erro vem da
hidrologia.

### 12.6. Correção necessária no texto do TCC

A seção 5 do projeto (e o texto futuro) não pode dar a entender que a calibração de Qp da Fase 1
(HU-SCS, Tc de Giandotti, fator de pico) alimenta o mapa — ela **não alimenta**. Ela é uma
**validação do modelo hidrológico** da bacia; o `pr` usado na MUSLE espacializada é o local de
Hao et al. (Q do pixel × razão de intensidade). Isso precisa estar claro para não parecer erro
metodológico.

## 13. Versão com volume observado como restrição (21/09/2026) — implementada

Implementação da recomendação da seção 12.5. Script:
[Scripts/calcular_sy_volume_restrito.py](Scripts/calcular_sy_volume_restrito.py).

**O que faz:** reescala `Q{n}_CN1.tif` por um fator único por evento, de modo que o volume total
da bacia bata exatamente o `T_R_m3` medido. O **padrão espacial** do CN-SCS (que vem do CN e da
chuva interpolada) é preservado — só o total é restringido pela medição. Depois refaz `pr`,
`E_unit` e `SY` a partir desse Q. Saídas com sufixo `_obs`, sem sobrescrever os resultados
anteriores.

### Resultados

| Métrica | Previsão pura (atual) | **Volume restrito** |
|---|---|---|
| c calibrado | 0,109049 | **0,140844** |
| NSE (in-sample) | 0,3714 | **0,8052** |
| NSE (leave-one-out) | 0,2816 | **0,7759** |
| WIA | 0,8683 | **0,9462** |
| PBIAS | -21,28% | **-0,99%** |
| Erro absoluto médio (LOO) | 46,1% | **27,8%** |

**Comparação com o artigo de referência:** Hao et al. (2022) reportam NSE > 0,70 e WIA > 0,89 nas
três bacias deles. A versão restrita (NSE 0,78-0,81, WIA 0,95) **atinge e supera** esse patamar —
e com uma formulação mais simples (escala constante em vez de FCI/DSC).

### Checagens

- **Consistência física (Q ≤ chuva):** o reescalonamento poderia gerar escoamento maior que a
  chuva do pixel. Aconteceu em **0,48% dos pixels** (12.619 de 2,6 milhões), concentrados nos dois
  eventos com maior fator de correção (evento 4, fator 4,06; evento 10, fator 6,95). Esses pixels
  foram limitados à lâmina de chuva. Precisa ser mencionado no texto.
- **Fatores de correção por evento:** variam de 0,55 (evento 9) a 6,95 (evento 10) — ou seja, a
  correção é grande em alguns eventos, o que é justamente a medida do erro do CN-SCS.
- **Robustez do padrão espacial:** correlação entre o mapa médio novo e o anterior **r = 0,9941**,
  e **96,9%** dos hot spots (top 5%) coincidem. Ou seja, **o mapa de áreas críticas — o produto
  central do TCC — praticamente não muda**. A correção de volume melhora a magnitude por evento,
  não a localização dos hot spots. Isso é um resultado de robustez forte pra reportar.

### Como descrever no TCC

Apresentar os **dois mapas lado a lado** (previsão pura × restrito pelo observado). A diferença
entre eles quantifica a parcela hidrológica do erro. Descrever com transparência como "volume
observado usado como restrição", **não** como previsão pura. Precedente direto: Baert et al.
(2026) usam volume e pico observados como entrada da MUSLE no caso de referência deles.

Figura pronta: `Figuras/comparacao_previsao_vs_volume_restrito.png` (dois mapas em escala de cor
compartilhada + dispersão SY_obs × SY_sim dos dois casos).
Tabela por evento: `Dados Iniciais/comparacao_SY_previsao_vs_restrito.csv`.

## 14. Verificações e correções de 02/10/2026 (preparação da apostila)

Ao montar a apostila explicativa (`Apostila_TCC_Do_dado_ao_mapa.pdf`, na raiz do repositório) e revisá-la com um
revisor independente, os itens abaixo foram verificados contra os scripts, a planilha e os artigos. Os que alteram
afirmações anteriores das notas estão marcados com **(corrige)**.

1. **(corrige) Eq. 8 do DSC.** Hao et al. escrevem `DSC = 1/(1+exp((FCI₀ − FCI)/k))` (k dividindo); o script
   `calcular_dsc_calibrar_validar.py` usava `exp(FCI₀ − k·FCI)` (k multiplicando). A comparação da seção 9 entre
   nossos FCI₀/k e a Tabela 4 de Hao ("ordens de grandeza diferentes") **não era válida**. Recalibração com a forma
   exata (FCI recalculado com piso na mediana, sem leave-one-out): objetivo NSE bruto → FCI₀ = 3,17 (no limite da
   busca), k = 4,90, NSE = 0,21, PBIAS −27,6%; objetivo log-NSE (Eq. 11) → k = 7,94, NSE = −2,63, PBIAS +47,3%.
   Baseline (só c): NSE 0,37. A conclusão de descartar o FCI/DSC **se mantém**. O sinal de FCI₀ na Tabela 4 não pôde
   ser confirmado (o sinal de menos se perdeu na extração do PDF).
2. **(corrige) Comparação com Hao e Baert.** Hao modela Q e pr pelo SCS-CN (Eqs. 2–4), com 26 postos; os NSE
   0,70–0,83 são de calibração, e a validação tem NSE > 0,78 (Fig. 6). A versão com volume restrito não é comparável
   com a previsão de Hao; a frase "atinge e supera" foi corrigida em `base_para_redacao_tcc.md`. Em Baert (Tabela 10),
   as formulações preditivas têm NSE de validação cruzada ≈ 0 (−0,03 a 0,04); 0,46 usa λ ótimo por evento.
3. **(corrige) Escala do coeficiente de Williams.** O 11,8 foi obtido em escala de bacia (não de parcela), como diz
   a seção 7b do `base_para_redacao_tcc.md`. Além disso, seguindo Hao, Q entra em mm e A em m², o que equivale a
   1.000 × o volume em m³: em unidades de Williams há um fator 1.000^0,56 ≈ 48. Mais um motivo para não ler `c` como
   razão de entrega.
4. **Desvios em relação a Hao na etapa de pr.** (a) A Eq. 4 de Hao não tem a divisão por 1.000 que usamos (necessária
   para m³/s); o pr daqui é 1.000× menor que o de uma leitura literal, o que desloca o FCI em cerca de −3,4 (log10),
   efeito constante absorvido por FCI₀. (b) RI e R são rasters interpolados em Hao e escalares por evento aqui.
   (c) RI é o máximo entre os dois postos e R é a chuva ponderada (pesos 0,307/0,693): RI/R passa de 1/h nos eventos
   1 (1,010) e 12 (1,382; DBT5 = 0 mm), o que é fisicamente impossível para um posto só.
5. **Hidrograma unitário do Qp (Fase 1).** Parâmetros finais: Tc = 10,652 h; Tp = D/2 + 0,6·Tc = 6,89 h; Tb = 2,67·Tp
   = 18,40 h (os 4,08 h/10,89 h citados na seção 3.6 são da versão antiga com Kirpich). Com k = 1,1184 o triângulo
   contém só ~54% do volume unitário (1,1184/2,08): o "fator de pico" é um fator de escala empírico, não um
   hidrograma conservativo. Não afeta o mapa (o Qp não alimenta a Fase 2).
6. **r = 0,994 entre os mapas com e sem restrição de volume** é praticamente garantido pela construção (fator f
   uniforme por evento, mapa de cada evento multiplicado por f^1,12). Mostra insensibilidade ao erro de volume total,
   não ao erro espacial de chuva ou CN. As correlações SY×C (0,70) e SY×LS (0,19) refletem a própria fórmula
   (SY ∝ C): são consistência interna, não validação independente.
7. **Fontes dos fatores (segundo o artigo da IC).** K por classe de solo com autores citados (ex.: Cambissolo 0,0475,
   Corrêa et al., 2015; Argissolo 0,0351, Silva, 2016); mapas de solo e uso do solo do Plano de Bacias
   (Consórcio Profill-Rhama, 2020), comparados com referências; LS pelo método de Moore et al. (1991) no SAGA, com MDE do
   USGS. Os dados de vazão e sedimento vêm do ponto de monitoramento hidrossedimentológico a partir de turbidez
   (Murillo-Bermúdez et al., 2021; Murillo-Bermúdez e Martim, 2022). **Ainda falta** registrar a origem dos valores de CN.
8. **Valle Junior et al. (2019):** o λ mediano de 0,045 e a falha do CN (NSE negativo, solos arenosos) são da **mesma**
   bacia (Guariroba). Autoria correta: VALLE JUNIOR, L. C. G.; RODRIGUES, D. B. B.; OLIVEIRA, P. T. S.
9. **Pequenas inconsistências a ter em mente:** (a) erro absoluto do baseline: 44,4% in-sample e 46,1% em
   leave-one-out; (b) WIA e PBIAS reportados são in-sample; (c) λ(chuva) no diagnóstico usa 0,273 como base, contra
   0,2816 do cálculo principal; (d) a acumulação de fluxo que deu 137,80 km² usou MFD, e o FCI usa D8; (e) o convention
   de sinal do PBIAS aqui é Σ(S−O)/ΣO (negativo = subestima), oposto ao comum em hidrologia.

---

## 15. Achado de 15/10/2026: `T_R_m3` inclui a vazão de base (conferência do evento 11, estendida aos 17 eventos)

Durante a auditoria do evento 11 (pasta `Evento11_Auditoria/`) reconstruí as variáveis observadas a partir da série
horária (`Dados_finais_histereses_corrigido.xlsx`, aba Planilha1, colunas Q, CSS, Bt):

- `SYY_t = Σ(Q·CSS·3600/10⁶)` na janela Inicio–Fim (92 leituras no evento 11): reproduz a planilha exatamente
  (1.821,7535 t); `SSY_Ris` = pontos até o pico (inclusive), `SSY_Fall` = depois do pico. **Carga total**, inclui o
  sedimento transportado pela vazão de base.
- `T_R_m3 = Σ(Q)·3600` na mesma janela, nos 17 eventos (diferença < 0,001%). `Ris_R_m3`/`Fall_R_m3` = antes/depois do
  pico. **É o volume TOTAL escoado no exutório, e não o escoamento direto.** Isso corrige a afirmação da seção 4 de
  `notas_qgis_calibracao_qp.md` (que estava errada).
- A coluna `Bt` da série horária (vazão de base, separada pelos autores dos dados; método a confirmar) soma 34–55% do
  `T_R_m3` por evento (evento 11: 957.727 m³ de 2.436.682 m³; escoamento direto = 1.478.955 m³).

**Consequência.** O SCS-CN calcula escoamento *direto*. A calibração CN-I + λ = 0,05 (erro médio +0,5%, absoluto 47,4%)
foi feita contra o volume TOTAL. Contra o escoamento direto (T_R − Σ(Bt)·3600) o mesmo `Vol_CN1_calc` tem erro médio
de **+92%** (absoluto 121%; NSE do volume −6,1 contra 0,18 com o total). Ou seja, os parâmetros "calibrados" (CN seco e
λ baixo) provavelmente compensam a vazão de base que o SCS-CN não modela. O fator f do volume restrito
(`V_med/V_calc`) também reescala Q para um alvo que contém vazão de base, e como E ∝ Q^1,12 isso infla `E_unit` nos
eventos com muita vazão de base.

**O que isso NÃO muda:** a calibração de `c` continua válida como ajuste empírico (c absorve escala), os mapas de padrão
espacial (hot spots) e o fato de `SY_obs` ser carga total medida. **O que muda:** a narrativa da Fase 1 (o "erro de
+0,5%" não pode ser descrito como acerto do SCS-CN sobre o escoamento direto) e a interpretação de `f`. A decisão
(manter volume total como alvo, declarando a limitação, ou recalibrar CN/λ contra o escoamento direto com Bt) deve ser
tomada com o orientador. Para recalibrar é preciso religar o Drive (rasters).

---

## 16. Diagnósticos de 15/10/2026: o que muda com o escoamento direto, e se dá para consertar

Scripts: `Scripts/_diagnostico_escoamento_direto.py`, `_diagnostico_vazao_base_antecedente.py`, `_diagnostico_previsao_com_base.py`.
Alvo "direto" = `T_R_m3 − Σ(Bt)·3600` (separação Bt do projeto).

1. **Volume x λ (Fase 1).** Contra o total, λ = 0,05 dá erro médio ≈ +0,5%. Contra o direto: +92% (NSE do volume −6,1); o viés zera em λ ≈ 0,15 e, com λ = 0,20, é −27,5%. O NSE do volume contra o direto é negativo para todo λ (melhor: −0,41 em λ = 0,28).
2. **Volume restrito ao direto:** f mediano 0,50 (contra 1,03 com o total); c = 0,285; NSE 0,767 / LOO 0,715 (com o total: 0,805 / 0,776).
3. **Triviais:** SY = c·V_direto: NSE 0,783 / LOO 0,733 (c·T_R: 0,809 / 0,765).
4. **Previsão pura com λ recalibrado ao direto:** λ = 0,14 → NSE 0,103 / LOO −0,280; λ = 0,20 → −0,102 / −0,950.
5. **Sensibilidade do alvo (separação da base):** direto = 52,8% do total (Bt), 47,0% (Lyne-Hollick 0,925, 3 passadas) ou 75,1% (linha reta em Qb_inicio). Correlação por evento Bt × LH = 0,996 (razão V_LH/V_Bt de 0,74 a 0,95).
6. **O que explica o erro do SCS-CN no volume direto:** não é a umidade antecedente (r do fator f = V_dir/V_SCS(0,2) com Qb_inicio = +0,03; com chuva antecedente de 5 dias = −0,09), e sim a lâmina de chuva (r = −0,89): a curva chuva-escoamento do SCS-CN tem forma errada para esta bacia (subestima chuvas pequenas e superestima as grandes). Regressões em log com leave-one-out sobre o V_direto: chuva do evento NSE-LOO 0,47; chuva + Qb_inicio + duração 0,50 (erro abs. 31,5%); SCS-CN cru λ = 0,2: −0,72.
7. **Escoamento direto (SCS-CN) + vazão de base prevista** (V_base = kb·Qb_inicio·duração·3600, kb = 1,93, LOO 1,77–2,00; base prevista x Bt observada: NSE-LOO 0,66): volume total com λ = 0,20: erro médio −7,0%, absoluto 25,5%, NSE 0,58 (contra 47,4% e 0,18 do esquema atual). Previsão pura de SY somando q_base uniforme ao Q de cada pixel: NSE in / LOO / erro abs. LOO = 0,502 / 0,425 / 30,1% (λ = 0,20), 0,523 / 0,469 / 30,7% (λ = 0,15), 0,587 / 0,563 / 35,9% (λ = 0,05, mas volume total péssimo, NSE −0,81). Referência atual: 0,371 / 0,282 / 46,1%.
   **Ressalvas:** `Duracao_horas` é a janela observada do evento (não é conhecida antes dele); kb tem 1 parâmetro ajustado nos 17 eventos (corrigido por LOO só para o próprio evento); somar base uniforme a cada pixel é um artifício estatístico (base não erode encostas), coerente apenas porque `SY_obs` é carga total (Q·CSS) medida; λ escolhido entre 4 valores olhando o mesmo conjunto; os benchmarks triviais (c·T_R: LOO 0,77) continuam acima.

---

## 17. Modelo com vazão de base implementado (15/10/2026) — `Scripts/calcular_sy_com_base.py`

> **Números refeitos em 16/10/2026 com o fator LS corrigido (seção 24):** c = 0,010216; SY NSE 0,501 (in-sample) / 0,380 (LOO); 153.855 pixels válidos (138,08 km²); r do mapa com K·C·LS = 0,880. O que está abaixo é o registro da implementação com o LS antigo.

**Definição.** Q_pixel = Q_dir,k (SCS-CN, CN-I, **λ = 0,20 padrão, fixado a priori**) + q_base (mm, uniforme sobre os 154.011 pixels válidos, 138,22 km²), com
q_base = V_base/A_bacia·1000 e V_base = kb·Qb_inicio·Duracao_horas·3600 (kb = 1,929, mínimos quadrados pela origem contra Σ Bt·3600 nos 17 eventos).
Depois: pr = Q/1000·A_pix·(RI/R)/3600; E_unit = 11,8·(Q·pr·A_pix)^0,56·K·C·LS; SY = c·E_unit; **c = 0,13238**.
Validação *leave-one-out* **aninhada** (kb e c refeitos sem o evento retido). Saídas: `Evento N/{Q,pr,E_unit,SY}N_vb.tif`,
`Dados Iniciais/SY_medio_eventos_vb.tif`, `Dados Iniciais/comparacao_SY_modelo_com_base.csv`.

| Resultado | Antes (λ = 0,05, sem base) | Modelo com base (λ = 0,20) |
|---|---|---|
| Volume total x T_R: erro médio / abs. / NSE | +0,5% / 47,4% / 0,18 | −7,7% / 25,5% / 0,58 |
| SY NSE in-sample | 0,371 | 0,498 |
| SY NSE LOO (aninhado) | 0,282 | **0,375** |
| SY erro abs. LOO | 46,1% | 30,2% |
| WIA / PBIAS | 0,868 / −21,3% | 0,892 / −16,5% |
| NSE em log / Spearman (in-sample) | — | 0,561 / 0,600 |

**Sensibilidade a λ (só reportada):** 0,05 → SY NSE-LOO 0,558, mas volume total NSE −0,76; 0,10 → 0,504 / 0,02; 0,15 → 0,437 / 0,42; 0,20 → 0,375 / 0,58. Há troca (trade-off) entre o desempenho do SY e a coerência do volume; adotou-se 0,20 por consistência física.

**Correção do que se afirmou no chat:** o NSE-LOO de 0,43–0,47 do diagnóstico `_diagnostico_previsao_com_base.py` não refazia c com E recalculado sem o evento retido; o valor honesto (aninhado) é 0,375.

**Fragilidades que persistem:** sem o evento 15 (49% da variância) o NSE in-sample cai para 0,07 (LOO −0,01); bootstrap de eventos (4.000 reamostragens, c refeito): IC 95% do NSE [−0,96; 0,88]; benchmarks sem MUSLE: c·T_R LOO 0,765; c·chuva 0,605; c·(V_dir SCS + V_base prevista) 0,383 (≈ o modelo espacial). Eventos 2, 4, 7 e 11 com −43% a −73% (volume total subestimado em 39–64%).
**Mapa:** inalterado em padrão (r = 0,996 com o mapa anterior; 97,3% de coincidência dos 5% superiores; r com K·C·LS = 0,886).
**Ressalvas do método:** Duracao_horas é a janela observada; kb ajustado nos mesmos 17 eventos; base uniforme por pixel é artifício estatístico, coerente porque SY_obs é carga total.

---

## 18. Métricas e calibração robustas ao evento 15 (15/10/2026) — `Scripts/_avaliacao_metricas_robustas.py`

Motivo: o evento 15 responde por 48,7% da variância linear do SY e 49,3% do peso no ajuste de `c` por mínimos quadrados.
**Calibração em log** (ln c = média(ln SY − ln E), erro relativo simétrico) e métricas independentes da variância linear:
mediana do erro percentual absoluto (MedAPE), fração de eventos dentro de fator 2, Spearman, NSE em log.
**Atenção:** no log, os 3 menores eventos (6, 12 e 1) respondem por 68% da variância (ev6 26%, ev12 24%, ev1 18%): troca-se um evento dominante por outros; por isso MedAPE/fator 2/Spearman são a leitura principal. O MAPE (média) favorece subestimar: preferir a mediana.

Resultados (LOO aninhado, c em log; MedAPE / fator 2 / NSE-log / Spearman):
- SY = c·T_R (volume total medido): 17,6% / 94% / 0,86 / 0,875
- SY = c·chuva do evento: 41,9% / 82% / 0,53 / 0,63
- Previsão pura antiga (λ 0,05, sem base): 62,6% / 53% / −0,06 / 0,55
- MUSLE esp. com direto λ 0,20 **sem base**: 97% / 24% / −3,11 / 0,58 (o teste "limpo": o escoamento direto do SCS-CN não prevê a carga)
- Direto λ 0,20 + base uniforme (usa duração observada): 44,0% / 82% / 0,60 / 0,59
- 2 componentes (E_dir λ 0,20 + **base observada**): 24,2% / 94% / 0,82 / 0,74 (usa Bt medida; não é previsão)
- 2 componentes (E_dir λ 0,20 + base prevista, duração observada): 37,7% / 94% / 0,69 / 0,53
- Volume restrito ao total (usa T_R): 23,4% / 94% / 0,83 / 0,76

Conclusão qualitativa **inalterada**: com as métricas robustas, os modelos que usam volume medido (e os de 2 componentes com a base observada) ficam muito à frente dos que só usam chuva e SCS-CN; o MUSLE espacializado sem volume medido não supera SY = c·chuva. Bootstrap de eventos (NSE-log in-sample, IC 95%): c·T_R [0,43; 0,97]; c·chuva [0,07; 0,76]; previsão pura antiga [−3,00; 0,65].
**Cuidado de método:** a escolha da métrica muda o ranking de alguns modelos (a previsão pura antiga piora com calibração em log: MedAPE 43,8% → 62,6%, porque a calibração por MQ subestimava de propósito); deve ser fixada antes e descrita no texto, com a justificativa (peso do evento 15), reportando também o NSE linear com e sem o evento 15.

---

## 19. Opção B implementada: modelo de dois componentes (15/10/2026) — `Scripts/calcular_sy_dois_componentes.py`

> **Números refeitos em 16/10/2026 com o fator LS corrigido (seção 24):** c1 = 0,00352; c2 = 0,013106; MedAPE LOO 32,6%; NSE-log LOO 0,477; parcela das encostas mediana 9% (máx. 35%); mapa: 58,5% de hot spots coincidentes e r = 0,692 com K·C·LS. O que está abaixo é o registro da implementação com o LS antigo.

**Modelo:** SY_evento = c1·Σ_pixels E_unit(Q_direto, SCS-CN CN-I λ = 0,20) + c2·(Qb_inicio·duração da CHUVA·3600). A base é um termo da bacia (não vai para os pixels); a duração é a da chuva (máx. dos dois postos), não a do hidrograma (vazamento). c1 = 0,04790; c2 = 0,012932; calibração em log (mínimos quadrados de ln SY), LOO aninhado. Saídas: `Evento N/{Qdir,pr,E_unit,SY}N_b2.tif`, `SY_medio_eventos_b2.tif`, `comparacao_SY_dois_componentes.csv`. O mapa mostra só a parcela das encostas.

Resultados (LOO; MedAPE / fator 2 / NSE-log / Spearman / NSE linear): 
- **B (adotado, base com duração da chuva):** 33,1% / 71% / 0,48 / 0,72 / −0,60 (sem o evento 15: −1,56).
- SY = c·chuva (referência): 41,9% / 82% / 0,53 / 0,63 / 0,58. SY = c·T_R: 17,6% / 94% / 0,86 / 0,88 / 0,78.
- B' (duração do hidrograma, vaza): 37,7% / 94% / 0,69 / 0,53 / 0,45. B* (base observada, diagnóstico): 24,2% / 94% / 0,82 / 0,74 / 0,60. MUSLE só com direto, sem base: 97% / 24% / −3,11 / 0,58.
- Contra a previsão pura antiga (calibrada em log): MedAPE 62,6% → 33,1%; fator 2 53% → 71%.

**Leitura honesta:** o ganho sobre SY = c·chuva é pequeno e não distinguível do ruído (mediana da diferença do erro % por evento −2,2 pontos, IC95% [−13,5; +18,8]; melhora em 11 de 17 eventos). A parcela das encostas é pequena na soma simulada (mediana 10%; máx. 37%): o termo de base (Qb·duração) carrega quase todo o SY previsto. Superestima fortemente os eventos 1, 9 e 16 (+103%, +177%, +170%) e subestima 4, 7, 11, 12 (−38% a −57%). NSE linear negativo.
**Mapa B:** r = 0,96 com o mapa anterior; 89,8% de coincidência dos 5% superiores; correlação com K·C·LS cai de 0,886 para 0,738 (Spearman 0,81): o padrão espacial passa a carregar mais informação de chuva/CN do que antes.

---

## 20. Desenho fisicamente mais coerente (D): escoamento direto MEDIDO ancorando a MUSLE (15/10/2026) — `Scripts/_avaliacao_direto_medido.py`

Ideia: o SCS-CN só dá o PADRÃO espacial; o total de cada evento é ancorado no escoamento direto medido (V_dir = T_R − Σ Bt·3600, f = V_dir/V_calc, Q = min(f·Q, P)); compara-se com a carga associada ao escoamento direto, SY_direto = Σ (Q − Bt)·CSS·3600/10⁶ (assume mesma CSS da hora; é 55–76% da carga total, mediana 65%). c em log, LOO aninhado.

Alvo A (carga do escoamento direto) — MedAPE / fator 2 / NSE-log / Spearman (LOO):
- MUSLE ancorada no direto medido, λ 0,20: 30,3% / 94% / 0,63 / 0,83; com λ 0,05: 17,2% / 94% / 0,80 / 0,79
- SY = c·V_dir (sem MUSLE): 17,8% / 94% / 0,83 / 0,85; SY = c·chuva: 32,8% / 76% / 0,53 / 0,61
- MUSLE só prevista com SCS-CN direto (sem medida): 96,3% / 18% / −3,07 / 0,56
Alvo B (carga total): MUSLE ancorada λ 0,20: 37,0% / 94% / 0,60 / 0,87; λ 0,05: 18,1% / 94% / 0,80 / 0,83.
Comparada com SY = c·V_dir (alvo A), a MUSLE ancorada (λ 0,20) melhora em 5 de 17 eventos (mediana +11,5 pontos de erro; IC95% [−0,1; +21,1]).
**Leitura:** com a água certa (medida), a fórmula de erosão distribui o volume no espaço e reproduz o sedimento (94% dos eventos em fator 2); com a água só prevista pelo SCS-CN, falha. Aqui λ só muda a FORMA espacial (o volume é ancorado): reportar a sensibilidade, não escolher λ pelo resultado. Desenho adequado ao objetivo (mapear onde os 17 eventos observados erodiram), não é previsão.

---

## 21. Escada da informação hidrológica: onde está o gargalo (15/10/2026) — `Scripts/_escada_gargalo_chuva_escoamento.py`, figura `TCC_Texto/figuras/escada_gargalo.png`

> **Números da escada refeitos em 16/10/2026 com o LS corrigido (seção 24):** N1 32,6%/71%/0,477; N2 38,8%/71%/0,527; N3 34,1%/94%/0,689; N4 13,6%/94%/0,868 (as linhas "simples (sem MUSLE)" não mudaram).

Modelo B (2 componentes, λ 0,20, c em log, LOO aninhado, alvo carga total) x teste simples de 2 termos com os MESMOS insumos (sem MUSLE):
| Nível | B: MedAPE / fator 2 / NSE-log | Simples: MedAPE / fator 2 / NSE-log | B melhor em / mediana da diferença (IC95%) |
|---|---|---|---|
| N1 só chuva e Qb inicial | 33,1% / 71% / 0,48 | 37,7% / 71% / 0,53 | 6/17; +3,4 [−4,0; +10,2] pts (B pior em erro) |
| N2 volume direto previsto (regressão na chuva) | 34,9% / 71% / 0,53 | 35,8% / 71% / 0,55 | 9/17; −0,1 [−3,3; +8,9] |
| N3 volume direto medido + base prevista | 32,5% / 94% / 0,71 | 24,5% / 94% / 0,83 | 7/17; +4,7 [−4,4; +24,1] (simples melhor) |
| N4 volume direto e base medidos (teto) | 11,7% / 94% / 0,87 | 19,5% / 94% / 0,85 | 10/17; −6,7 [−10,8; +7,3] (B melhor, IC cruza zero) |
Referência SY = c·chuva: 41,9% / 82% / 0,53.
**Leitura:** (1) o gargalo é transformar chuva em escoamento: fator 2 passa de 71% (N1/N2) para 94% (N3/N4) assim que o volume de escoamento direto é medido; o volume previsto por regressão (erro médio de 56%) não melhora nada. (2) **Não se pode afirmar que o B é melhor que um teste simples com os mesmos insumos**: ele é equivalente (diferenças dentro do ruído; no N3 o simples é melhor; só no N4 o B fica à frente, com IC cruzando zero). O que o B entrega a mais é o mapa de onde as encostas contribuem; a parcela das encostas no sedimento simulado sobe de 10% (N1) para 67% (N3).

---

## 22. Comparação com a IC (Vivarelli et al., 2025) — `Scripts/_comparacao_IC_x_B.py` (15/10/2026)

A IC é MUSLE **concentrada**: Y = α·(D·qp)^β·K·LS·C·P com D e qp MEDIDOS, K = 0,031, LS = 0,536, C = 0,267 (médias da bacia), α e β ajustados nos 17 eventos (publicado: 0,277 e 0,807; erro médio −4,15%, faixa −60,01% a +37,14%; originais 11,8 e 0,56: erro médio −29,58%, máx. 57,28%).
**Reprodução (D = `T_R_m3` em m³, qp = `Q_pico`):** originais → −32,6% (publicado −29,58%); calibrados publicados → +2,6%, faixa −47% a +62% (publicado −4,15%, −60% a +37%). Aproximada, não exata (provável diferença na fonte de D/qp; a IC cita outro sistema para esses dados). Refazer α, β em log dá α = 0,978, β = 0,733.
Métricas (alvo carga total; MedAPE / fator 2 / NSE-log / Spearman / NSE linear):
- IC originais de Williams: 42,7% / 88% / 0,54 / 0,93 / 0,18
- IC calibrada (α, β publicados), in-sample: 16,0% / 100% / 0,89 / 0,93 / 0,75
- IC refeita em log, **LOO**: 16,3% / 100% / 0,87 / 0,93 / 0,77 (faixa de erro −47% a +97%)
- B nível N1 (só chuva e Qb; previsão): 33,1% / 71% / 0,48 / 0,72 / −0,60 (LOO)
- B nível N3 (volume direto medido + base prevista): 32,5% / 94% / 0,71 / 0,81 / 0,61
- B nível N4 (volume direto e base medidos, mesma informação da IC): 11,7% / 94% / 0,87 / 0,87 / 0,80
**Leitura:** com informação equivalente (volume total e pico medidos na IC; volume direto e base medidos no B/N4) os dois têm qualidade equivalente. A IC supera o B quando o B só recebe parte da informação medida (N1, N3). A IC usa D e qp extraídos do mesmo hidrograma que gera SY_obs (alta circularidade), não prevê e não gera mapa; α e β foram ajustados in-sample (aqui o LOO confirma a robustez da lei de potência).

---

## 23. Teste independente do CN calibrado (subagente, 15/10/2026) — `Notas Claude/teste_cn_calibrado.md`

Conclusão: **calibrar a conversão chuva → escoamento (a, λ, S dependente de P, Hawkins, regressões; 11 formas, LOO aninhado) melhora o volume direto (erro mediano 69% → 40–47%; NSE −0,69 → ~0,4), mas NÃO melhora o sedimento do modelo B de forma distinguível** (ΔNSE-log +0,02 a +0,08; IC95% ≈ [−0,15; +0,35]; Wilcoxon p 0,6–0,9) nem supera SY = c·chuva. O coeficiente de escoamento direto medido varia de 0,03 a 0,22 e é praticamente independente da chuva (r = 0,19 em log); o SCS calibrado livremente "se desmonta" (λ → 0, CN-II ≈ 51, ou S ∝ P). O B é insensível à escala do volume (c₁ absorve; E ∝ Q^1,12).
**Correções ao que eu tinha dito:** (1) o "teto de 12% / 94% em fator 2" exige água medida **e** base observada; só com a água medida e a base prevista o teto é 32,5% / 94% / NSE-log 0,71; (2) o passo "volume previsto por regressão" de `_avaliacao_B_com_Q_bom.py` e `_escada...py` tinha um vazamento pequeno, corrigido na escada (N2: erro mediano do B 34,9% → 39,1%); (3) r = −0,89 com a lâmina só vale em log (−0,63 em linear), e as correlações com Qb_inicio e chuva de 5 dias, refeitas, deram +0,26 e +0,17 (fracas).
Incorporado ao rascunho 04 (seção 5.2, 5.4, apêndices C e E; limitações k e l).

---

## 24. Conferência do fator LS e migração do projeto (16/10/2026) — `Scripts/_recalcular_ls_moore.py`, `Scripts/_teste_sy_com_ls_moore.py`

### 24.1. O LS herdado da IC estava defeituoso

`Dados Iniciais/LS_raster.tif` (reprojetado de `LS Alto.tif`, herdado da IC) foi calculado sobre o
MDE em **WGS 84 geográfico** (pixel em graus), o que corrompe os termos de declividade e de área da
fórmula. Evidência da conferência:

| Teste | Resultado do LS antigo | Esperado |
|---|---|---|
| Correlação LS × declividade | **0,047** (linear); 0,148 (log) | forte e positiva |
| LS por faixa de declividade (0–2% … 70–200%) | praticamente constante, ~0,5 em todas | cresce com a declividade |
| Expoentes ajustados (As, sen β) | 0,13 / 0,13 | 0,4 / 1,3 (Moore) |
| Razão LS_antigo / LS_Moore | ≈ 0,06 | ≈ 1 |

A **declividade** foi confirmada correta: recálculo independente a partir do MDE bate com o raster
usado no projeto (correlação 1,0000). O defeito está no LS, não na declividade.

### 24.2. LS adotado

`Dados Iniciais/LS_moore.tif`, por Moore e Burch (1986) / Moore et al. (1991) sobre o MDE corrigido
em UTM (SIRGAS 2000 / 23S):

    LS = (As/22,13)^0,4 · (sen β / 0,0896)^1,3

com As = área de contribuição específica (área acumulada / largura da célula, em m), **limitada a
200 m** (comprimento de rampa máximo da USLE). O limite é necessário: sem ele, As chega a 4,6
milhões de m nos pixels de canal (a bacia inteira drenando por uma célula) e o LS perde sentido
físico — a USLE descreve erosão de encosta, não de canal. `LS_moore_sem_limite.tif` existe só como
referência e **não deve ser usado**. `LS_raster.tif` foi mantido no disco para comparação.

Resultado: média **7,80** (7,8155 nos pixels de cálculo; o antigo era 0,537), mediana 6,76, máximo
40,3; correlação com a declividade **0,943**; cresce de 0,14 (terreno plano) a ~25 (encostas
íngremes). Figura: `Figuras/comparacao_LS_antigo_vs_moore.png` (`Scripts/_figura_ls_antigo_vs_novo.py`).

**Efeito colateral na máscara de cálculo:** o LS novo não tem valor em 156 pixels em que o raster de
declividade é *nodata* (bordas). Os pixels de cálculo passam de **154.011 (138,22 km²) para 153.855
(138,08 km²)**. Isso desloca o volume do SCS-CN integrado na bacia em −0,15% (13.475 → 13.455 ×10³ m³
no total dos 17 eventos) e os erros por evento na quarta casa; as métricas agregadas de volume
(−7,8% / 25,4% / NSE 0,583) não mudam.

### 24.3. O que mudou no resultado (e o que não mudou)

O LS entra **linearmente** em E_unit, e a escala `c` (ou `c₁`) é calibrada, então o desempenho
agregado quase não muda; o que muda é o **mapa**.

| | LS antigo | LS novo |
|---|---|---|
| Modelo com base (`calcular_sy_com_base.py`): `c` | 0,13238 | **0,010216** |
| SY NSE in-sample / LOO aninhado | 0,498 / 0,375 | **0,501 / 0,380** |
| SY erro absoluto LOO | 30,2% | 30,2% |
| Modelo de 2 componentes (adotado no texto): c₁ / c₂ | 0,04790 / 0,012932 | **0,00352 / 0,013106** |
| B (N1): MedAPE / fator 2 / NSE-log / Spearman (LOO) | 33,1% / 71% / 0,481 / 0,716 | **32,6% / 71% / 0,477 / 0,716** |
| B (N3, água medida): MedAPE / NSE-log | 32,5% / 0,712 | **34,1% / 0,689** |
| B (N4, água e base medidas): MedAPE / NSE-log | 11,7% / 0,874 | **13,6% / 0,868** |
| Parcela das encostas no SY simulado (mediana / máx.) | 10% / 37% | **9% / 35%** |
| Mapa: r com K·C·LS (modelo com base) | 0,569 | **0,880** |
| Mapa: r com K·C·LS (2 componentes) | 0,738 | **0,692** (Spearman 0,789) |
| Mapa: hot spots coincidentes com o mapa λ=0,05 anterior | 97,3% | **56,9%** (58,5% para o de 2 componentes) |
| Volume total: erro médio / abs. / NSE | −7,8% / 25,4% / 0,583 | **idêntico** |
| Benchmarks sem MUSLE (LOO): c·T_R / c·V_direto / c·chuva | 0,765 / 0,733 / 0,605 | **idênticos** |
| IC refeita (α, β; métricas) | 0,978 / 0,733; 16,3% / 100% / 0,867 | **idênticos** (usa K, LS, C médios publicados da IC) |

Hot spots do mapa adotado com o LS novo: C médio 0,212 (bacia 0,050), LS médio 10,3 (bacia 7,8),
K médio 0,047 (bacia 0,039) — coerente.

**Leitura:** a conclusão qualitativa do trabalho **não muda** (o gargalo é a hidrologia; o modelo
espacializado empata com testes simples de mesmos insumos; a IC com dados medidos é melhor), mas o
**mapa de áreas críticas muda muito** e agora é consistente com o relevo: a correlação do mapa com
K·C·LS sobe de 0,57 para 0,88 no modelo com base, e a contribuição por classe de uso se redistribui
(lavoura temporária 29% → 23%; campo 36% → 39%; silvicultura 17% → 22%; solo exposto 12% → 9%).

### 24.4. Scripts migrados e re-executados

`calcular_e_unit.py`, `calcular_sy_com_base.py`, `calcular_sy_dois_componentes.py`,
`gerar_mapas_tcc.py`, `gerar_tabelas_tcc.py`, `gerar_figuras_tcc.py`, `gerar_planilha_comparacao.py`,
`_avaliacao_metricas_robustas.py`, `_avaliacao_B_com_Q_bom.py`, `_avaliacao_direto_medido.py`,
`_escada_gargalo_chuva_escoamento.py`, `_tabela_apendice_B.py`, `_comparacao_IC_x_B.py` (só os
números do B que estavam embutidos em `print`), `gerar_pacote_evento11_dados.py`,
`gerar_pacote_evento11_mapas.py`, `gerar_pacote_evento11_planilhas.py`.

**Não migrados de propósito (registro histórico de diagnósticos superados):**
`calcular_sy_final.py` e `calcular_sy_volume_restrito.py` (linha λ = 0,05, saídas `SY_medio_eventos.tif`
e `*_obs`, usadas como "versão anterior" nas comparações), `calibrar_alfa_beta_pixel.py`,
`_diagnostico_parte3_lambda_variavel.py`, `_diagnostico_escoamento_direto.py`,
`_diagnostico_previsao_com_base.py`, `_calibrar_cn_escoamento_direto.py`.

**Constante que NÃO deve ser trocada:** `KLSC = 0,031 · 0,536 · 0,267` em `gerar_tabelas_tcc.py`,
`gerar_figuras_tcc.py`, `_tabela_apendice_B.py` e `_comparacao_IC_x_B.py` são as médias **publicadas
pela IC** (Tabela 3 de Vivarelli et al., 2025); trocá-las deixaria de reproduzir a IC.

**Pendência:** as colunas de sedimento da Tabela 19 do rascunho 04 (Apêndice D, conversões
chuva-escoamento calibradas) e os números de `teste_cn_calibrado.md` foram calculados com o LS
antigo. Refazê-los depende de `_calibrar_cn_escoamento_direto.py` (forma (i)) e dos scripts do
revisor independente, que ficaram fora do repositório. As conclusões não dependem desses valores.

---

## 25. Conferência da seção 3.3 (Dados cartográficos) do Google Doc (17/10/2026)

Conferência de cada número da seção 3.3 contra os rasters do projeto.

### 25.1. Confere

| Afirmação na 3.3 | Valor conferido |
|---|---|
| grade 884 × 365 pixels | 884 × 365 ✔ |
| pixel 29,992 × 29,925 m; área 897,49 m² | exato ✔ |
| SIRGAS 2000 / UTM 23S | EPSG:31983 ✔ |
| K médio 0,039 | 0,0388 ✔ |
| C médio 0,050 | 0,0495 ✔ |
| ~154,7 mil pixels com CN | 154.667 ✔ |
| Tabela 5: K e C por classe e % dos pixels | todas as 13 linhas conferem na 1ª decimal ✔ |

### 25.2. Corrigido no documento (valores que mudaram com o LS novo)

| | antes | agora |
|---|---|---|
| LS médio (Tabela 4) | 0,536 | **7,80** |
| pixels com todos os fatores | 154,0 mil | **153,9 mil** (153.855) |
| área correspondente | 138,2 km² | **138,1 km²** (138,08) |
| pixels de borda descartados | ~650 | **~810** (812) |

Também corrigida a célula da Tabela 4 que trazia `[conferir]`: dizia "MDE (USGS) pelo método de
Moore et al. (1991) no SAGA", que é a procedência do LS **da IC** (descartado). O LS adotado foi
calculado em Python/GDAL (`_recalcular_ls_moore.py`) sobre o MDE corrigido em UTM; SAGA/QGIS
entrou só no tratamento do MDE e na área acumulada (MFD). Nova redação: "MDE de 30 m (USGS),
corrigido e com área acumulada no SAGA/QGIS; LS por Moore e Burch (1986), com rampa limitada a
200 m" — consistente com a seção 2.6 do texto.

### 25.3. O CN **não** vem do cruzamento uso × solo (resolve a pendência do item 7 da seção 11)

Rasterizei `Uso Solo Alto.shp` (campo `CLASSE`) e `Pedologia Alto.shp` (campo `Subordem`) **na
própria grade do `CN TCC.tif`** (973 × 362, sem reamostrar o CN) e cruzei com os três rasters de CN.

1. **AMC I e III são exatamente as conversões de Chow, Maidment e Mays (1988)** aplicadas ao raster
   de AMC II — conferido nos 20 valores distintos de CN II, com erro < 0,1. Isso está fechado e pode
   ser escrito com segurança.
2. **O raster de AMC II não é reproduzível a partir dos mapas de uso e de solo.** Dentro de uma
   mesma combinação o CN varia: em "Campo" aparecem 77 (44% dos pixels), 81 (32%), 65 (10%), 64 (4%);
   em "Mata Nativa", 65 (59%), 77 (18%), 52 (17%). E há valores que não são de tabela de CN
   (55, 67, 69, 72, 73, 74, 78, 82, 84, 88), típicos de média ponderada por área.
3. **Valor dominante por classe de uso** (serve para reconstruir a tabela, se a original não
   aparecer): Mata Nativa 65, Campo 77, Silvicultura 65, Lavoura Temporária 77, Área Urbanizada 85,
   Solo exposto 85, Mineração 77, Afloramento Rochoso 52, Corpos d'Água 98.
4. **Médias nos 153.855 pixels de cálculo:** CN I = 52,5; CN II = 71,6; CN III = 84,9.

Conclusão: a frase "o cruzamento entre uso e solo deu o número de curva" é imprecisa. Falta pedir ao
orientador (a) a tabela de CN com a referência, (b) o grupo hidrológico de cada classe de solo,
(c) a condição hidrológica por classe de uso. Registrado como comentário no Google Doc.

### 25.4. Vazão de base

A frase inconclusa "A vazão de base (Bt) [continuar mais tarde]" foi completada: Bt já vinha
calculada na base recebida, entra como dado de entrada e não como resultado, e o método de separação
será confirmado com o orientador (ver seção 17 e a investigação de procedência em
`dados_area_estudo_plano_bacias.md` §9–11).

### 25.5. Origem do CN resolvida: ANA, BR_CN-2022 (17/10/2026) — `scratchpad/ana_cmp*.py`

O usuário indicou a fonte: **ANA, "Curva Número na Base Ottocodificada (1985, 2014 e 2022)"**
(catálogo de metadados SNIRH, registro `d1c36d85-a9d5-4f6a-85f7-71c2dc801a67`). Conferido lendo os
rasters da ANA por `/vsicurl/` (sem baixar o Brasil inteiro) e reamostrando na grade do `CN TCC.tif`:

| Produto ANA | pixels idênticos | valores únicos | média |
|---|---|---|---|
| **BR_CN-2022.tif** | **90,7%** — e **100,00%** no interior das manchas homogêneas (73.558 px) | **20, o mesmo conjunto** | 71,60 (nosso: 71,595) |
| BR_CN-1985.tif | 55,7% | 17 | 70,60 |

As divergências com o 2022 ficam só nas bordas entre classes (efeito da reprojeção). O pixel de
27,25 × 30,17 m do `CN TCC.tif` também denuncia a origem geográfica (0,000269495° ≈ 27,6 × 30,0 m
nessa latitude). **Conclusão: `CN TCC.tif` = BR_CN-2022 reprojetado para SIRGAS 2000 / UTM 23S.**

Isso explica o item 25.3: o CN não bate com os mapas de uso/solo do Plano de Bacias porque vem de
**outros mapas** — uso do MapBiomas (coleção 2023, ano 2022) e solo do IBGE, com grupos
hidrológicos de Sartori, Lombardi Neto e Genovez (2005). Inconsistência registrada no texto como
limitação: CN e K/C usam mapas de uso diferentes.

Aplicado no Google Doc: frase de abertura da 3.3, célula CN da Tabela 4 (fonte + "71,6 (AMC II)")
e parágrafo de procedência do CN depois de "Todos os rasters..." (substitui o antigo [PENDENTE]).

---

## 26. Dúvidas do orientador e respostas (26/10/2026)

O orientador revisou o material e não entendeu dois pontos. Respostas dadas ao usuário (base para o texto):

1. **De onde veio a vazão de base:** coluna `Bt` de `Dados_finais_histereses_corrigido.xlsx` (Planilha1,
   col. G), a mesma série horária de Q e CSS do Murillo-Bermúdez — **não foi calculada por nós**; método
   não documentado (Lyne-Hollick e Eckhardt não reproduzem). Como a planilha é do próprio orientador,
   devolver a pergunta: quem gerou `Bt` e como. O modelo de previsão **não lê `Bt`**: o termo de base
   usa Qb_inicio × duração da chuva; `Bt` só serve para (a) mostrar que T_R é volume total e (b) o
   diagnóstico "água e base observadas".
2. **Por que a "base" carrega a maior parte do sedimento no modelo de dois componentes:** o termo
   c₂·Qb_inicio·T_chuva fica com 65–100% do SY previsto (mediana 91%). **Não é partição física**: mesmo
   com CSS igual, a base levaria no máximo sua fração do volume (34–55%). É estatístico: a MUSLE das
   encostas depende do escoamento direto do SCS-CN, que prevê mal (sozinha: 24% em fator 2), e
   Qb_inicio × duração mede o tamanho/umidade do evento. Sugestão de texto: chamar de **"termo de escala
   do evento"**, declarar que a partição é de ajuste; alternativa física (só se o orientador quiser):
   sedimento da base = Bt × CSS pré-evento, sem calibrar.
3. **Por que o modelo forçado melhora:** recebe a água medida — o SCS-CN erra o volume direto em 69%
   (mediana) e E ∝ Q^1,12; a carga medida é Σ Q·CSS (circularidade parcial). Parcela das encostas sobe de
   9% para ~38%. Não é previsão, é teto. A MUSLE acrescenta pouco sobre SY = c·volume medido (14% × 17,6%).
4. **Por que separar a base (o modelo antigo "funcionava"?):** o antigo (CN-I, λ = 0,05, alvo T_R)
   acertava só a média (+0,5%) por compensação — contra o escoamento direto errava +92%; volume abs. 47% /
   NSE 0,18 contra 25,5% / 0,58; sedimento MedAPE 62,6% → 33%, fator 2 53% → 71%, NSE-LOO 0,28 → 0,38; e
   o mapa erodia encostas com água subterrânea. Trade-off: λ = 0,05 no modelo com base dá NSE-LOO 0,56 mas
   volume NSE −0,76 — adotado 0,20 por coerência física.
5. **SY = c·chuva:** forma linear pela origem, c = **19,7 t/mm**, calibrado em log (média geométrica de
   SY/R; por MQ linear seria 22,3, puxado pelo evento 15), refeito a cada rodada do LOO.
6. **Comparações justas (mesma informação):** só chuva → c·chuva (42% / 82%) × calculado (33% / 71%):
   empate. Água medida → IC concentrada (16% / 100% / NSE-log 0,87) × forçado (14% / 94% / 0,87): empate.
   Leitura: espacializar não custa precisão; o limite é chuva → escoamento. Não comparar calculado × IC.

Obs.: em 26/10 os três CSVs de `Dados Iniciais/` apareciam modificados (gravados em 17/10 21h), mas os
valores são idênticos aos do commit — só formatação. O progresso do notebook não tinha sido enviado ao GitHub.

---

## 27. Vazão de base removida do modelo — modelo adotado só com escoamento direto (26/10/2026) — `Scripts/calcular_sy_so_direto.py`

**Decisão (usuário + orientador, 26/10/2026):** λ = 0,20 e **sem termo de vazão de base**. Argumento do orientador: a
MUSLE descreve erosão por escoamento superficial; a base não entrega sedimento das encostas, e a banca questionaria um
termo empírico de base carregando ~91% do sedimento. O alvo continua sendo a carga TOTAL medida (todo o sedimento do
evento é atribuído ao escoamento superficial; a base só transporta). `Bt` só serve para o escoamento direto medido.

- **MC:** SY = c·ΣE_unit(Q SCS-CN, CN-I, λ 0,20); **c = 0,0784**.
- **MFM:** SY = c·ΣE_unit(Q reescalado a V_dir = T_R − ΣBt); **c = 0,0302**. c em log, LOO.

| (LOO, carga total) | MedAPE | fator 2 | NSE-log | Spearman | NSE lin (in / LOO / s/ev15) |
|---|---|---|---|---|---|
| **MC** (adotado) | 97,9% | 24% | −3,95 | 0,57 | −49,8 / −65,3 / −30,9 |
| **MFM** (adotado) | 38,7% | 94% | 0,50 | 0,86 | 0,56 / 0,50 / 0,17 |
| sens. MC λ 0,05 | 63,2% | 47% | −0,09 | 0,55 | −0,86 / −1,17 / −1,22 |
| sens. MFM padrão λ 0,05 | 18,5% | 94% | 0,81 | 0,84 | 0,78 / 0,75 / 0,59 |
| SY = c·chuva | 41,9% | 82% | 0,53 | 0,63 | 0,62 / 0,58 / 0,41 |
| SY = c·V_dir medido | 15,9% | 94% | 0,85 | 0,90 | 0,77 / 0,74 / 0,56 |
| SY = c·T_R | 17,6% | 94% | 0,86 | 0,88 | 0,80 / 0,78 / 0,61 |
| IC concentrada | 16,3% | 100% | 0,87 | 0,93 | 0,82 / 0,77 / 0,65 |

Calibração linear (sensibilidade): MC NSE −0,14 / −1,11; MFM 0,80 / 0,79; c·chuva 0,67 / 0,61.
Escoamento direto SCS-CN/medido: mediana 0,58 (0,02 a 1,95); erro mediano 69%; NSE do volume −0,69.
Comparações por evento (erro % LOO): MC × c·chuva melhora em 3/17, +63 pontos [IC95% +15; +309];
MFM × c·V_dir 3/17, +14 [+3; +39]; MFM × IC 5/17, +21 [−2; +27].
**Mapas:** o padrão do MC é idêntico ao da parcela das encostas do modelo de dois componentes (r = 1,0000; só a
escala muda); MC × MFM r = 0,966, 90,9% das áreas críticas coincidentes; r com K·C·LS 0,692 (MC) e 0,633 (MFM).
As porcentagens por classe (Tabelas 12–13) não mudam; o kg/pixel muda.

**Leitura:** (1) o MC fica bem abaixo da regra da chuva — o termo de base mascarava a falha do SCS-CN; (2) com a água
medida, a MUSLE acerta a ordem de grandeza (94% em fator 2), mas fica abaixo da IC e de c·V_dir na régua em log
(empata no NSE linear); (3) no MFM, λ só muda o padrão espacial, e o padrão λ 0,05 é bem melhor (18,5%): o SCS-CN com
λ 0,20 concentra o escoamento em poucos pixels — reportar como sensibilidade. A conclusão "a espacialização mantém a
qualidade da formulação concentrada" deixa de valer na régua em log; o ganho passa a ser só o mapa.

**Arquivos:** novos — `calcular_sy_so_direto.py`, `Evento n/{Qdir,pr,E_unit,SY}{n}_sd.tif`,
`SY_medio_eventos_sd.tif`, `SY_medio_eventos_forcado_sd.tif`, `comparacao_SY_so_direto.csv`,
`tab_mc_mfm_eventos.md`, `tab_nse_linear.md`, `fig_volume_direto.png`. Atualizados — `gerar_tabelas_tcc.py`,
`gerar_figuras_tcc.py` (dispersão com 4 painéis; `fig_decomposicao.png` removida), `gerar_mapas_tcc.py` (mapas 5–8 e
fluxograma), `_escada_gargalo_chuva_escoamento.py` (3 degraus, sem base), `_tabela_apendice_B.py`,
`gerar_planilha_comparacao.py` (`Comparacao_Modelos_TCC.xlsx`, escalas por MQ linear). Mantidos como registro, **não
adotados**: `calcular_sy_dois_componentes.py` (_b2) e `calcular_sy_com_base.py` (_vb).
**Não atualizados (desatualizados, avisar se forem usados):** `Relatorio_Resultados_TCC.pdf` (relatório ao orientador,
setembro), pacote `Evento11_Auditoria/`, `TCC_rascunho_04.md/.docx` (o Google Doc é a fonte da verdade).
Mudanças a fazer no texto: `Notas Claude/mudancas_docs_sem_base_26-10.md`.


---

## 28. Origem da vazão de base confirmada: filtro de Eckhardt (27/10/2026) — `Scripts/_conferir_filtro_eckhardt.py`

O orientador informou o método: **Eckhardt (2005)**, com os coeficientes calibrados segundo Collischonn e Fan (2013,
DOI 10.1002/hyp.9391), e enviou a série (`Dados Iniciais/serie_Q_Qb_Qquick_Eckhardt_orientador.xlsx`; CLP, horária,
14/11/2018 a 31/03/2021, colunas Q, Qb e Qquick = Q − Qb).
- **Mesma série da coluna Bt** que usamos: r = 0,99999, max |dif| = 0,04 m³/s, somas por evento +0,1% a +0,4%.
  Nada a recalcular.
- **Reproduzida exatamente** (max |dif| 8,9e-16) por bₜ = [(1−BFImax)·α·bₜ₋₁ + (1−α)·BFImax·Qₜ]/(1 − α·BFImax), bₜ ≤ Qₜ,
  b₀ = Q₀, passada única para a frente, com **α = 0,995 e BFImax = 0,70**. O cabeçalho da planilha diz BFImax = 0,58
  (com 0,58: r = 0,982, BFI 0,567 contra 0,659) — **confirmar com o orientador**.
- Por que os testes de 16/10 falharam: a busca ia só até α = 0,98.
- Isso fecha a pendência das seções 15–17 e de `dados_area_estudo_plano_bacias.md` §9–11.
