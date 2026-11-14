# Slides da defesa do TCC: plano e decisões (14/11/2026)

## Onde está cada coisa
* **PowerPoint do autor (versão em construção):** `C:\Users\user\OneDrive\Documentos\slideTCC.pptx` (10 slides em 14/11, tema FECFAU: faixa azul com "Introdução", logo, fonte Calibri, equação em Cambria Math). O autor está montando à mão.
* **Deck de referência feito pela IA (artefato, 18 slides, texto e notas de fala prontos):** https://claude.ai/artifact/3oiHcBZGr55SqKYJxYrGoj (privado).
* **Mapas novos da bacia:** `TCC_Texto/figuras/mapas/mapa_bacia_jundiai.png` (bacia inteira, parte alta, municípios e rios) e `mapa_alta_jundiai_municipios_rios.png` (parte alta com rios nomeados). Scripts em `Scripts/mapa_bacia_jundiai/` (1: delimita a bacia a partir de DEM da AWS Terrain Tiles, 150 m; 2: desenha os mapas com limites municipais do IBGE). Tabela dos municípios: `TCC_Texto/tabelas/municipios_bacia_jundiai.csv`. Os dados baixados (tiles do DEM, malha do IBGE) não foram versionados; os scripts dizem de onde vêm.
* **Figuras A1/A2 (evento 11, painéis empilhados):** `mapa_08a_...` e `mapa_08b_...` em `TCC_Texto/figuras/mapas/`.

## Estrutura da parte já feita no PowerPoint (slides 1 a 10)
1 capa · 2 título completo · 3 MUSLE (Williams, 1975) · 4 (Q*qp) físico · 5 K, LS, C, P empíricos · 6 constantes 11,8 e 0,56 · 7 mapa pequeno da bacia (estudo de caso) · 8 mapa grande (efeito de crescer, depois volta) · 9 espacialização (pixels de 30 m, 153.855) · 10 objetivo (identificação de áreas críticas).

### Correções combinadas para esses slides
* **Slide 5:** K = erodibilidade do solo; **C = cobertura e manejo** (fração da erosão do solo exposto que ainda ocorre); **P = práticas conservacionistas** (1 = nenhuma). C e P não são "erodibilidade". Escrever "prática" com acento e tirar as linhas em branco.
* **Slide 6:** 11,8 e 0,56 são as constantes originais de Williams; α e β (0,277 e 0,807) são os da IC. Neste TCC só se calibra **c**.
* **Slides 7 e 8:** manter mapa pequeno que cresce e volta (Morfose). Para o efeito funcionar, nomear a imagem nos dois slides com o mesmo nome começando por `!!` (Painel de Seleção, Alt+F10). Versão do mapa para projeção, com letras maiores, ainda a fazer.
* **Slide 9:** ideia do autor: sem espacialização só há dados hidrossedimentológicos (quanto); com espacialização há também referência espacial (onde). Acrescentar "(~900 m² cada)" aos 153.855 pixels.
* **Slide 10:** deixar só o objetivo do TCC; não precisa de aspas, itálico nem auto-citação (é texto do próprio trabalho). Conferir se a frase é igual à seção 1.3.1.
* Vocabulário do ditado: "Hal/How" = Hao et al. (2022); "William" = Williams (1975); "Luiz Murilo" = Luis Murillo-Bermúdez; "Muzzle" = MUSLE; "SCN" = SCS-CN; "CN2/CN1" = CN-II/CN-I; "Woodhart" = Woodward et al. (2003).

## Plano dos próximos slides (autor, 20 min no total)
Estrutura: depois da introdução, segue-se um evento (o 11, como no Apêndice A) passo a passo, com "parênteses" para detalhes; depois sai do evento e usa os 17.

| # | Slide | Referência | Tempo |
|---|---|---|---|
| 11 | Dados e os 17 eventos (vazão DAEE, turbidez SABESP, chuva de 2 postos) | Murillo-Bermúdez e Martim (2022); Murillo-Bermúdez et al. (2023) | 1:00 |
| 12 | Evento 11 (rápido): 4 a 8/jul/2019, R = 74,0 mm, RI = 11,8 mm/h, carga medida 1.822 t | | 0:25 |
| 13 | Chuva espacializada (rápido): IDW | | 0:25 |
| 14 | Escoamento do pixel (SCS-CN) com números | Chow et al. (1988) | 0:45 |
| 15 | **Parêntese 1:** CN-I (seco) e λ = 0,05 com S por Woodward | Woodward et al. (2003); Brandão et al. (2025) | 0:50 |
| 16 | **Pico local** (Hao et al.): bem explicado | Hao et al. (2022) | 0:50 |
| 17 | Erosão local do pixel (Williams) com números | Williams (1975) | 0:40 |
| 18 | **Parêntese 2:** coeficiente c | | 1:10 |
| 19 | Calibração e validação (17 eventos, leave-one-out) do MC | | 0:50 |
| 20 | Resultado do MC e comparação com regra simples | | 0:50 |
| 21 | MFM (rápido): troca a entrada, repete o procedimento | | 0:40 |
| 22 | Comparação MFM x regra com volume x IC | Vivarelli et al. (2025) | 0:50 |
| 23 | Resultados: escoamento e sedimento | Baert et al. (2026) | 0:40 |
| 24 | O que o MFM mostra (leitura crítica) | | 0:40 |
| 25 | Mapas e áreas críticas | | 0:50 |
| 26 | Limitações e conclusão | | 1:30 |
| 27 | Agradecimentos | | 0:30 |
| 28 | Uso de IA (opcional; se não couber, falar em uma frase nos agradecimentos ou deixar oculto) | | 0:30 |

