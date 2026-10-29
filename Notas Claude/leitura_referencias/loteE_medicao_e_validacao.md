# Lote E - Medição de sedimentos, validação e fontes de incerteza

* Data: 30/10/2026
* Quem leu: subagente da sessão na nuvem (Claude Code), a pedido da sessão principal.
* Regra de leitura: só é registrada como utilizável a obra que foi realmente aberta e lida (texto completo, ou ao menos o resumo na página oficial do periódico, editora ou repositório). Nunca inventar números, páginas, DOIs ou conteúdo.

## AVISO IMPORTANTE - nenhuma obra pôde ser aberta nesta sessão

Nesta sessão na nuvem, a rede bloqueou todos os sites de periódicos e repositórios. O WebFetch e o curl falharam (host não resolvido / bloqueado) para: bmcbioinformatics.biomedcentral.com, jcheminf.biomedcentral.com, www.jmlr.org, pmc.ncbi.nlm.nih.gov, www.ncbi.nlm.nih.gov, pubs.usgs.gov, www.scielo.br, arxiv.org, doi.org, api.crossref.org, europepmc.org, api.openalex.org, api.semanticscholar.org, core.ac.uk, web.archive.org, scholar.archive.org, en.wikipedia.org e www.stat.cmu.edu. Só o GitHub respondia.

O que funcionou foi apenas o WebSearch, que devolve títulos, URLs e um resumo gerado pelo buscador a partir de trechos das páginas. Isso NÃO é a leitura do resumo oficial nem do texto completo. Por isso, pela regra central, TODAS as obras abaixo estão classificadas como "não acessível - não usar no texto" até que alguém abra a página oficial ou o PDF e confira.

O que este arquivo oferece, então, é:
* a identificação de cada obra (autores, título, periódico, volume, páginas e DOI conforme aparecem nos resultados de busca - conferir antes de usar);
* o que os trechos de busca indicam sobre o conteúdo (marcado como "segundo trechos de busca", não verificado);
* onde a obra serviria no TCC e uma frase-modelo PROVISÓRIA, para ser usada só depois de conferir na fonte.

Para concluir a leitura, é preciso liberar nas configurações de rede da sessão pelo menos: pmc.ncbi.nlm.nih.gov, bmcbioinformatics.biomedcentral.com, jcheminf.biomedcentral.com, www.jmlr.org (ou jmlr.csail.mit.edu), pubs.usgs.gov e water.usgs.gov, ou o usuário pode baixar os PDFs (todos os abertos listados abaixo) e colocá-los na pasta do TCC.

---

## Tema 1 - Validação cruzada aninhada e viés de otimismo

### Bias in error estimation when using cross-validation for model selection

* Referência ABNT (conferir): VARMA, S.; SIMON, R. Bias in error estimation when using cross-validation for model selection. **BMC Bioinformatics**, v. 7, art. 91, 2006. DOI: 10.1186/1471-2105-7-91.
* Nível de leitura: não acessível - não usar no texto (só trechos do buscador; a obra é de acesso aberto, mas o site da BMC e o PMC estavam bloqueados).
* Onde foi lido: nada foi aberto. Endereços para conferir: https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-7-91 e https://pmc.ncbi.nlm.nih.gov/articles/PMC1397873/
* O que diz (segundo trechos de busca, NÃO verificado): os autores testaram se o erro de validação cruzada de um classificador cujos parâmetros foram escolhidos minimizando esse mesmo erro é uma estimativa válida do erro em dados independentes. Usaram conjuntos de dados simulados sem diferença real entre classes ("dados nulos") e concluíram que esse erro é uma estimativa substancialmente enviesada (otimista) do erro verdadeiro. Propuseram a validação cruzada aninhada (laço interno escolhe parâmetros, laço externo estima o erro). O buscador citou um número (erro abaixo de 30 % em 18,5 % dos conjuntos nulos para Shrunken Centroids), mas ele NÃO deve ser usado sem conferir no texto.
* Onde usar no TCC: 2.8 Avaliação e validação; 3.4.6 Validação cruzada; 4.6 Fontes de incerteza.
* Frase-modelo PROVISÓRIA (usar só após conferir): "Quando o mesmo conjunto de dados é usado para escolher parâmetros e para avaliar o desempenho, a estimativa de erro tende a ser otimista, e a validação cruzada aninhada é a forma recomendada de separar as duas etapas (VARMA; SIMON, 2006)."

