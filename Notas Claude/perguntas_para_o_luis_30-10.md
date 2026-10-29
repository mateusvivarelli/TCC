# Perguntas para o Luis (30/10/2026)

Perguntas que só o orientador responde, reunidas pela sessão na nuvem. Cada uma diz por que importa e o que muda no texto conforme a resposta. As quatro primeiras vêm de `instrucoes_sessao_desktop.md` (seção 6) e ainda estão abertas.

## Sobre o modelo e os dados

1. **Aprova o modelo oficial** (CN-I da base da ANA, λ = 0,05 com a retenção convertida por Woodward et al. (2003), MUSLE por pixel só com o escoamento direto, SY = c * Σ E_unit, c calibrado em log, validação leave-one-out, alvo = carga total)? Todo o texto novo parte dele.

2. **Vazão de base (coluna Bt) e BFImax.** A série fornecida é reproduzida exatamente pelo filtro de Eckhardt com a = 0,995 e BFImax = 0,70, mas o cabeçalho do arquivo `serie_Q_Qb_Qquick_Eckhardt_orientador.xlsx` diz BFImax = 0,58. Qual foi usado, e por quê? Ponto novo: Eckhardt (2005), segundo Eckhardt (2012), sugere BFImax de 0,25 para rios perenes com aquífero em rocha dura, e a sub-bacia é dominada por embasamento cristalino com aquífero fraturado (86%). Há justificativa para 0,70 (por exemplo, calibração com recessões)? A resposta entra na 3.2 e na 4.6.

3. **Evento de 24/11/2018 x 17/12/2018.** A lista de 2022 e a IC usam 24/11/2018; o TCC usa 17/12/2018 (o "1B" da planilha foi excluído). Por que a troca? Ela afeta a comparação com a IC (4.3), e a 3.2 precisa de uma frase explicando.

4. **Curva turbidez-CSS.** A série de CSS foi gerada com a lei de potência CSS = 3,264 * Turbidez^0,7974 (trabalho de 2022) ou com a regressão linear por partes com quebra em 250 NTU (resumo do artigo de 2023)? Qual a faixa de turbidez das amostras de calibração? A 2.5, a 4.3 (evento 17) e a 4.6 dependem disso.

5. **Origem da coluna `Chuva_evento_mm`** (lâmina R da Tabela 2). Ela não é a média do raster IDW (no evento 11, 74,0 mm contra 73,5 mm) e é reproduzida, com resíduo de até 0,57 mm, por 0,307 * DBT5 + 0,693 * Campo Limpo. Como foi calculada? Hoje a 3.4.1.4 diz só "corresponde, com diferença de até 0,6 mm, à média ponderada...".

6. **Delimitação dos eventos.** As janelas foram definidas à mão sobre o hidrograma? Há um critério escrito (por exemplo, vazão de pelo menos 10 m³/s, como no trabalho de 2022, e um critério para o fim da recessão)? As durações do TCC diferem 1 a 2 h das do artigo de 2022. A 4.6 trata a delimitação como limitação sem estimativa; se houver critério, ele entra na 3.2.

7. **Intensidade RI.** A coluna `Intensidade_60min_mm/h` é a maior intensidade horária entre os dois postos (não a da média). Confirma? Por isso RI/R passa de 1 nos eventos 1 e 12, e o texto agora trata RI/R como índice de concentração temporal.

## Sobre a estrutura pedida nos comentários

8. **C24: qual gráfico de "vazão calculada e vazão medida"** você viu na reunião? Usei `TCC_Texto/figuras/fig_volume_direto.png` (escoamento direto do SCS-CN contra o medido, por evento, em log, com a faixa de fator 2). Se era outro (por exemplo, hidrogramas de um evento ou a figura antiga `Figuras/ilustrativas_27-10/B_volume_scs_x_medido.png`), dizer qual.

9. **C22: qual tabela tinha partes sobrepostas?** O comentário saiu sem o trecho. Refiz a Tabela 11 antiga (sedimento por evento, agora Tabela 12, 8 colunas estreitas) e a Tabela 10 antiga (evento 11, agora Tabela A1 com 2 colunas), e tirei 2 colunas da Tabela 3. Se era outra, indicar.

10. **C20: "Anexo 1" ou "Apêndice A"?** Pela NBR 14724, texto elaborado pelo próprio autor é apêndice; anexo é material de terceiros. Proponho "APÊNDICE A - Exemplo numérico: o evento 11". Concorda?

11. **Seção 4.6 "Fontes de incerteza e limitações".** Você pediu para lembrar das incertezas dentro da discussão (S22) e para falar bastante da defasagem do modelo. Proponho as duas coisas: incertezas citadas onde explicam um resultado e uma 4.6 curta com a cadeia de erros, da medição ao mapa. Prefere sem a 4.6?

12. **Parágrafo da IC na 2.2.** Deixei no capítulo 2 (é trabalho anterior, literatura) e o uso como comparação na 3.4.8. Prefere tudo na 3.4.8?

13. **C31 (R² do mapa).** A proposta mede, entre os pixels com erosão, o R² de ln(erosão média) com ln(K*LS*C) e com o termo de escoamento, e reparte o R² pela média dos ganhos nas duas ordens; em escala linear, o R² entre o mapa e K*LS*C (cerca de 0,59 pelo r de 0,77 já calculado). É isso que você imaginou? Os números serão calculados no PC.

14. **Comparação com a IC.** Por decisão do Mateus, a IC entra só com os valores originais (22,5% de erro mediano, 100% em fator 2, ajuste nos 17 eventos da IC). Como a lista de eventos e a carga medida diferem, a comparação com o MFM (20,6%, validação cruzada) é só lado a lado, sem teste pareado. Concorda com essa forma?

## Sobre referências

15. **Validação cruzada aninhada (C19) e artigos de alta resolução temporal (C10).** A sessão na nuvem não conseguiu ler nenhuma obra nova (a rede bloqueia os sites dos periódicos). Candidatas: Varma e Simon (2006) e Cawley e Talbot (2010) para a validação aninhada; Rasmussen et al. (2009, USGS) e Gray e Gartner (2009) para turbidez; Williams (1989) para histerese; Minella et al. (2008) para turbidez em bacia brasileira. Você tem outras preferidas, sobretudo de dados de turbidez de alta frequência em eventos no Brasil? Tem os PDFs para passar ao Mateus?

16. **Murillo-Bermúdez et al. (2023).** O artigo é de acesso fechado e só o resumo foi lido. Você pode passar o PDF? Ele sustenta as frases da 2.5 e da 4.6 sobre a curva turbidez-CSS e a quebra em 250 NTU.

17. **Fonte dos valores de K e C da IC.** Os valores de C do campo (0,050) e da lavoura temporária (0,212) e o K do Cambissolo (0,0475) não foram confirmados nas obras citadas pela IC (lote D). Você sabe de onde vieram? Eles mudam o peso das classes no mapa (4.5).
