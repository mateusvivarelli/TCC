// Slides 11 a 28 da defesa (e um slide de apoio), seguindo Notas Claude/plano_slides_defesa_14-11.md.
// Uso: node Scripts/slides_defesa/2_monta_slides.js   (depois de rodar 1_figuras_slides.py)
// Saida: TCC_Texto/slides/slides_defesa_completo.pptx (slide 8 e do 11 em diante)
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const BASE = path.resolve(__dirname, "..", "..");
const FIG = path.join(BASE, "TCC_Texto", "figuras");
const OUTDIR = path.join(BASE, "TCC_Texto", "slides");
fs.mkdirSync(OUTDIR, { recursive: true });

const NAVY = "1B3A6B", BLUE = "2F6DB5", TINT = "EEF3FA", ORANGE = "C77B12", TEXT = "262626", MUTED = "5F6670", WHITE = "FFFFFF", LINE = "C9D3E0";
const W = 13.333, M = 0.6;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Mateus Guilherme Vivarelli";
pres.title = "Defesa do TCC: slides 8 e 11 em diante";
pres.theme = { headFontFace: "Calibri", bodyFontFace: "Calibri" };

pres.defineSlideMaster({
  title: "CONTEUDO",
  background: { color: WHITE },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.7, w: W - 2 * M, h: 0.8, fontFace: "Calibri", fontSize: 30, bold: true, color: NAVY, valign: "middle", align: "left", margin: 0 }, text: "" } },
  ],
});

// dimensoes de um PNG (cabecalho IHDR)
function dims(f) { const b = fs.readFileSync(f); return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) }; }
function img(s, rel, x, y, w, h, alt) {
  const f = path.join(FIG, rel); const d = dims(f); const r = d.w / d.h;
  let iw = w, ih = w / r; if (ih > h) { ih = h; iw = h * r; }
  s.addImage({ path: f, x: x + (w - iw) / 2, y: y + (h - ih) / 2, w: iw, h: ih, altText: alt || rel });
}
function base(sec, title, fonte) {
  const s = pres.addSlide({ masterName: "CONTEUDO", sectionTitle: sec });
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: W, h: 0.55, fill: { color: NAVY }, line: { color: NAVY } });
  s.addText(sec, { x: M, y: 0, w: 8, h: 0.55, fontSize: 16, bold: true, color: WHITE, valign: "middle", margin: 0, isTextBox: true });
  s.addText(title, { placeholder: "title" });
  if (fonte) s.addText(fonte, { x: M, y: 6.86, w: W - 2 * M, h: 0.5, fontSize: 11, color: MUTED, italic: true, margin: 0, isTextBox: true, valign: "middle" });
  return s;
}
// marcacao simples: a_{sub} e a^{sup}
function rt(txt, o) {
  o = o || {}; const runs = []; const re = /([_^])\{([^}]*)\}/g; let last = 0, m;
  const push = (t, extra) => { if (!t) return; const parts = t.split("\n");
    parts.forEach((p, i) => { if (p) runs.push({ text: p, options: Object.assign({}, o, extra) }); if (i < parts.length - 1) runs.push({ text: "", options: Object.assign({}, o, { breakLine: true }) }); }); };
  while ((m = re.exec(txt))) { push(txt.slice(last, m.index), {}); push(m[2], m[1] === "_" ? { subscript: true } : { superscript: true }); last = re.lastIndex; }
  push(txt.slice(last), {}); return runs;
}
function eq(s, txt, x, y, w, h, size) {
  s.addText(rt(txt), { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.06, x, y, w, h, fill: { color: TINT }, fontFace: "Cambria Math", fontSize: size || 20, color: TEXT, align: "center", valign: "middle", margin: 0.1 });
}
function stat(s, big, small, x, y, w, color) {
  s.addText(big, { x, y, w, h: 0.75, fontSize: 40, bold: true, color: color || NAVY, margin: 0, isTextBox: true, valign: "bottom" });
  s.addText(small, { x, y: y + 0.78, w, h: 0.55, fontSize: 15, color: MUTED, margin: 0, isTextBox: true, valign: "top" });
}
function linhas(s, itens, x, y, w, h, size) {
  // itens: [ [rotulo, texto], ... ] -> paragrafos com rotulo em negrito
  const runs = [];
  itens.forEach((it, i) => {
    if (it[0]) runs.push({ text: it[0] + " ", options: { bold: true, color: NAVY } });
    runs.push({ text: it[1], options: { color: TEXT, breakLine: i < itens.length - 1, paraSpaceAfter: 10 } });
  });
  s.addText(runs, { x, y, w, h, fontSize: size || 17, valign: "top", margin: 0, isTextBox: true });
}
function marcadores(s, itens, x, y, w, h, size) {
  s.addText(itens.map((t, i) => ({ text: t, options: { bullet: { indent: 18 }, breakLine: i < itens.length - 1, paraSpaceAfter: 8 } })),
    { x, y, w, h, fontSize: size || 17, color: TEXT, valign: "top", margin: 0, isTextBox: true });
}
function caixa(s, txt, x, y, w, h, opt) {
  opt = opt || {};
  s.addText(txt, { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.06, x, y, w, h, fill: { color: opt.fill || TINT }, line: { color: opt.line || LINE, width: 1 },
    color: opt.color || TEXT, fontSize: opt.size || 15, bold: !!opt.bold, align: "center", valign: "middle", margin: 0.08 });
}
function seta(s, x, y, w) { s.addShape(pres.shapes.RIGHT_ARROW, { x, y, w, h: 0.32, fill: { color: BLUE }, line: { color: BLUE } }); }

const SM = "Método: o evento 11", SR = "Resultados", SC = "Conclusão", SE = "Encerramento", SA = "Apoio";
pres.addSection({ title: "Área de estudo" });
// ---------------------------------------------------------------- 8 solo e uso
{
  const s = base("Área de estudo", "Solo e uso do solo na parte alta da bacia", "Fonte: elaborado pelo autor, com os mapas de solo e de uso do Plano de Bacias (Consórcio Profill-Rhama, 2020)");
  img(s, "mapas/mapa_02_solo_uso.png", M, 1.7, W - 2 * M, 4.1, "Classes de solo e de uso do solo na área de estudo");
  linhas(s, [
    ["Solo:", "Cambissolos Háplicos em 69% da área (K = 0,0475) e Argissolos Vermelho-Amarelos em 18% (K = 0,0351)"],
    ["Uso:", "mata nativa 40%, campo 29%, área urbana 14%, silvicultura 13%, lavoura temporária 4%"],
  ], M, 5.95, W - 2 * M, 0.9, 16);
  s.addNotes("Antes do método, a distribuição do solo e do uso na bacia. O solo é dominado pelos Cambissolos Háplicos, cerca de 69% da área, com a maior erodibilidade (K = 0,0475); os Argissolos ocupam cerca de 18%. No uso, a mata nativa cobre cerca de 40%, sobretudo na cabeceira a leste; o campo, 29%; a área urbana, 14%, perto do exutório; a silvicultura, 13%; e a lavoura temporária, 4%. Esses mapas dão os fatores K e C de cada pixel, com os valores por classe de Vivarelli et al. (2025).");
}

pres.addSection({ title: SM });

