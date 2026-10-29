| Etapa | Grandeza | Valor |
|---|---|---|
| Chuva medida | DBT5 / Campo Limpo | 62,8 mm / 79,0 mm |
|  | lâmina do evento R = 0,307 * P1 + 0,693 * P2 | 74,0 mm |
|  | intensidade máxima RI; razão RI/R | 11,8 mm/h; 0,159 por hora |
| Chuva do pixel (IDW) | média nos pixels de cálculo (intervalo no raster) | 73,5 mm (63,2 a 79,0 mm) |
| Retenção | CN-I médio; S0,20 médio; S0,05 médio (convertido) | 52,5; 255,7 mm; 489,9 mm |
| Escoamento direto | Q médio dos pixels; pixels sem escoamento | 7,2 mm; 0% |
|  | volume calculado pelo SCS-CN / medido | 997 mil m³ / 1.479 mil m³ (razão 0,67) |
| Pixel de exemplo | posição; uso; solo | E 330,18 km; N 7.432,86 km; lavoura temporária; Argissolos Vermelho-Amarelos |
|  | chuva P; CN-II -> CN-I; S0,20 -> S0,05 | 75,4 mm; 81,0 -> 64,2; 141,9 mm -> 244,2 mm |
|  | abstração inicial λS; escoamento Q | 12,2 mm; (75,4 - 12,2)² / (75,4 + 0,95 * 244,2) = 13,00 mm |
|  | vazão de pico local pr | 13,00/1000 * 897,49 * 0,159 / 3600 = 5,17 * 10^-4 m³/s |
|  | K; C; LS | 0,0351; 0,212; 4,869 |
|  | índice de erosão E_unit | 11,8 * (13,00 * 5,17 * 10^-4 * 897,49)^0,56 * 0,0351 * 0,212 * 4,869 = 1,167 |
|  | sedimento do pixel c * E_unit | 0,0344 * 1,167 = 0,0401 t (40,1 kg) |
| Evento (MC) | soma de E_unit sobre os pixels | 40.885 |
|  | sedimento simulado SY = c * soma(E_unit) (ajuste) | 0,0344 * 40.885 = 1.406 t (-23%) |
|  | validação cruzada (c refeito sem o evento 11) | 1.383 t (-24%) |
| Evento (MFM) | soma de E_unit com o escoamento forçado ao medido | 63.451 |
|  | sedimento simulado (ajuste, c = 0,0222); validação cruzada | 1.410 t (-23%); 1.387 t (-24%) |
| Medido | SY_obs = soma(Q * CSS) | 1.822 t |
