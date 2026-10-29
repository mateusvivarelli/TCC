# Revisão independente do processo, dos resultados e do texto (29/10/2026)

Revisora: sessão na nuvem, sem acesso ao usuário, ao Google Doc ou aos rasters. Branch `claude/noite-29-10`.
Código das recomputações: `Scripts/revisao_29-10/` (`r1_recomputa.py`, `r1_eckhardt.py`, `r2_estatistica.py`).
Gravidade: **crítico** (muda uma conclusão ou um número), **importante** (erro ou risco que a banca notaria), **menor** (estilo ou detalhe).

## Resumo (os 5 problemas mais graves e a recomendação)

1. **Crítico (interpretação): o alvo contém o volume medido.** ln(volume) explica 88% da variância de ln(carga); SY = c*T_R, sem MUSLE, dá 17,6% de erro mediano, melhor que o MFM (20,6%). O MFM mostra o peso da água, não valida a fórmula de erosão nem o mapa (achados 8, 19). Reescrever a 5.3, a 5.4 e a conclusão 4 ("o limite é a água, e não a fórmula de erosão").
2. **Importante: "equivalente", "iguala", "não custa precisão" (Resumo, Abstract, 5.4, 5.5, conclusão 5) são mais fortes que os dados.** Os testes só dizem "não se distinguem" (Wilcoxon p de 0,49 a 0,58; MFM melhor em 6 ou 7 de 17); o "16%" do Resumo é da IC refeita, não da publicada (achados 18, 23).
3. **Importante: RI é o máximo entre os postos e R a média ponderada; RI/R passa de 1 nos eventos 1 e 12**, o que contradiz "fração da chuva na hora mais intensa" (achados 1, 25).
4. **Importante: métodos descartados já no Doc (2.3: "+94% sem conversão", "-12% com λ = 0,20") e citações de obras não lidas** (USDA-SCS 1972, Chow 1988, Williams 1975, Nash e Sutcliffe 1970; só resumo: Moore e Burch, Eckhardt 2005); NRCS (2004) citado e ausente da lista (achados 35, 37, 38).
5. **Importante: área de 137,8 km² (bacia) e 138,1 km² (pixels de cálculo) sem explicação; MFM não é exatamente o volume medido (limite Q <= P em eventos com f até 9,75; não verificado quanto)** (achados 2, 14).

Conferido e certo: todos os números oficiais (c, LOO, métricas, volumes, IC refeita com Spearman 0,93, bootstrap de §32, Eckhardt 0,995/0,70, planilha da noite recalculada sem erro). Sensibilidade sem os eventos 15 e 17 não muda nenhuma conclusão.

**Recomendação:** os números podem ir para o Doc como estão; antes de colar as propostas, (a) trocar a narrativa "a espacialização iguala/não custa" por "não se distingue, e o desempenho com a água medida vem do volume", (b) corrigir a definição de RI/R, (c) tirar da 2.3 as duas frases com configurações descartadas, (d) resolver as citações não lidas com "apud" e incluir o NRCS (2004), (e) explicar as duas áreas. Perguntas só o usuário responde: origem da coluna `Chuva_evento_mm` (pesos 0,307/0,693); por que o evento 1B (24/11/2018) ficou fora; se aceita manter as frases da 2.3 como exceção à regra 3.

---

## R1. Metodologia (o processo)

### R1.1 Código contra o texto

Conferido em `Scripts/calcular_sy_lambda005_woodward.py` (o "modelo oficial") contra `proposta_secao4.md` e as seções 2 e 3 de `doc_texto_completo_29-10.md`.

Conferidos e certos (uma linha cada):
- conferido: S0,20 = 25,4*(1000/CN - 10) vem pronto do raster `S - Seco.tif` (CN-I); a conversão no código é `25.4*1.33*(S/25.4)**1.15`, igual à equação em polegadas reescrita em mm da 4.2.3.
- conferido: SCS-CN no código `(P - λS)^2/(P + (1-λ)S)` com Q = 0 se P <= λS, λ = 0,05, igual à 4.3. As variáveis default (`lam=LAM`) são avaliadas na definição (0,20), mas todas as chamadas do modelo oficial passam λ = 0,05 explicitamente (`edir(i, LAM)`, `qdir(i, LAM)`, `campos` definida depois de `LAM = 0.05`). Sem erro.
- conferido: pr = Q/1000 * A * (RI/R)/3600 e E_unit = 11,8*(Q*pr*A)^0,56*K*C*LS (P = 1 implícito), com Q em mm, A = |gt1*gt5| = 897,49 m². Igual ao texto, que já declara Q em mm e o fator 1/1000.
- conferido: SY = c*soma(E_unit); c = exp(média(ln SY - ln E)) (`fit1`); LOO refaz só c (`roda`). Igual à 4.5 a 4.7.
- conferido: IC refeita = polyfit de ln(SY/KLSC) contra ln(T_R*Qpico), K = 0,031, LS = 0,536, C = 0,267; LOO refaz α e β. Igual à 5.5.
- conferido: IDW `P(x) = (P1*d2^2 + P2*d1^2)/(d1^2 + d2^2)` é algebricamente o IDW de potência 2 com dois postos (a reprodução do raster do QGIS não pôde ser conferida: sem rasters).
- conferido: 153.855 pixels * 897,49 m² = 138,08 km² (bate com "138,1 km²").
- conferido: S0,05 > S0,20 em todos os pixels (vale para S0,20 > 3,8 mm; o mínimo é 12 mm) e "8,4% dos pixels com CN-I < 35" equivale a S0,20 > 471,7 mm, coerente com o texto (contagem de pixels não verificada: sem rasters).
- conferido: E_unit proporcional a Q^1,12 (Q^0,56 * pr^0,56, pr proporcional a Q).

Achados:

1. **Importante. RI e R vêm de fontes diferentes; RI/R passa de 1 em dois eventos.** Onde: 4.2.1 (Tabela 7: "RI, intensidade máxima da chuva (maior chuva em 60 minutos)") e 4.4 ("a razão RI/R (por hora) indica a fração da chuva que cai na hora mais intensa"). Evidência: o código lê `Intensidade_60min_mm/h`, que na planilha é o **maior i60 entre os dois postos** (ev 1: max(23,6; 16,2) = 23,6; ev 12: max(0; 32,8)), enquanto R é a média ponderada dos postos. Resultado: RI/R = 1,01 no evento 1 e 1,38 no evento 12, ou seja, "a fração da chuva que cai na hora mais intensa" seria 101% e 138%, impossível. Sugestão: na Tabela 7 escrever "RI: maior intensidade em 60 min entre os dois postos"; na 4.4 trocar "indica a fração da chuva que cai na hora mais intensa" por "mede a concentração temporal da chuva do evento"; e declarar na 5.7 que RI é de um posto e R da média (no ev 12 o DBT5 tem chuva zero). O efeito numérico é uma constante por evento elevada a 0,56, absorvida só em parte por c.

