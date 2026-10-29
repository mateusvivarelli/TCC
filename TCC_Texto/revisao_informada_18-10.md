# Revisão informada do TCC (PDF "TCC arquivo", 56 páginas) — 18/10/2026

Método: li o PDF inteiro (texto e imagens das páginas), o README, as notas (seções 15 a 25), `checagem_TCC_arquivo_17-10.md`, o rascunho 04, as tabelas, as figuras finais, o artigo da IC e o artigo de Hao et al. Refiz os cálculos do zero com os dados brutos (cópia da lógica de `gerar_tabelas_tcc.py` rodada fora do repositório, só leitura): leitura das séries horárias, dos rasters de K, C, LS, S e da chuva IDW, calibração e validação cruzada do MC, do MFM, da IC e dos testes simples, intervalos por bootstrap. Nada foi gravado no repositório nem no Google Docs.

Legenda: **NOVO** = não estava em `checagem_TCC_arquivo_17-10.md` (inclusive o adendo de 18/10); **JÁ CONHECIDO** = já listado lá e ainda presente neste PDF.

---

## (a) Resumo e prioridades

**Resumo em 10 linhas.**
1. Os números do texto estão corretos. Reproduzi do zero as Tabelas 2, 3, 8, 10, 11, 12 e 13, os parâmetros c₁ e c₂ (MC 0,00352 / 0,01311; MFM 0,00986 / 0,00114; IC 0,978 e 0,733), as métricas de validação cruzada, a soma de E_unit do evento 11 (30.003), as estatísticas dos rasters (S, LS, K, C, CN, pixels, áreas) e as correlações entre mapas (0,966; 90,9%; 0,69). Todos batem.
2. O defeito mais grave é de forma, não de conteúdo: no PDF, **a imagem da Figura 11 está presa ao cabeçalho e se repete no topo das páginas 11 a 56**, e a Figura 11 não aparece no seu lugar do corpo do texto (NOVO).
3. A metodologia ainda não descreve os testes simples e a IC, mas os resultados (5.4, 5.5, Tabela 8, Tabela 11) dependem deles. A seção que sustenta a Conclusão 2 e uma frase do Resumo ("recalibrar o SCS-CN … não o resolveu") não está no texto. O rascunho 04 já tem as seções 4.9, 4.10, 5.2, Limitações e os Apêndices B, C e D prontos para colar.
4. Há alegações mais fortes do que a evidência permite: "a espacialização não perde precisão" e "o gargalo é transformar chuva em escoamento". Com 17 eventos, o que se mostrou foi "não se detectou diferença". Além disso, o ganho MC→MFM vem em boa parte da **vazão de base medida**, que sai do mesmo hidrograma que gera SY_obs (circularidade).
5. As colunas "Q inicial" da Tabela 2 e "vazão inicial" do Resumo e dos Resultados são na verdade a **vazão de base no início (Bt)**, não a vazão medida (NOVO, verificado nos dados).
6. Acabamento: sumário desatualizado (faltam 5.x e 6, páginas erradas), equações do Docs com glifos quebrados, folha de aprovação ausente, tabelas cortadas, Figuras 8 a 10 ilegíveis.
7. A bibliografia está correta onde pude conferir: os DOIs e dados de Murillo-Bermúdez 2023, Valle Junior 2019, Baert 2026, Sartori 2005 e Murillo-Bermúdez e Martim 2022 batem no Crossref. O 4º autor de Murillo-Bermúdez 2023 é **DALFRÉ FILHO, J. G.**
8. A parte espacial é a menos validada: o mapa de áreas críticas representa 14% da carga medida no MC (190 t por evento contra 1.403 t), não tem validação espacial e depende de K e C por classe vindos da IC.
9. Quase todas as pendências de conteúdo já estavam em `checagem_TCC_arquivo_17-10.md`; marquei abaixo o que é novo.
10. Vale ensaiar as perguntas da banca da seção (d), em especial as sobre o evento 1B excluído, a circularidade do MFM e a escolha de AMC I.

**As 5 prioridades.**
1. Corrigir a Figura 11 (imagem no cabeçalho) e as equações do Docs com glifos quebrados.
2. Completar a lógica do texto: colar 4.9 (testes simples), 4.10 (IC), a seção do SCS-CN que não prevê o escoamento direto (com Tabela de λ), Limitações e Apêndices. Sem isso, a Conclusão 2 e o Resumo ficam sem suporte.
3. Moderar as alegações ("não perde precisão", "gargalo", "permite direcionar medidas de contenção") e declarar a incerteza (IC por bootstrap, n = 17, circularidade do MFM e da IC).
4. Corrigir rótulos e números: "Q inicial" é Qb_inicio; Tabela 9; Tabela 7; Baert (154 eventos de escoamento, 46 com sedimento); "cruzamento uso × solo" nas seções 2.6 e 4.2.3 (o CN vem da ANA); Figura 5 (E_unit em "kg por pixel").
5. Formato: atualizar o sumário, incluir a folha de aprovação, preencher ou remover dedicatória e agradecimentos, e rever tabelas cortadas, Figuras 8 a 10, a folha de rosto e o espaçamento.

---

## (b) Achados

### B1. Formato e figuras (PDF)

**B1.1 — Figura 11 presa ao cabeçalho (gravidade ALTA, NOVO).**
- Local: p. 11 a 56 do PDF (topo de todas as páginas depois da Introdução); Figura 11, seção 5.6.2, PDF p. 50.
- Evidência: o PyMuPDF lista a imagem `xref 61` (1259 × 2046 px) em todas as páginas de 11 a 56, na mesma posição (98,38 a 537,308 pt). O número da página fica logo abaixo dela. Na p. 50, entre o parágrafo e a legenda "Figura 11…" não há imagem no corpo: a imagem que se vê é a do cabeçalho.
- Problema: a imagem foi colocada no cabeçalho (ou ancorada como "fixa na página") em vez de inline. Consome cerca de um quarto de cada página e tira o número da página do lugar.
- Sugestão: no Docs, abrir Inserir > Cabeçalhos e rodapés, apagar a imagem do cabeçalho e inserir `figuras/mapas/mapa_07_sedimento_medio.png` inline na seção 5.6.2. Depois reexportar o PDF e conferir se o espaçamento voltou ao normal (a entrega ao SIGA deve ser o PDF).

**B1.2 — Sumário desatualizado (ALTA para a entrega; NOVO quanto às páginas, JÁ CONHECIDO quanto à falta de itens).**
- Local: p. 9.
- Evidência: o sumário diz Resultados na p. 30 e Referências na p. 31, mas o texto está nas páginas impressas 40 e 53 (PDF 41 e 54). A 4.9 está listada na p. 28 e está na p. 38. Faltam 5.1 a 5.6, 6 CONCLUSÕES e os itens 3 e 5 estão com tamanhos de fonte diferentes. O número impresso no topo está uma unidade abaixo do índice do PDF (a p. 11 mostra "10"). O sumário parece listar a Introdução na p. 10, que coincide com o índice PDF e não com o número impresso. Há inconsistência entre o número impresso e o do sumário.
- Sugestão: no Docs, clicar no sumário e "Atualizar sumário"; fixar os títulos como Título 1/2/3 para entrarem sozinhos; uniformizar a fonte; definir o número da página inicial para que a Introdução seja a p. 1 ou 9, coerente com o sumário. Considerar numerar sem ponto (norma do modelo: "1 INTRODUÇÃO").

