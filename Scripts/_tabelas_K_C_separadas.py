"""Separa a Tabela 5 (K e C) em duas tabelas, com a fonte de cada valor (artigo da IC). Pedido do orientador, 27/10/2026."""
import io
linhas = [l.strip() for l in io.open(r"C:/TCC/TCC_Texto/tabelas/tab_fatores_classes.md", encoding="utf-8") if l.startswith("| Solo:") or l.startswith("| Uso:")]
FK = {"Cambissolos Háplicos": "Corrêa, Moraes e Pinto (2015)", "Argissolos Vermelho-Amarelos": "Silva (2016)",
      "Neossolos Litólicos": "Silva e Alvares (2005); Chagas (2011); Rocha Lima et al. (2016); Demarchi e Zimback (2014); Castro et al. (2011)",
      "Afloramento Rochoso": "Martins et al. (2011)", "Área Urbana": "sem classe de solo (área urbana); K = 0 adotado [conferir]"}
FC = {"Lavoura Temporária": "Silva e Luchiari (2016) (cultura anual)", "Campo": "Silva et al. (2016) (pastagem)",
      "Silvicultura": "Silva et al. (2016) (reflorestamento)", "Mata Nativa": "Silva et al. (2016) (vegetação nativa)",
      "Corpos D'Água": "Wischmeier e Smith (1978)", "Solo exposto": "Wischmeier e Smith (1978)",
      "Área Urbanizada": "C = 0 adotado (superfície impermeável) [sem fonte na IC]",
      "Mineração": "C = 1 adotado, como solo exposto [sem fonte na IC]", "Afloramento Rochoso": "C = 1 adotado [sem fonte na IC]"}
k = ["| Classe de solo | K (t·h·MJ⁻¹·mm⁻¹) | Pixels de cálculo (%) | Fonte do valor |", "|---|---|---|---|"]
c = ["| Classe de uso | C (adimensional) | Pixels de cálculo (%) | Fonte do valor |", "|---|---|---|---|"]
for l in linhas:
    _, cl, v, pct, _ = [x.strip() for x in l.split("|")]
    tipo, nome = cl.split(": ", 1)
    (k if tipo == "Solo" else c).append(f"| {nome} | {v} | {pct} | {(FK if tipo == 'Solo' else FC)[nome]} |")
io.open(r"C:/TCC/TCC_Texto/tabelas/tab_fator_K.md", "w", encoding="utf-8", newline="\n").write("\n".join(k) + "\n")
io.open(r"C:/TCC/TCC_Texto/tabelas/tab_fator_C.md", "w", encoding="utf-8", newline="\n").write("\n".join(c) + "\n")
print("gravados: tab_fator_K.md e tab_fator_C.md")
