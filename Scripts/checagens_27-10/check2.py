from common import *
pd.set_option("display.width", 250)
ev = le_eventos(); h = le_serie(); M = Modelo(ev)
Q = h.Q.to_numpy(float); Bt = h.Bt.to_numpy(float); C = h.CSS.to_numpy(float); t = pd.DatetimeIndex(h.Data)
R = ev.R.to_numpy()
cen = {"Bt fornecido": Bt, "Eckhardt BFImax 0,58": eck_serie(h, 0.995, 0.58), "Lyne-Hollick 0,925": lh_serie(h)}

# ---------- tabela por evento: parcela da carga atribuida a base
d0 = cargas(h, ev, Bt)
tab = pd.DataFrame({"ev": ev.ev, "SY_total_t": d0.SY_obs, "SY_base_t": d0.SY_base, "SY_dir_t": d0.SY_dir, "base_%carga": 100 * d0.SY_base / d0.SY_obs,
                    "base_%volume": 100 * d0.Vbase / d0.TR})
for nome in ("Eckhardt BFImax 0,58", "Lyne-Hollick 0,925"):
    dd = cargas(h, ev, cen[nome]); tab[f"base_%carga[{nome[:4]}]"] = 100 * dd.SY_base / dd.SY_obs
print("=== parcela da carga medida atribuida a base ===")
print(tab.round(1).to_string())
print("total: carga base", d0.SY_base.sum(), "de", d0.SY_obs.sum(), f"= {100*d0.SY_base.sum()/d0.SY_obs.sum():.1f}%; mediana por evento {np.median(tab['base_%carga']):.1f}% (min {tab['base_%carga'].min():.1f}, max {tab['base_%carga'].max():.1f})")
print("volume: base", d0.Vbase.sum(), "de", d0.TR.sum(), f"= {100*d0.Vbase.sum()/d0.TR.sum():.1f}%")
tab.to_csv(os.path.join(WORK, "check2_tabela_base_por_evento.csv"), index=False)

# ---------- metricas: alvo total x alvo direto
def bloco(alvo_nome, alvo, VD, rot_sep):
    linhas = []
    for k in ("CANDIDATA", "ADOTADA"):
        linhas.append((f"MC  {k}", metricas(alvo, M.Emc[k])))
        linhas.append((f"MFM {k}", metricas(alvo, M.Emfm(k, VD))))
    linhas.append(("REF c*chuva(R)", metricas(alvo, R)))
    linhas.append(("REF c*V_dir medido", metricas(alvo, VD)))
    linhas.append(("REF c*T_R (volume total)", metricas(alvo, d0.TR.to_numpy())))
    return linhas

res = {}
print("\n=== metricas LOO (log) por alvo; separacao Bt fornecido ===")
print(f"{'alvo / modelo':<42} MedAPE   F2 NSElog Spear")
VD0 = d0.Vdir.to_numpy()
for alvo_nome, alvo in (("TOTAL (SY_obs)", d0.SY_obs.to_numpy()), ("DIRETO (SY_dir_obs)", d0.SY_dir.to_numpy())):
    print("--", alvo_nome)
    for nome, m in bloco(alvo_nome, alvo, VD0, "Bt"):
        print(f"   {nome:<39}{fmt(m)}")
        res[(alvo_nome, nome)] = m
    # vies mediano das previsoes
rows = []
for (a, n), m in res.items():
    rows.append(dict(alvo=a, modelo=n, **{q: m[q] for q in ("MedAPE", "F2", "NSElog", "Spear")}))
pd.DataFrame(rows).to_csv(os.path.join(WORK, "check2_metricas_alvo_total_x_direto.csv"), index=False)

# vies: razao mediana sim/obs (LOO)
print("\nrazao mediana LOO sim/obs (alvo direto):", {n: round(float(np.median(m['loo'] / d0.SY_dir.to_numpy())), 2) for (a, n), m in res.items() if a.startswith("DIRETO")})
# c calibrado
print("c (t por unidade de E) alvo total x direto, MFM CANDIDATA:", res[("TOTAL (SY_obs)", "MFM CANDIDATA")]["c"], res[("DIRETO (SY_dir_obs)", "MFM CANDIDATA")]["c"])

