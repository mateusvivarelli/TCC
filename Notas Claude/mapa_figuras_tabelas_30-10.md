# Mapa de figuras e tabelas com a numeração nova (30/10/2026)

Sessão na nuvem. Substitui `mapa_figuras_tabelas_secoes_4_a_6.md` (29/10), que usava a numeração antiga e a "IC refeita". **Nada foi mudado no Doc.**

Regras: identificação acima de tabelas e figuras, "Fonte:" abaixo (como já está no Doc nas Tabelas 1 a 6 e Figuras 1 a 3). Colunas estreitas (C22): no máximo 8 colunas, cabeçalhos curtos, termos iguais aos de Materiais e métodos (MC, MFM, validação cruzada, escoamento direto, Vdir, SYobs, E_unit). IC só com valores originais.

Onde está o texto pronto de cada tabela: as tabelas novas estão escritas por inteiro, em markdown, dentro das propostas (indicado na coluna "Texto pronto"). Para colar no Docs: copiar a tabela do arquivo, colar no Doc e converter (ou digitar), depois pôr a legenda acima e a fonte abaixo.

## Tabelas

| Nº novo | Nº no Doc atual | Seção | Título (acima) | Texto pronto | Muda no Doc? |
|---|---|---|---|---|---|
| 1 | 1 | 3.2 | Tabela 1. Dados observados em campo. | Doc atual; só trocar "(seção 2.4)" por "(ver texto)" (`ajustes_cap1_a_3_30-10.md`, 5.2) | uma célula |
| 2 | 2 | 3.2 | Tabela 2. (título atual) | Doc atual | não |
| 3 | 3 | 3.2 | Tabela 3. Volume total, vazão de base, escoamento direto e sedimento medidos por evento. | `ajustes_cap1_a_3_30-10.md`, item 5.4 (6 colunas) | sim (saem as 2 colunas do SCS-CN) |
| 4 | 4 | 3.3 | Tabela 4. Dados geoespaciais. | Doc atual, só o título (S13) | título |
| 5 | 5 | 3.3 | Tabela 5. (atual) | Doc atual | não |
| 6 | 6 | 3.3 | Tabela 6. (atual) | Doc atual | não |
| 7 | 7 | 3.4.1.1 | Tabela 7. Variáveis usadas no modelo. | `proposta_cap3_30-10.md`, 3.4.1.1 (3 colunas) | sim (saem Tchuva, Vbase, Qbinicio; entram variáveis por pixel) |
| 8 | 8 | 3.4.4 | Tabela 8. Versões do modelo. | `proposta_cap3_30-10.md`, 3.4.4 (3 colunas) | sim (sai a coluna da vazão de base) |
| 9 | 9 | 3.4.5 | Tabela 9. Parâmetros fixos e calibrados. | `proposta_cap3_30-10.md`, 3.4.5 (3 colunas) | sim (c1/c2 viram c; saem "IC refeita" e os pesos dos postos) |
| 10 | (nova) | 3.4.8 | Tabela 10. Modelos de comparação. | `proposta_cap3_30-10.md`, 3.4.8 (4 colunas) | nova |
| 11 | (nova; colunas da antiga 3) | 4.1 | Tabela 11. Escoamento direto por evento: medido e calculado pelo SCS-CN. | `proposta_cap4_30-10.md`, 4.1 (5 colunas) | nova |
| 12 | 11 | 4.2 | Tabela 12. Sedimento por evento (t): medido e simulado pelo MC e pelo MFM. | `proposta_cap4_30-10.md`, 4.2 (8 colunas) | sim (C22: saem "Encostas" e "Base"; entra o MFM) |
| 13 | 12 | 4.3 | Tabela 13. Desempenho dos modelos (calibração em escala logarítmica; carga total de sedimentos). | `proposta_cap4_30-10.md`, 4.3 (7 colunas) | sim (todos os números; IC original com a coluna "Avaliação") |
| 14 | 13 | 4.5 | Tabela 14. Contribuição de cada classe de uso para a erosão média (MC e MFM). | `proposta_cap4_30-10.md`, 4.5 (5 colunas) | sim (números; sem kg/pixel) |
| 15 | 14 | 4.5 | Tabela 15. Contribuição de cada classe de solo para a erosão média (MC e MFM). | `proposta_cap4_30-10.md`, 4.5 (5 colunas) | sim |
| 16 | (nova) | 4.5 | Tabela 16. Contribuição de cada classe de declividade para a erosão média (MC e MFM). | `proposta_cap4_30-10.md`, 4.5 (4 colunas, valores [PC]) | nova; **números a calcular no PC** |
| A1 | 10 | Apêndice A | Tabela A1. Resultados do evento 11 e do pixel de exemplo. | `proposta_cap3_30-10.md`, Apêndice A (2 colunas, só resultados) | sim (C20: cálculo passa para o texto) |

