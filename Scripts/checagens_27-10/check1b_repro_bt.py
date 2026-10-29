"""Diagnostico: por que a diferenca mediana da reproducao de Bt (1,6e-3) nao e ~2e-4? Compara com a serie original do orientador."""
from common import *
h = le_serie(); Q = h.Q.to_numpy(float); Bt = h.Bt.to_numpy(float); v = np.isfinite(Q)
o = pd.read_excel(os.path.join(DI, "serie_Q_Qb_Qquick_Eckhardt_orientador.xlsx")).iloc[:, :4]; o.columns = ["Data", "Q", "Qb", "Qq"]
print("serie do orientador:", len(o), o.Data.iloc[0], o.Data.iloc[-1])
m = h.assign(Data=pd.to_datetime(h.Data)).merge(o.assign(Data=pd.to_datetime(o.Data)), on="Data", suffixes=("", "_o"))
print("horas comuns:", len(m), " |Q-Q_o| max:", np.nanmax(np.abs(m.Q - m.Q_o)), " |Bt-Qb_o| mediana:", np.nanmedian(np.abs(m.Bt - m.Qb)), "max:", np.nanmax(np.abs(m.Bt - m.Qb)))
print("diferencas de Q > 1e-6:", int((np.abs(m.Q - m.Q_o) > 1e-6).sum()))
# Eckhardt sobre Q do arquivo Dados_finais, variantes de b0
i0 = np.where(v)[0][0]
for rot, b0 in (("b0=Bt", Bt[i0]), ("b0=Q0", Q[i0]), ("b0=0,7*Q0", 0.7 * Q[i0])):
    b = np.full(len(Q), np.nan); b[i0:] = eckhardt(Q[i0:], 0.995, 0.70, b0); d = np.abs(b[v] - Bt[v])
    print(f"{rot:<12}: mediana|dif|={np.median(d):.2e} max={d.max():.2e}; dif em 1.000 h apos inicio: mediana={np.median(d[1000:]):.2e}")
# usando a serie do orientador (Q_o) e o filtro
Qo = o.Q.to_numpy(float); bo = eckhardt(Qo, 0.995, 0.70, Qo[0]); print("serie orientador: max|filtro - Qb|:", np.abs(bo - o.Qb.to_numpy(float)).max())
d = np.abs(m.Bt - m.Qb); print("onde Bt difere de Qb_o: horas com dif>1e-3:", int((d > 1e-3).sum()), "de", len(d))
# usando Q da planilha Dados_finais e inicio na mesma hora do orientador
