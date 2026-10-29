# Lote D: fontes dos valores de K e C por classe (29/10/2026, noite)

Pedido do orientador: a fonte de cada valor de K e C da Tabela 5 (K) e da Tabela 6 (C). Os valores e as fontes vêm da IC (Vivarelli et al., 2025, Tabelas 1 e 2 do artigo; conferi no PDF do artigo da IC que está na raiz do repositório). Nesta noite baixei e li os originais que estavam abertos na web. Nada foi mudado no Google Doc.

## Resumo (o mais importante)

| Valor da nossa tabela | Fonte dada pela IC | Confere? |
|---|---|---|
| K Cambissolo Háplico 0,0475 | Corrêa, Moraes e Pinto (2015) | **Confere, mas é o valor de UMA amostra** (amostra 8, CXvd, Tabela 5, p. 855). A média dos Cambissolos no próprio artigo é 0,036 (Tabela 6) |
| K Argissolo Vermelho-Amarelo 0,0351 | Silva (2016), dissertação UFRGS | **Não conferido**: o repositório LUME não abriu da nuvem (falha de conexão em 4 tentativas). Atenção: 0,0351 é exatamente a média dos **Neossolos** em Silva e Alvares (2005) |
| K Afloramento Rochoso 0,0087 | Martins et al. (2011) | **Não confere**: o artigo dá 0,007, 0,017 e 0,0004; não há classe "afloramento rochoso" nem o número 0,0087 |
| K Neossolo Litólico 0,0463 | 5 fontes | **Nenhuma fonte dá 0,0463**, e nenhuma média simples dos valores delas reproduz 0,0463. Uma das 5 (Castro et al., 2011) nem tem Neossolo Litólico. Efeito no resultado: nulo (0,0% dos pixels) |
| C cultura anual 0,2116 | Silva e Luchiari (2016) | **Número existe, mas é o C da soja** (Tabela 2, p. 23). O artigo dá 0,1418 para "cultura anual" (média de milho e soja) |
| C reflorestamento 0,121 | Silva et al. (2016) | **Confere** (eucalipto implantado em 2004, o mais jovem; Tabela 4, p. 440) |
| C vegetação nativa 0,015 | Silva et al. (2016) | **Confere** (floresta nativa; Tabela 4, p. 440) |
| C pastagem 0,050 | Silva et al. (2016) | **Não confere**: o artigo não trata de pastagem. (Silva e Luchiari, 2016, dão 0,0049 para pasto) |
| C solo exposto 1,0 | Wischmeier e Smith (1978) | Confere por definição (C é a razão contra o pousio limpo, que vale 1) |
| C corpo hídrico 0 | Wischmeier e Smith (1978) | Não visto no AH 537 (lote B); é convenção (água não tem perda de solo) |

**O que isso significa para o TCC.** Dos 10 valores, 4 conferem com o original (0,0475 com ressalva, 0,121, 0,015, 1,0), 1 não pôde ser conferido (0,0351), e 4 não conferem com a fonte citada (0,0087, 0,0463, 0,2116 como "cultura anual", 0,050). Os que não conferem pesam assim na bacia: Campo (C = 0,050) cobre 29,0% da área e responde por 37,4% do sedimento do mapa; Lavoura Temporária (C = 0,212) cobre 3,9% e responde por 20,9%; Afloramento (0,1%) e Neossolo Litólico (0,0%) não pesam. **O C do Campo e o da Lavoura Temporária são os dois que importam para o mapa.** No sedimento total, c absorve qualquer fator constante; o que muda é a distribuição espacial (o peso relativo de campo e lavoura).

**Sugestão (decisão do usuário/orientador):** (1) manter os valores (são os da IC; o resultado agregado não muda) e citar como fonte "Vivarelli et al. (2025), com base em ..." só onde a fonte confere; (2) para pastagem e cultura anual, declarar no texto que o valor vem da IC sem fonte primária conferida, ou trocar por valores com fonte conferida (por exemplo, pasto 0,0049 e cultura anual 0,1418 de Silva e Luchiari, 2016). A opção (2) muda o mapa e exige rodar de novo os rasters (não dá para fazer na nuvem). Eu não mudei nada.

