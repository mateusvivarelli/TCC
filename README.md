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
| LS (topográfico) | `Dados Iniciais/LS_raster.tif` | ✅ pronto (média 0,536, bate com a IC) |
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
