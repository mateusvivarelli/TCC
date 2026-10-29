# Proposta de texto: seção 5 (Resultados e Discussão), modelo oficial

Escrita na noite de 29/10/2026 por uma sessão na nuvem, sem acesso ao usuário. **Nada foi aplicado no Google Doc.**

Fontes dos números: `TCC_Texto/tabelas/*.md`, `Dados Iniciais/comparacao_SY_lambda005_woodward.csv`, `notas_musle_espacializada.md` (§29, §32 a §34), `relatorio_checagens_base_alvo_woodward_27-10.md` e a planilha `Planilhas/planilha_calculos_concentrados.xlsx` (recalculada; confere com os números oficiais). Números que eu mesmo calculei esta noite a partir do CSV estão marcados (calculado nesta noite).

Regras: caracteres de teclado; nada de método descartado; o NSE linear não é argumento principal; "IC refeita" sempre que o número for do TCC.

Numeração nova (ver `mapa_figuras_tabelas_secoes_4_a_6.md`): Tabelas 11 a 14 e Figuras 6 a 12 nesta seção. Figuras: legenda acima e "Fonte:" abaixo (ABNT); tabelas: título acima e fonte abaixo.

---

## 5.1 Escoamento direto: SCS-CN contra o medido

**Texto proposto**

O primeiro passo do modelo é transformar a chuva em escoamento direto. A Tabela 3 (seção 3.2) e a Figura 6 comparam, evento a evento, o volume calculado pelo SCS-CN com o escoamento direto medido (volume total menos a vazão de base). No conjunto, os dois quase coincidem: o SCS-CN soma 15,7 milhões de m³, contra 15,3 milhões medidos (viés de +2,9%). Evento a evento, porém, o erro é grande: o erro médio absoluto é de 53,9% e o mediano, de 46,3%; a razão entre calculado e medido vai de 0,10 (evento 10) a 2,15 (evento 9), e só 65% dos eventos ficam dentro de fator 2. O NSE do volume é -0,39, ou seja, como previsão evento a evento, o SCS-CN erra mais do que errar prevendo sempre a média dos eventos.

Os erros se compensam: o SCS-CN superestima 8 eventos (3, 8, 9, 13, 14, 15, 16 e 17), em geral os de maior chuva, e subestima os outros 9, em geral os de menor chuva (1, 4, 7 e 10 ficam abaixo de 0,25 do medido). Isso acontece porque, na curva do SCS-CN, o escoamento cresce mais que proporcionalmente com a chuva, enquanto nos eventos medidos a fração da chuva que escoa não depende da lâmina de chuva (correlação de -0,01 entre o coeficiente de escoamento medido e a chuva do evento). O viés pequeno do total não significa, portanto, um bom modelo de evento.

**Figura 6.** Arquivo: `TCC_Texto/figuras/fig_volume_direto.png`.
Legenda sugerida: "Figura 6. Escoamento direto por evento: calculado pelo SCS-CN (CN-I, λ = 0,05 com S convertido) contra o medido. A faixa indica fator 2." Fonte: elaborado pelo autor.

(c) O que muda no Doc: a 5.1 atual ("o volume e a carga medidos incluem a vazão de base") vira esta subseção. A constatação de que o medido inclui a base já está na 3.2.

---

## 5.2 Resultados do Modelo Calculado (MC)

**Texto proposto**

O MC usa só a chuva dos postos. Com c = 0,0344 t por unidade de E_unit, o erro percentual mediano na validação cruzada foi de 81,1%, e 35% dos eventos (6 de 17) ficaram dentro de fator 2; o NSE em escala logarítmica foi -0,69 e a correlação de Spearman, 0,59 (Tabela 12). O MC superestima 10 eventos e subestima 7, e os erros são grandes nos dois sentidos: o evento 10 recebe 10% do sedimento medido e o evento 9, 3,1 vezes o medido (Tabela 11). A Figura 7 compara o sedimento simulado, na validação cruzada, com o medido em cada evento, para o MC, o MFM e duas referências.