### On over-fitting in model selection and subsequent selection bias in performance evaluation

* Referência ABNT (conferir): CAWLEY, G. C.; TALBOT, N. L. C. On over-fitting in model selection and subsequent selection bias in performance evaluation. **Journal of Machine Learning Research**, v. 11, p. 2079-2107, 2010.
* Nível de leitura: não acessível - não usar no texto (só trechos do buscador; acesso aberto, mas jmlr.org bloqueado).
* Onde foi lido: nada foi aberto. Endereços para conferir: https://www.jmlr.org/papers/v11/cawley10a.html e https://jmlr.csail.mit.edu/papers/volume11/cawley10a/cawley10a.pdf
* O que diz (segundo trechos de busca, NÃO verificado): a variância do critério de seleção de modelo importa tanto quanto o viés, porque pode causar sobreajuste na própria seleção de modelo. Esse sobreajuste pode ser grande a ponto de rivalizar com as diferenças de desempenho entre algoritmos, e alguns protocolos de avaliação comuns ficam sujeitos a viés de seleção. Recomenda tratar a seleção de modelo como parte do ajuste e repeti-la a cada nova amostra de dados.
* Onde usar no TCC: 2.8 Avaliação e validação; 3.4.6 Validação cruzada; 4.6 Fontes de incerteza.
* Frase-modelo PROVISÓRIA: "A escolha de parâmetros feita sobre uma amostra finita também é uma etapa de ajuste e pode sobreajustar, de modo que ela deve ser repetida dentro de cada partição da validação cruzada para que o desempenho não seja superestimado (CAWLEY; TALBOT, 2010)."

### Cross-validation pitfalls when selecting and assessing regression and classification models

* Referência ABNT (conferir): KRSTAJIC, D.; BUTUROVIC, L. J.; LEAHY, D. E.; THOMAS, S. Cross-validation pitfalls when selecting and assessing regression and classification models. **Journal of Cheminformatics**, v. 6, art. 10, 2014. DOI: 10.1186/1758-2946-6-10.
* Nível de leitura: não acessível - não usar no texto (só trechos do buscador; acesso aberto, mas BMC e PMC bloqueados).
* Onde foi lido: nada foi aberto. Endereços para conferir: https://jcheminf.biomedcentral.com/articles/10.1186/1758-2946-6-10 e https://pmc.ncbi.nlm.nih.gov/articles/PMC3994246/
* O que diz (segundo trechos de busca, NÃO verificado): trata da escolha e da avaliação de modelos de regressão e classificação por validação cruzada; propõe validação cruzada repetida com busca em grade para ajustar parâmetros e validação cruzada aninhada repetida para avaliar o modelo, distinguindo explicitamente seleção de avaliação.
* Onde usar no TCC: 2.8 Avaliação e validação; 3.4.6 Validação cruzada.
* Frase-modelo PROVISÓRIA: "A seleção do modelo e a avaliação do seu desempenho são etapas distintas e, quando ambas usam validação cruzada, a avaliação deve ser feita num laço externo que não participou da seleção (KRSTAJIC et al., 2014)."

### Stone (1974) e Klemeš (1986)

* Não foram buscados nem abertos nesta sessão (por falta de acesso à rede). Não usar no texto a partir deste relatório.

---

## Tema 2 - Turbidez como substituto da CSS e alta resolução temporal

### Guidelines and procedures for computing time-series suspended-sediment concentrations and loads from in-stream turbidity-sensor and streamflow data

