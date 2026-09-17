# Notas de trabalho — Calibração de Q e espacialização de Qp

Registro de diagnóstico e passos executados nesta sessão (2026-09-12), para o TCC da bacia do
Rio Jundiaí (Desemboque do Túnel 5 / Campo Limpo Paulista).

## 1. Contexto encontrado no projeto

- Pipeline de chuva → CN-SCS já implementado em [Scripts/spatialRain.py](Scripts/spatialRain.py):
  para cada um dos 17 eventos, interpola a chuva pontual (2 postos: DBT5 e Campo Limpo Paulista)
  por IDW (potência 2, pixel 30 m) sobre a extensão do raster `CN TCC.tif`, e aplica a fórmula do
  SCS-CN (`Q = (P - 0,2S)² / (P + 0,8S)`, com `Q = 0` se `P ≤ 0,2S`) para 3 cenários fixos de CN
  (CN-1 seco / CN-2 normal / CN-3 úmido), gerando `Q{n}_CN{1,2,3}.tif` e `Qvol{n}_CN{1,2,3}.tif`
  (volume em m³, pixel = 900 m²) em cada pasta `Evento {n}`.
- [Scripts/excelReader.py](Scripts/excelReader.py) gera os CSVs de entrada de chuva a partir de
  `Dados Iniciais/eventos_processados_manuais.xlsx`, que também traz os dados **medidos** no
  exutório: `Q_pico` (vazão de pico, m³/s), `T_R_m3` (volume total de escoamento direto,
  já separado de base — `Ris_R_m3` + `Fall_R_m3`), e índices de precipitação antecedente já
  calculados (`Ap1_pond_mm` ... `Ap14_pond_mm`, ponderados entre os 2 postos).
- Para a vazão de pico (Qp) espacializada, havia uma tentativa em
  `Dados Iniciais/qp_spatial/`: MDE recortado numa área bem maior que a máscara da bacia,
  processado em SAGA (carve → fill sinks → flow direction → flow accumulation → "remendo"/patch
  → fill sinks final → flow accumulation final), mas sem chegar a um raster de Qp de fato.

## 2. Diagnóstico: calibração do volume (Q / CN-SCS)

Rodei o Python embutido do QGIS (`"C:\Program Files\QGIS 3.44.14\bin\python-qgis-ltr.bat"`, tem
GDAL e bindings do QGIS acessíveis) para somar os rasters `Qvol{n}_CN{1,2,3}.tif` já gerados e
comparar com `T_R_m3` medido. Resultado salvo em
[Dados Iniciais/comparacao_volumes_medido_vs_calculado.csv](Dados%20Iniciais/comparacao_volumes_medido_vs_calculado.csv).

Erro percentual médio (calculado vs. medido), 17 eventos:

| Cenário | erro médio | erro médio absoluto | desvio-padrão do erro |
|---|---|---|---|
| CN-1 (seco)   | -62,6% | 62,6%  | 32,0%  |
| CN-2 (normal) | +38,7% | 77,0%  | 83,9%  |
| CN-3 (úmido)  | +188,1%| 192,7% | 146,7% |

**Leitura importante:** não é só um viés sistemático (que daria pra corrigir com um fator de
escala). O CN-2, por exemplo, varia de -84% (evento 10) a +161% (evento 9) — ou seja, o mesmo
cenário de CN acerta bem alguns eventos e erra feio outros. Isso indica que o problema não é
"qual dos 3 CNs fixos é o certo", e sim que **um único CN fixo não serve para todos os eventos**.

### Causas prováveis, em ordem de impacto esperado

1. **AMC (condição de umidade antecedente) não está variando por evento.** O script roda os
   3 cenários para todos os eventos, mas a escolha de qual usar deveria depender da chuva
   antecedente de cada evento — e essa informação **já existe na planilha**
   (`Ap5_pond_mm`, chuva acumulada ponderada de 5 dias antes, que é o critério clássico do
   SCS para classificar AMC I/II/III). Isso explica a variância enorme dentro de um mesmo
   cenário: eventos com solo já saturado (Ap5 alto) deveriam usar CN-3, eventos secos (Ap5 baixo)
   deveriam usar CN-1, e hoje todos usam o mesmo raster.
2. **Razão de abstração inicial Ia = 0,2·S.** O CN-1 (o "mais parecido" no agregado, com -62%)
   subestima sistematicamente — sinal clássico de que 0,2 é alto demais para a bacia. Vários
   estudos em bacias tropicais/subtropicais e urbanizadas no Brasil (ex. Sartori, Silveira)
   recomendam λ = 0,05 em vez de 0,20. Isso aumenta o Q calculado para o mesmo S/CN sem precisar
   inflar CN artificialmente.
3. **IDW com apenas 2 postos pluviométricos.** A interpolação praticamente vira uma média
   ponderada entre 2 pontos — pouca informação espacial de fato. Como a fórmula do CN-SCS é
   não linear (quadrática acima do limiar), pequenos erros na lâmina P se amplificam bastante no
   Q calculado. Vale reportar isso como limitação, mas não dá pra resolver sem mais estações.
4. Vale conferir também se `T_R_m3` (medido) e o volume calculado estão na mesma base — pelo que
   vi, sim: `T_R_m3 = Ris_R_m3 + Fall_R_m3` já é escoamento direto separado da vazão de base
   (`Qb_inicio`), compatível com o que o CN-SCS estima (só escoamento direto, não base).

### Recomendação concreta de calibração

- **Curto prazo (baixo esforço, alto retorno):** em vez de rodar CN-1/2/3 para todo evento,
  escolher automaticamente o cenário por evento a partir de `Ap5_pond_mm` (usando os limiares
  padrão do SCS para as estações seca/chuvosa), e comparar o erro resultante — deve reduzir
  bastante a dispersão vista no CN-2.
- **Ajustar λ (Ia/S) para 0,05** e reprocessar, comparando o novo erro médio/desvio-padrão contra
  a tabela acima.
