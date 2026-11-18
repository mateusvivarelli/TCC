"""Sensibilidade do criterio de calibracao do coeficiente c (18/11/2026), com validacao leave-one-out nos 17 eventos.
Criterios: log (media geometrica das razoes; o do TCC), linear (minimos quadrados em t), relativo (minimos quadrados do erro relativo, peso 1/SY^2) e mediana das razoes.
Entradas: Dados Iniciais/comparacao_SY_lambda005_woodward.csv (soma de E_unit e SY medido) e a lamina R de cada evento (Tabela 2 do TCC)."""
import pandas as pd, numpy as np
d = pd.read_csv(r'C:\TCC\Dados Iniciais\comparacao_SY_lambda005_woodward.csv')
y = d.SY_obs_t.values; n = len(y)
R = np.array([23.4, 57.3, 65.4, 36.2, 60.9, 34.5, 35.5, 82.5, 92.9, 25.8, 74.0, 23.7, 74.9, 82.2, 139.4, 97.7, 65.6])
V = d.V_dir_medido_m3.values
ss = (y - y.mean()) ** 2
print('evento 15: %.1f%% da soma dos quadrados da carga medida em torno da media' % (100 * ss[14] / ss.sum()))
def c_of(k, E, yy):
    r = yy / E
    return {'log': np.exp(np.mean(np.log(r))), 'linear': np.sum(E * yy) / np.sum(E * E), 'relativo': np.sum(E / yy) / np.sum((E / yy) ** 2), 'mediana': np.median(r)}[k]
modelos = {'MC': d.soma_E_unit_calc_t.values, 'MFM': d.soma_E_unit_forc_t.values, 'regra chuva (R)': R, 'regra volume (Vdir)': V}
for nome, E in modelos.items():
    for k in ('log', 'linear', 'relativo', 'mediana'):
        ape = []; f2 = []
        for i in range(n):
            m = np.arange(n) != i
            p = c_of(k, E[m], y[m]) * E[i]
            ape.append(100 * abs(p - y[i]) / y[i]); f2.append(0.5 <= p / y[i] <= 2)
        print('%-22s %-9s MedAPE_LOO %5.1f%%  fator2 %3.0f%%' % (nome, k, np.median(ape), 100 * np.mean(f2)))