Os eventos com sedimento subestimado são os mesmos com escoamento subestimado (1, 2, 4, 7 e 10), e os superestimados são os de escoamento superestimado (3, 9, 13, 14 e 15). O erro do sedimento acompanha o erro da água: a correlação entre o logaritmo do erro do sedimento e o logaritmo da razão de volume (SCS-CN/medido) é de 0,96, e o erro da água explica 91% da variância do erro do sedimento.

**Tabela 11. Sedimento por evento (t): medido e simulado pelo MC e pelo MFM, no ajuste e na validação cruzada.** Arquivo: `TCC_Texto/tabelas/tab_mc_mfm_eventos.md` (colar inteiro). Fonte: elaborado pelo autor.

**Figura 7.** Arquivo: `TCC_Texto/figuras/fig_dispersao.png` (4 painéis).
Legenda sugerida: "Figura 7. Sedimento simulado na validação cruzada contra o medido nos 17 eventos: referência SY = c * chuva, MC, MFM e IC refeita. A faixa indica fator 2; os números identificam os eventos." Fonte: elaborado pelo autor.

(c) O que muda no Doc: todos os números (c1 = 0,0035 e c2 = 0,0131, 32,6%, 71%, 0,48, 0,72 saem); sai o parágrafo da composição encostas/base e a Figura 7 antiga (composição). A Tabela 11 perde as colunas "Encostas" e "Base".

**Pontos de atenção (não vão para o Doc)**
- A correlação 0,96 e os 91% são de `notas_musle_espacializada.md` §33 (modelo oficial).
- Contagem de 10 superestimados / 7 subestimados e razões 0,10 e 3,15: calculado nesta noite a partir do CSV (colunas SY_calc_LOO_t e SY_obs_t).

---

## 5.3 O gargalo: transformar chuva em escoamento

**Texto proposto**

O MFM recebe o escoamento direto medido e usa a mesma fórmula de erosão, os mesmos fatores K, C e LS e o mesmo padrão espacial do SCS-CN; só a quantidade de água de cada evento muda. Com c = 0,0222, o erro mediano na validação cruzada cai de 81,1% para 20,6%, a fração dentro de fator 2 sobe de 35% para 94%, o NSE em log passa de -0,69 para 0,84 e o Spearman, de 0,59 para 0,83 (Tabela 12). A Figura 8 mostra essa diferença lado a lado com as regras simples.

A qualidade do sedimento estimado depende, portanto, sobretudo da qualidade da estimativa do escoamento. A fórmula de erosão e a espacialização não são o limite: o limite está na conversão da chuva em escoamento direto. Um teste intermediário confirma o padrão: estimando o volume direto por uma regressão simples na chuva (em vez do SCS-CN), o erro mediano da MUSLE espacializada fica em 47,2%, entre o MC e o MFM.

**Figura 8.** Arquivo: `TCC_Texto/figuras/escada_gargalo.png`.
Legenda sugerida: "Figura 8. Erro percentual mediano e eventos dentro de fator 2, na validação cruzada, com a água calculada da chuva e com a água forçada ao medido, para a MUSLE espacializada e para a regra simples com o mesmo insumo." Fonte: elaborado pelo autor.

(c) O que muda no Doc: números (era 71% para 94%, 32,6% para 13,6%, parcela das encostas de 9% para 38%); saem as frases sobre os dois componentes e sobre a vazão de base medida.

**Pontos de atenção**
- O teste da regressão na chuva (47,2%) é o nível N2 de `escada_gargalo.csv` e **não está na figura** (a figura só mostra N1 e N3). Se o usuário não quiser descrever esse teste no método, cortar a última frase.
- A nota de rodapé da figura diz "Sem termo de vazão de base": é menção a método descartado dentro da imagem (ver item E). Sugiro regerar a figura sem essa frase quando houver acesso ao PC.

---

## 5.4 Comparação com as regras simples

**Texto proposto**

Para saber se a espacialização acrescenta algo, cada versão do modelo foi comparada a uma regra simples que usa a mesma informação medida (Tabela 12).

