# Comentários para o "TCC arquivo" (Google Doc)

Cada item traz o trecho do Doc onde o comentário deve ficar (selecione o trecho e use Ctrl+Alt+M) e o texto do comentário. O texto corrigido já está no `TCC_rascunho_04.md`.

| # | Seção | Trecho do Doc | Comentário |
|---|---|---|---|
| 1 | Resumo | "Este trabalho visa reproduzir a MUSLE" | Sem ação; só conferi: 71%, 33%, 94% e 14% batem com a validação cruzada (MC 32,6%; MFM 13,6%). |
| 2 | Abstract | "(137,8 km², São Paulo, Brazil)" | Em inglês, o decimal é ponto: 137.8 km². |
| 3 | Abstract | "**Keywords:** MUSLE; produção de sedimentos" | Palavras-chave em inglês: MUSLE; sediment yield; SCS-CN; distributed modelling; GIS; Jundiaí River basin. |
| 4 | 2.1 | "Nas três bacias estudadas por esses autores" | "Esses autores" ficou sem antecedente depois que o parágrafo foi dividido. Trocar por "Hao et al. (2022)". |
| 5 | 2.4 | "Murillo-Bermúdez et al., 2022" | A referência da turbidez/CSS é Murillo-Bermúdez et al. (2023, IJRBM v. 21). A de 2022 é Murillo-Bermúdez e Martim (proceedings). Trocar para 2023. |
| 6 | 2.4 | "sem que o método de separação esteja documentado na fonte" | Consegui reproduzir a coluna Bt com o filtro de Eckhardt (a = 0,995; BFImax = 0,698), com diferença máxima de 0,004 m³/s (mediana de 0,0002 m³/s). Decidir se mantém "não documentado" ou cita o filtro. Texto pronto na 3.2 do rascunho 04, marcado como PENDENTE (confirmar a origem dos parâmetros com os autores dos dados). |
| 7 | 3.1 | "entre cerca de 725 e 1.315 m" | Não consegui confirmar a altitude no MDE (o rascunho antigo dizia 740 a 1.320 m). Conferir no MDE dentro da máscara da bacia. |
| 8 | 3.2, Tabela 1 | "Separada da série de vazão pela fonte dos dados; método não documentado" | Mesmo ponto do comentário 6. |
| 9 | 3.2, Tabela 1 | "(MURILLO-BERMÚDEZ et al., 2021)" | Padronizar para 2023, como na lista de referências. |
| 10 | 3.2 | "Da série horária obtêm-se, para cada evento, o volume escoado total" | Sumiram as fórmulas T_R = Σ Q · 3600 (m³) e SY_obs = Σ (Q · CSS · 3600 / 10⁶) (t). Sem elas, o leitor não sabe como a carga foi calculada. Restaurei no rascunho como equação. |
| 11 | 4.1 | "Modelo Calculado (FC)" | "(FC)" deve ser "(MC)". |
| 12 | 4.2.1, Tabela 6 | "Variáveis usadas em cada evento" | Faltam a coluna "Origem ou cálculo" (R = w₁·P₁ + (1 − w₁)·P₂, com w₁ = 0,307; T_R, V_base, V_dir, Qb_inicio, SY_obs) e a frase sobre a unidade de CSS (mg/L = g/m³). Restaurei no rascunho; decida se volta ao Doc. |
| 13 | 4.2.1 | "154.011 pixels, 138,2 km²" | Com o LS novo são 153.855 pixels e 138,1 km², como na 3.3. |
| 14 | 4.2.2 | "pelo método de Moore et al. (1991)" | Usar Moore e Burch (1986), como na 2.6 e na Tabela 4; Moore et al. (1991) não está nas referências. Sugestão: incluir a equação LS = (A_s/22,13)^0,4 · (sen β/0,0896)^1,3, com A_s limitada a 200 m, média 7,80 e r = 0,94 com a declividade. |
| 15 | 4.3 | "não inclui a vazão de base.A condição" | Falta espaço depois do ponto. |
| 16 | 4.3 | "foi herdada da fase em que o modelo foi calibrado contra o volume total" | Essa justificativa cita uma fase descartada. Justificar o AMC I de outra forma. Dado de apoio: com AMC I e λ = 0,20, o SCS-CN calcula 88% do escoamento direto medido (13.455 de 15.263 mil m³, Tabela 3). |
| 17 | 4.5 | "a base é o volume de referência acima" | "Acima" é vago. Sugestão: "o termo de base usa o volume de referência Qb_inicio · T_chuva · 3600". Definir Qb_inicio (m³/s; primeiro valor de Bt na janela) e T_chuva (h; maior duração entre os dois postos). |
| 18 | 4.5 | "Q = min(f · Q_SCS, P)" | Manter `min`: o escoamento do pixel é limitado, por cima, à chuva do pixel. Sugestão de texto: "limitado, por cima, à chuva do pixel". |
| 19 | 4.5 | "o volume de referência Qb_inicio · T_chuva · 3600 (m³)" | Acrescentar: "volume que o rio escoaria se mantivesse a vazão que já tinha no início do evento durante todo o tempo de chuva". |
| 20 | Capa | "ESPACIALIZAÇÃO DA EQUAÇÃO UNIVERSAL MODIFICADA..." | A capa aparece duas vezes no Doc (folha de rosto repetida). Conferir se é intencional. |
