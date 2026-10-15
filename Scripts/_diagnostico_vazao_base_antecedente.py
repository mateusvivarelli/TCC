"""
DIAGNOSTICO (15/10/2026) - dá para consertar o volume 'direto'?

(a) Sensibilidade do alvo: escoamento direto por 3 separacoes de vazao de base
    (coluna Bt do projeto; filtro Lyne-Hollick; linha reta de Qb_inicio).
(b) A vazao/umidade ANTES do evento (Qb_inicio, chuva antecedente) explica o erro
    do SCS-CN no volume direto? Regressao com leave-one-out (so informacao
    disponivel antes do evento = previsao legitima).
(c) Modelo 'direto SCS-CN + vazao de base prevista' contra o volume TOTAL.
"""
import os
import sys

import numpy as np
import pandas as pd
from osgeo import gdal

gdal.UseExceptions()
sys.stdout.reconfigure(encoding="utf-8")
BASE = r"C:\TCC"; DI = os.path.join(BASE, "Dados Iniciais")


def le(p):
    ds = gdal.Open(p); b = ds.GetRasterBand(1)
    a = b.ReadAsArray().astype(np.float64); nd = b.GetNoDataValue()
    ok = np.isfinite(a) & (a > -1e30)
    if nd is not None:
        ok &= a != nd
    return np.where(ok, a, np.nan), ds


K, ds0 = le(os.path.join(DI, "K_raster.tif"))
gt = ds0.GetGeoTransform(); ny, nx = K.shape
o = gdal.Warp("", gdal.Open(os.path.join(DI, "S - Seco.tif")), format="MEM", width=nx, height=ny,
              outputBounds=(gt[0], gt[3] + ny * gt[5], gt[0] + nx * gt[1], gt[3]), dstSRS=ds0.GetProjection(),
              resampleAlg=gdal.GRA_NearestNeighbour)
S = o.GetRasterBand(1).ReadAsArray().astype(np.float64); S = np.where(S > -1e30, S, np.nan)
mq = np.isfinite(S)

ev = pd.read_excel(os.path.join(DI, "eventos_processados_manuais.xlsx"), sheet_name="Sheet1").iloc[:18]
h = pd.read_excel(os.path.join(DI, "Dados_finais_histereses_corrigido.xlsx"), sheet_name="Planilha1").iloc[:, :8]
h.columns = ["Data", "P1", "P2", "Ptot", "Q", "CSS", "Bt", "CSSBt"]; h["Data"] = pd.to_datetime(h["Data"]); h = h.set_index("Data")

# --- filtro Lyne-Hollick (alpha=0,925, 3 passadas) na serie horaria continua
q = h["Q"].interpolate(limit=24).to_numpy()


def lyne_hollick(q, a=0.925, passes=3):
    def fwd(x):
        f = np.zeros_like(x); f[0] = 0
        for t in range(1, len(x)):
            if np.isnan(x[t]) or np.isnan(x[t - 1]):
                f[t] = 0; continue
            f[t] = max(0.0, a * f[t - 1] + (1 + a) / 2 * (x[t] - x[t - 1]))
            f[t] = min(f[t], x[t])
        return f
    out = q.copy(); x = q.copy()
    for k in range(passes):
        f = fwd(x if k % 2 == 0 else x[::-1]) if k == 0 else fwd(x if k % 2 == 0 else x[::-1])
        if k % 2 == 1:
            f = f[::-1]
        xin = x if k % 2 == 0 else x
        x = np.where(np.isnan(xin), np.nan, xin - f)   # base restante
    return np.where(np.isnan(q), np.nan, np.minimum(x, q))


bf_lh = pd.Series(lyne_hollick(q), index=h.index)

N = 17
rows = []
Pr = []
for n in range(1, N + 1):
    r = ev.iloc[0 if n == 1 else n]; w = h.loc[r["Inicio"]:r["Fim"]]
    wl = bf_lh.loc[r["Inicio"]:r["Fim"]]
    TR = w.Q.sum() * 3600
    rows.append(dict(ev=n, TR=TR, V_bt=(w.Q - w.Bt).sum() * 3600, V_lh=(w.Q - wl).sum() * 3600,
                     V_reta=(w.Q - r["Qb_inicio"]).clip(lower=0).sum() * 3600,
                     Qb0=r["Qb_inicio"], dur=r["Duracao_horas"], R=r["Chuva_evento_mm"],
                     Ap5=r["Ap5_pond_mm"], Ap10=r["Ap10_pond_mm"], Ap14=r["Ap14_pond_mm"], Bt_vol=w.Bt.sum() * 3600))
    Pr.append(le(os.path.join(BASE, f"Evento {n}", f"ChuvaIDW{n}.tif"))[0])
d = pd.DataFrame(rows)
nse = lambda o_, s_: 1 - np.sum((o_ - s_) ** 2) / np.sum((o_ - o_.mean()) ** 2)

