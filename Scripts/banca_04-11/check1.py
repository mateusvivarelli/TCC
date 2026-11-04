import numpy as np
from scipy import stats
ev=np.arange(1,18)
dur=np.array([38,54,72,65,94,25,82,112,94,59,91,23,54,73,149,103,49],float)
P1=np.array([32.8,64,51,57,24,11,29,48.4,57,14.4,62.8,0,43.8,37.8,86,63.6,68])
P2=np.array([19.2,54.4,71.8,27,77.2,44.8,38.4,97.6,108.8,30.8,79,34.2,88.6,101.8,163,113.6,64.6])
R=np.array([23.4,57.3,65.4,36.2,60.9,34.5,35.5,82.5,92.9,25.8,74,23.7,74.9,82.2,139.4,97.7,65.6])
RI=np.array([23.6,19,53.2,35.2,36.6,29.4,15.4,30.6,23,12.6,11.8,32.8,36.6,37.4,47.8,15.8,43])
TR=np.array([409,2630,1070,1704,1840,325,1301,2581,1737,1236,2437,187,1198,1822,4280,3293,883],float)
B=np.array([185,899,485,716,1008,142,651,1331,936,684,958,87,464,891,2103,1699,434],float)
Vd=np.array([224,1731,585,987,832,183,650,1250,801,552,1479,101,735,931,2177,1595,449],float)
Vs=np.array([36,521,751,154,695,158,142,1336,1725,57,997,63,1073,1363,3963,1934,734],float)
SY=np.array([266,2040,928,1380,1372,199,1317,2109,1155,847,1822,211,1196,1731,3829,1736,1710],float)
MCa=np.array([74,990,2556,424,2034,463,269,3202,3396,100,1406,205,2919,3702,10361,3036,2157],float)
MCv=np.array([69,946,2723,394,2085,488,244,3287,3633,88,1383,204,3086,3882,11026,3144,2188],float)
MFa=np.array([357,2437,1249,2146,1609,352,940,1921,929,785,1410,226,1235,1562,3422,1580,804],float)
MFv=np.array([364,2464,1272,2206,1625,365,920,1909,917,782,1387,227,1238,1552,3399,1571,767],float)
A=137.8
print("n P1<P2",(P1<P2).sum(),"mean",P1.mean(),P2.mean(),"ratio",P2.mean()/P1.mean())
print("pares |P2/P1|", np.round(P2/np.where(P1>0,P1,np.nan),2))
print("sum MC aj",MCa.sum(),MCa.sum()/SY.sum(),"MC cv",MCv.sum(),MCv.sum()/SY.sum())
print("sum MFM aj",MFa.sum(),MFa.sum()/SY.sum(),"cv",MFv.sum(),MFv.sum()/SY.sum())
print("C esc Vd/(R*A)",np.round(Vd/(R*A),3))
print("C mean",np.mean(Vd/(R*A)))
print("corr C,R",stats.pearsonr(Vd/(R*A),R))
print("conc total mg/L",np.round(SY/TR*1000))
print("conc Vd mg/L",np.round(SY/Vd*1000))
def slope(x,y):
    r=stats.linregress(np.log(x),np.log(y));return r.slope,r.stderr,r.rvalue**2
print("Vs~R",slope(R,Vs));print("Vd~R",slope(R,Vd));print("TR~R",slope(R,TR))
print("SY~TR",slope(TR,SY));print("SY~Vd",slope(Vd,SY));print("SY~R",slope(R,SY));print("MCa~R",slope(R,MCa))
print("var lnSY",np.var(np.log(SY),ddof=1),"lnTR",np.var(np.log(TR),ddof=1),"ln conc",np.var(np.log(SY/TR),ddof=1))
# null model LOO
def loo(pred_x):
    out=[]
    for i in range(17):
        m=np.ones(17,bool);m[i]=False
        c=np.exp(np.mean(np.log(SY[m])-np.log(pred_x[m])))
        out.append(c*pred_x[i])
    return np.array(out)
def met(S,O=SY):
    ape=100*abs(S-O)/O
    f2=((S/O>=.5)&(S/O<=2)).mean()*100
    nse=1-np.sum((np.log(O)-np.log(S))**2)/np.sum((np.log(O)-np.log(O).mean())**2)
    return dict(med=round(np.median(ape),1),f2=round(f2,1),nse=round(nse,2),sp=round(stats.spearmanr(O,S)[0],2) if np.std(S)>0 else None)
