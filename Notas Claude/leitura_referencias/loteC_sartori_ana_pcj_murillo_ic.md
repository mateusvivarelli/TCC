# Lote C: leitura das referências (Sartori, ANA, Consórcio PCJ, Murillo-Bermúdez 2022 e 2023, IC/Vivarelli)

Data: 28/10/2026. Nada foi alterado em C:\TCC. Onde digo "(meu cálculo)", é conta que fiz agora; onde digo "(notas do projeto)", é o que já estava escrito em `Notas Claude/` e eu não refiz.

## Resumo rápido: o que mais importa

1. **Curva turbidez-CSS (ref. 5 e 4):** a equação CSS = 3,264·Turb^0,7974 está escrita no trabalho de **2022** (ref. 4), que eu li inteiro. O resumo do artigo de **2023** (ref. 5) diz que o melhor modelo foi uma **regressão linear por partes, com quebra em 250 NTU**, e não uma lei de potência. O TCC atribui a curva ao artigo de 2023. Não consegui ler o texto do artigo de 2023 (acesso pago), então não sei se a lei de potência aparece lá. Vale perguntar ao orientador, que é o primeiro autor dos dois.
2. **Lista dos 17 eventos (ref. 4):** a tabela do trabalho de 2022 e o gráfico da IC trazem o evento de **24/11/2018** (Qmax 12,48 m³/s). A Tabela 2 do TCC não o tem e traz no lugar o de **17/12/2018** (Qpico 16,6). Os outros 16 eventos batem. Essa troca pode explicar parte da diferença entre os erros publicados da IC e os que o TCC reproduz.
3. **Quarto autor (ref. 5):** é **J. G. Dalfré Filho** (José Gilberto Dalfré Filho). Na IC, "FILHO, J. G. D." está abreviado de forma errada. Forma correta: DALFRÉ FILHO, J. G.
4. **CN da ANA (ref. 2):** o raster BR_CN-2022 é **CN para a condição média (CN2, AMC II)**. A nota técnica da ANA diz que o CN2 vem da tabela de Tucci (2001) adaptada. Os valores de CN seco e úmido **não vêm do raster**: a ANA só traz CN1 e CN3 do dado global GCN250 (e só na base vetorial). O texto do TCC (seção 3.3 e Tabela 4: "em 3 condições... da base nacional da ANA") dá a entender que a ANA fornece as três condições. Convém reescrever.
5. **Grupo hidrológico (ref. 1 e 2):** o TCC cita Sartori para os grupos, o que está certo. Mas Sartori (2005) não traz tabela de CN; o CN por uso × grupo vem de Tucci (2001) adaptado pela ANA. E a ANA simplificou Sartori: todo Cambissolo Háplico/Húmico virou grupo C, e Argissolo virou só B ou C.
6. **IC (ref. 6):** o "16,3% de erro mediano" não é número da IC. É da IC **refeita pelo TCC** (α e β recalibrados em log, validação cruzada). A IC publicou só o erro médio (−4,15%) e a faixa (−60,01% a +37,14%).

---

## 1. SARTORI, LOMBARDI NETO e GENOVEZ (2005), RBRH 10(4):5-18

**Nível de leitura: texto completo** (PDF da ABRH, 14 páginas, extraído e lido; li as tabelas 1, 4 e a conclusão com cuidado; a Tabela 5 e as descrições por ordem de solo só por busca de trechos).

**O que é.** Artigo de classificação, tirado da dissertação de mestrado do primeiro autor (Unicamp, orientador Genovez). Mostra os quatro grupos do SCS (A a D), explica por que a regra americana (baseada quase só na textura) funciona mal para solos brasileiros e propõe uma extensão da classificação de Lombardi Neto et al. (1989) para os nomes atuais do Sistema Brasileiro de Classificação de Solos. Mostra, com dados de dois outros estudos (Bertolani e Vieira, 2001; Pott, 2001), que as taxas de infiltração medidas em solos brasileiros são bem maiores que os mínimos do SCS, e por isso esses mínimos não servem para classificar solos do Brasil. A base são perfis do Estado de São Paulo; a conclusão diz que pode ser usada no país onde há solos parecidos, com cuidado em regiões muito úmidas ou secas (Nordeste, Pantanal, Amazônia).