---

## Fontes de K

### 1. Corrêa, Moraes e Pinto (2015)

**Nível de leitura:** texto completo (PDF do periódico, 13 páginas, extraído e lido; tabelas 5 e 6 e discussão com cuidado).

**Conteúdo.** Estima a erodibilidade (K) pelo método indireto de Denardin (1990) e a tolerância de perda de solo para 15 amostras de solos derivados de arenitos e argilitos em duas bacias afluentes do rio Corumbataí (ribeirão Jacutinga e córrego do Monjolo Grande), centro-leste paulista: Argissolo Vermelho-Amarelo, Neossolo Quartzarênico e Cambissolo Háplico. K variou de 0,0075 a 0,1573 t h MJ-1 mm-1 entre as amostras. Os autores destacam a grande variação de K dentro de uma mesma classe de solo.

**Valor da nossa tabela:** K = 0,0475 (Cambissolos Háplicos). **Confere como número**: Tabela 5 (p. 855), amostra 8, Cambissolo Háplico Ta distrófico (CXvd), bacia do Jacutinga: 0,0475. O texto (p. 857) diz que é o maior valor dos Cambissolos do Jacutinga (faixa de 0,0075 a 0,0475). **Mas não é um valor representativo da classe:** os 6 Cambissolos do artigo têm K de 0,0075 a 0,0536, com média de 0,036 e desvio padrão de 0,019 (Tabela 6, p. 858). A IC escolheu uma amostra individual, sem dizer por quê.

**Referência ABNT:** CORRÊA, E. A.; MORAES, I. C.; PINTO, S. A. F. Estimativa da erodibilidade e tolerância de perdas de solo na região do centro leste paulista. **Geociências**, São Paulo, v. 34, n. 4, p. 848-860, 2015. Disponível em: https://periodicos.rc.biblioteca.unesp.br/index.php/geociencias/article/view/10582. Acesso em: 29 out. 2026.
(Sem DOI no Crossref; a busca no Crossref não achou o artigo.)

### 2. Silva (2016), dissertação UFRGS

**Nível de leitura:** **não acessível nesta noite.** O LUME (repositório da UFRGS) recusou a conexão nas 4 tentativas (curl e WebFetch, erro de proxy/503). Só vi o registro por resultado de busca: "Erodibilidade de um argissolo vermelho-amarelo e fator manejo e cobertura vegetal da equação universal de perdas de solo", Tiago Stumpf da Silva, orientador Elemar Antonino Cassol, PPG em Ciência do Solo da UFRGS, handle 10183/157631. Segundo o resumo (lido só no trecho do buscador), usa perdas de solo sob chuva natural de 1976 a 1989 em Argissolo Vermelho-Amarelo distrófico típico na Estação Experimental Agronômica da UFRGS (Eldorado do Sul, RS) para obter K (perda de solo contra erosividade na parcela padrão) e C (cinco estádios das culturas).

**Valor da nossa tabela:** K = 0,0351 (Argissolos Vermelho-Amarelos). **Não conferido.** Alerta: 0,0351 é exatamente a média dos **Neossolos** na Tabela 1 de Silva e Alvares (2005) (p. 37). Pode ser coincidência, mas vale abrir a dissertação para confirmar. O ano também precisa ser conferido (uma página da UFRGS lista o título em 2017).

**Referência ABNT (da IC, a conferir):** SILVA, T. S. **Erodibilidade de um Argissolo Vermelho-Amarelo e fator manejo e cobertura vegetal da Equação Universal de Perdas de Solo**. 2016. 166 f. Dissertação (Mestrado em Ciência do Solo) - Faculdade de Agronomia, Universidade Federal do Rio Grande do Sul, Porto Alegre, 2016. Disponível em: http://hdl.handle.net/10183/157631. Acesso em: 29 out. 2026 (página não carregou).

**Para a sessão das 02:30 ou para o usuário:** tentar de novo `https://lume.ufrgs.br/handle/10183/157631`, achar o PDF e procurar "0,0351".

### 3. Martins et al. (2011)

**Nível de leitura:** texto completo (PDF do periódico, 6 páginas, lido).

