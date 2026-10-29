# Progresso da tarefa da noite (29/10/2026)

Instruções completas: `Notas Claude/tarefa_noturna_29-10.md`. Branch de trabalho: `claude/noite-29-10`.
Legenda: `[ ]` a fazer, `[~]` em andamento (com horário UTC de início), `[x]` pronto.

- [x] A. `Notas Claude/proposta_secao4.md` (Metodologia, 4.1 a 4.9) — pronto: proposta_secao4.md com 4.1 a 4.9, dúvidas no fim
- [x] B. `Notas Claude/leitura_referencias/loteD_fontes_K_C.md` (fontes dos valores de K e C) — pronto: 10 fontes lidas (9 texto completo; dissertação Silva 2016 inacessível); 4 valores não conferem com a fonte citada (K afloramento 0,0087, K Neossolo Litólico 0,0463, C pastagem 0,050, C cultura anual 0,2116 = soja); tabelas K e C propostas
- [~] (início: 03:53 UTC) C. `Notas Claude/proposta_secao5.md` (Resultados e Discussão)
- [ ] D. `Notas Claude/proposta_secao6.md` (Conclusões)
- [ ] E. `Notas Claude/mapa_figuras_tabelas_secoes_4_a_6.md` (figuras e tabelas, numeração nova)
- [x] F. `Planilhas/planilha_calculos_concentrados.xlsx` (planilha mínima, sem formatação, com fórmulas vivas dos cálculos fora dos rasters; ver item F em `tarefa_noturna_29-10.md`) — pronto (script `Scripts/gerar_planilha_calculos_concentrados.py`)

## Registro (a sessão que trabalhar acrescenta linhas aqui)

- 29/10 00:35 (horário local): arquivos de instrução criados pela sessão do desktop; nada feito ainda.
- 29/10 00:45 (local): item F (planilha) acrescentado a pedido do usuário depois do envio para a nuvem. Prioridade: depois do item A e antes do C, porque é pequeno e o usuário vai conferir de manhã.
- F (planilha) concluído. Abas: serie (20.838 horas, Eckhardt em fórmula), eventos, calibracao, ajuste, metricas, volume, ic. Sem estilo. Recalculado no LibreOffice e conferido: c MC 0,03438 / MFM 0,02222 / chuva 19,72 / V_dir 0,001580 / TR 0,000832; MC 81,1% / 35% / -0,69; MFM 20,6% / 94% / 0,84; c*chuva 41,9% / 82% / 0,53; c*V_dir 15,9% / 94% / 0,85; IC refeita alfa 0,978, beta 0,733, 16,3% / 100% / 0,87; volume +2,9% / 53,9% / 46,3% / NSE -0,39; Eckhardt (0,995; 0,70) reproduz Bt da planilha (mediana 0,0016, máx 0,040 m3/s); TR, SomaBt e SY_obs por SOMASES batem com o CSV. Tudo bateu; nenhuma divergência. Arquivo salvo sem valores em cache (o Excel calcula ao abrir). Rótulo c do MC é 0,0344 (0,034379).
- A (seção 4) concluído; dúvidas para o usuário no fim de `proposta_secao4.md`.
- Teste do ambiente (pedido no item 0.3): Python 3.13; openpyxl, numpy, pandas presentes; Crossref, SciELO e doi.org respondem 200; LibreOffice disponível; LUME/UFRGS e (às vezes) Infoteca/Embrapa falham pelo proxy. Crossref limita requisições (HTTP 429) se forem muitas seguidas.