// ---------------------------------------------------------------- 11 dados
{
  const s = base(SM, "Dados: 17 eventos monitorados e mapas de 30 m", "Fontes: Murillo-Bermúdez e Martim (2022); Murillo-Bermúdez et al. (2023); Consórcio Profill-Rhama (2020); Agência Nacional de Águas e Saneamento Básico (2024); USGS");
  linhas(s, [
    ["Chuva:", "2 postos com registro horário: DBT5 (fora da bacia, a leste) e Campo Limpo Paulista (perto do exutório)"],
    ["Vazão:", "estação telemétrica do DAEE no exutório (SAISP), usada em intervalo horário"],
    ["Sedimento:", "turbidez horária da água bruta da SABESP, convertida em concentração (CSS) por curva de calibração"],
    ["Carga do evento:", "soma, hora a hora, de vazão × CSS"],
  ], M, 1.8, 5.2, 2.75, 16);
  s.addText([
    { text: "Dados espaciais (rasters de 30 m)", options: { bold: true, color: NAVY, fontSize: 16, breakLine: true } },
    { text: "Relevo e fator LS: ", options: { bold: true, color: TEXT, fontSize: 14 } }, { text: "MDE do USGS", options: { color: TEXT, fontSize: 14, breakLine: true } },
    { text: "Solo e uso (K e C): ", options: { bold: true, color: TEXT, fontSize: 14 } }, { text: "Plano de Bacias (Consórcio Profill-Rhama, 2020)", options: { color: TEXT, fontSize: 14, breakLine: true } },
    { text: "Número de curva: ", options: { bold: true, color: TEXT, fontSize: 14 } }, { text: "BR_CN-2022 (Agência Nacional de Águas e Saneamento Básico, 2024)", options: { color: TEXT, fontSize: 14 } },
  ], { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.06, x: M, y: 4.7, w: 5.3, h: 2.0, fill: { color: TINT }, line: { color: LINE, width: 1 }, valign: "top", margin: 10, paraSpaceAfter: 4 });
  const carga = [266, 2040, 928, 1380, 1372, 199, 1317, 2109, 1155, 847, 1822, 211, 1196, 1731, 3829, 1736, 1710];
  const labels = carga.map((_, i) => String(i + 1));
  s.addChart(pres.charts.BAR, [
    { name: "Demais eventos", labels, values: carga.map((v, i) => (i === 10 ? 0 : v)) },
    { name: "Evento 11", labels, values: carga.map((v, i) => (i === 10 ? v : 0)) },
  ], {
    x: 6.2, y: 1.75, w: 6.55, h: 4.95, barGrouping: "stacked", barGapWidthPct: 45, chartColors: ["9DB6D6", "C77B12"],
    showTitle: true, title: "Carga de sedimentos medida por evento (t)", titleFontSize: 15, titleColor: TEXT, titleFontFace: "Calibri",
    showLegend: true, legendPos: "b", legendFontSize: 12, legendFontFace: "Calibri", legendColor: TEXT,
    catAxisLabelColor: MUTED, valAxisLabelColor: MUTED, catAxisLabelFontSize: 12, valAxisLabelFontSize: 12, catAxisLabelFontFace: "Calibri", valAxisLabelFontFace: "Calibri",
    showCatAxisTitle: true, catAxisTitle: "Evento", catAxisTitleFontSize: 12, catAxisTitleColor: MUTED, catAxisTitleFontFace: "Calibri", dataLabelFontFace: "Calibri",
    valGridLine: { color: "E3E7ED", size: 0.5 }, catGridLine: { style: "none" }, valAxisLabelFormatCode: "#,##0",
  });
  s.addNotes("Os dados vêm do monitoramento do rio Jundiaí feito pelo grupo do Luis (Murillo-Bermúdez e Martim, 2022; Murillo-Bermúdez et al., 2023). A chuva vem de dois postos; um deles, o DBT5, fica fora da bacia, a leste. A vazão é da estação do DAEE no exutório. O sedimento não é medido direto: a SABESP mede a turbidez da água bruta de hora em hora, e uma curva de calibração converte turbidez em concentração. A carga de cada evento é a soma, hora a hora, da vazão vezes a concentração. São 17 eventos, de novembro de 2018 a fevereiro de 2020, com cargas de cerca de 200 t a 3.800 t. Os mapas, todos em pixels de 30 m, vêm de três fontes: o relevo e o fator LS, do modelo digital de elevação do USGS; o solo e o uso, que dão K e C, do Plano de Bacias (Consórcio Profill-Rhama, 2020), com os valores por classe de Vivarelli et al. (2025); e o número de curva, da base nacional BR_CN-2022 da Agência Nacional de Águas e Saneamento Básico (2024). Vou acompanhar o evento 11, em laranja, do começo ao fim, como no Apêndice A.");
}

// ---------------------------------------------------------------- 12 evento 11
{
  const s = base(SM, "Evento 11: 4 a 8 de julho de 2019", "Fonte: elaborado pelo autor, com os dados de Murillo-Bermúdez e Martim (2022)");
  img(s, "slides/ev11_hidrograma.png", M, 1.7, 8.4, 5.1, "Chuva dos dois postos, vazão, vazão de base e concentração de sedimentos no evento 11");
  stat(s, "74,0 mm", "chuva do evento (média ponderada dos 2 postos)", 9.4, 1.75, 3.4);
  stat(s, "11,8 mm/h", "maior intensidade em 1 hora", 9.4, 3.05, 3.4);
  stat(s, "1.479 mil m³", "escoamento direto medido (área azul)", 9.4, 4.35, 3.4);
  stat(s, "1.822 t", "carga de sedimentos medida", 9.4, 5.65, 3.4, ORANGE);
  s.addNotes("O evento 11 durou 91 horas, de 4 a 8 de julho de 2019. Choveu 74 mm em média, com no máximo 11,8 mm em uma hora: é uma chuva longa e pouco concentrada. A área azul é o escoamento direto, a vazão menos a vazão de base: 1,48 milhão de m³. A carga medida foi de 1.822 t. Esse é o valor que o modelo tenta reproduzir. (Rápido: 25 segundos.)");
}

// ---------------------------------------------------------------- 13 chuva IDW
{
  const s = base(SM, "Passo 1: chuva em cada pixel (IDW)", "Fonte: elaborado pelo autor. Método: Shepard (1968)");
  img(s, "slides/ev11_chuva.png", M, 1.7, 7.6, 5.1, "Chuva interpolada do evento 11");
  eq(s, "P_{k} = Σ w_{i} P_{i} / Σ w_{i} ,   w_{i} = 1 / d_{i}^{2}", 8.6, 1.85, 4.15, 0.9, 20);
  linhas(s, [
    ["Postos:", "DBT5 = 62,8 mm; Campo Limpo = 79,0 mm"],
    ["Pixels:", "de 63,2 a 79,0 mm (média 73,5 mm)"],
    ["Pixel de exemplo:", "P = 75,4 mm"],
  ], 8.6, 3.0, 4.15, 2.2, 17);
  s.addText("Com 2 postos, a chuva vira um gradiente suave entre leste e oeste.", { x: 8.6, y: 5.3, w: 4.15, h: 1.0, fontSize: 16, italic: true, color: NAVY, margin: 0, isTextBox: true, valign: "top" });
  s.addNotes("Primeiro passo: levar a chuva dos postos para cada pixel, pelo inverso do quadrado da distância. No evento 11 choveu mais a oeste, perto de Campo Limpo. O pixel que vou acompanhar recebeu 75,4 mm. Com só dois postos, a chuva é sempre um gradiente suave; núcleos de chuva entre os postos não aparecem. (Rápido: 25 segundos.)");
}

// ---------------------------------------------------------------- 14 SCS-CN
{
  const s = base(SM, "Passo 2: escoamento direto em cada pixel (SCS-CN)", "Fonte: elaborado pelo autor. Método: Chow, Maidment e Mays (1988). CN: raster BR_CN-2022 (Agência Nacional de Águas e Saneamento Básico, 2024)");
  img(s, "slides/ev11_escoamento.png", M, 1.7, 7.6, 5.1, "Escoamento direto calculado no evento 11");
  eq(s, "Q = (P − 0,05 S)^{2} / (P + 0,95 S)", 8.6, 1.85, 4.15, 0.8, 20);
  s.addText("Pixel de exemplo (lavoura temporária sobre Argissolo)", { x: 8.6, y: 2.85, w: 4.15, h: 0.4, fontSize: 15, bold: true, color: NAVY, margin: 0, isTextBox: true });
  eq(s, "Q = (75,4 − 12,2)^{2} / (75,4 + 0,95 × 244,2)\n= 13,0 mm", 8.6, 3.3, 4.15, 1.15, 17);
  linhas(s, [
    ["Bacia:", "escoamento médio de 7,2 mm"],
    ["Volume:", "997 mil m³ calculados contra 1.479 mil m³ medidos (67%)"],
  ], 8.6, 4.75, 4.15, 1.8, 16);
  s.addNotes("Segundo passo: transformar a chuva em escoamento direto pelo SCS-CN, pixel a pixel. No pixel de exemplo, a abstração inicial é 12,2 mm; da chuva de 75,4 mm, escoam 13 mm. Na bacia toda, o escoamento médio foi 7,2 mm, e o volume calculado ficou em 67% do medido. De onde vêm o S de 244 mm e o 0,05 da fórmula é o próximo slide.");
}

