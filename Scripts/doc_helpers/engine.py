# -*- coding: utf-8 -*-
import json, re, sys
from dochelp import load, paras

c, tab = load("cur.json")
P = paras(tab)

def find(prefix):
    m = [p for p in P if not p["tbl"] and p["t"].startswith(prefix)]
    assert len(m) == 1, (prefix, len(m))
    return m[0]

# ---------------------------------------------------------------- markup
TOK = re.compile(r"(\*\*.+?\*\*|\*[^*]+?\*|_\{.+?\}|\^\{.+?\}|==.+?==)")
def parse(mk):
    plain = ""; spans = []
    for part in TOK.split(mk):
        if not part: continue
        kind = None; inner = part
        if part.startswith("**") and part.endswith("**") and len(part) > 4: kind, inner = "bold", part[2:-2]
        elif part.startswith("*") and part.endswith("*") and len(part) > 2 and not part.startswith("**"): kind, inner = "italic", part[1:-1]
        elif part.startswith("_{") and part.endswith("}"): kind, inner = "sub", part[2:-1]
        elif part.startswith("^{") and part.endswith("}"): kind, inner = "sup", part[2:-1]
        elif part.startswith("==") and part.endswith("==") and len(part) > 4: kind, inner = "hl", part[2:-2]
        if kind: spans.append((len(plain), len(plain) + len(inner), kind))
        plain += inner
    return plain, spans

STY = {"bold": ({"bold": True}, "bold"), "italic": ({"italic": True}, "italic"),
       "sub": ({"baselineOffset": "SUBSCRIPT"}, "baselineOffset"), "sup": ({"baselineOffset": "SUPERSCRIPT"}, "baselineOffset"),
       "hl": ({"backgroundColor": {"color": {"rgbColor": {"red": 1.0, "green": 1.0, "blue": 0.0}}}}, "backgroundColor")}
RESET = "bold,italic,baselineOffset,backgroundColor,fontSize"

def rng(a, b): return {"startIndex": a, "endIndex": b}
def ins(i, t): return {"insertText": {"text": t, "location": {"index": i}}}
def delr(a, b): return {"deleteContentRange": {"range": rng(a, b)}}
def tstyle(a, b, st, fields): return {"updateTextStyle": {"range": rng(a, b), "textStyle": st, "fields": fields}}
def pstyle(a, b, st, fields): return {"updateParagraphStyle": {"range": rng(a, b), "paragraphStyle": st, "fields": fields}}

def span_reqs(base, spans):
    out = []
    for a, b, k in spans:
        st, f = STY[k]; out.append(tstyle(base + a, base + b, st, f))
    return out

PT = lambda x: {"magnitude": x, "unit": "PT"}
PRE = {
 "body": ({"namedStyleType": "NORMAL_TEXT", "alignment": "JUSTIFIED", "indentFirstLine": PT(56.7), "lineSpacing": 150, "spaceAbove": PT(0)},
          "namedStyleType,alignment,indentFirstLine,lineSpacing,spaceAbove", None),
 "body0": ({"namedStyleType": "NORMAL_TEXT", "alignment": "JUSTIFIED", "indentFirstLine": PT(0), "lineSpacing": 150, "spaceAbove": PT(0)},
          "namedStyleType,alignment,indentFirstLine,lineSpacing,spaceAbove", None),
 "center": ({"namedStyleType": "NORMAL_TEXT", "alignment": "CENTER", "indentFirstLine": PT(0), "lineSpacing": 150, "spaceAbove": PT(0)},
          "namedStyleType,alignment,indentFirstLine,lineSpacing,spaceAbove", None),
 "h1": ({"namedStyleType": "HEADING_1", "alignment": "START", "indentFirstLine": PT(0), "indentStart": PT(0), "pageBreakBefore": False}, "namedStyleType,alignment,indentFirstLine,indentStart,pageBreakBefore", None),
 "h1pb": ({"namedStyleType": "HEADING_1", "alignment": "START", "indentFirstLine": PT(0), "indentStart": PT(0), "pageBreakBefore": True}, "namedStyleType,alignment,indentFirstLine,indentStart,pageBreakBefore", None),
 "h2": ({"namedStyleType": "HEADING_2", "alignment": "START", "indentFirstLine": PT(0), "indentStart": PT(0), "lineSpacing": 150, "spaceAbove": PT(12), "pageBreakBefore": False}, "namedStyleType,alignment,indentFirstLine,indentStart,lineSpacing,spaceAbove,pageBreakBefore", {"bold": True, "fontSize": PT(12)}),
 "h3": ({"namedStyleType": "HEADING_3", "alignment": "JUSTIFIED", "indentFirstLine": PT(0), "indentStart": PT(0), "lineSpacing": 150, "pageBreakBefore": False}, "namedStyleType,alignment,indentFirstLine,indentStart,lineSpacing,pageBreakBefore", None),
 "cap": ({"namedStyleType": "NORMAL_TEXT", "alignment": "START", "indentFirstLine": PT(0), "indentStart": PT(0), "lineSpacing": 100, "spacingMode": "NEVER_COLLAPSE", "spaceAbove": PT(8), "spaceBelow": PT(4), "keepWithNext": True, "pageBreakBefore": False},
         "namedStyleType,alignment,indentFirstLine,indentStart,lineSpacing,spacingMode,spaceAbove,spaceBelow,keepWithNext,pageBreakBefore", {"fontSize": PT(10)}),
}
PRE["keep"] = ({}, "", None)
PRE["centerpb"] = ({**PRE["center"][0], "pageBreakBefore": True}, PRE["center"][1] + ",pageBreakBefore", None)

