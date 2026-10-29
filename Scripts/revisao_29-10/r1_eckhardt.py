"""Revisao 29/10: reproduz o filtro de Eckhardt contra a serie do orientador e contra o Bt da planilha de histereses."""
import numpy as np, pandas as pd
s = pd.read_excel("Dados Iniciais/serie_Q_Qb_Qquick_Eckhardt_orientador.xlsx"); s.columns = ["data", "Q", "Qb", "Qq", "x", "nota"]
h = pd.read_excel("Dados Iniciais/Dados_finais_histereses_corrigido.xlsx").iloc[:, [0, 4, 6]]; h.columns = ["data", "Q", "Bt"]
def eck(Q, a, B):
    b = np.empty_like(Q); b[0] = Q[0]
    for t in range(1, len(Q)):
        b[t] = min(((1 - B) * a * b[t-1] + (1 - a) * B * Q[t]) / (1 - a * B), Q[t])
    return b
Q = s.Q.values.astype(float)
print("NaN em Q do orientador:", np.isnan(Q).sum(), "n =", len(Q))
for B in (0.58, 0.70):
    b = eck(Q, 0.995, B)
    print(f"BFImax {B}: max|b - Qb orientador| = {np.nanmax(np.abs(b - s.Qb.values)):.4f}; BFI = {np.nansum(b)/np.nansum(Q):.3f}")
m = s.merge(h, on="data", suffixes=("_o", "_h"))
print("linhas em comum:", len(m), "max|Q_o - Q_h|", np.nanmax(np.abs(m.Q_o - m.Q_h)))
for B in (0.58, 0.70):
    b = eck(Q, 0.995, B); mm = pd.DataFrame({"data": s.data, "b": b}).merge(h, on="data")
    dif = np.abs(mm.b - mm.Bt); print(f"BFImax {B} x Bt da histerese: mediana {np.nanmedian(dif):.4f} max {np.nanmax(dif):.4f} m3/s")
print("Bt histerese x Qb orientador: max", np.nanmax(np.abs(m.Bt - m.Qb)))
print("BFI da planilha de histereses (Bt/Q):", np.nansum(h.Bt)/np.nansum(h.Q.where(h.Bt.notna())))
