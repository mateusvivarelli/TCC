# Progresso da tarefa da noite (29/10/2026)

Instruções completas: `Notas Claude/tarefa_noturna_29-10.md`. Branch de trabalho: `claude/noite-29-10`.
Legenda: `[ ]` a fazer, `[~]` em andamento (com horário UTC de início), `[x]` pronto.

- [x] A. `Notas Claude/proposta_secao4.md` (Metodologia, 4.1 a 4.9) — pronto: proposta_secao4.md com 4.1 a 4.9, dúvidas no fim
- [x] B. `Notas Claude/leitura_referencias/loteD_fontes_K_C.md` (fontes dos valores de K e C) — pronto: 10 fontes lidas (9 texto completo; dissertação Silva 2016 inacessível); 4 valores não conferem com a fonte citada (K afloramento 0,0087, K Neossolo Litólico 0,0463, C pastagem 0,050, C cultura anual 0,2116 = soja); tabelas K e C propostas
- [x] C. `Notas Claude/proposta_secao5.md` (Resultados e Discussão) — pronto: 5.1 a 5.7 com Tabelas 11-14 e Figuras 6-12; Spearman da IC refeita (0,93) calculado na planilha, conferir
- [x] D. `Notas Claude/proposta_secao6.md` (Conclusões) — pronto: 6 conclusões ligadas aos objetivos 1.3.2 + trabalhos futuros
- [x] E. `Notas Claude/mapa_figuras_tabelas_secoes_4_a_6.md` (figuras e tabelas, numeração nova) — pronto: Tabelas 7-14 e Figuras 4-12 com legenda, arquivo e troca; 10 inconsistências/pontos listados
- [x] F. `Planilhas/planilha_calculos_concentrados.xlsx` (planilha mínima, sem formatação, com fórmulas vivas dos cálculos fora dos rasters; ver item F em `tarefa_noturna_29-10.md`) — pronto (script `Scripts/gerar_planilha_calculos_concentrados.py`)

## Registro (a sessão que trabalhar acrescenta linhas aqui)

- 29/10 00:35 (horário local): arquivos de instrução criados pela sessão do desktop; nada feito ainda.
- 29/10 00:45 (local): item F (planilha) acrescentado a pedido do usuário depois do envio para a nuvem. Prioridade: depois do item A e antes do C, porque é pequeno e o usuário vai conferir de manhã.
- F (planilha) concluído. Abas: serie (20.838 horas, Eckhardt em fórmula), eventos, calibracao, ajuste, metricas, volume, ic. Sem estilo. Recalculado no LibreOffice e conferido: c MC 0,03438 / MFM 0,02222 / chuva 19,72 / V_dir 0,001580 / TR 0,000832; MC 81,1% / 35% / -0,69; MFM 20,6% / 94% / 0,84; c*chuva 41,9% / 82% / 0,53; c*V_dir 15,9% / 94% / 0,85; IC refeita alfa 0,978, beta 0,733, 16,3% / 100% / 0,87; volume +2,9% / 53,9% / 46,3% / NSE -0,39; Eckhardt (0,995; 0,70) reproduz Bt da planilha (mediana 0,0016, máx 0,040 m3/s); TR, SomaBt e SY_obs por SOMASES batem com o CSV. Tudo bateu; nenhuma divergência. Arquivo salvo sem valores em cache (o Excel calcula ao abrir). Rótulo c do MC é 0,0344 (0,034379).
- A (seção 4) concluído; dúvidas para o usuário no fim de `proposta_secao4.md`.
- Teste do ambiente (pedido no item 0.3): Python 3.13; openpyxl, numpy, pandas presentes; Crossref, SciELO e doi.org respondem 200; LibreOffice disponível; LUME/UFRGS e (às vezes) Infoteca/Embrapa falham pelo proxy. Crossref limita requisições (HTTP 429) se forem muitas seguidas.

## Resumo final da sessão da noite (todos os itens A a F prontos)

**Pronto:** A `proposta_secao4.md`; B `leitura_referencias/loteD_fontes_K_C.md`; C `proposta_secao5.md`; D `proposta_secao6.md`; E `mapa_figuras_tabelas_secoes_4_a_6.md`; F `Planilhas/planilha_calculos_concentrados.xlsx` (+ `Scripts/gerar_planilha_calculos_concentrados.py`). Nada foi aplicado no Google Doc.

**Achados que pedem atenção de manhã:**
1. Fontes de K e C (lote D): 4 valores não conferem com a fonte que a IC cita: C do campo 0,050 (Silva et al. 2016 não trata de pastagem), C da lavoura 0,2116 (é o C da soja; o artigo dá 0,1418 para cultura anual), K do afloramento 0,0087 (Martins et al. 2011 não tem esse número) e K do Neossolo Litólico 0,0463 (nenhuma das 5 fontes, nem média delas). O K do Cambissolo 0,0475 é o de uma amostra individual (média da classe no artigo: 0,036). Campo e lavoura pesam no mapa (37% e 21% do sedimento). Dados bibliográficos corrigidos: Demarchi e Zimback é na revista Energia na Agricultura (não Rev. Eng. Agrícola); Silva et al. 2016 é SILVA, B. P. C.; Silva e Luchiari é SILVA, L. C. N.
2. Dissertação Silva (2016, UFRGS, K do Argissolo 0,0351) não abriu (LUME inacessível da nuvem). 0,0351 coincide com a média dos Neossolos em Silva e Alvares (2005): conferir.
3. Figuras com texto de método descartado dentro da imagem (rodapés de `escada_gargalo.png` e `mapa_07`): regerar no PC.
4. Spearman da IC refeita (0,93) calculado só na planilha desta noite; conferir.

**Suposições feitas:** nomes MC/MFM mantidos; λ = 0,20 citado só como valor de definição do CN tabelado (4.2.3) e na frase de Brandão (5.7); Tabela 9 sem a linha da IC refeita; Figura 12 = `mapa_07`; legendas de figura acima e "Fonte:" abaixo (ABNT de memória). Dúvidas listadas no fim de cada proposta.

**Não feito:** nada ficou pendente dos itens A a F. A revisão independente (`tarefa_revisao_29-10.md`, com progresso próprio) não fazia parte desta tarefa e não foi tocada.
- 29/10 05:31 UTC: sessão agendada encontrou todos os itens A a F já [x]; nada a fazer, encerrada.
- 29/10 13:13 UTC: planilha refeita a pedido do usuário (estava ilegível): aba Leia-me, aba Resumo, uma aba por modelo com o mesmo desenho (MC, MFM, Regra_chuva, Regra_Vdir, Regra_TR, IC_refeita), cabeçalhos com nome e unidade, linha 'como é calculado', cores (azul cabeçalho, amarelo dado dos rasters, verde resultado). Recalculada no LibreOffice: todos os números oficiais conferem, nenhum erro de fórmula.