def text_block(s0, kind, mk):
    plain, spans = parse(mk); L = len(plain) + 1
    st, fields, extra = PRE[kind]
    r = [ins(s0, plain + "\n"), pstyle(s0, s0 + L, st, fields)]
    if L > 1:
        r.append(tstyle(s0, s0 + L - 1, {}, RESET))
        if extra: r.append(tstyle(s0, s0 + L - 1, extra, ",".join(extra.keys())))
        r += span_reqs(s0, spans)
    return r, L

HEADBG = {"color": {"rgbColor": {"red": 0.8509804, "green": 0.8862745, "blue": 0.9529412}}}
def table_unit(s0, spec):
    reqs, Lc = text_block(s0, "cap", spec["cap"])
    # prefixo "Tabela N." em negrito
    mm = re.match(r"\*\*(.+?)\*\*", spec["cap"])
    rows = [spec["header"]] + spec["rows"]; R = len(rows); C = len(spec["header"])
    q = s0 + Lc - 1; T = s0 + Lc
    reqs.append({"insertTable": {"rows": R, "columns": C, "location": {"index": q}}})
    p0 = lambda r, cc: T + 3 + r * (1 + 2 * C) + 2 * cc
    order = [(r, cc) for r in range(R) for cc in range(C)]
    for (r, cc) in reversed(order):
        t = rows[r][cc]
        if t: reqs.append(ins(p0(r, cc), t))
    cum = 0; fin = {}
    for (r, cc) in order:
        fin[(r, cc)] = p0(r, cc) + cum; cum += len(rows[r][cc])
    al = spec.get("align", ["START"] + ["CENTER"] * (C - 1))
    A = fin[(0, 0)]; Z = fin[(R - 1, C - 1)] + max(len(rows[R - 1][C - 1]), 1)
    reqs.append(pstyle(A, Z, {"alignment": "CENTER", "lineSpacing": 100, "spaceAbove": PT(1), "spaceBelow": PT(1), "spacingMode": "NEVER_COLLAPSE", "indentFirstLine": PT(0), "indentStart": PT(0)}, "alignment,lineSpacing,spaceAbove,spaceBelow,spacingMode,indentFirstLine,indentStart"))
    for cc in range(C):
        if al[cc] == "START":
            for r in range(1, R):
                a_ = fin[(r, cc)]; reqs.append(pstyle(a_, a_ + max(len(rows[r][cc]), 1), {"alignment": "START"}, "alignment"))
    reqs.append(tstyle(A, Z, {"fontSize": PT(10)}, "fontSize"))
    reqs.append(tstyle(A, fin[(0, C - 1)] + len(rows[0][C - 1]), {"bold": True}, "bold"))
    reqs.append({"updateTableCellStyle": {"tableRange": {"tableCellLocation": {"tableStartLocation": {"index": T}, "rowIndex": 0, "columnIndex": 0}, "rowSpan": 1, "columnSpan": C}, "tableCellStyle": {"backgroundColor": HEADBG}, "fields": "backgroundColor"}})
    if "widths" in spec:
        for i, w in enumerate(spec["widths"]):
            reqs.append({"updateTableColumnProperties": {"tableStartLocation": {"index": T}, "columnIndices": [i], "tableColumnProperties": {"widthType": "FIXED_WIDTH", "width": PT(w)}, "fields": "width,widthType"}})
    return reqs

OPS = []   # (sortindex, seq, [requests])
def add(s, reqs): OPS.append((s, len(OPS), reqs))

def replace_para(prefix, mk, kind=None):
    p = find(prefix); s = p["s"]; e = p["e"] - 1
    plain, spans = parse(mk)
    r = [delr(s, e), ins(s, plain), tstyle(s, s + len(plain), {}, RESET)] + span_reqs(s, spans)
    add(s, r)

def insert_before(prefix, blocks, at=None):
    p = find(prefix) if at is None else None
    s0 = p["s"] if at is None else at
    reqs = []
    for b in reversed(blocks):
        kind = b[0]
        if kind == "table": reqs += table_unit(s0, b[1])
        else: reqs += text_block(s0, kind, b[1])[0]
    add(s0, reqs)

def append_to_para(prefix, blocks):
    """insere novos paragrafos DEPOIS do paragrafo (herdam o estilo; estilo explicito aplicado)"""
    p = find(prefix); e = p["e"] - 1
    reqs = []
    # inserir tudo depois da quebra: no inicio do proximo paragrafo nao e seguro; usa fim do paragrafo
    pos = e
    full = ""; spec = []
    for kind, mk in blocks:
        plain, spans = parse(mk); spec.append((kind, plain, spans)); full += "\n" + plain
    reqs.append(ins(pos, full))
    cur = pos
    for kind, plain, spans in spec:
        a = cur + 1; b = a + len(plain)
        st, fields, extra = PRE[kind]
        if fields: reqs.append(pstyle(a, b + 1, st, fields))
        if b > a: reqs.append(tstyle(a, b, {}, RESET))
        reqs += span_reqs(a, spans); cur = b
    add(pos, reqs)

def delete_range(a, b): add(a, [delr(a, b)])

def out_batches(maxchars=14000):
    ops = sorted(OPS, key=lambda o: (-o[0], o[1]))
    flat = []
    for s, _, r in ops: flat.append(r)
    batches = []; cur = []; n = 0
    for r in flat:
        sz = len(json.dumps(r, ensure_ascii=False))
        if cur and n + sz > maxchars: batches.append(cur); cur = []; n = 0
        cur += r; n += sz
    if cur: batches.append(cur)
    return batches