- **Calibração formal (se o tempo do TCC permitir):** para cada evento, resolver por otimização
  o fator de escala do CN (ou de S) que reproduz o `T_R_m3` medido, dado o raster de chuva IDW já
  calculado. Depois, correlacionar o CN "calibrado eficaz" de cada evento com `Ap5_pond_mm` (ou
  outro índice antecedente) — isso constrói uma curva de calibração específica da bacia, com
  respaldo estatístico, em vez de assumir que os 3 cenários padrão do SCS servem para o Jundiaí.
  Recomendo separar ~70% dos eventos para calibrar e validar nos ~30% restantes.

## 3. Diagnóstico: geração do flow accumulation (para espacializar Qp)

Rodei `gdalinfo -stats` (via `"C:\Program Files\QGIS 3.44.14\bin\gdalinfo.exe"`) nos rasters de
`Dados Iniciais/qp_spatial/`. Achados:

- **Grade da bacia (CN/chuva) é diferente da grade usada no MDE/flow accumulation.**
  - `CN TCC.tif` / `ChuvaIDW*.tif`: origem X ≈ 318.646, ~884×365 pixels, ~30 m → cobre só a
    máscara da bacia (Máscara Jundiaí: X 318.648–345.131 / Y 7.424.317–7.434.818).
  - `qp_spatial/*.sdat`: origem X = 264.102, **2722×1097 pixels**, 30 m → cobre uma área muito
    maior (~82 km × 33 km) que engloba toda a drenagem a montante.
  - **Isso está correto, não é erro:** para calcular acumulação de fluxo de verdade, o MDE
    precisa incluir toda a área a montante do exutório, não só o polígono da máscara — se
    recortar primeiro, a acumulação fica errada nas bordas da bacia. O problema é que, **depois**
    de gerar a acumulação nessa grade grande, falta recortar/realinhar o resultado para a grade
    menor (30 m, mesma origem/alinhamento do `CN TCC.tif`) antes de combinar com a chuva —
    exatamente como o `spatialRain.py` já faz para o raster `S` via `gdal.Warp`.
- **O primeiro flow accumulation (`flowaccDEM.sdat`, antes do "carve"/queima da rede de
  drenagem) tem máximo de 983.700** → a 900 m²/célula (unidade "cell area", padrão do SAGA),
  isso é só **~1,1 km²** de área de contribuição no ponto de maior acumulação — muito pequeno
  pra ser o exutório de uma bacia desse tamanho. Isso é o sintoma clássico de MDE sem "queima"
  da rede de drenagem: depressões/planícies fazem o fluxo se perder em vários sub-sinks locais
  em vez de convergir pro canal principal.
- **Depois do carve + patch ("remendo") + fill sinks final, `flowaccFINAL.sdat` tem máximo de
  109.788.256** → **~122.000 células × 900 m² ≈ 110 km²** no ponto de maior acumulação. Esse
  valor já é fisicamente plausível para a bacia (a máscara tem bounding box de ~26,5 km × 11 km).
  **Ou seja: o flow accumulation final já parece ter funcionado**, ao contrário do que a primeira
  tentativa (`flowaccDEM`) sugeria.

### O que provavelmente ainda falta (a causa real do "não funciona")

Como o `flowaccFINAL.sdat` parece numericamente coerente, o bloqueio mais provável não é "gerar"
o flow accumulation, e sim:

1. **Conferir se o pixel do exutório real** (onde fica a estação/posto de medição de vazão,
   Desemboque do Túnel 5) **cai em cima do canal mapeado** no raster de acumulação — com MDE de
   30 m é comum o pixel "certo" (maior valor local de acumulação, alinhado com `drenagem.shp`)
   não coincidir exatamente com a coordenada do ponto de medição. Isso é resolvido com uma
   busca de "snap" (pegar, numa janela pequena ao redor da coordenada do posto, o pixel de maior
   flow accumulation).
2. **Recortar e realinhar `flowaccFINAL.sdat` para a grade de 30 m do `CN TCC.tif`** (mesma
   lógica do `gdal.Warp` usado em `spatialRain.py` para o raster S), pra poder combinar
   acumulação de área × intensidade de chuva pixel a pixel.
3. **Definir o método de espacialização do Qp em si** — flow accumulation dá a área de
   contribuição (A) por pixel; falta decidir a fórmula que transforma (A, intensidade de chuva,
   CN) em vazão de pico. O mais comum e compatível com o que já foi construído é o **Método
   Racional** (`Qp = C · i · A / 3,6`, com C relacionado ao CN e i em mm/h vindo do raster IDW),
   mas outras abordagens (hidrograma unitário SCS, por exemplo) também seriam possíveis.
   **Isso ainda precisa ser confirmado com o usuário antes de implementar o script.**

## 3.1. Achado crítico: coordenada de DBT5 fica fora da bacia modelada

Ao implementar o script [Scripts/spatialPeakFlow.py](Scripts/spatialPeakFlow.py) (Método
Racional, confirmado com o usuário), tentei localizar o pixel do exutório (posto **DBT5** =
"Desemboque do Túnel 5", coordenadas usadas em `excelReader.py`: lon -46.4809, lat -23.2646) na
grade de trabalho. Resultado, convertendo para SIRGAS 2000 / UTM 23S (EPSG:31983):

- **DBT5** → X = 348.520,8 / Y = 7.426.415,3
- Grade da bacia (CN/chuva): X entre 318.646 e 345.159
- MDE grande usado no flow accumulation (`qp_spatial`): X entre 264.102 e 345.762
- `drenagem.shp` (rede de drenagem digitalizada): X entre 318.981 e 345.022

**O ponto DBT5 fica cerca de 2,4 a 3,4 km a leste do limite direito de todas essas camadas** —
ou seja, fora da máscara da bacia, fora do MDE usado para o flow accumulation, e fora da própria
rede de drenagem digitalizada. (Como referência, o outro posto, Campo Limpo Paulista, cai bem
dentro de todas as grades — X = 319.862 — então não é um erro de eixo/CRS na conversão, é
específico do ponto DBT5.)

Isso tem duas implicações que preciso que você confirme antes de eu continuar:

1. **Para a chuva (IDW):** a interpolação em `spatialRain.py` usa DBT5 como um dos únicos 2
   postos, mas ele está fora da grade — ou seja, o IDW está **extrapolando** a partir de um ponto
   fora da bacia, não interpolando entre 2 pontos que a cercam. Isso pode ser parte da causa da
   variância enorme vista na calibração do volume (seção 2), porque o gradiente espacial da
   chuva fica sendo "puxado" por um ponto de fora.