Com só a chuva, a regra SY = c * R (c = 19,72 t por mm de chuva) teve erro mediano de 41,9%, 82% dos eventos dentro de fator 2 e NSE em log de 0,53, bem melhor que o MC (81,1%; 35%; -0,69). A diferença do erro por evento entre o MC e a regra da chuva tem mediana de +32,6 pontos, com intervalo de confiança de 95% de +3,1 a +117,5 pontos: o MC é pior, e a diferença não se explica pelo acaso. A razão é a mesma da seção 5.3: a regra da chuva não depende da forma da curva do SCS-CN, que é justamente a parte que falha nesta bacia.

Com o escoamento direto medido, a regra SY = c * V_dir (c = 0,00158 t/m³) teve erro mediano de 15,9%, 94% dentro de fator 2 e NSE em log de 0,85, e o MFM ficou em 20,6%, 94% e 0,84. A diferença entre os dois tem mediana de +1,6 pontos, com intervalo de -5,5 a +10,4: não se distinguem. A espacialização não perde precisão em relação à regra simples com a mesma água, e acrescenta o mapa de onde o sedimento é produzido.

**Tabela 12. Desempenho na validação cruzada (calibração em escala logarítmica; carga total de sedimentos).** Montada a partir de `notas_musle_espacializada.md` §32 e da planilha (não há arquivo `.md` pronto com o Spearman; ver nota):

| Modelo | Informação medida usada | Erro mediano (%) | Dentro de fator 2 (%) | NSE em log | Spearman |
|---|---|---|---|---|---|
| SY = c * chuva | chuva | 41,9 | 82 | 0,53 | 0,63 |
| MC | chuva | 81,1 | 35 | -0,69 | 0,59 |
| SY = c * V_dir | chuva e escoamento direto medido | 15,9 | 94 | 0,85 | 0,90 |
| MFM | chuva e escoamento direto medido | 20,6 | 94 | 0,84 | 0,83 |
| IC refeita | volume total e vazão de pico medidos | 16,3 | 100 | 0,87 | 0,93 |

Fonte: elaborado pelo autor.

(c) O que muda no Doc: a 5.4 atual ("O modelo de dois componentes e os testes simples") é reescrita; muda a conclusão: o MC agora fica **abaixo** da regra da chuva.

**Pontos de atenção**
- Spearman: MC 0,59 e MFM 0,83 vêm de §32; SY = c * chuva 0,63, SY = c * V_dir 0,90 e IC 0,93 vêm da planilha recalculada nesta noite (o relatório de checagens de 27/10 dá 0,63 e 0,90 para as duas regras; a IC refeita não tinha Spearman registrado nas notas: **0,93 é cálculo desta noite**, conferir).
- Intervalos de confiança: §32 (bootstrap de eventos). O método está descrito na proposta da 4.8.
- NSE linear: só no Apêndice (`tab_nse_linear.md`), como pede a regra. **Atenção:** `tab_nse_linear.md` tem linhas "Não adotado" (λ 0,20, dois componentes). Pela regra 3, essas linhas **não devem entrar no Apêndice do Doc**; usar só as 6 primeiras linhas.

---

## 5.5 Comparação com a IC refeita

**Texto proposto**

A formulação concentrada da IC (Vivarelli et al., 2025), Y = α * (V * qp)^β * K * LS * C * P, usa o volume e a vazão de pico medidos no hidrograma do evento e os fatores K, LS e C médios da bacia (0,031; 0,536; 0,267). A IC publicou o ajuste nos 17 eventos (α = 0,277 e β = 0,807), com erro médio de -4,15% e erros de -60% a +37%, sem validação cruzada. Para compará-la nas mesmas condições do modelo deste trabalho, ela foi refeita: α e β recalibrados em escala logarítmica (α = 0,978 e β = 0,733 com os 17 eventos) e avaliados na mesma validação cruzada. Para reproduzir os erros publicados, foi preciso usar o volume total e o pico total medidos, isto é, com a vazão de base incluída.

A IC refeita teve erro mediano de 16,3%, 100% dos eventos dentro de fator 2 e NSE em log de 0,87 (Tabela 12). O MFM, que recebe informação equivalente (o escoamento direto medido), ficou em 20,6%, 94% e 0,84. A diferença do erro por evento entre os dois tem mediana de +6,1 pontos, com intervalo de confiança de 95% de -8,6 a +7,9 pontos: com 17 eventos, os dois não se distinguem. As diferenças de formulação (expoente livre, volume total, pico medido) custam poucos pontos de erro, e a espacialização em si não custa nada.

