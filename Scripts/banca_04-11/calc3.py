import numpy as np, openpyxl, datetime as dt, collections
exec(open('calc1.py',encoding='utf8').read().split("print('== metricas')")[0])
P5=np.array([40.8,23.0,24.2,90.6,26.2,14.0,33.4,32.6,21.8,32.8,14.0,0.0,39.8,66.2,31.0,96.8,10.0])
Q0=np.array([1.28,1.87,1.62,2.44,3.72,1.79,1.33,1.6,1.84,3.71,1.87,.99,1.21,2.34,1.9,2.71,2.03])
print('Sp ln(O/Vd) x P5',round(c(rk(O/Vd),rk(P5)),2),'Sp ln(O/TR) x P5',round(c(rk(O/TR),rk(P5)),2),'sem ev17',round(c(rk((O/TR)[:16]),rk(P5[:16])),2),'Sp erro vol x P5',round(c(rk(Vs/Vd),rk(P5)),2),'Sp coef esc x P5',round(c(rk(Vd/R),rk(P5)),2))
print('Sp Vd/R x Q0',round(c(rk(Vd/R),rk(Q0)),2))
print('AMC NEH4 cresc (<35.6 I; >53.3 III) P5 CL:',(P5<35.6).sum(),((P5>=35.6)&(P5<=53.3)).sum(),(P5>53.3).sum(),'ev III',ev[P5>53.3])
print('T para CSS 4227 pela potencia',round((4227/3.264)**(1/.7974)),' CSS em 250 NTU',round(3.264*250**.7974))
wb=openpyxl.load_workbook('tcc_b/Dados Iniciais/Dados_finais_histereses_corrigido.xlsx',read_only=True,data_only=True)
rows=[r[:8] for r in wb.worksheets[0].iter_rows(min_row=2,values_only=True) if isinstance(r[0],dt.datetime)]
t=[r[0] for r in rows]
f=lambda j:np.array([np.nan if (r[j] is None or isinstance(r[j],str)) else float(r[j]) for r in rows])
P1,P2,Q,CSS=f(1),f(2),f(4),f(5)
ym=collections.OrderedDict()
for i,x in enumerate(t):
    k=(x.year,x.month)
    if k>=(2020,1): ym.setdefault(k,[0,0,0,0]);ym[k][0]+=np.nan_to_num(P1[i]);ym[k][1]+=np.nan_to_num(P2[i]);ym[k][2]+=np.isnan(P1[i]);ym[k][3]=max(ym[k][3],np.nan_to_num(Q[i]))
for k,v in ym.items(): print(k,'DBT5',round(v[0]),'CL',round(v[1]),'NaN1',int(v[2]),'Qmax',round(v[3],1))
print('valores distintos de CSS',len(set(np.round(CSS[~np.isnan(CSS)],1))),'de',int((~np.isnan(CSS)).sum()))
cn=collections.Counter(np.round(CSS[(~np.isnan(CSS))&(CSS>1000)],0));print('CSS>1000: horas',sum(cn.values()),'distintos',len(cn),'mais comuns',cn.most_common(6))
print('horas CSS>=999',int(np.nansum(CSS>=1000)),'horas >1000 em ev: ver acima; CSS em 250 NTU ~',round(3.264*250**.7974))