print("null",met(loo(np.ones(17))))
print("R",met(loo(R)));print("Vd",met(loo(Vd)));print("TR",met(loo(TR)))
print("MCv",met(MCv));print("MFv",met(MFv))
print("Vs direct rule",met(loo(Vs)))
# conc ~ RI/R
rr=RI/R;print("RI/R",np.round(rr,3),"(max/min)^.56",(rr.max()/rr.min())**.56)
print("ln(SY/Vd)~ln(RI/R)",stats.pearsonr(np.log(rr),np.log(SY/Vd)),"sem 17",stats.pearsonr(np.log(rr[:16]),np.log((SY/Vd)[:16])))
print("ln(SY/TR)~ln(RI/R)",stats.pearsonr(np.log(rr),np.log(SY/TR)),"sem17",stats.pearsonr(np.log(rr[:16]),np.log((SY/TR)[:16])))
print("ln(SY/TR)~ln RI",stats.pearsonr(np.log(RI),np.log(SY/TR)))
print("residuo MFM vs RI/R",stats.pearsonr(np.log(rr),np.log(MFa/SY)))
# split: calib 1-11, prever 12-17, and reverse
for nm,x in [("MFMbase",MFa),("MCbase",MCa),("Vd",Vd),("R",R)]:
    a=np.arange(17)<11
    c=np.exp(np.mean(np.log(SY[a])-np.log(x[a])))
    S=c*x
    r=S[~a]/SY[~a]
    c2=np.exp(np.mean(np.log(SY[~a])-np.log(x[~a])))
    S2=c2*x; r2=S2[a]/SY[a]
    print(nm,"1-11->12-17: razao",np.round(r,2),"med ape",round(np.median(abs(r-1))*100,1),"bias log",round(np.exp(np.mean(np.log(r))),2),"| 12-17->1-11 med ape",round(np.median(abs(r2-1))*100,1),"c ratio",round(c2/c,2))
# grupos conc
g1=np.log((SY/Vd)[:11]);g2=np.log((SY/Vd)[11:16])
print("mean mgL g1",(SY/Vd)[:11].mean()*1000,"g2",(SY/Vd)[11:16].mean()*1000,stats.mannwhitneyu(g1,g2),stats.ttest_ind(g1,g2,equal_var=False))
print("trend residuo MFM x ordem",stats.spearmanr(ev,np.log(MFv/SY)))
print("corr dur,R",stats.spearmanr(dur,R),"ratio Vs/Vd vs dur",stats.spearmanr(dur,Vs/Vd),"vs R",stats.spearmanr(R,Vs/Vd))
print("dur<=24",(dur<=24).sum(),"dur<=25",(dur<=25).sum(),"dur>48",(dur>48).sum(),"dur>72",(dur>72).sum())
print("c unidades",.0344*1000**.56,.0222*1000**.56,"1000^.56",1000**.56,"n^.12",153855**.12,"c ratio",.0344/.0222)
print("constante mm",25.4*1.33/25.4**1.15)
for S in [50,141.9,255.7,558]:
    print(S,25.4*1.33*(S/25.4)**1.15,25.4*1.33*(S/25.4)**1.15/S)
print("CNeq S490",25400/(489.9+254))
# Q com e sem Woodward no pixel exemplo e faixa de chuva
def q(P,S,l): return np.where(P>l*S,(P-l*S)**2/(P+(1-l)*S),0)
for CNII in [55,71.6,81,90]:
    CNI=4.2*CNII/(10-.058*CNII);S2II=25400/CNII-254;S2=25400/CNI-254;S5=25.4*1.33*(S2/25.4)**1.15
    for P in [25,63,100,140]:
        print(CNII,round(CNI,1),P,"QCN2 l.2",round(float(q(P,S2II,.2)),1),"QCN1 l.2",round(float(q(P,S2,.2)),1),"QCN1 l.05 S conv",round(float(q(P,S5,.05)),1),"QCN1 l.05 sem conv",round(float(q(P,S2,.05)),1))
print("a dia",.995**24,"tau h",-1/np.log(.995),"tau d",-1/np.log(.995)/24,"dist postos km",np.hypot(348520.8-319862.4,7426415.3-7432277.5)/1000)
print("Moore cap",(200/22.13)**.4, "As200 cells",200*30/897.49)
print("Intervalo entre eventos: ")
