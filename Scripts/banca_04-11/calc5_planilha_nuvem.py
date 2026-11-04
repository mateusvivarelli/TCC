import openpyxl, numpy as np, datetime as dt, sys
base=sys.argv[1]
wb=openpyxl.load_workbook(base+"/Dados Iniciais/Dados_finais_histereses_corrigido.xlsx",read_only=True,data_only=True)
rows=[r[:8] for r in wb.worksheets[0].iter_rows(min_row=2,values_only=True) if isinstance(r[0],dt.datetime)]
num=lambda v: np.nan if (v is None or isinstance(v,str)) else float(v)
T=np.array([r[0] for r in rows],dtype='datetime64[h]')
P1=np.array([num(r[1]) for r in rows]);P2=np.array([num(r[2]) for r in rows])
Q=np.array([num(r[4]) for r in rows]);C=np.array([num(r[5]) for r in rows]);Bt=np.array([num(r[6]) for r in rows])
wb2=openpyxl.load_workbook(base+"/Dados Iniciais/eventos_processados_manuais.xlsx",read_only=True,data_only=True)
ev=[(r[0],np.datetime64(r[1],'h'),np.datetime64(r[2],'h'),r[4]) for r in list(wb2.worksheets[0].iter_rows(values_only=True))[1:] if r[1] is not None and r[0]!='1B']
print('n eventos',len(ev))
print('CSS max serie',np.nanmax(C),'em',T[np.nanargmax(C)])
# A15 start flow
print('ev Qini Qpico Qini/Qpico Bt_ini Qini-Bt_ini  frac TR da vazao inicial*dur')
TRs=[];Vds=[]
for n,a,b,qp in ev:
    m=(T>=a)&(T<=b)
    q=Q[m];bt=Bt[m]
    TR=np.nansum(q)*3600;Vd=np.nansum(q-bt)*3600
    TRs.append(TR);Vds.append(Vd)
    print(n,round(q[0],2),round(qp,1),round(q[0]/qp,2),round(bt[0],2),round(q[0]-bt[0],2),round(q[0]*3600*len(q)/TR,2), 'TR mil',round(TR/1e3),'Vd mil',round(Vd/1e3))
TRs=np.array(TRs);Vds=np.array(Vds)
print('soma TR',TRs.sum()/1e3,'soma Vd(Bt)',Vds.sum()/1e3,'frac',Vds.sum()/TRs.sum())
# Eckhardt
def eck(q,a,B):
    b=np.zeros_like(q);b[0]=q[0]
    for i in range(1,len(q)):
        if np.isnan(q[i]): b[i]=b[i-1];continue
        qq=q[i];bb=((1-B)*a*b[i-1]+(1-a)*B*qq)/(1-a*B);b[i]=min(bb,qq)
    return b
qf=Q.copy();
# fill nan by previous for filter
for i in range(1,len(qf)):
    if np.isnan(qf[i]): qf[i]=qf[i-1]
st=np.where(~np.isnan(qf))[0][0]
Vs=np.array([36,521,751,154,695,158,142,1336,1725,57,997,63,1073,1363,3963,1934,734.])*1e3
for B in (0.25,0.58,0.70,0.80):
    b=np.full_like(qf,np.nan);b[st:]=eck(qf[st:],0.995,B)
    vd=[]
    for n,a,e,qp in ev:
        m=(T>=a)&(T<=e);vd.append(np.nansum(Q[m]-b[m])*3600)
    vd=np.array(vd)
    print('BFImax',B,'soma Vd mil',round(vd.sum()/1e3),'frac',round(vd.sum()/TRs.sum(),3),'vies V_SCS',round(100*(Vs.sum()/vd.sum()-1),1),'%')
# A13 evento 17 hourly
n,a,e,qp=ev[-1]
m=(T>=a-np.timedelta64(24,'h'))&(T<=e)
print('evento 17 hora a hora: T P_DBT5 P_CL Q CSS Bt')
for i in np.where(m)[0]:
    print(str(T[i])[5:16],P1[i],P2[i],Q[i],None if np.isnan(C[i]) else round(C[i]),round(Bt[i],2) if not np.isnan(Bt[i]) else None)
# CSS max per event
for n,a,e,qp in ev:
    mm=(T>=a)&(T<=e);print('ev',n,'CSS max',round(np.nanmax(C[mm])),'n nan CSS',int(np.isnan(C[mm]).sum()))
# antecedent rain 14 days before event 17
for n,a,e,qp in ev[-3:]:
    mm=(T>=a-np.timedelta64(14*24,'h'))&(T<a);print('ev',n,'chuva 14d antes DBT5',np.nansum(P1[mm]),'CL',np.nansum(P2[mm]))
print('== defasagem pico CSS - pico Q (h), negativo = CSS antes; CSS 1h antes da subida de Q')
for n,a,e,qp in ev:
    mm=np.where((T>=a)&(T<=e))[0]
    iq=mm[np.nanargmax(Q[mm])];ic=mm[np.nanargmax(C[mm])]
    print(n,int((T[ic]-T[iq]).astype(int)),'CSSmax',round(C[ic]),'Qmax',Q[iq])
