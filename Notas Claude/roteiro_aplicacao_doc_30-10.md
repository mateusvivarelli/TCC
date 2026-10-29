# Roteiro para aplicar a reestruturação no Doc (30/10/2026)

Para o Mateus. Ordem sugerida para levar as propostas de 30/10 ao Google Doc, do que é independente para o que depende de outra coisa. Tudo foi escrito pela sessão na nuvem, sem acesso ao Doc; leia cada proposta antes de colar.

## Arquivos (todos em `Notas Claude/`, branch `claude/noite-30-10`)

- `plano_reestruturacao_30-10.md`: sumário novo e a tabela C9 a C31 / S9 a S31 (comece por aqui).
- `ajustes_cap1_a_3_30-10.md`: pares "atual -> novo" para Resumo, Abstract e capítulos 1 a 3.
- `proposta_cap2_30-10.md`, `proposta_cap3_30-10.md` (com o Apêndice A), `proposta_cap4_30-10.md`, `proposta_cap5_30-10.md`.
- `mapa_figuras_tabelas_30-10.md`: numeração nova, arquivos de cada figura e situação de cada imagem.
- `perguntas_para_o_luis_30-10.md`: 17 perguntas.
- `leitura_referencias/loteE_medicao_e_validacao.md`: referências novas identificadas, **nenhuma lida** (rede bloqueada).
- Planilha `Planilhas/planilha_calculos_concentrados.xlsx` (aba `IC` com os valores originais) e figura `TCC_Texto/figuras/escada_gargalo_30-10.png`.

## Ordem sugerida

**Etapa 0 - antes de mexer no Doc (decisões).** Ler o plano (seção 3, decisões) e decidir: 4.6 separada ou não; "Apêndice A" ou "Anexo 1"; Tabela 3 dividida ou não; objetivo 5 reescrito (F). Mandar ao Luis as perguntas 1 a 7 (dados) e 8 a 14 (estrutura), que mudam frases dos capítulos 3 e 4.

**Etapa 1 - aceitar as sugestões do Luis no Doc** (itens 0.1 a 0.5 de `ajustes_cap1_a_3_30-10.md`): S9 a S18 (títulos e "foi"). São independentes e não mudam conteúdo.

**Etapa 2 - Resumo, Abstract e capítulo 1** (itens 1 a 3 dos ajustes): troca de "água" (C30) e o objetivo 4. Independente do resto. Se aceitar a mudança do objetivo 5, aplicar junto (texto em `proposta_cap5_30-10.md`).

**Etapa 3 - capítulo 3 antes do 2.** Primeiro inserir no capítulo 3 o que vem do 2 (3.2: série de base; 3.3: CN-I e LS), depois apagar do 2. Assim nada se perde no meio do caminho. Ordem:
1. 3.2 e 3.3: itens 5.2 a 5.8 dos ajustes (inclui a Tabela 3 nova).
2. Substituir o bloco "4. METODOLOGIA" (4.1 a 4.9 e os marcadores "3.4.xxx") pelo texto de `proposta_cap3_30-10.md` (3.4 a 3.4.9). Criar as equações no editor do Docs (marcas `[EQUAÇÃO]`, cerca de 20). Tabelas 7 a 10.
3. Levar o exemplo do evento 11 para o fim do documento (Apêndice A), com a Tabela A1 e as figuras em página inteira.

**Etapa 4 - capítulo 2** (`proposta_cap2_30-10.md` e itens 4.x dos ajustes): cortar o que já foi para o 3; criar a 2.5 (medição de sedimentos); renumerar 2.5 a 2.7 para 2.6 a 2.8; trocar "otimista" (C14). Os marcadores `[REFERÊNCIA A LER]` ficam até as referências serem lidas (Etapa 7); se for entregar antes disso, apagar o marcador e manter a frase sem citação, ou cortar a frase, conforme as notas de cada seção.

**Etapa 5 - capítulo 4** (`proposta_cap4_30-10.md`): substituir o capítulo 5 antigo inteiro (inclusive "O gargalo", 5.4 e 5.5, que viram a 4.3 sem subitens). Trocar as figuras na ordem do mapa (Figuras 5 a 11; a Figura 9 é a `escada_gargalo_30-10.png`). Depende das etapas 3 (remissões a 3.4.x) e 6 (números do PC na 4.5).