**Conteúdo.** Determina K por parcelas sob chuva natural (novembro de 1997 a maio de 2004) em três solos dos Tabuleiros Costeiros em Aracruz (ES): Argissolo Amarelo textura média/argilosa (PA1), Plintossolo Háplico (FX) e Argissolo Amarelo moderadamente rochoso (PA2). K foi o coeficiente angular da regressão entre perda de solo e erosividade (EI30).

**Valor da nossa tabela:** K = 0,0087 (Afloramento Rochoso). **Não confere.** O artigo dá 0,007 (PA1), 0,017 (FX) e 0,0004 Mg h MJ-1 mm-1 (PA2) (resumo, p. 322; conclusões, p. 326). Não há classe de afloramento rochoso, e o número 0,0087 não aparece no texto (procurei todos os números da forma 0,0xxx). O mais próximo em sentido é o PA2 (moderadamente rochoso, 0,0004), que é 20 vezes menor. Efeito no TCC: o afloramento é 0,1% dos pixels; não pesa.

**Referência ABNT:** MARTINS, S. G.; AVANZI, J. C.; SILVA, M. L. N.; CURI, N.; FONSECA, S. Erodibilidade do solo nos tabuleiros costeiros. **Pesquisa Agropecuária Tropical**, Goiânia, v. 41, n. 3, p. 322-327, 2011. DOI: https://doi.org/10.5216/pat.v41i3.9604. Acesso em: 29 out. 2026.
(Conferido no Crossref e na página do periódico.)

### 4. Neossolos Litólicos (K = 0,0463): cinco fontes

Nenhuma das cinco dá 0,0463. Os valores de Neossolo Litólico (ou de Neossolos) que elas trazem:

| Fonte | Valor(es) | Onde | O que é |
|---|---|---|---|
| Silva e Alvares (2005) | 0,0351 (média de 26 valores, DP 0,0127) | Tabela 1, p. 37 | **Neossolos em geral** (não separa o Litólico) |
| Chagas et al. (2011) | 0,043027 a 0,128948 (12 unidades RLd/RLe; média 0,0997) | Tabela 1, p. 20-21 | K calculado por (areia + silte)/argila/100 (fórmula de Mannigel et al., 2002) em Mato Grosso do Sul |
| Rocha Lima et al. (2016) | 0,0440 (n = 3) e 0,0179 (n = 1), horizonte A; 0,0349 e 0,0163, horizonte B | Tabela 1, p. 67 | Neossolo Litólico Eutrófico fragmentário, textura média e argilosa |
| Demarchi e Zimback (2014) | 0,048 (Denardin) e 0,018 (Mannigel), horizonte A | Tabela, p. 109 | Neossolo Litólico Eutrófico (RLe) |
| Castro et al. (2011) | **não tem Neossolo Litólico**; Neossolo Quartzarênico 0,0567 | Tabela 5, p. 316 | Solos do cerrado goiano |

Testei todas as médias simples de 2 a 5 desses valores: nenhuma dá 0,0463 (± 0,00006). A média de 0,0440 e 0,048 é 0,046, a mais próxima; pode ter sido arredondada, mas é suposição. **Efeito no TCC: nenhum** (Neossolo Litólico tem 0,0% dos pixels de cálculo).

**4a. Silva e Alvares (2005).** Nível: texto completo (PDF, 10 páginas; a Tabela 1 é imagem e foi lida visualmente). Revisão bibliográfica que monta um banco de dados de K por classe de solo do mapa pedológico paulista, com 134 valores de 13 trabalhos. Médias: Argissolos 0,0425, Cambissolos 0,0508, Latossolos 0,0162, Neossolos 0,0351, Organossolos 0,0610 (maior), Planossolos 0,0097 (menor). Conclui que a maioria dos solos paulistas tem erodibilidade alta. (Unidade impressa na tabela: t.ha-1.MJ-1.mm-1.)
Referência: SILVA, A. M.; ALVARES, C. A. Levantamento de informações e estruturação de um banco de dados sobre a erodibilidade de classes de solos no estado de São Paulo. **Geociências**, São Paulo, v. 24, n. 1, p. 33-41, 2005. Disponível em: https://www.periodicos.rc.biblioteca.unesp.br/index.php/geociencias/article/view/181. Acesso em: 29 out. 2026.
**Observação útil:** esta é a fonte mais próxima da bacia (São Paulo, por classe). Para o Cambissolo, ela dá 0,0508 (média de 7 valores), próximo do 0,0475 adotado.

