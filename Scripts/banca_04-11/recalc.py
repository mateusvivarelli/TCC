import numpy as np

def rank(x):
    x=np.asarray(x,float); o=np.argsort(x); r=np.empty(len(x)); r[o]=np.arange(1,len(x)+1)
    for v in np.unique(x):
        m=x==v; r[m]=r[m].mean()
    return r
class _R: pass
class stats:
    @staticmethod
    def spearmanr(a,b): return (np.corrcoef(rank(a),rank(b))[0,1],)
    @staticmethod
    def linregress(x,y):
        o=_R(); o.slope=np.polyfit(x,y,1)[0]; o.rvalue=np.corrcoef(x,y)[0,1]; return o
    @staticmethod
    def wilcoxon(d):
        d=np.asarray(d,float); d=d[d!=0]; n=len(d); r=rank(abs(d)); W=r[d>0].sum()
        # exato (permutacao de sinais)
        from itertools import product
        cnt={0.0:1}
        for ri in r:
            nc={}
            for k,v in cnt.items():
                nc[k]=nc.get(k,0)+v; nc[k+ri]=nc.get(k+ri,0)+v
            cnt=nc
        tot=2**n; m=min(W,r.sum()-W); p=2*sum(v for k,v in cnt.items() if k<=m+1e-9)/tot
        o=_R(); o.pvalue=min(1,p); return o
from datetime import datetime as D
ev=list(range(1,18))
dur=[38,54,72,65,94,25,82,112,94,59,91,23,54,73,149,103,49]
p1=[32.8,64.0,51.0,57.0,24.0,11.0,29.0,48.4,57.0,14.4,62.8,0.0,43.8,37.8,86.0,63.6,68.0]
p2=[19.2,54.4,71.8,27.0,77.2,44.8,38.4,97.6,108.8,30.8,79.0,34.2,88.6,101.8,163.0,113.6,64.6]
R=[23.4,57.3,65.4,36.2,60.9,34.5,35.5,82.5,92.9,25.8,74.0,23.7,74.9,82.2,139.4,97.7,65.6]
RI=[23.6,19.0,53.2,35.2,36.6,29.4,15.4,30.6,23.0,12.6,11.8,32.8,36.6,37.4,47.8,15.8,43.0]
qp=[10.3,30.4,16.6,17.0,22.1,14.7,16.4,20.4,11.8,10.6,20.9,13.1,16.0,22.3,28.4,23.1,21.4]
TR=[409,2630,1070,1704,1840,325,1301,2581,1737,1236,2437,187,1198,1822,4280,3293,883]
Bt=[185,899,485,716,1008,142,651,1331,936,684,958,87,464,891,2103,1699,434]
V=[224,1731,585,987,832,183,650,1250,801,552,1479,101,735,931,2177,1595,449]
SY=[266,2040,928,1380,1372,199,1317,2109,1155,847,1822,211,1196,1731,3829,1736,1710]
VS=[36,521,751,154,695,158,142,1336,1725,57,997,63,1073,1363,3963,1934,734]
MCa=[74,990,2556,424,2034,463,269,3202,3396,100,1406,205,2919,3702,10361,3036,2157]
MCv=[69,946,2723,394,2085,488,244,3287,3633,88,1383,204,3086,3882,11026,3144,2188]
MFa=[357,2437,1249,2146,1609,352,940,1921,929,785,1410,226,1235,1562,3422,1580,804]
MFv=[364,2464,1272,2206,1625,365,920,1909,917,782,1387,227,1238,1552,3399,1571,767]
errMC=[-74,-54,193,-71,52,146,-82,56,215,-90,-24,-3,158,124,188,81,28]
errMF=[37,21,37,60,18,84,-30,-9,-21,-8,-24,8,3,-10,-11,-10,-55]
A={k:np.array(v,float) for k,v in dict(dur=dur,p1=p1,p2=p2,R=R,RI=RI,qp=qp,TR=TR,Bt=Bt,V=V,SY=SY,VS=VS,MCa=MCa,MCv=MCv,MFa=MFa,MFv=MFv).items()}
print("medias T2", {k:round(float(A[k].mean()),1) for k in ['dur','p1','p2','R','RI','qp']})
print("R calc -R", np.round(.307*A['p1']+.693*A['p2']-A['R'],2))
print("somas T3", A['TR'].sum(),A['Bt'].sum(),A['V'].sum(),A['SY'].sum(), "base%",round(100*A['Bt'].sum()/A['TR'].sum(),1), "media SY",round(A['SY'].mean(),1))
print("TR-Bt-V",(A['TR']-A['Bt']-A['V']).astype(int))
print("base% ev",np.round(100*A['Bt']/A['TR']).astype(int))
print("soma VS",A['VS'].sum(),"razao",np.round(A['VS']/A['V'],2),"vies",round(100*(A['VS'].sum()/A['V'].sum()-1),2))
def met(s,o):
    ape=100*abs(s-o)/o; f2=100*np.mean((s/o>=.5)&(s/o<=2))
    lo,ls=np.log(o),np.log(s)
    nl=1-((lo-ls)**2).sum()/((lo-lo.mean())**2).sum()
    n=1-((o-s)**2).sum()/((o-o.mean())**2).sum()
    return dict(medape=round(float(np.median(ape)),1),meanape=round(float(ape.mean()),1),f2=round(float(f2),1),nselog=round(float(nl),2),nse=round(float(n),2),sp=round(float(stats.spearmanr(s,o)[0]),2))