2. **Para a vazão de pico:** se DBT5 é de fato o local de medição de vazão (o nome sugere a saída
   de um túnel, possivelmente uma estrutura de transposição de água entre bacias, ex. Sistema
   Cantareira — não uma seção natural do rio Jundiaí dentro da bacia mapeada), então a "área de
   drenagem" vinda do flow accumulation **não necessariamente representa** a área que contribui
   para essa vazão medida. Isso quebraria a premissa do Método Racional (`A` = área de
   contribuição natural a montante do ponto).

**Preciso saber:** DBT5 é mesmo o ponto de medição da vazão (exutório) usado para `Q_pico` e
`T_R_m3`? Se sim, ele é uma seção natural do rio ou a saída de uma estrutura de transferência de
água (túnel/adutora)? A coordenada foi conferida em campo/na fonte original, ou pode estar
digitada errada? Isso decide se dá pra seguir com o Método Racional como está, se precisa ajustar
a coordenada, ou se o conceito de "área de drenagem" precisa ser repensado para esse ponto.

## 3.2. Exutório real localizado e Qp calculado

Como o DBT5 não é o ponto de medição, localizei o exutório real de forma objetiva: interseção
entre `drenagem.shp` e o limite de `Máscara Jundiaí.shp` (script
[Scripts/_find_outlet.py](Scripts/_find_outlet.py)). Existe **um único** ponto de cruzamento —
X=318.980,77 / Y=7.432.307,08 (SIRGAS 2000 / UTM 23S) — e ele coincide exatamente com o pixel de
**maior valor de todo o raster de flow accumulation** (109,79 km²), o que é uma confirmação forte
de que o flow accumulation está correto e o ponto é mesmo o exutório principal da bacia. Esse
ponto fica a ~880 m do posto pluviométrico "Campo Limpo Paulista" (não do DBT5).

Rodei o script [Scripts/spatialPeakFlow.py](Scripts/spatialPeakFlow.py) completo (recorte/
realinhamento do `flowaccFINAL.sdat` para a grade de 30 m, Método Racional
`Qp = C·i·A/3,6` com `C = Q/P` pixel a pixel do CN-SCS já calculado, `i` = intensidade de pico do
IDW escalada pelo fator `Intensidade_60min_mm/h ÷ Chuva_evento_mm` de cada evento) usando essa
coordenada. Resultado salvo em
[Dados Iniciais/comparacao_qpico_medido_vs_calculado.csv](Dados%20Iniciais/comparacao_qpico_medido_vs_calculado.csv).

**O erro é enorme e sistemático, em todos os 17 eventos e nos 3 cenários de CN — de +190% a
mais de +8.500%, com médias de 1.656% (CN-1) a 4.295% (CN-3).** Isso não é o mesmo tipo de erro
disperso (com direções variadas) que vimos na calibração do volume — aqui o modelo **sempre**
superestima, e por uma ordem de grandeza (10x a 80x maior que o medido). Erro desse tamanho e
dessa consistência não se resolve ajustando CN/λ — é sinal de problema estrutural no método, não
de calibração fina.

**Causa mais provável: a bacia (109,79 km² no exutório) é grande demais para o Método
Racional.** A literatura de hidrologia (inclusive a própria origem do método e adaptações como o
TR-55/NRCS) recomenda o Método Racional só para bacias pequenas — tipicamente até 2-3 km², com
alguns autores tolerando até ~8 km² em condições especiais. A premissa do método é que a chuva de
projeto (intensidade de pico de 1h, no nosso caso) atinge a bacia inteira simultaneamente e que o
tempo de concentração é curto o suficiente pra toda a área contribuir ao mesmo tempo no pico. Numa
bacia de ~110 km², o tempo de concentração real é de muitas horas (possivelmente >1 dia), então
usar a intensidade de pico horária pontual multiplicada pela área inteira infla o resultado
de forma artificial e sistemática — exatamente o padrão observado (sempre superestima, por muito).

### Decisão necessária antes de prosseguir

Isso não é um bug para corrigir no script — é uma escolha de método que precisa ser revista:

1. **Trocar para Hidrograma Unitário SCS** (ou outro método distribuído/com routing) — mais
   correto fisicamemente para bacias desse porte, mas exige tempo de concentração (por
   sub-bacia ou pela bacia toda) e mais esforço de implementação.
2. **Manter o Método Racional mas documentar a limitação explicitamente no texto do TCC**,
   tratando o resultado como uma estimativa de referência/comparação simplificada, não como
   previsão de Qp real — alguns trabalhos fazem isso conscientemente.
3. **Conferir se a área de 109,79 km² está mesmo certa** para o ponto onde `Q_pico`/`T_R_m3`
   foram medidos (talvez a medição seja de um posto/seção menor dentro da bacia, não no exutório
   final mapeado) — vale confirmar com a fonte original dos dados de vazão.

## 3.3. Solução final: Hidrograma Unitário Triangular do SCS

Você apontou (com razão) que ponderar por flow accumulation pixel a pixel não resolve o problema
do Método Racional sozinho — e de fato não resolve: flow accumulation só dá **área**, não
**tempo**. O Método Racional superestima porque assume que a bacia inteira contribui
simultaneamente no pico; numa bacia de 138 km² isso é fisicamente irreal (tempo de concentração
de várias horas). A correção certa é trazer o tempo de concentração para dentro da conta, o que
o Hidrograma Unitário do SCS faz.

**Área oficial da bacia:** você confirmou 138 km² (o flow accumulation deu ~109,79 km² no
exutório — cerca de 20% a menos, provavelmente por imprecisão da máscara/MDE em relação ao
divisor de águas real; usei os 138 km² informados por você para o cálculo abaixo).

**Comprimento do curso d'água principal (L):** a tentativa de obter isso via
`sagang:flowpathlength` no MDE "remendo_fillsinks" (usado no flow accumulation) deu um valor
absurdo (522 m — pequeno demais pra uma bacia desse tamanho), sinal de que esse MDE específico
tem problemas de direção de fluxo mesmo com a acumulação de área batendo certo. Contornei isso
calculando o comprimento diretamente da rede de drenagem digitalizada (`drenagem.shp`, 911
segmentos): montei um grafo (nós = extremidades dos segmentos, arestas = comprimento de cada
segmento) com a biblioteca `networkx`, e calculei a maior distância, ao longo da rede, entre o
exutório e qualquer outro ponto da rede (`Scripts/spatialPeakFlowHU.py`, função
`comprimento_curso_principal`). Resultado: **L = 37,587 km** (bem mais plausível).