// ---------------------------------------------------------------- 15 parentese 1
{
  const s = base(SM, "Parêntese 1: condição seca (CN-I) e λ = 0,05", "Fontes: Chow, Maidment e Mays (1988); Woodward et al. (2003); Brandão et al. (2025). CN-II: raster BR_CN-2022 (Agência Nacional de Águas e Saneamento Básico, 2024)");
  const y = 1.95, h = 1.1, bw = 2.15, gap = 0.42;
  const etapas = [["CN-II = 81,0", "tabelado (uso × solo)"], ["CN-I = 64,2", "condição seca (Chow)"], ["S_{0,20} = 141,9 mm", "retenção do CN"], ["S_{0,05} = 244,2 mm", "convertida (Woodward)"], ["I_{a} = 12,2 mm", "0,05 × S_{0,05}"]];
  etapas.forEach((e, i) => {
    const x = M + i * (bw + gap);
    s.addText(rt(e[0], { bold: true, fontSize: 17, color: NAVY }).concat([{ text: "", options: { breakLine: true } }], rt(e[1], { fontSize: 13, color: MUTED })),
      { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.06, x, y, w: bw, h, fill: { color: TINT }, line: { color: LINE, width: 1 }, align: "center", valign: "middle", margin: 0.05 });
    if (i < etapas.length - 1) seta(s, x + bw + 0.06, y + h / 2 - 0.16, gap - 0.12);
  });
  img(s, "slides/ev11_retencao.png", M, 3.35, 6.3, 3.45, "Retenção S0,05 convertida no evento 11");
  s.addText("Por que essa combinação?", { x: 7.25, y: 3.4, w: 5.5, h: 0.45, fontSize: 18, bold: true, color: NAVY, margin: 0, isTextBox: true });
  marcadores(s, [
    "Aproxima o volume total dos 17 eventos (viés de +3%)",
    "λ = 0,05 teve melhor desempenho médio em 3.578 bacias (Brandão et al., 2025)",
    "S convertido pela relação de Woodward et al. (2003)",
    "Limitação: escolhida olhando os mesmos 17 eventos",
  ], 7.25, 3.95, 5.5, 2.8, 16);
  s.addNotes("Primeiro parêntese. O número de curva tabelado é para a condição média; usei a condição seca, CN-I. E usei a razão de abstração inicial de 0,05, e não a de 0,20, com a retenção convertida pela relação de Woodward et al. (2003). Essa combinação foi escolhida porque aproxima o volume total dos 17 eventos, com viés de 3%, e tem apoio na literatura: Brandão et al. (2025) encontraram melhor desempenho médio com 0,05 em milhares de bacias. Uma limitação: a escolha foi feita olhando os mesmos eventos que depois são avaliados. (Não dizer que foi 'calibrado com base' em Brandão.)");
}

// ---------------------------------------------------------------- 16 pico local
{
  const s = base(SM, "Passo 3: vazão de pico local (Hao et al., 2022)", "Fonte: elaborado pelo autor, com a formulação de Hao et al. (2022)");
  eq(s, "p_{r,k} = (Q_{k} / 1000) × A_{pix} × (RI / R) / 3600", M, 1.85, 7.2, 0.95, 22);
  s.addText("Pixel de exemplo, evento 11", { x: M, y: 3.05, w: 7.2, h: 0.4, fontSize: 16, bold: true, color: NAVY, margin: 0, isTextBox: true });
  const cx = [["11,67 m³", "volume do pixel\n0,013 m × 897 m²"], ["0,159 /h", "RI / R\n11,8 mm/h ÷ 74,0 mm"], ["5,17 × 10^{−4} m³/s", "pico local\n÷ 3.600 s"]];
  cx.forEach((c, i) => {
    const x = M + i * 2.45;
    s.addText(rt(c[0], { bold: true, fontSize: 18, color: NAVY }).concat([{ text: "", options: { breakLine: true } }], rt(c[1], { fontSize: 13, color: MUTED })),
      { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.06, x, y: 3.5, w: 2.2, h: 1.35, fill: { color: TINT }, line: { color: LINE, width: 1 }, align: "center", valign: "middle", margin: 0.05 });
  });
  s.addText("O que isso quer dizer", { x: 8.3, y: 1.85, w: 4.45, h: 0.45, fontSize: 18, bold: true, color: NAVY, margin: 0, isTextBox: true });
  marcadores(s, [
    "Não há hidrograma no pixel: o volume do pixel é distribuído no tempo conforme a concentração da chuva",
    "RI/R é um número por evento, então o pico local é proporcional a Q",
    "O pico local não traz informação espacial nova; dá mais peso a eventos de chuva concentrada",
    "Nos eventos 1 e 12, RI/R passa de 1 (índice, não fração)",
  ], 8.3, 2.4, 4.45, 4.3, 16);
  s.addText(rt("Consequência: E cresce com Q^{1,12}", {}), { x: M, y: 5.25, w: 7.2, h: 0.6, fontSize: 20, bold: true, color: ORANGE, margin: 0, isTextBox: true });
  s.addNotes("A fórmula de Williams precisa de uma vazão de pico, e um pixel não tem hidrograma. Seguindo Hao et al. (2022), o volume escoado no pixel é distribuído no tempo pela concentração da chuva, a razão entre a maior intensidade em uma hora e a lâmina do evento. No pixel de exemplo: 11,67 m³ vezes 0,159 por hora, dividido por 3.600, dá 5,17 × 10⁻⁴ m³/s. Ponto importante, que vale dizer antes que perguntem: como RI/R é um só número por evento, o pico local é proporcional ao escoamento. Ele não acrescenta informação espacial; o papel dele é dar mais peso aos eventos de chuva concentrada. Por isso a erosão cresce com Q elevado a 1,12. Nos eventos 1 e 12, RI/R passa de 1, porque RI vem do posto mais intenso e R é a média dos dois.");
}

// ---------------------------------------------------------------- 17 erosao local
{
  const s = base(SM, "Passo 4: erosão local em cada pixel (Williams, 1975)", "Fonte: elaborado pelo autor. Equação: Williams (1975). K e C: mapas de solo e uso do Consórcio Profill-Rhama (2020), com valores por classe de Vivarelli et al. (2025); LS: MDE de 30 m do USGS (Moore e Burch, 1986)");
  img(s, "slides/ev11_eunit_sem_escala.png", M, 1.7, 7.2, 4.55, "Índice de erosão E_unit no evento 11");
  s.addText("Mais escuro = maior índice de erosão (valor relativo)", { x: M, y: 6.3, w: 7.2, h: 0.4, fontSize: 14, color: MUTED, italic: true, margin: 0, isTextBox: true, align: "center" });
  eq(s, "E_{unit} = 11,8 (Q · p_{r} · A_{pix})^{0,56} · K · LS · C · P", 8.15, 1.85, 4.6, 0.85, 18);
  s.addText("Pixel de exemplo", { x: 8.15, y: 2.95, w: 4.6, h: 0.4, fontSize: 16, bold: true, color: NAVY, margin: 0, isTextBox: true });
  eq(s, "11,8 × (13,0 × 5,17·10^{−4} × 897)^{0,56}\n× 0,0351 × 4,869 × 0,212 = 1,167", 8.15, 3.4, 4.6, 1.15, 16);
  linhas(s, [
    ["K = 0,0351", "(Argissolo)   "],
    ["LS = 4,869", "(declividade e comprimento de rampa)   "],
    ["C = 0,212", "(lavoura temporária);  P = 1"],
  ], 8.15, 4.8, 4.6, 1.6, 15);
  s.addNotes("Com o escoamento e o pico de cada pixel, a erosão local é a equação de Williams com os coeficientes originais, 11,8 e 0,56. K e C vêm de Vivarelli et al. (2025) e não foram recalibrados aqui. Atenção: o 11,8 da equação é a constante de Williams, não a intensidade da chuva do slide anterior (coincidência de valores). No pixel de exemplo, o resultado é 1,167. Esse número é um índice, não toneladas: o mapa mostra onde a erosão é maior em termos relativos. Por que não é tonelada é o próximo parêntese.");
}

// ---------------------------------------------------------------- 18 parentese 2: c
{
  const s = base(SM, "Parêntese 2: o coeficiente c", "Fonte: elaborado pelo autor");
  stat(s, "40.885", "soma do índice E nos 153.855 pixels (evento 11)", M, 1.75, 3.3);
  stat(s, "1.822 t", "carga medida no evento 11", M + 3.5, 1.75, 2.6, ORANGE);
  eq(s, "SY_{n} = c × Σ_{k} E_{unit,k}", 7.1, 1.8, 5.65, 0.9, 24);
  s.addText("Lido como tonelada, o índice daria 22 vezes o medido: c = 0,0344 converte o índice em toneladas (MC)", { x: 7.1, y: 2.85, w: 5.65, h: 0.75, fontSize: 16, bold: true, color: NAVY, margin: 0, isTextBox: true, valign: "top" });
  marcadores(s, [
    "Williams ajustou a equação para bacias inteiras (m³ e m³/s); aqui ela é aplicada a pixels de 897 m²",
    "c faz o papel de uma taxa de transferência média da bacia (conectividade)",
    "c minúsculo = coeficiente de escala;  C maiúsculo = cobertura",
  ], M, 3.85, 5.6, 3.0, 16);
  img(s, "slides/ev11_sedimento.png", 6.5, 3.75, 6.25, 2.7, "Sedimento produzido em cada pixel no evento 11");
  s.addText("c × E: 40,1 kg no pixel de exemplo", { x: 6.5, y: 6.45, w: 6.25, h: 0.35, fontSize: 14, color: MUTED, italic: true, margin: 0, isTextBox: true, align: "center" });
  s.addNotes("Segundo parêntese, o coeficiente c. A equação de Williams foi ajustada para bacias inteiras, com volume em m³ e pico em m³/s. Aqui ela é aplicada a pixels de 897 m², com escoamento em mm. O resultado é um índice. Se eu somasse o índice como se fosse tonelada, o evento 11 daria 40.885 t, 22 vezes o medido. O coeficiente c faz essa conversão: 0,0344 no modelo calculado. Fisicamente, faz o papel de uma taxa de transferência média da bacia, a parte do que erode que chega ao exutório. Atenção à notação: c minúsculo é esse coeficiente; C maiúsculo é a cobertura. No pixel de exemplo, c vezes 1,167 dá 40,1 kg.");
}

