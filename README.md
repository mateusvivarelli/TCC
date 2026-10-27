# README — Status do TCC (espacialização da MUSLE)

## Sincronização entre dispositivos (git + Google Drive)

Este projeto vive em dois canais, por causa do tamanho dos rasters:

- **Git (GitHub privado, https://github.com/mateusvivarelli/TCC)**: código (`Scripts/`),
  documentação (`Notas Claude/`, este README), planilha de resultados, shapefiles e PDFs de
  referência. `.gitignore` exclui `*.tif`/`*.sdat` (rasters) e `.claude/` (estado local).
- **Google Drive**: as pastas `Dados Iniciais/` e `Evento 1` a `Evento 17` (rasters, ~3GB) moram
  fisicamente em `G:\Meu Drive\TCC_Dados\` (conta Google do usuário) e são acessadas de dentro de
  `C:\TCC` via **junction NTFS** (não são cópias — o conteúdo real está só no Drive, o
  `C:\TCC\Dados Iniciais` é um atalho especial do Windows que aponta pra lá). Isso existe porque os
  scripts têm caminhos fixos tipo `r"C:/TCC/Dados Iniciais"` — a junction deixa isso funcionar sem
  precisar editar nenhum script.

### Instruções pra configurar um PC novo (ex.: notebook) — pode ser seguido por outra instância do Claude Code

1. Confirmar que o Google Drive for Desktop está instalado e logado com a mesma conta, e que
   `TCC_Dados` (dentro de "Meu Drive") já sincronizou (~3GB — pode levar um tempo na primeira vez).
   Descobrir a letra de unidade do Google Drive nesse PC (pode não ser `G:`):
   ```powershell
   Get-PSDrive -PSProvider FileSystem | Select-Object Name, Root
   ```
   Procurar a pasta `Meu Drive\TCC_Dados` dentro da unidade encontrada.
2. `git clone https://github.com/mateusvivarelli/TCC.git "C:\TCC"` (ou outro caminho — mas se for
   outro caminho, os scripts em `Scripts/*.py` que têm `BASE = r"C:\TCC"` fixo vão precisar ser
   ajustados; mais simples manter `C:\TCC`).
3. Recriar as junctions (ajustar a letra de unidade `G:` se for diferente nesse PC):
   ```powershell
   $drive = "G:\Meu Drive\TCC_Dados"   # ajustar se a letra for outra
   cmd /c mklink /J "C:\TCC\Dados Iniciais" "$drive\Dados Iniciais"
   1..17 | ForEach-Object {
       cmd /c mklink /J "C:\TCC\Evento $_" "$drive\Evento $_"
   }
   ```
4. Instalar o QGIS 3.44 (mesma versão, se possível) — os scripts chamam caminhos fixos como
   `C:\Program Files\QGIS 3.44.14\bin\python-qgis-ltr.bat` e `qgis_process-qgis-ltr.bat`. Se a
   versão instalada for outra, tem que ajustar esses caminhos nos scripts (`grep -rn "QGIS 3.44"
   Scripts/` pra achar todas as ocorrências). **Nota (17/09/2026):** num PC com QGIS 3.42.1 (bat
   quebrado — pega o Python errado de outra instalação) e QGIS 4.2.1 (funciona, mas **não tem o
   provider `sagang`/SAGA** — só `gdal` e `qgis` nativos), os scripts que dependiam de
   `sagang:catchmentarea` (`calcular_fci_por_evento.py`) foram adaptados pra calcular a média de
   montante em Python puro (função `calcula_upslope_mean`, acumulação topológica sobre a mesma
   rede D8 já usada no resto do script) — não depende mais do SAGA. Os rasters fixos
   (`K_mean_upslope.tif`, `C_mean_upslope.tif`, `slope_mean_upslope_pct.tif`, calculados
   originalmente via SAGA MFD) são reaproveitados do disco se já existirem.
5. Conferir que `python-qgis-ltr.bat` (ou `python-qgis.bat` na versão instalada) tem `pdfplumber`,
   `pandas`, `scipy`, `openpyxl` instalados (mesmos pacotes usados nas sessões anteriores).
6. Ler este README e todo o conteúdo de `Notas Claude/` antes de continuar qualquer trabalho — é
   isso que dá o contexto completo do projeto, não alguma sincronização automática de memória
   entre instâncias do Claude Code (essa memória é local a cada máquina).