2. **Importante. No MFM o volume não é exatamente o medido (limite Q <= P).** Onde: 4.5 ("o volume de escoamento direto é forçado ao valor medido") e 4.1. Evidência: `campos()` faz `Q = np.minimum(V/(ΣQ*A/1000)*Q, p)`; depois do limite o volume não é reescalado. O fator f = V_dir/V_SCS passa de 1 em 9 dos 17 eventos e chega a 9,75 (ev 10), 6,4 (ev 4) e 6,3 (ev 1) (recalculado de `comparacao_SY_lambda005_woodward.csv`). Com f = 9,75 e R = 25,8 mm, um pixel de CN-II 98 (S0,05 de ~15 mm) teria f*Q de ~150 mm, muito acima de P; o limite corta. Não verificado quanto volume se perde (precisa dos rasters). Sugestão: no PC, imprimir ΣQ_MFM*A/1000 contra V_dir por evento; se a perda for pequena, escrever "o volume é forçado ao medido (a menos do limite Q <= P, que retira X% no evento 10)"; se for grande, redistribuir o excesso.

3. **Menor. R do código não é exatamente 0,307*P1 + 0,693*P2.** Onde: 4.2.4, Tabela 7, Tabela 9. Evidência: o código usa a coluna `Chuva_evento_mm`; refazendo, os pesos de mínimos quadrados que reproduzem essa coluna são 0,3063 e 0,6931, com resíduo de até 0,57 mm (ev 16: 97,68 contra 98,25). A planilha da noite usa 0,307*P1 + 0,693*P2 (por isso o c da chuva dela é 19,7158 e o oficial 19,7168; métricas iguais). Isso responde em parte a dúvida 1 da proposta 4: os pesos são o ajuste de mínimos quadrados da coluna `Chuva_evento_mm`. Essa coluna **não** é a média do raster IDW (no evento 11, 74,0 mm contra 73,5 mm de média nos pixels, Tabela 10); a origem dela não foi encontrada no repositório. Sugestão: o usuário confirmar de onde vem `Chuva_evento_mm` antes de escrever "contra o quê" na 4.2.4; se não houver resposta, escrever só "pesos fixos 0,307 e 0,693, os mesmos da planilha de eventos".

4. **Menor. O evento "1" é o 1A; o 1B da planilha foi excluído.** Evidência: `ev.iloc[0 if n == 1 else n]` pula a linha "1B" (24 a 26/11/2018). Isso conversa com o achado do lote C (a IC usa 24/11/2018 no lugar de 17/12/2018). Sugestão: uma frase na 3.2: "o evento de 24 a 26/11/2018 (1B da série) não foi usado porque ..." (motivo: perguntar ao usuário).

5. **Menor. Filtro de Eckhardt: conferido, com uma ressalva de rótulo.** `r1_eckhardt.py`: com a = 0,995 e BFImax = 0,70 o filtro reproduz a coluna Qb do arquivo do orientador **exatamente** (diferença máxima 0,0000 m³/s; BFI 0,66); com 0,58 não reproduz (diferença até 2,1 m³/s). O Bt usado no modelo (planilha de histereses) difere desse filtro em mediana 0,0016 e no máximo 0,040 m³/s (soma de Bt por evento difere ~0,1%), o que confere com "diferença mediana de 0,002 m³/s" da 2.4. Ressalva: o cabeçalho do próprio arquivo do orientador diz "alpha=0.995, BFImax=0.58". Sugestão: avisar o orientador do rótulo; manter 0,70 no texto.

6. **Menor. O script oficial ainda se chama "candidato" e tem código morto.** Docstring "CONFIGURACAO CANDIDATA ... ainda NAO adotada", rótulos `[CANDIDATO]`, e `E05`, `X2`, `fit2` (modelo de dois componentes) sem uso. Se o script for para apêndice ou repositório público, a banca verá método descartado. Sugestão: copiar para um script limpo antes de publicar (não é erro de cálculo).

7. **Menor. A 4.4 diz "como em Hao et al. (2022)" para as unidades e "a fórmula impressa em Hao não traz o 1/1000".** Não verificado (artigo não está no repositório em texto; o lote A diz texto completo lido). Sem efeito nos números (constante absorvida por c).

### R1.2 Lógica científica

8. **Crítico (de interpretação). O alvo contém o volume medido; boa parte do desempenho do MFM (e da IC e de SY = c*V_dir) é construída.** Onde: 5.3 ("A fórmula de erosão e a espacialização não são o limite"), 5.4 ("A espacialização não perde precisão"), 5.5 ("Com informação equivalente, a espacialização iguala a qualidade da formulação concentrada"), Conclusões 6. Evidência (`r1_recomputa.py`): SY_obs = Σ Q*CSS = T_R * (concentração média). Na escala log, a variância de ln SY é 0,655; a de ln T_R é 0,661 e a de ln(concentração média) só 0,081. ln T_R sozinho explica 88% da variância de ln SY (R² = 0,88; ln V_dir: 0,87; ln chuva: 0,60). A regra SY = c*T_R, que nem separa a base, dá 17,6% / 94% / NSE log 0,86, **melhor que o MFM** (20,6% / 94% / 0,84). ln E_MFM e ln V_dir têm correlação 0,956: o MFM é, na prática, c*V_dir^1,12 com um ruído espacial. Consequência: o bom desempenho do MFM mostra que **o volume medido explica o sedimento medido**, não que a MUSLE ou a espacialização acertam. A afirmação "a fórmula de erosão não é o limite" não está demonstrada: com a água medida, a MUSLE não acrescenta nada mensurável ao total do evento (é numericamente um pouco pior que c*V_dir e que c*T_R). Sugestão de frase para a 5.4/5.7: "Como a carga medida é o produto do volume escoado pela concentração, e o volume varia muito mais entre eventos que a concentração (variância de ln de 0,66 contra 0,08), qualquer modelo que receba o volume medido acerta a ordem de grandeza da carga. O desempenho do MFM, da IC refeita e de SY = c*V_dir mostra o peso do volume; não é uma validação da fórmula de erosão nem do mapa." Ajustar 5.3: "o limite do MC está na conversão da chuva em escoamento; com a água medida, a MUSLE espacializada não melhora a regra simples, e a sua contribuição própria é o mapa, que não pôde ser validado".