**Critérios dos grupos (Tabela 4 do artigo, "Sartori, 2004").**
- **A:** solos muito profundos (>200 cm) ou profundos (100 a 200 cm); alta infiltração; gradiente textural baixo (<1,20); bem ou excessivamente drenados; argila de baixa atividade (Tb). Entram: Latossolos Amarelo, Vermelho-Amarelo e Vermelho argilosos com alta macroporosidade, e os de textura média com horizonte superficial não arenoso.
- **B:** profundos (100 a 200 cm); infiltração moderada; gradiente textural de 1,20 a 1,50. Entram: Latossolo de textura média com superfície arenosa, Latossolo Bruno, Nitossolo Vermelho, Neossolo Quartzarênico, e **Argissolo Vermelho ou Vermelho-Amarelo sem mudança textural abrupta**.
- **C:** profundos ou pouco profundos (50 a 100 cm); infiltração baixa; gradiente textural >1,50, com mudança textural abrupta comum. Entram: **Argissolo profundo com mudança textural abrupta**, Argissolo pouco profundo sem mudança abrupta, **Cambissolo de textura média e Cambissolo Háplico ou Húmico "latossólico"**, Espodossolo Ferrocárbico, Neossolo Flúvico.
- **D:** infiltração muito baixa; solos rasos (<50 cm), ou pouco profundos com mudança textural abrupta, ou argilosos de argila de alta atividade (Ta), ou orgânicos. Entram: **Neossolo Litólico**, Organossolo, Gleissolo, Chernossolo, Planossolo, Vertissolo, Alissolo, Luvissolo, Plintossolo, afloramento de rocha, **"demais Cambissolos" (os que não entram no C)**, Argissolo Vermelho-Amarelo ou Amarelo pouco profundo com mudança abrupta.
- Os critérios que o artigo usa são: profundidade, textura, razão textural entre horizontes B e A, permeabilidade (porosidade e atividade da argila) e resistência à erosão (índice K).
- Os mínimos de infiltração do SCS (A >7,62; B 3,81 a 7,62; C 1,27 a 3,81; D <1,27 mm/h) aparecem só como a regra original; o artigo diz que não valem para o Brasil.

**O que usamos no TCC.**
- Seção 3.3 (rascunho 04): "classificando os solos em grupos hidrológicos conforme Sartori, Lombardi Neto e Genovez (2005)". Isso é verdade, mas quem aplicou foi a ANA (ver ref. 2). Sartori entra só como fonte indireta do grupo hidrológico do solo embutido no CN.
- Passo 2 do modelo (CN): o CN já traz o grupo; o TCC não refaz a classificação.

**Atenção.**
- Sartori (2005) **não dá valores de CN**. A frase da seção 2.3 ("o CN depende do grupo hidrológico do solo...") fica sustentada por USDA-SCS/Chow, não por Sartori.
- O Cambissolo Háplico é 68,6% dos solos da área. Pelo Sartori, ele é C só se for de textura média ou "latossólico"; os demais são D. A ANA pôs todo Cambissolo Háplico/Húmico em C (ver ref. 2). Então o grupo C dos Cambissolos da bacia é uma simplificação da ANA, não uma decisão de Sartori. Se o Cambissolo local fosse D, o CN subiria.
- O artigo descreve o Cambissolo como de "alta erodibilidade associada ao grande potencial de escoamento", o que concorda com o uso do grupo C ou D.
- Os dados são de São Paulo, o que ajuda: a bacia é paulista.
- Crossref lista os autores em outra ordem (Genovez, Neto, Sartori); o PDF traz Sartori, Lombardi Neto, Genovez. A referência do TCC está certa. O DOI 10.21168/rbrh.v10n4.p5-18 funciona (abre a página da ABRH).

---

## 2. ANA (2024), Curva Número na Base Ottocodificada (1985, 2014 e 2022), raster BR_CN-2022

