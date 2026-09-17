import pandas as pd
import os

excelPath = r"C:\Users\user\OneDrive\Área de Trabalho\TCC\Dados Iniciais\eventos_processados_manuais.xlsx"
csvFolder = r"C:\Users\user\OneDrive\Área de Trabalho\TCC\Dados Iniciais\ESTPLUV"

for i in range(17): 
    ev = i + 1
    if ev == 1: evIndex = 0
    else: evIndex = ev

    sheet = 'Sheet1'
    ev_1_row = 'chuva_p1_mm'
    ev_2_row = 'chuva_p2_mm'
    flow_row   = 'T_R_m3'

    print(f"Reading Excel for rain event {ev}... \n\n")

    df = pd.read_excel(excelPath, sheet_name=sheet)

    evLine = df.iloc[evIndex]

    rain_pt1 = evLine[ev_1_row]
    rain_pt2 = evLine[ev_2_row]

    data_csv = [
        {'id': 'DBT5',      'lon': -46.4809,   'lat': -23.2646,   'P': rain_pt1},
        {'id': 'Campo_Paulista', 'lon': -46.760284, 'lat': -23.208778, 'P': rain_pt2}
    ]

    df_qgis = pd.DataFrame(data_csv)

    csvName = f"ESTPLUV_{ev}.csv"
    csvPath = os.path.join(csvFolder, csvName)
    df_qgis.to_csv(csvPath, index=False, sep=';', float_format='%.6f', decimal='.')

    print(f"Arquivo CSV gerado com sucesso em:\n{csvPath}\n")

    totalFlow = evLine[flow_row]

    print(f"Volume total observado no campo:\n{totalFlow}\n")