print("vol",met(A['VS'],A['V']))
print("MC cv",met(A['MCv'],A['SY'])); print("MC aj",met(A['MCa'],A['SY']))
print("MFM cv",met(A['MFv'],A['SY'])); print("MFM aj",met(A['MFa'],A['SY']))
def loo(x,y):
    out=[]
    for i in range(len(y)):
        m=np.ones(len(y),bool); m[i]=False
        c=np.exp(np.mean(np.log(y[m])-np.log(x[m]))); out.append(c*x[i])
    return np.array(out)
sR=loo(A['R'],A['SY']); sV=loo(A['V'],A['SY'])
print("simples R",met(sR,A['SY'])); print("simples V",met(sV,A['SY']))
print("ev6 simples R razao",round(sR[5]/199,2),"ev17 simples V err",round(100*(sV[16]/1710-1),1))
e=lambda s:100*abs(s-A['SY'])/A['SY']
for name,a,b in [("MC-simplesR",A['MCv'],sR),("MFM-simplesV",A['MFv'],sV)]:
    d=e(a)-e(b); rng=np.random.default_rng(1)
    bs=[np.median(rng.choice(d,17)) for _ in range(4000)]
    print(name,"mediana",round(float(np.median(d)),1),"IC",np.round(np.percentile(bs,[2.5,97.5]),1),"wilcoxon p",round(float(stats.wilcoxon(d).pvalue),3),"a pior que b",int((d>0).sum()),"a melhor",int((d<0).sum()))