**Parâmetros calculados** (elevações lidas do `MDE 30m.tif`):

| Parâmetro | Valor |
|---|---|
| L (comprimento do curso principal) | 37,587 km |
| H exutório | 741,18 m |
| H cabeceira (ponto mais distante) | 1.187,18 m |
| ΔH | 446,00 m |
| S (declividade média) | 0,01187 m/m |
| Tc (Kirpich, forma SI/Tucci) | 5,966 h (358 min) |
| Tp (tempo de pico, HU-SCS: Tp = 0,667·Tc) | 3,979 h |
| qp unitário (HU-SCS: qp = 2,08·A/Tp) | 72,132 m³/s por cm de escoamento direto |

**Cálculo por evento:** reaproveitei os `Qvol{n}_CN{1,2,3}.tif` já existentes (volume total de
escoamento direto por evento/cenário), convertidos em lâmina média sobre os 138 km² oficiais, e
apliquei `Qp = qp_unitário × lâmina (cm)`. Script:
[Scripts/spatialPeakFlowHU.py](Scripts/spatialPeakFlowHU.py). Resultado salvo em
[Dados Iniciais/comparacao_qpico_HU-SCS_medido_vs_calculado.csv](Dados%20Iniciais/comparacao_qpico_HU-SCS_medido_vs_calculado.csv).

| Cenário | erro médio | erro médio absoluto | desvio-padrão |
|---|---|---|---|
| CN-1 (seco) | +103,1% | 171,3% | 237,6% |
| CN-2 (normal) | +552,0% | 559,0% | 574,3% |
| CN-3 (úmido) | +1.118,1% | 1.118,1% | 851,2% |

**Isso é uma melhora enorme em relação ao Método Racional** (que dava erro médio de 1.656% a
4.295%) — e, mais importante, **o padrão de erro que sobra agora é essencially o mesmo já visto
na calibração do volume** (seção 2): CN-1 fica mais perto (ainda que superestime, ao contrário do
volume que subestimava — o sinal muda porque agora depende também da fração de eventos onde o
CN-1 já subestimava menos), e CN-2/CN-3 superestimam bastante, na mesma direção e proporção geral
do erro de volume. Isso faz sentido: `qp_unitário` é uma constante física fixa (não depende do
CN), então **todo o erro que sobra em Qp vem exclusivamente do mesmo problema de calibração do
CN-SCS já diagnosticado** — não há mais erro estrutural do método de transformação
chuva-vazão-pico. Ou seja: as recomendações de calibração da seção 2 (escolher CN por evento via
`Ap5_pond_mm`, testar λ = 0,05) devem melhorar o Qp calculado na mesma proporção que melhorarem o
volume calculado — não precisa de uma calibração separada para o Qp.

## 3.4. Calibração final do volume: CN-1 + λ = 0,05

Testei diretamente (em vez de tentar selecionar CN por evento via chuva antecedente — ver
seção 3.5) trocar a razão de abstração inicial λ = Ia/S de 0,2 para 0,05, usando sempre o cenário
CN-1 (seco). Resultado nos 17 eventos:

| λ | erro médio | erro médio absoluto | desvio-padrão |
|---|---|---|---|
| 0,2 (original) | -62,6% | 62,6% | 32,0% |
| **0,05 (adotado)** | **+0,5%** | **47,4%** | 57,2% |

O viés sistemático praticamente desaparece. **Implementado em
[Scripts/spatialRain.py](Scripts/spatialRain.py)** (constante `LAMBDA = 0.05`, seção de
configuração no topo do arquivo) e já reprocessado para os 17 eventos — os rasters
`Q{n}_CN{1,2,3}.tif` / `Qvol{n}_CN{1,2,3}.tif` em cada pasta `Evento {n}` refletem esse valor.
CN-2 e CN-3 continuam sendo gerados (úteis para discussão de sensibilidade no texto do TCC), mas
**CN-1 é o cenário adotado**. Comparação completa em
[Dados Iniciais/comparacao_volumes_medido_vs_calculado.csv](Dados%20Iniciais/comparacao_volumes_medido_vs_calculado.csv).

## 3.5. Por que não selecionar CN por evento via chuva antecedente

Antes de adotar a solução acima, testei a ideia óbvia (classificar AMC I/II/III por evento via
`Ap5_pond_mm`, limiares clássicos do SCS por estação seca/chuvosa) e vi que ela **não é
confiável nesta bacia**: acerta o cenário empiricamente correto em apenas **41% dos 17 eventos**
(alguns exemplos erram feio — eventos 14 e 16 seriam classificados AMC-III/CN-3, mas CN-1 é o
que realmente bate). Testei correlação de Pearson entre a "posição de CN efetiva" (a posição
contínua entre CN-1/2/3 que reproduziria o volume medido) e todas as janelas de chuva antecedente
disponíveis (`Ap1` a `Ap14`): nenhuma correlação passou de r=0,365. Em contraste, a correlação com
o **tamanho do próprio evento** (`Chuva_evento_mm`) foi de **r=-0,770** — eventos pequenos
"precisam" de CN mais alto pra bater, eventos grandes precisam de CN mais baixo. Essa é a
assinatura clássica de λ alto demais, não de condição de umidade antecedente mal escolhida — e
foi isso que motivou o teste de λ=0,05 acima, com sucesso.

## 3.6. Qp final: convolução horária do HU-SCS (substitui a versão de "pulso único")

Depois de recalibrar o volume (λ=0,05), o Qp calculado com a versão "pulso único" do HU-SCS
(seção 3.3, `Scripts/spatialPeakFlowHU.py`) piorou muito (erro médio subiu de +103% para
+364%). Investigando, a causa é que **os eventos duram de 23h a 149h (média ~72h), enquanto o
tempo de pico da bacia (Tp) é de só ~4h** — tratar o volume inteiro do evento como um pulso único
do tamanho de Tp superestima o pico sempre que a chuva está espalhada por muito mais tempo que a
resposta da bacia, e quanto maior o volume (que agora está mais correto), pior fica essa
distorção.

