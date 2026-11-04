import numpy as np, math
ev=np.arange(1,18)
R=np.array([23.4,57.3,65.4,36.2,60.9,34.5,35.5,82.5,92.9,25.8,74.0,23.7,74.9,82.2,139.4,97.7,65.6])
RI=np.array([23.6,19.0,53.2,35.2,36.6,29.4,15.4,30.6,23.0,12.6,11.8,32.8,36.6,37.4,47.8,15.8,43.0])
Qp=np.array([10.3,30.4,16.6,17.0,22.1,14.7,16.4,20.4,11.8,10.6,20.9,13.1,16.0,22.3,28.4,23.1,21.4])
dur=np.array([38,54,72,65,94,25,82,112,94,59,91,23,54,73,149,103,49.])
TR=np.array([409,2630,1070,1704,1840,325,1301,2581,1737,1236,2437,187,1198,1822,4280,3293,883.])
Vd=np.array([224,1731,585,987,832,183,650,1250,801,552,1479,101,735,931,2177,1595,449.])
Vs=np.array([36,521,751,154,695,158,142,1336,1725,57,997,63,1073,1363,3963,1934,734.])
O=np.array([266,2040,928,1380,1372,199,1317,2109,1155,847,1822,211,1196,1731,3829,1736,1710.])
MCa=np.array([74,990,2556,424,2034,463,269,3202,3396,100,1406,205,2919,3702,10361,3036,2157.])
MC=np.array([69,946,2723,394,2085,488,244,3287,3633,88,1383,204,3086,3882,11026,3144,2188.])
MFa=np.array([357,2437,1249,2146,1609,352,940,1921,929,785,1410,226,1235,1562,3422,1580,804.])
MF=np.array([364,2464,1272,2206,1625,365,920,1909,917,782,1387,227,1238,1552,3399,1571,767.])
c=lambda x,y:float(np.corrcoef(x,y)[0,1])
rk=lambda x:np.argsort(np.argsort(x))
def loo(X):
    p=np.zeros(17)
    for i in range(17):
        m=np.ones(17,bool);m[i]=False
        p[i]=np.exp(np.mean(np.log(O[m])-np.log(X[m])))*X[i]
    return p
def met(S,name=''):
    ape=100*abs(S-O)/O;f2=100*np.mean((S/O>=.5)&(S/O<=2))
    ls,lo=np.log(S),np.log(O)
    nl=1-np.sum((lo-ls)**2)/np.sum((lo-lo.mean())**2)
    n=1-np.sum((O-S)**2)/np.sum((O-O.mean())**2)
    d=rk(S)-rk(O);rs=1-6*np.sum(d**2)/(17*(17**2-1))
    mla=np.median(abs(np.log(S/O)))
    print(f"{name:28s} MedAPE {np.median(ape):6.1f} F2 {f2:5.1f} NSElog {nl:6.2f} NSElin {n:7.2f} Sp {rs:5.2f} soma/obs {S.sum()/O.sum():5.2f} fatorMed {np.exp(mla):.2f}")
def wilc(d):
    d=d[d!=0];n=len(d);r=np.abs(d);sr=np.sort(r);rk2=np.zeros(n,int)
    for i,x in enumerate(r):
        rk2[i]=int(round(2*np.mean(np.where(sr==x)[0]+1)))
    W=rk2[d>0].sum();tot=rk2.sum();dist=np.zeros(tot+1);dist[0]=1
    for x in rk2:
        nd=dist.copy();nd[x:]+=dist[:-x];dist=nd
    dist/=2.0**n
    return min(1.0,2*min(dist[:W+1].sum(),dist[W:].sum()))
rng=np.random.default_rng(1)
def boot(d,B=4000):
    return np.percentile(np.median(d[rng.integers(0,17,(B,17))],axis=1),[2.5,97.5]).round(3)
def binom_cdf(k,n,p): return sum(math.comb(n,i)*p**i*(1-p)**(n-i) for i in range(k+1))
def cp(k,n,a=.05):
    g=np.linspace(0,1,10001)
    lo=0 if k==0 else next(x for x in g if 1-binom_cdf(k-1,n,x)>=a/2)
    hi=1 if k==n else next(x for x in g[::-1] if binom_cdf(k,n,x)>=a/2)
    return round(lo*100),round(hi*100)
def loo_reg(x):
    p=np.zeros(17)
    for i in range(17):
        m=np.ones(17,bool);m[i]=False
        b,a=np.polyfit(np.log(x[m]),np.log(O[m]),1)
        p[i]=np.exp(a+b*np.log(x[i]))
    return p