print("err MC dif",np.round(100*(A['MCv']/A['SY']-1)).astype(int)-np.array(errMC))
print("err MF dif",np.round(100*(A['MFv']/A['SY']-1)).astype(int)-np.array(errMF))
print("logerr corr cv",round(np.corrcoef(np.log(A['MCv']/A['SY']),np.log(A['VS']/A['V']))[0,1],3), "aj",round(np.corrcoef(np.log(A['MCa']/A['SY']),np.log(A['VS']/A['V']))[0,1],3))
r=np.corrcoef(np.log(A['MCv']/A['SY']),np.log(A['VS']/A['V']))[0,1]; print("r2",round(r*r,3))
print("corr C,R",round(np.corrcoef(A['V']/A['R'],A['R'])[0,1],3))
print("var lnTR",round(np.var(np.log(A['TR']),ddof=1),3),"var ln(SY/TR)",round(np.var(np.log(A['SY']/A['TR']),ddof=1),3),"var0",round(np.var(np.log(A['TR'])),3),round(np.var(np.log(A['SY']/A['TR'])),3))
sl=stats.linregress(np.log(A['TR']),np.log(A['SY'])); print("ln SY~ln TR slope",round(sl.slope,3),"r2",round(sl.rvalue**2,3))
sl=stats.linregress(np.log(A['V']),np.log(A['SY'])); print("ln SY~ln V slope",round(sl.slope,3),"r2",round(sl.rvalue**2,3))
d=(A['SY']-A['SY'].mean())**2; print("ev15 share",round(100*d[14]/d.sum(),1))
cc=1000*A['SY']/A['V']; print("conc",np.round(cc).astype(int))
print("1-11 simples",round(cc[:11].mean()),"mediana",round(np.median(cc[:11])),"soma",round(1000*A['SY'][:11].sum()/A['V'][:11].sum()))
print("12-16 simples",round(cc[11:16].mean()),"mediana",round(np.median(cc[11:16])),"soma",round(1000*A['SY'][11:16].sum()/A['V'][11:16].sum()))
print("16 sem17 media",round(cc[:16].mean()),"mediana",round(np.median(cc[:16])),"soma",round(1000*A['SY'][:16].sum()/A['V'][:16].sum()), "ev17/x",round(cc[16]/cc[:16].mean(),2),round(cc[16]/cc[:16].max(),2))
for drop in [16,14]:
    m=np.ones(17,bool); m[drop]=False
    s=loo(A['MFa'][m],A['SY'][m]); print("MFM sem ev",drop+1,met(s,A['SY'][m]), "sem recalibrar",met(A['MFv'][m],A['SY'][m]))
    s2=loo(A['MCa'][m],A['SY'][m]); s3=loo(A['R'][m],A['SY'][m]); print("  MC",met(s2,A['SY'][m]),"simplesR",met(s3,A['SY'][m]))
ini="22/11/18 09;30/11/18 22;17/12/18 22;24/12/18 06;04/01/19 19;16/01/19 12;25/01/19 00;15/02/19 13;25/02/19 15;17/03/19 05;04/07/19 12;30/12/19 09;02/01/20 11;07/01/20 18;02/02/20 20;09/02/20 14;20/02/20 09".split(";")
fim="23/11/18 23;03/12/18 04;20/12/18 22;26/12/18 23;08/01/19 17;17/01/19 13;28/01/19 10;20/02/19 05;01/03/19 13;19/03/19 16;08/07/19 07;31/12/19 08;04/01/20 17;10/01/20 19;09/02/20 01;13/02/20 21;22/02/20 10".split(";")
f="%d/%m/%y %H"
print("dur dif",[int((D.strptime(b,f)-D.strptime(a,f)).total_seconds()/3600)-x for a,b,x in zip(ini,fim,dur)])
print("RI/R>1",[i for i,a,b in zip(ev,RI,R) if a/b>1])
cn2=81.0;cn1=4.2*cn2/(10-.058*cn2);s20=25.4*(1000/cn1-10);s05=25.4*1.33*(s20/25.4)**1.15;ia=.05*s05;Q=(75.4-ia)**2/(75.4+.95*s05);vp=Q/1000*897.49;pr=vp*(11.8/74)/3600;E=11.8*(Q*pr*897.49)**.56*.0351*.212*4.869
print("apx",round(cn1,2),round(s20,1),round(s05,1),round(ia,1),round(Q,2),round(vp,2),pr,round(E,3),round(.0344*E,4))
print("area pix",29.992*29.925,"km2",153855*897.49/1e6,"5%",153855*.05,"f ev10",552/57,"1.48^1.12",1.48**1.12,63451/40885,63451*.0222,40885*.0344)
print("mm coef",1.33*25.4**(-.15))
print("K",.686*.0475+.176*.0351+.001*.0087,"C",.005+.039*.212+.127*.121+.29*.05+.396*.015)