**Solução:** encontrei `Dados Iniciais/Dados_finais_histereses_corrigido.xlsx`, com série
**horária** de chuva nos 2 postos e vazão medida (21.168 linhas, Nov/2018 em diante) — dado que
não tinha sido usado até então para o Qp. Com isso, implementei a convolução de verdade:
[Scripts/spatialPeakFlowHU_convolucao.py](Scripts/spatialPeakFlowHU_convolucao.py) faz, por
evento:

1. Combina a chuva horária dos 2 postos com um peso `w1` (ajustado por mínimos quadrados sobre
   os 17 eventos para reproduzir `Chuva_evento_mm`: `w1 ≈ 0,307` para o posto DBT5, `0,693` para
   Campo Limpo Paulista).
2. Acumula essa chuva bruta hora a hora e converte em escoamento efetivo acumulado via CN-SCS
   (S médio da bacia no cenário CN-1 = 255,69 mm, λ=0,05 — os mesmos parâmetros calibrados na
   seção 3.4), depois toma o incremento hora a hora (hietograma de chuva efetiva).
3. Convolui esse hietograma com o Hidrograma Unitário Triangular do SCS, recalculado para duração
   unitária de 1h (Tp=4,080h, Tb=10,893h, qp_UH=70,36 m³/s/cm — praticamente o mesmo Tp de antes,
   já que D=1h é próximo do D=0,133·Tc≈0,79h usado originalmente).
4. O pico do hidrograma resultante é o Qp calculado.

Como checagem, o máximo da série horária medida bate **exatamente** com o `Q_pico` da planilha
manual nos 17 eventos — confirma que as duas fontes de dado são consistentes.

**Resultado** (CSV completo em
[Dados Iniciais/comparacao_qpico_convolucao_medido_vs_calculado.csv](Dados%20Iniciais/comparacao_qpico_convolucao_medido_vs_calculado.csv)):

| Método | erro médio | erro médio absoluto | desvio-padrão |
|---|---|---|---|
| Método Racional (descartado, seção 3.2) | +1.656% a +4.295% | idem | muito alto |
| HU-SCS, pulso único (descartado, seção 3.3) | +364% (CN-1) | +373% | 398% |
| **HU-SCS, convolução horária (adotado)** | **+69,4%** | **107,6%** | 117,7% |

Essa é a versão final recomendada para o Qp. O erro que resta (média absoluta ~108%) é da mesma
ordem de grandeza do que já se via no volume (47%) e é atribuível às mesmas limitações já
documentadas (rede de apenas 2 postos pluviométricos, incerteza inerente do método CN-SCS) — não
há mais indício de erro estrutural de método.

## 3.7. Investigação: por que 109,79 km² em vez de 138 km²?

Você suspeitou que faltavam uns 15 pixels perto do exutório no MDE final. Investiguei
(`Scripts/_investigar_saidas.py`) e **não é isso** — mas achei a causa real.

**Descartado:** rasterizei o polígono real da `Máscara Jundiaí.shp` na mesma grade do MDE e
comparei com os pixels válidos do `remendo_fillsinks.sdat` (o MDE final usado no flow
accumulation):
- Polígono rasterizado: 154.284 pixels = **138,86 km²** (bate com os 138 km² oficiais).
- MDE final válido: 154.239 pixels = **138,82 km²** — só 45 pixels (0,04 km²) sem dado, e o mais
  próximo desses fica a **5 km** do exutório. Não é um problema de dado faltando perto do
  exutório.

Testei também se o método de fluxo (Multiple Flow Direction, usado no `flowaccFINAL`) estava
"dispersando" área entre pixels vizinhos ao exutório em vez de concentrar num só — refiz o
flow accumulation com Determinístico 8 (D8, concentra tudo num único caminho) e o resultado foi
praticamente o mesmo (107,92 km² contra 109,79 km² do MFD). Também descartado.

**Causa real: existe um segundo ponto de saída da bacia**, que `drenagem.shp` não mapeia como
cruzando o limite do polígono (por isso a interseção que usei pra achar o exutório só pegou um
ponto). Procurando, ao longo de todo o limite da máscara, por pixels com grande área acumulada
que ficam na borda do polígono, achei:

| Ponto | Localização (SIRGAS 2000 / UTM 23S) | Área acumulada |
|---|---|---|
| Exutório principal (já usado) | X=319.017, Y=7.432.318 | 107,92 km² |
| **2º ponto de saída** | X=336.088, Y=7.429.618 | **27,14 km²** |
| Soma dos dois | | **135,06 km²** |

135 km² já bate muito mais perto dos 138 km² oficiais (a diferença residual, ~3 km², está
espalhada em vazamentos pequenos pela borda). Investigando esse segundo ponto: ele fica a só
**60 m** de um segmento de `drenagem.shp` (ou seja, **há sim um rio mapeado bem ali**), e olhando
a elevação ao redor, é claramente um vale real (854-858 m no fundo, subindo pra 865-915 m nas
bordas) — não é ruído nem erro de MDE. O que acontece é que **o limite do polígono da máscara
passa exatamente em cima desse vale/canal**, em vez de seguir o divisor de águas — então o
algoritmo de fluxo "vê" essa sub-bacia de ~27 km² saindo pela borda ali, em vez de continuar
escoando rio abaixo até o exutório principal.

**Conclusão prática:** o mais provável é que o polígono `Máscara Jundiaí.shp` tenha sido
desenhado cortando essa sub-bacia (~27 km²) para fora, quando na verdade ela deveria estar
incluída (contribuindo pro exutório principal). Isso é uma correção no **traçado do polígono da
máscara**, não no MDE/flow accumulation em si — vale abrir o `Máscara Jundiaí.shp` no QGIS,
conferir o trecho perto de X=336.088/Y=7.429.618 contra o `drenagem.shp` e o hillshade do MDE, e
estender o polígono pra englobar essa sub-bacia (seguindo o divisor de águas real). Depois disso,
reprocessar o flow accumulation deve aproximar a área do exutório dos 138 km² oficiais.

