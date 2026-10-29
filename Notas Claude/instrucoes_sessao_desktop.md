# Instruções para a sessão do desktop: retomada da escrita do Google Doc (28/10/2026)

Este arquivo é o ponto de partida. Ele junta o contexto, as regras de trabalho e as pendências que estavam só na memória da sessão do notebook (cópia da memória em `Notas Claude/memoria_claude/`).

## 1. Leia nesta ordem

1. Este arquivo.
2. `Notas Claude/resumo_modelo_completo.md`: o modelo passo a passo, com fontes e justificativas. Atenção: ele ainda trata o candidato como "candidato"; agora ele é o **oficial** (seção 2 abaixo).
3. `Notas Claude/leitura_referencias/` (LEIAME e lotes A, B, C): o que cada referência diz, o que usamos dela e os pontos de atenção.
4. `Notas Claude/relatorio_checagens_base_alvo_woodward_27-10.md`: robustez do modelo oficial e conferência da fórmula de Woodward.
5. `Notas Claude/mudancas_docs_sem_base_26-10.md`: lista de mudanças por seção do Doc, escrita para o modelo de 26/10 (λ 0,20). Usar como roteiro, trocando os números pelos do modelo oficial.

## 2. Modelo oficial (decisão do usuário em 27 e 28/10/2026)

- CN-II da ANA (BR_CN-2022, 30 m) convertido para CN-I (Chow, Maidment e Mays, 1988).
- λ = 0,05, com a retenção convertida por Woodward et al. (2003): S0,05 = 1,33 * S0,20^1,15 (S em polegadas). No cálculo, em mm: S0,05 = 25,4 * 1,33 * (S0,20/25,4)^1,15. Fórmula conferida no manuscrito original (Eq. 8).
- MUSLE por pixel (Hao et al., 2022) **só com escoamento direto**; sem termo de vazão de base. SY = c * soma(E_unit).
- Alvo da calibração: carga **total** medida (todo o sedimento atribuído ao escoamento superficial; a base só transporta).
- c calibrado em log; validação cruzada leave-one-out.
- Dois modelos: MC (água do SCS-CN, previsão) e MFM (escoamento direto forçado ao medido, V_dir = T_R - soma(Bt)*3600).
- Script: `Scripts/calcular_sy_lambda005_woodward.py` (sufixo `_l05w`).
- Aprovação do orientador (Luis) ainda não confirmada.

**Números oficiais (LOO, calibração em log, carga total):**

| Modelo | Erro mediano | Fator 2 | NSE log |
|---|---|---|---|
| MC (oficial) | 81,1% | 35% | -0,69 |
| SY = c * chuva | 41,9% | 82% | 0,53 |
| MFM (oficial) | 20,6% | 94% | 0,84 |
| SY = c * V_dir medido | 15,9% | 94% | 0,85 |
| IC concentrada **refeita** | 16,3% | 100% | 0,87 |

- SCS-CN oficial erra o escoamento direto em 46% na mediana; viés de volume +3% (contra -12% com λ 0,20); sem a conversão de S o escoamento inflaria 94%.
- MFM x IC: diferença de +6,1 pontos, IC95% [-8,6; +7,9]: não se distinguem.
- Coeficiente c: MC 0,0344; MFM 0,0222 (t por unidade de E_unit).
- "IC 16,3%" é da IC refeita pelo TCC, não da IC publicada (que só dá erro médio -4,15% e faixa -60% a +37%).

**ATENÇÃO:** tabelas, figuras e mapas em `TCC_Texto/` ainda são do modelo de 26/10 (λ 0,20). Precisam ser regenerados com o modelo oficial antes de entrar no Doc.

## 3. Google Doc