// ---------------------------------------------------------------- 19 calibracao e validacao
{
  const s = base(SM, "Calibração e validação cruzada (leave-one-out)", "Métodos: Hao et al. (2022); Cawley e Talbot (2010)");
  eq(s, "c = exp[ (1/17) Σ ln (SY_{obs,n} / ΣE_{n}) ]", M, 1.85, 6.0, 0.9, 20);
  s.addText("Calibração em escala logarítmica: média geométrica das razões medido / índice. Nenhum evento grande comanda o ajuste.", { x: M, y: 2.9, w: 6.0, h: 0.9, fontSize: 16, color: TEXT, margin: 0, isTextBox: true, valign: "top" });
  // 17 quadradinhos: evento 11 retirado
  s.addText("Validação cruzada: para cada evento", { x: M, y: 4.0, w: 6.0, h: 0.4, fontSize: 16, bold: true, color: NAVY, margin: 0, isTextBox: true });
  for (let i = 0; i < 17; i++) {
    const out = i === 10;
    s.addText(String(i + 1), { shape: pres.shapes.RECTANGLE, x: M + i * 0.35, y: 4.5, w: 0.3, h: 0.42, fill: { color: out ? ORANGE : TINT }, line: { color: out ? ORANGE : LINE, width: 1 }, fontSize: 11, bold: out, color: out ? WHITE : TEXT, align: "center", valign: "middle", margin: 0 });
  }
  s.addText("ajusta c nos outros 16  →  prevê o evento retirado  →  repete 17 vezes", { x: M, y: 5.05, w: 6.0, h: 0.4, fontSize: 15, color: TEXT, margin: 0, isTextBox: true });
  s.addText("Evento 11 no MC", { x: 7.3, y: 1.85, w: 5.45, h: 0.45, fontSize: 18, bold: true, color: NAVY, margin: 0, isTextBox: true });
  stat(s, "1.406 t", "ajuste (c dos 17 eventos)", 7.3, 2.3, 2.6);
  stat(s, "1.383 t", "validação cruzada (c sem o evento 11)", 10.1, 2.3, 2.65);
  stat(s, "−24%", "em relação aos 1.822 t medidos", 7.3, 3.75, 2.6, ORANGE);
  s.addText("A validação refaz só o c. CN-I e λ foram escolhidos antes, nos mesmos eventos: as métricas tendem a ser um pouco otimistas.", { x: 7.3, y: 5.35, w: 5.45, h: 1.3, fontSize: 15, italic: true, color: MUTED, margin: 0, isTextBox: true, valign: "top" });
  s.addNotes("O único parâmetro calibrado com o sedimento medido é o c. Ele é calibrado em escala logarítmica: na prática, é a média geométrica das razões entre a carga medida e a soma do índice. Assim nenhum evento grande, como o 15, domina o ajuste. Para avaliar o modelo sem viés de otimismo, usei a validação cruzada deixando um de fora: tiro o evento, ajusto c com os outros 16, prevejo o que ficou de fora e repito para os 17. No evento 11: 1.406 t no ajuste, 1.383 t na validação, 24% abaixo do medido. Ressalva: a validação refaz só o c; as escolhas do CN-I e do λ foram feitas antes, olhando os mesmos eventos.");
}

// ---------------------------------------------------------------- 20 resultado do MC
pres.addSection({ title: SR });
{
  const s = base(SR, "Modelo calculado: pior que a regra simples com a chuva", "Fonte: elaborado pelo autor (validação cruzada, 17 eventos)");
  img(s, "slides/dispersao_simples_e_MC.png", M, 1.65, 8.3, 4.9, "Descarga de sedimentos simulada contra medida: modelo simples com a chuva e modelo calculado");
  s.addText("Mesma informação: só a chuva", { x: 9.2, y: 1.75, w: 3.55, h: 0.45, fontSize: 17, bold: true, color: NAVY, margin: 0, isTextBox: true });
  stat(s, "81%  ×  42%", "erro mediano: MC × regra simples", 9.2, 2.2, 3.55);
  stat(s, "35%  ×  82%", "eventos dentro de fator 2", 9.2, 3.55, 3.55);
  s.addText("O MC foi pior em 14 dos 17 eventos (Wilcoxon, p = 0,02). Erros de 10% do medido (evento 10) a 3,1 vezes (evento 9).", { x: 9.2, y: 5.0, w: 3.55, h: 1.6, fontSize: 15, color: TEXT, margin: 0, isTextBox: true, valign: "top" });
  s.addNotes("Agora saio do evento 11 e olho os 17. À direita, o modelo calculado, só com a chuva como entrada: erro mediano de 81% e só 35% dos eventos dentro de fator 2, isto é, entre a metade e o dobro do medido. À esquerda, uma regra simples: carga proporcional à chuva do evento. Ela usa a mesma informação e erra 42%, com 82% dentro de fator 2. O modelo calculado foi pior em 14 dos 17 eventos. Então o problema está no caminho entre a chuva e a carga, e o próximo slide mostra onde.");
}

// ---------------------------------------------------------------- 21 escoamento e o gargalo
{
  const s = base(SR, "O erro vem do escoamento calculado", "Fontes: elaborado pelo autor; Baert et al. (2026). Escoamento direto medido = volume total menos a vazão de base");
  const med = [224, 1731, 585, 987, 832, 183, 650, 1250, 801, 552, 1479, 101, 735, 931, 2177, 1595, 449];
  const calc = [36, 521, 751, 154, 695, 158, 142, 1336, 1725, 57, 997, 63, 1073, 1363, 3963, 1934, 734];
  const labels = med.map((_, i) => String(i + 1));
  s.addChart(pres.charts.BAR, [{ name: "Medido", labels, values: med }, { name: "Calculado (SCS-CN)", labels, values: calc }], {
    x: M, y: 1.6, w: 7.6, h: 5.2, barGrouping: "clustered", barGapWidthPct: 40, chartColors: [NAVY, "E39B3A"],
    showTitle: true, title: "Escoamento direto por evento (mil m³)", titleFontSize: 15, titleColor: TEXT, titleFontFace: "Calibri",
    showLegend: true, legendPos: "t", legendFontSize: 13, legendFontFace: "Calibri", legendColor: TEXT,
    catAxisLabelColor: MUTED, valAxisLabelColor: MUTED, catAxisLabelFontSize: 12, valAxisLabelFontSize: 12, catAxisLabelFontFace: "Calibri", valAxisLabelFontFace: "Calibri",
    showCatAxisTitle: true, catAxisTitle: "Evento", catAxisTitleFontSize: 12, catAxisTitleColor: MUTED, catAxisTitleFontFace: "Calibri", dataLabelFontFace: "Calibri",
    valGridLine: { color: "E3E7ED", size: 0.5 }, catGridLine: { style: "none" }, valAxisLabelFormatCode: "#,##0",
  });
  stat(s, "+3%", "no total dos 17 eventos (15,7 contra 15,3 milhões de m³)", 8.55, 1.65, 2.05);
  stat(s, "46%", "de erro mediano em cada evento", 10.75, 1.65, 2.0, ORANGE);
  marcadores(s, [
    "Superestima as chuvas grandes (9, 15) e subestima as pequenas (1, 4, 7, 10): os erros se compensam no total",
    "Em 15 de 17 eventos, o sedimento erra no mesmo sentido do escoamento",
    "A erosão cresce com Q elevado a 1,12: o erro do escoamento chega ao sedimento um pouco ampliado",
    "Baert et al. (2026): MUSLE com escoamento previsto teve NSE ≈ 0; com o medido, 0,66",
  ], 8.55, 3.5, 4.2, 3.3, 15);
  s.addNotes("Este gráfico compara, evento a evento, o escoamento direto medido (azul) com o calculado pelo SCS-CN (laranja). Na soma dos 17 eventos, os dois quase coincidem: 15,7 contra 15,3 milhões de m³, 3% de diferença. Mas evento a evento o erro é grande, 46% na mediana: o método superestima as chuvas grandes, como os eventos 9 e 15, e subestima as pequenas, como 1, 4, 7 e 10, onde calcula menos de um quarto do medido. Esse erro passa direto para o sedimento: em 15 de 17 eventos, o sedimento erra no mesmo sentido do escoamento, e o erro do escoamento explica 91% da variação do erro do sedimento. De onde vem o expoente 1,12: a erosão de Williams usa (Q vezes o pico) elevado a 0,56; como o pico local é proporcional a Q (pico = Q vezes RI/R, com RI/R igual em todos os pixels), fica (Q vezes Q) elevado a 0,56, ou Q elevado a 1,12. Então um escoamento com metade do valor medido dá sedimento com cerca de 46% do valor. Baert et al. (2026) encontraram o mesmo: com escoamento previsto, a MUSLE não teve desempenho; com o medido, sim.");
}