7. Depois de trabalhar em qualquer um dos dois PCs: `git add`/`commit`/`push` as mudanças de
   código/notas (o Google Drive sincroniza os rasters sozinho, por fora do git).

Ponto de partida pra retomar o trabalho. Detalhes completos em
[Notas Claude/notas_qgis_calibracao_qp.md](Notas%20Claude/notas_qgis_calibracao_qp.md) (Fase 1 —
calibração de Q e Qp) e [Notas Claude/notas_musle_espacializada.md](Notas%20Claude/notas_musle_espacializada.md)
(Fase 2 — MUSLE espacializada, concluída).

## Apostila explicativa (02/10/2026)

`Apostila_TCC_Do_dado_ao_mapa.pdf` (raiz do repositório, 42 páginas) explica todos os passos, métodos, fontes e a espacialização,
para quem não tem formação em hidrologia. A revisão que a acompanhou gerou correções nas notas: ver a seção 14 de
`Notas Claude/notas_musle_espacializada.md` e os ajustes em `Notas Claude/base_para_redacao_tcc.md` (comparação com Hao e
Baert, autoria de Valle Junior et al.). Pontos ainda a confirmar estão no Apêndice D da apostila.

## Atualização 27/10/2026

- **Vazão de base: método confirmado** — filtro de Eckhardt (2005), α = 0,995 e BFImax = 0,70, calibrado segundo
  Collischonn e Fan (2013). A série do orientador é a mesma Bt que usamos; nada muda nos resultados. O cabeçalho da
  planilha diz BFImax = 0,58, mas a série só bate com 0,70: confirmar com o orientador. Ver notas §28.
- **Sugestões de redação do orientador** (introdução, justificativa, fundamentação, MUSLE no SWAT e no Brasil) e textos
  sugeridos: `Notas Claude/mudancas_docs_sem_base_26-10.md`, parte "Atualização de 27/10/2026".
- Tabela 5 separada em K e C: `TCC_Texto/tabelas/tab_fator_K.md` e `tab_fator_C.md`.

## Onde estamos agora (26/10/2026) — VAZÃO DE BASE REMOVIDA (ler primeiro)

**Decisão com o orientador:** λ = 0,20 e **sem termo de vazão de base**. A MUSLE usa só o escoamento direto
(calculado: SCS-CN; forçado: escoamento direto medido = T_R − ΣBt). **Modelo adotado: `Scripts/calcular_sy_so_direto.py`**
(saídas `*_sd.tif`, `comparacao_SY_so_direto.csv`). Dados, tabelas, figuras, mapas e planilha já foram refeitos.

**Resultados (LOO, carga total):** MC 98% de erro mediano / 24% em fator 2 (abaixo de SY = c·chuva: 42% / 82%);
MFM 39% / 94% (abaixo da IC: 16% / 100%; empata no NSE linear). Detalhes em `notas_musle_espacializada.md` §27.

**PENDENTE (o usuário faz no Google Doc):** reescrever resumo, §4.1, §4.5–4.7, §4.9, §5.2–5.5, tabelas 8–13 e conclusões
— lista completa, seção por seção, com textos sugeridos em **`Notas Claude/mudancas_docs_sem_base_26-10.md`**.
Atenção: duas conclusões mudam (o MC fica abaixo da regra da chuva; o MFM deixa de empatar com a IC na régua em log).

## Onde estamos agora (17/10/2026) — PONTO DE RETOMADA (ler primeiro)

**A fonte da verdade do texto é o Google Doc "TCC arquivo"**
(id `12xwNDLmeeRB6IcbsprDWuI3XHx_At2RIgsPm6WBKiGo`), não o `TCC_rascunho_04.md` — os dois
divergiram. Para editar o Doc pelo Claude: conector Google Docs (`read_doc`/`update_doc`); o
`read_doc` estoura o limite e salva o JSON em `~/.claude/projects/.../tool-results/` — parsear com
Python. `replaceAllText` só bate dentro de um mesmo trecho de texto; para trechos com comentário
ancorado ou formatação mista, usar edição por índice (de trás para frente, com
`writeControl.requiredRevisionId`). Comentários: `insertComment` com o campo `content`.

**Feito nesta sessão (17/10), tudo já aplicado no Doc:**
- Epígrafe trocada para a versão em português (Flanagan, *Halt em Perigo*, Fundamento, 2011) e
  formatada (recuo 8 cm, 10 pt, título em itálico). Falta conferir a fala no livro.
