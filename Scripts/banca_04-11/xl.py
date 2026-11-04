import openpyxl, datetime as dt
p="tcc_b/Dados Iniciais/Dados_finais_histereses_corrigido.xlsx"
wb=openpyxl.load_workbook(p,read_only=True,data_only=True)
for ws in wb.worksheets:
    print(ws.title,ws.max_row,ws.max_column)
    for i,row in enumerate(ws.iter_rows(values_only=True)):
        if i<4: print(row[:16])
        else: break