// ---------------------------------------------------------------- 22 MFM
{
  const s = base(SR, "Modelo forçado ao medido (MFM): troca só o escoamento", "Fonte: elaborado pelo autor");
  const y = 1.9, h = 1.15;
  caixa(s, "Chuva IDW", M, y, 2.0, h, { size: 16 });
  seta(s, M + 2.08, y + h / 2 - 0.16, 0.35);
  caixa(s, "SCS-CN\n(padrão espacial)", M + 2.5, y, 2.3, h, { size: 16 });
  seta(s, M + 4.88, y + h / 2 - 0.16, 0.35);
  caixa(s, "Q × f\nf = V medido / V calculado", M + 5.3, y, 3.0, h, { size: 16, fill: "FCEFD9", line: ORANGE, bold: true });
  seta(s, M + 8.38, y + h / 2 - 0.16, 0.35);
  caixa(s, "Williams e c\n(recalibrado)", M + 8.8, y, 2.4, h, { size: 16 });
  s.addText("Evento 11", { x: M, y: 3.45, w: 6, h: 0.45, fontSize: 18, bold: true, color: NAVY, margin: 0, isTextBox: true });
  stat(s, "f = 1,48", "1.479 / 997 mil m³", M, 3.9, 2.8);
  stat(s, "1,55 ×", "a soma do índice (1,48 elevado a 1,12)", M + 3.0, 3.9, 2.8);
  stat(s, "1.387 t", "validação cruzada, c = 0,0222 (−24%)", M + 6.0, 3.9, 3.1);
  s.addText("O MFM não é uma previsão: usa o volume medido no mesmo hidrograma em que se mede a carga. Serve para isolar o efeito do escoamento.", { x: M, y: 5.6, w: 12.1, h: 0.9, fontSize: 17, italic: true, color: NAVY, margin: 0, isTextBox: true, valign: "top" });
  s.addNotes("Para testar o peso do escoamento, fiz uma segunda versão: o modelo forçado ao medido. Tudo continua igual, a mesma chuva distribuída, o mesmo padrão do SCS-CN, a mesma fórmula; só o volume de cada evento passa a ser o medido. Todos os pixels do evento são multiplicados pelo mesmo fator f, limitado à chuva do pixel. No evento 11, f é 1,48, a soma do índice cresce 1,55 vez, e o c recalibrado cai para 0,0222. Esse modelo não é uma previsão, porque usa o volume medido; ele serve para isolar o efeito do escoamento.");
}

// ---------------------------------------------------------------- 23 comparacao
{
  const s = base(SR, "Com o escoamento medido, o erro cai de 81% para 21%", "Fonte: elaborado pelo autor; modelo concentrado com os valores originais de Vivarelli et al. (2025)");
  img(s, "slides/escada_gargalo_vivarelli.png", M, 1.6, 12.1, 3.75, "Erro mediano e eventos dentro de fator 2, com escoamento calculado e com escoamento medido");
  const cards = [
    ["MFM × regra com o volume medido", "21% × 16% de erro mediano; diferença de +1,6 pontos (IC 95%: −5,5 a +10,4; p = 0,52): não se distinguem"],
    ["MFM × modelo concentrado (Vivarelli et al., 2025)", "21% × 22%: mesma ordem de erro. Comparação indicativa: o concentrado foi ajustado nos próprios eventos, sem validação cruzada"],
  ];
  cards.forEach((c, i) => {
    const x = M + i * 6.15;
    s.addText([{ text: c[0], options: { bold: true, color: NAVY, fontSize: 16, breakLine: true } }, { text: c[1], options: { color: TEXT, fontSize: 14 } }],
      { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.06, x, y: 5.5, w: 5.95, h: 1.3, fill: { color: TINT }, line: { color: LINE, width: 1 }, valign: "top", margin: 10 });
  });
  s.addNotes("Com o escoamento medido, o erro mediano da MUSLE espacializada cai de 81% para 21%, e 94% dos eventos ficam dentro de fator 2. Mas duas comparações são importantes. Primeiro, uma regra simples com o volume de escoamento direto medido, sem MUSLE, erra 16%: a diferença para o MFM é pequena e o intervalo de confiança inclui o zero; com 17 eventos, os dois não se distinguem. Segundo, o modelo concentrado de Vivarelli et al. (2025) erra 22%, a mesma ordem; mas ele foi ajustado nos próprios eventos, sem validação cruzada, então a comparação é só indicativa.");
}

// ---------------------------------------------------------------- 24 metricas
{
  const s = base(SR, "Como medimos o desempenho", "Fonte: elaborado pelo autor. Métodos: Nash e Sutcliffe (1970); Cawley e Talbot (2010). O = carga observada; S = carga simulada; n = evento");
  const cards = [
    ["Erro percentual mediano", "|S − O| / O em cada evento; mediana dos 17", "Quanto o modelo erra num evento típico. A mediana não deixa poucos eventos muito errados dominarem", "ideal: 0%"],
    ["Fator 2", "% de eventos com S entre O/2 e 2·O", "Quantos eventos ficam na ordem de grandeza certa", "ideal: 100%"],
    ["NSE (em log)", "1 − Σ(ln O − ln S)^{2} / Σ(ln O − ln Ō)^{2}", "Compara o modelo com prever sempre a média. Em log, pesa o erro relativo", "1 = perfeito; 0 = igual à média; < 0 = pior"],
    ["Spearman", "correlação entre as posições dos eventos", "Se o modelo coloca os eventos na ordem certa, do menor ao maior", "ideal: 1"],
    ["R²", "fração da variação explicada por uma regressão", "Usado para medir o que explica a carga (volume: 88%) e o padrão do mapa", "de 0 a 1"],
    ["Validação cruzada", "deixa um evento de fora, ajusta c nos outros 16", "Todas as métricas usam a previsão do evento que ficou de fora, sem viés de otimismo", "17 rodadas"],
  ];
  const cw = 3.85, ch = 2.45, gx = 0.275, gy = 0.2;
  cards.forEach((c, i) => {
    const x = M + (i % 3) * (cw + gx), y = 1.65 + Math.floor(i / 3) * (ch + gy);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: cw, h: ch, rectRadius: 0.06, fill: { color: TINT }, line: { color: LINE, width: 1 } });
    s.addText(c[0], { x: x + 0.15, y: y + 0.1, w: cw - 0.3, h: 0.4, fontSize: 17, bold: true, color: NAVY, margin: 0, isTextBox: true });
    s.addText(rt(c[1], { fontFace: "Cambria Math", fontSize: 13, color: TEXT }), { x: x + 0.15, y: y + 0.52, w: cw - 0.3, h: 0.5, margin: 0, isTextBox: true, valign: "top" });
    s.addText(c[2], { x: x + 0.15, y: y + 1.05, w: cw - 0.3, h: 0.95, fontSize: 13, color: TEXT, margin: 0, isTextBox: true, valign: "top" });
    s.addText(c[3], { x: x + 0.15, y: y + 2.0, w: cw - 0.3, h: 0.35, fontSize: 13, bold: true, color: ORANGE, margin: 0, isTextBox: true });
  });
  s.addNotes("Para comparar os modelos, usei quatro métricas, todas calculadas na validação cruzada. O erro percentual mediano diz quanto o modelo erra num evento típico; uso a mediana para que poucos eventos muito errados não dominem. O fator 2 é a fração de eventos em que o simulado fica entre a metade e o dobro do medido, ou seja, na ordem de grandeza certa. O NSE compara o modelo com a alternativa de prever sempre a média: 1 é perfeito, 0 é tão bom quanto a média e negativo é pior; calculo em log para pesar o erro relativo, como na calibração. O Spearman diz se o modelo ordena os eventos corretamente. O R² aparece em duas análises: quanto da carga o volume explica e quanto do padrão do mapa vem de cada fator. Para comparar dois modelos nos mesmos eventos, usei a mediana da diferença dos erros, com intervalo de confiança por bootstrap e o teste de Wilcoxon.");
}

// ---------------------------------------------------------------- apoio: tabela 13