**B1.3 — Equações do Docs com glifos quebrados (ALTA, NOVO).**
- Local: 4.4 (p. 33–34 do PDF: equações do pr e do E_unit), 4.5 (equação do SY, p. 35), 4.6 (equação de calibração, p. 36), 2.2 (p. 13).
- Evidência (nas imagens): "𝑝𝑟⍰ = (𝑄⍰ / 1000)·𝐴⍰ix…": o subscrito k virou caixa vazia. Em E_unit: "(𝑄𝑘 · 𝑝𝑟𝑘 · 𝐴𝑝𝑖𝑥)0,56" com o expoente não elevado e subscritos em linha. Em 4.5: "Σ⍰ 𝐸𝑢𝑛𝑖𝑡,𝑘" e "𝑄𝑏, 𝑖𝑛𝑖𝑐𝑖𝑜 · 𝑇𝑐ℎ𝑢𝑣𝑎". Em 4.6: "ln ln" duplicado e "mín" com subscrito deslocado. Na 2.2: "11, 8 * (𝑄* 𝑞𝑝)^0,56 *" com espaço depois da vírgula decimal e asterisco como produto.
- Problema: a equação central do trabalho aparece ilegível ou errada no PDF.
- Sugestão: redigitar no editor de equações do Docs, com `_` e `^` explícitos, "ln" como função, ponto médio "·" e a vírgula decimal sem espaço. Exemplo: `E_{unit,k} = 11,8 · (Q_k · pr_k · A_pix)^{0,56} · K_k · LS_k · C_k · P_k`. Conferir no PDF exportado, não só na tela.

**B1.4 — Figuras 8, 9 e 10 ilegíveis em A4 (MÉDIA, NOVO).**
- Evidência: 17 painéis em grade 4 × 5 numa largura de 16 cm; os títulos "Evento n (data; R = x mm)" ficam com cerca de 4 pt.
- Sugestão: dividir cada figura em duas (eventos 1 a 9 e 10 a 17) ou usar a página em paisagem; ou manter a grade e mover para o Apêndice, deixando no corpo uma figura com 4 eventos representativos (por exemplo 6, 11, 15, 16).

**B1.5 — Figura 2 (MÉDIA, NOVO).**
- Evidência: o arquivo `mapa_02_solo_uso.png` tem muito espaço em branco no topo e a legenda de uso é cortada embaixo (falta a linha "Solo exposto (0,5%)" completa, p. 25 do PDF). As porcentagens da legenda (Argissolos 17,7%; Cambissolos 68,5%; Silvicultura 12,6%) diferem das do texto e da Tabela 5 (17,6%; 68,6%; 12,7%). A figura calcula sobre a área da máscara da bacia; o texto, sobre os 153.855 pixels de cálculo.
- Sugestão: regerar a figura sem a faixa vazia e sem cortar a legenda (`gerar_mapas_tcc.py`) e usar na legenda a mesma base do texto, ou dizer "% da área da bacia (máscara)" e usar o mesmo número no texto.

**B1.6 — Rótulo de E_unit na Figura 5 (MÉDIA, NOVO).**
- Evidência: o painel "Índice de erosão E_unit" tem barra de cor "kg por pixel, sem calibrar", enquanto o texto da 4.4 diz que E_unit é um índice relativo e não uma massa.
- Sugestão: trocar para "E_unit (índice relativo, adimensional para efeito de comparação)".

**B1.7 — Demais figuras (BAIXA a MÉDIA, NOVO).**
- A Figura 1 não tem mapa de localização (inset do estado de SP / Brasil); em TCC, costuma ser esperado.
- As legendas de figura estão abaixo da figura; a ABNT NBR 14724 pede título acima e fonte abaixo. Confirmar com a biblioteca (a norma FEC de 2017 não detalha). Falta "Fonte:" em várias legendas (as figuras são elaboradas pelo autor, mas Fig. 2 e 3 usam dados do Plano de Bacias e da ANA).
- As Figuras 6 e 7 estão boas e legíveis. A Fig. 7 mostra bem que a base domina o MC.
- Figuras 3 e 4 já foram trocadas pelas versões corretas (LS novo; "T_chuva" na caixa do fluxograma). **Conferido, está certo.**
- Em geral, as figuras de mapa têm norte, escala gráfica, grade em km (UTM 23S) e barra de cor com unidade. Isso está bem feito.

**B1.8 — Tabelas cortadas entre páginas (BAIXA, NOVO).**
- Tabelas 3 (p. 23–24), 4 (p. 24–25), 5 (p. 25–26), 6 (p. 30–31), 10 (p. 42–43). O cabeçalho se repete, o que atenua. Há meia página em branco na p. 38 porque a Tabela 9 foi para a página seguinte.
- Sugestão: "manter linhas juntas" nas tabelas curtas (4, 5, 6) e quebra de página antes da Tabela 9, ou reduzir a Tabela 9 para caber na p. 38.
- Na Tabela 13, "Argissolos Vermelho-Amarelo/s" quebra a palavra: alargar a primeira coluna.
- Estilo: as tabelas têm bordas fechadas e fundo azul no cabeçalho; o padrão IBGE (ABNT) pede só linhas horizontais. É estético, opcional.

**B1.9 — Capa e folha de rosto (MÉDIA, parcialmente JÁ CONHECIDO).**
- Capa: segue o modelo (instituição, autor, título, cidade e ano). Falta, se desejado, "FEC" por extenso (já está).
- Folha de rosto: a norma pede "Trabalho Final de Curso apresentado como requisito parcial para obtenção do título de Bacharel em Engenharia Civil à Faculdade…" e "Orientador(a): Nome". No PDF está "…como requisito para a obtenção do título de Engenheiro Civil. Feito sob a orientação do Me. … e co-orientação do Prof. Dr. …". "co-orientação" deve ser "coorientação" (Acordo Ortográfico) e "Feito sob a orientação" é coloquial.
- Texto sugerido: "Trabalho Final de Curso apresentado como requisito parcial para obtenção do título de Bacharel em Engenharia Civil à Faculdade de Engenharia Civil, Arquitetura e Urbanismo da Universidade Estadual de Campinas. / Orientador: Me. Luis Fernando Murillo-Bermúdez / Coorientador: Prof. Dr. André Luís Sotero Salustiano Martim".
- Folha de aprovação ausente: a p. 3 está em branco (JÁ CONHECIDO). Dedicatória (p. 4) e Agradecimentos (p. 5) têm só o título e a página vazia; preencher ou remover (são opcionais). Uma página vazia com título parece inacabada.

**B1.10 — Espaçamento e fonte (BAIXA, JÁ CONHECIDO).**
- O corpo parece em Arial 12 com espaçamento próximo de 1,5; a checagem de 18/10 registra 1,15 no Doc. Confirmar qual vale (a norma dedutiva pede 1,5). As entradas de referência estão com espaço entre parágrafos irregular (USDA, Valle Junior, Vivarelli, Williams, Wischmeier sem o espaço) (p. 55).

### B2. Conferência de fatos e números

