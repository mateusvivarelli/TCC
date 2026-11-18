"""Copia do deck so com os slides 17 em diante (numeracao da apresentacao do autor).
O slide 1 do deck gerado e o slide 11 da apresentacao; remove os 6 primeiros (11 a 16)."""
import os
from pptx import Presentation

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(BASE, "TCC_Texto", "slides", "slides_11a28_defesa.pptx")
DST = os.path.join(BASE, "TCC_Texto", "slides", "slides_17a28_defesa.pptx")
N_REMOVER = 6

p = Presentation(SRC)
lst = p.slides._sldIdLst
ids = list(lst)[:N_REMOVER]
P14 = "{http://schemas.microsoft.com/office/powerpoint/2010/main}"
removidos = set()
for sid in ids:
    removidos.add(sid.get("id"))
    p.part.drop_rel(sid.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"))
    lst.remove(sid)
# secoes: tira os slides removidos e as secoes que ficaram vazias
for sec in p.part._element.iter(P14 + "section"):
    sl = sec.find(P14 + "sldIdLst")
    for e in list(sl):
        if e.get("id") in removidos:
            sl.remove(e)
    if len(sl) == 0:
        sec.getparent().remove(sec)
p.save(DST)
print("ok", DST, len(p.slides), "slides")