## 3.8. Correção da barreira: 137,80 km² (era 109,79 km²)

Confirmada a causa (estrada canalizando o rio, exatamente como você suspeitou), corrigi
diretamente em vez de só documentar. Script:
[Scripts/_corrigir_barreira_e_reprocessar.py](Scripts/_corrigir_barreira_e_reprocessar.py).

**Método:** em vez de caçar manualmente a célula exata do aterro (tentei — o perfil de elevação
ao longo da rede é naturalmente crescente do exutório até a cabeceira, e o ruído de encaixe
vetor→raster (30 m) mascara qualquer "degrau" isolado nesse nível de detalhe), forcei
matematicamente a consistência hidrológica em toda a rede:

1. Amostrei a elevação em cada um dos 912 nós de `drenagem.shp` (mínimo numa janela 3x3 do
   `carvedDEM`, pra reduzir ruído).
2. Percorri a rede (é uma árvore, uma só componente conexa) a partir do exutório via BFS, e
   forcei: nenhum nó pode ter elevação corrigida menor que a do nó logo a jusante dele
   (`elev_corrigida[nó] = max(elev_crua[nó], elev_corrigida[pai])`). Isso garante um perfil
   monotonicamente decrescente do exutório até qualquer cabeceira — elimina qualquer aterro/
   represamento em qualquer ponto da rede, não só no local que eu tinha identificado.
   **Resultado: 163 dos 912 nós tinham barreiras** (bem mais do que só a do segundo ponto de
   saída — provavelmente outras travessias de estrada menores espalhadas pela bacia).
3. Interpolei essa elevação corrigida ao longo dos vértices de cada segmento e "queimei"
   (rebaixei, por mínimo) 4.829 células do `carvedDEM` com esses valores — sempre no mesmo MDE
   que você já tinha fornecido, sem trocar para uma extensão maior.
4. Rodei fill sinks (Wang & Liu) e flow accumulation (MFD, mesmos parâmetros de antes) nesse DEM
   corrigido.

**Resultado:** área acumulada no exutório principal foi de **109,79 km² para 137,80 km²** —
diferença de só 0,2 km² (0,14%) em relação aos 138 km² oficiais. O segundo ponto de saída deixou
de existir como vazamento de borda; a água que antes "escapava" ali agora segue corretamente até
o exutório principal.

**Arquivos gerados** (em `Dados Iniciais/qp_spatial/`): `carvedDEM_corrigido.tif` (MDE com a
correção de barreiras, antes do fill sinks), `carvedDEM_corrigido_filled.tif` (depois do fill
sinks), `flowacc_corrigido.tif` (flow accumulation final, MFD) — **este é o raster de área de
contribuição recomendado para qualquer uso futuro** (mapas, HU-SCS espacializado por pixel, etc.),
substituindo `flowaccFINAL.sdat`.

**Nota:** o cálculo de Tc/Tp usado no Qp final (seção 3.6) já usava o comprimento do curso
d'água calculado diretamente da rede vetorial (`drenagem.shp`, via grafo), não do flow
accumulation — então essa correção **não muda** o Tc/Tp/qp_unitário já calculados. O que ela
resolve é a própria área de drenagem (que já foi usada como 138 km² "oficiais" desde o início,
por indicação sua) e deixa o raster de flow accumulation coerente com esse valor, útil para
qualquer análise espacial futura (ex. se quiser gerar um raster de Qp por pixel de verdade, em
vez do valor único no exutório).

## 3.9. Tentativa de calibração adicional: existe um teto real

Depois de fechar CN-1 + λ=0,05 (seção 3.4), os erros por evento ainda ficaram grandes (47% de
erro absoluto médio no volume). Antes de aceitar isso como definitivo, testei se dava pra
calibrar melhor ainda usando só os dados que já temos.

**Teste:** resolvi numericamente (`Scripts/_calibrar_lambda_por_evento.py`, busca de raiz com
`scipy.optimize.brentq`), para cada um dos 17 eventos, qual valor de λ (mantendo CN-1/S-Seco
fixo) reproduziria exatamente o `T_R_m3` medido.

**Resultado:**
- **12 de 17 eventos** têm um λ ótimo dentro de uma faixa fisicamente razoável (0 a 0,6), mas
  esse λ ótimo varia de **0,009 a 0,198** evento a evento — não converge para um valor único.
- **5 de 17 eventos (1, 2, 4, 7, 10) não têm solução alguma**: mesmo com λ→0 (o máximo de
  escoamento que o CN-1 consegue gerar para aquele evento), o volume calculado ainda fica abaixo
  do medido. Ou seja, para esses eventos o problema não é o valor de λ — é que o próprio CN-1
  (a capacidade de retenção S que ele assume) está systematicamente alto demais.
- Existe uma correlação real entre o λ ótimo e o tamanho do evento (r=0,57, mesma direção do
  padrão já visto na seção 2/3.4: eventos maiores precisam de λ maior). Mas um ajuste log-log
  simples (`λ = 0,0046 · Chuva_evento_mm^0,6424`) erra de -54% a +636% evento a evento — não é
  uma relação limpa o suficiente para virar uma regra de calibração confiável.

**Conclusão:** o teto observado (~47-108% de erro absoluto médio) não é falta de esforço de
calibração — é que **um único parâmetro escalar (CN ou λ) não é suficiente para explicar a
variabilidade evento a evento** presente nos dados. Isso é consistente com a rede de **apenas 2
postos pluviométricos** alimentando o IDW: a fórmula do CN-SCS é quadrática na lâmina de chuva,
então um erro espacial na chuva estimada se amplifica no escoamento calculado de um jeito que
nenhum ajuste de CN/λ compensa de forma sistemática e confiável.

### Dados adicionais que mais ajudariam (em ordem de impacto esperado)

1. **Mais postos pluviométricos na bacia** (ANA/CEMADEN/DAEE costumam ter estações telemétricas
   na região) — mesmo que só para alguns dos 17 eventos, ajudaria a confirmar se o problema é
   mesmo a interpolação de 2 pontos.
2. **Produto de chuva por satélite ou radar** (IMERG/GPM, CHIRPS, ou radar do IPMet-Unesp se
   cobrir a região) como comparação/complemento aos 2 postos.
