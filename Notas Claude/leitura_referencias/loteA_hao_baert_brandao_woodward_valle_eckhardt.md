# Lote A: leitura de 6 referências do TCC (MUSLE espacializada, Alto Jundiaí)

Como li o modelo do TCC: `resumo_modelo_completo.md` (origin/main, 27/10/2026) e `TCC_rascunho_04.md`. Atenção: o rascunho 04 é mais antigo que o resumo. Ele ainda tem o termo de vazão de base, λ = 0,20 e os números "71% / 33%", que o resumo já abandonou. Onde os dois divergem, digo qual é.

Resumo dos níveis de leitura:
- Hao (2022): texto completo (PDF local, 12 páginas).
- Baert (2026): texto completo (PDF local, 16 páginas). Os materiais suplementares (SM1 a SM7) não estavam no PDF e não li.
- Brandão (2025): texto completo (PDF local, 17 páginas). Os suplementos (S1 a S8) não estavam no PDF e não li.
- Woodward (2003): texto completo, do manuscrito (já extraído por outra checagem). Reconferi a Eq. 8 por conta própria.
- Valle Junior (2019): texto completo (o PDF local `C:\TCC\D3ySNXDWjrjvrpVvNP94W7H.pdf` é este artigo; 9 páginas).
- Eckhardt (2005): só resumo (e só parafraseado). O texto original está pago (a Wiley devolveu 403). Li o texto completo de outro trabalho do próprio Eckhardt (2012, HESS), que repete a equação do filtro e cita os valores de BFImax do artigo de 2005.

---

## 1. HAO et al. (2022): conectividade de sedimentos + MUSLE por pixel, em escala de evento

**Nível de leitura:** texto completo.

**O que é**
- Os autores aplicam a MUSLE em cada pixel de 30 m e depois multiplicam a erosão de cada pixel por um "grau de conectividade" (DSC, de 0 a 1). DSC é a fração do sedimento erodido no pixel que chega ao exutório. A soma dá o sedimento do evento: SY_sim = Σ E_unit · DSC.
- Três bacias chinesas, 58 eventos no total. Dali (Planalto de Loess, 1.310 km², 10 eventos), Duhe (montanhosa, 8.973 km², 18 eventos) e Xiangshui (morros com floresta, 1.749 km², 30 eventos). Chuva e vazão horárias. Chuva interpolada por IDW a partir de 26 postos.
- Desempenho (Tabela 4, ajuste com todos os eventos): NSE 0,74 (Dali), 0,83 (Duhe), 0,70 (Xiangshui). Willmott (WIA) 0,89, 0,95, 0,92. r = 0,98, 0,92, 0,85. Os parâmetros da conectividade (2 por bacia) foram calibrados por simulated annealing, maximizando um NSE em log (Eq. 11). Também fizeram validação cruzada leave-one-out; o texto diz que o NSE ficou acima de 0,78 (só li o texto, não os gráficos da Fig. 6).
- Resultado principal: em cerca de 80% da área a conectividade fica abaixo de 0,5, ou seja, a maior parte do sedimento erodido se deposita antes de chegar ao exutório. Em média 43,6% da área tem "descompasso" entre erosão alta e conectividade baixa.

**Fórmulas (Eqs. 1 a 4 do artigo)**
- Erosão local: `E_unit = 11,8 · (Q · pr · Área_unit)^0,56 · K · C · P · LS`. Q em mm, pr em m³/s, Área em m². E_unit é em toneladas, "perda potencial de solo de cada unidade por chuva".
- Escoamento: SCS-CN com λ = 0,2 (`Q = (R − 0,2S)² / (R + 0,8S)`), com R = chuva total do evento.
- Vazão de pico local, sem propagação: `pr = RI / (3600 · R_evento) · Q · Área_unit`. RI é a intensidade máxima do evento. Ou seja, o pico do pixel é o escoamento do pixel vezes a razão intensidade máxima / lâmina.
- K pelo método de Wischmeier e Smith; C pelo NDVI do mês do evento; LS por Liu et al. (2002); P por declividade e uso.
- A conectividade vem de um índice IC (Borselli) em que o peso W usa o próprio termo `11,8 · (Q · pr · Área)^0,56 · K · C · P`. Isso está nas Eqs. 5 a 9. O sedimento observado é `SY_obs = ∫ Qs · c dt`, vazão no exutório vezes concentração, e o artigo não fala em separar vazão de base.