{
  const s = base(SR, "Desempenho de todos os modelos", "Fonte: elaborado pelo autor (Tabela 13 do TCC). Validação cruzada, exceto o modelo concentrado (ajuste nos 17 eventos do trabalho original)");
  const H = (t) => ({ text: t, options: { bold: true, color: WHITE, fill: { color: NAVY } } });
  const rows = [
    [H("Modelo"), H("Informação medida"), H("Erro mediano"), H("Fator 2"), H("NSE log"), H("Spearman")],
    ["Regra simples com a chuva", "chuva", "41,9%", "82%", "0,53", "0,63"],
    ["MC (MUSLE espacializada)", "chuva", "81,1%", "35%", "−0,69", "0,59"],
    ["Regra simples com o volume", "escoamento direto", "15,9%", "94%", "0,85", "0,90"],
    ["MFM (MUSLE espacializada)", "escoamento direto", "20,6%", "94%", "0,84", "0,83"],
    ["Concentrado (Vivarelli et al., 2025)", "volume total e pico", "22,5%", "100%", "0,91", "0,93"],
  ];
  s.addTable(rows, { x: M, y: 1.9, w: 12.1, colW: [3.9, 2.5, 1.5, 1.3, 1.4, 1.5], fontSize: 16, fontFace: "Calibri", color: TEXT, border: { type: "solid", pt: 0.75, color: LINE }, rowH: 0.55, valign: "middle", align: "center" });
  marcadores(s, [
    "Com a mesma informação (só a chuva), a regra simples supera o MC",
    "Com o escoamento medido, MFM e regra com o volume não se distinguem (diferença de +1,6 pontos; p = 0,52)",
    "O concentrado foi ajustado nos próprios eventos, sem validação cruzada: comparação indicativa",
  ], M, 5.4, W - 2 * M, 1.4, 16);
  s.addNotes("Esta tabela reúne todos os modelos, com as quatro métricas. As duas primeiras linhas usam só a chuva: a regra simples erra 42% e o MC 81%. As duas seguintes usam o escoamento direto medido: a regra com o volume erra 16% e o MFM 21%; a diferença entre eles é pequena e, com 17 eventos, não se distingue de zero. A última é o modelo concentrado de Vivarelli et al. (2025), com os valores originais, ajustado nos mesmos 17 eventos e sem validação cruzada: tem a melhor métrica, mas a comparação é só indicativa.");
}

// ---------------------------------------------------------------- 25 mapas e areas criticas
{
  const s = base(SR, "Mapa de erosão média e áreas críticas", "Fonte: elaborado pelo autor. Erosão média dos 17 eventos (MC); áreas críticas = 5% dos pixels de maior erosão. Fatores: Consórcio Profill-Rhama (2020), Vivarelli et al. (2025), USGS e Agência Nacional de Águas e Saneamento Básico (2024)");
  img(s, "slides/mapa_medio_e_criticas_MC.png", M, 1.6, 5.4, 5.3, "Erosão média dos 17 eventos e áreas críticas do modelo calculado");
  stat(s, "46% → 83%", "campo, silvicultura e lavoura temporária: % da área → % da erosão", 6.4, 1.7, 3.1);
  stat(s, "93%", "da erosão vem dos Cambissolos Háplicos (69% da área)", 9.7, 1.7, 3.05);
  stat(s, "65% → 78%", "encostas acima de 20%: % da área → % da erosão", 6.4, 3.25, 3.1);
  stat(s, "94%", "das áreas críticas coincidem no MC e no MFM (r = 0,98)", 9.7, 3.25, 3.05, ORANGE);
  marcadores(s, [
    "Padrão espacial: 37% dos fatores K, LS e C e 63% do escoamento (chuva e CN), em escala log",
    "Mapa relativo: depende de K e C adotados, área urbana sem erosão e sem validação espacial",
    "Mostra onde a erosão é produzida, não onde o sedimento chega ao rio",
  ], 6.4, 4.85, 6.35, 2.0, 15);
  s.addNotes("Essa é a contribuição que o modelo concentrado não dá: onde a erosão acontece. As áreas críticas ficam na porção central e oeste. Campo, silvicultura e lavoura temporária ocupam 46% da área e respondem por 83% da erosão média; 93% vem dos Cambissolos; as encostas acima de 20% respondem por 78%. O mapa do MC e o do MFM coincidem em 94% das áreas críticas, o que é esperado, porque usam o mesmo padrão espacial; não é validação. Em escala logarítmica, 63% da variação espacial vem do escoamento, isto é, da chuva de dois postos e do CN, que é a parte menos confiável do mapa. Ressalvas: o mapa é relativo, depende dos K e C adotados de Vivarelli et al. (2025), considera a área urbana sem erosão e mostra onde a erosão é produzida, não onde chega ao rio.");
}

// ---------------------------------------------------------------- mapas grandes
{
  const s = base(SR, "Sedimento estimado em cada evento (MC)", "Fonte: elaborado pelo autor. Mesma escala de cores em todos os eventos; sedimento estimado c × E por pixel");
  img(s, "slides/mapa_17_eventos_MC.png", M, 1.5, 9.4, 5.35, "Sedimento estimado em cada pixel nos 17 eventos");
  marcadores(s, [
    "As mesmas manchas se repetem em todos os eventos",
    "A intensidade acompanha a chuva e o escoamento: eventos 8, 9, 15 e 16 os mais fortes",
    "Eventos de pouca chuva (1, 4, 6, 7, 10 e 12): erosão baixa em quase toda a bacia",
    "Cabeceira a leste: pouca erosão (menos chuva, CN baixo, mata)",
  ], 10.1, 1.8, 2.65, 5.0, 15);
  s.addNotes("Aqui está o sedimento estimado em cada pixel nos 17 eventos, com a mesma escala de cores. As manchas de maior erosão se repetem de um evento para outro; o que muda é a intensidade, que acompanha a chuva e o escoamento: os eventos 8, 9, 15 e 16, os de maior chuva, são os mais fortes. Nos eventos de pouca chuva, a erosão é baixa em quase toda a bacia. A cabeceira, a leste, produz pouco em todos os eventos, porque recebe menos chuva, tem número de curva mais baixo e é coberta sobretudo por mata. Lembrando: a intensidade de cada mapa depende do escoamento calculado, que erra 46% na mediana.");
}
{
  const s = base(SR, "Sedimento médio dos 17 eventos (MC)", "Fonte: elaborado pelo autor. Média, em cada pixel, do sedimento estimado nos 17 eventos (kg por pixel de 897 m²)");
  img(s, "slides/mapa_medio_MC.png", M, 1.5, W - 2 * M, 5.35, "Sedimento médio dos 17 eventos em cada pixel");
  s.addNotes("A média dos 17 eventos em cada pixel. As manchas mais escuras, na porção central e oeste, são campo, silvicultura e lavoura temporária sobre Cambissolos, em encostas íngremes; as manchas isoladas mais fortes são solo exposto e mineração, que têm C = 1 adotado. O mapa é relativo: depende dos K e C adotados e mostra onde a erosão é produzida, não onde o sedimento chega ao rio.");
}

// ---------------------------------------------------------------- conclusoes
pres.addSection({ title: SC });
{
  const s = base(SC, "Conclusões", null);
  marcadores(s, [
    "A conversão da chuva em escoamento é o principal limite: com a chuva, o MC erra 81%; com o volume medido, 21%",
    "Com o volume medido, a MUSLE espacializada não se distinguiu da regra com o volume: o trabalho não isola a contribuição da fórmula de erosão",
    "A espacialização chega a um erro da mesma ordem do modelo concentrado (22%) e acrescenta o mapa",
    "Áreas críticas: campo, silvicultura e lavoura temporária sobre Cambissolos, em encostas acima de 20% (46% da área, 83% da erosão)",
  ], M, 1.75, 5.6, 5.0, 17);
  img(s, "slides/mapa_criticas_MC.png", 6.45, 1.6, 6.3, 4.6, "Áreas críticas de erosão: 5% dos pixels de maior erosão média");
  s.addText("Áreas críticas: 5% dos pixels de maior erosão média (MC); 94% coincidem com o MFM", { x: 6.45, y: 6.25, w: 6.3, h: 0.5, fontSize: 14, italic: true, color: MUTED, margin: 0, isTextBox: true, align: "center" });
  s.addNotes("Primeiro: o que mais limita a estimativa da carga a partir da chuva é a conversão da chuva em escoamento; trocando pelo volume medido, o erro cai de 81% para 21%. Segundo: com o volume medido, a MUSLE espacializada não se distinguiu de uma regra simples com o volume; então o trabalho mostra o peso do escoamento, mas não isola a contribuição da fórmula e dos fatores. Terceiro: a espacialização chega a um erro da mesma ordem do modelo concentrado e acrescenta o mapa. Quarto: as áreas críticas, à direita, ficam no campo, na silvicultura e na lavoura temporária sobre Cambissolos, nas encostas mais íngremes: 46% da área respondem por 83% da erosão.");
}