- **Seção 3.3 conferida contra os rasters**: grade, pixel, SRC, K, C e a Tabela 5 inteira batem.
  Corrigidos os valores que vinham do LS antigo: LS médio 0,536 → **7,80**; pixels de cálculo
  154,0 mil → **153,9 mil**; 138,2 → **138,1 km²**; bordas ~650 → **~810 pixels**. Célula do LS na
  Tabela 4 reescrita (o LS não é "no SAGA"; é Python sobre o MDE corrigido, Moore e Burch, 1986).
- **Origem do CN resolvida**: `CN TCC.tif` = raster **BR_CN-2022 da ANA** (Curva Número na Base
  Ottocodificada), reprojetado para UTM 23S — 100% idêntico no interior das manchas, mesmos 20
  valores. Uso do MapBiomas 2022 + solo IBGE + grupos hidrológicos de Sartori et al. (2005).
  AMC I/III = conversões de Chow et al. (1988), conferidas. Parágrafo de procedência inserido no Doc
  (no lugar do antigo [PENDENTE]), com a limitação: CN usa MapBiomas 2022, K/C usam Plano de Bacias
  2020. Ver `notas_musle_espacializada.md` §25.
- **Referências consolidadas** em ordem alfabética, com DOI: `Notas Claude/referencias_consolidadas.md`
  (✔ = citada no Doc). Lista de itens a conferir no fim do arquivo.
- Equação do IDW dada ao usuário na forma de fração única, mais fácil de digitar no editor do Docs:
  P(x) = (P₁·d₂² + P₂·d₁²) / (d₁² + d₂²). Colar LaTeX no Docs **não funciona**; ou se digita no
  editor (`\frac` + espaço, `_`, `^`, setas) ou se cola a linha Unicode.

**Atualização 26/10/2026:** o orientador revisou e teve dúvidas sobre (1) a origem da vazão de base e (2) por que o termo de base carrega ~91% do sedimento no modelo de dois componentes. Respostas e sugestão de reformulação do texto ("termo de escala do evento") em `notas_musle_espacializada.md` §26.

**Pendências abertas (em ordem de prioridade):**
1. ~~**Perguntar ao orientador** como foi separada a vazão de base~~ (RESOLVIDO em 27/10: Eckhardt) (coluna `Bt`) — método não
   documentado; os filtros de Lyne-Hollick e Eckhardt não reproduzem a série (ver
   `dados_area_estudo_plano_bacias.md` §9–11). O usuário apagou do Doc a frase que eu tinha escrito
   sobre isso; não recolocar sem ele pedir.
2. **§2.4 do Doc**: "(Murillo-Bermúdez et al., 2022)" sobre curvas turbidez→CSS provavelmente deveria
   ser o artigo do IJRBM (2021 on-line / 2023 fascículo). Não alterado — decisão do usuário.
3. **§2.6 do Doc** ainda diz "O número de curva resulta do cruzamento dos mapas de uso e de solo" —
   sugerido trocar por "obtido da base nacional da ANA, que cruza uso da terra e grupo hidrológico".
4. Falta inserir no Doc a tabela de resultados (`TCC_Texto/tabelas/tab_resultados.md`, já com o LS
   novo). O usuário começou a escrever a seção 4 (Metodologia) no Doc.
5. Decisões da migração do LS ainda sem resposta do usuário: (a) aceitar os 156 pixels de borda
   perdidos; (b) Apêndice D / `teste_cn_calibrado.md` com colunas de sedimento no LS antigo (scripts
   do revisor fora do repo); (c) linha congelada λ = 0,05 (`SY_medio_eventos.tif`, FCI) ainda no LS
   antigo, enquanto `E_unit{n}.tif` já foi regenerado.
6. Conferir a fonte da epígrafe no livro e se a norma da FEC exige a epígrafe nas referências.

**Ambiente (este PC):** o Python padrão não tem GDAL. Rodar scripts com GDAL pelo ambiente do QGIS:
`call "C:\Program Files\QGIS 3.44.14\bin\o4w_env.bat"` e depois `"%PYTHONHOME%\python.exe" script.py`
(um `.bat` wrapper resolve). No notebook, conferir o caminho do QGIS.

## Onde estamos agora (16/10/2026) — fator LS recalculado e projeto migrado