**Nível de leitura: texto completo da ficha de metadados, da planilha de referência (CN_2022_Referencias.xlsx, todas as abas) e da Nota Técnica nº 9/2025 COMUC/SHE (36 páginas, extraída; li métodos, resultados e limitações). Também li a Nota Técnica 46/2018 (versão 2014).** Não consegui abrir as figuras das notas.

**O que é.** Base nacional de número de curva, de domínio livre. O raster de 2022 tem 30 m. Foi feito cruzando (a) o mapa de uso e cobertura do **MapBiomas** (ficha: "versão 2023", ano 2022, 30 m) com (b) o mapa de solos do **IBGE (versão 2023, escala 1:250.000)**, transformado em grupos hidrológicos A a D pela classificação de **Sartori et al. (2005)** (arquivo SoilHidro-2023). Cada combinação uso × grupo recebe um CN **CN2** de uma tabela adaptada de **Tucci (2001)** (por exemplo: formação florestal A 26, B 52, C 65, D 69; pastagem 47, 67, 81, 88; área urbanizada 67, 78, 85, 89; água e afloramento 98). Os dados foram feitos em QGIS; a célula tem 0,00027 grau (≈30 m), embora o solo original seja 1:250.000. A ficha cita a Nota Técnica 9/2025 e o responsável é Filipe S. C. Pinhati (ANA).

**Condição de umidade (AMC).** A ficha de metadados não diz. A nota técnica 9/2025 chama os valores de "CN2" ("CN2ANA", "CN2-2022") e descreve CN1/CN3 só como correção possível (limites de chuva de 5 dias: seco <36 mm na estação de crescimento e <13 mm fora dela; úmido >53 e >28 mm). Os CN1 e CN3 que a ANA traz vêm do **dado global GCN250** e só aparecem na base vetorial (BHAE_CN-2022), não no raster. A planilha tem uma aba "CN1,2,3" com a correção da literatura (CN2 70 vira CN1 51 e CN3 85, por exemplo). Pela ficha, o raster é CN2 (AMC II); isso é o que o TCC escreve.

**Resolução e escala.** Raster de 30 m; solo 1:250.000. Isso significa que o grupo hidrológico vem de um mapa muito mais grosseiro que o uso.

**O que usamos no TCC.**
- Dado de entrada do CN (seção 3.3 e Tabela 4; passo 2 do modelo): raster BR_CN-2022 recortado e reprojetado para SIRGAS 2000 / UTM 23S. A conferência das notas do projeto (§25.5) mostra 90,7% de pixels idênticos ao raster da ANA e 100% nas áreas homogêneas.
- CN-II vira CN-I pela fórmula de Chow, Maidment e Mays (1988).
- Os 20 valores de CN do recorte (52, 55, 64, 65, 67, 69, 70, 72, 73, 74, 77, 78, 81, 82, 84, 85, 87, 88, 89, 98; conferi no raster `CN TCC.tif`) **estão todos na tabela da ANA** (meu cálculo). Isso mostra que são valores de tabela, e não médias por área como a seção 25.3 das notas sugeria.
- A nota técnica diz que, para validar o CN com vazão medida, é preciso separar a vazão de base (limitação IV), e que a abstração inicial fixa em 0,2·S é uma suposição vinda de bacias agrícolas dos EUA e deve ser adaptada se outra relação for usada (limitação II). Isso apoia duas decisões do TCC (usar só escoamento direto; discutir λ). A nota também recomenda calibrar e validar o CN localmente.