**O que usamos no TCC**
- Seção 4.4 do rascunho / Passo 6 do resumo: a ideia de calcular o pico local do pixel sem roteamento, `pr = (Q/1000) · A_pix · (RI/R) / 3600`.
- Seção 4.4 / Passo 7: a MUSLE por pixel com 11,8 e 0,56 (E_unit).
- Seção 4.5 / Passos 9 e 10: o cálculo do parâmetro de escala em log (equivale ao Hao Eq. 11 com um único parâmetro) e a validação leave-one-out. Também a ideia de usar a soma dos E_unit como previsão do sedimento do evento.
- Seção 2 (rascunho, linhas 42 a 43): a estatística "cerca de dez eventos podem responder por mais da metade da produção anual (1.314 bacias)" e o "80% da área com conectividade abaixo de 0,5". Os dois estão corretos no artigo. O "dez eventos / 1.314 bacias" é citação de segunda mão (Hao cita Gonzalez-Hidalgo et al. 2010 e Li et al. 2020; não é resultado dele).
- Na prática, o TCC é o modelo do Hao com DSC = 1 (ou constante) em todos os pixels: SY = c · Σ E_unit. A conectividade não é usada.

**Atenção**
1. **Constantes 11,8 e 0,56 sem atribuição no Hao.** Hao não cita Williams (1975) em nenhum lugar (nem no texto, nem na lista de referências). A origem de 11,8 e 0,56 é Williams, mas isso vem do conhecimento geral, não do Hao. O TCC faz certo em citar "WILLIAMS, 1975; HAO et al., 2022"; só que a fonte que prova que o Hao usa esses valores é o Hao, e a fonte da origem é o Williams.
2. **Falta o fator 1/1000 na Eq. 4 do Hao.** A fórmula impressa no Hao não tem o `/1000` (Q em mm × Área em m² não dá m³). O TCC usa `Q/1000` (certo em unidade). O texto do TCC diz "com Q em mm, pr em m³/s e A_pix em m², como em Hao et al. (2022)": isso vale para as unidades declaradas, mas não para a fórmula impressa. O efeito é só de escala (fator 1000^0,56 ≈ 48 em todo pixel), que o c absorve. Vale uma frase dizendo que o `/1000` é correção do TCC.
3. **Erro de digitação no Hao.** A Eq. 3 do Hao diz `S = 25,4 · (100/CN − 10)`; o correto é 1000/CN. O TCC usa 1000/CN (certo).
4. **Q "em mm" dentro de (Q·pr·A)^0,56.** A fórmula de Williams original usa o volume de escoamento (m³); o Hao mistura mm, m³/s e m². O resumo já diz que E_unit é um "índice relativo", o que é a leitura honesta.
5. **Comparação de desempenho.** Os NSE do Hao (0,70 a 0,83) vêm de bacias cerca de 10 a 65 vezes maiores, de 10 a 30 eventos cada, com 8 ou mais postos de chuva por bacia e com a conectividade calibrada. O TCC tem 138 km², 17 eventos e 2 postos. Não dá para dizer que "chegamos ao nível do Hao"; o TCC só compara o MFM com a IC e com regras simples. O NSE da Tabela 4 é do ajuste com todos os eventos, não da validação cruzada.
6. **Não conciliado:** o texto do Hao diz NSE > 0,78 na validação cruzada (Fig. 6), mas a Tabela 4 tem NSE de 0,70 e 0,74 no ajuste. Uma validação cruzada acima do ajuste é estranha; não consegui ver a figura para conferir.
7. O TCC não usa conectividade, e o Hao mostra que, nas 3 bacias, ela muda o resultado (a erosão sozinha acerta menos). O TCC cita isso no texto (seção 2), então a limitação está dita. Vale deixar claro na Discussão que o Hao calibra 2 parâmetros de conectividade por bacia e o TCC calibra só 1 (c).

---

## 2. BAERT et al. (2026): regimes de início do escoamento e exportação de sedimento (Catena 274, 110497)

**Nível de leitura:** texto completo do artigo principal. Não li os suplementos (SM1 a SM7; neles estão as equações das formulações de Woodward/Hawkins/Jain e a lista de eventos).