O fator LS herdado da IC (`Dados Iniciais/LS_raster.tif`, derivado de `LS Alto.tif`) estava
**defeituoso**: foi calculado sobre o MDE em WGS 84 **geográfico** (pixel em graus), o que corrompe
os termos de declividade e de área. Conferência de 16/10/2026: correlação LS × declividade de
**0,047** (0,148 em log), LS praticamente constante (~0,5) em todas as faixas de declividade, de
0–2% a 70–200%, e expoentes ajustados de 0,13/0,13 contra os 0,4/1,3 de Moore. A declividade foi
confirmada correta (recálculo independente a partir do MDE, correlação 1,0000).

**LS adotado: `Dados Iniciais/LS_moore.tif`** — Moore e Burch (1986) / Moore et al. (1991) sobre o
MDE corrigido em UTM, LS = (As/22,13)^0,4 · (sen β/0,0896)^1,3, com a área de contribuição
específica As limitada a 200 m (comprimento de rampa máximo). Média 7,80 (o antigo era 0,537),
correlação com a declividade **0,943**. Script: `Scripts/_recalcular_ls_moore.py`. Existe também
`LS_moore_sem_limite.tif`, **só referência — não usar**. `LS_raster.tif` foi mantido para comparação.

Todos os scripts de resultado adotado foram migrados para o LS novo e re-executados (ver seção 24
de `Notas Claude/notas_musle_espacializada.md`). Efeito: **o desempenho agregado quase não muda**
(o LS entra linearmente e o `c` absorve a escala), mas **o mapa muda muito** — só 56,9% dos hot
spots coincidem com o mapa anterior e a correlação do mapa com K·C·LS sobe de 0,569 para 0,880.
A hidrologia (volume, λ = 0,20, CN-I, kb) e os testes sem MUSLE não mudaram.

## Onde estamos agora (15/10/2026) — modelo com vazão de base

- **Achado:** `T_R_m3` = Σ Q·3600 (volume total, inclui vazão de base, 34–55%) e `SYY_t` = Σ Q·CSS·3600 (carga total). O SCS-CN calcula só escoamento direto. Ver seções 15–17 de `Notas Claude/notas_musle_espacializada.md`.
- **Modelo atual a adotar:** `Scripts/calcular_sy_com_base.py` — Q = Q_direto (SCS-CN, CN-I, λ = 0,20) + vazão de base prevista (kb·Qb_inicio·duração). Saídas `*_vb.tif` e `Dados Iniciais/comparacao_SY_modelo_com_base.csv`. SY previsão pura: NSE 0,50 (in-sample) / 0,380 (LOO aninhado); volume total NSE 0,58. (Números já com o LS novo, `c` = 0,010216; ver a seção de 16/10/2026 acima.)
- **Revisões independentes:** `Notas Claude/revisao_independente.md` (rodada 1) e `revisao_independente_modelo_com_base.md` (rodada 2, ao ser concluída).
- **Rascunho do TCC:** `TCC_Texto/TCC_rascunho_01.md/.docx` (formato Informação CCPG 004/2017); gerador `Scripts/md_para_docx.py`.
- **Auditoria do evento 11:** `Evento11_Auditoria/` (planilha 01 pronta; planilha 02 com erro de abertura no Excel, pendente).

## Onde estamos agora (21/09/2026) — versão com volume observado como restrição

Diagnóstico completo das fontes de erro (seção 12 das notas) mostrou que o erro do SY é quase
todo herdado do volume do CN-SCS, não da estrutura espacial nem da MUSLE. Três tentativas de
melhorar o volume de forma preditiva falharam com evidência (λ por evento: 5 de 17 eventos são
impossíveis; λ(chuva): piora em validação cruzada; classificação AMC padrão: piora muito).

**Implementado (seção 13 das notas):** versão com o volume medido usado como restrição do raster
de Q — `Scripts/calcular_sy_volume_restrito.py`, saídas com sufixo `_obs`.

| Métrica | Previsão pura | **Volume restrito** |
|---|---|---|
| NSE (leave-one-out) | 0,2816 | **0,7759** |
| WIA | 0,8683 | **0,9462** |
| PBIAS | -21,3% | **-1,0%** |
| Erro absoluto médio | 46,1% | **27,8%** |

Supera o patamar de Hao et al. (2022) (NSE > 0,70, WIA > 0,89). O mapa de hot spots praticamente
não muda entre as duas versões (r=0,994; 96,9% dos hot spots coincidem) — resultado de robustez.

Figura: `Figuras/comparacao_previsao_vs_volume_restrito.png`.

**Pendências de texto:** reportar o NSE leave-one-out (não só in-sample); deixar claro que a
calibração de Qp da Fase 1 é validação do modelo hidrológico e **não** alimenta o mapa (o `pr` da
MUSLE espacializada é o local de Hao et al.); mencionar os 0,48% de pixels limitados à chuva.

