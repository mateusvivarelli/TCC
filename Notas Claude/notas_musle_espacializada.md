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
| LS | `Dados Iniciais/LS_raster.tif` | `LS Alto.tif` (reprojetado de WGS84) | 0,536 | 0,536 (bate exato) |
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