**O que é**
- Bacia agrícola de loess em Chastre (Valônia, Bélgica), **83,84 ha (0,84 km²)**, sem rio permanente (rede de drenagem efêmera), quase só cultivo. Monitoramento de 2015 a 2023, chuva a 5 min, vazão em calha San Dimas, sedimento em coletor automático.
- Dados: 2.766 eventos de chuva, 1.057 acima de 1,27 mm, **154 eventos de escoamento** usados na parte hidrológica (15 foram descartados porque nenhum λ ≥ 0 reproduzia o escoamento). **46 desses 154 têm sedimento completo** e formam o conjunto da MUSLE. Os outros 108 não podem ser tratados como "sem sedimento": a amostragem era por evento e muitos tinham amostras incompletas ou rejeitadas.
- Método: acham, para cada evento, o λ ótimo (λopt) que reproduz o escoamento medido. Mediana de λopt = **0,056**, média 0,076, 80% central de 0,016 a 0,161. Depois agrupam os λopt em 5 "regimes" (K-means) e também tentam uma regressão contínua, e testam se dá para prever o regime/λ só com chuva, energia cinética, I30 e estação do ano.
- Fixos e da literatura (volume de escoamento, 154 eventos, Tabela 2): λ = 0,20 gera escoamento em **só 20 de 154 eventos** e dá NSE 0,13; λ = 0,05 (130 eventos com escoamento) dá NSE −7,00 e viés −217%; λ = 0,01 dá NSE −13,83; a fórmula de Woodward (0,05) dá NSE −0,87 e viés −45% ("a menos ruim das publicadas", em suas palavras).
- Diagnóstico (usando o próprio λopt do evento): 5 regimes preservam o volume (NSE 0,94) e o pico (NSE 0,67). Previsão fora da amostra (validação cruzada 5 vezes, repetida 10): regimes NSE 0,21 (volume) e −0,26 (pico); regressão contínua NSE 0,40 (volume) e 0,34 (pico).
- MUSLE: `SY = α · (Q · qp)^β · K · LS · C · P`, com **β fixo em 0,56 e só α calibrado** (Williams). Com Q e qp **medidos**: NSE de validação cruzada 0,66. Com Q e qp vindos do λopt: 0,46. Com regimes diagnósticos: 0,48. Com previsão fora da amostra: **−0,03 (regimes) e 0,01 (contínua)**; erro relativo (RRMSE) em torno de 260%.
- Conclusão deles: o início do escoamento (abstração inicial) é incerteza central; os erros do volume e do pico são amplificados pelo termo (Q·qp)^β; um λ único e mais baixo não resolve.

**O que usamos no TCC**
- Seção 2.2, rascunho linha 50: citam Baert para dizer que a qualidade da MUSLE depende da hidrologia, com NSE de sedimento próximo de zero (−0,03 e 0,01), bacia de 0,84 km², 154 eventos, 2015 a 2023.
- Seção 2.3, rascunho linha 67: NSE máximo de 0,13 para o volume com formulações fixas ou da literatura, e NSE de 0,21 a 0,40 fora da amostra; e a ideia de que a abstração inicial é uma das principais incertezas.
- (Uso potencial, ainda não no texto) Baert fixa β = 0,56 e calibra só o multiplicador, igual ao `c` do TCC. Esse é um apoio direto para o desenho do TCC.

**Atenção**
1. **"154 eventos alimentaram a MUSLE": não.** A MUSLE foi rodada só nos **46 eventos com sedimento**. Os 154 são a base hidrológica (escoamento e pico). O rascunho (linha 50) mistura as duas coisas. Sugestão: "154 eventos de escoamento, dos quais 46 com sedimento completo".
2. **"mesmo com o volume e o pico melhorados"** (rascunho, linha 50). Os NSE de −0,03 e 0,01 são de previsão fora da amostra, em que o volume tem NSE 0,21 e 0,40 e o pico −0,26 e 0,34. Ou seja, o pico por regimes ficou pior que a média. "Melhorado" só vale em relação ao 0,13 do λ fixo, e para o volume. Com volume e pico *medidos*, a MUSLE de Baert chega a NSE 0,66, e esse número é o que mostra que o gargalo é a hidrologia, como o TCC argumenta. Vale citar também esse 0,66 (é mais forte para o argumento do TCC do que os −0,03 e 0,01).
3. **"formulações calibradas por regimes, NSE de 0,21 a 0,40"** (linha 67): 0,21 é regimes e 0,40 é a regressão contínua. Não são os dois "por regimes".
4. **Baert é um contraponto ao uso do λ = 0,05.** Ele mostra que λ = 0,05 com CN não reconvertido infla o escoamento (viés −217%), e que mesmo a conversão de Woodward fica com NSE negativo e viés de −45% em 154 eventos. O resumo do TCC (Passo 3) já reconhece a inflação sem conversão (+94%) mas não cita Baert nesse ponto. Baert também diz que a "dificuldade não foi resolvida por escolher um λ universalmente mais baixo". Isso deve entrar na Discussão do candidato λ = 0,05, para não parecer que a literatura recente só apoia o 0,05.
5. A mediana λopt = 0,056 de Baert é compatível com 0,05, mas com dispersão enorme (0,016 a 0,161) e com um CN anual e λ ajustados juntos por evento. É uma bacia pequena, temperada, agrícola, sem rio permanente: bem diferente do Alto Jundiaí. Não há vazão de base no estudo.
6. Os autores avisam que o conjunto de 46 pode sub-representar eventos grandes e que não tinham acesso aos registros originais de campo.

