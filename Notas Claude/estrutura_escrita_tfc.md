# Estrutura da escrita do TFC

**As regras oficiais estão em `Notas Claude/entrega_tfc_regras.md`**, extraídas dos documentos da FECFAU que você enviou (regulamento de 2023, normalização da biblioteca e diretrizes do LALT). Esta nota guarda só a **proposta de estrutura** do texto, alinhada a essas regras. A pesquisa na web feita antes (06/10/2026) foi superada por esses documentos.

## 1. Proposta de estrutura para o seu TFC (minha proposta; elementos obrigatórios conforme o modelo da biblioteca)

Mapeada ao que o projeto já tem; o texto-base está em `Notas Claude/base_para_redacao_tcc.md`.

**Pré-textual:** capa; folha de rosto; ficha catalográfica (só se o trabalho for selecionado para o acervo); folha de aprovação; agradecimentos (opcional); **resumo (parágrafo único, ≤ 500 palavras) e abstract**, obrigatórios (palavras-chave: MUSLE, produção de sedimentos, SIG, SCS-CN, bacia do rio Jundiaí); listas de figuras, tabelas, siglas e símbolos (opcionais); sumário.

**Textual:**
1. **Introdução** — erosão e sedimentos em bacias, bacia do Jundiaí, lacuna (modelo concentrado da IC não localiza fontes), pergunta de pesquisa.
2. **Objetivos** (no modelo da biblioteca ficam em 1.2, dentro da Introdução, junto com a Justificativa 1.1) — geral e específicos (ajustar ao que foi feito: simulação de cenários foi cortada do escopo em 14/09/2026).
3. **Revisão bibliográfica / fundamentos teóricos** — USLE/MUSLE e Williams (1975); SCS-CN e λ; espacialização e conectividade (Hao et al., 2022; Borselli et al., 2008); limites de acurácia (Baert et al., 2026; Brandão et al., 2025; Valle Junior et al., 2019).
4. **Área de estudo e dados** — alta bacia do Jundiaí (137,8 km²), postos (DBT5, Campo Paulista), 17 eventos, séries de vazão e turbidez, solo, uso, MDE.
5. **Metodologia e detalhamento das atividades desenvolvidas** (o regulamento pede os dois) — Q (SCS-CN, CN-1, λ = 0,05); pr; E_unit; fatores K, C, LS, P; calibração de `c`; versão simulada e versão com volume forçado; métricas (NSE, WIA, PBIAS, leave-one-out).
6. **Resultados e discussão** — calibração de Q (Fase 1); mapas de E_unit/SY; hot spots; comparação simulado × forçado; por que FCI/DSC não superou o baseline linear; limitações; comparação honesta com Hao et al. e Baert et al.
7. **Conclusões e recomendações** — incluindo trabalhos futuros (cenários de conservação, outras bacias, rede de postos).

**Pós-textual:** referências (ABNT); apêndices (tabelas por evento, roteiro de cálculo do evento 11, scripts); anexos.

## 2. Ordem sugerida para começar a escrever

1. Levar as perguntas da seção 7 de `entrega_tfc_regras.md` ao orientador (cronograma, páginas, escopo, banca).
2. Montar o documento no **formato do modelo da biblioteca**: A4, margens 3/3/2/2 cm (esq./sup./dir./inf.), Arial 12, espaçamento 1,5, justificado (confirmar). Word é o caminho mais simples; o modelo de 2017 é `.doc`.
3. Escrever primeiro **Metodologia** e **Resultados** (já têm texto-base e números fechados), depois Introdução/Revisão, por último Resumo/Abstract e Conclusões.
4. Usar o roteiro do evento 11 como **apêndice de reprodutibilidade**.
5. Resolver antes as pendências de texto do README: NSE leave-one-out, deixar claro que o forçado não é previsão pura, 0,48% de pixels limitados à chuva, origem dos valores de CN.

## Fontes

- Documentos enviados pelo usuário: Regulamento do PFC/TFC 2023 (FECFAU), Normalização para TFC (BAE/FECFAU, 2017), Diretrizes TFC do LALT.
- [Página do TFC da FECFAU](https://www.fecfau.unicamp.br/graduacao/ec/tfc/) (não consegui abrir por bloqueio de rede; só o link)
- [CV954 — Trabalho Final de Curso I, DAC](https://www.dac.unicamp.br/portal/caderno-de-horarios/2026/1/S/G/FECFAU/CV954)
- [CV955 — Trabalho Final de Curso II, DAC](https://www.dac.unicamp.br/portal/caderno-de-horarios/2025/1/S/G/FECFAU/CV955)
