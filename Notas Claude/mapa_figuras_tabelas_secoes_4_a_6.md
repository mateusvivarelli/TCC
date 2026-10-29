# Mapa de figuras e tabelas das seções 4 a 6 (numeração nova)

Feito na noite de 29/10/2026 (sessão na nuvem). Base: `doc_texto_completo_29-10.md` e `doc_estado_secoes_4_a_6_28-10.md` (texto do Doc antes da reescrita) e as propostas `proposta_secao4.md`, `proposta_secao5.md` e `proposta_secao6.md`. **Nada foi mudado no Doc.**

Regra ABNT (de memória, ver `notas_musle_espacializada.md` §36; conferir no guia da FEC): figura com a identificação **acima** e "Fonte: ..." **abaixo**; tabela com título acima e fonte abaixo. Hoje as legendas das figuras do Doc estão **abaixo** e não há linha "Fonte:".

## Tabelas

As Tabelas 1 a 6 (seções 2 e 3) já estão no Doc e não mudam de número.

| Nº atual no Doc | Nº novo | Título sugerido (acima da tabela) | Arquivo em `TCC_Texto/` | Trocar no Doc? |
|---|---|---|---|---|
| 7 | 7 | Tabela 7. Variáveis usadas em cada evento. | sem arquivo; conteúdo proposto em `proposta_secao4.md` (4.2.1) | editar: tirar T_chuva / vazão inicial como variável do modelo; incluir V_dir e SY_obs (carga total) |
| 8 | 8 | Tabela 8. Origem da água em cada versão do modelo. | sem arquivo; conteúdo em `proposta_secao4.md` (4.5) | sim: tirar a coluna "Vazão de base (termo 2)" e "de dois componentes" do título |
| 9 | 9 | Tabela 9. Parâmetros fixos e calibrados. | `tabelas/tab_parametros.md` | sim (c1/c2 viram c); sugiro tirar a linha "IC refeita: α e β" (vai para o texto da 5.5) |
| 10 | 10 | Tabela 10. O evento 11 passo a passo, com um pixel exemplificado. | `tabelas/tab_evento11_passo_a_passo.md` | sim (todos os números; agora 3 colunas: Etapa, Grandeza, Valor) |
| 11 | 11 | Tabela 11. Sedimento por evento (t): medido e simulado pelo MC e pelo MFM, no ajuste e na validação cruzada. | `tabelas/tab_mc_mfm_eventos.md` | sim (antes: só MC, com colunas Encostas e Base) |
| 12 | 12 | Tabela 12. Desempenho na validação cruzada (calibração em escala logarítmica; carga total de sedimentos). | sem arquivo pronto; tabela montada em `proposta_secao5.md` (5.4) | sim (todos os números; linha nova SY = c * V_dir) |
| 13 | 13 | Tabela 13. Contribuição de cada classe de uso para o sedimento médio (MC e MFM). | `tabelas/tab_classes_uso.md` | sim (números; tirar "das encostas" do título; decidir sobre a coluna extra "Contribuição / área") |
| 14 | 14 | Tabela 14. Contribuição de cada classe de solo para o sedimento médio (MC e MFM). | `tabelas/tab_classes_solo.md` | sim (idem) |

Abaixo de cada tabela: "Fonte: elaborado pelo autor." (Tabela 9: "Fonte: elaborado pelo autor, com base em Williams (1975), ANA (2024), Chow, Maidment e Mays (1988) e Woodward et al. (2003).")

Tabelas de `TCC_Texto/tabelas/` que **não** entram nas seções 4 a 6:
- `tab_eventos.md` e `tab_volumes.md`: já são as Tabelas 2 e 3 (seção 3).
- `tab_fator_K.md`, `tab_fator_C.md`, `tab_fatores_classes.md`: Tabelas 5 e 6 (seção 3); ver as versões com fonte verificada em `leitura_referencias/loteD_fontes_K_C.md`.
- `tab_resultados.md` (por evento: c*chuva, MC, MFM, IC): opcional, como apêndice.
- `tab_nse_linear.md`: NSE linear, opcional como apêndice; **usar só as 6 primeiras linhas** (as outras são de modelos não adotados, o que fere a regra 3).
- `tab_qpico.md` (pico pelo hidrograma unitário do SCS): não é usado pelo modelo oficial; não entra.