print('== metricas');met(MC,'MC LOO tab12');met(MF,'MFM LOO tab12');met(MCa,'MC ajuste');met(MFa,'MFM ajuste')
SR,SV,ST,S0=loo(R),loo(Vd),loo(TR),loo(np.ones(17))
met(SR,'c*R LOO');met(SV,'c*Vdir LOO');met(ST,'c*TR LOO');met(S0,'constante LOO')
met(loo(Vs**1.12),'c*Vscs^1.12');met(loo(Vd**1.12),'c*Vd^1.12');met(loo(Vd**1.12*(RI/R)**.56),'c*Vd^1.12*(RI/R)^.56')
met(loo(R**1.12),'c*R^1.12');met(loo(R**1.12*(RI/R)**.56),'c*R^1.12*(RI/R)^.56')
ICloo=loo_reg(TR*Qp);met(ICloo,'a*(TR*qp)^b LOO');met(loo_reg(R),'a*R^b LOO');met(loo_reg(Vd),'a*Vd^b LOO')
print('b(TR*qp)',round(np.polyfit(np.log(TR*Qp),np.log(O),1)[0],3),'b Vd',round(np.polyfit(np.log(Vd),np.log(O),1)[0],3),'b TR',round(np.polyfit(np.log(TR),np.log(O),1)[0],3))
print('== pareados: mediana dif, IC, p Wilcoxon, n A melhor')
for nm,A,B in [('MC-chuva',MC,SR),('MFM-cVd',MF,SV),('MC-const',MC,S0),('chuva-const',SR,S0),('MFM-const',MF,S0),('cVd-const',SV,S0),('MFM-ICloo',MF,ICloo)]:
    dA=100*abs(A-O)/O-100*abs(B-O)/O;dL=abs(np.log(A/O))-abs(np.log(B/O))
    print(nm,'APE',round(float(np.median(dA)),1),boot(dA),'p',round(wilc(dA),4),'melhor',int((dA<0).sum()),'| log',round(float(np.median(dL)),3),boot(dL),'p',round(wilc(dL),4))
print('== Clopper-Pearson');[print(k,'/17',cp(k,17)) for k in (6,13,14,16,17)]
print('== volume');lr=np.log(Vs/Vd)
print('ln(Vs/Vd) x lnR',round(c(lr,np.log(R)),2),'x dur',round(c(lr,dur),2),'x ln dur',round(c(lr,np.log(dur)),2),'x ln(R/dur)',round(c(lr,np.log(R/dur)),2),'| R x dur',round(c(R,dur),2))
ce=Vd/(R*137.8);print('coef esc min max',ce.min().round(3),ce.max().round(3),'x R',round(c(ce,R),2))
print('r ln(MC/O) x ln(Vs/Vd)',round(c(np.log(MC/O),lr),3))
print('== concentracao');print('O/Vd mg/L',(O/Vd*1000).round(0));print('O/TR mg/L',(O/TR*1000).round(0))
print('ln(O/Vd) x ln(RI/R)',round(c(np.log(O/Vd),np.log(RI/R)),2),'ln(O/TR) x ln(RI/R)',round(c(np.log(O/TR),np.log(RI/R)),2),'ln(O/TR) x ln(qp/TR)',round(c(np.log(O/TR),np.log(Qp/TR)),2))
print('== tendencia');res=np.log(MF/O);print('res MFM x ordem r',round(c(res,ev),2),'Sp',round(c(rk(res),ev),2))
print('== split temporal')
EMC,EMF=MCa/.0344,MFa/.0222
for nm,E in [('MC',EMC),('MFM',EMF),('chuva',R),('Vdir',Vd)]:
    for tr,te,l in [(np.arange(11),np.arange(11,17),'1-11->12-17'),(np.arange(11,17),np.arange(11),'12-17->1-11')]:
        cc=np.exp(np.mean(np.log(O[tr]/E[tr])));S=cc*E[te];Y=O[te]
        print(nm,l,'MedAPE',round(float(np.median(100*abs(S-Y)/Y)),1),'F2',round(100*np.mean((S/Y>=.5)&(S/Y<=2))),'razao mediana',round(float(np.median(S/Y)),2))
print('== mapa: peso de cada evento na soma (%)');print('MC',(MCa/MCa.sum()*100).round(1));print('MFM',(MFa/MFa.sum()*100).round(1))
print('== uso');C=np.array([.015,.05,.121,.212,1,1]);E=np.array([19,129,191,530,1772,3784.]);ar=np.array([39.6,29,12.7,3.9,.5,.048]);ob=np.array([7.5,37.4,24.2,20.9,8.2,1.8])
print('r ln E/area x ln C',round(c(np.log(E),np.log(C)),3));print('so C*area %',(ar*C/np.sum(ar*C)*100).round(1),'obs',ob)
print('== S');[print(s,'S005',round(25.4*1.33*(s/25.4)**1.15,1),'Ia',round(.05*25.4*1.33*(s/25.4)**1.15,1)) for s in (12,255.7,558)]
print('coef mm',round(1.33*25.4**-.15,4),'As200 pixels',round(200*30/897.49,1))
