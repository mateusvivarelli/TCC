from common import *
ev = le_eventos(); h = le_serie(); M = Modelo(ev)
Q = h.Q.to_numpy(float); Bt = h.Bt.to_numpy(float); v = np.isfinite(Q)
print("=== Reproducao do Bt fornecido ===")
for a, bfi in ((0.995, 0.70), (0.995, 0.58), (0.995, 0.80), (0.98, 0.70)):
    b = eck_serie(h, a, bfi); d = np.abs(b[v] - Bt[v])
    print(f"Eckhardt a={a} BFImax={bfi}: mediana|dif|={np.median(d):.2e}  max|dif|={d.max():.2e}  r={np.corrcoef(b[v], Bt[v])[0,1]:.6f}  BFI global={np.nansum(b)/np.nansum(Q):.3f}")
lh = lh_serie(h); d = np.abs(lh[v] - Bt[v]); print(f"Lyne-Hollick 0,925 3 passadas: mediana|dif|={np.median(d):.3f}  BFI global={np.nansum(lh)/np.nansum(Q):.3f}  r={np.corrcoef(lh[v], Bt[v])[0,1]:.4f}")
print(f"Bt fornecido: BFI global={np.nansum(Bt)/np.nansum(Q):.3f}; Bt<=Q sempre: {np.all(Bt[v] <= Q[v] + 1e-9)}")

cen = {"(0) Bt fornecido": Bt,
       "(i) Eckhardt a=0,995 BFImax=0,70": eck_serie(h, 0.995, 0.70),
       "(ii) Eckhardt a=0,995 BFImax=0,58": eck_serie(h, 0.995, 0.58),
       "(iii) Eckhardt a=0,995 BFImax=0,80": eck_serie(h, 0.995, 0.80),
       "(iv) Eckhardt a=0,98 BFImax=0,70": eck_serie(h, 0.98, 0.70),
       "(v) Lyne-Hollick 0,925 (3 passadas)": lh}
d0 = cargas(h, ev, Bt)
SY = d0.SY_obs.to_numpy(); R = ev.R.to_numpy()
print("\n=== Checagem 1: V_dir por evento (m3) e razoes ===")
vd_tab = pd.DataFrame({"ev": ev.ev})
res = []
for nome, b in cen.items():
    d = cargas(h, ev, b); VD = d.Vdir.to_numpy()
    vd_tab[nome[:5]] = VD / d0.Vdir.to_numpy()
    row = dict(cenario=nome, frac_direta=d.Vdir.sum() / d.TR.sum(), razao_med=np.median(VD / d0.Vdir.to_numpy()),
               razao_min=np.min(VD / d0.Vdir.to_numpy()), razao_max=np.max(VD / d0.Vdir.to_numpy()),
               fracdir_med_evento=np.median(VD / d.TR.to_numpy()), VD_neg=int((VD <= 0).sum()))
    for k in ("CANDIDATA", "ADOTADA"):
        m = metricas(SY, M.Emfm(k, VD)); row.update({f"{k[:4]}_{q}": m[q] for q in ("MedAPE", "F2", "NSElog", "Spear")})
    m = metricas(SY, VD); row.update({f"Vdir_{q}": m[q] for q in ("MedAPE", "F2", "NSElog", "Spear")})
    res.append(row)
    print(nome, "| V_dir por evento (x1000 m3):", np.round(VD / 1000).astype(int).tolist())
R_ = pd.DataFrame(res); R_.to_csv(os.path.join(WORK, "check1_resultado.csv"), index=False)
pd.set_option("display.width", 250)
print(R_.round(3).to_string())
print("\nrazao V_dir(cenario)/V_dir(Bt) por evento:"); print(vd_tab.round(2).to_string())