9. **Importante. Vazamento: escolhas feitas nos mesmos 17 eventos.** Onde: 4.2.3, 4.7, 5.7 ("Escolhas e avaliação nos mesmos eventos"). Evidência (`notas_musle_espacializada.md` §30 e §31): λ = 0,05, CN-I, a conversão de Woodward e os pesos 0,307/0,693 foram escolhidos olhando os 17 eventos; o LOO só refaz c. Nuance que falta no texto: o critério de escolha foi o **volume**, não o sedimento, e, para o MC, a configuração escolhida **não** é a de menor erro de sedimento (CN-III λ 0,20 daria 50,9%; CN-II λ 0,05 convertido, 55,5%; a oficial dá 81,1%), então as métricas do MC não estão infladas pela escolha. Para o MFM, a troca de λ 0,20 por 0,05 levou o erro de 38,7% para 20,6%, e §30 registra "escolhida após ver os resultados": ali o vazamento é real. A frase proposta "as métricas da validação cruzada são, portanto, um pouco otimistas" serve; acrescentar: "a escolha seguiu o volume de escoamento, e não o sedimento; para o MC, outras escolhas dariam erro de sedimento menor". Atenção à regra do usuário: citar números de configurações descartadas no texto viola a regra 3; a nuance pode ir sem números.

10. **Importante. Circularidade na comparação com a IC.** A IC refeita usa T_R e Q_pico do hidrograma do mesmo evento cuja carga é Σ Q*CSS: a mesma vazão está nos dois lados. O MFM também (V_dir). A proposta 5.5 diz que a IC "não é uma previsão" (certo), mas descreve o MFM como recebendo "informação equivalente". Não é equivalente: a IC usa também o pico medido e o volume total, e tem 2 parâmetros livres contra 1. Sugestão: "informação medida da mesma natureza (volume do hidrograma)" no lugar de "equivalente".

11. **Importante. "Toda a carga atribuída ao escoamento direto" é hipótese forte e não é a única coerente.** Onde: 4.5 ("Admite-se que todo o sedimento do evento foi mobilizado pelo escoamento superficial"). O alvo inclui sedimento de canal, margens e da carga trazida pela base (47% do volume). Defensável como convenção (é o que a IC faz e o que o SY medido é), mas o texto deve dizer "toda a carga medida é comparada com a erosão das encostas, que é o que o modelo representa; parte dela vem de canal e margens, que o modelo não separa", e a 5.7 já traz a sensibilidade (12,9%, conferida na R2).

12. **Menor. MFM: "redistribui pelo padrão do SCS-CN com fator único f".** O que permite concluir: onde, dado o volume, a MUSLE põe o sedimento (padrão relativo). O que não permite: que o padrão do SCS-CN esteja certo (não há medida espacial), nem que a parcela de cada uso esteja certa (K e C não conferem com as fontes em 4 valores; lote D). A proposta 5.6.2 já diz que o mapa não foi validado e que MC x MFM não é validação independente: conferido, está certo.

13. **Menor. Calibração em log e LOO.** conferido: a forma fechada é o mínimo de Σ(ln SY - ln c - ln E)²; "equivalente a maximizar o NSE em log" vale no ajuste (não no LOO), e o texto fala do ajuste: certo. A estimativa em log dá a mediana geométrica, não a média: a soma prevista dos 17 eventos fica abaixo da medida (efeito de retransformação). Não muda MedAPE nem fator 2; vale meia linha se a banca perguntar por carga anual.

### R1.3 Recomputação independente

Script `Scripts/revisao_29-10/r1_recomputa.py`, a partir de `eventos_processados_manuais.xlsx`, `Dados_finais_histereses_corrigido.xlsx` e das somas de E_unit do CSV oficial (E_unit não pode ser refeito sem rasters).

- conferido: T_R = Σ Q*3.600 na janela = coluna `T_R_m3` (17/17, exato); SY_obs = Σ Q*CSS*3.600/10^6 = `SYY_t` = CSV (diferença < 10^-12 t); Σ Bt*3.600 e V_dir = CSV (exato); sem horas faltando de Q ou CSS nas janelas.
- conferido: c MC 0,034379; c MFM 0,022216; c chuva 19,717; c V_dir 0,0015799; c T_R 0,00083240; IC α 0,978 e β 0,733.
- conferido (LOO): MC 81,1% / 35% / NSE log -0,69 / Spearman 0,59; MFM 20,6% / 94% / 0,84 / 0,83; c*chuva 41,9% / 82% / 0,53 / 0,63; c*V_dir 15,9% / 94% / 0,85 / 0,90; IC refeita 16,3% / 100% / 0,87 / **0,93** (confirma o Spearman novo da noite); c*T_R 17,6% / 94% / 0,86 / 0,88 (não usado no texto; ver achado 8). As previsões LOO batem com o CSV (diferença < 10^-11 t).
- conferido: NSE linear MC -4,35 / -5,43; MFM 0,80 / 0,78; evento 15 = 48,7% da soma dos quadrados dos desvios da carga (frase da 4.6).
- conferido: volume SCS-CN: viés +2,9%, erro mediano 46,3%, erro médio 53,9%, NSE -0,39, razão mediana 0,86, de 0,10 (ev 10) a 2,15 (ev 9).
- conferido: Eckhardt (achado 5).
- conferido: `Planilhas/planilha_calculos_concentrados.xlsx`, recalculada pelo LibreOffice (`soffice --headless --convert-to xlsx`): nenhuma célula com erro nas 7 abas (serie, eventos, calibracao, metricas, ajuste, volume, ic); c, LOO, métricas, volume (+2,87% / 53,9% / 46,3% / -0,39 / 0,864) e IC (α 0,97824, β 0,73324) iguais aos acima. Única diferença: a aba eventos calcula R = 0,307*P1 + 0,693*P2 (achado 3), o que muda o c da chuva na 5ª casa.
- não verificado: soma de E_unit por evento, 153.855 pixels, 8,4% com CN-I < 35, médias de S (255,7 e 489,9 mm), pixel do evento 11 (Q recalculado a partir da tabela: 12,99 mm, confere com a proposta), correlações dos mapas (0,984; 94,2%; 0,77; 0,76): dependem dos rasters.

### R1.4 As 10 perguntas mais prováveis da banca (com a melhor resposta honesta)

