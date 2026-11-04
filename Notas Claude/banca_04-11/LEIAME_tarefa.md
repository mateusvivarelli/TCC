# Simulação de banca e revisão (04/11/2026): instruções comuns

Branch de trabalho: `claude/banca-04-11`. Autor do TCC: Mateus Guilherme Vivarelli (Unicamp, FEC, Depto. de Recursos Hídricos). Orientador: Me. Luis Fernando Murillo-Bermúdez; coorientador: Prof. Dr. André Luís Sotero Salustiano Martim. Tema: espacialização da MUSLE no alto rio Jundiaí (17 eventos, 2018 a 2020).

## O texto a analisar (versão enviada ao orientador)
- `TCC_Texto/TCC_versao_04-11.pdf`: PDF exportado do Google Doc, 68 páginas, com figuras e equações. É a referência para citar páginas, figuras e equações.
- `Notas Claude/doc_texto_pdf_paginas_04-11.txt`: texto do PDF, marcado por página.
- `Notas Claude/doc_texto_completo_04-11.md`: texto com títulos e tabelas; `[[EQ]]` marca as equações e `[[IMAGEM...]]` as figuras (para vê-las, abra o PDF).

Leia o texto inteiro antes de escrever. Diga no relatório o que foi lido e o que não foi (por exemplo, figuras que não conseguiu abrir).

## Regras
1. Responder em português do Brasil, com vocabulário simples.
2. Usar caracteres de teclado: `*` para multiplicação e `-` para negativo. Especiais só λ, α, β, ², ³ e Σ.
3. Não editar o Google Doc nem os arquivos dos colegas. Gravar só o arquivo do seu papel, em `Notas Claude/banca_04-11/`.
4. Não inventar números, referências, páginas nem conteúdo de obras. Toda afirmação sobre a literatura precisa dizer como foi conferida. Se não puder conferir, diga.
5. Citar o local exato: seção, página, tabela ou figura, e o trecho.
6. Os rasters (.tif) não estão no repositório. O que depende deles não pode ser recalculado na nuvem: diga "não recalculado". CSVs e tabelas estão no repositório (`Dados Iniciais/`, `TCC_Texto/tabelas/`; algumas pastas podem estar fora do git, por isso confira antes de afirmar que algo não existe).
7. Ao terminar: `git add` só do seu arquivo, commit no branch `claude/banca-04-11` (terminando a mensagem com `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`), `git pull --rebase origin claude/banca-04-11` e `git push origin claude/banca-04-11`. Se o push falhar, tente de novo depois do pull. Devolva também o conteúdo completo do relatório na mensagem final.

## Material de apoio (só onde o seu papel permitir)
`Notas Claude/resumo_modelo_completo.md`, `notas_musle_espacializada.md`, `leitura_referencias/` (lotes A a E), `relatorio_checagens_base_alvo_woodward_27-10.md`, `revisao_processo_29-10.md`, `revisao_independente_03-11.md`, `alteracoes_doc_03-11.md`, `perguntas_para_o_luis_30-10.md`, `resultados_analise_mapa_pc_02-11.md`, `Scripts/`, `Planilhas/`.
Ponto já conhecido a verificar: o registro de 03/11 diz que o evento de 24/11/2018 foi descrito como inexistente na série, mas a planilha `Dados Iniciais/Dados_finais_histereses_corrigido.xlsx` tem pico de 12,48 m³/s em 24/11/2018 às 23h.

## Arquivos de saída
- `1_revisao_texto.md`: revisor do texto.
- `2_avaliador_A.md` e `3_avaliador_B.md`: avaliadores da banca, trabalhando de forma independente.
- `4_respostas_e_faq.md`: respostas às perguntas da banca e FAQ.
