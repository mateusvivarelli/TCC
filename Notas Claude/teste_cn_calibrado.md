# Teste independente: um CN "melhor calibrado" melhora o volume e o sedimento? (15/10/2026)

Revisor independente. Nenhum arquivo do projeto foi editado. Scripts e saídas brutas ficam em
`C:\Users\sonek\AppData\Local\Temp\claude\revisor2\` (`teste_cn.py`, `teste_cn_parte2.py` a `parte4.py`, `saida1.txt` a `saida3.txt`, `saida_orig_Qbom.txt`).
Pipeline reproduzido a partir de `_calibrar_cn_escoamento_direto.py` / `_avaliacao_B_com_Q_bom.py`: 154.011 pixels válidos (138,2 km²), S de `S - Seco.tif` realinhado por vizinho mais próximo, chuva `ChuvaIDW{N}.tif`, E_unit = 11,8·(Q·pr·A)^0,56·K·C·LS, SY = c1·ΣE + c2·Qb_inicio·dur·3600, com c1, c2 ≥ 0 em log.

## Resumo executivo

1. Calibrar a conversão chuva→escoamento melhora o **volume** direto previsto (LOO): o erro mediano cai de 69% para cerca de 40–47% e o NSE sobe de −0,69 para 0,39–0,46. Mas o resultado **não supera uma regressão log-log simples na chuva** (NSE 0,46).
2. O teto de qualquer conversão que use só a chuva é baixo. O coeficiente de escoamento direto medido varia de 0,03 a 0,22 (fator 7) e é praticamente independente da lâmina (r = 0,19 em log), de Qb_inicio e da chuva antecedente.
3. Calibradas livremente, as formas do tipo CN "desmontam" o SCS-CN. Em (i), λ vai para 0 e o CN-II equivalente cai para cerca de 51. Em (ii), S passa a crescer ∝ P^0,85–0,9, ou seja, o modelo vira um **coeficiente de escoamento quase constante** (0,07–0,12).
4. No **sedimento** (modelo B, LOO totalmente aninhado), nenhuma candidata difere do B original de forma estatisticamente distinguível. As diferenças em NSE-log vão de +0,02 a +0,08, com IC 95% bootstrap de cerca de [−0,2; +0,4]. O teste de Wilcoxon dá p de 0,6 a 0,9.
5. As melhores conversões para volume, (ii) e (iii), dão erro mediano de SY **pior** (37–40%) que o B original (33,1%). A melhor para sedimento, (i) com λ=0 (26,7%; NSE-log 0,56), é a **pior** das calibradas para volume (NSE −0,42).
6. Isso acontece porque o modelo B é insensível à escala do volume: c1 absorve o fator, e E ∝ Q^1,12. O SCS-CN com λ=0 e a=1 **superestima o volume em 165% (mediana) e dá o mesmo SY** que (i). O ganho de (i) vem do padrão espacial e entre eventos com λ=0, não de um volume melhor.
7. Correção importante sobre o "teto": o valor de 12%/94% em fator 2 só aparece com **água medida E base OBSERVADA (ΣBt)**. Forçando apenas a água ao medido, com a base prevista por Qb0·dur, o teto é 32,5% / 94% / NSE-log 0,71 com o padrão λ=0,20, e 19,9% / 94% / 0,82 com o padrão λ=0,05.
8. O evento 15 (48,7% da soma de quadrados linear de SY) não decide o ranking. Sem ele, todas as candidatas convergem para 33–42% de erro mediano e NSE-log 0,47–0,49, e o B original cai para 0,38–0,40.
9. A seleção honesta do candidato (LOO duplo: em cada evento retido, escolhe-se a melhor forma no LOO interno) dá NSE-log 0,530, erro mediano 26,7% e 71% dos eventos em fator 2. Isso é praticamente igual à referência trivial SY = c·chuva (0,534 / 41,9% / 82%).
10. Recomendação: o TCC **não** deve afirmar que um CN recalibrado resolve o gargalo. Pode afirmar que (a) o SCS-CN tabelado tem estrutura inadequada para o escoamento direto desta bacia, (b) o desempenho do sedimento é limitado pela variabilidade não explicada do coeficiente de escoamento (e da base), e (c) com n=17 nenhuma das variantes se distingue entre si nem de SY = c·chuva.

## 1. Verificação do que "já se sabe"

| Afirmação | Verificado? | Observação |
|---|---|---|
| V_dir = T_R_m3 − ΣBt·3600 | sim | coincide com Σ(Q−Bt)·3600 (diferença 0); a base é 34–55% do volume total |
| SCS λ=0,20 subestima 11/17, razão mediana 0,59 | sim | ev. 10: 0,02; 1: 0,03; 4: 0,06; 7: 0,06; 15: 1,94; 9: 1,95 |
| r(medido/SCS, lâmina) = −0,89 | **só em log** | r linear = −0,63; r(ln razão, ln P) = −0,88 |
| r com Qb_inicio = +0,03; com chuva de 5 dias = −0,09 | **não reproduzido** | obtive +0,26 e +0,17 (P5d = ΣPtot nos 5 dias antes do Início). Ambos são fracos e não significativos com n=17; a conclusão não muda |
| Regressão log-log: NSE LOO 0,47, erro absoluto médio 56% | aproximadamente | NSE 0,46; erro absoluto médio 47% no meu cálculo, porque meço o volume depois do limite Q ≤ P do pixel ao redistribuir; o script original mede antes |
| B original: 33,1% / 71% / NSE-log 0,48 / encostas ≈10% | sim | 33,1 / 71 / 0,481 / 10% |
| Teto "≈12% e 94% com a água forçada ao medido" | **não** | 11,7% exige também a **base observada** ΣBt (diagnóstico de `_avaliacao_B_com_Q_bom.py`). Só com a água medida: 32,5% / 94% / 0,712 (padrão λ=0,20) ou 19,9% / 94% / 0,821 (padrão λ=0,05) |

Vazamento menor no script `_avaliacao_B_com_Q_bom.py`, no passo intermediário com regressão: os volumes dos eventos de treino são previsões LOO que **incluem o evento retido**. Ao refazer de forma totalmente aninhada (meu (iii-a)), o erro mediano de SY passa de 34,9% para 39,3%. O efeito é pequeno, mas mostra que o erro mediano oscila cerca de 4 pontos com detalhes de procedimento.

## 2. Volume de escoamento direto (LOO aninhado; parâmetros sempre ajustados sem o evento avaliado)

Objetivo da calibração: mínimos quadrados de ln V. P = lâmina média IDW do evento; P0 = 54,8 mm (média geométrica).
Nas formas (iii), o volume é distribuído pelo padrão espacial do SCS-CN (λ=0,20), com Q ≤ P no pixel.

| Candidata | n. par. | Erro med. % | Erro médio % | Fator 2 % | NSE | NSE-log | Spearman | Parâmetros (17 eventos) |
|---|---|---|---|---|---|---|---|---|
| SCS-CN original (a=1, λ=0,20) | 0 | 69 | 58 | 59 | −0,69 | −3,72 | 0,67 | – |
| (i) S'=a·S, λ livre | 2 | 65 | 62 | 65 | −0,42 | 0,26 | 0,64 | a=2,68, λ=0,000 (borda) |
| (ii-a) S'=a·S·(P/P0)^k, λ=0,20 | 2 | 43 | 66 | 71 | 0,39 | 0,27 | 0,59 | a=0,70, k=0,89 |
| (ii-a) idem, λ=0,05 | 2 | 43 | 62 | 71 | 0,42 | 0,33 | 0,59 | a=1,46, k=0,85 |
| (ii-a') idem, λ livre | 3 | 43 | 59 | 71 | 0,45 | 0,38 | 0,58 | a=2,78, k=0,76, λ=0 |
| (ii-b) S'=a·S·(1−e^(−P/Pc)), λ=0,20 (forma assintótica de Hawkins) | 2 | 42 | 65 | 76 | 0,39 | 0,30 | 0,59 | a=5,6, Pc=409 mm |
| (ii-b) idem, λ=0,05 | 2 | 40 | 61 | 71 | 0,43 | 0,36 | 0,60 | a=7,6, Pc=253 mm |
| (iii-a) ln V = b0 + b1·ln P (coef. ∝ P^0,19) | 2 | 47 | 47 | 76 | 0,46 | 0,35 | 0,65 | b1=1,19 |
| (iii-b) ln V = b0 + b1·ln V_SCS | 2 | 51 | 51 | 71 | 0,38 | 0,30 | 0,62 | b1=0,31 |
| (iii-c) V = Cr·(P−Ia)·área | 2 | 53 | 48 | 71 | 0,46 | 0,33 | 0,65 | Cr=0,114, Ia=9 mm |
| (iii-d) ln V ~ ln P + ln Qb_inicio | 3 | 56 | 49 | 65 | 0,26 | 0,33 | 0,64 | – |
| TETO: V_dir medido (padrão SCS, Q≤P) | 0 | 1 | 13 | 94 | 0,93 | 0,79 | 0,95 | o limite Q≤P corta os eventos 1, 4, 7 e 10 |

Razão calculado/medido por evento (LOO):

| Ev. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P (mm) | 24 | 58 | 65 | 37 | 59 | 33 | 35 | 81 | 91 | 25 | 74 | 23 | 73 | 80 | 137 | 97 | 66 |
| Coef. medido | ,068 | ,217 | ,065 | ,192 | ,102 | ,040 | ,134 | ,112 | ,064 | ,158 | ,146 | ,032 | ,072 | ,084 | ,115 | ,119 | ,049 |
| SCS original | 0,03 | 0,18 | 0,88 | 0,06 | 0,59 | 0,31 | 0,06 | 0,90 | 1,95 | 0,02 | 0,51 | 0,16 | 1,15 | 1,26 | 1,94 | 1,13 | 1,10 |
| (i) a, λ | 0,58 | 0,40 | 1,68 | 0,30 | 1,05 | 1,70 | 0,43 | 1,20 | 2,41 | 0,27 | 0,80 | 1,62 | 1,74 | 1,65 | 1,80 | 1,29 | 2,22 |
| (ii-a) λ=0,20 | 0,95 | 0,34 | 1,42 | 0,34 | 1,06 | 2,83 | 0,56 | 0,92 | 1,74 | 0,44 | 0,60 | 4,68 | 1,43 | 1,34 | 0,98 | 0,86 | 1,76 |
| (ii-b) λ=0,05 | 1,11 | 0,35 | 1,40 | 0,36 | 0,99 | 2,75 | 0,57 | 0,88 | 1,69 | 0,49 | 0,60 | 4,03 | 1,37 | 1,25 | 0,97 | 0,82 | 1,79 |
| (iii-a) regressão | 0,62 | 0,40 | 1,47 | 0,37 | 0,90 | 1,90 | 0,46 | 0,87 | 1,68 | 0,20 | 0,64 | 1,64 | 1,37 | 1,19 | 0,93 | 0,83 | 1,99 |
| (iii-c) Cr·(P−Ia) | 0,55 | 0,41 | 1,54 | 0,38 | 0,94 | 1,87 | 0,47 | 0,90 | 1,70 | 0,19 | 0,66 | 1,62 | 1,42 | 1,22 | 0,91 | 0,85 | 2,09 |

Leitura dos resultados:

- O ganho sobre o SCS original é real em NSE-log (IC bootstrap da diferença sempre acima de 0) e em fator 2 (+12 a +18 pontos, IC [0; +30]). No erro mediano o IC é amplo: cerca de −55 a +25 pontos.
- Nenhuma forma do tipo CN supera a regressão (iii-a). As diferenças de erro mediano em relação a ela ficam entre −7 e +18 pontos, com IC cruzando zero, exceto (i), que é pior.
- O resíduo é dominado por eventos de mesma chuva e coeficientes muito diferentes: o evento 2 (58 mm, coeficiente 0,217) contra o 17 (66 mm, coeficiente 0,049), e o 12 (23 mm, 0,032) contra o 10 (25 mm, 0,158). Nenhuma forma baseada em P separa esses pares. Qb_inicio também não ajuda: (iii-d) piora no LOO.

## 3. Sedimento: modelo B em LOO totalmente aninhado

Em cada fold: parâmetros da conversão ajustados nos 16 eventos, E recalculado para todos, e c1, c2 ajustados nos 16. Só então o evento retido é previsto.

| Modelo | Erro med. % | Erro médio % | Fator 2 % | NSE-log | NSE lin. | Spearman | Parcela das encostas (mediana) |
|---|---|---|---|---|---|---|---|
| **B + SCS-CN original** | 33,1 | 55 | 71 | 0,481 | −0,60 | 0,72 | 10% |
| B + (i) a, λ (→λ=0) | **26,7** | 49 | 71 | **0,564** | −0,04 | 0,71 | 31% |
| B + (ii-a) λ=0,20 | 37,6 | 53 | 71 | 0,528 | −0,39 | 0,72 | 16% |
| B + (ii-a) λ=0,05 | 38,4 | 53 | 71 | 0,528 | −0,34 | 0,72 | 19% |
| B + (ii-a') 3 par. | 39,1 | 53 | 76 | 0,528 | −0,28 | 0,71 | 22% |
| B + (ii-b) λ=0,20 | 37,5 | 53 | 71 | 0,523 | −0,42 | 0,72 | 14% |
| B + (ii-b) λ=0,05 | 38,3 | 54 | 71 | 0,523 | −0,37 | 0,72 | 16% |
| B + (iii-a) regressão | 39,3 | 53 | 76 | 0,539 | −0,01 | 0,65 | 38% |
| B + (iii-b) | 39,9 | 55 | 76 | 0,520 | −0,14 | 0,66 | 34% |
| B + (iii-c) | 40,5 | 53 | 76 | 0,543 | −0,02 | 0,63 | 39% |
| B + (iii-d) | 38,7 | 56 | 71 | 0,503 | −0,23 | 0,67 | 40% |
| Seleção honesta do candidato (LOO duplo) | 26,7 | – | 71 | 0,530 | – | 0,71 | escolheu (i) em 16/17 folds |
| **Referência SY = c·chuva** | 41,9 | 55 | **82** | 0,534 | **0,58** | 0,63 | – |
| Referência SY = c·Qb0·dur (só base) | 38,8 | 58 | 76 | 0,483 | −0,83 | 0,71 | – |
| TETO água medida, padrão λ=0,20 | 32,5 | 35 | 94 | 0,712 | 0,61 | 0,81 | 67% |
| TETO água medida, padrão λ=0,05 | 19,9 | 28 | 94 | 0,821 | 0,73 | 0,82 | 83% |
| TETO água e base observadas (diagnóstico) | 11,7 | 21 | 94 | 0,874 | 0,80 | 0,87 | 42% |

### Sensibilidade ao padrão espacial: o resultado que explica (i)

| Mesmo volume, padrão SCS com λ_padrão = | 0,20 | 0,05 | 0,0 |
|---|---|---|---|
| SCS-CN a=1 (volume: erro mediano) | 69% | 101% | **165%** |
| SCS-CN a=1 → SY: erro med. / NSE-log | 33,1 / 0,481 | 37,4 / 0,548 | **26,7 / 0,566** |
| TETO (V medido) → SY | 32,5 / 0,712 | 19,9 / 0,821 | 20,4 / 0,824 |
| (iii-a) regressão → SY | 39,3 / 0,539 | 39,1 / 0,528 | 38,8 / 0,529 |

O SCS-CN **sem calibração** com λ=0 erra o volume em 165% (mediana) e dá exatamente o desempenho de sedimento de (i). O "ganho" de (i) no sedimento, portanto, não vem de um volume melhor. Vem da forma como λ=0 redistribui o escoamento entre eventos e no espaço, uma propriedade que nenhuma medição da bacia restringe (só se mede o volume no exutório). O padrão espacial também desloca o teto de 32,5% para 20%. Em suma, a parte "física" do B depende de uma escolha não identificável.

### Bootstrap pareado (5000 reamostragens dos 17 eventos sobre as previsões LOO)

| Comparação | ΔErro mediano (pp) | ΔFator 2 (pp) | ΔNSE-log | Wilcoxon (\|ln erro\|) |
|---|---|---|---|---|
| (i) − B original | −6,4 [−26,1; +9,1] | 0 [−24; +24] | +0,08 [−0,12; +0,33] (P>0: 0,81) | p = 0,64 |
| (ii-a) λ=0,20 − B original | +4,5 [−23; +15] | 0 [−18; +18] | +0,05 [−0,13; +0,31] | p = 0,78 |
| (ii-b) λ=0,20 − B original | +4,4 [−22; +16] | 0 [−18; +18] | +0,04 [−0,14; +0,30] | p = 0,89 |
| (iii-a) − B original | +6,3 [−17; +23] | +6 [−18; +29] | +0,06 [−0,19; +0,40] | p = 0,64 |
| (iii-c) − B original | +7,4 [−16; +22] | +6 [−18; +29] | +0,06 [−0,19; +0,39] | p = 0,61 |
| (i) − SY=c·chuva | −15,2 [−22; +21] | −12 [−35; +12] | +0,03 [−0,78; +0,26] | – |
| B original − SY=c·chuva | −8,8 [−20; +18] | −12 [−35; +12] | −0,05 [−0,97; +0,29] | – |
| TETO λ=0,20 − B original | −0,6 [−33; +19] | **+24 [0; +53]** (P>0: 0,95) | +0,23 [−0,10; +0,99] (P>0: 0,93) | p = 0,16 |
| Candidatas (ii)/(iii) − TETO | +5 a +8 | −18 a −24 [−50; 0] | −0,17 a −0,21 [−0,9; +0,15] | p = 0,13–0,28 |

Os IC das diferenças entre conversões calibradas e B original cruzam zero em todas as métricas, e por margem larga. Até o teto (volume perfeito) fica só no limite da significância em relação ao B original (fator 2: IC [0; +53]; NSE-log: P>0 = 0,93). Com n=17, a resolução estatística do teste é de cerca de ±0,2 em NSE-log e ±20 pontos no erro mediano. Qualquer diferença menor que isso é ruído.

### Papel do evento 15

O evento 15 tem SY = 3829 t (média 1403 t), o que representa 48,7% da soma de quadrados linear de SY (confere) e 30,3% da de V_dir.

- Por isso o NSE linear é inutilizável. Todos os B ficam entre −0,6 e 0 e passam a cerca de −1 a −2 quando o evento 15 sai da avaliação. Só SY = c·chuva (0,58) e os tetos (0,6–0,8) têm NSE linear positivo.
- As conversões calibradas consertam o volume do evento 15 (razão 1,94 → 0,95), mas **pioram** seu SY (razão 0,78 → 0,60). Corrigir o volume do maior evento não ajuda o sedimento, porque c1 e c2 são reajustados.
- Com o evento 15 fora da avaliação, o B original vai a 36,4% / 69% / 0,397. As candidatas (ii) vão a 33,1% / 69% / 0,47, (i) a 34,5% / 0,49 e (iii) a 39–42% / 0,47. As diferenças entre (i) e (ii)/(iii) somem.
- Refazendo tudo sem o evento 15 (n=16, LOO aninhado), o resultado é: B original 37,4% / 0,380 (encostas 4%), (i) 34,9% / 0,485, (ii-a) 35,2% / 0,474, (iii-a) 41,3% / 0,475, SY = c·chuva 41,2% / 0,462 e teto 35,3% / 94% / 0,661. O ranking entre as candidatas não é robusto. Só a distância até o teto (em fator 2 e NSE-log) persiste.

## 4. Plausibilidade física e riscos

**Valores calibrados** (S de `S - Seco.tif`, CN-I; CN pixel-médio 52,5 ≈ CN-II 71,6; Ia = 0,2·S ≈ 51 mm em média, maior que a chuva de 5 dos 17 eventos):

- (i): a = 2,54–2,95 nos folds, λ = 0 em **todos** os folds (borda do domínio). Isso dá CN-I ≈ 30, CN-II ≈ 51, sem abstração inicial. É fisicamente pouco crível como "CN da bacia": é um CN de mata densa em solo B para uma bacia com uso agrícola e urbano. λ=0 só significa que parte da bacia produz escoamento desde o primeiro milímetro (área impermeável ou saturada perto da rede). A forma do SCS está sendo usada como ajuste de curva, não como teoria.
- (ii-a)/(ii-b): S cresce com a chuva do evento (k = 0,82–1,04 nos folds; Pc ≫ P). O CN-II equivalente vai de 89 nos eventos pequenos a 63 nos grandes (λ=0,20). A literatura registra CN decrescente com P ("comportamento padrão" de Hawkins), o que dá alguma defesa à forma. Mas aqui não há assíntota dentro da faixa observada, e o expoente ≈ 1 transforma o SCS em coeficiente de escoamento constante (0,065–0,126 previsto contra 0,032–0,217 medido). A curvatura do SCS é rejeitada pelos dados. É mais honesto escrever diretamente (iii-c) V = 0,11·(P − 9 mm)·área.
- (iii-c): Cr = 0,11 e Ia = 9 mm são valores plausíveis e interpretáveis, e o desempenho equivale ao de qualquer forma CN.

**Riscos de vazamento e sobreajuste:**

1. *Seleção de forma.* Testei 11 formas e escolhi a melhor olhando o mesmo LOO. Em (i), a seleção honesta (LOO duplo) devolve NSE-log 0,530 em vez de 0,564: um otimismo de cerca de 0,03, do mesmo tamanho do ganho sobre SY = c·chuva. O "ganho" de (i) sobre a referência trivial desaparece.
2. *Parâmetros na borda.* λ=0 em todos os folds indica que o ótimo está fora do domínio do modelo. Os IC usuais dos parâmetros não valem nesse caso.
3. *Graus de liberdade.* A conversão usa 2 parâmetros (até 3) e o B mais 2: são 4–5 parâmetros para 17 pontos. O LOO aninhado protege o erro de previsão, mas a variância entre candidatas (erro mediano de SY de 26,7 a 40,5%) é do mesmo tamanho dos IC. Não há informação para escolher.
4. *Alvo com erro.* V_dir depende da separação de base (34–55% do volume). Um erro de ±10% em ΣBt muda V_dir em ±10–20%, o que limita qualquer calibração do volume.
5. *Métrica.* O erro mediano com n=17 muda cerca de 4 pontos com detalhes de procedimento (ex.: 34,9 → 39,3% só por aninhar corretamente a regressão). Não deve ser usado sozinho para ranquear modelos.
6. *Parcela das encostas.* Ela depende da conversão (10% → 14–40%) e do padrão espacial (teto: 67% com λ=0,20 contra 83% com λ=0,05). Portanto não é uma estimativa física robusta; é um subproduto da escolha da conversão.

## 5. Conclusão e o que o TCC pode afirmar

**O "CN melhor" não resolve o gargalo.** A calibração melhora o volume de forma modesta, até o nível de uma regressão na chuva (NSE ~0,45, erro mediano ~45%). Essa melhora **não se transmite** ao sedimento: as diferenças contra o B original são ruído (IC de NSE-log [−0,15; +0,35]; Wilcoxon p ≥ 0,6). O único candidato que parece melhor, (i), melhora por causa de λ=0 no padrão espacial, não do volume, e com seleção honesta empata com SY = c·chuva. O teto com água medida (32,5% / 94% / 0,71, ou 20% / 94% / 0,82 dependendo do padrão espacial) mostra que haveria ganho real em fator 2 e NSE-log **se** o volume de cada evento fosse conhecido. Mas o que falta para chegar lá é a variabilidade do coeficiente de escoamento entre eventos de mesma chuva (fator ~7), que nenhuma conversão baseada só em P captura com estes dados.

**Afirmações defensáveis:**

- O SCS-CN com CN tabelado (CN-I, λ=0,20) é estruturalmente inadequado para o escoamento direto desta bacia. Ele subestima eventos pequenos em até 50 vezes e superestima os grandes em cerca de 2 vezes, e o coeficiente medido é quase independente da lâmina.
- Recalibrar CN e λ, ou tornar o CN dependente da chuva, reduz o erro de volume ao nível de uma regressão empírica. Os parâmetros obtidos (λ→0, CN-II ≈ 51, ou S ∝ P) indicam que o comportamento é de coeficiente de escoamento aproximadamente constante (~0,1), não de SCS.
- No sedimento, com 17 eventos, o modelo de dois componentes não se distingue estatisticamente da referência SY = c·chuva, com nenhuma das conversões testadas. A parcela atribuída às encostas (10–40%) depende da conversão e do padrão espacial adotados, e deve ser apresentada como indeterminada ou dependente de hipótese.
- O potencial do modelo, se o volume direto fosse conhecido, é real em fator 2 (94% contra 71%, IC [0; +53] pp), mas fica no limite da significância com n=17.

**O que não afirmar:** que a calibração do CN "melhora o modelo de sedimento"; que o erro de 26,7% de (i) é uma melhoria (é seleção e ruído); que o teto é 12% (isso exige base observada); qualquer ranking entre as variantes (ii) e (iii).

**Sugestão, se houver espaço:** apresentar (iii-c) [V = Cr·(P − Ia)] ou (iii-a) como conversão empírica transparente e documentar o SCS-CN como "testado e rejeitado". Mostrar no texto o teto com água medida separando "água medida" de "água e base observadas". Reportar o resultado do sedimento contra SY = c·chuva, com IC bootstrap.