1. **"Se o MFM usa o volume medido e o alvo é Σ Q*CSS, o bom resultado não é circular?"** Em parte, sim: o volume explica 88% da variância de ln(carga). Por isso o MFM é apresentado como referência, não como previsão, e comparado com SY = c*V_dir, que usa a mesma água; os dois não se distinguem. O MFM serve para separar o erro da água do erro da fórmula, não para validar a MUSLE.
2. **"Então o que a MUSLE espacializada acrescenta?"** No total do evento, nada mensurável com 17 eventos (a regra simples é tão boa ou um pouco melhor). Acrescenta um mapa de áreas críticas coerente com K, C e LS, que não pôde ser validado no espaço (só há medição no exutório).
3. **"O MC é pior que SY = c*chuva. Por que usar o MC?"** Porque o SCS-CN erra o escoamento evento a evento (NSE do volume -0,39); 91% da variância do erro do sedimento vem do erro da água. O resultado é um diagnóstico: nesta bacia, com dois postos e CN tabelado, o gargalo é a geração de escoamento.
4. **"λ = 0,05, CN-I e a conversão foram escolhidos com os mesmos eventos. O LOO não é otimista?"** É, para essas escolhas; o LOO só refaz c. A escolha seguiu o volume de escoamento, não o sedimento, e com 17 eventos não havia como separar um conjunto de teste. Está declarado como limitação.
5. **"Por que CN-I se o NEH-630 abandonou o critério dos 5 dias?"** O CN-I é uma condição única que reproduz o volume direto medido no conjunto (viés +3%); o critério antigo só indica que a maioria dos eventos teve pouca chuva antecedente. Não é uma medida da umidade de cada evento.
6. **"8,4% dos pixels estão fora da faixa de Woodward. E daí?"** Neles a conversão é extrapolação; são pixels de CN baixo (mata), que geram pouco escoamento e pouca erosão. Não verificado quanto do sedimento sai deles (vale calcular no PC para responder com número).
7. **"K e C não conferem com as fontes. Isso invalida o mapa?"** Não muda o sedimento total (c absorve a escala), mas muda o peso relativo das classes: campo e lavoura somam 58% do sedimento. O mapa deve ser lido como contribuição relativa sob os valores adotados.
8. **"Somar picos de pixels sem roteamento faz sentido físico?"** Não como vazão; pr é um índice de intensidade local, como em Hao et al. (2022). Como E_unit ∝ Q^1,12, o pr só muda a escala entre eventos (RI/R), e c absorve o resto.
9. **"O evento 17 e o evento 15 dominam?"** O 15 domina o NSE linear (48,7% da variância), por isso as métricas principais são em log e medianas. Sem o 17, o MFM teria 100% em fator 2; as conclusões não mudam (R2.3).
10. **"Por que a IC refeita, com 2 parâmetros e o pico medido, empata com o MFM?"** Porque as duas recebem o volume medido do hidrograma, que domina a carga. A diferença mediana MFM - IC é +6 pontos, com intervalo de 95% que inclui zero; com 17 eventos não dá para ordenar os dois.

---

## R2. Resultados (a pesquisa)

Script: `Scripts/revisao_29-10/r2_estatistica.py` (bootstrap com 4.000 reamostragens de eventos, semente 29102026; Wilcoxon pareado do scipy; LOO refeito em cada subconjunto).

### R2.1 Consistência de números

Conferidos e certos:
- conferido: `tab_resultados.md`, `tab_mc_mfm_eventos.md`, `tab_volumes.md` e `tab_evento11_passo_a_passo.md` batem com o CSV oficial e com a minha recomputação (todas as linhas; pr do pixel = 5,17*10^-4 m³/s e E_unit = 1,167 refeitos à mão a partir da tabela; Q médio 7,2 mm = 997 mil m³ / 138,08 km²).
- conferido: 3.2 do Doc: base de 34% a 55% por evento e 47% no conjunto; direto 15,3 de 28,9 milhões de m³; SCS-CN 15,7 milhões (5.1).
- conferido: 5.1 a 5.4 da proposta: superestima 8 eventos (3, 8, 9, 13 a 17); 1, 4, 7 e 10 abaixo de 0,25; razões 0,10 e 2,15; MC 10 superestimados e 7 subestimados; razões 0,10 e 3,15; c = 19,72 e 0,00158; Spearman 0,63 / 0,59 / 0,90 / 0,83 / 0,93; coeficiente de escoamento x chuva r = -0,01.
- conferido: 5.6.2 contra `tab_classes_uso.md` e `tab_classes_solo.md` (37,4 / 24,2 / 20,9 / 8,2 / 7,5%; 530% e 1.772%; 92,9%); conclusão 6 (45,6% da área, 82,5% do sedimento).
- conferido: 5.7: SY/V_dir de 1.085 a 3.806 mg/L (máximo sem o 17: 2.088); MFM +18% a +84% nos eventos 1 a 6 e -10% a -55% nos 14 a 17; alvo só do escoamento direto = 15.752 de 23.846 t (66,1%) e MFM 12,9%.

Divergências:

14. **Importante. Duas áreas da bacia no mesmo texto: 137,8 km² (Resumo, Abstract, 3.1, Figura 1) e 138,1 km² (3.3, 4.2.1).** Evidência: `doc_texto_completo_29-10.md` linhas do Resumo e da 3.1 (137,8, área por acumulação de fluxo) e da 3.3/4.2.1 (153.855 pixels = 138,1 km²). A área de cálculo é **maior** que a da bacia, o que a banca vai estranhar. Os rascunhos antigos têm ainda 138,2 e 138,9 km²; o Murillo-Bermúdez e Martim (2022) dá 139,3. Sugestão: uma frase na 3.3: "os pixels de cálculo somam 138,1 km², um pouco mais que a área de contribuição (137,8 km²), porque a grade de 30 m inclui pixels de borda parcialmente fora do divisor" (conferir no PC se a explicação é essa: não verificado).

15. **Menor. "Sobe de cerca de 1.480 para cerca de 2.040 mg/L" depende do evento 17 e de quais eventos entram.** Onde: 5.7 ("O que sobra no modelo forçado"). Evidência: 1.477 é a média simples dos eventos 1 a 10 e 2.038 a dos eventos 12 a 17; sem o 17, a segunda vira 1.685 mg/L; ponderando pelo volume, 1.448 contra 1.739. Sugestão: "a carga por m³ de escoamento direto é, em média, maior nos eventos de 2019/20 (cerca de 1.700 mg/L sem o evento 17, contra cerca de 1.480 mg/L em 2018/19)", ou citar a mediana.

16. **Menor. A diferença "+6,1 pontos" entre MFM e IC não é a diferença dos erros medianos (20,6 - 16,3 = 4,3).** Onde: 5.5 e notas §32. Evidência: +6,1 é a mediana das diferenças por evento (o script faz isso); a diferença das medianas é +4,3, IC95% [-11,4; +17,7]. O leitor vai subtrair os números da Tabela 12 e não achar 6,1. Sugestão: "a mediana das diferenças de erro, evento a evento, é de +6,1 pontos" (deixar explícito), ou dar a diferença das medianas.

17. **Menor. Numeração e remissões.** O Doc atual (seções 4 e 5 antigas) chama a dispersão de Figura 6 e o mapa médio de Figura 11; as propostas renumeram para 7 e 12 e inserem as Figuras 6 e 8 novas. conferido: o mapa de figuras lista essas trocas. O Resumo e as seções 1 a 3 não citam figuras das seções 4 e 5. As remissões "seção 4.x" nas seções 2.4 e 2.5 continuam pendentes (já apontado pela noite). `tab_nse_linear.md` tem 5 linhas de modelos não adotados (já apontado: usar só as 6 primeiras).

### R2.2 Afirmações contra os dados (bootstrap e Wilcoxon)

