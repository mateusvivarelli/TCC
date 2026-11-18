"""Gera, a partir do deck completo, o arquivo so com os slides novos para o autor colar:
o slide 8 (solo e uso) e os slides do resultado do MC (20 na apresentacao) em diante."""
import os
from pptx import Presentation

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(BASE, "TCC_Texto", "slides", "slides_defesa_completo.pptx")
DST = os.path.join(BASE, "TCC_Texto", "slides", "slides_novos_8_e_20_em_diante.pptx")
MANTER_PRIMEIRO = 1          # slide 8
INICIO_RESULTADOS = 11       # posicao, no deck completo, do slide "Modelo calculado: pior que a regra simples"

p = Presentation(SRC)
lst = p.slides._sldIdLst
todos = list(lst)
remover = todos[MANTER_PRIMEIRO:INICIO_RESULTADOS - 1]
P14 = "{http://schemas.microsoft.com/office/powerpoint/2010/main}"
RID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
ids = set()
for sid in remover:
    ids.add(sid.get("id")); p.part.drop_rel(sid.get(RID)); lst.remove(sid)
for sec in list(p.part._element.iter(P14 + "section")):
    sl = sec.find(P14 + "sldIdLst")
    for e in list(sl):
        if e.get("id") in ids:
            sl.remove(e)
    if len(sl) == 0:
        sec.getparent().remove(sec)
p.save(DST)
print("ok", DST, len(p.slides), "slides")