Fontes abaixo das tabelas: "Fonte: elaborado pelo autor." em todas, com os acréscimos já escritos nas propostas (Tabela 9: "com base em Williams (1975), ANA (2024), Chow, Maidment e Mays (1988) e Woodward et al. (2003)"; Tabela 10: "com a formulação e os coeficientes de Vivarelli et al. (2025)"; Tabela 13: "linha da IC calculada com os valores simulados e medidos de Vivarelli et al. (2025)").

Tabela que sai: a antiga Tabela 10 (evento 11 com as contas dentro da tabela) vira texto no Apêndice A e a Tabela A1. Se o Doc numerar o apêndice em sequência, A1 vira Tabela 17.

Sobre a C22 (tabela com partes sobrepostas): o comentário não mostra o trecho. Pela hora (entre os comentários da 4.9 e da 5.2), deve ser a Tabela 11 antiga (7 colunas, com "Encostas" e "Base") ou a Tabela 10 antiga (evento 11, com contas longas nas células). As duas foram refeitas com colunas estreitas: Tabela 12 (8 colunas curtas, só números) e Tabela A1 (2 colunas, só resultados). A Tabela 3 também perdeu 2 colunas (de 8 para 6). Se ainda houver sobreposição no Doc, a Tabela 12 pode ser dividida em duas (MC e MFM, 5 colunas cada).

## Figuras

| Nº novo | Nº no Doc atual | Seção | Legenda (acima) | Arquivo | Situação da imagem |
|---|---|---|---|---|---|
| 1 a 3 | 1 a 3 | 3.1, 3.3 | atuais | `mapa_01`, `mapa_02`, `mapa_03` | sem mudança |
| 4 | 4 | 3.4 | Figura 4. Fluxograma do método. | `TCC_Texto/figuras/mapas/fig_fluxograma.png` | trocar pela regerada (28/10). Conferida nesta sessão: sem "água", sem método descartado; usa setas "→" dentro da imagem (aceitável em figura) |
| 5 | (nova) | 4.1 | Figura 5. Escoamento direto por evento: calculado pelo SCS-CN (CN-I, λ = 0,05, S convertido) contra o medido. A faixa indica o fator 2. | `TCC_Texto/figuras/fig_volume_direto.png` | pronta (C24; ver pergunta ao Luis) |
| 6 | 8 | 4.1 | Figura 6. Chuva total de cada evento, interpolada pelo inverso do quadrado da distância a partir de dois postos. | `TCC_Texto/figuras/mapas/mapa_04_chuva_eventos.png` | igual; só renumerar e mover para 4.1 (C26) |
| 7 | 9 | 4.1 | Figura 7. Escoamento direto calculado pelo SCS-CN (CN-I, λ = 0,05, S convertido) em cada evento. | `TCC_Texto/figuras/mapas/mapa_05_escoamento_eventos.png` | trocar pela regerada; mover para 4.1 (C26). Conferida: sem "água" |
| 8 | 6 | 4.2 | Figura 8. Sedimento simulado contra o medido nos 17 eventos: modelo simples com a chuva, MC e MFM (validação cruzada) e modelo concentrado da IC (valores originais, ajuste nos 17 eventos da IC). A faixa indica o fator 2; os números identificam os eventos. | `TCC_Texto/figuras/fig_dispersao.png` | pronta, com IC original. Conferida: sem "água" |
| 9 | (nova) | 4.3 | Figura 9. Erro percentual mediano e eventos dentro de fator 2 com o escoamento calculado a partir da chuva e com o escoamento forçado ao medido: MUSLE espacializada, modelo simples com a chuva e modelo concentrado da IC (valores originais). | **`TCC_Texto/figuras/escada_gargalo_30-10.png`** (refeita nesta sessão, ver abaixo) | a `escada_gargalo.png` de 29/10 diz "Água calculada / Água forçada" (C30) e tem rodapé de método; usar a de 30/10 |
| 10 | 10 | 4.4 | Figura 10. Erosão produzida em cada pixel em cada evento (MC). | `TCC_Texto/figuras/mapas/mapa_06_sedimento_eventos.png` | trocar pela regerada; **não aberta nesta sessão**; segundo o relatório de 28/10, o rótulo interno diz "Sedimento das encostas" (regerar no PC ou aceitar) |
| 11 | 11 | 4.5 | Figura 11. Erosão média dos 17 eventos e áreas críticas (5% dos pixels de maior erosão média), para o MC e o MFM. | `TCC_Texto/figuras/mapas/mapa_07_sedimento_medio.png` | **regerar no PC**: título do painel do MC diz "água calculada pelo SCS-CN" (C30) e o rodapé diz "sem termo de vazão de base" (método descartado); títulos internos dizem "Sedimento médio" (preferir "Erosão média", S29) |
| A1, A2 | 5 | Apêndice A | Figura A1. Evento 11: chuva interpolada, retenção S0,05 e escoamento direto. Figura A2. Evento 11: índice de erosão E_unit e sedimento produzido em cada pixel (MC). | `TCC_Texto/figuras/mapas/mapa_08_evento11.png` (5 painéis juntos) | C20: imagens maiores. Ideal: dividir em duas figuras de página inteira (regerar no PC); alternativa: a imagem atual em página inteira, paisagem. Rótulo interno "Sedimento das encostas" |