Diferença pareada do erro absoluto percentual, LOO (A - B; negativo = A melhor):

| Comparação | Mediana das diferenças | IC95% bootstrap | A melhor em | Wilcoxon p | Diferença das medianas [IC95%] |
|---|---|---|---|---|---|
| MC x SY = c*chuva | +32,6 | [+3,1; +117,5] | 3 de 17 | 0,020 | +39,2 [+11,7; +103,9] |
| MFM x SY = c*V_dir | +1,6 | [-5,5; +10,4] | 6 de 17 | 0,52 | +4,7 [-15,3; +16,2] |
| MFM x IC refeita | +6,1 | [-8,6; +7,9] | 6 de 17 | 0,58 | +4,3 [-11,4; +17,7] |
| MFM x SY = c*T_R | +6,1 | [-6,4; +11,8] | 7 de 17 | 0,49 | +3,0 [-13,4; +18,0] |
| SY = c*V_dir x IC refeita | 0,0 | [-11,6; +10,5] | 8 de 17 | 1,00 | -0,4 [-11,5; +18,1] |

- conferido: os intervalos de §32 e da proposta 5.4/5.5 se reproduzem exatamente (mesmo procedimento).
- conferido: "o MC é pior que a regra da chuva" é sustentado (bootstrap e Wilcoxon p = 0,02; pior em 14 de 17).

18. **Importante. "Equivalente", "iguala" e "não perde precisão" são mais fortes que os dados.** Onde: Resumo ("a espacialização tem desempenho equivalente ao da formulação concentrada (erro mediano de 16%)"), Abstract ("performs equivalently"), proposta 5.4 ("A espacialização não perde precisão em relação à regra simples com a mesma água"), 5.5 ("a espacialização iguala a qualidade"; "a espacialização em si não custa nada"), conclusão 5 ("não custa precisão"). Evidência: a tabela acima. "Não se distinguem" é o que os testes dizem (p > 0,5), mas o MFM é numericamente pior que as três referências com a água medida e melhor em só 6 ou 7 de 17 eventos; com 17 eventos, uma perda de até ~10 a 15 pontos de erro mediano não seria detectada. "Equivalente" exige teste de equivalência, que não foi feito. Sugestão: "não se distingue estatisticamente da formulação concentrada refeita (diferença mediana de +6 pontos de erro, intervalo de 95% de -9 a +8)"; trocar "não perde precisão" por "não se mostrou pior, com 17 eventos"; tirar "não custa nada". No Resumo, escrever "IC refeita" ou "formulação concentrada recalibrada", porque "16%" não é o erro da IC publicada.

19. **Importante. A conclusão 4 e a 5.3 atribuem o limite à água "e não à fórmula de erosão"; os dados só mostram a primeira metade.** Ver achado 8 (R1). Com a água medida, a regra c*T_R, sem MUSLE e sem separar a base, é tão boa ou melhor que o MFM. Sugestão para a conclusão 4: "O fator que mais limita a estimativa do MC é a conversão da chuva em escoamento: com o escoamento direto medido (MFM), o erro mediano cai para 21% e 94% dos eventos ficam dentro de fator 2. Esse ganho vem do volume medido; com ele, a MUSLE espacializada não supera uma regra proporcional ao volume."

20. **Menor. Resumo: "porque o SCS-CN erra o escoamento direto em 46% na mediana dos eventos".** O nexo causal é sustentado pela correlação de 0,96 e pelos 91% (§33; não refeitos aqui, dependem das somas de E_unit; com as somas do CSV obtive o mesmo sinal: o sinal do erro do sedimento do MC é o do erro da água em 15 de 17 eventos). conferido no essencial; ver achado 21.

21. **Menor. 5.2: "Os eventos com sedimento subestimado são os mesmos com escoamento subestimado (1, 2, 4, 7 e 10), e os superestimados são os de escoamento superestimado (3, 9, 13, 14 e 15)."** Evidência: a lista é uma seleção. O sinal coincide em 15 de 17 eventos; nos eventos 5 e 6 o SCS-CN subestima a água (razão 0,83 e 0,86) e o MC superestima o sedimento (+52% e +146%), porque c compensa o viés médio. Sugestão: "Em 15 dos 17 eventos o erro do sedimento tem o mesmo sinal do erro do escoamento; as exceções (5 e 6) têm água quase certa e sedimento superestimado pelo coeficiente."

22. **Menor. 5.7: "o MFM teria erro mediano de 12,9% em vez de 20,6%, sem mudar a ordem dos modelos".** Evidência: com o alvo só do escoamento direto, a ordem **muda** entre os modelos com água medida: IC refeita 9,1% (88% em fator 2), MFM 12,9%, c*V_dir 17,8%, c*chuva 32,8%, MC 80,2%. Sugestão: "sem mudar as conclusões (o MC continua pior que a regra da chuva, e os modelos com a água medida continuam próximos entre si)".

### R2.3 Sensibilidade (LOO refeito em cada subconjunto; MedAPE % / fator 2 % / NSE log)

| Modelo | 17 eventos | sem o 15 | sem o 17 | sem 15 e 17 |
|---|---|---|---|---|
| MC | 81,1 / 35 / -0,69 | 76,5 / 38 / -0,87 | 82,9 / 31 / -0,73 | 80,1 / 40 / -0,94 |
| SY = c*chuva | 41,9 / 82 / 0,53 | 41,2 / 75 / 0,46 | 41,3 / 81 / 0,53 | 44,6 / 73 / 0,45 |
| MFM | 20,6 / 94 / 0,84 | 20,6 / 94 / 0,81 | **15,3 / 100 / 0,90** | 15,8 / 100 / 0,88 |
| SY = c*V_dir | 15,9 / 94 / 0,85 | 20,2 / 94 / 0,82 | 18,3 / 100 / 0,93 | 21,7 / 100 / 0,92 |
| SY = c*T_R | 17,6 / 94 / 0,86 | 18,6 / 94 / 0,83 | 17,1 / 100 / 0,93 | 18,7 / 100 / 0,92 |
| IC refeita | 16,3 / 100 / 0,87 | 18,9 / 100 / 0,84 | 16,3 / 100 / 0,91 | 16,7 / 100 / 0,89 |

