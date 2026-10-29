"""Sensibilidade exploratoria: agua de base com concentracao constante = mediana do CSS nas horas em que Q ~ Bt (coluna CSS_Bt, 911 h)."""
from common import *
ev=le_eventos(); h=le_serie(); M=Modelo(ev); Bt=h.Bt.to_numpy(float); R=ev.R.to_numpy()
cb=h.CSSBt.to_numpy(float); ok=np.isfinite(cb)
d0=cargas(h,ev,Bt); VD=d0.Vdir.to_numpy()
for rot,c0 in (("mediana CSS_Bt",np.median(cb[ok])),("P25 CSS_Bt",np.percentile(cb[ok],25)),("P75 CSS_Bt",np.percentile(cb[ok],75))):
    base=d0.Vbase.to_numpy()*c0/1e6; alvo=d0.SY_obs.to_numpy()-base
    print(f"C_base const = {c0:.0f} mg/L ({rot}): base = {100*base.sum()/d0.SY_obs.sum():.1f}% da carga total (mediana por evento {np.median(100*base/d0.SY_obs):.1f}%, max {np.max(100*base/d0.SY_obs):.1f}%)")
    for n,x in (("MFM CANDIDATA",M.Emfm("CANDIDATA",VD)),("MFM ADOTADA",M.Emfm("ADOTADA",VD)),("c*V_dir",VD),("c*chuva",R),("MC CANDIDATA",M.Emc["CANDIDATA"])):
        print(f"    {n:<16}{fmt(metricas(alvo,x))}")