## Figuras

As Figuras 1 a 3 (seção 3) já estão no Doc. **Todas as Figuras 4 a 11 do Doc são do modelo antigo** e precisam ser substituídas à mão (a API do Docs não troca imagem).

| Nº atual no Doc | Nº novo | Legenda sugerida (acima da figura) | Arquivo em `TCC_Texto/` | Trocar a imagem? |
|---|---|---|---|---|
| 4 | 4 | Figura 4. Fluxograma do método. | `figuras/mapas/fig_fluxograma.png` | sim (regerada) |
| 5 | 5 | Figura 5. Etapas espaciais do modelo no evento 11: chuva interpolada, retenção S, escoamento direto, índice de erosão E_unit e sedimento do pixel (MC). | `figuras/mapas/mapa_08_evento11.png` | sim (regerada; painel de S mostra S0,05) |
| (não existe) | 6 | Figura 6. Escoamento direto por evento: calculado pelo SCS-CN (CN-I, λ = 0,05 com S convertido) contra o medido. A faixa indica fator 2. | `figuras/fig_volume_direto.png` | figura nova (inserir na 5.1) |
| 6 | 7 | Figura 7. Sedimento simulado na validação cruzada contra o medido nos 17 eventos: SY = c * chuva, MC, MFM e IC refeita. A faixa indica fator 2. | `figuras/fig_dispersao.png` | sim (agora 4 painéis, com o MFM) |
| 7 | (sai) | composição encostas/base | sem arquivo | **remover** (era do modelo de dois componentes) |
| (não existe) | 8 | Figura 8. Erro percentual mediano e eventos dentro de fator 2, na validação cruzada, com a água calculada da chuva e com a água forçada ao medido. | `figuras/escada_gargalo.png` | figura nova (inserir na 5.3) |
| 8 | 9 | Figura 9. Chuva total de cada evento, interpolada pelo inverso do quadrado da distância a partir de dois postos. | `figuras/mapas/mapa_04_chuva_eventos.png` | não precisa (igual); só renumerar |
| 9 | 10 | Figura 10. Escoamento direto calculado pelo SCS-CN (CN-I, λ = 0,05 com S convertido) em cada evento. | `figuras/mapas/mapa_05_escoamento_eventos.png` | sim |
| 10 | 11 | Figura 11. Sedimento produzido em cada pixel em cada evento (MC). | `figuras/mapas/mapa_06_sedimento_eventos.png` | sim |
| 11 | 12 | Figura 12. Sedimento médio dos 17 eventos e áreas críticas (5% dos pixels de maior contribuição), para o MC e o MFM. | `figuras/mapas/mapa_07_sedimento_medio.png` | sim |

Abaixo de cada figura: "Fonte: elaborado pelo autor." (Figura 9 a 12, se o usuário quiser: "Fonte: elaborado pelo autor, com dados de ... ".)

`figuras/fig_mapa_sy_medio.png` (só MC, 2 painéis) é alternativa à Figura 12; sugiro o `mapa_07`.

**Remissões no texto que mudam:** "Figuras 8 a 10" vira "Figuras 9 a 11"; "Figura 9" (escoamento) vira 10; "Figura 11" (mapa médio) vira 12; "Figura 6" (dispersão) vira 7. Nas seções 2.4 e 2.5 ainda há remissões "seção 4.x" a preencher (pendência antiga).

## Inconsistências e problemas encontrados

