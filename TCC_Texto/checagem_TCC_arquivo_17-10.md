# Checagem do "TCC arquivo" (até 4.10, antes de Resultados e Discussão) — 17/10/2026

Vista considerada: Doc com as minhas 8 sugestões aceitas.

## A. Corrigir

### Texto e numeração
1. **Numeração da seção 4.** O Doc vai de 4.8 direto para "4.10 Exemplo numérico". Faltam 4.9 (Testes simples) e 4.10 (Comparação com a IC). A 4.1 diz "seções 4.9 e 4.10" para testes simples e IC. Quando escrever essas seções, o exemplo passa a ser 4.11; se não, corrigir a 4.1.
2. **4.8, item do NSE.** O texto começa repetido ("NSE em escala logarítmica: O NSE em escala logarítmica é...") e termina no meio da explicação: faltam por que o log dá peso ao erro relativo, o fato de os 3 menores eventos dominarem (68%) e por que é métrica de apoio. O parágrafo completo está na 4.8 do `TCC_rascunho_04.md`.
3. **4.5, item do MC.** Ainda diz "a base é o volume de referência acima". Reescrever com a fórmula explícita (ver `comentarios_para_TCC_arquivo.md`, itens 17 a 19).
4. **4.3, AMC I.** Ainda diz "herdada da fase em que o modelo foi calibrado contra o volume total". Justificar de outro modo.
5. **Tabela 7.** Está com "Modelo calculado" e "Modelo forçado ao medido" por extenso e "Qb_inicio × T_chuva". Usar "MC" e "MFM" e "Qb_inicio × T_chuva × 3600". Na linha do MFM, trocar "vazão de base medida (Bt)" por "Σ Bt × 3600".
6. **Resumo, última frase** ("A espacialização mantém a qualidade da formulação concentrada"). Isso vale para o MFM (14% contra 16% da IC). O MC é pior que a IC (33% contra 16%). Acrescentar "quando recebe informação equivalente" no resumo e no abstract.
7. **2.2, Baert et al. (2026).** O artigo tem 154 eventos de escoamento, mas só **46** com sedimento completo; o NSE de −0,03 e 0,01 é do sedimento. Ajustar para "154 eventos de escoamento, 46 deles com sedimento medido". A área de 0,84 km² confere (83,84 ha).
8. **Título "4. METODOLOGIA".** O negrito está só no número; os outros títulos estão todos em negrito.

### Tabela 9 (evento 11)
9. **Linha "sedimento do pixel":** `0,00352 · 1,038`. A linha de cima já diz E_unit = 1,039. Usar 1,039 nas duas.
10. **Linha do escoamento do pixel:** com os valores arredondados da própria tabela (P = 75,4; S = 141,9), a conta dá **11,69 mm**, não 11,72. O valor 11,72 vem de P = 75,45 mm. Mostrar P = 75,45 mm ou avisar que os valores estão arredondados.
11. **Linha do volume de referência:** `0,945 · 23 · 3.600 = 78.226`. Com 0,945 dá 78.246. Usar Qb_inicio = 0,9448 m³/s.
12. **"Validação cruzada" na Tabela 9** (MC 1.098 t; MFM 1.711 t): explicar em uma frase que é a previsão com c₁ e c₂ recalibrados sem o evento 11.

### 4.6 (equação)
13. A equação de calibração está como **imagem** (606 × 65 px). Refazer como equação do Docs. Ela escreve a soma dos pixels como "E_unit,n", enquanto a 4.5 escreve "Σₖ E_unit,k". Padronizar para "Σₖ E_unit,k,n", ou definir E_n.

### Figuras
14. **Figura 3 (fatores):** ainda está com o LS antigo (escala de 0 a 2). Trocar por `figuras/mapas/mapa_03_fatores.png` (LS de 0 a 25).
15. **Figura 4 (fluxograma):** a versão do Doc tem o texto "Qb_inicio × duração da chuva" estourando a caixa "Termo de base". `figuras/mapas/fig_fluxograma.png` tem "MC: Qb_inicio × T_chuva".
16. **Figuras 1, 2 e 5:** estão certas. A Figura 5 já traz 106 t + 1.025 t.

### Referências
17. **ABNT na 2.4:** "(Murillo-Bermúdez et al., 2023)" está em minúsculas. Chamada entre parênteses vai em maiúsculas: "(MURILLO-BERMÚDEZ et al., 2023)". O mesmo vale para citações semelhantes.
18. **Autoria do artigo do IJRBM:** "POLETO, C.; FILHO, J. G. D. ." tem um espaço antes do ponto e a abreviação do quarto autor está incerta. A nota da outra sessão registra "[nome do 4º autor]". Confirmar o nome com o orientador.
19. **Espaçamento:** as entradas USDA-SCS, Valle Junior, Vivarelli, Williams e Wischmeier estão sem o espaço entre parágrafos usado nas demais.
20. Dos conferidos nos PDFs do projeto (Baert, Brandão, Hao), os dados bibliográficos batem. Os demais (Chow, Eckhardt, Lyne e Hollick, Moore e Burch, Nash, Sartori, Valle Junior, Williams, Wischmeier, Murillo-Bermúdez) não foram testados online nesta checagem.

