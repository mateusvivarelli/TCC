# README — Status do TCC (espacialização da MUSLE)

Ponto de partida pra retomar o trabalho. Detalhes completos em
[Notas Claude/notas_qgis_calibracao_qp.md](Notas%20Claude/notas_qgis_calibracao_qp.md) (Fase 1 —
calibração de Q e Qp) e [Notas Claude/notas_musle_espacializada.md](Notas%20Claude/notas_musle_espacializada.md)
(Fase 2 — MUSLE espacializada, em andamento).

## Onde estamos agora (14/09/2026) — PAUSADO a pedido do usuário

FCI (17/17 eventos) rodou com sucesso e passou por checagem visual (padrão espacial coerente com a
declividade). A calibração de FCI₀/k_FCI (`Scripts/calcular_dsc_calibrar_validar.py`) rodou várias
vezes e **achou um problema real, ainda não resolvido**: calibrando via log-NSE (Eq. 11, o mesmo
objetivo do artigo), o otimizador converge pra k_FCI≈0 (a conectividade espacial vira irrelevante,
DSC quase constante) e o NSE bruto resultante fica negativo (-0,72). Mas um teste de baseline
(escala constante de ΣE_unit, sem FCI/DSC nenhum) já dá **NSE=0,37 (através da origem) ou 0,65 (com
intercepto)** — melhor que a calibração via FCI! Ou seja: **a forma como está calibrando agora
(log-NSE) está pior que simplesmente ignorar a conectividade**. Última mudança feita (ainda não
testada): troquei o objetivo de otimização de log-NSE pra NSE bruto direto, pra ver se a
conectividade consegue superar o baseline de 0,37/0,65 dessa forma. **Não rodar ainda — usuário
pediu pra deixar pra depois.**

Rerun (quando for retomar):
```bash
"C:\Program Files\QGIS 3.44.14\bin\python-qgis-ltr.bat" "C:\TCC\Scripts\calcular_dsc_calibrar_validar.py"
```
Leva uns 8-10 minutos. Ver [notas_musle_espacializada.md](Notas%20Claude/notas_musle_espacializada.md)
seção 7/9 pro histórico completo das tentativas e valores encontrados.

**Corte de escopo (14/09/2026):** a simulação de cenários de conservação (alterar C/P) foi
removida do projeto do TCC — decisão do usuário dado o prazo. Não é mais um item pendente.

## Fase 1 (concluída): calibração de Q e Qp

Resumo em [Resultados_Calibracao_TCC.xlsx](Resultados_Calibracao_TCC.xlsx) e nas notas
[notas_qgis_calibracao_qp.md](Notas%20Claude/notas_qgis_calibracao_qp.md). Adotado:

- **Volume (Q):** CN-1 (seco) + λ=0,05 (recalibrado do padrão 0,2). Erro médio +0,5%, absoluto
  47,4%. Script: `Scripts/spatialRain.py`.
- **Vazão de pico (Qp):** HU-SCS por convolução horária, Tc de Giandotti (10,65h) + fator de pico
  recalibrado (2,08→1,1184). Erro médio -38,4%, absoluto 46,0%. Script:
  `Scripts/spatialPeakFlowHU_convolucao.py`.
- **Área da bacia (MDE):** corrigida de 109,79 km² pra 137,80 km² (barreiras de drenagem
  corrigidas — aterros de estrada que o MDE não capturava). Raster final:
  `Dados Iniciais/qp_spatial/flowacc_corrigido.tif`.
- **Exutório real da bacia** (não confundir com o posto de chuva DBT5, que fica fora da bacia):
  X=318980,77, Y=7432307,08 (SIRGAS 2000/UTM 23S).

## Fase 2 (em andamento): espacializar a MUSLE

Objetivo do TCC: gerar um **mapa** de produção de sedimentos (não um valor único por evento como
na IC), seguindo Hao et al. (2022) — `1-s2.0-S0022169422011490-main.pdf`, já na pasta.

### O que já está pronto