* Referência ABNT (conferir): RASMUSSEN, P. P.; GRAY, J. R.; GLYSSON, G. D.; ZIEGLER, A. C. **Guidelines and procedures for computing time-series suspended-sediment concentrations and loads from in-stream turbidity-sensor and streamflow data**. Reston: U.S. Geological Survey, 2009. (Techniques and Methods, book 3, chap. C4). DOI: 10.3133/tm3C4.
* Nível de leitura: não acessível - não usar no texto (só trechos do buscador; documento aberto, mas pubs.usgs.gov bloqueado).
* Onde foi lido: nada foi aberto. Endereço para conferir: https://pubs.usgs.gov/tm/tm3c4/
* O que diz (segundo trechos de busca, NÃO verificado): o primeiro passo é uma regressão linear simples (mínimos quadrados) da CSS em função da turbidez instantânea; se o erro-padrão percentual do modelo (MSPE) atender a um critério mínimo, esse modelo é usado para gerar a série de CSS, caso contrário entra a vazão como variável adicional. Os modelos são específicos do local e "nunca devem ser considerados estáticos". O método é voltado a sensores nefelométricos. O número de páginas aparece de forma diferente em fontes distintas (52 ou 54), outro motivo para conferir.
* Onde usar no TCC: 2.5 Medição de sedimentos; 3.x Carga medida; 4.6 Fontes de incerteza (curva turbidez-CSS e extrapolação).
* Frase-modelo PROVISÓRIA: "A estimativa contínua da concentração de sedimentos em suspensão a partir da turbidez se baseia numa regressão específica do local, que deve ser revista periodicamente (RASMUSSEN et al., 2009)."

### Technological advances in suspended-sediment surrogate monitoring

* Referência ABNT (conferir): GRAY, J. R.; GARTNER, J. W. Technological advances in suspended-sediment surrogate monitoring. **Water Resources Research**, v. 45, W00D29, 2009. DOI: 10.1029/2008WR007063.
* Nível de leitura: não acessível - não usar no texto (só trechos do buscador; há PDF aberto no USGS, mas o host estava bloqueado).
* Onde foi lido: nada foi aberto. Endereços para conferir: https://pubs.usgs.gov/publication/70038123 e https://water.usgs.gov/osw/techniques/2008WR007063.pdf
* O que diz (segundo trechos de busca, NÃO verificado): compara tecnologias substitutas para monitoramento contínuo de sedimentos (turbidímetros, perfiladores acústicos, laser, diferença de pressão). Os turbidímetros são os mais usados e fornecem dados confiáveis onde a medição pontual pode ser relacionada de forma confiável à concentração média na seção.
* Onde usar no TCC: 2.5 Medição de sedimentos; 4.6 Fontes de incerteza (medição pontual versus média da seção).
* Frase-modelo PROVISÓRIA: "A turbidez é o substituto mais difundido da concentração de sedimentos, desde que a leitura pontual do sensor represente bem a concentração média na seção (GRAY; GARTNER, 2009)."

### Estimating suspended sediment concentrations from turbidity measurements and the calibration problem

* Referência ABNT (conferir): MINELLA, J. P. G.; MERTEN, G. H.; REICHERT, J. M.; CLARKE, R. T. Estimating suspended sediment concentrations from turbidity measurements and the calibration problem. **Hydrological Processes**, v. 22, n. 12, p. 1819-1830, 2008. DOI: 10.1002/hyp.6763.
* Nível de leitura: não acessível - não usar no texto (só trechos do buscador; artigo pago, página da Wiley não testada por falta de rede).
* Onde foi lido: nada foi aberto. Endereço para conferir: https://doi.org/10.1002/hyp.6763
* O que diz (segundo trechos de busca, NÃO verificado): estudo numa pequena bacia rural no sul do Brasil, comparando duas formas de calibrar o turbidímetro: com amostras coletadas junto à sonda durante cheias e com amostras preparadas a partir de solos da bacia. A calibração com amostras de cheia acompanhou bem as concentrações medidas, e a feita com solos introduziu erros apreciáveis.
* Onde usar no TCC: 2.5 Medição de sedimentos; 4.6 Fontes de incerteza (origem das amostras da curva de calibração).
* Frase-modelo PROVISÓRIA: "A curva turbidez-CSS é mais confiável quando calibrada com amostras coletadas durante os próprios eventos de cheia do que com suspensões preparadas a partir de solo (MINELLA et al., 2008)."