A IC refeita, no entanto, não é uma previsão: precisa do hidrograma do evento, que é medido no mesmo lugar e ao mesmo tempo que o sedimento; não gera mapa; e seus dois coeficientes foram ajustados nos mesmos 17 eventos. Com informação equivalente, a espacialização iguala a qualidade da formulação concentrada e acrescenta o mapa de áreas críticas.

(c) O que muda no Doc: números; frase "IC refeita" no lugar de "IC"; a Tabela 12 passa a ter a linha da regra SY = c * V_dir. **O erro mediano de 16,3% não deve ser atribuído à IC publicada.**

**Pontos de atenção**
- "Espacializar em si não custa nada": vem da escada IC -> MFM de §29 (passos 4 e 5: 22,2% e 18,5% nessa escada). Os números da escada são de uma análise de 27/10 com o padrão espacial λ 0,05; o passo 5 (18,5%) difere do MFM oficial (20,6%) porque a escada usa outro arranjo de entradas. Se o usuário quiser os números da escada no texto, conferir antes; a proposta só usa a frase qualitativa.
- A IC usa 17 eventos com um evento diferente do TCC (24/11/2018 no lugar de 17/12/2018; ver lote C). Isso afeta a comparação com os erros publicados. Pergunta pendente ao orientador; vale uma frase na 5.7 se ele confirmar.

---

## 5.6 Mapas

### 5.6.1 Da chuva ao sedimento, evento a evento

**Texto proposto**

As Figuras 9 a 11 mostram, para os 17 eventos, a chuva interpolada, o escoamento direto calculado pelo SCS-CN e o sedimento produzido em cada pixel pelo MC, com a mesma escala de cores em todos os eventos. Na chuva (Figura 9), o gradiente leste-oeste varia conforme o que cada posto registrou: a chuva é maior a oeste (posto de Campo Limpo) em 13 dos 17 eventos e maior a leste (posto DBT5) nos eventos 1, 2, 4 e 17; no evento 12, o DBT5 não registrou chuva.

O escoamento direto (Figura 10) acompanha a lâmina de chuva do evento e o número de curva: é baixo nos eventos de menor chuva e alto no evento 15, o maior, e é maior nas áreas de CN mais alto (Figura 3). O sedimento (Figura 11) tem sempre os mesmos pontos de maior contribuição, que mudam de intensidade de um evento para outro, mas não de lugar: o padrão espacial é dominado pelos fatores fixos (K, C e LS), e a chuva e o escoamento definem a intensidade do evento.

**Figuras:**
- Figura 9: `TCC_Texto/figuras/mapas/mapa_04_chuva_eventos.png` (não mudou). Legenda: "Figura 9. Chuva total de cada evento, interpolada pelo inverso do quadrado da distância a partir de dois postos."
- Figura 10: `TCC_Texto/figuras/mapas/mapa_05_escoamento_eventos.png` (regerado). Legenda: "Figura 10. Escoamento direto calculado pelo SCS-CN (CN-I, λ = 0,05 com S convertido) em cada evento."
- Figura 11: `TCC_Texto/figuras/mapas/mapa_06_sedimento_eventos.png` (regerado). Legenda: "Figura 11. Sedimento produzido em cada pixel em cada evento (MC)."
- Em todas: "Fonte: elaborado pelo autor."

(c) O que muda no Doc: saem "quase nulo nos eventos menores (1, 4, 6, 7, 10 e 12)" e "o extremo oeste sempre com os maiores valores" (eram do modelo antigo; **não conferi nos mapas novos**, por isso o texto proposto ficou genérico); legenda da Figura 10 troca "CN seco, λ = 0,20"; legenda da Figura 11 troca "nas encostas".

**Atenção:** eu não abri os mapas 4 a 6 nesta noite para descrever o padrão novo. O usuário deve olhar a Figura 10 e, se quiser, acrescentar uma frase concreta (quais eventos têm pouco escoamento). Pela Tabela 3, os eventos 1, 10, 12, 4 e 7 têm os menores volumes calculados.

