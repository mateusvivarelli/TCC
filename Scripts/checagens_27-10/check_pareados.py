"""Comparacoes pareadas por evento (diferenca de erro percentual LOO) para os cenarios das checagens 1 e 2. Bootstrap de eventos."""
from common import *
rng = np.random.default_rng(27102026)
ev = le_eventos(); h = le_serie(); M = Modelo(ev); R = ev.R.to_numpy()
Bt = h.Bt.to_numpy(float)
cen = {"Bt fornecido": Bt, "(i) Eck 0,995/0,70": eck_serie(h, 0.995, 0.70), "(ii) Eck 0,995/0,58": eck_serie(h, 0.995, 0.58),
       "(iii) Eck 0,995/0,80": eck_serie(h, 0.995, 0.80), "(iv) Eck 0,98/0,70": eck_serie(h, 0.98, 0.70), "(v) Lyne-Hollick": lh_serie(h)}


def par(a, b, rot):
    d = a["ape"] - b["ape"]; bs = [np.median(rng.choice(d, N)) for _ in range(4000)]
    return f"{rot:<44} melhora em {np.sum(d < 0):>2}/17 | dif. mediana {np.median(d):+6.1f} pt | IC95% [{np.percentile(bs, 2.5):+6.1f}; {np.percentile(bs, 97.5):+6.1f}]"


print("=== Checagem 1 (alvo total): pareado ===")
for nome, b in cen.items():
    dd = cargas(h, ev, b); VD = dd.Vdir.to_numpy(); SY = dd.SY_obs.to_numpy()
    mc, ma, mv, mr = metricas(SY, M.Emfm("CANDIDATA", VD)), metricas(SY, M.Emfm("ADOTADA", VD)), metricas(SY, VD), metricas(SY, R)
    print(f"-- {nome}")
    print("   ", par(mc, ma, "MFM candidata - MFM adotada"))
    print("   ", par(mc, mv, "MFM candidata - c*V_dir"))
print("\n=== Checagem 2 (alvo direto, separacao consistente): pareado ===")
for nome in ("Bt fornecido", "(ii) Eck 0,995/0,58", "(v) Lyne-Hollick"):
    dd = cargas(h, ev, cen[nome]); VD = dd.Vdir.to_numpy(); SY = dd.SY_dir.to_numpy()
    mc, ma, mv, mr = metricas(SY, M.Emfm("CANDIDATA", VD)), metricas(SY, M.Emfm("ADOTADA", VD)), metricas(SY, VD), metricas(SY, R)
    print(f"-- {nome}")
    print("   ", par(mc, ma, "MFM candidata - MFM adotada"))
    print("   ", par(mc, mv, "MFM candidata - c*V_dir"))
    print("   ", par(mc, mr, "MFM candidata - c*chuva"))
    print("   ", par(ma, mr, "MFM adotada - c*chuva"))
    print("   ", par(metricas(SY, M.Emc["CANDIDATA"]), mr, "MC candidata - c*chuva"))
print("\n=== alvo total, Bt fornecido (comparacao) ===")
dd = cargas(h, ev, Bt); VD = dd.Vdir.to_numpy(); SY = dd.SY_obs.to_numpy(); mr = metricas(SY, R)
print("   ", par(metricas(SY, M.Emfm("ADOTADA", VD)), mr, "MFM adotada - c*chuva"))
print("   ", par(metricas(SY, M.Emc["CANDIDATA"]), mr, "MC candidata - c*chuva"))