- **Nenhuma conclusão muda.** MC pior que a chuva em todos os cenários; os modelos com água medida ficam entre 15% e 22% e trocam de posição conforme sai um evento (sem o 17, o MFM passa a ser o melhor em erro mediano). Isso reforça "não se distinguem" e enfraquece qualquer frase que ordene MFM, IC e c*V_dir.
- conferido: "sem o evento 17, o MFM teria 100% em fator 2" (§34): sim, 100%.
- Evento a evento (erro LOO): o MC erra mais nos eventos 9 (+215%), 3 (+193%), 15 (+188%) e 10 (-90%); o MFM no 6 (+84%), 4 (+60%) e 17 (-55%); a IC refeita no 6 (+97%), 16 (+60%) e 17 (-47%); c*V_dir no 17 (-61%), 6 e 16 (+49%). O evento 6 (o menor, 199 t) e o 17 são difíceis para todos os modelos com água medida.
- Erro contra tamanho do evento (Spearman entre ln(simulado/medido) e o sedimento medido): MFM -0,45 (superestima os pequenos e subestima os grandes; contra a chuva, -0,51); c*chuva -0,60; MC +0,07 com o sedimento, mas +0,68 com a chuva (superestima os eventos de chuva grande, coerente com a curva do SCS-CN); c*V_dir -0,11; IC -0,03. O padrão do MFM (pequenos para cima, grandes para baixo) é o expoente 1,12 da MUSLE contra a inclinação observada de 0,94 entre ln SY e ln V_dir. Vale uma frase na 5.7: "a MUSLE faz o sedimento crescer com a potência 1,12 do escoamento, e nesta bacia o sedimento medido cresce com a potência 0,94 do volume direto; por isso o MFM tende a superestimar os eventos pequenos e subestimar os grandes".

### R2.4 Limitações que faltam ou estão fracas (frases curtas propostas)

conferido (já estão na 5.7 proposta): 17 eventos e intervalos largos; 8,4% dos pixels fora da faixa de Woodward; critério do NEH-4 abandonado no NEH-630; mapa sem validação espacial; alvo carga total e sensibilidade da base; K e C sem fonte confirmada; K = 0 e C = 0 no urbano; sem conectividade; escolhas nos mesmos eventos.

Faltam:
- **Circularidade do alvo (R1, achado 8).** "A carga medida é o produto do volume pela concentração, e o volume varia muito mais entre os eventos; por isso, os modelos que recebem o volume medido têm desempenho alto por construção."
- **Chuvas abaixo de 25,4 mm.** A 2.3 do Doc diz que a relação de Woodward foi ajustada "para chuvas de pelo menos 25,4 mm"; os eventos 1 (23,4 mm) e 12 (23,7 mm) ficam abaixo, e muitos pixels nos eventos pequenos também. Frase: "Dois eventos (1 e 12) têm lâmina abaixo de 25,4 mm, fora da faixa de chuva em que a conversão de Woodward et al. (2003) foi obtida."
- **RI de um posto, R da média (R1, achado 1).** "A intensidade máxima é a do posto mais intenso, e a lâmina é a média ponderada; no evento 12, em que um posto não registrou chuva, a razão RI/R passa de 1."
- **Mesma concentração na água de base.** Já está como sensibilidade; falta dizer que a hipótese "base só transporta" não foi testada contra a concentração medida antes dos eventos (a planilha tem CSS da base, coluna `CSS_Bt`, não usada; não verificado o que ela contém).
- **Um único c para todos os pixels** (sem razão de entrega por distância ao canal): está como "sem conectividade"; conferido.
- **Pesos 0,307/0,693 ajustados nos 17 eventos** e de origem não documentada (R1, achado 3).
- **Expoente fixo 1,12 contra 0,94 observado** (R2.3).
- **Contraste entre as duas estações chuvosas depende do evento 17** (achado 15).
- **Mineração: 1,8% do sedimento em 0,0% da área, com C = 1 sem fonte** (`tab_classes_uso.md`; lote D). Frase: "A mineração, com C = 1 adotado sem fonte, responde por 1,8% do sedimento em poucos pixels."
- **Área de cálculo maior que a da bacia** (achado 14).

---

## R3. Tese (o texto)

Revisado: `doc_texto_completo_29-10.md` (Resumo, Abstract, seções 1 a 3 e REFERÊNCIAS; as seções 4 a 6 antigas não foram revisadas, como pedido) e as propostas `proposta_secao4.md`, `proposta_secao5.md`, `proposta_secao6.md` e `mapa_figuras_tabelas_secoes_4_a_6.md`. `leitura_referencias/loteD_fontes_K_C.md` não foi revisado a fundo (só usado como fonte dos achados sobre K e C).

### R3.1 Erros factuais, números e inconsistências entre seções

conferido: IC publicada (PDF `Aplicação da Equação Universal de Perda de Solo Modificada.docx.pdf`): α 0,277, β 0,807, erros de -60,01% a +37,14%, média -4,15% (proposta 5.5 certa).
conferido: Tabela 2 e 3 do Doc contra a planilha e o CSV; 3.2 (199 a 3.829 t, média 1.403 t, soma 23.846 t); Tabela 4 (K médio 0,039 e C médio 0,050 refeitos pelas áreas das Tabelas 5 e 6); 2.3 (CN-I de 31 a 95 a partir de 52 a 98); 1.1 ("cerca de 42%" = 29,0 + 12,7).

23. **Importante. Resumo e Abstract: "desempenho equivalente ao da formulação concentrada (erro mediano de 16%)".** Ver achado 18. Além do "equivalente", o leitor do Resumo entende que 16% é o erro da IC publicada. Sugestão: "Nessas condições, a espacialização não se distingue de uma formulação concentrada recalibrada com o volume e o pico medidos (erro mediano de 16%) e acrescenta um mapa de áreas críticas, que não pôde ser validado no espaço." No Abstract: "performs indistinguishably from a recalibrated lumped formulation".

24. **Importante. Resumo e 1.2 prometem uso do mapa ("permite direcionar medidas de contenção").** O mapa não tem validação espacial e os C do campo e da lavoura não conferem com as fontes (lote D). Sugestão: "indica, em termos relativos, onde priorizar medidas de contenção, sob os valores de K e C adotados".

25. **Importante. RI/R descrito como "fração da chuva que cai na hora mais intensa" (Doc 4.4 antigo e proposta 4.4).** Passa de 1 nos eventos 1 e 12 (achado 1). Corrigir a frase e a Tabela 7.

26. **Importante. Área: 137,8 km² (Resumo, 3.1, Figura 1) e 138,1 km² (3.3, 4.2.1).** Achado 14.

27. **Menor. Tabela 1 diz que Bt vem do "Filtro de Eckhardt (2005) aplicado à vazão horária"; a 2.4 diz que a série "foi fornecida junto com os dados" e é reproduzida pelo filtro.** Sugestão na Tabela 1: "série fornecida com os dados, reproduzida pelo filtro de Eckhardt (2005) (seção 2.4)".

28. **Menor. Tabela 2: legenda "chuva ponderada (R)", mas a coluna R não é exatamente 0,307*P1 + 0,693*P2** (ev 16: 97,7 na tabela, 98,25 pela fórmula; achado 3). E as colunas "Q inicial" e "T chuva" não são usadas pelo modelo oficial (já apontado pela noite). Sugestão: tirar as duas colunas e explicar a origem de R.

