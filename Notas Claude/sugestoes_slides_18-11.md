# Sugestões para a apresentação (versão de 18/11, 11h)

Arquivo com as sugestões aplicadas: `Apresentacao/slideTCC_18-11_sugestoes.pptx` (gerado por `Scripts/slides_defesa/4_slides_no_modelo_do_autor.py` a partir de `Apresentacao/slideTCC_18-11.pptx`).
Os slides 1 a 19 do autor não foram alterados; foram acrescentados o slide de solo e uso (novo 9) e os slides 20 em diante, no layout "Título e Conteúdo" do modelo FECFAU. A fala de cada slide novo está nas anotações.

## O que foi acrescentado

| Nº no arquivo | Slide | Tempo sugerido |
|---|---|---|
| 9 | Introdução: solo e uso (pedido do orientador) | 0:30 |
| 21 | Resultados: modelo calculado (MC) | 0:45 |
| 22 | Resultados: o erro vem do escoamento (barras medido × calculado) | 0:50 |
| 23 | Resultados: modelo forçado ao medido (MFM) | 0:30 |
| 24 | Resultados: com o escoamento medido | 0:40 |
| 25 | Resultados: métricas de desempenho | 0:50 |
| 26 | Resultados: comparação dos modelos (tabela) | 0:30 |
| 27 | Resultados: áreas críticas | 0:40 |
| 28 | Resultados: sedimento por evento (17 mapas) | 0:20 |
| 29 | Resultados: sedimento médio | 0:20 |
| 30 | Conclusões (com o mapa de áreas críticas) | 0:50 |
| 31 | Limitações: de onde vem o erro | 0:50 |
| 32 | Limitações: o que falta validar | 0:40 |
| 33 | Agradecimentos | 0:20 |
| 34 | Uso de IA (opcional) | 0:15 |
| 35–36 | Apoio: histerese; critério de calibração | só se perguntarem |

Soma de 21 a 34: cerca de 8:50. Com 1 a 20 (cerca de 11:30 + 0:30 do slide 9), fica em cerca de 20:50: **passa um pouco dos 20 min**. Onde cortar, se precisar: falar o 23 (MFM) em uma frase junto do 24; passar rápido pelo 26 (a tabela repete o 24 e o 25) ou levá-lo para o apoio; IA em uma frase nos agradecimentos.

## Sugestões nos slides 1 a 19 (não aplicadas; para você decidir)

1. **Fonte (todos os slides do 11 em diante):** o tema do arquivo usa Aptos, e os slides colados do deck de referência ficaram em Aptos. No arquivo de sugestões, a fonte do tema foi trocada para Calibri (Design > Variantes > Fontes > Office/Calibri faz o mesmo no seu arquivo).
2. **Slide 12:** trocar o hidrograma pela versão nova (`TCC_Texto/figuras/slides/ev11_hidrograma.png`), que marca "início do evento" e "fim do evento". Vale perguntar ao Luis sobre a chuva antes da janela (12 a 14 mm em cada posto, de 3h a 11h de 04/07).
3. **Slide 13:** Shepard (1968) **está** nas referências do TCC (seção 2.7); a pendência anotada em 18/11 pode ser desconsiderada.
4. **Slide 15:** acrescentar Chow, Maidment e Mays (1988) no rodapé (o CN-I vem dessa fórmula; Woodward converte só o λ) e escrever "condição seca (Chow)" na caixa do CN-I.
5. **Slide 16:** deixar as unidades explícitas nas caixas: "0,013 m × 897 m²" e "11,8 mm/h ÷ 74,0 mm" (o 11,8 aparece de novo no slide 17 como constante de Williams).
6. **Slide 18:** (pendência de 18/11) mostrar o c = 0,0344 em destaque, não só no rodapé; e alinhar com o texto do TCC: "faz o papel de uma taxa de transferência de sedimentos média da bacia; por ser calibrado, também absorve a diferença de escala e parte do erro do escoamento". O termo "(conectividade)" pode sair.
7. **Slide 19:** (pendência de 18/11) acrescentar na fala que minimizar a soma dos quadrados em log equivale a maximizar o NSE em log, a função objetivo de Hao et al. (2022), e que o evento 15 responde por 48,7% da variabilidade da carga medida (por isso o log).
8. **Slide 4:** a equação usa "q_p" e o texto "Qp"; usar a mesma grafia.

## Ponto de atenção para a defesa
A análise de sensibilidade de 18/11 mostra que "o MC é pior que a regra com a chuva" depende do critério de calibração (log: 81% contra 42%; linear: 45% contra 39%). O slide 21 mantém o resultado do TCC (critério em log); o slide de apoio "o critério de calibração" tem a tabela e a resposta pronta. O que não depende do critério: o MC tem erro alto (40 a 80%) e o MFM fica em cerca de 20%.
