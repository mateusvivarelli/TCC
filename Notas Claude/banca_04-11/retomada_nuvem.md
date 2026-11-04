# Retomada na nuvem (04/11/2026, 13h)

O usuário precisou desligar o notebook. Os subagentes da banca rodaram no notebook, e não na nuvem, e foram interrompidos para salvar o avanço.

## Estado
- `1_revisao_texto.md`: enviado como completo, com seção "Falta fazer".
- `2_avaliador_A.md`: A1 a A25, parcial, com "Falta fazer"; as contas ainda não entraram nas perguntas A4, A6, A14, A17 e A21.
- `3_avaliador_B.md`: B1 a B25, com "Falta fazer"; falta revisão final.
- `4_respostas_e_faq.md`: não iniciado.
- Scripts de conta dos subagentes: `Scripts/banca_04-11/` (têm caminhos do notebook; ajustar antes de rodar).

## O que falta
1. Completar nos arquivos 1 a 3 o que dá para fazer sem rasters. O que depende de rasters (.tif) fica como "não recalculado", para rodar no PC.
2. Fazer o 4_respostas_e_faq.md: responder a todas as perguntas A e B e a outras perguntas frequentes, em linguagem simples, para o aluno estudar. Para cada resposta: a resposta falada, a evidência (seção, tabela, arquivo), e a classificação "sustentada", "parcial" ou "depende do orientador". Não inventar: quando o trabalho não tem resposta, dizer isso e o que o aluno pode dizer ou fazer.
3. Fazer commit e push no branch `claude/banca-04-11` e resumir ao usuário o que corrigir primeiro.

## Regras
Ver `LEIAME_tarefa.md` e `Notas Claude/memoria_claude/`. Não editar o Google Doc sem o usuário pedir. Trabalho mais recente: este branch, que parte de `claude/noite-30-10`; o `main` está em 28/10.