### Comentários antigos no Doc (8, ainda abertos)
21. Já aplicados: #2 (fontes dos dados), #4 em parte (separação do escoamento), #5 (fecho do abstract) e #8 em parte (municípios e população).
22. **Ainda não aplicados:** #3 (a equação CSS = 3,264 · Turb^0,7974 não aparece no texto), #6 (outras áreas, 138,8 e 139,3 km², e o exutório 894 m a jusante da estação), #7 (as classes citadas somam 99,8%) e a frase "O rio nasce na Serra da Pedra Vermelha" do #8.
23. **O comentário #4 contradiz o que encontrei sobre o Bt.** Ele diz que os filtros padrão não reproduzem a série (Lyne e Hollick: 1,7% das horas). Reexecutei com o filtro de Eckhardt (a = 0,995; BFImax = 0,698) e a série é reproduzida quase por inteira: diferença mediana de 0,0002 m³/s e máxima de 0,004 m³/s em 20.838 h. Quem escreveu o #4 provavelmente não testou o Eckhardt com esses parâmetros. Decida se mantém "método não documentado". Corrigi no rascunho a frase anterior "erro menor que 10⁻⁴", que estava errada.

## B. Conferido e correto
- **Tabelas 2 e 3:** iguais às geradas pelos scripts (totais 28.934 / 13.671 / 15.263 / 13.455 mil m³; sedimento total 23.846 t).
- **Tabela 4:** K 0,039, C 0,050, LS 7,80 e CN 71,6 conferem. **Tabela 5:** K, C e % de pixels conferem.
- **Tabela 8:** c₁ e c₂ do MC e do MFM, IC refeita (0,978 e 0,733) e pesos 0,307 / 0,693 conferem.
- **Pixels:** 884 × 365; 897,49 m²; 154.667 pixels com CN; 153.855 de cálculo = 138,08 km²; diferença de 812 pixels (o texto diz "cerca de 810").
- **CN:** 20 valores entre 52 e 98 (AMC II); AMC I de 31,3 a 95,4 (o texto diz "31 a 95").
- **Coordenadas dos postos (UTM 23S):** DBT5 348.520,8 / 7.426.415,3 e Campo Limpo 319.862,4 / 7.432.277,5 conferem com o shapefile.
- **Evento 11:**
  - Pixel de exemplo: K 0,0351, C 0,212, LS 4,869, centro em E 330,18 km / N 7.432,86 km.
  - Chuva IDW: média 73,5 mm (63,2 a 79,0).
  - Q médio 5,4 mm, sem escoamento em 10,4% dos pixels, volume do SCS-CN 751 mil m³ contra 1.479 mil m³ medidos.
  - Soma de E_unit 30.003, encostas 106 t, base 1.025 t.
  - R = 74,0 mm e RI/R = 0,159.
- **Altitude (3.1):** "725 e 1.315 m" confere com o MDE original (723,5 a 1.314,1 m). No raster de 30 m dos pixels de cálculo, de 740 a 1.314 m.
- **Resumo e abstract:** 71%, 33%, 94% e 14% conferem (MC 32,6%; MFM 13,6%).
- **Literatura (conferida nos PDFs do projeto):**
  - Hao et al.: 1.314 bacias, conectividade abaixo de 0,5 em cerca de 80% da área.
  - Brandão et al.: 3.578 bacias, melhor desempenho com λ = 0,05.
  - Baert et al.: NSE máximo de 0,13 no volume, 0,21 a 0,40 fora da amostra.
- **Citações no texto e na lista de referências:** todas as citadas estão na lista e todas as da lista são citadas.
- **Numeração:** Tabelas 1 a 9 e Figuras 1 a 5 em sequência.

---

# Atualização de 18/10/2026: o Doc agora vai até as Conclusões; o que falta

## Estado
- Estão no Doc: capa, folha de rosto, epígrafe, resumo (224 palavras), abstract (212), sumário (34 entradas), seções 1 a 6 e referências.
- As 11 figuras do Doc coincidem com as versões finais em `figuras/`. A Figura 3 já está com o LS novo.
- Formato conferido: A4, margens 3/3/2/2 cm e Arial 12 conferem com a norma. O espaçamento entre linhas é 1,15 e a norma deduzida pede 1,5 (confirmar).

## Faltando
1. **Folha de aprovação** (obrigatória na norma). Dedicatória e agradecimentos estão vazios (opcionais).
2. **Seções 4.9 e 4.10 (testes simples e comparação com a IC)** foram removidas da metodologia, mas os resultados usam esses modelos (Tabela 8: IC refeita; Tabela 11; seções 5.4 e 5.5).
3. **Seção sobre o SCS-CN não prever o escoamento direto** foi removida dos resultados, mas a Conclusão 2 depende dela. Sem tabela de λ, sem o coeficiente de escoamento e sem a recalibração (Apêndice D).
4. **5.3 e 5.4 sem tabela e figura** (a figura da escada e a Tabela de desempenho do modelo × teste simples). A 5.4 cita a "Tabela 13", que é a de classes de solo.
5. **Limitações** (seção 6 do rascunho 04) ausentes. As Conclusões estão sem numeração e sem trabalhos futuros.
6. **Apêndices:** a 4.7 cita o Apêndice C, que não existe. Apêndice A (evento 11 passo a passo nas planilhas) pendente.

## Numeração e referências cruzadas
- Seção 5.5 é seguida da 5.7 (falta 5.6).
- 5.2 cita "(Tabela 11)" para os erros no ajuste; é a Tabela 10. A Tabela 11 (comparação) não é citada em 5.5.
- Tabelas 2 e 6 e a Figura 6 não são citadas no texto.
- Tabela 7: "(MCM)" deve ser "(MFM)".
