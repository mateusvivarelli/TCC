# Revisão do texto: versão de 04/11 (RELATÓRIO PARCIAL, em andamento)

**Situação:** versão provisória, gravada a pedido da coordenação. O relatório completo vai substituir este arquivo.

## (a) O que foi lido e o que falta

- Lido por inteiro: texto das 68 páginas (`Notas Claude/doc_texto_pdf_paginas_04-11.txt`) e `Notas Claude/entrega_tfc_regras.md`.
- Ainda não feito: conferência visual das figuras e equações no PDF; recálculo por script (as contas abaixo foram feitas à mão, a partir das tabelas do próprio texto); leitura de `Normas FECFAU/`; conferência das citações contra `leitura_referencias/`; comparação com `revisao_independente_03-11.md` e `alteracoes_doc_03-11.md`; verificação do evento de 24/11/2018.

## (b) Achados até agora (preliminares)

### Crítico

1. **Sumário, p. 9 do PDF.** A paginação está defasada em relação às páginas impressas. Exemplos: seção 2 diz 11 (está na 12); seção 5 diz 57 (está na 59); Referências dizem 59 (estão na 61); Apêndice A diz 63 (está na 65). Correção: atualizar o sumário no fim da edição.
2. **Pré-textuais, p. 3 a 5 do PDF.** A p. 3 está em branco, e Dedicatória e Agradecimentos só têm o título. A folha de aprovação, obrigatória no modelo da biblioteca (`entrega_tfc_regras.md`, seção 4), não aparece. Correção: incluir a folha de aprovação; preencher ou retirar as páginas opcionais.
3. **Conclusões, p. 60 impressa.** Trecho: "A comparação demonstra que a espacialização não se mostrou pior". A seção 4.3 (p. 50) diz que "a comparação é só indicativa". O texto se contradiz. Sugestão: "A comparação indica apenas que, com o escoamento medido, a espacialização chega a um erro da mesma ordem, e ela acrescenta o mapa de onde a erosão é produzida."

### Importante

4. **Seção 4.3, p. 50.** Trecho: "em média, maior nos eventos 12 a 16 (cerca de 1.700 mg/L, sem o evento 17) do que nos eventos 1 a 11 (cerca de 1.450 mg/L)". Pela Tabela 3, a média simples dá cerca de 1.684 e 1.364 mg/L, e a razão entre as somas dá cerca de 1.571 e 1.449 mg/L. Os valores do texto parecem misturar duas contas. Falta confirmar por script qual foi usada.
5. **Seção 4.6, p. 57.** Trecho: "quase o dobro da dos demais". A seção 4.3 dá 3.806 mg/L contra 1.085 a 2.088 mg/L: cerca de 1,8 vez o maior valor, e bem mais que isso em relação à média. Sugestão: "cerca de 1,8 vez a maior entre os demais eventos".
6. **Seção 4.3, p. 49, contra a seção 3.4.7.** O teste de Wilcoxon é usado nos resultados, mas o método não o descreve (só o bootstrap). Sugestão: acrescentar o teste ao fim da seção 3.4.7.
7. **Seção 3.1, p. 21, contra as seções 4.1 e 4.4 (p. 44 e 51).** A seção 3.1 diz que "a cabeceira tende a estar na porção mais chuvosa da sub-bacia"; as seções 4.1 e 4.4 dizem que a cabeceira "recebe menos chuva" na maioria dos eventos. Pela Tabela 2, DBT5 registra menos que Campo Limpo em 13 de 17 eventos. Sugestão: explicar a diferença entre a média anual regional e os 17 eventos.
8. **Termo "medido", seção 3.2 (p. 23), Tabelas 3 e 7, seção 4.1.** O mesmo Vdir aparece como "estimado" (seção 3.2, Tabela 3) e "medido" (Tabela 7, Tabela 11). Sugestão: dizer uma vez que "medido" significa obtido do hidrograma medido, com a base separada por filtro, e manter um só termo.
9. **Tabela 14, p. 53.** A coluna "Erosão por área, MC" não tem unidade. Pelos valores (129 = 37,4 / 29,0 * 100), é um índice com a média da bacia = 100. Sugestão: "Erosão por área, MC (média da bacia = 100)".
10. **Tabela 4 e fonte, p. 25.** "USGS" é citado, mas não há entrada nas referências, e a sigla não é explicada.
11. **Símbolo TR, seção 3.2, p. 23.** Aparece em "o volume TR" sem definição; só é definido na Tabela 7 (p. 29).

### Menor

12. **Seção 2.2, p. 13.** "eficiência de Nash-Sutcliffe (NSE) de validação cruzada próximo de zero": concordância. Sugestão: "próxima de zero".
13. **Seção 3.4.7, p. 36.** "Absolute Percentual Error": o termo em inglês é "Absolute Percentage Error".
14. **Apêndice A, p. 65.** "recebe P = 75,4 mm" contraria a seção 3.4.1.1 (p. 29), em que P sem índice é o fator de práticas. Sugestão: "P_k = 75,4 mm".
15. **Conclusões, p. 59.** A incerteza da separação da vazão de base e a chuva de dois postos aparecem em duas frases seguidas. Sugestão: juntar as duas.
16. **Folha de rosto, p. 2 do PDF.** O texto diz "título de Engenheiro Civil"; o modelo da biblioteca diz "título de Bacharel em Engenharia Civil".

## (c) O que está bom (conferido à mão até agora)

- Somas de áreas e contribuições das Tabelas 14 a 16 fecham em 100%, e as frases da seção 4.5 batem com elas.
- As métricas do volume na seção 4.1 (46%, 54%, 11 de 17) e os erros do MC e do MFM (81%, 21%, 6 e 16 eventos em fator 2, 10 e 7 eventos por sentido) batem com as Tabelas 11 e 12.
- A conversão de Woodward para milímetros (0,8189) e as contas principais do Apêndice A estão coerentes.

## (d) Resumo

Será escrito no relatório final.