**Atenção.**
- **Condições seca e úmida.** O TCC escreve que o CN veio da ANA "em três condições de umidade antecedente". A ANA entrega CN2 no raster. O CN-I do TCC é conversão do TCC (Chow), não dado da ANA. Os arquivos "CN TCC - Seco.tif" e "- Úmido.tif" da pasta Dados Iniciais devem ter sido gerados no projeto; as notas confirmam que batem com Chow, mas não registram quem os gerou.
- **Chow versus tabela da ANA/de Mello.** Pela aba "CN1,2,3", CN2 = 70 dá CN1 = 51; pela fórmula de Chow dá 49,5. Para CN2 de 50 a 75, a tabela da planilha fica cerca de 1 a 1,5 ponto acima de Chow (meu cálculo). A diferença é pequena, mas a escolha da fórmula deveria ser dita como escolha do TCC.
- **Ficha de metadados confusa.** A data de publicação aparece como 2018 e 2024 em campos diferentes; o raster foi gerado em 2025 segundo a ficha. Para a referência, vale citar também a Nota Técnica nº 9/2025 e dar o ano certo. O acesso do TCC é "17 out. 2026"; a ficha foi atualizada por último em 25/11/2025.
- **Argissolos só B ou C.** A nota diz que o mapa IBGE não traz Argissolos pouco profundos com mudança abrupta (que seriam D), então todo Argissolo ficou B ou C. A aba "Solos_Prova" mostra "Classe 1 / Classe 2" para Argissolo Vermelho-Amarelo (B ou C). Cambissolo Háplico e Húmico = C nas duas colunas; Neossolo Litólico, Gleissolo e Afloramento = D; "Área urbana" do IBGE = D.
- **Uso x solo em mapas diferentes.** O cruzamento no raster não bate com o mapa de uso do Plano de Bacias (o CN usa MapBiomas, K e C usam o Plano). O TCC já declara isso. Na região, a ANA calcula "Mata Nativa" × Cambissolo em maioria com CN 65, que é floresta no grupo C (conferi no raster, meu cálculo): 62% dos pixels.
- A nota técnica afirma que a classificação "foi realizada com sucesso", mas **não traz validação** do CN com vazão medida; diz que a validação é o próximo passo. O TCC pode usar isso como justificativa para comparar o CN com o escoamento medido.
- A frase da ficha "uso do solo na escala 1:60.000" não bate com a nota (MapBiomas 1:50.000). Não afeta o TCC.

---

## 3. CONSÓRCIO PROFILL-RHAMA (2020), Plano de Recursos Hídricos das Bacias PCJ 2020 a 2035, Relatório Final

**Nível de leitura: não consegui acessar o documento.** O arquivo completo (RELAT_FINAL_E_ANEXOS.pdf, 1.342 páginas, cerca de 183 MB) está no site da Agência das Bacias PCJ e como link do Google Drive no site dos Comitês, mas as ferramentas não leem arquivo desse tamanho (o Relatório Síntese também passou do limite de 10 MB). Confirmei só por fora: o plano existe, foi feito pelo Consórcio Profill-Rhama (Profill Engenharia e Ambiente + Rhama), foi aprovado pela Deliberação dos Comitês PCJ nº 332/2020 (set. 2020), e o endereço do relatório está em https://agencia.baciaspcj.org.br/wp-content/uploads/RELAT_FINAL_E_ANEXOS.pdf. Uma busca na web trouxe a frase da faixa de chuva de **1.195 a 1.609 mm** como texto do site do Plano, o que confirma esse número (a página exata eu não vi). **Todo o resto vem do arquivo `Notas Claude/dados_area_estudo_plano_bacias.md`, que registra uma leitura do PDF em 16/10/2026 com páginas. Eu não reverifiquei esses números.**

**O que é.** Plano de bacias (diagnóstico, prognóstico e plano de ações) das bacias Piracicaba, Capivari e Jundiaí. Traz mapas e quadros de clima, geologia, solos, uso, população e recursos hídricos por sub-bacia.

**Afirmações do TCC (seção 3.1 e 3.3) e o que sustenta cada uma.**
| Afirmação no TCC | Fonte dentro do Plano segundo as notas | Situação |
|---|---|---|
| Chuva anual nos municípios PCJ de 1.195 a 1.609 mm; chuvas de outubro a março | p. 117 do PDF; fonte primária CEPAGRI (2017), normais 1961 a 1990 | Faixa confirmada por mim em texto do site do Plano |
| Clima "Cfa/Cfb" para o alto Jundiaí | Plano dá Köppen só para as bacias PCJ inteiras (Cfa 41%, Cfb 36%, Cwa 19%, Cwb 4%; Figura 3.6, p. 119) | **Não sustentado diretamente**: o Plano não atribui classe ao alto Jundiaí. As notas já marcam isso como pendente |
| "alto curso na porção mais chuvosa da sub-bacia" | Plano diz que as menores chuvas ficam no centro-sul, nos municípios a jusante de Capivari e Jundiaí | **Inferência do TCC**, não frase do Plano |
| Geologia da sub-bacia Jundiaí: cristalino 86,1%, cenozoico 9,9%, Grupo Tubarão 4,1%; aquífero fraturado | Quadro 3.2, p. 103 (86,06 / 9,90 / 4,08) | Confere com as notas |
| Campo Limpo Paulista 73.664 hab., 100% nas Bacias PCJ; sub-bacia Jundiaí com 16,55% da população PCJ | Quadro 2.3, ≈ p. 55 | Confere com as notas; o ano-base do número não está nas notas |
| Mapas de solo e uso do Plano usados para K e C | A IC diz usar os mapas do Plano de Bacias para K e C (IC, "Materiais e Métodos") | Sustentado pela IC; escala e ano do mapa de solo não verificados |

