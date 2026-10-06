# Estrutura da escrita do TFC — pesquisa sobre normas da Unicamp (Engenharia Civil)

Pesquisa feita em 06/10/2026. **Limite importante:** o proxy do ambiente bloqueou os domínios da Unicamp (`fecfau.unicamp.br`, `ft.unicamp.br`, `lalt.fecfau.unicamp.br`), então **não consegui abrir o regulamento do TFC da FECFAU nem modelos reais**. O que está abaixo é só o que apareceu nos resultados de busca (marcado como confirmado) mais uma proposta minha (marcada como proposta). Itens como número de páginas e formatação **precisam ser confirmados com a coordenação**.

## 1. O que foi confirmado

- Em Engenharia Civil da Unicamp o TCC se chama **Trabalho Final de Curso (TFC)**, em duas disciplinas: **CV954 (TFC I)** e **CV955 (TFC II)**. Seu próprio `Projeto TCC.pdf` também usa "TFC".
- É individual, com orientador docente permanente, e requisito obrigatório para a formatura. O objetivo é sintetizar o conhecimento do curso, de preferência aplicado a um problema real.
- Existe um **Regulamento do Trabalho Final de Curso** da graduação em Engenharia Civil (FECFAU), citado na página do TFC: <https://www.fecfau.unicamp.br/graduacao/ec/tfc/>. Esse é o documento que define prazos, banca, estrutura e formato.
- A faculdade hoje se chama **FECFAU** (antiga FEC).
- Há trabalho da própria Unicamp na sua bacia: "Análise dos processos hidrossedimentológicos na bacia do rio Jundiaí" (E. V. da Silva, I. J. Silva, Y. C. Lima; orientador André L. S. Salustiano Martim) — resultado de busca de repositório, vale localizar como TFC/IC de referência.

## 2. O que NÃO foi confirmado (perguntar à coordenação)

- Número mínimo/máximo de páginas.
- Fonte, margens, espaçamento, modelo oficial (Word/LaTeX) da FECFAU.
- Composição da banca, datas de entrega e defesa, forma de depósito (repositório Unicamp).
- Requisitos para o orientador e coorientador.
- Onde ver TFCs anteriores (a biblioteca da FEC e o repositório da Unicamp costumam ter).

Pergunta pronta para enviar: "Pode me enviar o regulamento atual do TFC, o modelo de formatação, o limite de páginas, o calendário de CV954/CV955 e 2 ou 3 TFCs recentes de hidrologia como exemplo?"

## 3. Referências de formatação de outras unidades da Unicamp (não são da FECFAU)

Usar só como pista, **não como norma**:

- Orientação de formatação de TCC do LABJOR/Unicamp: <https://labjor.unicamp.br/wp-content/uploads/2024/10/Orientacao-formatacao-TCC.pdf> — estrutura pré-textual (capa, folha de rosto, dedicatória, agradecimentos, epígrafe, resumo, listas, sumário), textual (introdução, revisão, objetivos, materiais e métodos, resultados e discussão, conclusões) e pós-textual (referências, apêndices, anexos); páginas pré-textuais contadas mas sem número; numeração em arábicos a partir da Introdução, canto superior direito.
- Template LaTeX para a Faculdade de Tecnologia (FT/Unicamp): <https://www.overleaf.com/latex/templates/template-for-graduation-work-masters-dissertation-or-doctoral-thesis-for-school-of-technology-unicamp/rhznqbkjvpcr> — serve de ponto de partida em LaTeX, mas é de outra unidade.
- Normas gerais: ABNT NBR 14724 (trabalhos acadêmicos), NBR 6023 (referências), NBR 10520 (citações), NBR 6024 (numeração de seções), NBR 6027 (sumário), NBR 6028 (resumo).

## 4. Proposta de estrutura para o seu TFC (minha proposta, a ajustar ao regulamento)