Abaixo de cada figura: "Fonte: elaborado pelo autor." (Figura 8: "Fonte: elaborado pelo autor; painel da IC com os valores de Vivarelli et al. (2025).")

Títulos dentro das imagens: as Figuras 5, 7, 8 e 11 têm título interno que repete a legenda; com a legenda ABNT acima, o título interno sobra. Não é erro; resolver ao regerar no PC, se o usuário quiser.

### Figura 9 refeita nesta sessão

- Script novo: `Scripts/_escada_gargalo_figura_csv_30-10.py` (lê só `TCC_Texto/figuras/escada_gargalo.csv`; não precisa de rasters). Não alterei o script original nem a `escada_gargalo.png` de 29/10 (regra: não mexer em arquivos de outras sessões).
- Mudanças: rótulos "Escoamento calculado a partir da chuva" e "Escoamento direto forçado ao medido" (C30); legenda "MUSLE espacializada (MC e MFM)" e "Modelo simples: c * chuva do evento"; sem o rodapé (o método está na legenda e na 3.4.8). Valores idênticos aos do CSV (MC 81%, chuva 42%, MFM 21%, IC original 22%; fator 2: 35%, 82%, 94%, 100%).
- Situação: gerada em 30/10 na nuvem (matplotlib instalado via pip) e conferida visualmente: valores e rótulos corretos.

## Remissões que mudam no texto (para o roteiro K)

| Onde | Antigo | Novo |
|---|---|---|
| texto da 4.1 antiga (5.1) | "Tabela 3" (volumes com SCS-CN) | "Tabela 11" |
| 5.2 antiga | "Tabela 11", "Figura 6" | "Tabela 12", "Figura 8" |
| 5.5 antiga | "Tabela 12" | "Tabela 13" |
| 5.6.1 antiga | "Figuras 8 a 10" | "Figuras 6 e 7" (4.1) e "Figura 10" (4.4) |
| 5.6.2 antiga | "Figura 11", "Tabela 13", "Tabela 14" | "Figura 11", "Tabela 14", "Tabela 15" |
| 4.9 antiga | "Tabela 10", "Figura 5" | "Tabela A1", "Figuras A1 e A2" |
| 2.4 e 2.5 antigas | "seção 4.x" | resolvidas: os textos com remissão foram para o capítulo 3 |

## Planilha `Planilhas/planilha_calculos_concentrados.xlsx` (refeita em 30/10)

- Script: `Scripts/gerar_planilha_calculos_concentrados.py`. A aba `IC_refeita` foi trocada pela aba `IC`, com os **valores originais** da IC (`Scripts/_ic_original.py`: datas, volume, pico, sedimento medido e simulado da planilha da IC, α 0,277 e β 0,807), sem recalibração e sem validação cruzada. A linha da IC no `Resumo` aponta para essa aba. Também troquei "água" por "escoamento" nos títulos e notas das abas (C30). Estilo: mantido o mínimo que o script já tinha; nada acrescentado.
- Recalculada no LibreOffice (`soffice --headless --convert-to xlsx`) e conferida: nenhuma célula com erro; IC: erro mediano absoluto 22,46%; fator 2 100%; NSE log 0,910; NSE linear 0,831; Spearman 0,926; erro médio com sinal +4,15%; faixa -37,1% a +60,0% (iguais aos valores originais). Demais modelos iguais aos oficiais (MC 81,1% / 35% / -0,69 / 0,59; MFM 20,6% / 94% / 0,84 / 0,83; chuva 41,9%; Vdir 15,9%; TR 17,6%; volume: viés +2,87%, erro mediano 46,3%, NSE -0,39). O arquivo salvo no repositório é a versão recalculada pelo LibreOffice (com os valores guardados nas células).