### 5.6.2 Sedimento médio e áreas críticas

**Texto proposto**

A Figura 12 mostra o sedimento médio dos 17 eventos e as áreas críticas, definidas como os 5% de pixels de maior contribuição, para o MC e o MFM. Os dois mapas são muito parecidos (correlação de 0,98; 94,2% das áreas críticas coincidem): o padrão espacial quase não depende da forma de estimar a quantidade de água. A correlação de cada mapa com o produto K * C * LS é de 0,77 (MC) e 0,76 (MFM), o que mostra que os fatores fixos explicam a maior parte do padrão, mas não todo: o escoamento de cada pixel, que depende do CN, também pesa.

As áreas críticas se concentram em manchas na porção central e oeste da bacia e em algumas manchas pequenas ao sul. A contribuição é muito desigual entre os usos (Tabela 13): o campo ocupa 29,0% da área e responde por 37,4% do sedimento; a silvicultura ocupa 12,7% e responde por 24,2%; a lavoura temporária ocupa 3,9% e responde por 20,9%; o solo exposto ocupa 0,5% e responde por 8,2%; a mata nativa ocupa 39,6% e responde por 7,5%; e as áreas urbanizadas (14,1%) têm erosão nula no modelo (C = 0). Por unidade de área, a lavoura temporária produz cerca de cinco vezes a média da bacia e o solo exposto, cerca de 18 vezes. Entre os solos (Tabela 14), 92,9% do sedimento vem dos Cambissolos Háplicos, que têm o maior K (0,0475) e ocupam 68,6% da área. As porcentagens do MFM são quase iguais (Tabelas 13 e 14).

Esses resultados dependem dos valores de K e C adotados por classe e não foram validados no espaço, porque só há medição de sedimento no exutório; devem ser lidos como contribuições relativas. A coincidência entre os mapas do MC e do MFM também não é uma validação independente: os dois distribuem a água pelo mesmo padrão do SCS-CN e usam os mesmos K, C e LS.

**Figura 12.** Arquivo: `TCC_Texto/figuras/mapas/mapa_07_sedimento_medio.png` (regerado; 4 painéis MC e MFM). Legenda: "Figura 12. Sedimento médio dos 17 eventos e áreas críticas (5% dos pixels de maior contribuição), para o MC e o MFM." Fonte: elaborado pelo autor.
(Existe também `fig_mapa_sy_medio.png`, só MC, 2 painéis; sugiro usar o `mapa_07`, que corresponde à Figura 11 atual do Doc.)

**Tabela 13. Contribuição de cada classe de uso para o sedimento médio (MC e MFM).** Arquivo: `TCC_Texto/tabelas/tab_classes_uso.md`.
**Tabela 14. Contribuição de cada classe de solo para o sedimento médio (MC e MFM).** Arquivo: `TCC_Texto/tabelas/tab_classes_solo.md`.
Nos dois arquivos há uma última coluna "Contribuição / área, calculado (%)" que não existe no Doc; manter ou cortar (o texto acima usa a ideia em "cinco vezes" e "18 vezes": 530% e 1.772% da média).

(c) O que muda no Doc: correlação 0,97 para 0,98; 90,9% para 94,2%; frase sobre K*LS*C (era 0,69 e Spearman 0,79; agora 0,77 e 0,76, Pearson; não há Spearman registrado); todas as porcentagens por classe; Cambissolos 94% para 92,9%.

**Atenção**
- A mineração aparece com 1,8% do sedimento (MC) em 0,0% da área (`tab_classes_uso.md`): poucos pixels de C = 1 sem fonte (lote D). Vale uma frase se o orientador perguntar.
- Os valores de C do campo (0,050) e da lavoura temporária (0,212), as duas classes que mais pesam depois da silvicultura, **não conferem com as fontes citadas pela IC** (ver `leitura_referencias/loteD_fontes_K_C.md`). Isso entra na 5.7 como limitação.

---

## 5.7 Discussão e limitações

**Texto proposto** (parágrafos curtos; o usuário pode cortar)