Tudo o que testei bate. **Reproduzido do zero e correto:**
- Tabela 2 (dados por evento) e Tabela 3 (volumes): totais 28.934 / 13.671 / 15.263 / 13.455 mil m³; razão total 0,88; proporção de base 34% a 55% (47% no total); SY total 23.846 t, média 1.403 t, de 199 a 3.829 t. A razão SCS-CN/medido por evento bate nos 17 (de 0,02 a 1,95). Dos 17 eventos, 11 têm SCS-CN abaixo do medido.
- Séries horárias: SY_obs e T_R, recalculados da planilha horária, batem com a planilha (diferença da ordem de 1e-16).
- Parâmetros: MC c₁ = 0,003521 e c₂ = 0,013106; MFM c₁ = 0,009858 e c₂ = 0,001136; IC α = 0,9782 e β = 0,7332.
- Métricas em validação cruzada: MC 32,6% / 70,6% / NSE-log 0,477 / Spearman 0,716; MFM 13,6% / 94,1% / 0,868 / 0,850; IC 16,3% / 100% / 0,867 / 0,931; c·chuva 41,9% / 82,4% / 0,534 / 0,630; c·V_total 17,6% / 94,1% / 0,860 / 0,875; teste simples MC 37,7% / 70,6%; teste simples MFM 19,5% / 94,1%. Bate com as Tabelas 10 e 11, com o Resumo e com a Figura "escada".
- Evento 15 = 48,69% da variância linear; os três menores em log (6, 12, 1) = 68,5% da variância em log.
- Parcela das encostas: mediana 9,3% (máx. 35%) no MC e 38,4% no MFM.
- Evento 11: soma de E_unit 30.003; encostas 105,6 t; base 1.025,2 t; ajuste 1.130,9 t (−37,9%); LOO MC 1.097,6 t (−40%); LOO MFM 1.710,6 t (−6%).
- Erros por evento da Tabela 10 (MC, ajuste e LOO): todos conferem com `comparacao_SY_dois_componentes.csv`.
- Rasters: grade 884 × 365; pixel 29,992 × 29,925 m (897,49 m²); 153.855 pixels de cálculo = 138,08 km²; S médio 255,7 (de 12,3 a 558,2 mm); K 0,0388; C 0,0495; LS 7,82 (de 0,0007 a 40,3; mediana 6,76).
- Mapas: correlação MC × MFM 0,966 (Spearman 0,996); coincidência dos 5% superiores 90,9%; correlação do mapa MC com K·LS·C 0,692 (Spearman 0,789; para o MFM é 0,633).
- Tabelas 12 e 13: áreas, % e kg/pixel conferem; somas ≈ 100%.
- Contas à mão: pr do pixel de exemplo = 4,65 · 10⁻⁴ m³/s; E_unit com os valores arredondados da tabela ≈ 1,04; CN_II 81,0 → CN_I 64,2 e S 141,9 mm conferem.
- Literatura conferida nos PDFs: Hao (1.314 bacias; conectividade < 0,5 em cerca de 80%), Brandão (3.578 bacias; λ = 0,05 melhor; associações com regiões áridas, lavoura, áreas urbanas e solo arenoso), Baert (NSE-volume ≤ 0,13 e 0,21 a 0,40).
- IC: K 0,031, LS 0,536, C 0,267, α 0,277, β 0,807 e erros (−4,15%, de −60,01% a +37,14%; −29,58%; máx. 57,28%) conferem com o artigo da IC.

**Divergências e imprecisões encontradas (detalhe em (c)):**

**B2.1 — "Q inicial" é na verdade Qb_inicio (ALTA, NOVO).**
- Local: Tabela 2 (coluna "Q inicial", legenda "vazão antes do evento"), Resumo ("vazão inicial"), 5.2 ("só chuva e vazão inicial"), Tabela 11, Tabela 6 ("vazão no início do evento"), 4.5.
- Evidência: em `Scripts/gerar_tabelas_tcc.py` a coluna "Q inicial" usa `Qb_inicio`, que é o primeiro valor de Bt da janela. Comparado com a primeira leitura de Q na mesma janela: evento 11, Q = 1,869 e Bt = 0,945; evento 10, 3,708 e 2,539; evento 5, 3,717 e 1,712; evento 4, 2,440 e 1,589. Só no evento 1 são iguais. Num texto que insiste que "vazão" e "vazão de base" são coisas diferentes, o leitor vai entender Q.
- Sugestão: renomear a coluna para "Qb início (m³/s)" e a legenda para "vazão de base no início do evento", e substituir "vazão inicial" por "vazão de base inicial" em todo o texto, incluindo Resumo, Abstract e Tabela 11 ("chuva, vazão de base inicial").

