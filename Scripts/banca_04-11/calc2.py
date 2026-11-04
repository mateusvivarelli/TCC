import numpy as np, openpyxl, datetime as dt
exec(open('calc1.py',encoding='utf8').read().split("print('== metricas')")[0])
print('== proxy sem raster')
for nm,S,X in [('MFM',MFa,Vd**1.12*(RI/R)**.56),('MC',MCa,Vs**1.12*(RI/R)**.56)]:
    x=np.log(X);y=np.log(S);b,a=np.polyfit(x,y,1);r=c(x,y);res=y-(a+b*x)
    print(nm,'r ln',round(r,4),'r2',round(r*r,4),'b',round(b,3),'res sd',round(float(res.std()),3),'fator max',round(float(np.exp(abs(res).max())),2))
    print('  evento pior',int(ev[abs(res).argmax()]))
x=loo(Vs**1.12*(RI/R)**.56);met(x,'proxy MC c*Vs^1.12*(RI/R)^.56');met(loo(Vd**1.12*(RI/R)**.56),'proxy MFM')
print('razao proxy/MFM ajuste, min max',np.round(np.sort(loo(Vd**1.12*(RI/R)**.56)/MF)[[0,-1]],2))
res=np.log(MF/O)
print('tendencia sem ev17: r',round(c(res[:16],ev[:16]),2),' t com17',round(c(res,ev)*np.sqrt(15)/np.sqrt(1-c(res,ev)**2),2))
print('CP 12/17',cp(12,17))
def fz(r,n=17):
    z=np.arctanh(r);s=np.sqrt(1.06/(n-3));return np.round(np.tanh([z-1.96*s,z+1.96*s]),2)
for nm,r in [('MC',.59),('chuva',.63),('MFM',.83),('cVd',.90),('IC',.93)]: print('Spearman IC',nm,r,fz(r))

print('== planilha')
wb=openpyxl.load_workbook('tcc_b/Dados Iniciais/Dados_finais_histereses_corrigido.xlsx',read_only=True,data_only=True)
rows=[r[:8] for r in wb.worksheets[0].iter_rows(min_row=2,values_only=True) if isinstance(r[0],dt.datetime)]
t=[r[0] for r in rows]
f=lambda j:np.array([np.nan if (r[j] is None or isinstance(r[j],str)) else float(r[j]) for r in rows])
P1,P2,PT,Q,CSS,Bt=f(1),f(2),f(3),f(4),f(5),f(6)
print('linhas',len(t),t[0],t[-1])
okq=~np.isnan(Q);okc=~np.isnan(CSS);print('Q valido',okq.sum(),t[np.where(okq)[0][0]],t[np.where(okq)[0][-1]],'CSS valido',okc.sum(),'ambos',(okq&okc).sum())
W=[("22/11/18 09","23/11/18 23"),("30/11/18 22","03/12/18 04"),("17/12/18 22","20/12/18 22"),("24/12/18 06","26/12/18 23"),("04/01/19 19","08/01/19 17"),("16/01/19 12","17/01/19 13"),("25/01/19 00","28/01/19 10"),("15/02/19 13","20/02/19 05"),("25/02/19 15","01/03/19 13"),("17/03/19 05","19/03/19 16"),("04/07/19 12","08/07/19 07"),("30/12/19 09","31/12/19 08"),("02/01/20 11","04/01/20 17"),("07/01/20 18","10/01/20 19"),("02/02/20 20","09/02/20 01"),("09/02/20 14","13/02/20 21"),("20/02/20 09","22/02/20 10")]
pd=lambda s:dt.datetime.strptime(s,"%d/%m/%y %H")
W=[(pd(a),pd(b)) for a,b in W]
T=np.array(t,dtype='datetime64[h]')
inw=np.zeros(len(t),bool);lo=[]
for a,b in W:
    m=(T>=np.datetime64(a,'h'))&(T<=np.datetime64(b,'h'));inw|=m
    L=np.nansum(Q[m]*CSS[m]*3.6/1000);lo.append(L)