**Não executar a pendência da seção 11** (grade 2×2 com "outro Qp") — é inócua, ver seção 12.4.

## Histórico (17/09/2026) — Fase 2, FCI/DSC abandonado, baseline adotado

Retomando o trabalho pausado em 14/09: a troca do objetivo de calibração pra NSE bruto não
resolveu (NSE continuou negativo, -0,60). Investigação encontrou um bug real (pixel de água/urbano
junto ao exutório inflando o denominador Ddn em toda a bacia) e corrigiu — mas mesmo corrigido, a
calibração **piorou** (NSE=-0,91). Não foi possível fazer o FCI/DSC (Hao et al., 2022) superar o
baseline trivial de escala linear constante nesta bacia. Decisão do usuário: **adotar o baseline**
como resultado final da Fase 2 (`SY_sim = c · E_unit`, c=0,109049, NSE=0,37). Ver
[notas_musle_espacializada.md](Notas%20Claude/notas_musle_espacializada.md) seção 9 pro histórico
completo (o que foi tentado, o bug encontrado, a hipótese não testada sobre escala de bacia).

Mapas finais gerados (`Scripts/calcular_sy_final.py`): `Evento {n}/SY{n}.tif` por evento e
`Dados Iniciais/SY_medio_eventos.tif` (mapa principal de hot spots erosivos, média dos 17 eventos).
Checagem física OK: hot spots (top 5%) têm C médio 5× maior que a bacia e LS mais alto — coerente.

**Corte de escopo (14/09/2026):** a simulação de cenários de conservação (alterar C/P) foi
removida do projeto do TCC — decisão do usuário dado o prazo. Não é mais um item pendente.

**Pendência para a próxima sessão (17/09/2026, não executada ainda):** testar SY_total com o
"outro Qp" (fator de pico recalibrado pra viés zero, alternativa deixada em aberto na seção 3.10
de `notas_qgis_calibracao_qp.md`) e com "minha calibração" (o experimento de alfa/beta livres,
seção 10 de `notas_musle_espacializada.md`), e gerar gráficos de SY e E_unit/MUSLE nos 4 casos
(2×2: Qp atual/alternativo × alfa,beta fixos de Hao/livres). Ver seção 11 de
`notas_musle_espacializada.md` para os detalhes completos.

**Próximo passo:** resolver a pendência acima, depois redação e figuras finais do TCC (Fase 2
tecnicamente concluída quanto ao baseline adotado).

## Fase 1 (concluída): calibração de Q e Qp

Resumo em [Resultados_Calibracao_TCC.xlsx](Resultados_Calibracao_TCC.xlsx) e nas notas
[notas_qgis_calibracao_qp.md](Notas%20Claude/notas_qgis_calibracao_qp.md). Adotado:

- **Volume (Q):** CN-1 (seco) + λ=0,05 (recalibrado do padrão 0,2). Erro médio +0,5%, absoluto
  47,4%. Script: `Scripts/spatialRain.py`.
- **Vazão de pico (Qp):** HU-SCS por convolução horária, Tc de Giandotti (10,65h) + fator de pico
  recalibrado (2,08→1,1184). Erro médio -38,4%, absoluto 46,0%. Script:
  `Scripts/spatialPeakFlowHU_convolucao.py`.
- **Área da bacia (MDE):** corrigida de 109,79 km² pra 137,80 km² (barreiras de drenagem
  corrigidas — aterros de estrada que o MDE não capturava). Raster final:
  `Dados Iniciais/qp_spatial/flowacc_corrigido.tif`.
- **Exutório real da bacia** (não confundir com o posto de chuva DBT5, que fica fora da bacia):
  X=318980,77, Y=7432307,08 (SIRGAS 2000/UTM 23S).

## Fase 2 (concluída): espacializar a MUSLE

Objetivo do TCC: gerar um **mapa** de produção de sedimentos (não um valor único por evento como
na IC), seguindo Hao et al. (2022) — `1-s2.0-S0022169422011490-main.pdf`, já na pasta.

### O que já está pronto