---

## 3. BRANDÃO et al. (2025): CN e razão de abstração inicial em 3.578 bacias (J. Hydrology 655, 132941)

**Nível de leitura:** texto completo do artigo principal. Não li os suplementos S1 a S8 (neles estão a descrição do filtro de Eckhardt usado e as tabelas por país).

**O que é**
- Dados diários de chuva e vazão (Caravan e extensões: Dinamarca, Israel, Suíça, Espanha, Islândia, GRDC), 1950 a 2023, bacias com menos de 250 km², 32 países. Para separar o escoamento superficial da vazão total, usaram **o filtro de Eckhardt (2005)** (os parâmetros estão no S1, que não li).
- Calibram o CN em cada bacia por três métodos (mediana NEH, mínimos quadrados LS e assintótico ASY), com **λ = 0,20 e com λ = 0,05**, e com dois cortes de chuva: eventos > 25,4 mm (Grupo 1, **3.398 bacias**) e todos os eventos (Grupo 2, **3.578 bacias**).
- Achados: o LS é o melhor método. λ = 0,05 dá estimativas "mais adequadas" que 0,20 nos três métodos e nos cinco indicadores (R², RSE, NSE, PBIAS, KGE). Eles comparam só esses dois valores; **não estimam um λ por bacia**.
- Mas o desempenho absoluto é baixo: só uma pequena fração das bacias (menos de 15% em qualquer combinação da Tabela 1) passa no critério de bom ajuste (NSE > 0,5) com qualquer método (Tabela 1; exemplo LS Grupo 2: 10,7% com λ = 0,05 contra 8,9% com 0,20).
- Controles do λ (floresta aleatória + SHAP): a cobertura do solo manda; **lavoura (maior influência), áreas urbanas, solo arenoso, área da bacia e aridez empurram para λ = 0,05; mais pasto e clima úmido (índice de aridez baixo) apontam para λ = 0,2**.
- Equações de conversão (S em mm, Eqs. 17 a 20): `S0,05 = 0,919 · S0,20^1,174` (n = 3.398, R² 90,5%) e **`S0,05 = 0,917 · S0,20^1,170`** (n = 3.578, R² 89,9%), além de versões lineares com R² baixo (35% e 46%) e versões por país (Tabela 2).
- Eles citam Woodward (S0,05 = 1,33·S0,20^1,15, polegadas, que em mm vira 0,8187·S^1,15) e Hawkins et al. (2020), e dizem que seus resultados "ficam perto" desses.

**O que usamos no TCC**
- Seção 2.3, rascunho linha 66: "Brandão calibraram o CN por mínimos quadrados em 3.578 bacias e concluíram que o desempenho é melhor com λ = 0,05... associado a regiões áridas, maior área de cultivo, áreas urbanas e solos arenosos... fornecem equações para converter os parâmetros de λ = 0,2 para 0,05". Tudo isso confere com o resumo e as conclusões do artigo.
- Resumo do modelo, Passo 3, item 1 (apoio ao candidato λ = 0,05).

