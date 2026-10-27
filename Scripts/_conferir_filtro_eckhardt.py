"""Confere a serie de vazao de base enviada pelo orientador (27/10/2026): filtro de Eckhardt (2005).
Resultado: reproduzida exatamente com alpha = 0,995 e BFImax = 0,70 (o cabecalho da planilha diz 0,58)."""
import sys
import numpy as np, pandas as pd
sys.stdout.reconfigure(encoding="utf-8")
p = r"C:\TCC\Dados Iniciais\serie_Q_Qb_Qquick_Eckhardt_orientador.xlsx"
a = pd.read_excel(p).iloc[:, :4]; a.columns = ["Data", "Q", "Qb", "Qq"]
Q = a.Q.to_numpy(float); ref = a.Qb.to_numpy(float)
print("Qb + Qquick = Q ?", np.abs(a.Qb + a.Qq - a.Q).max())
print("horas com Qb == Q:", np.mean(np.isclose(ref, Q)))

def eck(Q, al, bfi, b0=None, rev=False):
    q = Q[::-1] if rev else Q
    b = np.zeros_like(q); b[0] = q[0] if b0 is None else b0
    for i in range(1, len(q)):
        b[i] = min(((1 - bfi) * al * b[i - 1] + (1 - al) * bfi * q[i]) / (1 - al * bfi), q[i])
    return b[::-1] if rev else b

def nota(b, nome):
    d = np.abs(b - ref); print(f"{nome:<46} r={np.corrcoef(b, ref)[0,1]:.6f}  max|dif|={d.max():.4f}  % horas iguais (1e-4)={100*np.mean(d<1e-4):.1f}")

nota(eck(Q, 0.995, 0.58), "direto, b0 = Q0")
nota(eck(Q, 0.995, 0.58, b0=0.58 * Q[0]), "direto, b0 = BFImax*Q0")
nota(eck(Q, 0.995, 0.58, rev=True), "de tras para frente")
f = eck(Q, 0.995, 0.58); nota(np.minimum(f, eck(Q, 0.995, 0.58, rev=True)), "min(ida, volta)")
nota(eck(eck(Q, 0.995, 0.58), 0.995, 0.58), "duas passadas")
# busca do alpha e BFImax que melhor reproduzem
best = None
for al in (0.98, 0.985, 0.99, 0.993, 0.995, 0.997, 0.998, 0.999):
    for bfi in np.arange(0.40, 0.81, 0.02):
        b = eck(Q, al, bfi); e = np.sqrt(np.mean((b - ref) ** 2))
        if best is None or e < best[0]: best = (e, al, bfi, np.corrcoef(b, ref)[0, 1])
print(f"melhor ajuste direto: alpha={best[1]} BFImax={best[2]:.2f} RMSE={best[0]:.4f} r={best[3]:.6f}")
# a serie comeca em 14/11/2018: talvez o filtro tenha sido rodado numa serie mais longa (aquecimento)
i = np.argmax(np.abs(eck(Q, 0.995, 0.58) - ref)); print("maior diferenca na hora", a.Data[i], "Q =", Q[i], "Qb ref =", ref[i])
d = np.abs(eck(Q, 0.995, 0.58) - ref)
for k in (100, 500, 2000, 5000, 10000, 20000):
    print(f"  max|dif| a partir da hora {k}: {d[k:].max():.4f}")
b70 = eck(Q, 0.995, 0.70)
print(f"\nalpha 0,995 / BFImax 0,70: max|dif| com a planilha = {np.abs(b70 - ref).max():.2e}")
print(f"BFI global com 0,70: {b70.sum()/Q.sum():.3f}  | com 0,58: {eck(Q,0.995,0.58).sum()/Q.sum():.3f}")