3. **Curva-chave (rating curve) da estação de vazão** — conferir se foi calibrada até vazões
   próximas das de pico observadas ou se está extrapolando bastante; isso pode explicar parte do
   "erro" como incerteza de medição, não erro de modelo.
4. **Mapa de uso do solo/tipo de solo mais recente ou detalhado**, se o `CN TCC.tif` atual for de
   fonte antiga ou resolução grossa — para refinar o CN em si, não só o λ.

## 3.10. Refinamento do Qp: separando o efeito do Tc do efeito de escala

Depois de fechar a seção 3.9, o usuário perguntou se o Qp usa o Q calculado (que já tem erro
próprio) — e sim, usa: o hietograma de chuva efetiva vem do mesmo CN-SCS (mesmo S, mesmo λ=0,05)
usado no volume. Verificamos que a correlação entre erro do volume e erro do Qp é **r=0,80** —
confirma que o Qp herda a maior parte do erro do volume, mas não 100% (o Qp muitas vezes erra
*mais* que o volume no mesmo evento, ex. evento 13: volume +75% / Qp +291%).

### Teste 1: usar o volume medido em vez do calculado (isolar o efeito da "forma")

Reescalamos o hietograma de chuva efetiva pra bater exatamente com o volume medido (T_R_m3),
mantendo a mesma forma temporal que o modelo já calcula. Resultado: o erro **piorou**, de +69,4%
para +149,4%. Ou seja, o volume errado do modelo estava **mascarando** um viés de superestimação
já presente no mecanismo de gerar o pico — a recalibração do volume (λ=0,2→0,05, seção 3.4) só
parecia ter funcionado bem pro Qp (seção 3.6) porque o volume subestimado compensava esse viés
escondido.

### Investigação da causa: rajadas horárias extremas

Inspecionamos o hietograma de chuva efetiva hora a hora (`Q_incremental`) nos eventos com pior
erro. Achado no evento 3: na hora 43, uma rajada de **36,85 mm numa hora só** — como a chuva
acumulada já tinha passado do limiar (λS=12,78mm), o CN-SCS converteu quase tudo isso (7,90 dos
8,98 mm do evento inteiro, **88%**) em escoamento efetivo numa única hora. Isso é um artefato de
aplicar a fórmula do CN-SCS (feita pra totais de tempestade) ponto a ponto numa série horária
real com rajadas abruptas — gera picos sintéticos de chuva efetiva mais afiados do que a resposta
real da bacia produziria.

### Teste 2: Tc alternativos e suavização do hietograma

Testamos, usando o volume medido pra isolar o efeito (metodologia do Teste 1):

| Configuração | erro médio | erro absoluto médio |
|---|---|---|
| Tc Kirpich (5,966h), sem suavização | +149,4% | 154,0% |
| Tc Kirpich, suavização 24h (média móvel) | +53,9% | 66,3% |
| Tc Giandotti (10,652h), sem suavização | +65,1% | 76,6% |
| Tc Ven Te Chow (6,744h), sem suavização | +124,6% | 130,9% |
| **Tc calibrado ≈ 21-23h, sem suavização** | **~0%** | **~30%** |

Aumentar o Tc (isoladamente, sem suavizar) reduzia o erro tanto quanto suavizar — o que sugeriu
inicialmente que "Tc estava subestimado". Isso levou à primeira versão adotada (Tc=21h) que dava,
com o **volume do modelo** (não mais o medido), erro médio -29,9% e erro absoluto 47,6% — já uma
melhora grande sobre a versão anterior (+69,4%/108%).

### A pergunta certa do usuário: por que não um fator de calibração em vez de mexer no Tc?

Essa pergunta revelou o mecanismo real. Testamos separar explicitamente dois efeitos:
- **Tc/Tb**: controla a forma/espalhamento temporal da convolução.
- **Fator de pico (α)**: um fator de escala aplicado sobre o Qp calculado.

Otimizando α para minimizar o erro absoluto médio, **para cada Tc entre 6h e 50h**, o erro
absoluto médio resultante ficou quase constante: **45,4% a 47,0%**, não importa o Tc escolhido.
Isso mostra que a "melhora" observada ao aumentar o Tc antes era só uma correção de escala
disfarçada (Tc entra na fórmula do HU-SCS como `qp_UH = FATOR_PICO·A/Tp`, ou seja, aumentar Tc
*é* reduzir a escala) — **não é uma melhora real de forma/tempo**. O Tc, isoladamente, não reduz
a dispersão evento a evento.

**Conclusão importante:** uma vez que a escala é corrigida à parte, o piso de erro real do
método (~45-46% de erro absoluto médio) é quase igual ao piso já visto no volume (47,4%,
seção 3.4) — ou seja, **o mecanismo de conversão volume→pico não está mais adicionando erro
extra além do que já vem do volume**, que é o resultado esperado e desejado.

### Parâmetros finais adotados

- **Tc pela fórmula de Giandotti** (mais adequada que Kirpich para bacias médias/grandes mistas
  no Brasil — Kirpich foi desenvolvida para bacias agrícolas pequenas):
  $$T_c = \frac{4\sqrt{A} + 1{,}5L}{0{,}8\sqrt{H_m}} = 10{,}652 \text{ h}$$
  com A=138 km², L=37,587 km, Hm = altitude média da bacia (888,3 m) − altitude do exutório
  (741,2 m) = 147,1 m.
- **Fator de pico do HU-SCS recalibrado**: o padrão do SCS é 2,08 (equivalente ao PRF=484 em
  unidades imperiais), derivado de bacias americanas com uma forma de hidrograma específica. É
  documentado na literatura de hidrologia que bacias mais planas/com mais atenuação (várzeas,
  uso do solo misto) precisam de um fator de pico reduzido — alguns manuais citam PRF tão baixo
  quanto 100-300 (ou seja, 0,2-0,62 do padrão). Calibramos esse fator contra os 17 eventos
  (minimizando o erro percentual absoluto médio, Tc fixo em Giandotti):
  **fator calibrado = 2,08 × 0,5377 = 1,1184** — dentro da faixa documentada, e consistente com a
  baixa declividade média desta bacia (0,0119 m/m).