29. **Menor. Tabela 4 diz "área acumulada no SAGA/QGIS"; a proposta 4.2.2 diz trocar "(SAGA)" por "cálculo sobre o MDE em UTM"; a 2.6 diz "rampa"/"área de contribuição específica limitada a 200 m".** Três formas para a mesma coisa. Sugestão: usar sempre "área de contribuição específica limitada a 200 m" e uma única ferramenta (conferir em `_recalcular_ls_moore.py` qual foi usada: não verificado).

30. **Menor. 2.2 diz que a MUSLE "dispensa a razão de entrega de sedimentos" (Neitsch et al., 2011); a 2.5 e a 4.5 dizem que c faz o papel de conectividade e absorve a razão de entrega.** A banca pode ver contradição. Sugestão (2.5): "Na escala da bacia, a MUSLE dispensa a razão de entrega; aplicada ao pixel, ela estima a erosão local, e a parte que chega ao exutório precisa de um fator, aqui o coeficiente c."

31. **Menor. Notação diferente entre o Doc e as propostas:** Doc usa Qk, Eunit, Apix, SYobs (com índice k do pixel); as propostas usam Q, E_unit, A_pix, SY_obs, sem k. "Taxa de abstração inicial" (Resumo) e "razão de abstração inicial" (2.3, 4.2.3). "modelo forçado ao medido" (2.4, minúsculas) e "Modelo Forçado ao Medido (MFM)" (4.1). Sugestão: uma notação só (recomendo a do Doc, com o índice k, que deixa claro o que é por pixel) e "razão de abstração inicial" em todo o texto.

32. **Menor. Siglas.** NSE é definido na 2.7 e de novo na 4.8 (proposta repete a explicação inteira); IC é "Iniciação Científica", e as notas usam "IC95%" para intervalo de confiança (a proposta 5 escreve por extenso: conferido, manter assim). MC e MFM só são definidos na 4.1, mas a 2.4 já fala em "modelo forçado ao medido": ok, sem sigla.

33. **Menor. Remissões.** Proposta 4.2.2 cita "Tabelas 5 e 6" (certo); proposta 4.2.3 diz "A origem do CN e da conversão já está na Tabela 4 (3.3)": a Tabela 4 tem a origem do CN, não a conversão de Woodward. Proposta 5.3 cita um "teste intermediário" (regressão do volume na chuva, 47,2%) que não está descrito na seção 4 nem na Figura 8: resultado sem método (cortar ou descrever na 4.8).

34. **Menor. Resultados sem conferência nos mapas.** Proposta 5.6.2 ("As áreas críticas se concentram em manchas na porção central e oeste da bacia e em algumas manchas pequenas ao sul") e conclusão 6 ("nas mesmas manchas da porção central e oeste") repetem o texto do modelo antigo; a própria sessão da noite diz que não abriu os mapas novos. Não verificado (sem rasters/imagens conferidas). Sugestão: o usuário olhar `mapa_07_sedimento_medio.png` antes de manter.

### R3.2 Regras do usuário

35. **Importante. Métodos descartados no Doc atual (seção 2.3), já aplicados:** "sem a conversão, o escoamento calculado seria superestimado em 94%" (λ 0,05 sem converter) e "(viés de +3%, contra -12% com λ = 0,20)". As duas frases apresentam configurações testadas e descartadas, o que a regra 3 proíbe (a proposta 4.2.3 evitou de propósito a mesma frase dos 94%). Sugestão: "Neste trabalho adotou-se λ = 0,05 com S convertido por essa relação, porque com ela o volume calculado no conjunto dos eventos ficou próximo do escoamento direto medido (viés de +3%)." e cortar a frase dos 94%. Decidir com o usuário (ele aprovou a 2.3; pode ter aceitado a exceção).

36. **Menor. "λ = 0,20" na proposta 4.2.3 e na 5.7 (Brandão).** Uso como valor de definição do CN tabelado e como resultado da literatura; não é método do TCC. conferido: aceitável; a noite já deixou a alternativa de redação.

37. **Importante. Citações de obras não lidas (regra das citações).** Pelos próprios relatórios de leitura, não foram acessados: USDA-SCS (1972) (citado na 2.3 e nas propostas 4.2.3 e 4.3), Chow, Maidment e Mays (1988) (2.3, 2.6, 3.3, 4.2.3), Williams (1975) (1.1, 2.2, 4.4), Nash e Sutcliffe (1970) (2.7, 4.8); só resumo: Moore e Burch (1986) (2.6, Tabela 4, 4.2.2) e Eckhardt (2005) (2.4, Tabela 1). Sugestão: usar "apud" (NBR 10520) com a fonte lida, por exemplo "Williams (1975 apud NEITSCH et al., 2011)", "(USDA-SCS, 1972 apud NRCS, 2004)", ou trocar pela fonte lida (NEH-630 para a equação do SCS-CN e as conversões de AMC, se a tabela do cap. 10 tiver as conversões: não verificado). Para o LS, a própria noite sugere conferir se os expoentes 0,4 e 1,3 são de Moore e Burch (1986) ou Moore e Wilson (1992).

38. **Importante. Referência citada e ausente da lista:** NRCS (2004), NEH Parte 630, cap. 10 (propostas 4.2.3 e 5.7). Também ausentes, se o usuário adotar as tabelas de K e C com fonte verificada do lote D: as fontes dos valores de K e C (hoje as Tabelas 5 e 6 só citam "valor da IC"). Lista sem citação: nenhuma (conferidas as 26 entradas contra o texto das seções 1 a 3 e as propostas).

39. **Menor. ABNT nas chamadas.** O Doc usa caixa alta dentro dos parênteses ("(HAO et al., 2022)", "(NASH; SUTCLIFFE, 1970)"); as propostas usam caixa baixa ("(Valle Junior; Rodrigues; Oliveira, 2019)", "(Nash; Sutcliffe, 1970)", "(Vivarelli et al., 2025)"). Escolher um padrão (a NBR 10520:2023 aceita maiúsculas e minúsculas; conferir o guia da FEC) e aplicar a tudo. Na 2.3 do Doc aparece "Valle Junior et al. (2019)" e, na mesma seção, "Valle Junior, Rodrigues e Oliveira (2019)": com três autores, a NBR 10520:2023 pede os três nomes.

40. **Menor. ABNT na lista.** USDA-SCS: entidade governamental vai pela jurisdição ("UNITED STATES. Department of Agriculture. Soil Conservation Service."); Vivarelli et al. (2025): falta indicar onde está disponível (relatório PIBIC ou anais); Chow et al.: faltam páginas totais (opcional). Baert et al. (2026), Catena v. 274: volume e artigo não conferidos (não verificado). Espaços no fim de várias linhas (cosmético).

41. **Menor. Caracteres.** Seções 1 a 3 e propostas: nenhum caractere fora dos permitidos (fora a epígrafe, que é citação, e "Köppen", nome próprio). `tab_fator_K.md` usa "t·h·MJ⁻¹·mm⁻¹" (já apontado pela noite; a Tabela 5 do Doc já usa "t h MJ-1 mm-1").

