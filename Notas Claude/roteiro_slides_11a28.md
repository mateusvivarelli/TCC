# Roteiro dos slides 11 a 28 da defesa (14/11/2026)

Base: `Notas Claude/plano_slides_defesa_14-11.md` e o texto final do TCC (números conferidos com o Apêndice A e a Tabela 13).
Arquivo pronto: `TCC_Texto/slides/slides_11a28_defesa.pptx` (19 slides: 11 a 28 + 1 de apoio; a fala de cada slide está nas **anotações do apresentador**).
Figuras novas: `TCC_Texto/figuras/slides/` (gerar de novo: `python Scripts/slides_defesa/1_figuras_slides.py`; montar o pptx: `node Scripts/slides_defesa/2_monta_slides.js`).

## Linha da história
1. **Método pelo evento 11 (slides 11 a 19):** um único evento, do dado ao sedimento, com o mesmo pixel de exemplo do Apêndice A. Os dois "parênteses" explicam as escolhas que a banca vai perguntar.
2. **Resultados com os 17 eventos (20 a 25):** o MC erra muito → o erro vem do escoamento → o MFM isola isso → comparação com a regra do volume e com o concentrado → leitura crítica → mapa.
3. **Fecho (26 a 28):** conclusões, limitações e próximos passos; agradecimentos; uso de IA.

## Mudança de ordem sugerida
No plano, "Resultados: escoamento e sedimento" era o 23, depois do MFM. Passei para logo depois do resultado do MC (slide 21): primeiro se mostra que o MC erra, depois **por que** (o escoamento), e só então o MFM, que testa essa explicação. A nova ordem é 20 MC → 21 escoamento → 22 MFM → 23 comparação → 24 leitura crítica. Se preferir a ordem original, é só arrastar o slide.

## Slide a slide

| # | Título | O que aparece | Mensagem (uma frase) | Tempo |
|---|---|---|---|---|
| 11 | Dados: 17 eventos monitorados e mapas de 30 m | 4 linhas (chuva, vazão, sedimento, carga) + caixa "Dados espaciais" (MDE do USGS; solo e uso do Consórcio Profill-Rhama, 2020; CN BR_CN-2022 da Agência Nacional de Águas e Saneamento Básico, 2024) + gráfico da carga medida por evento, evento 11 em laranja | De onde vêm os dados medidos e os mapas | 1:00 |
| 12 | Evento 11: 4 a 8 de julho de 2019 | Hietograma, hidrograma com escoamento direto e CSS + 4 números (74,0 mm; 11,8 mm/h; 1.479 mil m³; 1.822 t) | É esse valor (1.822 t) que o modelo tenta reproduzir | 0:25 |
| 13 | Passo 1: chuva em cada pixel (IDW) | Mapa da chuva + fórmula do IDW + 62,8 / 79,0 mm; pixel com 75,4 mm | Com 2 postos, a chuva é um gradiente suave | 0:25 |
| 14 | Passo 2: escoamento direto em cada pixel (SCS-CN) | Mapa do escoamento + conta do pixel (Q = 13,0 mm) + volume 997 contra 1.479 mil m³ | O SCS-CN dá 67% do volume medido neste evento | 0:45 |
| 15 | Parêntese 1: condição seca (CN-I) e λ = 0,05 | Cadeia CN-II 81,0 → CN-I 64,2 → S0,20 141,9 → S0,05 244,2 → Ia 12,2 mm + mapa de S + 4 motivos | Escolha que acerta o volume total (+3%), com apoio na literatura, feita sobre os mesmos eventos | 0:50 |
| 16 | Passo 3: vazão de pico local (Hao et al., 2022) | Fórmula + 3 caixas (11,67 m³; 0,159/h; 5,17 × 10⁻⁴ m³/s) + 4 pontos | O pico local é proporcional a Q: não traz informação espacial nova (dizer antes que perguntem) | 0:50 |
| 17 | Passo 4: erosão local em cada pixel (Williams, 1975) | Mapa do índice (sem escala em kg, de propósito) + conta do pixel (1,167) + K, LS, C | E é um índice relativo, não tonelada | 0:40 |
| 18 | Parêntese 2: o coeficiente c | 40.885 contra 1.822 t; fórmula SY = c × ΣE; mapa do sedimento | c converte o índice em toneladas (0,0344) e faz o papel de uma conectividade média; c minúsculo ≠ C maiúsculo | 1:10 |
| 19 | Calibração e validação cruzada (leave-one-out) | Fórmula da média geométrica + 17 quadradinhos com o 11 retirado + 1.406 / 1.383 t (−24%) | Só o c é calibrado; as métricas tendem a ser um pouco otimistas | 0:50 |
| 20 | Modelo calculado: pior que a regra simples com a chuva | Dispersões (regra simples e MC) + 81% × 42% e 35% × 82% | Com a mesma informação, o MC erra mais (14 de 17 eventos; p = 0,02) | 0:50 |
| 21 | O erro vem do escoamento calculado | Dispersão do volume (Fig. 5) + 46% e 91% + Baert et al. (2026) | O erro do escoamento explica 91% do erro do sedimento | 0:40 |
| 22 | Modelo forçado ao medido (MFM): troca só o escoamento | Fluxo com a etapa trocada em destaque + f = 1,48; 1,55 ×; 1.387 t | MFM não é previsão; serve para isolar o escoamento | 0:40 |
| 23 | Com o escoamento medido, o erro cai de 81% para 21% | Figura 10 + 2 cartões (regra com o volume: 16%, não se distingue; concentrado: 22%, comparação indicativa) | O escoamento é o gargalo; o MFM empata com a regra do volume | 0:50 |
| 24 | O que o MFM mostra: o peso do volume medido | Figura 11 + 88% e 0,66 × 0,08 | Quem recebe o volume medido acerta a carga por construção; não valida a fórmula | 0:40 |
| 25 | Mapa de erosão média e áreas críticas | Mapa médio e áreas críticas do MC + 46% → 83%, 93%, 65% → 78%, 94% + 3 ressalvas | O que a espacialização acrescenta: onde a erosão é produzida | 0:50 |
| 26 | Conclusões e limitações | 4 conclusões + caixa de limitações + caixa de próximos passos | As 4 conclusões do TCC, em ordem | 1:30 |
| 27 | Agradecimentos | Nomes e papéis + "Obrigado!" | | 0:30 |
| 28 | Uso de inteligência artificial (opcional) | 3 cartões (programação, texto, figuras) + frase de responsabilidade | Ajustar ao que realmente foi feito; pode ficar oculto | 0:30 |
| apoio | Desempenho de todos os modelos | Tabela 13 completa | Para responder perguntas | — |

