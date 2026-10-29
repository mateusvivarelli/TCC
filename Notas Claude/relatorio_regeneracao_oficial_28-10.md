# Relatório: regeneração das tabelas, figuras e mapas com o modelo oficial (28/10/2026)

Modelo oficial: CN-II da ANA convertido para CN-I; λ = 0,05 com S convertido por Woodward et al. (2003); MUSLE por pixel só com escoamento direto; SY = c * soma(E_unit); c em log; validação leave-one-out. Nada foi commitado, o Google Doc não foi tocado, e os rasters e CSVs de Dados Iniciais só foram lidos.

## Arquivos gerados (todos em C:\TCC)

Tabelas (`TCC_Texto\tabelas\`), por `Scripts\gerar_tabelas_tcc.py` e `Scripts\_tabela_apendice_B.py`:
- `tab_resultados.md`, `tab_parametros.md`, `tab_volumes.md`, `tab_classes_uso.md`, `tab_classes_solo.md`: regeneradas.
- `tab_mc_mfm_eventos.md` (Tabela 10): refeita, com medido, MC e MFM no ajuste e na validação cruzada e a razão SCS-CN/medido.
- `tab_evento11_passo_a_passo.md`: nova (colunas Etapa | Grandeza | Valor, como a Tabela 9 do Doc).
- `tab_nse_linear.md` (Apêndice B): refeita; modelos antigos mantidos como "não adotado".
- Sem mudança (conteúdo idêntico): `tab_eventos.md`, `tab_qpico.md`, `tab_fatores_classes.md`. Não mexi em `tab_fator_K.md` e `tab_fator_C.md`.

Figuras (`TCC_Texto\figuras\`), por `gerar_figuras_tcc.py` e `_escada_gargalo_chuva_escoamento.py`:
- `fig_dispersao.png` (4 painéis), `fig_volume_direto.png`, `fig_mapa_sy_medio.png`, `escada_gargalo.png` e `escada_gargalo.csv`.

Mapas (`TCC_Texto\figuras\mapas\`), por `gerar_mapas_tcc.py`:
- Mudaram: `mapa_03_fatores.png` (título do painel do CN), `mapa_05_escoamento_eventos.png`, `mapa_06_sedimento_eventos.png`, `mapa_07_sedimento_medio.png`, `mapa_08_evento11.png`, `fig_fluxograma.png`.
- Sem mudança (regerados idênticos): `mapa_01`, `mapa_02`, `mapa_04`.

Planilha: `C:\TCC\Comparacao_Modelos_TCC.xlsx`, por `gerar_planilha_comparacao.py`. A linha ADOTADO agora é o modelo oficial (MC e MFM); o modelo de λ 0,20 ficou como "Não adotado (26/10/2026)". A aba Entradas ganhou 5 colunas do modelo oficial.

Scripts editados (histórico no git): `gerar_tabelas_tcc.py`, `gerar_figuras_tcc.py`, `gerar_mapas_tcc.py`, `_escada_gargalo_chuva_escoamento.py`, `_tabela_apendice_B.py`, `gerar_planilha_comparacao.py`.

## Números conferidos (LOO, calibração em log, carga total)

O `gerar_tabelas_tcc.py` recalcula o modelo por conta própria e compara com `comparacao_SY_lambda005_woodward.csv`: soma de E_unit, volume SCS-CN, MC LOO, MFM LOO, c*chuva LOO e IC LOO batem com o CSV (diferença relativa máxima de 2e-16). O script para se divergir.

| Modelo | Erro mediano | Fator 2 | NSE log | Referência |
|---|---|---|---|---|
| MC | 81,1% | 35% | -0,69 | confere |
| MFM | 20,6% | 94% | 0,84 | confere |
| SY = c*chuva | 41,9% | 82% | 0,53 | confere |
| SY = c*V_dir medido | 15,9% | 94% | 0,85 | confere |
| IC refeita | 16,3% | 100% | 0,87 | confere |

- c: MC 0,0344 e MFM 0,0222 (conferem).
- SCS-CN oficial / medido (escoamento direto): mediana 0,86 (de 0,10 a 2,15), viés total +3%, NSE do volume -0,39, erro mediano 46%, 65% dentro de fator 2 (conferem).
- NSE linear (Apêndice B): MC -4,35 / -5,43 / -3,52 (ajuste / LOO / sem o evento 15); MFM 0,80 / 0,78 / 0,62 (conferem a seção 32 das notas).
- Mapas: MC x MFM r = 0,984 e 94,2% das áreas críticas coincidentes (confere).
- Planilha (calibração linear, só sensibilidade): MC NSE 0,19 / LOO -0,10; MFM 0,80 / 0,77.

## O que mudou em relação ao modelo de 26/10 (λ 0,20)

- MC: erro mediano de 98% para 81%; fator 2 de 24% para 35%; NSE log de -3,95 para -0,69. c de 0,0784 para 0,0344. Continua pior que SY = c*chuva.
- MFM: erro mediano de 39% para 21%; NSE log de 0,50 para 0,84; fator 2 igual (94%). c de 0,0302 para 0,0222. MFM e IC passam a não se distinguir.
- Volume SCS-CN / medido: mediana de 0,58 para 0,86; erro mediano de 69% para 46%; NSE do volume de -0,69 para -0,39.
- Evento 11: MC LOO 1.383 t (-24%) e MFM LOO 1.387 t (-24%), contra 2.391 t (+31%) e 1.931 t (+6%) antes. Nenhum pixel fica sem escoamento no evento 11 (antes, 10%).
- Contribuição por classe de uso muda pouco (Campo 37,4% do sedimento, antes 39,4%; Silvicultura 24,2%, antes 21,6%; Lavoura temporária 20,9%, antes 22,5%; Mata nativa 7,5%, antes 6,3%). O kg/pixel muda bastante (ex.: Campo no MC 18,38, antes 37,43; MFM 11,34, antes 14,48) porque c e o padrão de escoamento mudaram. Vale reler as porcentagens citadas nas Tabelas 12 e 13 e no texto da 5.6.
- Textos nas figuras e tabelas trocados de "λ = 0,20" e "CN seco" para "CN-I" e "λ = 0,05 com S convertido (Woodward)".

## Pixel de exemplo do evento 11

Conferi o pixel (E 330,18 km; N 7.432,86 km): lavoura temporária sobre Argissolo, P 75,4 mm, CN-II 81,0, K 0,0351, C 0,212, LS 4,869 (iguais aos da Tabela 9 antiga). Com o modelo oficial: CN-I 64,2; S0,20 141,9 mm; S0,05 244,2 mm; λS 12,2 mm; Q 13,00 mm; E_unit 1,167; c*E_unit 0,0401 t. Soma de E_unit do MC: 40.885; SY ajustado 1.406 t.

## O que NÃO foi feito, e por quê

- Tabela 19 do Apêndice D (conversões calibradas): os scripts do revisor não estão no repositório. Não refeita.
- Figuras ilustrativas de `Figuras\ilustrativas_27-10\`: não mexi, como pedido.
- Google Doc, git add/commit/push: não feitos, como pedido.
- Scripts de pacote do evento 11 (`gerar_pacote_evento11_*.py`, pasta `Evento11_Auditoria`), `Relatorio_Resultados_TCC.pdf` e `TCC_rascunho_04`: continuam no modelo antigo (fora do pedido).
- `mapa_01`, `mapa_02`, `mapa_04`: não dependem do modelo; regerados sem mudança.

## Problemas e observações

- A figura `mapa_08` mostra a retenção S0,05 (convertida); o raster `S - Seco.tif` é o S0,20 do CN-I e a conversão é feita dentro do script. O mapa 3 usa `CN_I_alinhado.tif` de `Evento11_Auditoria` (CN-I), só mudei o título.
- Correção de layout feita nas figuras novas: título de `fig_volume_direto` em duas linhas; caixa da fórmula do fluxograma estreitada (encostava na caixa do modelo forçado); títulos do mapa 8 encurtados (um passava por baixo da barra de cores).
- Caracteres: nas tabelas e rótulos novos usei "*" e "-"; a tabela do evento 11 usa "->" no lugar de seta e "10^-4" no lugar de potência com sinal. "λ", "Σ", "²", "³" ficaram. Nas tabelas antigas que reaproveitei (ex.: `tab_mc_mfm_eventos.md` e `tab_nse_linear.md`), os "−" e "·" foram trocados por "-" e "*".
- Os rótulos "Sedimento das encostas" (mapas 6 e 8) foram mantidos como estavam no Doc; vale decidir se continua esse nome, já que o modelo agora só tem escoamento direto.
- Na tabela do evento 11, a coluna extra "Etapa" segue o formato da Tabela 9 do Doc (3 colunas), e não só "grandeza | valor".
- O texto do Doc ainda precisa ser reescrito com estes números (a lista `mudancas_docs_sem_base_26-10.md` está com os números do modelo de 26/10).