**O que limita o modelo calculado é a água.** O erro do MC é quase todo herdado do erro do volume de escoamento direto (91% da variância). O SCS-CN, com CN tabelado e um único CN para todos os eventos, não reproduz a resposta desta bacia, em que a fração da chuva que escoa quase não depende do tamanho da chuva. Melhorar o MC passa por melhorar a água: mais postos de chuva ou chuva por radar e satélite, outra forma de gerar o escoamento, ou, na prática, usar a vazão medida onde houver posto.

**O que sobra no modelo forçado é a concentração de sedimento.** Com a água medida, a variação que o modelo não explica é a da quantidade de sedimento por m³ de escoamento direto, que vai de 1.085 a 3.806 mg/L entre os eventos (3,5 vezes). O erro do MFM acompanha o da regra SY = c * V_dir (correlação de 0,67), que usa a mesma água sem a MUSLE: o erro de 15,9% dessa regra está perto do mínimo possível com estes dados. Há também um contraste entre as duas estações chuvosas: o MFM superestima os eventos de 2018/19 (eventos 1 a 6, de +18% a +84%) e subestima os de 2019/20 (eventos 14 a 17, de -10% a -55%); a carga por m³ de escoamento direto sobe, em média, de cerca de 1.480 mg/L para cerca de 2.040 mg/L. A causa não foi identificada: pode ser uma mudança na fonte de sedimento, no sensor de turbidez ou na curva que converte turbidez em CSS.

**O evento 17 (20/02/2020)** é o único fora do fator 2 no MFM (simulado 0,45 vez o medido, -55%). Sua carga por m³ de escoamento direto é de 3.806 mg/L, contra 1.085 a 2.088 mg/L nos outros 16 eventos, e a regra SY = c * V_dir também o subestima (-61%). Uma explicação possível é a curva turbidez-CSS operar fora da faixa em que foi calibrada; outra é uma fonte de sedimento que o modelo não representa. O evento foi mantido.

**Razão de abstração inicial.** O λ = 0,05 com a conversão de Woodward et al. (2003) foi a configuração em que o volume calculado mais se aproximou do medido nesta bacia, mas a literatura recente não é unânime. Baert et al. (2026), numa bacia agrícola de 0,84 km² na Bélgica, obtiveram NSE de volume de -0,87 com a fórmula de Woodward e concluíram que um λ fixo mais baixo não resolve a incerteza do início do escoamento. Brandão et al. (2025), em 3.578 bacias, acharam desempenho melhor com λ = 0,05 do que com 0,20 em média, mas associaram clima úmido e mais pasto a valores próximos de 0,20, e o Alto Jundiaí é úmido e tem 29% de campo. Valle Junior, Rodrigues e Oliveira (2019) estimaram λ mediano de 0,045 numa bacia de Mato Grosso do Sul, mas concluíram que o SCS-CN não era adequado para ela. A própria conversão é incerta: a equação de Brandão et al. (2025) daria, nesta bacia, retenções 24% a 27% maiores que a de Woodward. Além disso, 8,4% dos pixels têm CN-I abaixo de 35, fora da faixa tabelada por Woodward et al. (2003); neles, a conversão é extrapolação.

**Condição de umidade.** O CN-I foi usado como condição única para os 17 eventos. O critério dos 5 dias de chuva antecedente do NEH-4 (USDA-SCS, 1972), que coloca 13 eventos na condição seca, foi abandonado no manual atual do NRCS (NEH Parte 630, 2004), que não encontrou relação entre chuva antecedente e CN em várias bacias. Por isso o CN-I é sustentado aqui pelo volume medido, não pelo critério antecedente.

**Escolhas e avaliação nos mesmos eventos.** O λ, a condição de umidade e a conversão foram escolhidos olhando o escoamento dos mesmos 17 eventos usados na avaliação, e a validação cruzada refaz apenas o coeficiente c. As métricas da validação cruzada são, portanto, um pouco otimistas para essas escolhas. Com 17 eventos, diferenças de 2 a 4 pontos no erro mediano não são interpretáveis, e os intervalos de confiança das comparações são largos.

