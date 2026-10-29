"""Modulo comum das checagens (27/10/2026). Somente LE de C:/TCC; grava apenas na pasta de trabalho."""
import os, re, sys
import numpy as np, pandas as pd
from osgeo import gdal
from scipy.stats import spearmanr
gdal.UseExceptions()
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
WORK = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(WORK, "..", ".."))  # raiz do repositório
DI = os.path.join(BASE, "Dados Iniciais")
COEF, EXPO, N = 11.8, 0.56, 17


def le(p):
    ds = gdal.Open(p); b = ds.GetRasterBand(1)
    a = b.ReadAsArray().astype(np.float64); nd = b.GetNoDataValue()
    ok = np.isfinite(a) & (np.abs(a) < 1e30)
    if nd is not None:
        ok &= a != nd
    return np.where(ok, a, np.nan), ds


# ---------------------------------------------------------------- eventos (tab_eventos.md)
def le_eventos():
    rows = []
    for ln in open(os.path.join(BASE, "TCC_Texto", "tabelas", "tab_eventos.md"), encoding="utf-8"):
        c = [x.strip() for x in ln.strip().strip("|").split("|")]
        if len(c) >= 11 and c[0].isdigit():
            f = lambda s: pd.to_datetime(s.replace("h", ":00"), format="%d/%m/%y %H:%M")
            rows.append(dict(ev=int(c[0]), ini=f(c[1]), fim=f(c[2]), R=float(c[6].replace(",", ".")), RI=float(c[7].replace(",", "."))))
    return pd.DataFrame(rows)


def le_serie():
    h = pd.read_excel(os.path.join(DI, "Dados_finais_histereses_corrigido.xlsx"), sheet_name="Planilha1").iloc[:, :8]
    h.columns = ["Data", "P1", "P2", "Ptot", "Q", "CSS", "Bt", "CSSBt"]
    return h


# ---------------------------------------------------------------- cargas por evento
def cargas(h, ev, base):
    """base: array (len(h)) de vazao de base usada na separacao. Retorna DataFrame por evento."""
    t = pd.DatetimeIndex(h.Data); Q = h.Q.to_numpy(float); C = h.CSS.to_numpy(float)
    out = []
    for _, r in ev.iterrows():
        m = (t >= r.ini) & (t <= r.fim)
        q, c, b = Q[m], C[m], base[m]
        out.append(dict(ev=r.ev, nh=int(m.sum()), SY_obs=np.sum(q * c * 3.6 / 1000), TR=np.sum(q * 3600),
                        Vbase=np.sum(b * 3600), SY_dir=np.sum((q - b) * c * 3.6 / 1000), SY_base=np.sum(np.minimum(b, q) * c * 3.6 / 1000)))
    d = pd.DataFrame(out); d["Vdir"] = d.TR - d.Vbase
    return d


# ---------------------------------------------------------------- filtros de vazao de base
def eckhardt(Q, a, bfi, b0):
    b = np.zeros_like(Q); b[0] = b0
    for i in range(1, len(Q)):
        b[i] = min(((1 - bfi) * a * b[i - 1] + (1 - a) * bfi * Q[i]) / (1 - a * bfi), Q[i])
    return b


def eck_serie(h, a, bfi):
    Q = h.Q.to_numpy(float); Bt = h.Bt.to_numpy(float); ok = np.where(np.isfinite(Q))[0]; i0 = ok[0]
    out = np.full(len(Q), np.nan); out[i0:] = eckhardt(Q[i0:], a, bfi, Bt[i0]); return out


def _lh_pass(x, alpha, rev=False):
    """uma passada de Lyne-Hollick sobre x; devolve (rapido, base=x-rapido)."""
    y = x[::-1] if rev else x
    q = np.zeros_like(y)
    for i in range(1, len(y)):
        qi = alpha * q[i - 1] + (1 + alpha) / 2 * (y[i] - y[i - 1])
        q[i] = min(max(qi, 0.0), y[i])
    b = y - q
    return (q[::-1], b[::-1]) if rev else (q, b)


def lh_serie(h, alpha=0.925):
    Q = h.Q.to_numpy(float); ok = np.where(np.isfinite(Q))[0]; i0 = ok[0]
    x = Q[i0:].copy()
    q1, b1 = _lh_pass(x, alpha)             # frente sobre Q
    q2, b2 = _lh_pass(b1, alpha, rev=True)  # tras sobre a base da passada 1
    q3, b3 = _lh_pass(b2, alpha)            # frente sobre a base da passada 2
    out = np.full(len(Q), np.nan); out[i0:] = b3; return out


# ---------------------------------------------------------------- rasters
_cache = os.path.join(WORK, "cache_rasters.npz")