**Atenção**
1. **"Em 3.578 bacias, ficaram perto de 0"** (resumo do modelo, Passo 3, item 1): **isso não está no Brandão.** O artigo só compara λ = 0,05 com λ = 0,20; não estima um λ por bacia. A introdução do Brandão cita outros estudos que convergem a valores como 0, 0,01, 0,03 e medianas perto de 0,05, mas é revisão da literatura, não resultado dele. Troque por "o desempenho foi melhor com 0,05 do que com 0,20". (No rascunho 04, linha 66, a frase está correta; o erro está só no resumo.)
2. **"Melhor" é relativo.** Mesmo com 0,05, só uma fração pequena das bacias tem bom ajuste (NSE > 0,5). O artigo apoia "0,05 é preferível a 0,20", não "0,05 faz o SCS-CN prever bem".
3. **O próprio Brandão associa clima úmido e pasto a λ = 0,2**, e o Alto Jundiaí é úmido, com pasto, floresta, urbano e agricultura. A leitura honesta é "a literatura global favorece 0,05 em média, com exceções ligadas a clima úmido e pasto". Vale dizer isso se o candidato for adotado.
4. **A conversão de Brandão não é a de Woodward.** Em mm, Brandão dá S0,05 cerca de 21% a 26% maior que Woodward na faixa de S da bacia (conta minha: S = 50 mm → 73,6 contra 89,2; S = 180,6 → 322,4 contra 400,6; coincide com a faixa de 24 a 27% da checagem anterior). A escolha de Woodward não é a única possível, e a diferença entre as duas é grande. Vale registrar como incerteza da conversão.
5. Os dados são **diários** e o CN é **calibrado** por bacia; o TCC usa evento horário e CN **tabelado** (ANA) convertido. Ou seja, as equações de conversão foram ajustadas em calibrações, não em CN de tabela. Sobre isso, Woodward também ajustou S por bacia.
6. Brandão usa o filtro de Eckhardt (2005) para tirar a vazão de base antes de calibrar o CN: isso dá apoio à prática de comparar o SCS-CN só com o escoamento direto (não com o total).
7. Pequeno erro de digitação no artigo (conclusão cita "λ = 0,05 e 0,02" onde seria 0,20). Não afeta o TCC.

---

## 4. WOODWARD et al. (2003): razão de abstração inicial λ = Ia/S

**Nível de leitura:** texto completo (manuscrito de 10 páginas em PDF, extraído em `checagens_27-10\woodward_texto.txt`). A versão editorial da ASCE (DOI 10.1061/40685(2003)308) não abriu (403), então a numeração de páginas e equações é a do manuscrito.

**O que é**
- Reanálise dos dados chuva-escoamento de **307 bacias ou parcelas dos EUA** (ARS 134 bacias, parcelas da USLE 137, USFS 26, Jornada 6, USGS 4), 23 estados, majoritariamente leste, centro-oeste e sul; sem dados do noroeste. Só chuvas "grandes" (P ≥ 1 polegada = 25,4 mm; pelo menos 20 eventos por unidade).
- Dois métodos: análise de eventos (Ia = chuva até o hidrograma subir; λ mediano) e ajuste por mínimos quadrados de λ e S juntos. Na análise de eventos, λ variou de 0,0005 a 0,491, mediana **0,0476**, mais de 90% abaixo de 0,2. Em 252 dos 307 casos, λ = 0,05 deu r² maior e erro padrão menor que 0,20.
- Conclusão: λ ≈ 0,05 ajusta melhor que 0,20. Mudar λ exige mudar o CN. Eq. (8) (conferida por mim no texto): **`S0,05 = 1,33 · S0,20^1,15`, com S em polegadas**, arredondamento de dois ajustes, Eq. (6) `1,344·S^1,149` (dados naturais, r² 99,38%) e Eq. (7) `1,316·S^1,164` (ordenados, r² 99,44%). Eq. (9): `CN0,05 = 100 / (1,879·[100/CN0,20 − 1]^1,15 + 1)`.
- Efeito: o λ = 0,05 gera mais escoamento em chuvas pequenas e CN baixo, e menos em chuvas grandes (há uma chuva P_crit em que as duas curvas se cruzam). As relações se igualam em S = 0,148 pol (≈ 3,8 mm) e S = 0. No exemplo de hidrograma, CN = 50 dá pico cerca de 60% maior com λ = 0,05.

