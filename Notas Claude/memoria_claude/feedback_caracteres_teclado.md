---
name: feedback-caracteres-teclado
description: Nos textos do TCC, usar caracteres de teclado (* para multiplicação, - para negativo); especiais só λ, α, β
metadata:
  type: feedback
---

Nos textos do TCC (Doc e rascunhos), escrever com caracteres do teclado: `*` para multiplicação (não "·" nem "×"), `-` para sinal negativo e subtração (não "−"). Evitar caracteres especiais ao máximo; exceções permitidas: λ, α e β.

**Why:** pedido do usuário em 28/10/2026, depois que escrevi a 2.3 com "·" e "−".

**How to apply:** aplicar em todo texto novo que eu escrever para o Doc ou para os .md do TCC. Não trocar em massa o que já existe sem o usuário pedir (ver [[feedback-editar-doc-so-quando-pedir]]); mostrar antes quantos casos há.

**Armadilha técnica (28/10/2026):** no Google Docs, `replaceAllText` com `×` (U+00D7) trocou também todas as letras "x" minúsculas por `*` (168 casos). Foi desfeito comparando o texto antes e depois. Nunca usar `replaceAllText` com `×` ou outros símbolos que possam ser dobrados em letras; comparar o número de ocorrências trocadas com a contagem esperada ANTES de seguir, e conferir o Doc depois. Preferir trocas dirigidas por contexto (palavras inteiras) ou por índice.