| Item | Arquivo(s) | Status |
|---|---|---|
| pr_pixel (vazão de pico local, por pixel) | `Evento {n}/pr{n}.tif` | ✅ pronto, 17 eventos |
| K (erodibilidade do solo) | `Dados Iniciais/K_raster.tif` | ✅ pronto (média 0,039) |
| LS (topográfico) | `Dados Iniciais/LS_raster.tif` | ✅ pronto (média 0,536, bate com a IC) |
| C (uso do solo) | `Dados Iniciais/C_raster.tif` | ✅ pronto (média 0,05 — **confirmado com você**, diferente dos 0,267 da Tabela 3 da IC, que provavelmente usou outra fonte) |
| P (práticas conservacionistas) | constante = 1,0 | ✅ (sem áreas de preservação ativa) |
| E_unit (erosão local por pixel) | `Evento {n}/E_unit{n}.tif` | ✅ pronto, 17 eventos — checado: E_unit sempre > sedimento medido em todos os eventos (faz sentido fisicamente) |
| SY_obs (sedimento medido por evento) | coluna `SYY_t` da planilha `eventos_processados_manuais.xlsx` | ✅ localizado, não precisou digitalizar nada |
| IC genérico (placeholder, W=1) | `Dados Iniciais/qp_spatial/IC_placeholder.tif` | ✅ só teste inicial, não usar pra calibração |
| IC por evento (Eq. 5 genérica, **desatualizado**) | `Evento {n}/IC{n}.tif` | ⚠️ calculado com fórmula errada (ver abaixo) — não usar |
| **FCI por evento (Eq. 7 exata, a correta)** | `Evento {n}/FCI{n}.tif` | 🔄 **rodando/precisa rodar** (ver comando acima) |

### Correção importante feita nesta sessão

A primeira versão do índice de conectividade (`calcular_ic_por_evento.py`) usava a fórmula
genérica do IC (Borselli 2008), com W̄ = média do E_unit já calculado. Você mandou as imagens das
Eq. 5 e Eq. 7 do artigo (o texto extraído do PDF estava corrompido nessa parte) e ficou claro que
a Eq. 7 (a que Hao et al. realmente usam) é diferente: o numerador usa médias **separadas** de Q,
pr, K, C, P, S (não a média do E_unit combinado), e **sem o fator LS**. Corrigido em
`Scripts/calcular_fci_por_evento.py` — **é esse que precisa terminar de rodar**, não o
`calcular_ic_por_evento.py` antigo.

## Próximos passos (depois que o FCI terminar)

1. **Normalizar FCI em DSC** (probabilidade de conectividade, 0 a 1) via a curva sigmoide:
   $DSC_{unit,k} = \dfrac{1}{1+\exp(FCI_0 - k_{FCI}\cdot FCI_k)}$ — conferir a forma exata da
   fórmula (Eq. 8 do artigo) antes de implementar, mesmo cuidado que tivemos com a Eq. 7.
2. **Calcular SY_sim por evento**: $SY_{sim} = \sum_{pixels} E_{unit} \times DSC$.
3. **Calibrar FCI₀ e k_FCI** (2 parâmetros, únicos pra toda a bacia — não por evento, conforme
   Tabela 4 do artigo) contra os 17 valores de `SYY_t` (já localizados, ver tabela na seção 6.1
   das notas). Usar `scipy.optimize` (já usamos várias vezes nesta sessão pra esse tipo de
   calibração).
4. **Validar**: comparar SY_sim×SY_obs (NSE, WIA, erro % — mesmas métricas do artigo, Tabela 4).
5. **Mapas finais**: produção de sedimentos por pixel/evento — os "hot spots" erosivos, resultado
   central do TCC.
6. **Simulação de cenários**: alterar C e/ou P localmente pra simular intervenções de conservação
   (mantas biotêxteis, gabiões, bacias de sedimentos) e quantificar a redução de sedimentos.

## Prazo

~6 semanas a partir de 12/09/2026 pra entregar o TCC (ver cronograma detalhado nas notas se
precisar reconferir o ritmo).

## Arquivos-chave pra retomar

- Este README (visão geral e checklist)
- `Notas Claude/notas_qgis_calibracao_qp.md` — histórico completo da Fase 1 (Q, Qp, correção do
  MDE), incluindo todas as tentativas descartadas e por quê.
- `Notas Claude/notas_musle_espacializada.md` — histórico completo da Fase 2, incluindo as
  fórmulas exatas do artigo e o histórico de discussão de por que não fizemos diferente
  (Método Racional pixel a pixel, qp constante, sub-bacias — todos descartados antes de achar a
  solução do Hao et al.).
- `1-s2.0-S0022169422011490-main.pdf` — artigo de referência completo.
- `Resultados_Calibracao_TCC.xlsx` — planilha com os resultados da Fase 1 (envie pro orientador
  se ainda não enviou).
