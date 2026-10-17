"""
COMPARACAO COM A IC (Vivarelli et al., 2025) - 15/10/2026.

A IC: MUSLE CONCENTRADA, Y = alfa*(D*qp)^beta * K*LS*C*P com D = volume do evento (m3) e qp = vazao de pico
MEDIDOS, K = 0,031, LS = 0,536, C = 0,267 (medias da bacia, Tabela 3 do artigo), P = 1; alfa e beta ajustados nos 17 eventos
(publicado: alfa = 0,277, beta = 0,807; erro % medio -4,15%, faixa -60,01% a +37,14%; com os coeficientes originais 11,8 e 0,56:
erro medio 29,58% de subestimativa, maximo 57,28%).
Este script (1) tenta reproduzir esses numeros, (2) refaz a calibracao da IC (alfa, beta) como ajuste de lei de potencia em log,
(3) avalia a IC com as mesmas metricas do B (LOO aninhado, MedAPE, fator 2, NSE em log, Spearman).
"""
import os
import sys

import numpy as np
import pandas as pd
from scipy.optimize import least_squares
from scipy.stats import spearmanr

sys.stdout.reconfigure(encoding="utf-8")
DI = r"C:\TCC\Dados Iniciais"
N = 17
ev = pd.read_excel(os.path.join(DI, "eventos_processados_manuais.xlsx"), sheet_name="Sheet1").iloc[:18]
R_ = [ev.iloc[0 if n == 1 else n] for n in range(1, N + 1)]
SY = np.array([float(r["SYY_t"]) for r in R_]); V = np.array([float(r["T_R_m3"]) for r in R_]); QP = np.array([float(r["Q_pico"]) for r in R_])
KLSC = 0.031 * 0.536 * 0.267
ids = np.arange(N)
pct = lambda s: 100 * (s - SY) / SY
ape = lambda s: 100 * np.abs(s - SY) / SY
f2 = lambda s: 100 * np.mean((s / SY >= 0.5) & (s / SY <= 2.0))
nlog = lambda y, s: 1 - np.sum((np.log(y) - np.log(np.clip(s, 1e-6, None))) ** 2) / np.sum((np.log(y) - np.log(y).mean()) ** 2)
nse = lambda y, s: 1 - np.sum((y - s) ** 2) / np.sum((y - y.mean()) ** 2)

print("=" * 110)
print("(1) REPRODUCAO DOS NUMEROS PUBLICADOS")
for nome, a_, b_ in (("coeficientes originais (11,8; 0,56)", 11.8, 0.56), ("calibrados publicados (0,277; 0,807)", 0.277, 0.807)):
    for un, d in (("D em m3", V), ("D em 10^3 m3", V / 1e3), ("D em 10^6 m3", V / 1e6)):
        s_ = a_ * (d * QP) ** b_ * KLSC
        e = pct(s_)
        print(f"  {nome:<38} {un:<13} erro medio {e.mean():+8.2f}% | min {e.min():+8.2f}% | max {e.max():+8.2f}%")
print("  alvo publicado: originais -29,58% (max 57,28%) | calibrados -4,15% (faixa -60,01% a +37,14%)")

print("=" * 110)
print("(2) CALIBRACAO ALFA, BETA REFEITA (K, LS, C medios da IC; D = T_R_m3 e qp = Q_pico medidos)")
x = np.log(V * QP); y = np.log(SY / KLSC)
b1, a1 = np.polyfit(x, y, 1)
print(f"  regressao em log (ln(SY/KLSC) ~ ln(D*qp)): alfa = {np.exp(a1):.4f}  beta = {b1:.4f}")
def fit_ab(xx, yy):
    return np.polyfit(xx, yy, 1)[::-1]
def lin_fit(Dq, SYv):
    f = lambda p: (p[0] * Dq ** p[1] * KLSC - SYv)
    r = least_squares(f, [0.3, 0.8], bounds=([1e-6, 0.1], [50, 1.5]), x_scale="jac"); return r.x
pl = lin_fit(V * QP, SY)
print(f"  minimos quadrados lineares (em t): alfa = {pl[0]:.4f}  beta = {pl[1]:.4f}")
rel = lambda p: (p[0] * (V * QP) ** p[1] * KLSC - SY) / SY
r = least_squares(rel, [0.3, 0.8], bounds=([1e-6, 0.1], [50, 1.5]), x_scale="jac")
print(f"  minimos quadrados do erro relativo: alfa = {r.x[0]:.4f}  beta = {r.x[1]:.4f}")

print("=" * 110)
print("(3) METRICAS - IC reproduzida (lei de potencia, 2 parametros) x modelos do TCC; alvo carga total; LOO aninhado; calibracao em log")
def loo_power(Dq):
    out = np.zeros(N)
    for i in range(N):
        m = ids != i; b, a = np.polyfit(np.log(Dq[m]), np.log(SY[m] / KLSC), 1); out[i] = np.exp(a) * Dq[i] ** b * KLSC
    return out
b, a = np.polyfit(np.log(V * QP), np.log(SY / KLSC), 1); sim_ic = np.exp(a) * (V * QP) ** b * KLSC
loo_ic = loo_power(V * QP)
orig = 11.8 * (V * QP) ** 0.56 * KLSC
pub = 0.277 * (V * QP) ** 0.807 * KLSC
print(f"{'modelo':<66} {'MedAPE':>7} {'fator2':>7} {'NSE-log':>8} {'Spearman':>8} {'NSE lin':>8} {'viesM%':>8} {'faixa %':>16}")
def lin(nome, s, loo=None):
    z = loo if loo is not None else s
    print(f"{nome:<66} {np.median(ape(z)):7.1f} {f2(z):7.0f} {nlog(SY, z):8.3f} {spearmanr(SY, z)[0]:8.3f} {nse(SY, z):8.3f} {pct(z).mean():+8.1f} {pct(z).min():+7.0f} a {pct(z).max():+5.0f}")
lin("IC com coeficientes ORIGINAIS de Williams (D, qp medidos)", orig)
lin("IC calibrada publicada (alfa 0,277; beta 0,807), in-sample", pub)
lin("IC calibrada refeita em log, in-sample (alfa, beta ajustados)", sim_ic)
lin("IC calibrada refeita em log, LOO (alfa e beta sem o evento)", sim_ic, loo_ic)
print(f"   (IC refeita: alfa={np.exp(a):.4f}, beta={b:.4f})")
print("  --- modelos do TCC (leave-one-out, calibracao em log), ja calculados nos scripts anteriores:")
print("  B, N1  so chuva e vazao inicial (previsao)                          MedAPE 32,6 | fator2 71 | NSE-log 0,477 | Spearman 0,716 | NSE lin LOO -0,636")
print("  B, N3  volume direto medido + base prevista (como a IC: entrada medida) MedAPE 34,1 | fator2 94 | NSE-log 0,689 | Spearman 0,811 | NSE lin LOO  0,547")
print("  B, N4  volume direto e base medidos (teto)                           MedAPE 13,6 | fator2 94 | NSE-log 0,868 | Spearman 0,850 | NSE lin LOO  0,784")
print("=" * 110)
