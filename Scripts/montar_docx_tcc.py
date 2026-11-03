import zipfile, re, io, copy, sys
from lxml import etree
from PIL import Image
SP = r"C:\Users\user\AppData\Local\Temp\claude\C--TCC\6f697bf5-4a56-4dbc-a537-266e661ffede\scratchpad"
SRC = SP + chr(92) + 'tcc_base.docx'
FIG = r'C:/TCC/TCC_Texto/figuras/mapas/'
OUT = r'C:/TCC/TCC_Texto/TCC_versao_03-11.docx'

# ---- 0. sanear numeros decimais em atributos w: (o export do Google grava twips fracionarios)
zin = zipfile.ZipFile(SRC)
buf = io.BytesIO()
zout = zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED)
pat = re.compile(r'(\sw:[A-Za-z]+=")(-?\d+)\.\d+(")')
for it in zin.infolist():
    data = zin.read(it.filename)
    if it.filename.startswith('word/') and it.filename.endswith('.xml'):
        s = data.decode('utf-8')
        s2 = pat.sub(lambda m: m.group(1) + str(int(round(float(m.group(2) + '.' + m.group(0).split('.')[1].rstrip('"'))))) + m.group(3), s)
        data = s2.encode('utf-8')
    zout.writestr(it, data)
zout.close(); buf.seek(0)
import docx
from docx.shared import Cm
from docx.oxml.ns import qn
d = docx.Document(buf)

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
NS = 'xmlns:w="%s" xmlns:m="%s"' % (W, M)

# ---- 1. construtor de equacoes (OMML)
def esc(t): return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
def r(t, up=False):
    rp = '<m:rPr><m:sty m:val="p"/></m:rPr>' if up else ''
    return '<m:r>%s<m:t xml:space="preserve">%s</m:t></m:r>' % (rp, esc(t))
def up(t): return r(t, True)
def sub(b, s): return '<m:sSub><m:e>%s</m:e><m:sub>%s</m:sub></m:sSub>' % (b, s)
def sup(b, s): return '<m:sSup><m:e>%s</m:e><m:sup>%s</m:sup></m:sSup>' % (b, s)
def subsup(b, s, p): return '<m:sSubSup><m:e>%s</m:e><m:sub>%s</m:sub><m:sup>%s</m:sup></m:sSubSup>' % (b, s, p)
def frac(n, dn): return '<m:f><m:num>%s</m:num><m:den>%s</m:den></m:f>' % (n, dn)
def par(x, b='(', e=')'): return '<m:d><m:dPr><m:begChr m:val="%s"/><m:endChr m:val="%s"/></m:dPr><m:e>%s</m:e></m:d>' % (b, e, x)
def brk(x): return par(x, '[', ']')
def absv(x): return par(x, '|', '|')
def nsum(lim, body): return '<m:nary><m:naryPr><m:chr m:val="\u2211"/><m:limLoc m:val="undOvr"/><m:supHide m:val="1"/></m:naryPr><m:sub>%s</m:sub><m:sup></m:sup><m:e>%s</m:e></m:nary>' % (lim, body)
def lim(base, l): return '<m:limLow><m:e>%s</m:e><m:lim>%s</m:lim></m:limLow>' % (base, l)
def cat(*a): return ''.join(a)