**Etapa 6 - capítulo 5** (`proposta_cap5_30-10.md`): substituir o capítulo 6 antigo. Depende do capítulo 4 (números) e da decisão sobre o objetivo 5.

**Etapa 7 - referências.** Acrescentar à lista: Eckhardt (2012) (conferir título e DOI no PDF; está no lote A como texto completo). Retirar da lista o que deixou de ser citado (nada, pelas propostas). Decidir sobre as obras citadas e não lidas no original: USDA-SCS (1972), Chow, Maidment e Mays (1988), Williams (1975), Nash e Sutcliffe (1970), Lyne e Hollick (1979) e as só lidas no resumo (Moore e Burch, 1986; Eckhardt, 2005; Murillo-Bermúdez et al., 2023). Opções: manter como está (já estavam no Doc), usar "apud" com a obra lida, ou ler o original. Quando for possível baixar PDFs, ler primeiro Varma e Simon (2006) e Rasmussen et al. (2009) (C19 e C10) e trocar os marcadores.

**Etapa 8 - numeração e remissões** (C18, C27): conferir com a tabela "Remissões que mudam" do mapa; atualizar o sumário; conferir "Fonte:" abaixo de todas as tabelas e figuras novas.

**Etapa 9 - responder os comentários do Luis no Doc**, um a um, dizendo o que foi feito (a coluna "Ação planejada" do plano serve de resposta curta).

## O que ainda precisa ser calculado ou refeito no PC (sem rasters na nuvem)

Script pronto, **não testado** (a nuvem não tem os rasters): `Scripts/_analise_mapa_declividade_r2_30-10.py`. Ele lê os mesmos arquivos de `calcular_sy_lambda005_woodward.py`, `gerar_tabelas_tcc.py` e `_recalcular_ls_moore.py` e imprime:

1. **R² do mapa (C31)**: R² de ln(erosão média) com ln(K*LS*C) e com o termo de escoamento, partição em % (fatores fixos x escoamento), e R² linear (para MC e MFM). Preenche a 4.5 e a 5.
2. **Declividade (Tabela 16)**: área e erosão por classe (0-3, 3-8, 8-20, 20-45, 45-75, >75%) e o cruzamento uso x solo x declividade nos pixels críticos. Preenche a 4.5 e a 5.
3. **Limite Q <= P no MFM**: volume distribuído contra o medido por evento (diferença em %). Preenche a 3.4.4.
4. **Pixels com CN-I < 35**: fração da erosão média neles. Opcional, para a 4.6.

Figuras a regerar no PC (`Scripts/gerar_mapas_tcc.py`; o script é de outra sessão, então mudar só os rótulos):
- `mapa_07_sedimento_medio.png` (Figura 11): título do MC diz "água calculada pelo SCS-CN" (C30) e o rodapé diz "sem termo de vazão de base" (método descartado); trocar "Sedimento médio" por "Erosão média".
- `mapa_06_sedimento_eventos.png` (Figura 10) e `mapa_08_evento11.png` (Figuras A1 e A2): rótulo "Sedimento das encostas" -> "Erosão no pixel"; dividir o `mapa_08` em duas figuras de página inteira (C20).
- Conferir no `mapa_06` a frase da 4.4 sobre os eventos 9, 14, 15 e 16 (não abri essa imagem).

Outras conferências no PC:
- Título e DOI de Eckhardt (2012).
- A frase da 4.5 "área urbanizada concentrada perto do exutório" contra a Figura 2 (não conferida).
- Faixa de CN 35 a 100 da tabela de Woodward et al. (2003) (repetida das notas, não reaberta nesta sessão).

## Pendências que dependem do Luis (ver perguntas)

Origem de `Chuva_evento_mm` (3.4.1.4); BFImax 0,70 x 0,58 x valor-guia 0,25 (3.2, 4.6); evento 24/11 x 17/12/2018 (3.2, 4.3); curva turbidez-CSS (2.5, 4.3, 4.6); critério de delimitação dos eventos (3.2, 4.6); qual gráfico e qual tabela ele quis dizer em C24 e C22; Anexo x Apêndice; 4.6 separada.