print("=" * 96)
print("(a) ESCOAMENTO DIRETO conforme o metodo de separacao da vazao de base (soma dos 17 eventos, m3)")
for c_, nome in [("TR", "volume total (sem separar)"), ("V_bt", "separacao Bt do projeto"), ("V_lh", "filtro Lyne-Hollick (0,925; 3 passadas)"),
                 ("V_reta", "linha reta em Qb_inicio")]:
    print(f"   {nome:<42} {d[c_].sum():>14,.0f}  ({100*d[c_].sum()/d.TR.sum():5.1f}% do total)")
print(f"   correlacao por evento: Bt x LH = {np.corrcoef(d.V_bt, d.V_lh)[0,1]:.3f} | Bt x reta = {np.corrcoef(d.V_bt, d.V_reta)[0,1]:.3f}")
print(f"   razao V_lh/V_bt por evento: min={np.min(d.V_lh/d.V_bt):.2f} max={np.max(d.V_lh/d.V_bt):.2f}")

mask = mq & np.isfinite(K)
for lam in (0.05, 0.10, 0.20):
    d[f"Vc{lam}"] = [np.nansum(np.where(np.isfinite(Pr[i]) & mq, np.where(Pr[i] <= lam * S, 0, (Pr[i] - lam * S) ** 2 / (Pr[i] + (1 - lam) * S)), np.nan)) / 1000 * 900 for i in range(N)]


def loo_log(y, X, nome, alvo_nome):
    """regressao em log com leave-one-out; devolve NSE (volume em m3)"""
    ly = np.log(y); Xm = np.column_stack([np.ones(len(y))] + [np.log(x) for x in X])
    pred = np.zeros(len(y))
    for i in range(len(y)):
        m = np.arange(len(y)) != i
        b = np.linalg.lstsq(Xm[m], ly[m], rcond=None)[0]; pred[i] = np.exp(Xm[i] @ b)
    b = np.linalg.lstsq(Xm, ly, rcond=None)[0]; insample = np.exp(Xm @ b)
    err = 100 * (pred - y) / y
    print(f"   {nome:<58} NSE in={nse(y, insample):6.3f}  LOO={nse(y, pred):6.3f}  erro abs LOO={np.abs(err).mean():5.1f}%")
    return pred


print("=" * 96)
print("(b) PREVER O ESCOAMENTO DIRETO (alvo: separacao Bt) - regressoes em log, com leave-one-out")
y = d.V_bt.to_numpy()
print("   referencia: SCS-CN cru (sem ajuste)")
for lam in (0.05, 0.20):
    print(f"     SCS-CN lambda={lam:<5} NSE={nse(y, d[f'Vc{lam}'].to_numpy()):6.3f}  erro abs={np.mean(np.abs(100*(d[f'Vc{lam}']-y)/y)):5.1f}%")
print("   regressoes (so informacao disponivel antes/durante a chuva):")
loo_log(y, [d["Vc0.2"].to_numpy()], "V_dir ~ V_SCS(lambda=0,20)", "")
loo_log(y, [d["Vc0.2"].to_numpy(), d.Qb0.to_numpy()], "V_dir ~ V_SCS(0,20) + Qb_inicio", "")
loo_log(y, [d["Vc0.05"].to_numpy(), d.Qb0.to_numpy()], "V_dir ~ V_SCS(0,05) + Qb_inicio", "")
loo_log(y, [d.R.to_numpy()], "V_dir ~ chuva do evento", "")
loo_log(y, [d.R.to_numpy(), d.Qb0.to_numpy()], "V_dir ~ chuva + Qb_inicio", "")
loo_log(y, [d.R.to_numpy(), d.Ap5.to_numpy() + 1e-3], "V_dir ~ chuva + chuva antecedente 5d", "")
loo_log(y, [d.R.to_numpy(), d.Qb0.to_numpy(), d.dur.to_numpy()], "V_dir ~ chuva + Qb_inicio + duracao", "")
print("   correlacao (log) do fator f = V_dir/V_SCS(0,20) com preditores antes do evento:")
f = np.log(y / d["Vc0.2"].to_numpy())
for c_ in ["Qb0", "Ap5", "Ap10", "Ap14", "R", "dur"]:
    print(f"     {c_:<6} r = {np.corrcoef(np.log(d[c_] + 1e-3), f)[0,1]:+.2f}")

print("=" * 96)
print("(c) VOLUME TOTAL previsto = escoamento direto (SCS-CN) + vazao de base prevista")
tot = d.TR.to_numpy()
print("   a vazao de base do evento (soma Bt) e proporcional a Qb_inicio * duracao?")
xb = (d.Qb0 * d.dur * 3600).to_numpy(); kb = np.sum(xb * d.Bt_vol) / np.sum(xb ** 2)
print(f"     razao media Bt_vol/(Qb_inicio*dur*3600) = {kb:.2f}; correlacao = {np.corrcoef(xb, d.Bt_vol)[0,1]:.3f}")
for lam in (0.05, 0.10, 0.20):
    pred = d[f"Vc{lam}"].to_numpy() + kb * xb
    e = 100 * (pred - tot) / tot
    print(f"     direto SCS-CN(lambda={lam:<4}) + {kb:.2f}*Qb_inicio*dur : erro medio={e.mean():+6.1f}% abs={np.abs(e).mean():5.1f}%  NSE={nse(tot, pred):6.3f}")
print("=" * 96)
