# Tarefa de revisão independente (29/10/2026): processo, resultados e texto do TCC

Quem lê: uma sessão na nuvem do Claude Code que atua como **revisora independente**, sem acesso ao usuário (ele está dormindo ou acabou de acordar) e **sem acesso ao Google Docs/Drive**. A sessão que escreveu as propostas é outra; **você não deve confiar nela**: confira tudo contra os dados e o código. Você **não corrige nada nos arquivos dos outros**: só produz um relatório. Se uma dúvida só o usuário pode resolver, escreva a pergunta no relatório e siga em frente.

## 0. Antes de começar

1. `git fetch origin claude/noite-29-10` e `git checkout -B claude/noite-29-10 origin/claude/noite-29-10`. Trabalhe só nessa branch, nunca em `main`.
2. Leia `Notas Claude/progresso_noturno_29-10.md`: mostra o que a sessão da noite já entregou. **Revise o que existir.** Se alguma proposta ainda não existir, registre "não revisado: não existe" e siga; não espere por ela.
3. Crie `Notas Claude/progresso_revisao_29-10.md` com os itens R1, R2 e R3 (`[ ]`, `[~] (início HH:MM UTC)`, `[x]`). Faça `git commit` + `git pull --rebase origin claude/noite-29-10` + `git push origin claude/noite-29-10` **depois de cada parte**, mesmo parcial. Se R1 a R3 estiverem `[x]`, pare. Se um item estiver `[~]` há menos de 40 min, pule para o próximo.
4. Teste do ambiente (uma linha no progresso): `python3 --version`; `python3 -c "import numpy, pandas, scipy, openpyxl"` (instale o que faltar com pip); `which soffice libreoffice`.

## 1. O que revisar (arquivos do repositório)

- **Texto atual do Doc:** `Notas Claude/doc_texto_completo_29-10.md` (seções 1 a 3 e Resumo/Abstract estão no modelo oficial; **4 a 6 estão no modelo antigo e serão substituídas** pelas propostas; revise as propostas, não o texto antigo das seções 4 a 6, exceto a lista de REFERÊNCIAS).
- **Propostas da noite (se existirem):** `Notas Claude/proposta_secao4.md`, `proposta_secao5.md`, `proposta_secao6.md`, `leitura_referencias/loteD_fontes_K_C.md`, `mapa_figuras_tabelas_secoes_4_a_6.md`, `Planilhas/planilha_calculos_concentrados.xlsx`.
- **O modelo e os números:** `Notas Claude/resumo_modelo_completo.md` (chama o modelo oficial de "candidato"), `notas_musle_espacializada.md` (§24 a §36), `relatorio_regeneracao_oficial_28-10.md`, `relatorio_checagens_base_alvo_woodward_27-10.md`, `instrucoes_sessao_desktop.md`.
- **Código e dados:** `Scripts/calcular_sy_lambda005_woodward.py` (modelo oficial), `Scripts/calcular_sy_so_direto.py`, `Scripts/gerar_tabelas_tcc.py`, `Scripts/_recalcular_ls_moore.py`; `Dados Iniciais/comparacao_SY_lambda005_woodward.csv`, `Dados Iniciais/Dados_finais_histereses_corrigido.xlsx`, `eventos_processados_manuais.xlsx`, `serie_Q_Qb_Qquick_Eckhardt_orientador.xlsx`; `TCC_Texto/tabelas/*.md`.
- **Referências lidas:** `Notas Claude/leitura_referencias/` (lotes A, B, C e, se existir, D) e `referencias_consolidadas.md`.
- **Não há rasters nem QGIS na nuvem.** Tudo o que depende dos pixels só pode ser conferido pelo código e pelos CSV/tabelas já prontos.

## 2. Partes (nesta ordem)

### R1: Metodologia (o processo)
Saída: seção "R1" de `Notas Claude/revisao_processo_29-10.md`. Audite a cadeia inteira, do dado bruto ao resultado, como um revisor cético:
1. **Código contra o texto:** as equações do Doc/propostas (IDW com dois postos e pesos 0,307/0,693; S = 25,4*(1000/CN - 10); conversão de Woodward, unidades em polegadas; Q do SCS-CN com abstração λS; pr = Q/1000 * A * (RI/R)/3600; E_unit = 11,8*(Q*pr*A)^0,56*K*C*LS; SY = c*soma(E_unit); c = exp(média(ln SY - ln E)); LOO) batem com o que `calcular_sy_lambda005_woodward.py` de fato faz? Aponte diferenças, unidades erradas e hipóteses implícitas (por exemplo, cap Q <= P, máscara de pixels, janela dos eventos, uso de RI/R como número único por evento).
2. **Lógica científica:** o MFM redistribui o volume medido pelo padrão do SCS-CN (fator único f por evento); o que isso permite e não permite concluir? A calibração em log e o LOO simples (só `c` é refeito) estão corretos? Onde há **vazamento** (λ, CN-I, a conversão e a máscara foram escolhidos olhando os 17 eventos)? Há circularidade na comparação com a IC (a IC usa o hidrograma do evento que gera o SY medido)? O alvo "carga total atribuída ao escoamento direto" é defensável? O que mais a banca atacaria? Liste **as 10 perguntas mais prováveis da banca** com a melhor resposta honesta de 2 a 3 linhas para cada.
3. **Recomputação independente:** com os CSV e as planilhas de dados do repositório, refaça em Python (numpy/pandas) a chuva ponderada R, V_dir = TR - ΣBt, `c` (MC e MFM), as previsões LOO e as métricas, e compare com os números oficiais (MC 81,1% / 35% / NSE em log -0,69; MFM 20,6% / 94% / 0,84; SY = c*chuva 41,9% / 82% / 0,53; SY = c*V_dir 15,9% / 94% / 0,85; IC refeita 16,3% / 100% / 0,87; c: MC 0,0344, MFM 0,0222). Se existir `Planilhas/planilha_calculos_concentrados.xlsx`, recalcule as fórmulas (com `soffice --headless --convert-to xlsx` ou refazendo as contas) e confira cada aba. Reproduza também o filtro de Eckhardt (alfa 0,995; BFImax 0,70) contra a série do orientador.

