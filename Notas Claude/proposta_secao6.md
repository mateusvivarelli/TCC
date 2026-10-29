# Proposta de texto: seção 6 (Conclusões), modelo oficial

Escrita na noite de 29/10/2026 (sessão na nuvem, sem acesso ao usuário). **Nada foi aplicado no Google Doc.** Os números são os da proposta da seção 5 (`proposta_secao5.md`). Cada conclusão indica, entre colchetes, o objetivo específico da seção 1.3.2 a que responde (texto dos objetivos tirado de `doc_texto_completo_29-10.md`); os colchetes não vão para o Doc.

---

## Texto proposto

# 6. CONCLUSÕES

1. A MUSLE foi espacializada pixel a pixel nos 17 eventos, com o escoamento direto do SCS-CN e a vazão de pico local de cada pixel, numa rotina em Python que lê os dados e gera os mapas e as métricas de forma automática. [objetivos 1 e 2]

2. O SCS-CN, com o CN-I e λ = 0,05 com a retenção convertida, acerta o volume total de escoamento direto dos 17 eventos (viés de +2,9%), mas não o de cada evento: o erro mediano por evento é de 46% e o NSE do volume é negativo (-0,39), porque a fração da chuva que escoa nesta bacia não cresce com a chuva, como a curva do método supõe. [objetivo 5]

3. Só com a chuva, o modelo espacializado (MC) teve desempenho pior que uma regra simples proporcional à chuva do evento (erro mediano de 81% contra 42%; 35% contra 82% dos eventos dentro de fator 2, na validação cruzada). O erro do sedimento é quase todo herdado do erro da água (91% da variância). [objetivos 3 e 4]

4. O fator que mais limita a estimativa é a conversão da chuva em escoamento, e não a fórmula de erosão: com o escoamento direto medido (MFM), o mesmo modelo passa a erro mediano de 21% e 94% dos eventos dentro de fator 2 (NSE em log de 0,84). [objetivo 5]

5. Com informação equivalente, a espacialização não custa precisão: o MFM não se distingue da regra simples com o escoamento direto medido (erro mediano de 16%) nem da formulação concentrada da IC refeita (16%; 100% dentro de fator 2), e acrescenta o mapa de onde o sedimento é produzido. [objetivos 3 e 4]

6. As áreas críticas, os 5% de pixels de maior contribuição, ficam nas mesmas manchas da porção central e oeste da bacia nos dois modelos (94% de coincidência). Campo, silvicultura e lavoura temporária, com 46% da área, respondem por 83% do sedimento estimado, e a lavoura temporária e o solo exposto produzem, por unidade de área, cerca de 5 e 18 vezes a média da bacia. Esses números são relativos: dependem dos valores de K e C adotados e não foram validados no espaço. [objetivo 6]

**Trabalhos futuros.** Os resultados indicam que o ganho maior está na água: usar a vazão medida onde houver posto, ou melhorar a chuva (mais postos, radar ou satélite) antes de refinar a fórmula de erosão. Com a água medida, o que resta é a variação da carga de sedimento por m³ de escoamento entre os eventos, que pede rever a curva turbidez-CSS e os dados de 2019/20, em especial o evento 17. A validação do mapa exige medir sedimento em sub-bacias ou mapear feições erosivas em campo, e os valores de K e C por classe devem ser conferidos com medidas locais.

---

## Notas para o usuário (não vão para o Doc)

- **Contas da conclusão 6:** área de campo + silvicultura + lavoura temporária = 29,0 + 12,7 + 3,9 = 45,6% (arredondado para 46%); sedimento (MC) = 37,4 + 24,2 + 20,9 = 82,5% (arredondado para 83%). Fonte: `tab_classes_uso.md`. No MFM: 37,4 + 23,0 + 20,0 = 80,4%. Se preferir um número só, escreva "cerca de 80%".
- **Conclusão 1** fala em "rotina em Python": o objetivo diz "Python/SIG". A rotina principal é `Scripts/calcular_sy_lambda005_woodward.py` (Python com GDAL); o SIG (QGIS) entrou na preparação dos rasters. Ajustar a frase se o usuário quiser citar o QGIS.
- **O que mudou em relação às conclusões atuais do Doc:** saem a conclusão sobre "volume e carga incluem a vazão de base" (já está na 3.2 como dado), a do "modelo de dois componentes" e os números antigos (33%, 71%, 14%). A conclusão 3 inverte a mensagem antiga: o MC agora fica **abaixo** da regra da chuva.
- **Sem promessas além dos dados:** não escrevi que o modelo serve para prever sedimento sem dados de vazão; pelo resultado, não serve melhor que a regra da chuva.
- Nome dos modelos (MC/MFM): decisão pendente.