### Sediment concentration versus water discharge during single hydrologic events in rivers

* Referência ABNT (conferir): WILLIAMS, G. P. Sediment concentration versus water discharge during single hydrologic events in rivers. **Journal of Hydrology**, v. 111, n. 1-4, p. 89-106, 1989. DOI: 10.1016/0022-1694(89)90254-0.
* Nível de leitura: não acessível - não usar no texto (só trechos do buscador; há registro no pubs.usgs.gov, bloqueado).
* Onde foi lido: nada foi aberto. Endereço para conferir: https://pubs.usgs.gov/publication/70015117
* O que diz (segundo trechos de busca, NÃO verificado): classifica as relações CSS-vazão dentro de um evento em cinco tipos comuns: unívoca (reta ou curva), laço horário, laço anti-horário, unívoca mais laço e em forma de oito. O tipo de relação estaria ligado à moda e à assimetria das curvas temporais de CSS e vazão.
* Onde usar no TCC: 2.5 Medição de sedimentos; 4.x Discussão dos eventos (histerese); 5 Trabalhos futuros.
* Frase-modelo PROVISÓRIA: "Dentro de um mesmo evento, a relação entre concentração de sedimentos e vazão costuma apresentar histerese, em laço horário, anti-horário ou em forma de oito (WILLIAMS, 1989)."

### Gippel (1995) e Lewis (1996)

* Não foram buscados nem abertos nesta sessão. Não usar no texto a partir deste relatório.

---

## Tema 3 - Delimitação de eventos e separação da vazão de base

### A comparison of baseflow indices, which were calculated with seven different baseflow separation methods

* Referência ABNT (conferir): ECKHARDT, K. A comparison of baseflow indices, which were calculated with seven different baseflow separation methods. **Journal of Hydrology**, v. 352, n. 1-2, p. 168-173, 2008. DOI: 10.1016/j.jhydrol.2008.01.005.
* Nível de leitura: não acessível - não usar no texto (só trechos do buscador; artigo pago).
* Onde foi lido: nada foi aberto. Endereço para conferir: https://doi.org/10.1016/j.jhydrol.2008.01.005
* O que diz (segundo trechos de busca, NÃO verificado): compara índices de vazão de base de 65 bacias norte-americanas calculados por sete métodos (HYSEP 1, 2 e 3, PART, BFLOW, UKIH e o filtro de Eckhardt). Como o valor verdadeiro é desconhecido, não se pode dizer qual método é o mais exato, mas os resultados do filtro de Eckhardt parecem hidrologicamente mais plausíveis, e o filtro pode ser aplicado a hidrogramas de qualquer passo de tempo. Apresenta uma técnica simples para estimar a constante de recessão.
* Onde usar no TCC: 2.x Separação da vazão de base; 3.x Escoamento direto; 4.6 Fontes de incerteza.
* Frase-modelo PROVISÓRIA: "Como o valor verdadeiro da vazão de base é desconhecido, nenhum método de separação pode ser considerado o mais exato, o que torna a separação uma fonte de incerteza do escoamento direto observado (ECKHARDT, 2008)."

### A hydrograph separation method based on information from rainfall and runoff records