// ---------------------------------------------------------------- limitacoes 1: origem do erro
{
  const s = base(SC, "Limitações: de onde vem o erro", "Fonte: elaborado pelo autor");
  stat(s, "81% → 21%", "erro mediano com o escoamento calculado e com o medido: cerca de 3/4 do erro vem da hidrologia", M, 1.6, 5.2, ORANGE);
  stat(s, "91%", "da variação do erro do sedimento é explicada pelo erro do escoamento", 6.6, 1.6, 6.1);
  const itens = [
    ["Chuva de 2 postos", "um deles fora da bacia; a chuva vira um gradiente suave e núcleos de chuva entre os postos não aparecem"],
    ["Delimitação manual dos eventos", "no evento 11, 12 a 14 mm em cada posto (cerca de 16% da chuva do evento) caíram nas 9 h antes do início da janela e ficaram fora do cálculo"],
    ["Forma do SCS-CN", "a fração da chuva que escoa não cresceu com a chuva (r = −0,01); CN-I e λ ajustam o total (+3%), mas não o erro de cada evento"],
    ["Vazão de base estimada", "o escoamento direto \"medido\" depende do filtro (BFImax = 0,70) e também é incerto"],
  ];
  itens.forEach((it, i) => {
    const y = 3.2 + i * 0.9;
    s.addText(String(i + 1), { shape: pres.shapes.OVAL, x: M, y: y + 0.05, w: 0.5, h: 0.5, fill: { color: NAVY }, color: WHITE, fontSize: 16, bold: true, align: "center", valign: "middle", margin: 0 });
    s.addText([{ text: it[0] + ": ", options: { bold: true, color: NAVY } }, { text: it[1], options: { color: TEXT } }], { x: M + 0.7, y, w: W - 2 * M - 0.7, h: 0.8, fontSize: 16, margin: 0, isTextBox: true, valign: "middle" });
  });
  s.addNotes("A maior parte do erro está na hidrologia, não na fórmula de erosão. Com o escoamento calculado, o erro mediano é 81%; com o medido, 21%: cerca de três quartos do erro vêm de transformar a chuva em escoamento, e o erro do escoamento explica 91% da variação do erro do sedimento. As causas, em ordem de importância provável: primeiro, a chuva de só dois postos, um fora da bacia, que vira um gradiente suave. Segundo, a delimitação manual dos eventos: no evento 11, por exemplo, choveram cerca de 12 a 14 mm em cada posto nas 9 horas antes do início da janela, e essa chuva ficou fora do cálculo, embora tenha molhado o solo. Terceiro, a forma do SCS-CN: nesta bacia, a fração da chuva que escoa não cresceu com a chuva, ao contrário do que o método supõe; a escolha de CN-I e lambda ajusta o volume total, mas não corrige o erro de cada evento. Quarto, a separação da vazão de base, que torna incerto até o escoamento direto medido. Resolver essas quatro é o que mais melhoraria o resultado.");
}

// ---------------------------------------------------------------- limitacoes 2: validacao e mapa
{
  const s = base(SC, "Limitações: o que falta validar", "Fonte: elaborado pelo autor");
  const cards = [
    ["Mapa sem validação espacial", "Só há medição de sedimento no exutório; não dá para testar se a erosão está onde o mapa aponta"],
    ["K e C adotados", "Valores por classe de Vivarelli et al. (2025), sem recalibração; área urbana com erosão nula"],
    ["c único", "Sem conectividade: o mapa mostra onde a erosão é produzida, não onde o sedimento chega ao rio"],
    ["Medição do sedimento", "Curva turbidez × CSS sem incerteza estimada; parte da carga pode vir do canal (pico de CSS antes da vazão)"],
    ["Poucos eventos", "17 eventos: diferenças de poucos pontos não são interpretáveis; conclusões qualitativas"],
  ];
  const cw = 3.85, ch = 2.45;
  cards.forEach((c, i) => {
    const x = M + (i % 3) * (cw + 0.275), y = 1.65 + Math.floor(i / 3) * (ch + 0.2);
    s.addText([{ text: c[0], options: { bold: true, color: NAVY, fontSize: 17, breakLine: true } }, { text: c[1], options: { color: TEXT, fontSize: 16 } }],
      { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.06, x, y, w: cw, h: ch, fill: { color: TINT }, line: { color: LINE, width: 1 }, valign: "top", margin: 10 });
  });
  s.addText([{ text: "Próximos passos", options: { bold: true, color: ORANGE, fontSize: 17, breakLine: true } },
    { text: "Medir sedimento em sub-bacias e verificar as áreas críticas em campo; mais postos ou radar; índice de conectividade por pixel; novos eventos como teste independente", options: { color: TEXT, fontSize: 16 } }],
    { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.06, x: M + 2 * (cw + 0.275), y: 1.65 + ch + 0.2, w: cw, h: ch, fill: { color: "FCEFD9" }, line: { color: "E8C79A", width: 1 }, valign: "top", margin: 10 });
  s.addNotes("Outras limitações não explicam tanto o erro, mas impedem validar o resultado, principalmente o mapa. Não há medição de sedimento dentro da bacia, então o mapa não pode ser validado no espaço. K e C foram adotados de Vivarelli et al. (2025), sem recalibração, e a área urbana tem erosão nula por hipótese. O coeficiente c é único, sem conectividade, então o mapa mostra onde a erosão acontece, não onde o sedimento chega ao rio. A carga medida depende da curva entre turbidez e concentração, cuja incerteza não foi estimada, e o pico de concentração antes da vazão sugere fontes perto do canal, que o modelo não representa. E, com 17 eventos, as conclusões são qualitativas. Os próximos passos atacam essas lacunas: medir sedimento em sub-bacias, mais postos ou radar, conectividade por pixel e novos eventos.");
}

// ---------------------------------------------------------------- 27 agradecimentos
pres.addSection({ title: SE });
{
  const s = base(SE, "Agradecimentos", null);
  const pessoas = [
    ["Me. Luis Fernando Murillo-Bermúdez", "orientação e dados de monitoramento"],
    ["Prof. Dr. André Luís Sotero Salustiano Martim", "coorientação"],
    ["Dr. Hugo de Oliveira Fagundes e Me. Gustavo Ribeiro da Silva", "banca"],
    ["CNPq / PIBIC", "bolsa de iniciação científica"],
    ["Família, Larissa e amigos", "apoio durante a graduação"],
  ];
  linhas(s, pessoas.map(p => [p[0], "— " + p[1]]), M, 1.9, 8.5, 4.6, 20);
  s.addText("Obrigado!", { x: 9.3, y: 2.6, w: 3.45, h: 1.2, fontSize: 44, bold: true, color: NAVY, margin: 0, isTextBox: true, align: "right" });
  s.addText("[e-mail de contato]", { x: 9.3, y: 3.8, w: 3.45, h: 0.5, fontSize: 16, color: MUTED, margin: 0, isTextBox: true, align: "right" });
  s.addNotes("Agradecer ao Luis, pela orientação e pelos dados; ao professor André, pela coorientação desde a iniciação científica; à banca; ao CNPq e ao PIBIC pela bolsa; e à família, à Larissa e aos amigos. (30 segundos.)");
}

// ---------------------------------------------------------------- 28 uso de IA
{
  const s = base(SE, "Uso de inteligência artificial", null);
  s.addText("[Opcional: confirme se o texto corresponde ao que você fez e ao que a FECFAU pede]", { x: M, y: 1.75, w: 12.1, h: 0.4, fontSize: 14, italic: true, color: ORANGE, margin: 0, isTextBox: true });
  const usos = [["Programação", "apoio na escrita e revisão das rotinas em Python"], ["Texto", "revisão de redação e da formatação"], ["Figuras", "apoio na preparação de gráficos e mapas"]];
  usos.forEach((u, i) => {
    const x = M + i * 4.1;
    s.addText([{ text: u[0], options: { bold: true, fontSize: 20, color: NAVY, breakLine: true } }, { text: u[1], options: { fontSize: 15, color: TEXT } }],
      { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.06, x, y: 2.45, w: 3.85, h: 1.7, fill: { color: TINT }, line: { color: LINE, width: 1 }, align: "center", valign: "middle", margin: 0.12 });
  });
  s.addText("As escolhas de método, os cálculos e os resultados foram conferidos pelo autor e discutidos com o orientador.", { x: M, y: 4.6, w: 12.1, h: 0.9, fontSize: 19, color: NAVY, margin: 0, isTextBox: true, valign: "top" });
  s.addNotes("Opcional. Se não couber, falar em uma frase depois dos agradecimentos, ou deixar o slide oculto. Ajuste os itens ao que realmente foi feito.");
}