Ek = sub(r('E'), up('unit,k'))
Ekn = sub(r('E'), up('unit,k,n'))
SYo = sub(up('SY'), up('obs,n'))
pr = sub(r('p'), up('r,k'))
Apix = sub(r('A'), up('pix'))
dk1 = subsup(r('d'), r('1,k'), r('2')); dk2 = subsup(r('d'), r('2,k'), r('2'))
S005 = sub(r('S'), r('0,05,k')); S020 = sub(r('S'), r('0,20,k'))
EQ = {}
EQ[461] = cat(sub(up('CN-I'), r('k')), r(' = 4,2 * '), frac(sub(up('CN-II'), r('k')), cat(r('10 - 0,058 * '), sub(up('CN-II'), r('k')))))
EQ[463] = cat(S020, r(' = 25,4 * '), par(cat(frac(r('1000'), sub(up('CN-I'), r('k'))), r(' - 10'))))
EQ[466] = cat(S005, r(' = 25,4 * 1,33 * '), sup(par(frac(S020, r('25,4'))), r('1,15')))
EQ[471] = cat(sub(r('P'), r('k')), r(' = '), frac(cat(sub(r('P'), r('1')), r(' * '), dk2, r(' + '), sub(r('P'), r('2')), r(' * '), dk1), cat(dk1, r(' + '), dk2)))
EQ[476] = cat(sub(r('Q'), r('k')), r(' = '), frac(sup(par(cat(sub(r('P'), r('k')), r(' - 0,05 * '), S005)), r('2')), cat(sub(r('P'), r('k')), r(' + 0,95 * '), S005)), up(',  se  '), sub(r('P'), r('k')), r(' > 0,05 * '), S005)
EQ[477] = cat(sub(r('Q'), r('k')), r(' = 0,  '), up('se  '), sub(r('P'), r('k')), r(' \u2264 0,05 * '), S005)
EQ[481] = cat(pr, r(' = '), frac(cat(par(frac(sub(r('Q'), r('k')), r('1000'))), r(' * '), Apix, r(' * '), par(frac(sub(r('R'), r('I')), r('R')))), r('3600')))
EQ[484] = cat(Ek, r(' = 11,8 * '), sup(par(cat(sub(r('Q'), r('k')), r(' * '), pr, r(' * '), Apix)), r('0,56')), r(' * '), sub(r('K'), r('k')), r(' * '), sub(r('C'), r('k')), r(' * '), sub(up('LS'), r('k')), r(' * P'))
EQ[489] = cat(sub(up('SY'), r('n')), r(' = c * '), nsum(r('k'), Ekn))
EQ[494] = cat(sub(r('Q'), up('MFM,k')), r(' = '), up('min'), par(cat(sub(r('f'), r('n')), r(' * '), sub(r('Q'), r('k')), r(', '), sub(r('P'), r('k')))))
inner500 = cat(up('ln'), par(SYo), r(' - '), up('ln'), par(cat(r('c * '), nsum(r('k'), Ekn))))
EQ[500] = cat(lim(up('min'), r('c')), nsum(r('n'), sup(brk(inner500), r('2'))))
EQ[502] = cat(up('ln'), r(' c = '), frac(r('1'), r('N')), r(' * '), nsum(r('n'), brk(cat(up('ln'), par(SYo), r(' - '), up('ln'), par(nsum(r('k'), Ekn))))))
EQ[521] = cat(sub(up('EPA'), r('n')), r(' = 100 * '), frac(absv(cat(sub(r('S'), r('n')), r(' - '), sub(r('O'), r('n')))), sub(r('O'), r('n'))))
EQ[522] = cat(up('MedAPE = mediana'), par(cat(sub(up('EPA'), r('1')), r(', ..., '), sub(up('EPA'), r('N')))))
EQ[525] = cat(r('F2 = '), frac(r('100'), r('N')), r(' * '), brk(cat(up('n\u00famero de eventos com  0,5 \u2264 '), frac(sub(r('S'), r('n')), sub(r('O'), r('n'))), r(' \u2264 2'))))
On = sub(r('O'), r('n')); Sn = sub(r('S'), r('n'))
num527 = nsum(r('n'), sup(brk(cat(up('ln'), par(On), r(' - '), up('ln'), par(Sn))), r('2')))
den527 = nsum(r('n'), sup(brk(cat(up('ln'), par(On), r(' - '), up('média'), par(cat(up('ln'), r(' O')))) ), r('2')))
EQ[527] = cat(sub(up('NSE'), up('log')), r(' = 1 - '), frac(num527, den527))
EQ[530] = cat(sub(r('r'), r('s')), r(' = 1 - '), frac(cat(r('6 * '), nsum(r('n'), subsup(r('d'), r('n'), r('2')))), cat(r('N * '), par(cat(sup(r('N'), r('2')), r(' - 1'))))))
EQ[533] = cat(up('Vi\u00e9s'), r(' = 100 * '), frac(cat(nsum(r('n'), sub(r('V'), up('SCS,n'))), r(' - '), nsum(r('n'), sub(r('V'), up('dir,n')))), nsum(r('n'), sub(r('V'), up('dir,n')))))
EQ[540] = cat(sub(r('Y'), r('n')), r(' = \u03b1 * '), sup(par(cat(sub(r('D'), r('n')), r(' * '), sub(r('q'), r('p,n')))), r('\u03b2')), r(' * K * '), up('LS'), r(' * C * P'))
G = sub(r('G'), r('k'))
EQ[548] = cat(sub(r('E'), up('med,k')), r(' = c * 11,8 * P * '), par(cat(sub(r('K'), r('k')), r(' * '), sub(up('LS'), r('k')), r(' * '), sub(r('C'), r('k')))), r(' * '), G, up(',  com  '), G, r(' = '), frac(r('1'), r('17')), r(' * '), nsum(r('n'), sup(par(cat(sub(r('Q'), r('k,n')), r(' * '), sub(r('p'), r('r,k,n')), r(' * '), Apix)), r('0,56'))))

