====================================================================================================
(1) R² do mapa de erosão média com K*LS*C (pixels com erosão > 0)
MC: pixels 125008 | log: R2(KLSC) = 0.455; R2(G) = 0.712; R2 total = 1.000 | partição: fatores fixos 37.1%, escoamento 62.9% | linear: R2(M, KLSC) = 0.577 (Pearson 0.760)
MFM: pixels 125008 | log: R2(KLSC) = 0.424; R2(G) = 0.744; R2 total = 1.000 | partição: fatores fixos 34.0%, escoamento 66.0% | linear: R2(M, KLSC) = 0.563 (Pearson 0.750)
====================================================================================================
(2) Contribuição por classe de declividade (Tabela 16)
pixels com erosão e declividade: 153855 (conferir contra 153.855)
Declividade (%)  Área (%)  Erosão MC (%)  Erosão MFM (%)
          0 a 3       0.6            0.0             0.0
          3 a 8       4.0            0.7             0.8
         8 a 20      30.4           20.9            22.0
        20 a 45      55.2           63.9            63.5
        45 a 75       9.4           13.9            13.2
      75 a mais       0.4            0.5             0.5

pixels críticos (MC, >= percentil 95 = 60.7 kg): 7693
uso                 solo                          decl 
Lavoura Temporária  Cambissolos Háplicos          20-45    26.7
Silvicultura        Cambissolos Háplicos          20-45    19.2
Lavoura Temporária  Cambissolos Háplicos          8-20     13.8
Campo               Cambissolos Háplicos          45-75    10.1
                                                  20-45     8.7
Silvicultura        Cambissolos Háplicos          45-75     7.1
Solo exposto        Cambissolos Háplicos          8-20      4.4
                                                  20-45     2.6
Lavoura Temporária  Argissolos Vermelho-Amarelos  20-45     2.4
Silvicultura        Argissolos Vermelho-Amarelos  45-75     0.8
====================================================================================================
(3) MFM: volume depois do limite Q <= P contra o escoamento direto medido
 Evento  Vdir medido (10³ m³)  V_SCS (10³ m³)    f  V_MFM após limite (10³ m³)  Diferença (%)  Pixels limitados (%)
      1                223.80           35.54 6.30                      206.86          -7.57                  0.19
      2               1731.15          521.00 3.32                     1706.87          -1.40                  0.19
      3                584.93          750.55 0.78                      584.93           0.00                  0.00
      4                987.44          154.47 6.39                      951.23          -3.67                  1.04
      5                832.00          694.67 1.20                      832.00           0.00                  0.00
      6                183.08          158.26 1.16                      183.08           0.00                  0.00
      7                650.39          141.73 4.59                      630.37          -3.08                  0.19
      8               1250.31         1336.33 0.94                     1250.31           0.00                  0.00
      9                800.96         1725.17 0.46                      800.96           0.00                  0.00
     10                552.10           56.65 9.75                      495.11         -10.32                  1.66
     11               1478.95          997.50 1.48                     1474.66          -0.29                  0.19
     12                100.91           62.53 1.61                      100.67          -0.24                  0.07
     13                734.89         1072.54 0.69                      734.89          -0.00                  0.00
     14                931.29         1362.54 0.68                      931.29          -0.00                  0.00
     15               2177.09         3963.44 0.55                     2177.09           0.00                  0.00
     16               1594.65         1934.50 0.82                     1594.65           0.00                  0.00
     17                449.21          734.47 0.61                      449.21           0.00                  0.00
====================================================================================================
(4) Pixels com CN-I < 35 (S0,20 > 471,7 mm)
pixels: 12933 (8.4% dos pixels de cálculo); erosão média MC nesses pixels: 0.1% do total; MFM: 0.1%

---
Notas (02/11/2026): saída bruta do script `Scripts/_analise_mapa_declividade_r2_30-10.py`, rodado no PC com os rasters (QGIS Python). Todos os números são do modelo oficial.
- (1) O R2 em log soma 1,000 por construção: E_unit é o produto exato de K*LS*C e do termo de escoamento (E_unit = 11,8 * (Q*pr*A)^0,56 * K*C*LS, e pr é proporcional a Q), então ln(E_unit) = ln(K*LS*C) + 1,12 ln(Q) + constante. A partição (37% fatores fixos e 63% escoamento no MC; 34% e 66% no MFM) é uma descrição do mapa, não uma validação. Em escala linear, R2 do mapa com K*LS*C = 0,58 (MC) e 0,56 (MFM).
- (2) Declividade: 55% da área está em 20 a 45% e responde por 64% da erosão média; 8 a 20% responde por 21%; acima de 45% (9,8% da área) responde por 14%. Pixels críticos (5% maiores): lavoura temporária e silvicultura sobre Cambissolos Háplicos, declividade de 20 a 45%.
- (3) Limite Q <= P: a maior perda é de 10,3% do volume medido (evento 10) e de 7,6% (evento 1); nos demais eventos afetados é de no máximo 3,7%, e 10 dos 17 eventos não perdem nada. Fator f vai de 0,46 a 9,75.
- (4) Pixels com CN-I < 35: 8,4% dos pixels de cálculo, 0,1% da erosão média: a extrapolação da relação de Woodward quase não afeta o resultado.
