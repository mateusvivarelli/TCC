"""
Valores ORIGINAIS da IC (Vivarelli et al., 2025), lidos da planilha do Drive "Cópia de Tabela Resumo" (abas "CLP Eventos" e
"CLP Resultados Calibrados"), sem recalcular nada: alfa = 0,277 e beta = 0,807 ajustados nos 17 eventos da IC (sem validação cruzada).
Convenção da planilha: erro = (observado - simulado) / observado; aqui usamos o erro absoluto em % de |simulado - observado| / observado.
Este módulo só guarda os números e calcula as métricas; é importado pelos scripts de figuras e tabelas.
"""
import numpy as np

DATA = ["22/11/2018", "24/11/2018", "30/11/2018", "24/12/2018", "04/01/2019", "16/01/2019", "25/01/2019", "15/02/2019", "25/02/2019",
        "17/03/2019", "04/07/2019", "30/12/2019", "02/01/2020", "08/01/2020", "02/02/2020", "09/02/2020", "20/02/2020"]
VOL_M3 = np.array([409024.8, 1391198.4, 2629890.0, 1703552.4, 1839636.0, 325375.2, 1301475.6, 2581041.6, 1736787.6, 1235833.2, 2436681.6,
                   187488.0, 1198490.4, 1618617.6, 4238715.6, 3293269.2, 883083.6])
QP_M3S = np.array([10.3, 12.5, 30.4, 17.0, 22.1, 14.7, 16.4, 20.4, 11.8, 10.6, 21.0, 13.1, 16.0, 22.3, 28.4, 23.1, 21.4])
Y_OBS = np.array([266.4, 1237.9, 2275.6, 1335.3, 1370.4, 188.8, 1316.6, 2108.7, 1190.7, 842.0, 1821.6, 129.3, 1196.5, 1449.8, 3972.9, 1864.7, 1455.7])
# Y simulado com os coeficientes calibrados da IC (alfa 0,277; beta 0,807), coluna "Y simulado (ton)" de "CLP Resultados Calibrados"
Y_SIM_CAL = np.array([272.655783, 855.9613114, 2933.440673, 1294.895187, 1699.444241, 302.1279676, 1011.85047, 2094.029293, 977.7511952,
                      682.6683263, 2043.260788, 177.0996475, 927.742273, 1542.236255, 4079.712621, 2820.681574, 915.0106781])
ALFA, BETA = 0.277, 0.807


def metricas(obs=Y_OBS, sim=Y_SIM_CAL):
    from scipy.stats import spearmanr
    ape = 100 * np.abs(sim - obs) / obs
    r = sim / obs
    nl = 1 - np.sum((np.log(obs) - np.log(sim)) ** 2) / np.sum((np.log(obs) - np.log(obs).mean()) ** 2)
    nlin = 1 - np.sum((obs - sim) ** 2) / np.sum((obs - obs.mean()) ** 2)
    return dict(MedAPE=float(np.median(ape)), fator2=float(100 * np.mean((r >= 0.5) & (r <= 2))), NSE_log=float(nl), NSE_lin=float(nlin),
                Spearman=float(spearmanr(obs, sim)[0]), erro_medio_sinal=float(100 * np.mean((sim - obs) / obs)),
                erro_min=float(100 * np.min((sim - obs) / obs)), erro_max=float(100 * np.max((sim - obs) / obs)))


if __name__ == "__main__":
    import json
    print(json.dumps(metricas(), indent=1))