# ---------- separacoes alternativas, alvo e V_dir consistentes
print("\n=== MFM/MC e referencias com alvo DIRETO consistente com a separacao ===")
print(f"{'separacao / modelo':<48} MedAPE   F2 NSElog Spear")
rows = []
for nome, b in cen.items():
    dd = cargas(h, ev, b); alvo = dd.SY_dir.to_numpy(); VD = dd.Vdir.to_numpy()
    print(f"-- {nome}: carga de base = {100*dd.SY_base.sum()/dd.SY_obs.sum():.1f}% do total; alvo soma {alvo.sum():.0f} t")
    for rot, x in (("MC  CANDIDATA", M.Emc["CANDIDATA"]), ("MFM CANDIDATA", M.Emfm("CANDIDATA", VD)), ("MC  ADOTADA", M.Emc["ADOTADA"]), ("MFM ADOTADA", M.Emfm("ADOTADA", VD)),
                   ("c*chuva", R), ("c*V_dir", VD)):
        m = metricas(alvo, x); print(f"   {rot:<45}{fmt(m)}"); rows.append(dict(separacao=nome, modelo=rot, **{q: m[q] for q in ("MedAPE", "F2", "NSElog", "Spear")}))
pd.DataFrame(rows).to_csv(os.path.join(WORK, "check2_separacoes_alvo_direto.csv"), index=False)

# ---------- diagnostico por evento (MFM candidata, alvo direto vs total)
mt = res[("TOTAL (SY_obs)", "MFM CANDIDATA")]; md = res[("DIRETO (SY_dir_obs)", "MFM CANDIDATA")]
ev_tab = pd.DataFrame({"ev": ev.ev, "obs_total": d0.SY_obs, "LOO_total": mt["loo"], "erro_total_%": 100 * (mt["loo"] / d0.SY_obs - 1),
                       "obs_dir": d0.SY_dir, "LOO_dir": md["loo"], "erro_dir_%": 100 * (md["loo"] / d0.SY_dir - 1)})
print("\n", ev_tab.round(1).to_string())

# ---------- hipotese de mesma concentracao: diagnostico fisico
print("\n=== Diagnostico da hipotese C_base = C_direta no instante ===")
cb = h.CSSBt.to_numpy(float); ok = np.isfinite(cb)
print("CSS_Bt informado em", ok.sum(), "horas; periodo", t[ok].min(), "a", t[ok].max())
print("CSS_Bt nas horas informadas: mediana", np.nanmedian(cb[ok]), "| CSS (mistura) nas mesmas horas: mediana", np.nanmedian(C[ok]), "| Q/Bt mediano nessas horas", np.nanmedian(Q[ok] / Bt[ok]))
print("corr(CSS_Bt, CSS) nessas horas:", np.corrcoef(cb[ok & np.isfinite(C)], C[ok & np.isfinite(C)])[0, 1], " iguais:", np.mean(np.isclose(cb[ok], C[ok])))
# concentracao pre-evento como limite para a base
rows = []
for _, r in ev.iterrows():
    jan = (t >= r.ini - pd.Timedelta(hours=48)) & (t < r.ini)
    cpre = np.nanmedian(C[jan]) if np.isfinite(C[jan]).any() else np.nan
    m = (t >= r.ini) & (t <= r.fim)
    base_pre = np.sum(np.minimum(Bt[m], Q[m]) * cpre * 3.6 / 1000)
    cflow = np.sum(Q[m] * C[m]) / np.sum(Q[m])
    rows.append(dict(ev=int(r.ev), CSS_pre_mgL=cpre, CSS_medio_evento_mgL=cflow, base_carga_pre_t=base_pre))
pre = pd.DataFrame(rows); pre["SY_dir_alt_t"] = d0.SY_obs - pre.base_carga_pre_t; pre["base_%carga_pre"] = 100 * pre.base_carga_pre_t / d0.SY_obs
print(pre.round(1).to_string())
alt = pre.SY_dir_alt_t.to_numpy()
print("limite alternativo (base com CSS pre-evento, mediana 48h antes): base =", f"{100*pre.base_carga_pre_t.sum()/d0.SY_obs.sum():.1f}% da carga total; mediana por evento {np.median(pre['base_%carga_pre']):.1f}%")
for rot, x in (("MFM CANDIDATA", M.Emfm("CANDIDATA", VD0)), ("MFM ADOTADA", M.Emfm("ADOTADA", VD0)), ("c*V_dir", VD0), ("c*chuva", R), ("MC CANDIDATA", M.Emc["CANDIDATA"])):
    print(f"   alvo direto-alternativo | {rot:<16}{fmt(metricas(alt, x))}")
pre.to_csv(os.path.join(WORK, "check2_hipotese_conc_pre_evento.csv"), index=False)