**4b. Chagas et al. (2011).** Nível: texto completo (boletim de 63 p., PDF de 15 MB da Infoteca-e da Embrapa; li a seção 2.2.5.2 e a Tabela 1). Zoneamento agroecológico de um município de MS, com potencial natural de erosão por K * LS * R. O K de cada unidade de mapeamento foi calculado pela fórmula K = [(%areia + %silte)/(%argila)]/100 (Mannigel et al., 2002), com média ponderada até 100 cm.
**Correção bibliográfica:** são 13 autores, pela ficha catalográfica (Chagas é o primeiro); é o Boletim de Pesquisa e Desenvolvimento n. 181.
Referência: CHAGAS, C. S. et al. **Zoneamento agroecológico do município de Dois Irmãos do Buriti - MS**. Rio de Janeiro: Embrapa Solos, 2011. 63 p. (Boletim de Pesquisa e Desenvolvimento, 181). Disponível em: https://www.infoteca.cnptia.embrapa.br/infoteca/handle/doc/919009. Acesso em: 29 out. 2026.

**4c. Rocha Lima et al. (2016).** Nível: texto completo (PDF, 14 páginas; li a Tabela 1 e o resumo). Erodibilidade (método indireto) e tolerância de perda de 33 tipos de solo na bacia do baixo São José dos Dourados (noroeste paulista) e correlação com atributos químicos; carbono orgânico e cálcio foram os melhores indicadores.
Referência: ROCHA LIMA, C. G.; CARVALHO, M. P.; SOUZA, A.; COSTA, N. R.; MONTANARI, R. Influência de atributos químicos na erodibilidade e tolerância de perda de solo na bacia hidrográfica do baixo São José dos Dourados. **Geociências**, São Paulo, v. 35, n. 1, p. 63-76, 2016. Disponível em: https://periodicos.rc.biblioteca.unesp.br/index.php/geociencias/article/view/10992. Acesso em: 29 out. 2026.
(Na ABNT o sobrenome composto pode entrar como "LIMA, C. G. R." ; mantive a forma da IC. Conferir a regra da FEC.)

**4d. Demarchi e Zimback (2014).** Nível: texto completo (PDF, 13 páginas; li a tabela de K e a discussão). Levantamento detalhado de solos da sub-bacia do Ribeirão das Perobas (Santa Cruz do Rio Pardo, SP) e mapas de erodibilidade (Denardin, 1990, e Mannigel et al., 2002) e de tolerância de perda. O método de Denardin deu K mais altos e diferenciou menos as classes.
**Correção bibliográfica (importante):** a revista é **Energia na Agricultura** (Botucatu), não "Revista de Engenharia Agrícola" como está na IC; e a segunda autora é Célia Regina Lopes Zimback (ZIMBACK, C. R. L., não "C. R. L. M."). Conferido no Crossref e no PDF.
Referência: DEMARCHI, J. C.; ZIMBACK, C. R. L. Mapeamento, erodibilidade e tolerância de perda de solo na sub-bacia do Ribeirão das Perobas. **Energia na Agricultura**, Botucatu, v. 29, n. 2, p. 102-114, 2014. DOI: https://doi.org/10.17224/EnergAgric.2014v29n2p102-114. Acesso em: 29 out. 2026.