**Vazão de base e alvo.** Todo o sedimento do evento foi atribuído ao escoamento superficial, e a vazão de base foi tratada só como transporte. Se a água de base tiver a mesma concentração da mistura em cada hora, a carga do escoamento direto seria cerca de 66% da total, e o MFM teria erro mediano de 12,9% em vez de 20,6%, sem mudar a ordem dos modelos. A separação da base pelo filtro de Eckhardt também é uma escolha: com outras separações, o MFM fica entre 15,1% e 21,9% de erro mediano e 94% dentro de fator 2.

**Fatores K e C.** Os valores por classe vêm da IC. Na conferência das fontes, os valores da mata nativa, da silvicultura e do solo exposto conferem; os do campo (C = 0,050) e da lavoura temporária (C = 0,212) não puderam ser confirmados nas fontes citadas, e o K do Cambissolo (0,0475) é o valor de uma amostra individual. Isso não muda o sedimento total do evento (c absorve a escala), mas muda o peso relativo das classes no mapa.

**Espaço.** O modelo não tem roteamento nem conectividade: o sedimento de cada pixel chega ao exutório na mesma proporção (c), o que é uma simplificação forte em relação a Hao et al. (2022), que calibram um índice de conectividade. E a área urbana tem erosão nula por hipótese (K = 0 e C = 0), embora obras, vias não pavimentadas e solo exposto urbano produzam sedimento.

(c) O que muda no Doc: seção nova (o Doc não tem 5.7). Junta a discussão que hoje está espalhada e os contrapontos.

**Pontos de atenção (não vão para o Doc)**
- **Regra 3:** evitei λ = 0,20 como alternativa nossa; ele aparece só na frase de Brandão ("valores próximos de 0,20"), que é resultado da literatura, como pedido no item C. Se o usuário achar que fere a regra, trocar por "associaram clima úmido e mais pasto a valores mais altos de λ".
- **Alvo direto (12,9%) e separações alternativas (15,1% a 21,9%):** são análises de sensibilidade (`relatorio_checagens_base_alvo_woodward_27-10.md`), não métodos descartados; mas o usuário pode preferir não citar números de sensibilidade. A frase "cerca de 66% da total" vem de 15.752/23.846 t = 66,1% (calculado nesta noite a partir do relatório).
- **Baert (2026):** "-0,87" é o NSE do volume com Woodward em 154 eventos; o relatório do lote A recomenda também citar que, com volume e pico **medidos**, a MUSLE de Baert chega a NSE 0,66 (apoio ao "gargalo é a água"). Pode entrar no primeiro parágrafo da 5.7.
- **Brandão:** "24% a 27% maiores" é da checagem de 27/10 (mediana na bacia); o lote A dá 21% a 26% por conta própria. Use "cerca de um quarto maiores" se quiser evitar o número exato.
- **NEH-630 (2004):** lido (cap. 10, texto aberto, lote B). Precisa entrar na lista de referências se for citado.
- **Turbidez-CSS:** a pergunta da curva (lei de potência de 2022 ou regressão por partes de 2023) é do orientador; o texto só diz "curva que converte turbidez em CSS".
- **Evento 24/11 x 17/12/2018:** não incluí (depende de resposta do orientador).

---

## Referências citadas na seção 5 e nível de leitura

| Referência | Nível | Uso |
|---|---|---|
| Vivarelli et al. (2025), IC | texto completo | IC publicada e refeita |
| Baert et al. (2026) | texto completo (sem suplementos) | contraponto ao λ = 0,05 |
| Brandão et al. (2025) | texto completo (sem suplementos) | contraponto; conversão alternativa |
| Valle Junior, Rodrigues e Oliveira (2019) | texto completo | λ 0,045; SCS-CN inadequado na bacia deles |
| Woodward et al. (2003) | texto completo do manuscrito | faixa da Tabela 4 (CN 35 a 100) |
| USDA-SCS (1972), NEH-4 | original não acessado; limites por fonte secundária | critério dos 5 dias |
| NRCS (2004), NEH Parte 630, cap. 10 | texto completo do capítulo | abandono do critério dos 5 dias (acrescentar à lista) |
| Hao et al. (2022) | texto completo | conectividade |
| Eckhardt (2005) | só resumo (Eckhardt 2012 completo) | separação da base (já citado na 2.4) |