**O que usamos no TCC**
- Passo 3 do resumo (candidato): `S0,05 = 1,33 · S0,20^1,15` (S em polegadas); no código, `25,4·1,33·(S/25,4)^1,15`, que equivale a `S0,05(mm) = 0,8189 · S0,20(mm)^1,15`. Confere com o que o Brandão cita (0,8187).
- Justificativa de que λ = 0,05 é sustentado pela literatura (Passo 3, item 1: "Woodward et al. (2003) propõem 0,05") e que, ao mudar λ, é preciso converter S.
- No rascunho 04, Woodward ainda não aparece (o rascunho ficou com λ = 0,20).
- Observação: a nota "⚠️ Conferir a fórmula de conversão no original (citada de memória)" no Passo 3 do resumo **já pode ser removida**: confirmei a Eq. 8 com coeficiente 1,33, expoente 1,15 e unidade em polegadas.

**Atenção**
1. **A relação é uma regressão entre S's ajustados**, não uma identidade do SCS-CN. Foi feita só com chuvas ≥ 25,4 mm, em bacias e parcelas dos EUA. O TCC a aplica a eventos horários, com CN-I e pixel a pixel, inclusive eventos pequenos.
2. **Extrapolação.** A Tabela 4 do artigo vai de CN0,20 = 100 até 35. No TCC, 8,4% dos pixels têm CN-I < 35 (fora da tabela); a checagem anterior calculou isso.
3. O TCC usa o CN-I (condição seca) como "CN de λ = 0,20" e converte. Woodward ajusta o CN dos dados observados e fala dos CN de tabela do handbook; o texto não menciona umidade antecedente (AMC), então a aplicação da conversão ao CN-I é decisão do TCC, que o artigo não discute.
4. Woodward mesmo escreve que o efeito é "maior em CN baixos e chuvas baixas": é onde o candidato muda mais o resultado (e onde está o problema do λ = 0,20 nas chuvas pequenas). Isso é coerente com o §29 do TCC, mas a mesma região é onde a conversão é menos testada.
5. O artigo cita 28.301 eventos no texto e 28.031 na Tabela 3 (inconsistência interna do original; não afeta o TCC).
6. Citação: no manuscrito a lista de autores traz Hawkins, Hjelmfelt, Quan, Van Mullem, Woodward (sem Jiang); o Crossref traz Woodward, Hawkins, Jiang, Hjelmfelt, Van Mullem, Quan. A lista do TCC (referencias_consolidadas) segue o Crossref. Não é erro.

---

## 5. VALLE JUNIOR, RODRIGUES e OLIVEIRA (2019): λ e CN numa bacia tropical (RBRH 24, e5)

**Nível de leitura:** texto completo (o PDF local `D3ySNXDWjrjvrpVvNP94W7H.pdf` é este artigo, 9 páginas, acesso aberto).

**O que é**
- **Bacia do Guariroba**, Campo Grande, MS: área usada de 31.571 ha (**cerca de 316 km²**), 73% de pasto, 7% de eucalipto, 11% de floresta, solo quase todo arenoso (Neossolo Quartzarênico 95,7%), declividade média de 3,7%, clima Am, 1.400 mm/ano.
- **30 eventos** de chuva-vazão de 2015 a 2017, só eventos acima de ~25,4 mm (na verdade a faixa é de 22,6 a 88,1 mm; o resumo diz "> 25 mm", pequena inconsistência). Chuva a cada 10 min em 5 pluviômetros (Thiessen), vazão por régua de pressão.
- **Escoamento direto separado com filtro de Eckhardt**, usando a ferramenta WHAT (Lim et al., 2005), com BFImax = 0,80 ("sugerido por Eckhardt para rios perenes com aquífero poroso") e parâmetro de filtro 0,98, em dados diários.
- λ pela análise de eventos (Ia = chuva até o hidrograma subir). **λ de 0,005 a 0,455, mediana 0,045**; 96,7% dos valores abaixo de 0,2. Recomendam λ = 0,05.
- CN estimado por 5 métodos. Com λ = 0,2: CN de 53,1 (mínimos quadrados) a 69,3 (mediana). Com λ = 0,05: de 17,7 a 44,3. Conversão **linear** `S0,05 = a · S0,20` com **a = 2,865** (o valor recomendado pelo ASCE/NRCS em 2017 era 1,42).
- **Resultado negativo para o SCS-CN**: NSE negativo em quase todos os métodos, comportamento "complacente" (o coeficiente de escoamento não sobe com a chuva), e os autores concluem que o SCS-CN **não é adequado** nessa bacia, provavelmente porque domina o escoamento subsuperficial. Usar `Q = C·P` com C médio de 0,025 deu R² 0,71, NSE 0,66.