### R2: Resultados (a pesquisa)
Saída: seção "R2" do mesmo arquivo.
1. **Consistência de números** entre `TCC_Texto/tabelas/*.md`, `notas_musle_espacializada.md`, `relatorio_regeneracao_oficial_28-10.md`, o README e as propostas das seções 4 a 6: liste toda divergência (por exemplo, 137,8 / 138,1 / 138,8 km²; número de pixels; tabelas citadas com numeração velha).
2. **Afirmações contra os dados:** para cada afirmação central das propostas (e do Resumo/Abstract do Doc), diga se os números a sustentam, se há exagero ("equivalente", "melhor", "não se distingue") e qual intervalo ou teste a apoia (use bootstrap de eventos com 4.000 reamostragens e Wilcoxon pareado, em Python, para as diferenças MFM x IC, MFM x SY = c*V_dir e MC x SY = c*chuva; registre os valores).
3. **Sensibilidade que a banca pediria:** sem o evento 17 e sem o evento 15 (MedAPE, fator 2, NSE em log); evento a evento, onde cada modelo erra mais; erro relativo contra tamanho do evento; o que acontece com a conclusão. Diga se alguma conclusão muda.
4. **Limitações que faltam** nas propostas ou no Doc (17 eventos, 8,4% dos pixels com CN-I < 35 fora da faixa de Woodward, critério do NEH-4 abandonado no NEH-630, mapa sem validação espacial, hipótese de mesma concentração na base, K = 0 e C = 0 na área urbana etc.). Proponha frases curtas.

### R3: Tese (o texto)
Saída: seção "R3" do mesmo arquivo.
Revise **todo o texto**: o Doc atual (seções 1 a 3, Resumo/Abstract, REFERÊNCIAS) e as propostas das seções 4 a 6. Procure:
1. **Erros factuais e de número** (conferir contra os arquivos acima), **inconsistências entre seções** (siglas definidas duas vezes ou nenhuma; nomes dos modelos; numeração de tabelas e figuras; remissões "seção 4.x" que apontam para o lugar errado), **frases que se contradizem** ou prometem o que os dados não mostram.
2. **Regras do usuário (violações):** métodos ou parâmetros descartados no texto (λ = 0,20, modelo de dois componentes, termo de vazão de base, AMC III, calibração linear, FCI/DSC etc.); caracteres especiais fora de λ, α, β, ², ³, Σ (`*` e `-` são os de teclado); citações sem leitura (cruze com `leitura_referencias/`); referências citadas e ausentes da lista, e o contrário; ABNT (NBR 6023 e 10520) nas referências e chamadas; legenda de figuras e tabelas com "Fonte:".
3. **Clareza para um graduando e fluxo:** parágrafos longos demais, jargão sem explicação, ordem das ideias. Dê exemplos de reescrita para os 10 piores trechos (texto proposto, curto).
4. **Cobertura dos objetivos:** a seção 1.3 promete algo que as seções 4 a 6 não entregam, ou entregam algo que não é objetivo?

## 3. Formato do relatório

`Notas Claude/revisao_processo_29-10.md`: um resumo de 10 linhas no topo (os 5 problemas mais graves e a recomendação), depois R1, R2 e R3. Cada achado: **gravidade** (crítico: muda uma conclusão ou um número; importante: erro ou risco que a banca notaria; menor: estilo ou detalhe), **onde** (arquivo e trecho citado), **evidência** (número, linha de código ou fonte) e **sugestão de correção** (texto ou valor). Não repita elogios; só problemas, dúvidas e o que foi conferido e está certo, em uma linha cada ("conferido: ...").

## 4. Regras

1. Não edite o Google Doc nem use ferramentas do Google. Não altere os arquivos das outras sessões (propostas, notas, scripts, tabelas): só crie `revisao_processo_29-10.md`, `progresso_revisao_29-10.md` e, se precisar guardar o código das recomputações, `Scripts/revisao_29-10/*.py`.
2. Nada de métodos descartados nos textos que você **propuser** (veja as regras na tarefa da noite, `tarefa_noturna_29-10.md`, seção 2); no relatório de revisão você pode citá-los para apontar violações.
3. Seja honesta sobre incertezas: se não conseguir verificar algo (sem rasters, sem acesso a um artigo), diga "não verificado" e por quê.
4. Português simples. Não abra pull request nem faça merge.