Soma ≈ 18 min com a introdução (≈ 4:30). Cortes se estourar: juntar 12+13 e 23+24; o slide de classes de uso/solo já está fora.

## Números do evento 11 (Apêndice A do TCC, conferidos)
R 74,0 mm; RI 11,8 mm/h; RI/R 0,159 por hora; chuva nos pixels 63,2 a 79,0 mm (média 73,5); pixel exemplo (lavoura temporária sobre Argissolo): P = 75,4 mm, CN-II 81,0, CN-I 64,2, S0,20 141,9 mm, S0,05 244,2 mm, abstração inicial 12,2 mm, **Q = 13,0 mm**, pr = 5,17 x 10^-4 m³/s, K 0,0351, C 0,212, LS 4,869, **E_unit = 1,167**, sedimento do pixel 40,1 kg. Bacia: escoamento médio 7,2 mm; volume SCS-CN 997 mil m³ contra medido direto 1.479 mil m³ (f = 1,48). **MC:** soma de E = 40.885; c = 0,0344; 1.406 t no ajuste e 1.383 t na validação cruzada (-24%). **MFM:** soma de E = 63.451 (1,55 vez); c = 0,0222; 1.410 t e 1.387 t (-24%). Medido 1.822 t.

## Explicações dos três parênteses (para a fala)
1. **CN-I e λ = 0,05:** combinação escolhida porque aproxima o volume total dos 17 eventos (+3%), com apoio da literatura (Brandão et al., 2025) e conversão de Woodward. Não dizer "calibrado com base naquela pesquisa". Limitação: a escolha foi feita sobre os mesmos eventos da avaliação.
2. **Pico local (Hao et al., 2022):** pr = (Q/1000)*A*(RI/R)/3600. Não há hidrograma no pixel; espalha-se o volume do pixel conforme a concentração da chuva. RI/R é um número por evento, logo pr é proporcional a Q: o pico local não traz informação espacial além do escoamento (dá peso a eventos de chuva concentrada; E cresce com Q^1,12). Dizer isso antes de perguntarem. Nos eventos 1 e 12, RI/R passa de 1.
3. **Coeficiente c:** a equação de Williams foi ajustada para bacias inteiras (m³ e m³/s) e aqui é aplicada a pixels de 897 m² com escoamento em mm; E é um índice, não toneladas. Se somássemos E como toneladas, o evento 11 daria 40.885 t, 22 vezes o medido (1.822 t). c converte o índice em toneladas (0,0344 MC; 0,0222 MFM) e faz o papel de uma conectividade média. Usar **c minúsculo** (coeficiente de escala) e **C maiúsculo** (cobertura) e avisar na fala.

## Sobre K e C na fala (atenção)
O texto atual do TCC diz só que K e C foram **adotados de Vivarelli et al. (2025)** e não foram recalibrados; as Tabelas 5 e 6 usam "com base em". Não afirmar em slide que "o TCC diz que não foram confirmados" (essa frase saiu do texto). Se a banca perguntar a origem de C do campo (0,050), da lavoura (0,212) e do K do Cambissolo (0,0475): foram adotados da IC e não foram recalibrados nem revalidados aqui. O artefato do deck ainda tem frases antigas de "fontes não confirmadas" nos slides de limitações e classes (corrigir se for reutilizado).

## Pendências para a próxima sessão
1. Painéis do evento 11 em arquivos separados e grandes (chuva IDW, retenção S, escoamento Q, E_unit, sedimento) para os slides 13, 14, 17 e 19.
2. Gráfico do evento 11 (vazão e chuva no tempo), se a série horária estiver disponível.
3. Mapa da bacia para projeção (letras maiores).
4. Texto curto e fala dos slides 11 a 19, depois 20 a 28.
5. Atualizar o artefato conforme a nova estrutura (ou abandoná-lo, já que o autor monta no PowerPoint).
6. Conferir a frase do slide 10 com a seção 1.3.1 do TCC.

* Os scripts em Scripts/mapa_bacia_jundiai/ foram escritos com o caminho de uma pasta temporária (variável D) e precisam dessa pasta ajustada; os dados vêm de: tiles https://s3.amazonaws.com/elevation-tiles-prod/geotiff/10/{x}/{y}.tif (x 376 a 380, y 578 a 581) e malha municipal do IBGE (API servicodados.ibge.gov.br/api/v3/malhas/estados/35, intrarregiao=municipio).