print('confere carga eventos (t) soma',round(sum(lo)),'ev15',round(lo[14]),'ev17',round(lo[16]))
both=okq&okc;L=Q*CSS*3.6/1000
per=(T>=np.datetime64(W[0][0],'h'))&(T<=np.datetime64(W[-1][1],'h'))
print('periodo 1o a ultimo evento: horas',per.sum(),'validas Q&CSS',(per&both).sum(),'% ev das horas',round(100*(inw&per).sum()/per.sum(),1))
print('carga periodo t',round(np.nansum(L[per&both])),'em eventos',round(np.nansum(L[inw&both])),'% ',round(100*np.nansum(L[inw&both])/np.nansum(L[per&both]),1))
print('volume % em eventos',round(100*np.nansum(Q[inw&okq])/np.nansum(Q[per&okq]),1),'chuva CL % em eventos',round(100*np.nansum(P2[inw])/np.nansum(P2[per]),1),'chuva DBT5 %',round(100*np.nansum(P1[inw])/np.nansum(P1[per]),1))
print('carga em toda a serie valida t',round(np.nansum(L[both])))
# picos fora das janelas
idx=np.where(okq&(Q>=10)&~inw)[0]
grp=[]
for i in idx:
    if grp and (T[i]-T[grp[-1][-1]])<=np.timedelta64(24,'h'): grp[-1].append(i)
    else: grp.append([i])
print('agrupamentos Q>=10 fora das janelas:',len(grp))
for g in grp:
    k=g[int(np.nanargmax(Q[g]))]
    pr=np.nansum(P2[max(0,g[0]-48):g[-1]+1]);pr1=np.nansum(P1[max(0,g[0]-48):g[-1]+1])
    print(' ',t[g[0]],'->',t[g[-1]],'pico',round(float(Q[k]),2),'em',t[k],'CSS validos',int(okc[g].sum()),'/',len(g),'P48h CL',round(float(pr),1),'DBT5',round(float(pr1),1),'carga t',round(float(np.nansum(L[g]))))
a=np.datetime64('2018-11-24T00','h');b=np.datetime64('2018-11-25T12','h');m=(T>=a)&(T<=b)
print('24/11/18 Qmax',np.nanmax(Q[m]),'em',t[np.where(m)[0][int(np.nanargmax(Q[m]))]])
# postos
print('== postos, soma no periodo: DBT5',round(np.nansum(P1[per])),'CL',round(np.nansum(P2[per])),'razao',round(np.nansum(P1[per])/np.nansum(P2[per]),2))
print('fora de eventos: DBT5',round(np.nansum(P1[per&~inw])),'CL',round(np.nansum(P2[per&~inw])))
d0=np.array([x.astype('datetime64[D]') for x in T])
# razao mensal
ym=np.array([(x.year,x.month) for x in t]);
for y,mo in sorted(set(map(tuple,ym[per]))):
    k=(ym[:,0]==y)&(ym[:,1]==mo)&per
    print(' ',y,mo,'DBT5',round(np.nansum(P1[k])),'CL',round(np.nansum(P2[k])),'horas NaN DBT5',int(np.isnan(P1[k]).sum()),'CL',int(np.isnan(P2[k]).sum()))
# antecedente 5 dias
print('== P5d e Bt inicial')
for i,(a,b) in enumerate(W):
    s=np.where(T==np.datetime64(a,'h'))[0][0];k=range(max(0,s-120),s)
    print(i+1,'P5 CL',round(float(np.nansum(P2[list(k)])),1),'P5 DBT5',round(float(np.nansum(P1[list(k)])),1),'Q0',round(float(Q[s]),2),'CSSmax',round(float(np.nanmax(CSS[(T>=np.datetime64(a,'h'))&(T<=np.datetime64(b,'h'))])),0))
print('CSS max serie',round(float(np.nanmax(CSS)),0),'p50',round(float(np.nanmedian(CSS)),0),'p99',round(float(np.nanpercentile(CSS,99)),0))