**O que usamos no TCC**
- Seção 2.3, rascunho linha 66: "Em bacia brasileira (Guariroba, MS), Valle Junior, Rodrigues e Oliveira (2019) estimaram λ mediano de 0,045." Confere (0,045, Guariroba, MS).
- Passo 3 do resumo, item 1: mesmo número, como apoio a λ baixo.

**Atenção**
1. **O artigo conclui que o SCS-CN não funciona na bacia estudada.** O TCC usa só o número de λ; vale não citar o artigo como se validasse o SCS-CN no Brasil. Na Discussão, o resultado de que "Q = C·P" supera o SCS-CN lembra o resultado do TCC (SY = c·chuva empata com o MC).
2. Bacia diferente da nossa: 316 km² (o Alto Jundiaí tem 138 km²), solo arenoso de alta infiltração e plano, sem urbanização. O Jundiaí tem relevo e urbano.
3. Só eventos grandes (≥ 22,6 mm), e λ vem de um método de evento (Ia lido no hidrograma), não de ajuste conjunto. Os valores são sensíveis a esse método.
4. **A conversão de S desse artigo (linear, a = 2,865) é muito maior que a de Woodward** (que dá razão 1,2 a 2,1 nos pixels do TCC). Se alguém propuser trocar a conversão por uma "brasileira", o escoamento muda bastante. O TCC usa Woodward; é uma escolha, não a única literatura.
5. A frase do rascunho "Em todos esses trabalhos, o CN é calibrado em conjunto com λ" vale para Woodward, Brandão e Valle Junior (que calcula CN pelos cinco métodos e depois converte o tabelado), mas **não vale para Baert**: Baert manteve o CN anual de λ = 0,20 sem recalibrar e variou só λ. Se Baert entrar na frase, ajustar.
6. Também usa o Eckhardt (2005): reforça o uso do filtro, mas com BFImax 0,80 (rio perene, aquífero poroso). Ver item 6 abaixo.

---

## 6. ECKHARDT (2005): filtros digitais recursivos para separar vazão de base (Hydrol. Processes 19(2), 507-515)

**Nível de leitura:** **só resumo** do artigo de 2005 (resumo conferido via Crossref, em paráfrase; o texto está atrás de pagamento, a Wiley devolveu 403). Para a equação e para os valores de BFImax, usei **Eckhardt (2012), HESS 16, 451-455, texto completo (PDF aberto)**, que repete o filtro e cita os valores de 2005, e uma página de documentação (baseflowx) para os três valores-guia. Não li o artigo de 2005 em si.

**O que é**
- Mostra que vários filtros de um parâmetro (Chapman-Maxwell, Boughton etc.) são casos de um filtro de **dois parâmetros**, baseado em armazenamento linear do aquífero. Os parâmetros são a constante de recessão **a** (que pode ser achada objetivamente por análise de recessão) e o **BFImax** (o maior índice de vazão de base que o filtro pode produzir). O BFImax não é mensurável, é um elemento subjetivo; o autor sugere que valores típicos poderiam ser associados a classes de bacias.
- Equação do filtro (a forma de Eckhardt 2012, Eq. 1, que reproduz a de 2005): `b_k = [ (1 − BFImax)·a·b_{k−1} + (1 − a)·BFImax·y_k ] / (1 − a·BFImax)`, com `b_k ≤ y_k` (b = vazão de base, y = vazão total, k = passo de tempo).
- Valores-guia atribuídos a Eckhardt (2005): **0,80** para rio perene com aquífero poroso, **0,50** para rio efêmero com aquífero poroso, **0,25** para rio perene com aquífero de rocha dura. Eckhardt (2012) confirma por escrito 0,80 e 0,50 como sugestão de 2005 e usa o 0,25 (rocha dura) no exemplo da análise de 2005. A página de documentação confirma os três e diz que são "ordem de grandeza", ponto de partida e não calibração.
- No estudo de 65 bacias norte-americanas de Eckhardt (2012): rios perenes com aquífero poroso tiveram a = 0,970 (passo diário) e BFI 0,67; efêmeros, a = 0,961 e BFI 0,42. E a constante **a** influencia mais o BFI do que o BFImax, quando ela é estimada por análise de recessão.

