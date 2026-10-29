from common import *
ev = le_eventos(); h = le_serie()
print(ev.to_string())
d = cargas(h, ev, h.Bt.to_numpy(float))
x = pd.read_excel(os.path.join(DI, "eventos_processados_manuais.xlsx"), sheet_name="Sheet1").iloc[:18]
ref = [x.iloc[0 if n == 1 else n] for n in range(1, 18)]
d["SY_xlsx"] = [r["SYY_t"] for r in ref]; d["TR_xlsx"] = [r["T_R_m3"] for r in ref]
d["difSY%"] = 100 * (d.SY_obs / d.SY_xlsx - 1); d["difTR%"] = 100 * (d.TR / d.TR_xlsx - 1)
print(d.round(2).to_string())
print("soma SY_obs", d.SY_obs.sum(), "SY_base", d.SY_base.sum(), "SY_dir", d.SY_dir.sum(), "fracao base", d.SY_base.sum() / d.SY_obs.sum())
fb = d.SY_base / d.SY_obs
print("frac base por evento: med", np.median(fb), "min", fb.min(), "max", fb.max())
M = Modelo(ev)
print("Vscs/Vdir adotada:", np.round(M.Vscs["ADOTADA"] / d.Vdir, 2))
print("Vscs/Vdir candidata:", np.round(M.Vscs["CANDIDATA"] / d.Vdir, 2))
print("S20 min/max/med", np.nanmin(M.S20), np.nanmax(M.S20), np.median(M.S20))
SY = d.SY_obs.to_numpy(); VD = d.Vdir.to_numpy()
print("modelo                 MedAPE   F2  NSElog Spear")
for k in ("ADOTADA", "CANDIDATA"):
    print(k, "MC ", fmt(metricas(SY, M.Emc[k])))
    print(k, "MFM", fmt(metricas(SY, M.Emfm(k, VD))))
print("c*chuva", fmt(metricas(SY, ev.R.to_numpy())))
print("c*Vdir", fmt(metricas(SY, VD)))
print("c*TR", fmt(metricas(SY, d.TR.to_numpy())))