42. **Menor. Figuras e legendas.** As legendas do Doc estão abaixo das figuras e sem "Fonte:"; a ABNT (NBR 14724) pede identificação acima e fonte abaixo; o mapa da noite já propõe isso para as Figuras 4 a 12, mas as Figuras 1 a 3 e as Tabelas 1 a 6 do Doc também precisam de "Fonte:" (Tabela 4: "Fonte: elaborado pelo autor com dados de CONSÓRCIO PROFILL-RHAMA (2020), ANA (2024) e USGS"). Imagens com texto de método descartado (`escada_gargalo.png`, `mapa_07`): já apontado pela noite; confirmo a necessidade de regerar.

### R3.3 Clareza: os 10 piores trechos e reescritas curtas

1. **Resumo, final** ("O gargalo está, portanto, em transformar chuva em escoamento. Nessas condições, a espacialização tem desempenho equivalente..."). Proposta: "O limite está, portanto, na conversão da chuva em escoamento. Com a água medida, a espacialização não se distingue de uma formulação concentrada recalibrada (erro mediano de 16%) nem de uma regra proporcional ao volume, e acrescenta um mapa relativo das áreas críticas."
2. **2.3, parágrafo de λ (Woodward, Brandão, Valle Junior), 5 frases e 3 estudos.** Proposta: dividir em dois: (a) "O valor padrão é λ = 0,20, mas estudos com muitos eventos encontraram valores menores: Woodward et al. (2003) ... ; Brandão et al. (2025) ... ; Valle Junior, Rodrigues e Oliveira (2019) ..."; (b) "Os mesmos estudos mostram limites: ..." (clima úmido, NSE baixo, CN calibrado junto).
3. **2.6, parágrafo único que mistura IDW, K, C, LS (com As) e CN.** Proposta: um parágrafo por fator, cada um com uma frase de "o que é" e uma de "de onde vem".
4. **2.3, "A relação é uma regressão entre valores de S ajustados a bacias norte-americanas, para chuvas de pelo menos 25,4 mm. Na bacia estudada, 8,4% dos pixels..."** Proposta: "A relação foi ajustada a bacias dos EUA, com chuvas de pelo menos 25,4 mm e CN de 35 a 100. Aqui, 8,4% dos pixels têm CN-I abaixo de 35, e os eventos 1 e 12 têm menos de 25,4 mm de chuva: nesses casos, a relação é extrapolada."
5. **Proposta 4.2.3, parágrafo do CN-I (NEH-4, estação de crescimento, 35,6 mm, NEH-630, r = 0,37).** Proposta: "Adotou-se a condição seca (CN-I) para os 17 eventos, porque com ela o volume calculado no conjunto ficou próximo do medido. O critério antigo da chuva dos 5 dias anteriores (USDA-SCS, 1972) coloca 13 dos 17 eventos nessa condição, mas esse critério foi abandonado pelo NRCS (2004) e, aqui, a chuva antecedente quase não se relaciona com o escoamento medido (r = 0,37)."
6. **Proposta 4.4, "Em palavras: ..."** Proposta: "Q/1000 * A_pix é o volume escoado no pixel (m³). A razão RI/R mede quão concentrada no tempo foi a chuva do evento: é maior quando a hora mais intensa tem uma parte grande da chuva. A divisão por 3.600 passa de horas para segundos."
7. **Proposta 4.4, parágrafo do E_unit ("índice relativo... fora da faixa... Q em mm...").** Proposta: "Como a fórmula de Williams foi ajustada para bacias inteiras, o valor calculado num pixel de 897 m² não é uma massa em toneladas: é um índice de erosão (E_unit). O coeficiente c (seção 4.5) converte a soma desses índices em toneladas, e absorve também as escolhas de unidade (Q em mm)."
8. **Proposta 4.5, item do MFM (uma frase com f, V_SCS, min e justificativa).** Proposta: "No MFM, o volume de escoamento direto de cada evento é o medido. O SCS-CN só diz onde ele cai: o escoamento de todos os pixels é multiplicado pelo mesmo fator, f = V_dir / V_SCS, e limitado à chuva do pixel."
9. **Proposta 5.5, dois últimos parágrafos.** Proposta: "Com a água medida, MFM, IC refeita e SY = c * V_dir ficam entre 16% e 21% de erro mediano e não se distinguem com 17 eventos. A IC refeita não é previsão (usa o hidrograma do próprio evento) e não gera mapa; o MFM gera o mapa, mas também depende do volume medido."
10. **Proposta 5.7, "Razão de abstração inicial" (5 estudos e números num parágrafo).** Proposta: começar pela conclusão ("o λ = 0,05 convertido foi escolhido pelo volume desta bacia e não é consenso"), depois um estudo por frase, e mover a frase dos 8,4% para o parágrafo das limitações de faixa (junto com os eventos abaixo de 25,4 mm).

### R3.4 Cobertura dos objetivos (1.3)

- Objetivo 1 (escoamento e pr por pixel): entregue (4.3, 4.4, Figura 10). conferido.
- Objetivo 2 (rotina em Python/SIG): entregue só na conclusão 1; **a seção 4 não descreve a rotina** (linguagem, bibliotecas, onde está o código, o que é automático). Sugestão: um parágrafo curto na 4.1 ou um apêndice: "Os cálculos foram feitos em Python (NumPy, pandas, GDAL), num script que lê os rasters e as séries, calcula os 17 eventos e gera tabelas e mapas; o QGIS foi usado na preparação dos rasters."
- Objetivo 3 (validar por validação cruzada com métricas robustas): entregue (4.7, 4.8, Tabela 12). Ressalva: "validar" é forte para LOO de um coeficiente com escolhas feitas nos mesmos eventos; a 5.7 já declara.
- Objetivo 4 (comparar com modelos simples e IC, "verificar se a espacialização custa precisão"): entregue, mas a resposta honesta é "não se mostrou pior com 17 eventos", não "não custa" (achado 18).
- **Objetivo 5 (identificar o fator que mais limita: escoamento ou erosão): entregue pela metade.** O MC mostra que o escoamento limita; a parte da erosão não foi isolada, porque com a água medida o desempenho vem do volume (achado 8). A conclusão 4 afirma "e não a fórmula de erosão": reescrever (achado 19).
- Objetivo 6 (mapear áreas críticas e contribuição por classe): entregue (5.6, Tabelas 13 e 14), sem validação espacial (declarado).
- Entregue sem objetivo: a análise da concentração por m³ (variação entre estações, evento 17) e a sensibilidade da separação da base: cabem na discussão, sem objetivo próprio. conferido: nada a mudar.
- 1.2 promete "separar duas fontes de erro, a estimativa da água e a fórmula de erosão": mesma ressalva do objetivo 5.