**Implementado em `Scripts/spatialPeakFlowHU_convolucao.py`** (constantes `Tc_h = 10.652` e
`FATOR_PICO = 2.08 * 0.5377`).

### Resultado final

| Evento | Qp medido (m³/s) | Qp calculado (m³/s) | erro (%) |
|---|---|---|---|
| 1 | 10,29 | 0,89 | -91,4% |
| 2 | 30,39 | 9,40 | -69,1% |
| 3 | 16,56 | 17,91 | +8,2% |
| 4 | 17,03 | 4,14 | -75,7% |
| 5 | 22,09 | 9,78 | -55,7% |
| 6 | 14,69 | 3,38 | -77,0% |
| 7 | 16,42 | 3,47 | -78,9% |
| 8 | 20,39 | 12,33 | -39,6% |
| 9 | 11,79 | 10,91 | -7,5% |
| 10 | 10,62 | 1,30 | -87,8% |
| 11 | 20,95 | 16,51 | -21,2% |
| 12 | 13,15 | 0,97 | -92,6% |
| 13 | 16,01 | 21,74 | +35,8% |
| 14 | 22,26 | 23,55 | +5,8% |
| 15 | 28,37 | 32,58 | +14,8% |
| 16 | 23,11 | 23,11 | 0,0% |
| 17 | 21,36 | 17,02 | -20,3% |

**Erro médio: -38,4% | Erro absoluto médio: 46,0% | Desvio-padrão: 42,9%**

Note que este resultado tem um viés sistemático de subestimação (-38,4%), diferente da versão
anterior (Tc=21h ad hoc, seção anterior) que tinha viés de -29,9% com erro absoluto ligeiramente
melhor (47,6%, mas isso porque o α não estava calibrado corretamente naquela versão — usamos
"Tc alto" fazendo o papel de escala de forma menos precisa). Do ponto de vista de erro absoluto
médio os dois são equivalentes (~46-48%); a diferença é que a versão com Giandotti+fator de pico
calibrado é **metodologicamente mais defensável** (Tc de uma fórmula reconhecida, fator de pico
calibrado com respaldo na literatura), enquanto a versão anterior tinha um Tc escolhido sem
justificativa física clara (só "porque deu o menor erro").

**Se for importante não subestimar sistematicamente** (ex. para fins de dimensionamento/segurança
contra cheias), é possível recalibrar o fator de pico para zerar o viés médio em vez de minimizar
o erro absoluto — isso aumentaria o erro absoluto médio para algo entre 55-65% (testado na seção
anterior). Essa é uma escolha de critério que vale alinhar com o orientador antes de finalizar o
texto do TCC.

## 4. Status e próximos passos

Feito nesta sessão:
- [x] Diagnóstico do erro de volume (Q) com números reais (seção 2).
- [x] Localização do exutório real da bacia (seção 3.2, `Scripts/_find_outlet.py`).
- [x] Método Racional implementado e testado (`Scripts/spatialPeakFlow.py`) — descartado por
      inadequação de escala (erro 1.656%-4.295%).
- [x] Testada seleção de CN por evento via chuva antecedente — descartada, só 41% de acerto e
      correlação fraca (seção 3.5).
- [x] Calibração do volume: CN-1 + λ=0,05 adotados, erro médio de -62,6% para +0,5% (seção 3.4).
      Já implementado em `Scripts/spatialRain.py` e reprocessado para os 17 eventos.
- [x] Hidrograma Unitário Triangular do SCS (pulso único) implementado e testado — funcionou bem
      com λ=0,2 mas piorou muito com λ=0,05 (eventos duram muito mais que o Tp da bacia).
- [x] Qp final: convolução horária do HU-SCS com o hietograma real (`Scripts/spatialPeakFlowHU_convolucao.py`),
      usando a série horária de `Dados_finais_histereses_corrigido.xlsx` — erro médio caiu para
      +69,4% (médio absoluto 107,6%), seção 3.6. Esta é a versão recomendada.

Ainda em aberto (a fazer, dependendo de quanto tempo resta pro TCC):
- [x] Investigada e corrigida a diferença entre 138 km² oficiais e 109,79 km² do flow
      accumulation (seções 3.7/3.8) — causa: estrada canalizando o rio em pelo menos um ponto
      (confirmado por você), com o MDE não capturando o canal ali. Corrigido forçando um perfil
      monotonicamente decrescente ao longo de toda `drenagem.shp` (163 nós corrigidos) e
      reprocessando fill sinks + flow accumulation. Resultado final: **137,80 km²** (era 109,79).
- [x] Investigado se dá pra calibrar melhor que CN-1+λ=0,05 fixos (seção 3.9) — não com um único
      parâmetro escalar; o teto de erro (~47-108%) reflete principalmente a limitação de só 2
      postos pluviométricos, não falta de esforço de calibração. Lista de dados adicionais que
      ajudariam registrada na seção 3.9.
- [ ] O peso w1=0,307/0,693 entre os postos foi ajustado por mínimos quadrados sobre o total dos
      17 eventos (não é um peso "fisico" tipo Thiessen) — se quiser, dá pra comparar com um peso
      Thiessen calculado a partir da geometria real dos polígonos de influência dos 2 postos.
- [ ] Se conseguir mais postos pluviométricos ou um produto de chuva por satélite/radar (seção
      3.9), reprocessar `spatialRain.py` com a chuva espacial melhorada e comparar o novo erro
      contra a tabela desta nota.
- [ ] Conferir a curva-chave (rating curve) da estação de vazão — se a incerteza de medição em
      vazões de pico explica parte do erro que sobra.
- [x] Investigado e recalibrado o mecanismo de conversão volume→pico do Qp (seção 3.10) — Tc
      pela fórmula de Giandotti + fator de pico do HU-SCS recalibrado (2,08→1,1184, dentro da
      faixa documentada na literatura para bacias atenuadas). Erro final: médio -38,4%,
      absoluto médio 46,0% — praticamente igual ao piso já visto no volume (47,4%).
- [ ] Decisão pendente com o orientador: manter o fator de pico calibrado para menor erro
      absoluto (viés -38,4%) ou recalibrar para viés ~0% (erro absoluto sobe pra ~55-65%) — é
      uma escolha de critério (ajuste geral x não subestimar sistematicamente picos de cheia),
      não uma questão técnica.