**B2.2 — Evento 12 e Evento 1B (MÉDIA, NOVO em parte).**
- Evento 12: DBT5 = 0,0 mm em todas as horas (nenhuma lacuna na série; 91% das horas do posto são zero), enquanto Campo Limpo registra 32,8 mm numa hora. No texto, "o DBT5 não registrou chuva" pode ser falha do posto ou chuva localizada; a IDW com dois postos faz o posto zerado puxar a chuva para baixo a leste. Vale uma frase.
- Evento 12: a CSS sobe a 4.602 mg/L às 19h enquanto Q só salta de 1,06 para 13,1 m³/s às 21h. Há descompasso de 2 h entre a turbidez (medida na ETA da SABESP) e a vazão (estação DAEE, distinta). Isso afeta SY_obs = Σ Q · CSS nos eventos curtos (o 12 tem 24 leituras). A turbidez vem da ETA, a vazão do posto do DAEE, e o exutório do modelo fica 894 m a jusante da estação (`dados_area_estudo_plano_bacias.md`, comentário #6). Nenhuma dessas diferenças de local está no texto (Tabela 1 diz que CSS vem da "seção de controle").
- Evento 1B: a planilha tem 18 eventos (linha "1B": 24/11 a 26/11/2018; P = 9,4 e 37,6 mm). O texto usa 17 sem explicar a exclusão (a pendência existe no rascunho 04, Limitações c, com "[PENDENTE]"). A banca vai perguntar.

**B2.3 — Área da bacia e área de cálculo (BAIXA, NOVO).**
- Evidência: o texto declara 137,8 km² (acumulação de fluxo) e, na 3.3 e 4.2.1, 138,1 km² de área de cálculo, maior que a da bacia. As notas registram ainda 138,84 km² (shapefiles) e 138,58 km² (máscara). Ver comentário #6 antigo, que continua sem resposta (JÁ CONHECIDO, item 22 da checagem).
- Sugestão: uma frase: "A área de 137,8 km² vem da acumulação de fluxo do MDE corrigido; a área dos pixels de cálculo (138,1 km²) difere por efeitos de borda e de reamostragem, cerca de 0,2%".

**B2.4 — Fórmula do pr difere da de Hao (BAIXA, NOVO).**
- Evidência: na Eq. (4) de Hao, pr = RI/(3600 · R) · Q · Area, sem o fator 1/1000 que o TCC inclui (Q em mm, A em m²). O TCC usa o fator para obter m³/s e a 4.4 diz "como em Hao et al. (2022)". Como Q entra em E_unit em mm, o efeito é um fator constante que c₁ absorve (1000^0,56 ≈ 47,9). Não muda resultado, mas "seguindo Hao" deve dizer que a conversão de unidade foi explicitada.

**B2.5 — Peso do posto (BAIXA, NOVO).**
- Tabela 6 e Tabela 8: "0,307 / 0,693 — mínimos quadrados nos 17 eventos". Ajustado a quê? A resposta correta, segundo o script: contra a lâmina de chuva do evento da planilha (`Chuva_evento_mm`), uma ponderação feita fora do trabalho. Dizer isso na 4.2.1. Não há vazamento com SY, mas a origem da ponderação original é desconhecida (já observado na `revisao_independente.md`).

### B3. Consistência interna (siglas, seções, citações)

**B3.1 — "IC" sem definição (MÉDIA, NOVO).** A Seção 1.1 escreve "Iniciação Científica anterior" sem "(IC)". A sigla aparece pela primeira vez no Objetivo 5, na Tabela 4 e na Tabela 8. IC também é a sigla usual de índice de conectividade (Hao et al., 2022), o que pode confundir quem conhece o artigo. Sugestão: em 1.1 escrever "uma Iniciação Científica anterior (IC; VIVARELLI et al., 2025)" e usar "IC" só para o trabalho anterior; a formulação concentrada pode ser "MUSLE concentrada da IC". Também definir AMC, MDE, SABESP, PCJ; a lista de siglas é opcional, mas ajuda neste texto.

**B3.2 — Objetivos prometem comparações que a metodologia não descreve (ALTA, JÁ CONHECIDO).** O Objetivo 5 (testes simples e IC) e o Objetivo 6 (identificar o fator limitante) não têm seção de metodologia correspondente: a 4.1 foi cortada nesse ponto. A Tabela 8 traz uma linha "IC refeita: α e β" com K = 0,031, LS = 0,536 e C = 0,267, números que contradizem a Tabela 4 (K 0,039; LS 7,80; C 0,050) sem explicação. O rascunho 04 já traz as seções 4.9 e 4.10 que explicam (inclusive que a diferença no LS não afeta a IC porque α é recalibrado).

**B3.3 — Remissões quebradas (MÉDIA, JÁ CONHECIDO).**
- 5.4 cita "(Tabela 13)" para modelo × teste simples; deve ser Tabela 11.
- 4.7 cita Apêndice C e 4.8 deveria citar Apêndice B, ambos inexistentes no PDF.
- 5.5 começa com a Tabela 11 antes do texto que a apresenta.
- Estado atual: a numeração das seções 5.1 a 5.6 e das Tabelas 1 a 13 e Figuras 1 a 11 está contínua e todas as tabelas e figuras são citadas (as pendências de 18/10 sobre 5.6, Tabelas 2 e 6 e Figura 6 já foram resolvidas).

**B3.4 — CN "do cruzamento do uso com o solo" (MÉDIA, parte JÁ CONHECIDO, parte NOVO).**
- 2.6 diz "O número de curva resulta do cruzamento dos mapas de uso e de solo" (JÁ CONHECIDO, pendência 3 do README).
- A seção **4.2.3** repete: "O CN foi obtido do cruzamento do uso com o solo" (NOVO). Isso contradiz a 3.3, que informa corretamente a base BR_CN-2022 da ANA, e a Tabela 4.
- Sugestão: "O CN foi obtido da base nacional da ANA (seção 3.3), na condição de umidade média (AMC II), e convertido para a condição seca (AMC I) por …".

**B3.5 — Notação de Q (MÉDIA, NOVO).** Em 2.2, Q é volume (m³); em 2.3, 4.3 e 4.4, Q é lâmina (mm); em 4.5, Q "igual ao escoamento direto". Sugestão: em 2.2, usar V (m³) ou escrever Q_vol; em 4.3 em diante, manter q (mm) para a lâmina. Do mesmo modo, "SY", "Y", "carga", "sedimento medido" e "produção de sedimentos" se alternam. Escolher: SY_obs = carga de sedimentos medida; SY = produção de sedimentos estimada.

**B3.6 — Equação Universal Modificada (BAIXA, NOVO).** A 1.1 escreve "Equação Modificada de Perda de Solo (MUSLE…)"; o Resumo e a 2.2 usam "Equação Universal Modificada…". Padronizar.

**B3.7 — Citações e referências (ABNT) (BAIXA).**
- Citações: todas as citadas estão na lista e vice-versa (conferido). A forma "Hao et al. (2022)" no corpo e "(AUTOR, ano)" entre parênteses está de acordo com a ABNT; "(MURILLO-BERMÚDEZ et al., 2023)" já foi corrigido.
- 4º autor de Murillo-Bermúdez et al. 2023: o Crossref dá "J.G. Dalfré Filho". Referência correta em ABNT: `MURILLO-BERMÚDEZ, L. F.; MARTIM, A. L. S. S.; POLETO, C.; DALFRÉ FILHO, J. G. Correlation of turbidity …` (sem espaço antes do ponto). JÁ CONHECIDO como dúvida; agora **confirmado**. O Crossref registra o fascículo de 2023 (abril) e a publicação on-line em 2021; o DOI com "2021" está certo e o ano da ref (2023) também.
- Confirmados no Crossref: Baert et al. (Catena, 274, 110497, 2026, 5 autores); Valle Junior, Rodrigues e Oliveira (RBRH 24, e5, 2019); Sartori, Lombardi Neto e Genovez (RBRH 10(4), 5–18, 2005); Murillo-Bermúdez e Martim (2022, p. 56–60, DOI iwisdw.n1.2022.4793).
- Conferidos no PDF do repositório: Hao (J. Hydrol. 614, 128579), Brandão (J. Hydrol. 655, 132941).
- **Não pude confirmar online:** Eckhardt 2005 (confio no conhecimento próprio: HP 19(2), 507–515), Nash e Sutcliffe 1970, Moore e Burch 1986 (confio: SSSAJ 50(5), 1294–1298), Lyne e Hollick 1979 (páginas 89–93: a `referencias_consolidadas.md` já marca "conferir páginas"; não confirmei), Chow et al. 1988, Williams 1975, Wischmeier e Smith 1978, USDA-SCS 1972.
- VIVARELLI et al. (2025): "Artigo (Iniciação Científica)" é vago. O PDF do artigo não indica evento nem periódico. Se foi publicado ou apresentado, citar o evento (ou, se for só o texto do PIBIC, citar o relatório: `Relatório Final de Atividades PIBIC 2024/2025`). Autores no artigo: Vivarelli, Murillo-Bermúdez, Palha Braga e Martim; "et al." está certo.
- Referência da epígrafe: a ABNT não exige; só incluir se a biblioteca pedir.
- O DOI da ANA é um URL longo que quebra a linha; usar a forma curta do catálogo, se existir.

### B4. Completude frente à norma e à lógica do trabalho

**B4.1 — Elementos obrigatórios (norma FEC):** capa ✓, folha de rosto (ajustar, B1.9), **folha de aprovação ✗ (ALTA, JÁ CONHECIDO)**, resumo (224 palavras, dentro do limite de 500) ✓ com palavras-chave ✓, abstract ✓, sumário ✓ (desatualizado), introdução com justificativa e objetivos ✓, fundamentação ✓, metodologia (incompleta), resultados e discussão ✓, conclusão ✓, referências ✓. Listas de figuras e tabelas são opcionais, mas com 11 figuras e 13 tabelas ajudam; lista de siglas idem.

**B4.2 — O que falta e o rascunho 04 já tem pronto (JÁ CONHECIDO, ALTA):**

| Falta no PDF | Onde está pronto no rascunho 04 | Observação |
|---|---|---|
| 4.9 Testes simples e referências sem MUSLE | seção 4.9 | colar; renumerar o Exemplo para 4.11 |
| 4.10 Comparação com a IC | seção 4.10 | colar |
| Seção "O SCS-CN não prevê o escoamento direto", com Tabela 10 (λ) | 5.2 e Tabela 10 do rascunho | sustenta a Conclusão 2 e uma frase do Resumo; ver B5.4 |
| Tabela por evento MC × MFM × IC × c·chuva | `tab_resultados.md` (gerada, já com LS novo) | incluir (a Figura 6 depende dela) |
| Tabela da escada (testes simples) e figura | `escada_gargalo.csv`, `escada_gargalo.png` (conferidas, batem com o texto) | placeholder `{{TABELA_ESCADA}}` ainda não expandido |
| Limitações | seção 6 | ver B5.7 |
| Trabalhos futuros | Conclusão 6 | ausente no PDF |
| Apêndice B (NSE linear com e sem o evento 15) | pronto (Tabela 17) | necessário para a 4.8 |
| Apêndice C (versões intermediárias N2/N3) | placeholder `{{TABELA_INTERM}}` | gerar com `md_para_docx.py` |
| Apêndice D (calibração chuva-escoamento) | pronto, com a **pendência de LS antigo** nas colunas de sedimento | ver B5.4 |
| Apêndice A (evento 11 nas planilhas) | só "[PENDENTE]" | opcional; a Seção 4.9 e a Figura 5 já fazem o essencial |

**B4.3 — Pendências de conteúdo (JÁ CONHECIDO):** a frase de justificativa da AMC I na 4.3 já foi trocada, mas a nova versão ainda diz "herdada da fase em que o modelo foi calibrado contra o volume total", o que o texto deveria evitar (ver B5.5). A equação CSS = 3,264 · Turb^0,7974 (comentário #3) continua sem aparecer; ela ajudaria a mostrar a origem de SY_obs. O MC no bullet da 4.5 ainda diz "a base é o volume de referência acima".

**B4.4 — Elementos ausentes que um leitor esperaria (NOVO):** incerteza dos dados observados (curva de descarga do DAEE, curva turbidez–CSS, amostragem horária, descompasso entre turbidez e vazão); discussão do que o modelo não inclui (erosão de margens e voçorocas, fontes urbanas, deposição em canal) e o que isso significa para "SY no exutório" × "erosão nas encostas".

### B5. Rigor científico e honestidade das alegações

**B5.1 — "A espacialização não perde precisão" (ALTA, NOVO quanto ao PDF; o rascunho 04 já moderava).**
- Local: 5.4 (p. 44), 5.5 (p. 45), Resumo, Abstract e Conclusão 5.
- Evidência (bootstrap por eventos, 20 mil reamostragens, reproduzi os intervalos do rascunho): diferença mediana do erro percentual entre o modelo e o teste simples, MC: +3,0 pontos, IC95% [−3,7; +11,6]; MFM: −4,1 [−11,7; +6,6]. MC − c·chuva: −2,1 [−14,0; +18,8]. IC − MFM: +1,5 [−7,5; +10,3]. Todos incluem zero e as larguras (cerca de ±10 pontos) são do tamanho do erro mediano (14% a 38%). Intervalos do próprio MedAPE: MC [21; 61], MFM [3; 34], IC [6; 23]. A fração dentro de fator 2 tem IC binomial largo (12/17: 44% a 90%; 16/17: 71% a 99,9%).
- Problema: com n = 17, "não perde precisão" lê-se como equivalência demonstrada; só se mostrou que não há diferença detectável. Na 5.4 o PDF já diz "equivalentes".
- Texto sugerido para a 5.4: "Com os mesmos insumos, o modelo de dois componentes e o teste simples têm desempenho semelhante (Tabela 11). Com 17 eventos, a diferença do erro mediano por evento não é distinguível de zero (IC de 95% por bootstrap de −3,7 a +11,6 pontos no MC e de −11,7 a +6,6 no MFM). Não se detectou, portanto, perda de precisão com a espacialização, nem ganho: a contribuição do modelo espacializado é o mapa."
- Para o Resumo e a Conclusão 5, trocar "mantém a qualidade da formulação concentrada" por "não apresentou perda detectável de precisão em relação à formulação concentrada quando recebe informação equivalente".

**B5.2 — O "gargalo" e a circularidade do MFM e da IC (ALTA, NOVO quanto ao PDF; parte já nas notas).**
- Evidência: (i) o MFM usa V_base = Σ Bt · 3600 e V_dir = T_R − V_base, ambos tirados do mesmo hidrograma e da mesma janela que dão SY_obs = Σ Q · CSS · 3600. A SY_obs é, aritmeticamente, o volume total vezes uma CSS média ponderada, de modo que acertar o volume já acerta boa parte da carga. Isso é visível: SY = c · V_total (sem MUSLE e sem espaço) tem 17,6% / 94% / NSE-log 0,86, quase igual ao MFM (13,6% / 94% / 0,87). O MFM, portanto, não mostra "desempenho possível do modelo espacial", mostra que o volume medido explica a carga. (ii) O nível N3 da escada (escoamento direto medido, base prevista) tem fator 2 de 94% mas erro mediano de 34% (teste simples: 24%); o erro mediano só cai a 14% quando a **base também é medida**. Logo, o ganho MC→MFM em erro mediano vem sobretudo da base medida, e a base medida é a parte mais circular. (iii) A mesma observação vale para a IC (D e q_p medidos do próprio hidrograma); o texto já avisa isso na 5.5 ("não prevê").
- Problema: o Resumo diz "o gargalo está em transformar chuva em escoamento", mas a evidência diz "o gargalo está em estimar a água do evento, escoamento direto e vazão de base, e a vazão de base é a que mais pesa em erro mediano".
- Texto sugerido para o Resumo: "…o acerto sobe a 94% e o erro mediano cai a 14%. A melhora exige a água medida, e a vazão de base medida é a parte que mais pesa; estimar a água do evento a partir da chuva é, portanto, o principal limite."
- Para a 5.3, acrescentar: "Como o escoamento direto e a vazão de base medidos vêm do mesmo hidrograma que gera a carga medida, o MFM deve ser lido como referência de decomposição do erro, não como desempenho esperado de uma aplicação."

**B5.3 — O mapa é a parte menos validada, e o texto sugere uso prático (ALTA, NOVO).**
- Evidência: no MC, a soma dos mapas é 190 t por evento contra 1.403 t medidos (13,6%); no MFM, 535 t (38%). Em mediana, as encostas respondem por 9% do SY simulado no MC. O resto é o termo empírico Qb_inicio · T_chuva. O mapa tem escalas 2,8 vezes diferentes entre MC e MFM (Figura 11: 0 a 17 contra 0 a 49 kg por pixel), efeito de c₁. A correlação do mapa com K·LS·C é 0,69 (MC) e 0,63 (MFM), ou seja, o padrão é metade (r² ≈ 0,48 e 0,40) dos fatores fixos, o resto é CN, chuva e não linearidade. A coincidência de 90,9% entre MC e MFM só mostra que os dois usam o mesmo K, C, LS e padrão SCS-CN (o texto já avisa). Não há validação espacial, e a ordem das classes depende de K e C herdados da IC e de C = 1 para solo exposto, mineração e afloramento rochoso (classes que somam 0,5% da área e 10% do sedimento no MC, 15% no MFM).
- Problemas: (1) 5.6.1 diz que o padrão espacial "é dominado pelos fatores fixos" e 5.6.2 diz que "carrega também informação da chuva e do escoamento" (tensão de redação; r = 0,69 é moderado). (2) O Resumo diz que o mapa "permite direcionar medidas de contenção". (3) A erosão em áreas urbanas (14% da bacia) é nula por construção (K = 0 e C = 0), embora elas tenham o CN mais alto e sejam fonte conhecida de sedimento em obras. (4) Faltam fontes não modeladas (margens, canais).
- Sugestões: no Resumo, "…acrescenta um mapa relativo de áreas críticas, ainda não validado no espaço, que indica onde priorizar a investigação de campo". Em 5.6.1, trocar "dominado" por "fortemente condicionado". Em 5.6.2, listar as classes de C = 1 como as de maior contribuição por pixel (solo exposto 23 kg/pixel; mineração 44), com a ressalva da ponderação.

**B5.4 — Conclusão 2 e frase do Resumo sem suporte no PDF (ALTA, JÁ CONHECIDO).**
- O Resumo diz "recalibrar o método SCS-CN contra o escoamento direto não o resolveu" e a Conclusão 2 afirma "NSE do volume negativo para qualquer λ testado" e "Recalibrar a conversão melhora o volume, mas não o sedimento". O PDF não tem nenhuma tabela, nenhum teste ou apêndice que mostre isso. Só a nota técnica de 5.1.
- Solução: colar 5.2 e o Apêndice D do rascunho 04. Atenção: no Apêndice D as colunas de sedimento das linhas (i) a (iii) e da linha "Teto, padrão espacial λ = 0,05" ainda usam o LS antigo. O rascunho avisa isso em um [PENDENTE]. As conclusões (a) a (e) provavelmente não mudam porque o LS entra como fator e c₁ é recalibrado, mas o texto diz o LS "antigo" nessas células; deixar explícito na legenda da Tabela 19: "valores de sedimento calculados com o fator LS da IC; o fator entra de forma multiplicativa e a escala é recalibrada, de modo que não se esperam mudanças qualitativas".
- Verifiquei no rascunho 04: os números que entram em 5.2 (razão mediana 0,59) diferem por arredondamento do que reproduzi (0,584); usar 0,58.

**B5.5 — Parâmetros e escolhas feitas olhando os mesmos 17 eventos (MÉDIA, NOVO no PDF).**
- A validação cruzada refaz c₁ e c₂ em cada rodada, mas λ = 0,20, AMC I, a duração da chuva (e não a do hidrograma), a calibração em log e o descarte de outras formas foram decididos depois de ver diagnósticos nos mesmos eventos (nota §21 e §23: "o otimismo de seleção é cerca de 0,03 no NSE-log"). A validação é "aninhada" só quanto a c₁ e c₂. A seção 4.7 diz "A validação é aninhada: qualquer etapa que dependa de ajuste … é refeita"; isso é verdade para as etapas ajustadas, mas não para a escolha da forma do modelo. Dizer isso na 4.7 e nas Limitações (o rascunho 04 tem os itens i e l).
- Texto sugerido para a 4.7: "A validação cruzada refaz os parâmetros ajustados (c₁, c₂ e os dos modelos de comparação) sem o evento retido. A escolha da forma do modelo (λ = 0,20, AMC I, duração da chuva no termo de base, calibração em escala logarítmica) foi feita com os mesmos 17 eventos, de modo que o desempenho reportado ainda carrega algum otimismo de seleção."

**B5.6 — Desempenho do MC não é melhor que a referência trivial (MÉDIA, JÁ CONHECIDO nas notas, NOVO no PDF).**
- O PDF diz que o MC é "equivalente" ao c·chuva. Dados: MC 32,6% / 71% / 0,48 / 0,72; c·chuva 41,9% / 82% / 0,53 / 0,63. O MC tem erro mediano e Spearman melhores, o c·chuva tem fator 2 e NSE-log melhores. De fato, "equivalente, dentro do ruído". O Resumo e a 5.3 deveriam dizer isso com a mesma clareza.
- NSE linear do MC é negativo (−0,64 na validação cruzada; −1,58 sem o evento 15) e o do c·chuva é +0,58; isso está só no Apêndice B do rascunho. Se o Apêndice B não for colado, um leitor que conheça o NSE linear (como em Hao et al.) vai querer ver. Recomenda-se incluir pelo menos uma frase em 5.2 ou nas Limitações.

**B5.7 — Limitações ausentes (ALTA, JÁ CONHECIDO).** A seção 6 do rascunho 04 já tem os itens (a) a (l). Os mais importantes, se for preciso cortar: (a) só o MC é previsão; (b) a parte espacial pesa pouco sem volume medido; (c) 17 eventos, um deles com 49% da variância, IC largos e o evento 1B excluído; (e) sem validação espacial; (f) vazão de base e carga total; (h) RI/R > 1/h nos eventos 1 e 12 (RI é o máximo entre postos e R é a lâmina ponderada, fisicamente impossível; confirmado: RI/R = 1,01 e 1,38), o que superestima pr nesses dois eventos; (i) CN da ANA (MapBiomas 2022) × K e C do Plano de Bacias (2020); (j) a duração da chuva só é conhecida ao fim da chuva. Acrescentar (NOVO): incertezas de medição de SY_obs, descompasso entre turbidez (SABESP) e vazão (DAEE), exutório 894 m a jusante da estação, urbanas com erosão nula por construção, erosão de margens e canais não modelada, e que c₁ não é razão de entrega.

**B5.8 — Vazão de base: "método não documentado" × filtro de Eckhardt (MÉDIA, JÁ CONHECIDO).** A Tabela 1 e a 2.4 dizem que o método não está documentado. A checagem de 17/10 mostrou que Eckhardt com a = 0,995 e BFImax = 0,698 reproduz Bt (mediana de 2 · 10⁻⁴ m³/s). Há também uma verificação que fiz: Bt ≤ Q em todas as horas da série (0 violações), consistente com um filtro recursivo causal, o que reforça que Qb_inicio (primeiro Bt da janela) não usa informação do futuro. Decidir com o orientador se se escreve "consistente com o filtro de Eckhardt (a = 0,995; BFImax = 0,698), cuja aplicação pelos fornecedores não foi confirmada". O parágrafo está pronto no rascunho 04 (3.2).

**B5.9 — Termo de base como "indicador" (MÉDIA, NOVO).** A 4.5 apresenta o termo c₂ · Qb_inicio · T_chuva · 3600 como "contribuição da vazão de base". No MC, ele responde por 91% (mediana) do SY simulado, enquanto o rascunho 04 reconhece que "funciona como indicador do tamanho e da duração do evento; não deve ser lido como processo físico isolado". Essa frase deve estar no PDF (5.2), porque o texto atual induz à leitura física ("é fisicamente coerente" na Conclusão 3). Sugestão: trocar "fisicamente coerente" por "conceitualmente coerente (separa a água das encostas da água de base)" e acrescentar a frase do rascunho.

**B5.10 — Riscos de vazamento (resumo).**
- Calibração e avaliação: refeitas sem o evento retido para c₁ e c₂ (ok). A IC usa D e q_p do mesmo hidrograma (circular, reconhecido).
- MC: Qb_inicio é causal (sem vazamento); T_chuva só é conhecido ao fim da chuva (limitação j); RI e R vêm da chuva medida.
- O peso do posto (0,307) vem da chuva, não do sedimento (sem vazamento).
- O fator f do MFM (V_dir/V_SCS) usa o volume medido do evento (por definição).
- λ e AMC I foram escolhidos olhando o volume medido (diagnóstico com os 17 eventos), antes de se calcular o SY: leve vazamento de seleção, ver B5.5.
- O descarte do evento 1B e a janela Inicio–Fim definida sobre o hidrograma que gera SY_obs não são vazamento do modelo, mas seleção de dados que deve ser explicada.

### B6. Escrita

**B6.1 — Ortografia e gramática (itens pontuais).**
- Resumo, 1ª frase: "(Modified Universal Soil Loss Equation; MUSLE), estima" tem vírgula entre sujeito e verbo. Sugestão: "A Equação Universal Modificada de Perda de Solo (*Modified Universal Soil Loss Equation*, MUSLE) estima a produção de sedimentos de bacias hidrográficas em eventos de chuva." Idem no Abstract.
- Resumo: "Este trabalho visa reproduzir a MUSLE de maneira espacializada em pixels de 30 x 30 metros" → "Este trabalho espacializa a MUSLE em pixels de 30 m × 30 m na parte alta da bacia do rio Jundiaí (137,8 km², São Paulo) e avalia o que limita a qualidade das estimativas." O objetivo geral do texto é identificar áreas críticas e o fator limitante, não "reproduzir".
- Abstract: "production of sediments on basins" → "sediment yield in watersheds"; "a 30 x 30 meters pixel scale" → "at a 30 m × 30 m pixel resolution"; "With the water forced to measured values (…) the hit rate" → vírgula depois de ")"; "hit rate" → "fraction of events"; "median error of 33%" ok.
- "co-orientação" → "coorientação" (folha de rosto).
- 2.5: parágrafo de uma frase só, e 2.5 "MUSLE espacializada" é a seção mais curta do referencial, quando é o centro do trabalho. Sugestão: ampliar com a ideia do FCI/DSC de Hao (conectividade) e dizer por que o trabalho não o usa (foi testado e abandonado: `notas` §9). Isso responde a uma pergunta óbvia da banca.
- Usar "×" (U+00D7) em "30 m × 30 m". "E 330,18 km; N 7.432,86 km": usar "E 330,18 km e N 7.432,86 km".
- "O sedimento das encostas (Figura 10) tem sempre os mesmos pontos de maior contribuição, que mudam de intensidade de um evento para outro, mas não de lugar": "sempre" e "mudam de intensidade… mas não de lugar" são redundantes. Sugestão: "Os pontos de maior contribuição são sempre os mesmos e só mudam de intensidade entre eventos, porque o padrão espacial é fixado por K, C e LS; a chuva e o escoamento definem a intensidade."

**B6.2 — Trechos fracos, com reescrita proposta.**
- 5.1 (p. 40–41): "Os resultados da seção 3.2 mostram que a comparação direta… é desigual: … O resultado mais importante desta fase é, portanto, de definição: qualquer calibração do SCS-CN contra T_R ajusta o modelo a uma grandeza que ele não representa." A 3.2 é seção de dados, não de resultados; "desigual" e "de definição" são vagos. Sugestão: "Como mostra a seção 3.2, o volume medido (T_R) inclui a vazão de base (34% a 55% do total), que o SCS-CN não calcula. Calibrar o SCS-CN contra T_R seria, portanto, ajustá-lo a uma grandeza que ele não representa; por isso, a comparação com o SCS-CN é feita contra o escoamento direto (T_R − V_base)."
- 5.3: "O que muda entre as duas versões é só a água; a fórmula…" → após B5.2, acrescentar a ressalva sobre a água medida e a circularidade.
- 4.5, 4.1: "o que antecipava o resultado" é obscuro. Sugestão: "porque a duração do hidrograma só se conhece depois de ele ocorrer e acompanha o volume observado, o que introduziria informação do resultado na previsão".
- 4.4: "Eventos em que a chuva se concentra em poucas horas (RI/R alto) têm picos locais maiores." ok.
- 4.8 (p. 37 a 38): "As métricas principais não dependem da variância dos dados" é contraditória, porque o NSE em log faz parte da lista. Sugestão: "As métricas principais (…) são pouco sensíveis a um único evento."
- 3.1: "uma rede de drenagem densa, cujo eixo principal é o rio Jundiaí": ok. "O uso do solo é dominado por mata nativa (39,6% da área)": a base dos % é "área de cálculo", não "da área" total; trivial.
- 1.2: "Passar de uma pesquisa de calibração técnica para um estudo útil à gestão da bacia exige resultados distribuídos no espaço." Bom.
- Repetição: "pouco sensíveis ao evento dominante" aparece em 1.3, 4.1, 4.8; "mesmos insumos" aparece mais de 6 vezes nos Resultados.
- Termos: alternam "escoamento", "escoamento direto", "água", "volume": definir uma vez e manter ("água do evento" = escoamento direto + vazão de base).
- Vírgula e ponto decimal: usam vírgula decimal e ponto de milhar de forma consistente (1.403; 0,84) ✓. Há "10⁻⁵" em vez de "10⁻⁵" ok.

### B7. Tabelas e valores a corrigir (JÁ CONHECIDOS, ainda presentes)

- **Tabela 7** (p. 35): ainda "Modelo calculado" e "Modelo forçado ao medido" por extenso, "Qb_início × T_chuva" sem "× 3600"; MFM com "Vazão de base medida (Bt)" em vez de "Σ Bt × 3600". A versão do rascunho (com coluna "É previsão?") é melhor.
- **Tabela 9** (p. 39): "0,00352 · 1,038" (a linha de cima tem 1,039); P = 75,4 dá Q = 11,69 mm, e não 11,72 (11,72 vem de 75,45 mm); "0,945 · 23 · 3.600 = 78.226" (com 0,945 dá 78.246; o certo é Qb_inicio = 0,9448). "MC: validação cruzada 1.098 t (−40%)" precisa de uma frase dizendo que é a previsão com c₁ e c₂ refeitos sem o evento 11. Sugestão: mostrar "P = 75,45 mm" e "Qb_inicio = 0,9448 m³/s".
- **4.8**: o item do NSE em log termina mal ("0 quando erra tanto quanto errar prevendo sempre a média" é redundante e o parágrafo do rascunho com o 68% dos três menores eventos não foi colado).
- **2.2 / Baert** (p. 13): "154 eventos monitorados" → "154 eventos de escoamento, 46 deles com sedimento medido". O NSE de −0,03 e 0,01 é do sedimento.
- **Resumo e Abstract**: última frase, ver B5.1.
- **Tabela 8**: c₁ "0,0035" (2 algarismos significativos) e c₂ "0,01311" (4) e a Tabela 9 usa "0,00352". Uniformizar: c₁ = 0,00352; c₂ = 0,01311; MFM c₁ = 0,00986; c₂ = 0,00114.

---

## (c) Divergências entre o texto e os dados

| Onde | Valor no texto | Valor nos dados | Arquivo / evidência | Situação |
|---|---|---|---|---|
| Tabela 2, coluna "Q inicial"; Resumo, 5.2, Tabela 11 "vazão inicial" | "Q inicial" (vazão antes do evento) | é Qb_inicio = primeiro Bt da janela; ex.: evento 11, Q(1ª leitura) = 1,869 e Bt = 0,945 | `Dados_finais_histereses_corrigido.xlsx` (Planilha1) e `eventos_processados_manuais.xlsx` (Qb_inicio); `gerar_tabelas_tcc.py` | **NOVO** |
| Figura 11 | imagem no corpo | imagem presa ao cabeçalho, repetida nas p. 11 a 56; ausente da p. 50 | PDF (PyMuPDF `xref 61`) | **NOVO** |
| Sumário | Resultados p. 30; Referências p. 31; 4.9 p. 28 | p. impressas 40, 53 e 38 (PDF 41, 54, 39) | PDF p. 9 × p. 41, 54 | **NOVO** (páginas); JÁ CONHECIDO (falta de itens) |
| Legenda da Figura 2 | Argissolos 17,7%; Cambissolos 68,5%; Silvicultura 12,6% | texto e Tabela 5: 17,6%; 68,6%; 12,7% (153.855 pixels de cálculo) | `mapa_02_solo_uso.png` × `tab_fatores_classes.md` | **NOVO** (base diferente) |
| Figura 5, barra E_unit | "kg por pixel, sem calibrar" | E_unit é índice relativo, não massa | `mapa_08_evento11.png` × texto 4.4 | **NOVO** |
| 4.2.3 | "O CN foi obtido do cruzamento do uso com o solo" | CN = ANA BR_CN-2022 (conferido 100% no interior das manchas) | `notas_musle_espacializada.md` §25.5; texto 3.3 | **NOVO** (4.2.3); JÁ CONHECIDO (2.6) |
| Tabela 9, pixel | 0,00352 · 1,038 | E_unit = 1,039 (linha de cima) | checagem item 9; Tabela 9 | JÁ CONHECIDO |
| Tabela 9, Q do pixel | 11,72 mm com P = 75,4 | 11,69 mm com P = 75,4; 11,72 com P = 75,45 | conta refeita | JÁ CONHECIDO |
| Tabela 9, volume de referência | 0,945 · 23 · 3.600 = 78.226 | 78.246 com 0,945; 78.225,8 com 0,9448 | `comparacao_SY_dois_componentes.csv` (volume_base_ref_m3 = 78.225,79) | JÁ CONHECIDO |
| 2.2 (Baert) | "154 eventos monitorados" | 154 de escoamento; 46 com sedimento | PDF de Baert (checagem item 7) | JÁ CONHECIDO |
| 5.4 | "(Tabela 13)" | Tabela 11 | PDF p. 44 | JÁ CONHECIDO |
| 4.7 | "Apêndice C" | inexistente no PDF | — | JÁ CONHECIDO |
| Resumo, Conclusão 2 | "recalibrar o SCS-CN … não o resolveu" | só há sustento na seção 5.2 e no Apêndice D do rascunho 04 (não colados) | rascunho 04 | JÁ CONHECIDO |
| Tabela 1 e 2.4 | Bt "método não documentado" | reproduzido por Eckhardt (a = 0,995; BFImax = 0,698); Bt ≤ Q em todas as horas | checagem item 23 | JÁ CONHECIDO |
| 3.1 × 3.3 | 137,8 km² (bacia) e 138,1 km² (cálculo) | 138,08 km² nos pixels de cálculo; 138,84 (shapefiles); 138,58 (máscara) | notas `dados_area_estudo...` | JÁ CONHECIDO |
| `Comparacao_Modelos_TCC.xlsx` | "ADOTADO: SCS-CN direto + base prevista (kb)" (NSE LOO 0,38) | o modelo adotado no TCC é o de dois componentes; a planilha é de 15/10 e não tem MC/MFM finais | planilha, aba Resumo | **NOVO** (arquivo defasado; não é o texto) |
| Tabelas 12/13 × texto 5.6.2 | "cerca de 23%" para lavoura | 22,5% | `tab_classes_uso.md` | irrelevante (arredondamento) |

Contas que **não** divergem: parâmetros de calibração, métricas, correlações de mapa, estatísticas de raster, Tabelas 2, 3, 10, 11, 12 e 13, números do evento 11 (exceto os arredondamentos acima).

---

## (d) Perguntas prováveis da banca

1. Por que 17 eventos, e não os 18 da planilha? O que é o evento 1B? (B2.2.)
2. Se o MFM usa a vazão de base e o escoamento direto medidos do mesmo hidrograma que gera a carga, como isso difere de SY = c · volume total? Qual é, então, a contribuição da MUSLE espacializada? (B5.2.)
3. Os intervalos de confiança de todas as diferenças incluem zero. O que permite dizer que "a espacialização não perde precisão"? (B5.1.)
4. Com apenas 9% do SY simulado vindo das encostas, o que o mapa significa? Em que unidade e escala ele pode ser usado? Como foi validado? (B5.3.)
5. Por que AMC I (seco)? Por que λ = 0,20 e não 0,05 (que é o que Brandão et al. recomendam)? Foi escolhido olhando o resultado? (B4.3 e B5.5.)
6. Por que não aplicar o índice de conectividade de Hao et al. (2022), se o trabalho segue Hao? (Resposta, nas notas §9: foi testado e não superou o baseline; hoje não aparece no PDF.)
7. A vazão de base veio de onde? Qual foi o filtro? (B5.8.)
8. O termo de base (Qb_inicio · T_chuva) é um processo físico? Por que o carregamento de sedimento da base é tão grande? Isso não seria erosão de margem, fontes urbanas ou ressuspensão? (B5.9.)
9. O que é c₁? É razão de entrega? Por que 0,0035? (O texto já diz que não deve ser lido como razão de entrega.)
10. Como foi obtida a CSS (curva turbidez–CSS)? Qual a incerteza? A turbidez é medida na SABESP e a vazão no DAEE: há defasagem? (B2.2.)
11. Por que usar a MUSLE (um modelo de evento calibrado em escala de bacia) com pixels de 30 m, se o próprio texto diz que o produto Q·pr·A está fora da faixa de calibração de Williams? (4.4 reconhece.)
12. Quais são as consequências de K = 0 e C = 0 nas áreas urbanas, que somam 14% da bacia, para a leitura das áreas críticas?
13. LS: por que limitar A_s a 200 m? Qual a sensibilidade do mapa a esse limite? (O LS antigo da IC estava defeituoso; a banca pode perguntar como se detectou e se os resultados da IC publicada precisam de correção. Importante: o texto 4.10 do rascunho diz que isso não afeta as métricas da IC refeita.)
14. A IC (artigo publicado) tem LS = 0,536 calculado em coordenadas geográficas. Isso invalida os α e β publicados (0,277 e 0,807)? (Eles absorvem o erro de escala, mas o LS defeituoso também distorce a forma; vale uma frase.)
15. Duas estações de chuva, uma delas fora da bacia, e o evento 12 com DBT5 = 0: o que isso faz com a IDW? A sensibilidade a uma chuva uniforme foi testada? (Nas notas: trocar a IDW por chuva uniforme quase não altera a correlação com o volume medido, de 0,67 para 0,69; não está no PDF.)
16. O que o trabalho acrescenta em relação à IC, se a IC com volume e pico medidos já tinha 100% dos eventos em fator 2?

---

## (e) O que está bem feito

- Os números são rastreáveis e reproduzíveis: tudo que testei bate com os scripts e os dados, inclusive o exemplo numérico do evento 11, que é um ótimo recurso didático.
- A honestidade metodológica é rara em TCC: separar MC (previsão) de MFM (referência), declarar que o SCS-CN calcula só escoamento direto, calibrar em log com validação cruzada aninhada, reportar métricas robustas ao evento 15 (49% da variância) e dizer explicitamente que a coincidência MC × MFM não é validação independente.
- A decisão de refazer o LS depois de detectar o defeito herdado da IC, e de documentar o efeito (o mapa muda muito, o desempenho agregado quase não), é exemplar.
- Os mapas têm norte, escala, grade em km e barra de cor com unidade; as Figuras 6, 7 e a "escada" são claras.
- O texto da Fundamentação é enxuto e bem apoiado nas referências (Hao, Brandão, Baert, Valle Junior), com dados bibliográficos corretos nos itens que consegui conferir.
- As seções 3.3 e 4.2 explicam a procedência dos dados cartográficos (CN da ANA, limitação de anos diferentes) com franqueza.

---

## Anexo — itens sobre os quais não tive certeza

- Se a imagem repetida (Figura 11) é artefato da exportação para PDF ou existe no Doc: a evidência no PDF é de que está no cabeçalho; confirmar abrindo o Doc.
- Se o número impresso no PDF (uma unidade abaixo do índice) é intencional (contagem a partir da capa com a folha de rosto etc.). O sumário não bate de qualquer modo.
- Se a norma FEC exige título da figura acima da ilustração (a norma deduzida em `entrega_tfc_regras.md` não detalha legendas).
- Páginas de Lyne e Hollick (1979) e as demais referências antigas (ver B3.7).
- Sobre o descompasso de 2 h entre CSS e Q no evento 12, a leitura é minha a partir da série horária; pode ser histerese real ou defasagem de medição.
