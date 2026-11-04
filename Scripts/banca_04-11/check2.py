import openpyxl,sys
for f in ["Dados Iniciais/Dados_finais_histereses_corrigido.xlsx","Dados Iniciais/serie_Q_Qb_Qquick_Eckhardt_orientador.xlsx","Dados Iniciais/eventos_processados_manuais.xlsx","Dados Iniciais/eventos_definidos_artigo_I4SDWI_corrigido.xlsx"]:
    wb=openpyxl.load_workbook(f,read_only=True,data_only=True)
    print("==",f)
    for ws in wb.worksheets:
        print(" sheet",ws.title,ws.max_row,ws.max_column)
        for i,row in enumerate(ws.iter_rows(values_only=True)):
            if i>3:break
            print("  ",row[:14])