Soma dos slides 11 a 28: cerca de 14 min; com a introdução (cerca de 4:30), cerca de 18:30 dos 20 min.
Se estourar: juntar 12 e 13; juntar 21 e 24; falar o 28 em uma frase.

## Fontes dos rasters nos rodapés
* Slide 11: todas (monitoramento e rasters).
* Slides 14 e 15: CN do raster BR_CN-2022 (Agência Nacional de Águas e Saneamento Básico, 2024).
* Slide 17: K e C dos mapas do Consórcio Profill-Rhama (2020), com valores de Vivarelli et al. (2025); LS do MDE de 30 m do USGS (Moore e Burch, 1986).
* Slide 25: todas as fontes dos fatores.

## Cuidados na fala (do plano, ainda valem)
* K e C: "adotados de Vivarelli et al. (2025), não recalibrados aqui". Não dizer que "não foram confirmados".
* CN-I e λ = 0,05: "escolhidos porque aproximam o volume total, com apoio de Brandão et al. (2025)". Não dizer "calibrado com base naquela pesquisa".
* MFM: "não é previsão"; o bom desempenho vem do volume medido.
* Concentrado: "comparação indicativa", porque foi ajustado nos próprios eventos, sem validação cruzada.
* No slide do índice E (17), o mapa está sem a escala em kg de propósito: a figura original rotula o índice como "kg por pixel, sem calibrar", o que contradiz a fala de que E não é tonelada.

## Para conferir antes de usar
* Slide 27: falta o e-mail de contato (`[e-mail de contato]`).
* Slide 28: o texto é um rascunho; confirme se corresponde ao que você fez e se a FECFAU pede esse slide.
* A faixa azul com o nome da seção imita o seu modelo; ao colar no seu PowerPoint, use a faixa do modelo e apague a etiqueta.
* Os números dos eixos do gráfico do slide 11 aparecem com o separador do idioma do PowerPoint (em português, 4.500).