**O que usamos no TCC.** Seção 3.1 (clima, geologia, população) e seção 3.3/Tabela 4 (mapas de solo e uso: 5 classes de solo, 9 de uso; fatores K e C por classe).

**Atenção.**
- Páginas: a IC cita "712 p."; o arquivo completo (relatório mais anexos) tem 1.342. A referência do TCC deve dizer qual versão (o link do site dos Comitês chama de "Relatório Final Completo"; os anexos ficam em arquivo separado).
- O Plano diz que a área tem predomínio de Argissolos Vermelho-Amarelos (50,5%) e Cambissolos Háplicos <2% nas Bacias PCJ; na área de estudo é o contrário (Cambissolo 68,6%, Argissolo 17,6%). Vale um parágrafo, pois explica por que a área não é típica da região (nota do projeto).
- Os números de população são totais do município, não da área de 137,8 km² a montante. A fonte melhor da população da área de captação é o município listado em Murillo-Bermúdez e Martim (2022).
- Eu não vi os mapas. Se alguém for citar a escala do mapa de solo do Plano, precisa abrir o PDF.

---

## 4. MURILLO-BERMÚDEZ e MARTIM (2022), IWISDW 1, p. 56-60

**Nível de leitura: texto completo** (PDF de 5 páginas do repositório da Unicamp, extraído e lido).

**O que é.** Trabalho curto de congresso. Usa a vazão do posto telemétrico do DAEE/SAISP (dados a cada 10 min, coordenadas -23,20883 / -46,76017, perto do fechamento da bacia) e a turbidez da água bruta medida de hora em hora na ETA da SABESP em Campo Limpo Paulista, convertida em concentração de sedimentos em suspensão (CSS). Seleciona os eventos com vazão de pelo menos 10 m³/s (menos de 1,5% do tempo monitorado) e analisa o laço de histerese entre Q e CSS. Resultado: 17 eventos, 13 em forma de oito (76%) e 4 horários. Não há chuva, nem vazão de base, nem carga de sedimento no texto.

**Dados no artigo.** Área da parte alta: "139,3 m²" (erro de digitação; certamente km²). Municípios da captação: Mairiporã, Atibaia, Jarinu e Campo Limpo Paulista. Equação (1): CSS = 3,264 × Turbidez^0,7974, descrita como "representativa para o local"; a calibração usou amostrador manual DH-48 e automático ISCO, com CSS pelo método de filtração. **Não informa número de amostras, R² nem faixa de validade.** A Tabela 1 lista, para cada evento: data, duração (h), Qmin, Qmax, CSSmin, CSSmax e tipo de histerese.

**O que usamos no TCC.**
- Seção 3.1: municípios da área de captação.
- Seção 3.2 e Tabela 1: vazão do DAEE/SAISP em 10 min; turbidez horária da ETA da SABESP.
- Origem da base dos 17 eventos (a planilha `Dados_finais_histereses_corrigido.xlsx`): conferi (meu cálculo) que o Qmax de cada um dos 17 eventos da Tabela 1 do artigo bate com a planilha, e o CSSmax bate em 15 de 17. Diferem o evento 6 (artigo 1.286,8; a planilha tem 1.286,8 às 23h de 16/01, mas um valor maior, 1.340, na janela que testei) e o evento 15 (artigo 2.596,2; planilha com máximo de 1.954 na janela). O evento 15 é o que domina 49% da variância linear no TCC.