- Doc oficial: "TCC arquivo", id `12xwNDLmeeRB6IcbsprDWuI3XHx_At2RIgsPm6WBKiGo` (https://docs.google.com/document/d/12xwNDLmeeRB6IcbsprDWuI3XHx_At2RIgsPm6WBKiGo/edit).
- **Não usar** a cópia "TCC arquivo (revisado)" (id 18e7373U...): é do modelo antigo de dois termos.

**Estado em 28/10/2026:**
- Resumo e Abstract: aplicados com os números oficiais.
- 1.1, 1.2, 1.3, 2.1 a 2.7: revisados, conferidos com as fontes e alinhados ao modelo oficial.
- 2.3: duas marcas amarelas "[INSERIR EQUAÇÃO DO DOCS ...]" para o usuário criar as equações de Woodward (polegadas e mm).
- Lista de referências: completa para tudo o que é citado até a 2.7 (Renard e Woodward incluídos; quarto autor de Murillo-Bermúdez 2023 corrigido para DALFRÉ FILHO, J. G.).
- Símbolos trocados no Doc inteiro por caracteres de teclado (* e -); mantidos ², ³ e Σ; epígrafe intocada.
- Da seção 3 em diante: **ainda no modelo antigo**. Próximo passo: seção 3 (Área de estudo e dados).

## 4. Regras de trabalho pedidas pelo usuário

1. **Editar o Doc só quando ele pedir.** Mostrar a proposta no chat antes. "Aplico?" não é pedido. Não trocar a redação que o usuário escreveu.
2. **Caracteres de teclado:** `*` para multiplicação, `-` para negativo; especiais só λ, α, β (e ², ³, Σ já existentes).
3. **Toda referência nova:** ler o original antes de citar e contar ao usuário o conteúdo e o que usamos dela; dizer o nível de leitura (texto completo, resumo, não acessível). Toda referência citada entra na lista.
4. Responder em português, vocabulário simples. Ser honesto sobre o que foi ou não conferido.
5. Commit e push só quando pedir. Não versionar mudanças de .qmd/.prj (só fim de linha).
6. Sempre `git fetch` e trabalhar sobre `origin/main` antes de analisar ou editar (outras sessões fazem commits).

## 5. Como editar o Doc pela API (lições aprendidas)

- `read_doc` devolve um JSON grande que vai para arquivo; ler com Python. Helpers em `Scripts/doc_helpers/` (`dochelp.py` lista parágrafos com índices; `engine.py` monta `batchUpdate` de substituição e inserção de parágrafos; ele lê `cur.json` da pasta atual).
- Sempre reler o Doc imediatamente antes de editar e usar `writeControl.requiredRevisionId`; se o usuário estiver editando, a requisição é recusada (sem dano) e é preciso reler.
- **Nunca usar `replaceAllText` com `×`**: o Docs trocou todas as letras "x" por `*` (168 casos) em 28/10; foi desfeito. Usar `replaceAllText` só com trechos de contexto (palavras inteiras) e conferir o número de trocas.
- A API não cria equações: deixar marca amarela para o usuário.
- Conferir o Doc depois de cada edição (estrutura, estilos, contagem de caracteres).

## 6. Pendências

**Doc**
- Seção 3 em diante: atualizar para o modelo oficial. Na 3.3 e Tabela 4, a ANA entrega só CN-II; o CN-I é conversão nossa (o texto diz "em três condições").
- Remissões "seção 4.x" na 2.4 e 2.5, a preencher quando a seção 4 fechar.
- Equação da MUSLE na 2.2 e as das 4.4 a 4.6: refazer como equação do Docs (subscritos quebravam no PDF).
- Citar fonte na 1.1 para "grande concentração urbana e atividades agrícolas intensivas" (ver 3.1 / Plano PCJ).
- Separar a Tabela 5 em duas (K e C), pedido do Luis.
- Páginas iniciais (capa, folha de rosto, aprovação, sumário, listas) não revisadas; atualizar o sumário.
- 8 comentários antigos abertos no Doc.
- Discussão: incluir os contrapontos ao λ 0,05 (Baert: Woodward deu NSE de volume -0,87; Brandão associa λ 0,20 a clima úmido e pasto; Valle Junior: SCS-CN não serviu).
- Limitações: 17 eventos com escolhas feitas nos mesmos eventos; 8,4% dos pixels com CN-I < 35 fora da faixa de Woodward; hipótese de mesma concentração na base (alvo direto daria MFM 12,9%, sem mudar conclusões); critério dos 5 dias do NEH-4 abandonado no NEH-630 (2004).

**Referências**
- Expoentes do LS (0,4 e 1,3): podem ser de Moore e Wilson (1992), não de Moore e Burch (1986). Conferir.
- Reda (λ 0,023), Sadeghi, Azmeri e Hoppen lidos só pelo resumo; iniciais dos autores de Azmeri a conferir.
- 2.2: a frase "a IC ajustou os coeficientes aos dados de campo" (no relatório PIBIC, o ajuste da bacia inteira foi forçado ao intervalo da literatura; no artigo, α 0,277 e β 0,807 por regressão).

**Perguntas para o Luis**
1. Aprova o modelo oficial (λ 0,05 + Woodward)?
2. BFImax: 0,70 reproduz a série; o cabeçalho da planilha diz 0,58. A coluna Bt de `Dados_finais_histereses_corrigido.xlsx` difere da série dele em até 0,04 m³/s.
3. Evento de 24/11/2018 (lista de 2022 e IC) foi trocado pelo de 17/12/2018 na Tabela 2 do TCC. Por quê?
4. Curva turbidez-CSS: a equação 3,264 * Turb^0,7974 é do trabalho de 2022; o resumo do artigo de 2023 fala em regressão por partes com quebra em 250 NTU. Qual foi usada?

## 7. Onde está cada coisa

- Branch `backup-local-28-10`: trabalho local do notebook (rascunho 04, figuras e tabelas do modelo antigo de dois termos, revisões de 17-18/10). Só para consulta; não é a versão oficial.
- `Scripts/checagens_27-10/`: scripts das checagens de 27/10 (usam caminhos relativos ao repositório; a primeira execução cria `cache_rasters.npz`, ignorado pelo git).
- `Notas Claude/memoria_claude/`: cópia da memória da sessão do notebook.
- Python com GDAL no notebook: `C:\Program Files\QGIS 4.2.1\bin\python-qgis.bat` com `PYTHONUTF8=1` (conferir o caminho no desktop).