**O que usamos no TCC**
- Resumo, Seção 1 (dados): "Vazão de base (Bt): filtro de Eckhardt (2005), α = 0,995 e BFImax = 0,70, calibrado segundo Collischonn e Fan (2013), aplicado pelo orientador". O TCC reproduz a coluna Bt da série com esses parâmetros (checagem anterior: mediana de diferença 0,0016 m³/s). Passo 5 e Passo 8: a vazão de base serve para achar o escoamento direto medido (V_dir) que o MFM usa; **o sedimento-alvo continua sendo a carga total** e não há mais termo de base no modelo.
- Rascunho 04 (parágrafo marcado PENDENTE, linha 108, e item f, linha 395): equação do filtro e os parâmetros a = 0,995 e BFImax = 0,698; esse trecho ainda é anterior à decisão de 26/10 e traz as dependências do resultado (escoamento direto de 38% a 75% conforme o método).

**Atenção**
1. **BFImax = 0,70 não é nenhum dos três valores-guia (0,80; 0,50; 0,25).** Está entre o de rio perene poroso e o efêmero poroso. Eckhardt diz que o BFImax é subjetivo, então não é um erro, mas a justificativa deve vir de Collischonn e Fan (2013), que não está neste lote, e não de Eckhardt (2005). Se o aquífero da bacia for de rocha cristalina (não verifiquei a geologia), o guia de Eckhardt seria o 0,25, bem menor; isso precisa ser dito por quem conhece a bacia.
2. **A constante a depende do passo de tempo.** Os valores típicos de Eckhardt (cerca de 0,96 a 0,98) são para passo **diário**. O TCC usa a = 0,995 em passo **horário**. Pela conta de recessão exponencial (minha dedução, não do artigo), 0,995 por hora equivale a cerca de 0,89 por dia, uma recessão rápida. Isso não é incorreto, mas o TCC não deve comparar 0,995 com os 0,96 a 0,98 da literatura sem converter o passo.
3. **Origem dos parâmetros.** Os parâmetros foram obtidos por engenharia reversa da coluna Bt (o rascunho tem "PENDENTE: confirmar com os autores dos dados"). Não são calibrados pelo TCC. E o cabeçalho da planilha diz BFImax = 0,58, que não reproduz a série (pendência 2 do resumo).
4. **A equação do filtro no TCC confere** com a de Eckhardt (2012, Eq. 1) e, por ser a mesma forma, com a de 2005. Mas eu li a forma de 2012; se for citar a equação como "de Eckhardt (2005)", confira com o artigo original.
5. Os valores 0,80/0,50/0,25 foram confirmados por fonte secundária; o TCC precisa conferir no original (já está na pendência 3 do resumo).
6. Brandão (2025) e Valle Junior (2019) também usaram o filtro de Eckhardt para tirar o escoamento direto antes de calibrar o CN (Valle com BFImax 0,80 e parâmetro 0,98, em dados diários). Isso apoia a prática, mas nenhum dos dois justifica o 0,70 do TCC.

---

## Pontos que mais pedem correção no TCC (resumo)

1. **Resumo do modelo, Passo 3, item 1:** "Brandão ... ficaram perto de 0" não é do Brandão (ele só compara 0,05 com 0,20).
2. **Rascunho linha 50 (Baert):** a MUSLE foi rodada em 46 eventos, não nos 154; e os NSE −0,03 e 0,01 são de previsão fora da amostra (com o pico por regimes em NSE −0,26). Convém citar também o NSE 0,66 da MUSLE com Q e qp medidos.
3. **Rascunho linha 67 (Baert):** NSE 0,21 é regimes e 0,40 é regressão contínua.
4. **Candidato λ = 0,05:** Baert mostra NSE negativo mesmo com a fórmula de Woodward (−0,87) e λ = 0,05 sem conversão (−7,00); Brandão associa clima úmido e pasto a λ = 0,2; Valle Junior mostra que o SCS-CN falhou na bacia dele. A Discussão deve mostrar esses contrapontos.
5. **Hao:** declarar que o `/1000` na vazão de pico é correção do TCC e que o Hao não atribui 11,8 e 0,56 a Williams.
6. **Woodward:** a nota "citada de memória" pode sair; a Eq. 8 foi conferida (1,33, 1,15, polegadas).
7. **Eckhardt:** BFImax = 0,70 não vem dos valores-guia de Eckhardt; a = 0,995 é horário (≈ 0,89 diário). A justificativa depende de Collischonn e Fan (2013).
