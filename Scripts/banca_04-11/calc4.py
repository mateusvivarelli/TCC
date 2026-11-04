import numpy as np, openpyxl, datetime as dt
wb=openpyxl.load_workbook('tcc_b/Dados Iniciais/Dados_finais_histereses_corrigido.xlsx',read_only=True,data_only=True)
rows=[r[:8] for r in wb.worksheets[0].iter_rows(min_row=2,values_only=True) if isinstance(r[0],dt.datetime)]
f=lambda j:np.array([np.nan if (r[j] is None or isinstance(r[j],str)) else float(r[j]) for r in rows])
Q,C=f(4),f(5);T=np.array([r[0] for r in rows],dtype='datetime64[h]')
per=(T>=np.datetime64('2018-11-22T09'))&(T<=np.datetime64('2020-02-22T10'))&~np.isnan(Q)&~np.isnan(C)
L=Q*C*3.6/1000
for th in (267,1000):
    m=per&(C>=th);print('CSS>=',th,'horas %',round(100*m.sum()/per.sum(),1),'carga %',round(100*L[m].sum()/L[per].sum(),1))