**Atenção.**
- **Lista de eventos diferente.** Artigo (e gráfico da IC): 22/11, **24/11**, 30/11, 24/12/2018, 03/01, 16/01, 25/01, 15/02, 25/02, 17/03, 04/07, 30/12/2019, 02/01, 07/01, 02/02, 09/02, 20/02/2020. TCC (Tabela 2): 22/11, 30/11, **17/12**, 24/12/2018, 04/01... (os outros iguais). O evento de 24/11/2018 existe na planilha (Qmax 12,48 m³/s em 24/11 às 23h) e o de 17/12/2018 também (Qmax 16,56 em 19/12 às 20h). Não achei nas notas do projeto o motivo da troca; a fonte é o arquivo `eventos_processados_manuais.xlsx`, que não está no repositório. Pode ser escolha consciente, mas o TCC diz só "17 eventos... definidos na base de dados". Se for escolha, precisa ser explicada, e isso muda a comparação com a IC.
- Durações do artigo (23 a 147 h) e do TCC (23 a 149 h) diferem em 1 a 2 horas por evento: janelas definidas de outro modo.
- A frase "vazão igual a 10 m³/s" do artigo é critério de "pelo menos 10". O menor Qpico no TCC é 10,3, consistente.
- A equação (1) é para um período anterior ao do TCC? O artigo não diz o ano da calibração. Ver ref. 5.
- No artigo, a Martim aparece como "Martin"; nos metadados, "Salustiano-Martim".

---

## 5. MURILLO-BERMÚDEZ, MARTIM, POLETO e DALFRÉ FILHO (2023), Int. J. River Basin Management 21(2):233-241

**Nível de leitura: só resumo (e metadados).** A página da Taylor & Francis deu erro 403 e o artigo é de acesso fechado. Li o resumo por duas bases abertas (OpenAlex e Semantic Scholar) e por um trecho de busca que citava o resumo; os três concordam.

**O que é.** Estudo da bacia alta do Jundiaí em Campo Limpo Paulista. Os autores reaproveitaram a turbidez medida por uma empresa de tratamento de água na saída da bacia, e a combinaram com medições de amostradores tradicionais e análise de tamanho de partículas de um ano hidrológico inteiro para montar correlações turbidez-CSS. Compararam regressões lineares por R², valores-p, MSPE, PRESS e resíduos. **O melhor modelo foi uma regressão linear por partes, com quebra em 250 NTU, que superestimou pouco o CSS em turbidez alta.** O resultado foi usado para montar a série horária histórica de descarga sólida em suspensão. Palavras-chave: turbidez, CSS, descarga sólida, granulometria, regressão linear por partes. Datas: recebido 18/12/2020, aceito 27/06/2021, publicado online 28/10/2021, fascículo de abril de 2023.

**Autores (Crossref e OpenAlex):** L. F. Murillo-Bermúdez; A. L. S. Salustiano-Martim; C. Poleto; **J. G. Dalfré Filho** (José Gilberto Dalfré Filho). Confirmado nas duas bases. Forma ABNT sugerida: MURILLO-BERMÚDEZ, L. F.; MARTIM, A. L. S. S.; POLETO, C.; DALFRÉ FILHO, J. G.

**O que usamos no TCC.**
- Seção 2.4: "a carga é estimada a partir da turbidez convertida em CSS por curvas de calibração (Murillo-Bermúdez et al., 2023)". Isso o resumo sustenta.
- Seção 3.2, Tabela 1 e passo 1 do modelo: série de CSS "convertida por curva de calibração (MURILLO-BERMÚDEZ et al., 2023)".
- O pedido original menciona CSS = 3,264·Turb^0,7974.