// ---------------------------------------------------------------- apoio: histerese
pres.addSection({ title: SA });
{
  const s = base(SA, "Apoio: a concentração chega antes da vazão", "Fonte: elaborado pelo autor, com os dados de Murillo-Bermúdez e Martim (2022). Correlações com 17 eventos: valores de p apenas indicativos");
  img(s, "slides/ev11_hidrograma.png", M, 1.65, 6.6, 3.6, "Hidrograma e concentração de sedimentos no evento 11");
  s.addText("Evento 11", { x: M, y: 5.35, w: 6.6, h: 0.4, fontSize: 16, bold: true, color: NAVY, margin: 0, isTextBox: true });
  marcadores(s, [
    "Pico de CSS cerca de 25 h antes do pico de vazão (laço horário)",
    "68% da carga passa até o pico de vazão; cerca de 72% está na parcela do escoamento direto",
  ], M, 5.75, 6.6, 1.1, 15);
  s.addText("Nos 17 eventos", { x: 7.5, y: 1.7, w: 5.25, h: 0.45, fontSize: 18, bold: true, color: NAVY, margin: 0, isTextBox: true });
  stat(s, "88%", "da variação da carga (log) explicada pelo volume escoado", 7.5, 2.15, 2.5, ORANGE);
  stat(s, "0%", "explicada só pela intensidade máxima da chuva", 10.25, 2.15, 2.5);
  marcadores(s, [
    "13 de 17 eventos com laço horário (planilha de eventos)",
    "A intensidade da chuva aparece na concentração média (Spearman 0,49; p = 0,04)",
    "O modelo trabalha com o total do evento; a dinâmica dentro do evento e as fontes perto do canal não são representadas",
  ], 7.5, 3.75, 5.25, 3.1, 15);
  s.addNotes("Se perguntarem sobre a histerese: o pico de concentração vem antes do pico de vazão, um laço horário, típico de sedimento disponível perto do canal que se esgota durante o evento. O modelo não representa essa dinâmica dentro do evento, nem as fontes do canal. Mas, no total do evento, o volume escoado explica 88% da variação da carga, e a intensidade da chuva aparece mais na concentração, o que o modelo considera em parte pelo pico local (RI/R). No evento 11, 68% da carga passa até o pico de vazão e cerca de 72% está na parcela do escoamento direto (supondo a mesma concentração na vazão de base). Com 17 eventos e vários testes, os valores de p são só indícios.");
}

// ---------------------------------------------------------------- 24 leitura critica
{
  const s = base(SA, "Apoio: o peso do volume medido", "Fonte: elaborado pelo autor, com os dados da Tabela 3 do TCC");
  img(s, "slides/fig_volume_concentracao.png", M, 1.6, 8.6, 3.9, "Descarga de sedimentos contra o volume escoado e variação de volume e concentração entre eventos");
  stat(s, "88%", "da variância do log da carga é explicada só pelo volume", 9.45, 1.75, 3.3, ORANGE);
  stat(s, "0,66 × 0,08", "variância do log: volume × concentração", 9.45, 3.25, 3.3);
  s.addText("Carga = volume × concentração média. Quem recebe o volume medido acerta a ordem de grandeza da carga por construção. O bom desempenho do MFM não valida a fórmula de erosão nem o mapa.", { x: M, y: 5.65, w: 12.1, h: 1.2, fontSize: 17, color: NAVY, margin: 0, isTextBox: true, valign: "top" });
  s.addNotes("Por que o MFM vai tão bem? A carga de um evento é o volume escoado vezes uma concentração média. Entre os 17 eventos, o volume varia muito mais que a concentração: a variância do log do volume é 0,66, contra 0,08 da concentração, e só o volume explica 88% da variância da carga. Então qualquer modelo que receba o volume medido acerta a ordem de grandeza. A conclusão honesta é: o trabalho mostra o peso do escoamento, mas não consegue avaliar separadamente a fórmula de erosão e os fatores K, LS e C. O evento 17 é o mais difícil para todos os modelos com volume medido, com concentração bem acima dos outros; foi mantido porque não há base para excluí-lo.");
}

// ---------------------------------------------------------------- apoio: RI/R
{
  const s = base(SA, "Apoio: o índice RI/R e os eventos 1 e 12", "Fonte: elaborado pelo autor. RI = maior chuva em 1 h no posto mais intenso; R = chuva total ponderada dos dois postos");
  const H = (t) => ({ text: t, options: { bold: true, color: WHITE, fill: { color: NAVY } } });
  s.addTable([
    [H("Evento"), H("DBT5: total; maior hora"), H("Campo Limpo: total; maior hora"), H("R ponderado"), H("RI"), H("RI/R")],
    ["1", "32,8 mm; 23,6 mm/h", "19,2 mm; 16,2 mm/h", "23,4 mm", "23,6 mm/h", "1,01"],
    ["12", "0 (sem registro)", "34,2 mm; 32,8 mm/h", "23,7 mm", "32,8 mm/h", "1,38"],
    ["11", "62,8 mm; 11,8 mm/h", "79,0 mm; 9,4 mm/h", "74,0 mm", "11,8 mm/h", "0,16"],
  ], { x: M, y: 1.85, w: 12.1, colW: [1.1, 2.9, 3.1, 1.8, 1.7, 1.5], fontSize: 16, fontFace: "Calibri", color: TEXT, border: { type: "solid", pt: 0.75, color: LINE }, rowH: 0.55, valign: "middle", align: "center" });
  marcadores(s, [
    "RI/R mede quanto da chuva do evento caiu na hora mais intensa; é único por evento, igual em todos os pixels",
    "Acima de 1 não é físico: RI vem do posto mais intenso e R é a média dos dois; a chuva forte pegou praticamente um só posto",
    "No mesmo posto: 0,72 (evento 1) e 0,96 (evento 12), chuvas curtas e muito concentradas",
    "Efeito: pico local cerca de 1,4 vez maior e índice E cerca de 20% maior nesses dois eventos pequenos",
  ], M, 4.35, 12.1, 2.5, 16);
  s.addNotes("RI/R acima de 1 não é físico: aparece porque a intensidade vem do posto mais chuvoso e a lâmina é a média ponderada dos dois. Nos eventos 1 e 12, um temporal curto pegou praticamente um só posto. Calculado num mesmo posto, daria 0,72 e 0,96. Por isso o TCC trata RI/R como índice de concentração temporal da chuva, e não como fração. Uma forma mais consistente seria calcular RI e R no mesmo posto ou ponderar também a intensidade.");
}

// ---------------------------------------------------------------- apoio: CN-I e Woodward
{
  const s = base(SA, "Apoio: do CN tabelado à retenção usada", "Fontes: Agência Nacional de Águas e Saneamento Básico (2024); Chow, Maidment e Mays (1988); Woodward et al. (2003)");
  const y = 1.95, h = 1.3, bw = 2.6, gap = 0.5;
  const etapas = [["CN-II", "raster BR_CN-2022 (Agência\nNacional de Águas, 2024)"], ["CN-I", "condição seca\nChow et al. (1988)"], ["S_{0,20}", "25,4 (1000/CN − 10)"], ["S_{0,05}", "1,33 S_{0,20}^{1,15} (pol.)\nWoodward et al. (2003)"]];
  etapas.forEach((e, i) => {
    const x = M + i * (bw + gap);
    s.addText(rt(e[0], { bold: true, fontSize: 20, color: NAVY }).concat([{ text: "", options: { breakLine: true } }], rt(e[1], { fontSize: 13, color: MUTED })),
      { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.06, x, y, w: bw, h, fill: { color: TINT }, line: { color: LINE, width: 1 }, align: "center", valign: "middle", margin: 0.05 });
    if (i < etapas.length - 1) seta(s, x + bw + 0.08, y + h / 2 - 0.16, gap - 0.16);
  });
  marcadores(s, [
    "Woodward et al. (2003) convertem só a razão de abstração inicial (de 0,20 para 0,05); a umidade antecedente vem de Chow et al. (1988)",
    "A combinação das duas conversões é escolha deste trabalho: aproxima o volume total dos 17 eventos (+3%)",
    "Aplicada ao CN-I, a conversão de Woodward é extrapolada em 8,4% dos pixels (CN-I abaixo de 35)",
  ], M, 3.7, 12.1, 3.0, 17);
  s.addNotes("Se perguntarem: Woodward converte só o lambda; o CN-I vem da fórmula de Chow, Maidment e Mays (1988). A combinação foi escolhida porque aproxima o volume total dos 17 eventos, e foi feita olhando os mesmos eventos. Como é aplicada a retenções grandes (CN da condição seca), a conversão de Woodward é extrapolada em 8,4% dos pixels.");
}

pres.writeFile({ fileName: path.join(OUTDIR, "slides_defesa_completo.pptx") }).then(f => { require("child_process").execSync(`zip -dq "${f}" "*/" || true`); console.log("ok", f); });