1. **Texto dentro das imagens com método descartado (regra 3):**
   - `escada_gargalo.png`: rodapé "Sem termo de vazão de base." e "Validação leave-one-out ... (um coeficiente)".
   - `mapa_07_sedimento_medio.png`: rodapé "Modelo só com escoamento direto (sem termo de vazão de base)."
   - `mapa_06` e `mapa_08`: segundo `relatorio_regeneracao_oficial_28-10.md`, mantêm o rótulo "Sedimento das encostas" (eco do modelo de dois termos; não conferi as imagens esta noite).
   Sugestão: regerar as figuras sem essas frases quando houver acesso ao PC (scripts `gerar_mapas_tcc.py` e `_escada_gargalo_chuva_escoamento.py`). Não é possível na nuvem (sem rasters).
2. **Títulos dentro das imagens repetem a legenda** (Figuras 6, 7, 8, 12 têm título interno). Com legenda ABNT acima, o título interno fica duplicado. Mesma pendência das Figuras 1 a 3.
3. **Apêndice inexistente:** as propostas da 4.8 e 5.4 citam "Apêndice" para o NSE linear, mas o Doc não tem apêndices hoje. Ou criar o Apêndice A (NSE linear, 6 linhas de `tab_nse_linear.md`), ou cortar as menções.
4. **Caracteres especiais em tabelas:** `tab_fator_K.md` usa "t·h·MJ⁻¹·mm⁻¹" (ponto médio e sobrescrito negativo), contra a regra 2. No Doc, escrever "t*h*MJ-1*mm-1" ou "t h MJ-1 mm-1". `tab_evento11_passo_a_passo.md` já usa "10^-4" e "->".
5. **Tabela 12 sem arquivo:** não há `.md` pronto com a Tabela 12 nova (com Spearman). Montei a tabela em `proposta_secao5.md`; o Spearman da IC refeita (0,93) e das duas regras (0,63; 0,90) vem da planilha recalculada nesta noite, não de um arquivo de tabelas.
6. **Coluna extra nas Tabelas 13 e 14:** os arquivos têm "Contribuição / área, calculado (%)", que o Doc não tem. Decidir.
7. **Tabela 2 (seção 3) com colunas que o modelo não usa mais:** "Q inicial" e "T chuva" eram do termo de base. A seção 3 já foi revisada pelo usuário; se as colunas ficarem, o texto não precisa delas (não é inconsistência de número, só sobra).
8. **Conferências de números feitas nesta noite (todas bateram):**
   - `tab_evento11_passo_a_passo.md`: Q do pixel = (75,4 - 12,2)² / (75,4 + 0,95 * 244,2) = 12,99 mm (tabela: 13,00, arredondamento); 0,0344 * 40.885 = 1.406 t; 0,0222 * 63.451 = 1.409 t (tabela 1.410, com c = 0,022216); Q médio 7,2 mm = 997 mil m³ / 138,1 km².
   - Coerência MC x MFM no evento 11: f = 1.479 / 997 = 1,48; soma(E) MFM / MC = 1,55 = f^1,12 (como esperado, E proporcional a Q^1,12).
   - `tab_mc_mfm_eventos.md` e `tab_resultados.md`: colunas de validação cruzada iguais entre si e iguais ao CSV.
   - `tab_volumes.md`: total 15.702 / 15.263 = 1,029 (+2,9%), igual ao texto.
   - `fig_volume_direto.png`: 65% em fator 2 e 46% de erro mediano, iguais à nota §34.
   - Planilha `Planilhas/planilha_calculos_concentrados.xlsx`: reproduz todos os números oficiais (ver progresso).
9. **Mediana x média de S0,05:** a Tabela 10 dá S0,05 médio 489,9 mm; a checagem de 27/10 dá mediana 322,5 mm. Não é erro (média e mediana), mas o texto deve dizer "média".
10. **Doc 5.6 atual:** fala em "correlação 0,69 com K*LS*C (Spearman 0,79)"; nas notas novas só há Pearson (0,77 MC; 0,76 MFM). A proposta usa Pearson.