**Atenção.**
- **A equação com esses coeficientes não está no resumo do artigo de 2023.** Ela está no trabalho de 2022 (ref. 4). O resumo de 2023 fala de regressão linear por partes com quebra em 250 NTU. Pode ser que a série da planilha tenha sido gerada com a lei de potência de 2022 e o artigo de 2023 mostre outro ajuste (ou também a lei de potência entre os modelos testados). Eu não consegui saber. Não encontrei na internet o número de amostras, o R² nem a faixa de turbidez de validade; só o texto do artigo ou os autores respondem.
- O CSS máximo da Tabela 1 de 2022 chega a 4.602 mg/L. Pela lei de potência isso corresponde a uma turbidez de ordem de milhares de NTU (meu cálculo, ~9.000 NTU), bem acima de 250 NTU, onde o resumo de 2023 diz que a regressão linear por partes mudou de comportamento. Se a faixa de validade for curta, a extrapolação aumenta a incerteza da carga medida, e o TCC deve declarar que a CSS é estimada, não medida diretamente.
- A planilha do TCC não tem turbidez, só CSS; então o TCC não consegue testar qual curva foi usada.
- Citação: IC usa "2021" para o mesmo artigo; o TCC usa 2023. Crossref: online 2021, fascículo 2023. Usar um ano só, de preferência o do fascículo com DOI, e dizer em nota "publicado online em 2021".

---

## 6. VIVARELLI et al. (2025), artigo da IC e Relatório Final PIBIC 2024/2025

**Nível de leitura: texto completo** (artigo de 5 páginas e relatório de 10 páginas, extraídos e lidos; tabelas e gráficos conferidos nas imagens).

**O que é.** MUSLE concentrada na parte alta do Jundiaí, forma Y = α·(D·qp)^β·K·LS·C·P, com D (volume) e qp (pico) do hidrograma medido (dados do SAISP) e K, LS, C médios da bacia inteira. Os autores calibram α e β nos 17 eventos e comparam com os coeficientes originais de Williams (1975).
- **Originais:** α = 11,8; β = 0,56. A IC diz que subestimam em média 29,58%, com erro máximo de 57,28% (o erro aumenta nos eventos de mais chuva).
- **Calibrados:** α = 0,277; β = 0,807 (ajuste de potência com R² = 0,91 na figura 2 do artigo, feito em planilha, sem validação separada). Erro percentual entre −60,01% e +37,14%, médio −4,15%.
- **Fatores médios:** K = 0,031; LS = 0,536; C = 0,267; P = 1. LS pelo método de Moore et al. (1991) no SAGA/QGIS, com MDE do USGS. K e C por classe vêm de mapas do Plano de Bacias comparados com valores de estudos brasileiros (Tabelas 1 e 2 do artigo).
- **K por classe:** Cambissolo Háplico 0,0475; Argissolo Vermelho-Amarelo 0,0351; Afloramento Rochoso 0,0087, e outros. **C por classe:** cultura anual 0,2116; pastagem 0,05; reflorestamento 0,121; solo exposto 1,0; vegetação nativa 0,015; corpo hídrico 0.
- O **relatório PIBIC** é mais longo: também aplica a MUSLE à bacia inteira do Jundiaí (10 eventos medidos com amostrador manual, menos confiáveis). Para essa aplicação, tentou três calibrações; as duas primeiras (α = 0,00112 e β = 1,03; α = 0,00000496 e β = 1,35) ficaram fora do intervalo da literatura, e a terceira foi **forçada manualmente** para α = 0,0385 e β = 0,8. Os fatores médios dessa bacia inteira são K = 0,033; LS = 0,544; C = 0,114. O relatório conclui que os fatores médios escondem a heterogeneidade (áreas urbanas, agrícolas, barramentos) e sugere, como continuidade, subdividir a bacia e usar MDE de maior resolução, o que é o que o TCC faz.

