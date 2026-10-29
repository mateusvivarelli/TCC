from common import *
from scipy.optimize import brentq
Pv,S20,K,A=rasters()
for rot,S in (("mediana",np.median(S20)),("p5",np.percentile(S20,5)),("p95",np.percentile(S20,95))):
    S5=s005(S); f=lambda P: qscs(np.array([P]),S5,.05)[0]-qscs(np.array([P]),S,.2)[0]
    xs=np.linspace(0.3*S+1,20*S,4000); v=[f(x) for x in xs]; i=next(k for k in range(1,len(v)) if v[k-1]<0 and v[k]>=0 or v[k-1]>0 and v[k]<=0) if any(a*b<0 for a,b in zip(v,v[1:])) else None
    print(rot,"S20=%.1f S05=%.1f"%(S,S5),"Pcrit=",None if i is None else round(brentq(f,xs[i-1],xs[i]),1),"mm")