| Item | Arquivo(s) | Status |
|---|---|---|
| pr_pixel (vazão de pico local, por pixel) | `Evento {n}/pr{n}.tif` | ✅ pronto, 17 eventos |
| K (erodibilidade do solo) | `Dados Iniciais/K_raster.tif` | ✅ pronto (média 0,039) |
| LS (topográfico) | `Dados Iniciais/LS_moore.tif` | ✅ pronto (média 7,80; Moore e Burch 1986 / Moore et al. 1991 sobre o MDE em UTM, As ≤ 200 m — ver 16/10/2026). O antigo `LS_raster.tif` (média 0,536, herdado da IC) está defeituoso e só é usado para comparação |
| C (uso do solo) | `Dados Iniciais/C_raster.tif` | ✅ pronto (média 0,05 — **confirmado com você**, diferente dos 0,267 da Tabela 3 da IC, que provavelmente usou outra fonte) |
| P (práticas conservacionistas) | constante = 1,0 | ✅ (sem áreas de preservação ativa) |
| E_unit (erosão local por pixel) | `Evento {n}/E_unit{n}.tif` | ✅ pronto, 17 eventos — checado: E_unit sempre > sedimento medido em todos os eventos (faz sentido fisicamente) |
| SY_obs (sedimento medido por evento) | coluna `SYY_t` da planilha `eventos_processados_manuais.xlsx` | ✅ localizado, não precisou digitalizar nada |
| IC genérico (placeholder, W=1) | `Dados Iniciais/qp_spatial/IC_placeholder.tif` | ✅ só teste inicial, não usar pra calibração |
| IC por evento (Eq. 5 genérica, **desatualizado**) | `Evento {n}/IC{n}.tif` | ⚠️ calculado com fórmula errada (ver abaixo) — não usar |
| FCI por evento (Eq. 7 exata) | `Evento {n}/FCI{n}.tif` | ✅ pronto, 17 eventos (mas não usado no resultado final — ver seção "Onde estamos agora") |
| **SY final por evento (baseline linear adotado)** | `Evento {n}/SY{n}.tif` e `Dados Iniciais/SY_medio_eventos.tif` | ✅ **pronto — resultado final da Fase 2** |

### Correção importante feita nesta sessão

A primeira versão do índice de conectividade (`calcular_ic_por_evento.py`) usava a fórmula
genérica do IC (Borselli 2008), com W̄ = média do E_unit já calculado. Você mandou as imagens das
Eq. 5 e Eq. 7 do artigo (o texto extraído do PDF estava corrompido nessa parte) e ficou claro que
a Eq. 7 (a que Hao et al. realmente usam) é diferente: o numerador usa médias **separadas** de Q,
pr, K, C, P, S (não a média do E_unit combinado), e **sem o fator LS**. Corrigido em
`Scripts/calcular_fci_por_evento.py` — **é esse que precisa terminar de rodar**, não o
`calcular_ic_por_evento.py` antigo.

## Próximos passos

Fase 2 tecnicamente concluída (ver "Onde estamos agora"). O que falta é redação:

1. **Atualizar o texto do TCC** com o resultado final (baseline linear, NSE=0,37) e a discussão
   honesta de por que a conectividade espacial (Hao et al., 2022) não superou essa escala simples
   nesta bacia — ver `Notas Claude/notas_musle_espacializada.md` seção 9 pros detalhes e possíveis
   referências de apoio (Baert et al., 2026, já mostra tetos de precisão baixos pra MUSLE
   espacializada mesmo com dados observados perfeitos).
2. **Figuras finais**: mapa de `SY_medio_eventos.tif` (hot spots) com contexto (uso do solo,
   declividade) pra composição visual no TCC.
3. ~~Simulação de cenários~~ — cortado do escopo em 14/09/2026, não é mais um item pendente.

## Prazo

~6 semanas a partir de 12/09/2026 pra entregar o TCC (ver cronograma detalhado nas notas se
precisar reconferir o ritmo).

## Arquivos-chave pra retomar

- Este README (visão geral e checklist)
- `Notas Claude/notas_qgis_calibracao_qp.md` — histórico completo da Fase 1 (Q, Qp, correção do
  MDE), incluindo todas as tentativas descartadas e por quê.
- `Notas Claude/notas_musle_espacializada.md` — histórico completo da Fase 2, incluindo as
  fórmulas exatas do artigo e o histórico de discussão de por que não fizemos diferente
  (Método Racional pixel a pixel, qp constante, sub-bacias — todos descartados antes de achar a
  solução do Hao et al.).
- `1-s2.0-S0022169422011490-main.pdf` — artigo de referência completo.
- `Resultados_Calibracao_TCC.xlsx` — planilha com os resultados da Fase 1 (envie pro orientador
  se ainda não enviou).
