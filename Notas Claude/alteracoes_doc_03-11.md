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