* Referência ABNT (incompleta - conferir periódico, volume, páginas e DOI): MEI, Y.; ANAGNOSTOU, E. N. A hydrograph separation method based on information from rainfall and runoff records. **Journal of Hydrology**, 2015.
* Nível de leitura: não acessível - não usar no texto (o buscador não trouxe nem a página do periódico).
* Onde foi lido: nada foi aberto. Fonte secundária vista no buscador: https://ucwater.engr.uconn.edu/models-data
* O que diz (segundo trechos de busca, NÃO verificado): o método tem duas partes, a separação da vazão de base (método FRCK, que combina a constante k revisada com um filtro digital recursivo) e a identificação automática de eventos (método do ponto característico, CPM) a partir de séries longas de chuva média e vazão.
* Onde usar no TCC: 4.6 Fontes de incerteza (delimitação dos eventos); 5 Trabalhos futuros (automatizar a seleção de eventos).
* Frase-modelo PROVISÓRIA: "A identificação dos eventos chuva-vazão pode ser automatizada a partir das séries de chuva e vazão (MEI; ANAGNOSTOU, 2015)."

### Tang e Carey (2017)

* Não buscado nem aberto nesta sessão. Não usar no texto a partir deste relatório.

---

## Tema 4 - Densidade de postos e interpolação da chuva

### Impact of small-scale spatial rainfall variability on runoff modeling

* Referência ABNT (conferir): FAURÈS, J.-M.; GOODRICH, D. C.; WOOLHISER, D. A.; SOROOSHIAN, S. Impact of small-scale spatial rainfall variability on runoff modeling. **Journal of Hydrology**, v. 173, n. 1-4, p. 309-326, 1995. DOI: 10.1016/0022-1694(95)02704-S.
* Nível de leitura: não acessível - não usar no texto (só trechos do buscador; artigo pago).
* Onde foi lido: nada foi aberto. Endereço para conferir: https://doi.org/10.1016/0022-1694(95)02704-S
* O que diz (segundo trechos de busca, NÃO verificado): estuda o efeito da variabilidade espacial da chuva em pequena escala sobre a modelagem do escoamento numa bacia experimental muito pequena, usando o modelo distribuído de eventos KINEROS. Atenção: a escala da bacia estudada é muito menor que a do alto Jundiaí, o que limita a transferência das conclusões; conferir na fonte.
* Onde usar no TCC: 4.6 Fontes de incerteza (dois postos e IDW).
* Frase-modelo PROVISÓRIA: "Mesmo em bacias pequenas, a variabilidade espacial da chuva afeta de forma importante o escoamento simulado em eventos (FAURÈS et al., 1995)."

### Arnaud et al. (2002) e Zhang e Han (2017)

* Não buscados nem abertos nesta sessão. Não usar no texto a partir deste relatório.

---

## Tema 5 - Erosão e produção de sedimentos em áreas urbanas

### A cycle of sedimentation and erosion in urban river channels

* Referência ABNT (conferir; há dois DOIs diferentes nos índices): WOLMAN, M. G. A cycle of sedimentation and erosion in urban river channels. **Geografiska Annaler: Series A, Physical Geography**, v. 49, n. 2-4, p. 385-395, 1967. DOI: 10.1080/04353676.1967.11879766 (outro índice traz 10.2307/520904).
* Nível de leitura: não acessível - não usar no texto (só trechos do buscador; artigo pago).
* Onde foi lido: nada foi aberto. Endereço para conferir: https://doi.org/10.1080/04353676.1967.11879766
* O que diz (segundo trechos de busca, NÃO verificado): com base em dados do Piedmont de Maryland (EUA), descreve um ciclo ligado à urbanização: estágio estável antes da ocupação (ou agrícola), fase de construção com solo exposto e produção de sedimentos muito alta, e paisagem urbana final, com menos sedimento mas mais escoamento e erosão das margens. O buscador citou ordens de grandeza de produção de sedimentos em obras, que NÃO devem ser usadas sem conferir.
* Onde usar no TCC: 2.x Erosão em áreas urbanas; 4.x Discussão (áreas em urbanização na bacia); 5 Trabalhos futuros.
* Frase-modelo PROVISÓRIA: "A fase de construção, com solo exposto, é a de maior produção de sedimentos no ciclo da urbanização de uma bacia (WOLMAN, 1967)."