**4e. Castro et al. (2011).** Nível: texto completo (PDF, 16 páginas; li o resumo, a discussão e a Tabela 5, que é imagem). Analisa textura, densidade, porosidade e retenção de água de 4 classes de solos agrícolas de Goiás (Argissolo Vermelho eutrófico, Latossolo Vermelho acriférrico, Neossolo Quartzarênico e Nitossolo Vermelho eutroférrico) e o K pela classificação de Mannigel et al. (2002): 0,0031; 0,0042; 0,0567; 0,0027. **Não tem Neossolo Litólico**: não sustenta o valor.
Referência: CASTRO, W. J.; LEMKE-DE-CASTRO, M. L.; LIMA, J. O.; OLIVEIRA, L. F. C.; RODRIGUES, C.; FIGUEIREDO, C. C. Erodibilidade de solos do cerrado goiano. **Revista em Agronegócios e Meio Ambiente**, Maringá, v. 4, n. 2, p. 305-320, maio/ago. 2011. Disponível em: https://periodicos.unicesumar.edu.br/index.php/rama/article/view/1656. Acesso em: 29 out. 2026.
(A IC omitiu o número do fascículo, n. 2.)

### K = 0 da Área Urbana (sem fonte)

Classe "Área Urbana" do mapa de solos (13,7% dos pixels): K = 0 adotado pela IC, sem fonte. Só listo.

---

## Fontes de C

### 5. Silva e Luchiari (2016)

**Nível de leitura:** texto completo (PDF, 14 páginas; li métodos, Tabela 2 e resultados).

**Conteúdo.** Aplica a USLE em SIG na bacia do Córrego Baguaçu (oeste paulista) para estimar a perda de solo. O fator C foi calculado pela metodologia de Wischmeier e Smith (1978), por estádio das culturas, para cana-de-açúcar, pasto, milho, soja e eucalipto. A maior parte da bacia tem perda baixa (0 a 3 t/ha/ano), com predomínio de pastagem e cana.

**Valor da nossa tabela:** C = 0,212 (Lavoura Temporária; a IC escreve 0,2116 para "cultura anual"). **O número existe, mas é o C da soja** (Tabela 2, p. 23, coluna "Soja", linha "Fator C (total)"; milho = 0,0720). O texto diz (p. 22-23): "A média do fator C para o milho e soja, ou seja, cultura anual é de 0,1418". Então, se a classe é "cultura anual", o valor do próprio artigo seria 0,1418, não 0,2116. O mesmo artigo dá **pasto = 0,0049** e eucalipto = 0,000829.

**Correção bibliográfica:** a primeira autora é Laís Coêlho do Nascimento Silva (SILVA, L. C. N.); a IC escreve "SILVA, L." e "Córrego Baguaçus".

**Referência ABNT:** SILVA, L. C. N.; LUCHIARI, A. Estimativa de perda de solos por erosão laminar na bacia hidrográfica do Córrego Baguaçu-SP. **Revista do Departamento de Geografia**, São Paulo, v. 32, p. 15-28, 2016. DOI: https://doi.org/10.11606/rdg.v32i0.114308. Acesso em: 29 out. 2026.

### 6. Silva et al. (2016)

**Nível de leitura:** texto completo (PDF do SciELO, 11 páginas; li resumo, métodos, Tabelas 3 e 4 e discussão).

**Conteúdo.** Perdas de solo e água em parcelas de 2007 a 2012 numa sub-bacia piloto em Eldorado do Sul (RS): dois plantios de eucalipto (EF1, implantado em 2004; EF2, em 2001), floresta nativa (NF) e solo descoberto. Determina R (4.228,52 MJ mm ha-1 h-1 ano-1), K do Argissolo Vermelho (0,0026 Mg ha h ha-1 MJ-1 mm-1) e C. As perdas nos eucaliptos ficaram bem abaixo da tolerância e, a partir do 5º ano, iguais às da mata.

**Valores da nossa tabela:**
- C = 0,121 (Silvicultura/reflorestamento): **confere** com EF1, o plantio mais jovem (Tabela 4, p. 440; resumo, p. 432). O plantio mais velho (EF2) deu 0,016. A escolha do valor do plantio jovem é da IC (conservadora).
- C = 0,015 (Mata Nativa): **confere** com NF (Tabela 4, p. 440).
- C = 0,050 (Campo/pastagem): **não confere.** O artigo não estuda pastagem nem campo, e o número 0,05 não aparece como fator C. A fonte do 0,050 é desconhecida.

**Correção bibliográfica:** a primeira autora é Bárbara Pereira Christofaro Silva: SILVA, B. P. C. (a IC escreve "SILVA, B. C. P.").