def rasters():
    if os.path.exists(_cache):
        z = np.load(_cache); return z["Pv"], z["S20"], z["KCLS"], float(z["A"])
    K, ds0 = le(os.path.join(DI, "K_raster.tif")); C, _ = le(os.path.join(DI, "C_raster.tif")); LS, _ = le(os.path.join(DI, "LS_moore.tif"))
    ref = gdal.Open(os.path.join(BASE, "Evento 11", "ChuvaIDW11.tif"))
    gt = ref.GetGeoTransform(); ny, nx = ref.RasterYSize, ref.RasterXSize
    assert K.shape == (ny, nx), (K.shape, ny, nx)
    A = abs(gt[1] * gt[5])
    o = gdal.Warp("", gdal.Open(os.path.join(DI, "S - Seco.tif")), format="MEM", width=nx, height=ny,
                  outputBounds=(gt[0], gt[3] + ny * gt[5], gt[0] + nx * gt[1], gt[3]), dstSRS=ref.GetProjection(), resampleAlg=gdal.GRA_NearestNeighbour)
    S = o.GetRasterBand(1).ReadAsArray().astype(np.float64); S = np.where(np.abs(S) < 1e30, S, np.nan)
    nd = o.GetRasterBand(1).GetNoDataValue()
    if nd is not None:
        S = np.where(S == nd, np.nan, S)
    valido = np.isfinite(S) & np.isfinite(K) & np.isfinite(C) & np.isfinite(LS)
    print("pixels validos:", valido.sum(), "A =", A)
    Pv = np.array([le(os.path.join(BASE, f"Evento {n}", f"ChuvaIDW{n}.tif"))[0][valido] for n in range(1, N + 1)])
    KCLS = (K * C * LS)[valido]; S20 = S[valido]
    np.savez(_cache, Pv=Pv, S20=S20, KCLS=KCLS, A=A)
    return Pv, S20, KCLS, A


def s005(S20mm):
    return 25.4 * 1.33 * (S20mm / 25.4) ** 1.15


def qscs(P, S, lam):
    return np.where(P <= lam * S, 0.0, (P - lam * S) ** 2 / (P + (1 - lam) * S))


def E_unit(Q, P, KCLS, A, RI, R):
    pr = Q / 1000.0 * A * (RI / R) / 3600.0
    return COEF * np.maximum(Q * pr * A, 0.0) ** EXPO * KCLS


# ---------------------------------------------------------------- metricas
def fit1(x, y):
    return np.exp(np.mean(np.log(y) - np.log(x)))


def metricas(obs, x):
    """LOO com c em log. Retorna dict com MedAPE, fator 2, NSE-log, Spearman, e a previsao LOO."""
    ids = np.arange(len(obs))
    loo = np.array([fit1(x[ids != i], obs[ids != i]) * x[i] for i in ids])
    ape = 100 * np.abs(loo - obs) / obs
    lo, ls = np.log(obs), np.log(np.clip(loo, 1e-12, None))
    r = loo / obs
    return dict(MedAPE=np.median(ape), F2=100 * np.mean((r >= .5) & (r <= 2)), NSElog=1 - np.sum((ls - lo) ** 2) / np.sum((lo - lo.mean()) ** 2),
                Spear=spearmanr(obs, loo)[0], loo=loo, ape=ape, c=fit1(x, obs))


def fmt(m):
    return f"{m['MedAPE']:6.1f} {m['F2']:5.0f} {m['NSElog']:6.2f} {m['Spear']:5.2f}"


class Modelo:
    """Pre-calcula E (MC) para adotada e candidata; MFM para um dado vetor de V_dir."""

    def __init__(self, ev):
        self.Pv, self.S20, self.KCLS, self.A = rasters()
        self.R = ev.R.to_numpy(); self.RI = ev.RI.to_numpy()
        self.cfg = {"ADOTADA": (self.S20, 0.20), "CANDIDATA": (s005(self.S20), 0.05)}
        self.Q = {k: [qscs(self.Pv[i], S, lam) for i in range(N)] for k, (S, lam) in self.cfg.items()}
        self.Vscs = {k: np.array([q.sum() / 1000.0 * self.A for q in self.Q[k]]) for k in self.cfg}
        self.Emc = {k: np.array([E_unit(self.Q[k][i], self.Pv[i], self.KCLS, self.A, self.RI[i], self.R[i]).sum() for i in range(N)]) for k in self.cfg}

    def Emfm(self, k, V):
        out = np.zeros(N)
        for i in range(N):
            Q = np.minimum(V[i] / self.Vscs[k][i] * self.Q[k][i], self.Pv[i])
            out[i] = E_unit(Q, self.Pv[i], self.KCLS, self.A, self.RI[i], self.R[i]).sum()
        return out