Mapeada ao que o projeto já tem; o texto-base está em `Notas Claude/base_para_redacao_tcc.md`.

**Pré-textual:** capa; folha de rosto; folha de aprovação; agradecimentos; resumo e *abstract* (palavras-chave: MUSLE, produção de sedimentos, SIG, SCS-CN, bacia do rio Jundiaí); listas de figuras, tabelas, siglas e símbolos; sumário.

**Textual:**
1. **Introdução** — erosão e sedimentos em bacias, bacia do Jundiaí, lacuna (modelo concentrado da IC não localiza fontes), pergunta de pesquisa.
2. **Objetivos** — geral e específicos (ajustar ao que foi feito: simulação de cenários foi cortada do escopo em 14/09/2026).
3. **Revisão bibliográfica** — USLE/MUSLE e Williams (1975); SCS-CN e λ; espacialização e conectividade (Hao et al., 2022; Borselli et al., 2008); limites de acurácia (Baert et al., 2026; Brandão et al., 2025; Valle Junior et al., 2019).
4. **Área de estudo e dados** — alta bacia do Jundiaí (137,8 km²), postos (DBT5, Campo Paulista), 17 eventos, séries de vazão e turbidez, solo, uso, MDE.
5. **Metodologia** — Q (SCS-CN, CN-1, λ = 0,05); pr; E_unit; fatores K, C, LS, P; calibração de `c`; versão simulada e versão com volume forçado; métricas (NSE, WIA, PBIAS, leave-one-out).
6. **Resultados e discussão** — calibração de Q (Fase 1); mapas de E_unit/SY; hot spots; comparação simulado × forçado; por que FCI/DSC não superou o baseline linear; limitações; comparação honesta com Hao et al. e Baert et al.
7. **Conclusões e recomendações** — incluindo trabalhos futuros (cenários de conservação, outras bacias, rede de postos).

**Pós-textual:** referências (ABNT); apêndices (tabelas por evento, roteiro de cálculo do evento 11, scripts); anexos.

## 5. Ordem sugerida para começar a escrever

1. Pedir à coordenação regulamento, modelo e exemplos (seção 2) — é o que destrava formato e tamanho.
2. Escolher o formato: Word (modelo da FECFAU, se existir) ou Overleaf (template da FT adaptado).
3. Escrever primeiro **Metodologia** e **Resultados** (já têm texto-base e números fechados), depois Introdução/Revisão, por último Resumo e Conclusões.
4. Usar o roteiro do evento 11 como **apêndice de reprodutibilidade**.
5. Resolver antes pendências de texto já listadas no README: NSE leave-one-out, deixar claro que o forçado não é previsão pura, 0,48% de pixels limitados à chuva, origem dos valores de CN.

## Fontes

- [Página do TFC da FECFAU (Engenharia Civil)](https://www.fecfau.unicamp.br/graduacao/ec/tfc/)
- [CV954 — Trabalho Final de Curso I, DAC](https://www.dac.unicamp.br/portal/caderno-de-horarios/2026/1/S/G/FECFAU/CV954)
- [CV955 — Trabalho Final de Curso II, DAC](https://www.dac.unicamp.br/portal/caderno-de-horarios/2025/1/S/G/FECFAU/CV955)
- [Orientação de formatação de TCC (LABJOR/Unicamp)](https://labjor.unicamp.br/wp-content/uploads/2024/10/Orientacao-formatacao-TCC.pdf)
- [Template LaTeX Unicamp FT (Overleaf)](https://www.overleaf.com/latex/templates/template-for-graduation-work-masters-dissertation-or-doctoral-thesis-for-school-of-technology-unicamp/rhznqbkjvpcr)
- [Instrução normativa de TCC da FT/Unicamp](https://www.ft.unicamp.br/sites/default/files/graduacao/InstrucaoNormativaparaTrabalhodeConclusaodeCurso.pdf) (não consegui abrir; só o link)