**Referência ABNT:** SILVA, B. P. C.; SILVA, M. L. N.; BATISTA, P. V. G.; PONTES, L. M.; ARAÚJO, E. F.; CURI, N. Soil and water losses in eucalyptus plantation and natural forest and determination of the USLE factors at a pilot sub-basin in Rio Grande do Sul, Brazil. **Ciência e Agrotecnologia**, Lavras, v. 40, n. 4, p. 432-442, 2016. DOI: https://doi.org/10.1590/1413-70542016404013216. Acesso em: 29 out. 2026.

### 7. Wischmeier e Smith (1978), AH 537

Já lido no lote B (texto completo acessado, trechos relevantes). C é a razão entre a perda com a cobertura considerada e a perda no pousio limpo contínuo (p. 3 e definições); por isso **solo exposto C = 1,0 é consistente com a definição**. **Corpo hídrico C = 0** não foi visto nas tabelas do AH 537 (o lote B diz que não viu valores para urbano, mineração ou água); é convenção (água não sofre perda de solo). Sugiro citar o AH 537 só para o solo exposto.
Referência (já na lista do TCC): WISCHMEIER, W. H.; SMITH, D. D. **Predicting rainfall erosion losses**: a guide to conservation planning. Washington, DC: USDA, 1978. (Agriculture Handbook, n. 537).

### Classes de uso sem fonte (só listo)

- Área Urbanizada, C = 0 (14,1% dos pixels): adotado (superfície impermeável).
- Mineração, C = 1 (0,0%): adotado como solo exposto.
- Afloramento Rochoso (uso), C = 1 (0,0%): adotado.

---

## Tabelas propostas (coluna "Fonte" só com o que foi verificado)

Os valores são os que o modelo usa hoje (não mudei nenhum). Onde a fonte não conferiu, escrevi "IC" (Vivarelli et al., 2025) e uma nota. Decimais com vírgula; caracteres de teclado.

**Tabela 5. Fator K por classe de solo.**

| Classe de solo | K (t h MJ-1 mm-1) | Pixels de cálculo (%) | Fonte |
|---|---|---|---|
| Cambissolos Háplicos | 0,0475 | 68,6 | Corrêa, Moraes e Pinto (2015), amostra individual (a média da classe no mesmo trabalho é 0,036) |
| Neossolos Litólicos | 0,0463 | 0,0 | Vivarelli et al. (2025), a partir de Rocha Lima et al. (2016), Demarchi e Zimback (2014) e Chagas et al. (2011), que dão de 0,018 a 0,129 |
| Argissolos Vermelho-Amarelos | 0,0351 | 17,6 | Vivarelli et al. (2025), com base em Silva (2016) [não conferido] |
| Afloramento Rochoso | 0,0087 | 0,1 | Vivarelli et al. (2025) [sem fonte primária conferida] |
| Área Urbana | 0,0000 | 13,7 | adotado (área urbana) |

**Tabela 6. Fator C por classe de uso.**

| Classe de uso | C (adimensional) | Pixels de cálculo (%) | Fonte |
|---|---|---|---|
| Solo exposto | 1,000 | 0,5 | Wischmeier e Smith (1978) (por definição) |
| Afloramento Rochoso | 1,000 | 0,0 | adotado |
| Mineração | 1,000 | 0,0 | adotado, como solo exposto |
| Lavoura Temporária | 0,212 | 3,9 | Silva e Luchiari (2016), valor da soja (o mesmo trabalho dá 0,142 para a média de milho e soja) |
| Silvicultura | 0,121 | 12,7 | Silva et al. (2016), eucalipto jovem |
| Campo | 0,050 | 29,0 | Vivarelli et al. (2025) [sem fonte primária conferida] |
| Mata Nativa | 0,015 | 39,6 | Silva et al. (2016), floresta nativa |
| Corpos D'Água | 0,000 | 0,2 | adotado (água) |
| Área Urbanizada | 0,000 | 14,1 | adotado (superfície impermeável) |

**Nota sobre a unidade de K:** as fontes escrevem t h MJ-1 mm-1, t.ha.h.ha-1.MJ-1.mm-1 ou Mg h MJ-1 mm-1 (formas equivalentes da unidade métrica por hectare). A Tabela 5 do Doc usa t*h*MJ-1*mm-1 (`tab_fator_K.md`); mantive.

