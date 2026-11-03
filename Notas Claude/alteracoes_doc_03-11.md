# Alterações no Doc em 03/11/2026

## Formatação (padronização)
* Títulos e subtítulos (nível 1 a 3): Arial 12, negrito, alinhados à esquerda, 12 pt acima, espaçamento 1,5. Renderização conferida no PDF exportado (todos os títulos saem em Arial negrito 12).
* Tabelas: legenda ("Tabela N." em negrito) e "Fonte:" à esquerda, 10 pt, legenda com 8 pt acima e 4 pt abaixo, fonte com 4 pt acima e 10 pt abaixo.
* Figuras: imagem, legenda ("Figura N." em negrito) e "Fonte:" centralizadas, 10 pt. Nas Figuras 5 a 9 a imagem tinha sido inserida depois da legenda (ou no fim dela); as legendas foram movidas para baixo da imagem, como nas Figuras 1 a 4.

## Referências (marcadores "[REFERÊNCIA A LER]" substituídos)
| Trecho | Fonte usada | Observação |
|---|---|---|
| 2.5, carga = soma no tempo; CSS por turbidez; limites da curva | Rasmussen et al. (2009); Gray e Gartner (2009) | "integral" trocado por "soma ao longo do tempo"; "só é confiável" trocado por "de preferência na faixa das amostras" |
| 2.5, histerese | Minella, Merten e Magnago (2011) | só o que o artigo sustenta (bacia de 1,19 km2, laço horário em 17 de 19 eventos, variação entre eventos); a frase da "relação fixa" ficou como raciocínio do trabalho, sem citação. Minella et al. (2008) e Williams (1989) saíram do texto (não lidos) |
| 2.7, densidade de postos | Ochoa-Rodriguez et al. (2015) | com ressalva (bacias urbanas, chuva de radar). Faurès et al. (1995) saiu do texto (não lido) |
| 2.8 e 3.4.6, validação cruzada aninhada | Varma e Simon (2006); Cawley e Talbot (2010) | frase "validação cruzada simples corrige apenas o viés dos parâmetros" trocada por redação que as obras sustentam |

Seis referências novas na lista (ordem alfabética): Cawley e Talbot; Gray e Gartner; Minella, Merten e Magnago; Ochoa-Rodriguez et al.; Rasmussen et al.; Varma e Simon.

Ordem dos autores conferida nos próprios PDFs: Cawley, G. C.; Talbot, N. L. C. / Gray, J. R.; Gartner, J. W. / Minella, J. P. G.; Merten, G. H.; Magnago, P. F. / Ochoa-Rodriguez, S. et al. / Rasmussen, P. P.; Gray, J. R.; Glysson, G. D.; Ziegler, A. C. (citado como Rasmussen et al.) / Varma, S.; Simon, R.

## Figuras regeneradas (Scripts/gerar_mapas_tcc.py)
* Figura 2 (mapa_02): sem título geral nem rodapé na imagem, legenda inteira (bbox tight).
* Figura 4 (fig_fluxograma): modelo oficial (CN-I, lambda 0,05, MC e MFM, Vdir = T_R - SBt*3600), legenda de cores no topo, sem texto cortado.
* mapa_06, mapa_07, mapa_08: rótulos "Sedimento estimado" (no lugar de "Sedimento das encostas"), "escoamento calculado" (no lugar de "água"), rodapé do mapa_07 sem a menção ao método descartado.

## Conferência Figura 4 x texto (seção 3.4)
Texto e figura batem: IDW com 2 postos; CN-I; lambda 0,05 com S convertido; E_unit = 11,8*(Q*pr*A)^0,56*K*LS*C (P = 1); soma sobre os pixels; SY = c * soma; c em escala logarítmica contra SY_obs; leave-one-out; MC e MFM; comparação com testes simples e com a IC.

## Pendente (manual)
Inserir as Figuras 10, 11, A1 e A2 (mapa_06, mapa_07, mapa_08), trocar as imagens das Figuras 2 e 4 pelas novas, converter as linhas amarelas de equação, atualizar o sumário, responder aos comentários do Luis.

## Correções do revisor independente aplicadas (03/11, tarde)
Resumo e Abstract (MFM equivale à regra com o volume medido; "sugere" no lugar de "indica"); 4.4 (padrão do mapa; eventos 8, 9, 15 e 16); 4.5 (escala log x linear; Cambissolos; "campo degradado" e "bacia de abastecimento" retirados; mineração e solo exposto por C = 1 adotado; "sugere"); 4.3 (padrão entre estações descrito só para os eventos 1 a 6 e 14 a 17; IC no evento 17 em 37% pela carga da própria IC; expoente efetivo 1,12); 4.1 e Conclusões (+3% era o critério de escolha; "indica que" no lugar de "porque"); 3.1 (0,2%); 1.1 (14,1% e 42%); 3.2 (sem Lyne e Hollick como método testado); 3.4.3 (cita o Apêndice A); 3.4.6 (ponto duplicado); 3.4.7 (Wilcoxon definido; frase sobre variância); evento datado de 24/11/2018 na lista da IC descrito como inexistente na série; ordem CASTRO antes de CAWLEY.
Não aplicadas: símbolos com vários sentidos, siglas na primeira ocorrência, níveis de título 3.4.x, iniciais de AZMERI, padrão de DOI, Dedicatória e Agradecimentos vazios, fatores médios da IC, origem de R e dos pesos, sensibilidade a K e C.

## Versão em Word
`TCC_Texto/TCC_versao_03-11.docx` (e `.pdf`): exportada do Doc, com as Figuras 2 e 4 novas, as Figuras 10, 11, A1 e A2 inseridas (A1 e A2 são as duas metades do mapa_08), 20 equações nativas do Word no lugar das linhas amarelas, a linha duplicada do LS removida e todo o destaque amarelo retirado. Script: `Scripts/montar_docx_tcc.py`. O sumário vem do Google e precisa ser atualizado no Word (botão direito, Atualizar campo).

## Revisão final (03/11, manhã)
* O Doc voltou a ser o importado do Word (equações e imagens já dentro). Formatação conferida no PDF exportado e na estrutura: títulos 1 a 3 padronizados (Arial 12 negrito, 12 pt acima, espaçamento 1,5), parágrafos das Tabelas 1 a 6 com espaçamento 1,0 como as demais, 27 parágrafos vazios antes de legendas de tabela apagados, legendas e "Fonte:" já uniformes.
* Texto: siglas definidas na primeira ocorrência (SCS-CN no Resumo e no Abstract, WEPP, LISEM, SWAT, DAEE, SABESP, NSE), DOI no mesmo formato, "coorientação", frase sobre os símbolos Q, V, P e c/C na 3.4.1.1, explicação da diferença entre os fatores médios da IC e os deste trabalho (3.4.8), frases de ausência na literatura e sobre a série de vazão de base mais cautelosas.
* AZMERI: o autor tem nome único (Azmeri, Muhammad Iqbal, Muhammad Fauzi, Maimun Rizalihadi); a entrada "AZMERI et al." está correta.
* Dados conferidos: Tabela 13 contra as tabelas-fonte; "91% da variância" (r = 0,956; R² = 0,914); regra com o escoamento no evento 17 (-61%) e erro mediano 15,9% recalculados.
* Figuras A1 e A2 refeitas com os painéis empilhados (mapa_08a e mapa_08b), uma por página; as imagens do Doc ainda são as antigas até você substituí-las (ou reimportar o `.docx`).