### Russell et al. (2017) e Ziegler et al. (2001)

* Não buscados nem abertos nesta sessão. Não usar no texto a partir deste relatório.

---

## Tabela resumo

| Obra | Nível | Usar? | Onde |
|---|---|---|---|
| Varma e Simon (2006) | não acessível (só trechos de busca) | Não, até conferir (aberto) | 2.8; 3.4.6; 4.6 |
| Cawley e Talbot (2010) | não acessível (só trechos de busca) | Não, até conferir (aberto) | 2.8; 3.4.6; 4.6 |
| Krstajic et al. (2014) | não acessível (só trechos de busca) | Não, até conferir (aberto) | 2.8; 3.4.6 |
| Rasmussen et al. (2009) | não acessível (só trechos de busca) | Não, até conferir (aberto) | 2.5; 4.6 |
| Gray e Gartner (2009) | não acessível (só trechos de busca) | Não, até conferir (PDF aberto no USGS) | 2.5; 4.6 |
| Minella et al. (2008) | não acessível (só trechos de busca) | Não, até conferir | 2.5; 4.6 |
| Williams (1989) | não acessível (só trechos de busca) | Não, até conferir | 2.5; 4.x; 5 |
| Eckhardt (2008) | não acessível (só trechos de busca) | Não, até conferir | 2.x; 4.6 |
| Mei e Anagnostou (2015) | não acessível (referência incompleta) | Não | 4.6; 5 |
| Faurès et al. (1995) | não acessível (só trechos de busca) | Não, até conferir | 4.6 |
| Wolman (1967) | não acessível (só trechos de busca; DOI divergente) | Não, até conferir | 2.x; 4.x; 5 |

## Não acessíveis / não usar

* Todas as obras deste lote, pois nenhuma página oficial nem PDF pôde ser aberto nesta sessão (rede bloqueada para os sites de periódicos e repositórios).
* Não buscadas: Stone (1974), Klemeš (1986), Gippel (1995), Lewis (1996), Tang e Carey (2017), Arnaud et al. (2002), Zhang e Han (2017), Russell et al. (2017), Ziegler et al. (2001).
* Prioridade para conferir quando houver acesso (todas abertas): Varma e Simon (2006), Cawley e Talbot (2010), Krstajic et al. (2014), Rasmussen et al. (2009) e Gray e Gartner (2009).

---

## Conferência da sessão principal (30/10/2026)

- Conferi o bloqueio com `curl` (código 000 em pubs.usgs.gov, bmcbioinformatics.biomedcentral.com, www.jmlr.org, pmc.ncbi.nlm.nih.gov e api.crossref.org; só o GitHub respondeu) e com WebFetch (www.jmlr.org: "host fora dos domínios permitidos"). O bloqueio é da configuração de rede do ambiente da nuvem, não das obras.
- Consequência: **nenhuma obra deste lote foi citada** nas propostas de 30/10. Os lugares onde caberiam estão marcados `[REFERÊNCIA A LER: ...]` em `proposta_cap2_30-10.md` (2.5, 2.7, 2.8) e `proposta_cap3_30-10.md` (3.4.6), e listados em `proposta_cap4_30-10.md` (notas da 4.6).
- Prioridade de leitura (todas de acesso aberto, segundo os resultados de busca): (1) Varma e Simon (2006), para a validação aninhada pedida pelo Luis (C19); (2) Rasmussen et al. (2009), USGS TM 3-C4, para a turbidez como substituto da CSS (C10); (3) Gray e Gartner (2009); (4) Cawley e Talbot (2010). Depois de ler, completar neste arquivo o "Nível de leitura" e o "O que diz", e trocar os marcadores pelas chamadas.
- Para a referência de erosão urbana e de densidade de postos, nada foi lido; as frases correspondentes nas propostas não têm citação.