## Referências a acrescentar à lista do TCC (só as que foram lidas e que sustentam algum valor)

CHAGAS, C. S. et al. **Zoneamento agroecológico do município de Dois Irmãos do Buriti - MS**. Rio de Janeiro: Embrapa Solos, 2011. 63 p. (Boletim de Pesquisa e Desenvolvimento, 181). Disponível em: https://www.infoteca.cnptia.embrapa.br/infoteca/handle/doc/919009. Acesso em: 29 out. 2026.

CORRÊA, E. A.; MORAES, I. C.; PINTO, S. A. F. Estimativa da erodibilidade e tolerância de perdas de solo na região do centro leste paulista. **Geociências**, São Paulo, v. 34, n. 4, p. 848-860, 2015. Disponível em: https://periodicos.rc.biblioteca.unesp.br/index.php/geociencias/article/view/10582. Acesso em: 29 out. 2026.

DEMARCHI, J. C.; ZIMBACK, C. R. L. Mapeamento, erodibilidade e tolerância de perda de solo na sub-bacia do Ribeirão das Perobas. **Energia na Agricultura**, Botucatu, v. 29, n. 2, p. 102-114, 2014. DOI: https://doi.org/10.17224/EnergAgric.2014v29n2p102-114.

ROCHA LIMA, C. G.; CARVALHO, M. P.; SOUZA, A.; COSTA, N. R.; MONTANARI, R. Influência de atributos químicos na erodibilidade e tolerância de perda de solo na bacia hidrográfica do baixo São José dos Dourados. **Geociências**, São Paulo, v. 35, n. 1, p. 63-76, 2016. Disponível em: https://periodicos.rc.biblioteca.unesp.br/index.php/geociencias/article/view/10992. Acesso em: 29 out. 2026.

SILVA, B. P. C.; SILVA, M. L. N.; BATISTA, P. V. G.; PONTES, L. M.; ARAÚJO, E. F.; CURI, N. Soil and water losses in eucalyptus plantation and natural forest and determination of the USLE factors at a pilot sub-basin in Rio Grande do Sul, Brazil. **Ciência e Agrotecnologia**, Lavras, v. 40, n. 4, p. 432-442, 2016. DOI: https://doi.org/10.1590/1413-70542016404013216.

SILVA, L. C. N.; LUCHIARI, A. Estimativa de perda de solos por erosão laminar na bacia hidrográfica do Córrego Baguaçu-SP. **Revista do Departamento de Geografia**, São Paulo, v. 32, p. 15-28, 2016. DOI: https://doi.org/10.11606/rdg.v32i0.114308.

Opcionais / dependem da decisão:
- SILVA, T. S. (2016), dissertação: só depois de abrir e conferir o 0,0351.
- SILVA, A. M.; ALVARES, C. A. (2005): não sustenta nenhum valor da tabela; só entra se o texto citar a faixa de K dos solos paulistas (é a fonte mais adequada para isso).
- MARTINS et al. (2011) e CASTRO et al. (2011): **não** acrescentar (não sustentam os valores).

## Nível de leitura (resumo)

| Fonte | Nível |
|---|---|
| Corrêa, Moraes e Pinto (2015) | texto completo |
| Silva (2016), dissertação | não acessível (LUME fora do ar para a nuvem); só registro por busca |
| Martins et al. (2011) | texto completo |
| Silva e Alvares (2005) | texto completo (Tabela 1 lida como imagem) |
| Chagas et al. (2011) | texto completo (seção do fator K e Tabela 1) |
| Rocha Lima et al. (2016) | texto completo (Tabela 1 e resumo) |
| Demarchi e Zimback (2014) | texto completo (tabela de K e discussão) |
| Castro et al. (2011) | texto completo (Tabela 5 lida como imagem) |
| Silva e Luchiari (2016) | texto completo |
| Silva et al. (2016) | texto completo |
| Wischmeier e Smith (1978) | lote B (texto completo acessado, trechos relevantes) |

Os PDFs ficaram só no scratchpad da sessão (não versionados).