**O que usamos no TCC.**
- Seções 1.1 e 2.2: a IC é a referência concentrada anterior (volume e pico medidos, fatores médios).
- Seção 3.3 e Tabela 5: valores de K por classe de solo e C por classe de uso, "adotados na IC" (conferi: Cambissolo 0,0475, Argissolo 0,0351, Afloramento 0,0087, lavoura temporária 0,212, silvicultura 0,121, campo 0,05, mata nativa 0,015, solo exposto 1, corpo d'água 0 batem com as tabelas da IC).
- Seção 4.10 e 5.6, passo 11: a IC é comparador. Resultados publicados citados: α e β (0,277 e 0,807), erro médio −4,15%, faixa −60% a +37%. A "IC refeita" do TCC: α e β recalibrados em log, validação cruzada leave-one-out, volume total e pico medidos: erro mediano 16,3%, 100% dentro de fator 2, NSE em log 0,87.

**Atenção (divergências entre a IC e o que o TCC diz sobre ela).**
1. **"16,3%" não é da IC.** A IC não publica erro mediano, fator 2, NSE, nem validação cruzada. É só erro médio e faixa, no mesmo conjunto usado na calibração. O texto do TCC (seção 5.6) já chama de "IC refeita"; manter essa palavra em toda tabela e figura.
2. **A IC diz "volume de escoamento superficial"** (D). O TCC descobriu que, para reproduzir os erros, D tem de ser o volume **total** (com vazão de base). O artigo da IC não diz isso. O TCC está correto em apontar, mas a base disso é a reprodução numérica das notas do projeto, não texto da IC.
3. **Reprodução inexata.** O TCC reproduz erro médio de +2,6% e faixa de −47% a +62% contra −4,15% e −60% a +37% da IC (seção 4.10). Além da fonte de D e qp, **a lista de eventos pode ser um motivo**: a IC (gráfico da Figura 3) usa o evento de 24/11/2018, o TCC usa 17/12/2018 no lugar (ver ref. 4). A IC cita só "17 eventos de altas precipitações entre 2018 e 2020", sem lista.
4. **Sinal do erro.** O resumo da IC diz que com coeficientes calibrados a produção "foi superestimada" mas dá erro médio negativo (−4,15%); a conclusão fala em "tendência de superestimação". O sinal usado na definição do erro não é dado. Citar o −4,15% sem explicar a convenção pode confundir; sugiro dizer "erro médio de −4,15% segundo a convenção da IC".
5. **LS da IC.** O TCC diz que o LS médio da IC (0,536) foi calculado sobre MDE em coordenadas geográficas. O texto da IC não diz isso (só cita Moore et al., 1991, e SAGA); é conclusão das notas do projeto. O TCC já não usa esse LS (7,80).
6. **K e C médios da IC não são os do TCC.** A IC usa K = 0,031 e C = 0,267; o TCC calcula médias espaciais K = 0,039 e C = 0,050 com as mesmas classes mais as classes que a IC não tinha (área urbana K = 0 e C = 0, mineração e afloramento C = 1). Com a tabela da IC, a média simples das 6 classes de C dá 0,233 e a das 7 de K dá 0,043 (meu cálculo); nenhum bate com 0,267 e 0,031. Não dá para saber como a IC calculou as médias. O TCC afirma só que os valores **por classe** vêm da IC, o que é verdade.
7. **Classes sem fonte na IC.** A IC não tem classe de área urbanizada, campo, mineração, nem K de área urbana; o TCC atribuiu C = 0 (urbana e água), C = 1 (mineração e afloramento) e K = 0 (urbana). As notas já listam isso como "fontes que faltam".
8. **Calibração em dois níveis.** O α e β da IC vêm de uma regressão do artigo (R² = 0,91, ajuste de potência), mas o relatório conta que para a bacia inteira os coeficientes foram ajustados à mão para ficarem dentro do intervalo da literatura. Para o alto Jundiaí, o relatório não repete o método; o artigo é a fonte. O TCC pode dizer que a IC calibrou com todos os eventos de uma vez, sem validação separada.
9. **Referências da IC com defeitos que o TCC herda se copiar.** A IC lista autores corrompidos para Rubiano et al. (2011), "Sadeghu" em vez de Sadeghi, Moore et al. (1991) e Martin/Martim; e coloca "Sotero" como sobrenome em "Murillo-Bermúdez e Sotero, 2022". Não afeta o TCC se as referências forem conferidas pelo Crossref.
10. **Autoria.** O artigo da IC tem 4 autores (Vivarelli, Murillo-Bermúdez, Braga, Martim); o TCC cita "VIVARELLI et al., 2025", o que está certo. O relatório PIBIC é só Vivarelli (orientador Martim, coorientador Murillo-Bermúdez) e traz "Setembro / Maio de 2024" na capa (data inconsistente).