P = d.paragraphs
# conferir que os indices ainda apontam para as linhas certas
chk = {461: 'CN-I_k', 463: 'S0,20,k', 466: 'S0,05,k', 471: 'P_k', 476: 'Q_k = (P_k', 477: 'Q_k = 0', 481: 'pr,k', 484: 'E_unit,k = 11,8', 489: 'SY_n', 494: 'Q_MFM', 500: 'min_c', 502: 'ln c', 521: 'EPA_n', 522: 'MedAPE', 525: 'F2', 527: 'NSE_log', 530: 'r_s', 533: 'Vi', 540: 'Y_n', 548: 'E_med'}
for i, k in chk.items():
    assert P[i].text.strip().startswith(k), (i, P[i].text[:40])
assert P[457].text.startswith('LS_k')
assert 'oMath' in P[456]._p.xml
for i, xml in EQ.items():
    p = P[i]._p
    for ch in list(p):
        if ch.tag != qn('w:pPr'): p.remove(ch)
    el = etree.fromstring('<m:oMathPara %s><m:oMath>%s</m:oMath></m:oMathPara>' % (NS, xml))
    p.append(el)
    ppr = p.find(qn('w:pPr'))
    if ppr is not None:
        for t in ('w:shd', 'w:ind'):
            for e in ppr.findall(qn(t)): ppr.remove(e)
# remover a linha de texto duplicada do LS (a equacao ja existe no paragrafo anterior)
dup = P[457]._p; dup.getparent().remove(dup)

# ---- 2. figuras
text_w = 16.0
def put_picture(par, path, width_cm, crop=None):
    p = par._p
    for ch in list(p):
        if ch.tag != qn('w:pPr'): p.remove(ch)
    ppr = p.find(qn('w:pPr'))
    if ppr is not None:
        for e in ppr.findall(qn('w:shd')): ppr.remove(e)
    run = par.add_run()
    run.add_picture(path, width=Cm(width_cm))
    par.alignment = 1

def crop_save(src, box, dst):
    im = Image.open(src); im.crop(box).save(dst)

P = d.paragraphs  # reindexar apos remover a linha duplicada
imgs = [i for i, p in enumerate(P) if 'pic:pic' in p._p.xml]
# figuras 2 e 4 sao a 2a e a 4a imagem do documento
put_picture(P[imgs[1]], FIG + 'mapa_02_solo_uso.png', text_w)
put_picture(P[imgs[3]], FIG + 'fig_fluxograma.png', 14.0)
def ph(txt):
    hits = [p for p in P if p.text.startswith(txt)]
    assert len(hits) == 1, txt
    return hits[0]
put_picture(ph('[IMAGEM a inserir: Figura 10'), FIG + 'mapa_06_sedimento_eventos.png', text_w)
put_picture(ph('[IMAGEM a inserir: Figura 11'), FIG + 'mapa_07_sedimento_medio.png', text_w)
im8 = Image.open(FIG + 'mapa_08_evento11.png'); w8, h8 = im8.size
crop_save(FIG + 'mapa_08_evento11.png', (0, int(h8 * 0.055), w8, int(h8 * 0.53)), SP + chr(92) + 'a1.png')
crop_save(FIG + 'mapa_08_evento11.png', (0, int(h8 * 0.53), w8, h8), SP + chr(92) + 'a2.png')
put_picture(ph('[IMAGEM a inserir: Figura A1'), SP + chr(92) + 'a1.png', text_w)
put_picture(ph('[IMAGEM a inserir: Figura A2'), SP + chr(92) + 'a2.png', text_w)

# ---- 3. tirar o destaque amarelo / sombreado de revisao em todo o documento
body = d.element.body
n = 0
for e in list(body.iter(qn('w:shd'))):
    if (e.get(qn('w:fill')) or '').lower() == 'fff299':
        e.getparent().remove(e); n += 1
for e in list(body.iter(qn('w:highlight'))):
    e.getparent().remove(e); n += 1
print('destaques removidos', n)
d.save(OUT)
print('salvo', OUT)
