---
name: orientador-vazao-de-base-sedimento
description: Vazão de base JÁ foi removida do modelo em 26/10/2026 (origin/main); minha árvore local estava atrasada
metadata:
  node_type: memory
  type: project
  originSessionId: 426ab00d-357d-475d-bdcb-5bb27ed7a0ba
  modified: 2026-10-28T01:00:40.667Z
---

O orientador (Me. Luis Fernando Murillo-Bermúdez) questionou o termo de base (91% do sedimento no MC). Em 26/10/2026 outra sessão já **removeu a vazão de base do modelo** (commit ff51641 em origin/main): MUSLE só com escoamento direto, SY = c·ΣE_unit, alvo = carga total medida, λ = 0,20 (`Scripts/calcular_sy_so_direto.py`, sufixos `_sd`). Resultado (LOO): MC 98% / 24% em fator 2; MFM 39% / 94%. Em 27/10 há o **candidato** λ = 0,05 com S convertido por Woodward (`_l05w`; MFM 20,6% / 94%; MC 81% / 35%). **O usuário decidiu usar o Woodward (27/10) e confirmou em 28/10 que o candidato é a forma OFICIAL agora (aprovação do orientador não confirmada).** Resumo/abstract do Doc devem usar os números do candidato. Checagens 1, 2 e 4 (BFImax, alvo só-direto, fórmula de Woodward no original) rodando em subagente. Eckhardt confirmado (α 0,995; BFImax 0,70). Ler `README.md` (seções de 26 e 27/10), `Notas Claude/resumo_modelo_completo.md` e `Notas Claude/mudancas_docs_sem_base_26-10.md`.

**Why:** em 27/10 eu respondi como se a decisão estivesse pendente, porque a minha árvore local estava em 1fa905e, 9 commits atrás de origin/main. O usuário lembrava corretamente.

**How to apply:** SEMPRE rodar `git fetch` e comparar com origin/main antes de analisar ou editar. O Doc "TCC arquivo (revisado)" criado em 18/10 (modelo de dois termos) está desatualizado em relação a essa decisão.
