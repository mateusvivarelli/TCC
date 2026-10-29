# Pendências da edição do Google Doc — ponto de retomada de 27/10/2026

> **Desatualizado:** o estado atual e as instruções estão em `Notas Claude/instrucoes_sessao_desktop.md` (28/10/2026).

Nota de passagem entre sessões (o Doc é editado fora do repositório). Estado do modelo: ver `Notas Claude/resumo_modelo_completo.md`.

Sessão de 27/10/2026 parou no meio da revisão do Doc original (id 12xwNDLmeeRB6IcbsprDWuI3XHx_At2RIgsPm6WBKiGo), seção por seção. Decisão do usuário: **usar Woodward** (λ 0,05, S₀,₀₅ = 1,33·S₀,₂₀^1,15, CN-I, MUSLE só com escoamento direto, sem termo de base). Ver [[orientador-vazao-de-base-sedimento]] e [[feedback-ler-referencias-novas]].

**Já aplicado no Doc (edição direta):** 1.1, 1.2, 1.3 (objetivo de mapear K/LS/C/P removido, novo objetivo de mapa de áreas críticas), 2.1 e 2.2 (lista de aplicações da MUSLE movida da 1.1 para a 2.2; correção Baert 154/46 eventos); 7 referências novas na lista (Avanzi, Azmeri, Hoppen, Neitsch, Reda, Sadeghi — sem Renard).

**NÃO aplicado ainda (só enviado no chat):** Resumo e Abstract com os números do candidato (MC 35% fator 2 / 81% erro mediano; MFM 94% / 21%; SCS-CN erra o escoamento direto em 46%; IC 16%; frase do gargalo mantida; frase final "desempenho equivalente à formulação concentrada"). O Doc ainda tem o Resumo antigo de dois termos.

**Subagentes de leitura de referências (lotes A, B, C), disparados em 27/10:** os três não terminaram (A e C foram interrompidos pelo fim da sessão; B parou por limite de uso). Ainda não há resumos gravados; precisam ser retomados ou refeitos. Conteúdo de cada lote: A = Hao, Baert, Brandão, Woodward, Valle Junior, Eckhardt; B = Williams, Wischmeier, Renard, Moore e Burch, Nash e Sutcliffe, Lyne e Hollick, Chow, USDA-SCS; C = Sartori, ANA, Consórcio PCJ, Murillo-Bermúdez 2022 e 2023, IC.

**Pendências de referências:** incluir RENARD et al. (1997) na lista (citado na 1.1 e 2.1; ler antes); conferir iniciais dos autores de AZMERI et al.; conferir λ = 0,023 de Reda no artigo original (só resumo lido); Hoppen/Sadeghi/Azmeri/Reda só no resumo (pedir PDFs ao usuário); adicionar Woodward et al. (2003) à lista (DOI 10.1061/40685(2003)308; fórmula confirmada no manuscrito, Eq. 8; checagem 4) quando citar; Mauri et al. (2020, RBCS, SWAT na bacia do rio das Mortes) é opcional; 4º autor de Murillo-Bermúdez 2023 ("FILHO, J. G. D.") a confirmar; conferir frase da 2.2 sobre a IC "ajustou os coeficientes" (relatório PIBIC: α 0,0385 e β 0,8 forçados ao intervalo da literatura) — lote C vai conferir.

**Pendências do Doc:** equação da MUSLE na 2.2 (e 2.2/4.4/4.5/4.6) precisa ser refeita à mão como equação do Docs (API não cria equação); citar fonte na 1.1 para "grande concentração urbana e atividades agrícolas intensivas" (ver seção 3.1); Luis pediu separar a Tabela 5 em duas (K e C); resto do Doc ainda está no modelo antigo de dois termos: seguir a lista `Notas Claude/mudancas_docs_sem_base_26-10.md` (origin/main) adaptada ao candidato (3.2, 4.1, 4.2 Tabela 6, 4.4, 4.5 reescrever, 4.6 calibração com um c, 4.7, 4.9 Tabela 9 do evento 11, Figura 4 fluxograma, Tabelas 7/8, 5.x resultados, conclusões, limitações). Doc "TCC arquivo (revisado)" (id 18e7373U...) está desatualizado (dois termos); não usar como base.

**Checagens de 27/10 (subagente; relatório em `...\Temp\claude\checagens_27-10\relatorio_checagens.md`):** o candidato é robusto à separação da base (Eckhardt 0,58/0,70/0,80, α 0,98, Lyne-Hollick) e ao alvo (total ou direto); MFM candidato ≈ c·V_dir ≈ IC; MC continua ruim. Declarar como limitações: 17 eventos com parâmetros escolhidos nos mesmos eventos; 8,4% dos pixels com CN-I < 35 fora da faixa tabelada por Woodward; base com mesma concentração da mistura é hipótese alta (alvo direto é limite inferior). Dúvidas para o orientador: aprovar o candidato (aprovação do Luis não confirmada); BFImax 0,70 (reproduz) contra 0,58 (cabeçalho da planilha); coluna Bt de `Dados_finais_histereses_corrigido.xlsx` difere da série do orientador em até 0,04 m³/s (efeito 0,2% no V_dir); alvo no TCC = carga total ou direta.

**Repositório local (C:\TCC):** continua em 1fa905e, 9 commits atrás de origin/main, de propósito ("não atualize ainda, estamos validando o método"). Alterações locais não commitadas (rascunho 04, scripts, tabelas, figuras do modelo antigo). Só atualizar, com backup em branch, quando o usuário disser. Não commitar nem enviar sem pedido.

**Por quê:** o usuário teve que parar a sessão e pediu para guardar tudo.
**Como retomar:** ao retomar, ler este arquivo, fazer `git fetch`, reunir os resultados dos subagentes de referências, e perguntar por qual seção continuar (próxima natural: aplicar Resumo/Abstract, depois 2.3).
