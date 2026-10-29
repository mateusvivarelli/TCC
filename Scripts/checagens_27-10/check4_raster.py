from common import *
Pv, S20, KCLS, A = rasters()
S05 = s005(S20)
cn = lambda S: 25400.0 / (254.0 + S)
print("n pixels", S20.size)
q = [0, 1, 5, 25, 50, 75, 95, 99, 100]
print("S0,20 (mm): min %.1f  p5 %.1f  mediana %.1f  p95 %.1f  max %.1f  | em pol: min %.2f max %.2f" % (S20.min(), np.percentile(S20, 5), np.median(S20), np.percentile(S20, 95), S20.max(), S20.min()/25.4, S20.max()/25.4))
print("S0,05 (mm): min %.1f  p5 %.1f  mediana %.1f  p95 %.1f  max %.1f  | em pol: min %.2f max %.2f" % (S05.min(), np.percentile(S05, 5), np.median(S05), np.percentile(S05, 95), S05.max(), S05.min()/25.4, S05.max()/25.4))
print("CN-I (lambda 0,20): min %.1f  mediana %.1f  max %.1f" % (cn(S20).min(), np.median(cn(S20)), cn(S20).max()))
print("CN0,05 equivalente: min %.1f  mediana %.1f  max %.1f" % (cn(S05).min(), np.median(cn(S05)), cn(S05).max()))
r = S05 / S20
print("S05/S20: min %.2f  mediana %.2f  max %.2f ; fracao S05<S20: %.4f ; fracao S05>S20: %.4f" % (r.min(), np.median(r), r.max(), np.mean(S05 < S20), np.mean(S05 > S20)))
print("ponto de cruzamento S05=S20 em S = %.2f mm (%.3f pol)" % (25.4 * (1/1.33) ** (1/0.15), (1/1.33) ** (1/0.15)))
print("pixels com CN-I < 35 (fora da Tabela 4 de Woodward, S20 > 472 mm):", int((cn(S20) < 35).sum()), f"({100*np.mean(cn(S20)<35):.2f}%)")
print("pixels com CN-I < 20.71?? nao aplicavel; CN-I min", cn(S20).min())
# verificacao da implementacao contra a Tabela 4 de Woodward (pol)
tab = [(95, .526, 94.02, .636), (90, 1.111, 86.95, 1.501), (80, 2.5, 72.39, 3.815), (70, 4.286, 58.51, 7.091), (60, 6.667, 45.90, 11.785), (50, 10.0, 34.74, 18.787), (35, 18.571, 20.71, 38.285)]
print("verificacao Tabela 4 (S em pol): CN20 | S20 | S05 tab | S05 calc 1,33*S^1,15 | CN05 tab | CN05 eq.9 | CN05 de S05calc")
for c20, s20, c05, s05 in tab:
    calc = 1.33 * s20 ** 1.15; eq9 = 100 / (1.879 * (100 / c20 - 1) ** 1.15 + 1)
    print(f"  {c20:>3} | {s20:7.3f} | {s05:7.3f} | {calc:7.3f} | {c05:6.2f} | {eq9:6.2f} | {1000/(10+calc):6.2f}")
# outras equacoes de conversao citadas por Brandao et al. 2025 (mm)
for nome, f in (("Woodward 0,8187*S^1,15 (mm)", lambda s: 0.8187 * s ** 1.15), ("Brandao Eq.17 0,919*S^1,174", lambda s: 0.919 * s ** 1.174), ("Brandao Eq.19 0,917*S^1,170", lambda s: 0.917 * s ** 1.170)):
    o = f(S20); print(f"{nome:<32}: S05 mediana {np.median(o):7.1f} mm | razao mediana a Woodward-calc {np.median(o/S05):.3f} (min {np.min(o/S05):.3f} max {np.max(o/S05):.3f})")
# plausibilidade no escoamento: Q para P tipicos, S mediano
for P in (10, 25, 50, 100):
    for k, (S, lam) in (("adotada", (np.median(S20), .2)), ("candidata", (np.median(S05), .05))):
        Q = 0 if P <= lam * S else (P - lam * S) ** 2 / (P + (1 - lam) * S); print(f"P={P:>3} mm S={S:6.1f} lam={lam}: Q={Q:6.2f} mm ({k})", end=" | ")
    print()
# Pcrit (P onde Q0,05 = Q0,20) para S mediano
Sm20, Sm05 = np.median(S20), np.median(S05)
f = lambda P: qscs(np.array([P]), Sm05, .05)[0] - qscs(np.array([P]), Sm20, .2)[0]
from scipy.optimize import brentq
print("Pcrit (S mediano) = %.1f mm" % brentq(f, 5, 2000))
# fracao de pixel-eventos com P <= lambda*S
for k, S, lam in (("adotada", S20, .2), ("candidata", S05, .05)):
    print(f"{k}: fracao de pixel-evento sem escoamento (P<=lam*S) = {100*np.mean(Pv <= lam*S[None,:]):.1f}% ; lam*S mediano = {np.median(lam*S):.1f} mm")
