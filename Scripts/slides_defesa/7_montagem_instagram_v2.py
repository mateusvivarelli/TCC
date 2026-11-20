"""Montagem para o Instagram, versao 2 (1080 x 1350): foto que se dissolve no fundo escuro e o mapa
de erosao media sem fundo, como se flutuasse. Uso: python 7_...py foto.jpg saida.jpg"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FOTO, OUT = sys.argv[1], sys.argv[2]
FUNDO = np.array([14, 30, 58]); LARANJA = (240, 165, 60); BRANCO = (255, 255, 255); CLARO = (190, 208, 232)
F = lambda s, b=True: ImageFont.truetype(f"/usr/share/fonts/truetype/crosextra/Carlito-{'Bold' if b else 'Regular'}.ttf", s)
W, H, FH = 1080, 1350, 770

img = Image.new("RGB", (W, H), tuple(FUNDO))
f = Image.open(FOTO).convert("RGB"); fw, fh = f.size
alvo = W / FH
if fw / fh > alvo:
    nw = int(fh * alvo); x0 = (fw - nw) // 2; f = f.crop((x0, 0, x0 + nw, fh))
else:
    nh = int(fw / alvo); f = f.crop((0, 0, fw, nh))
f = np.array(f.resize((W, FH), Image.LANCZOS)).astype(float)
# degrade: a parte de baixo da foto se dissolve no fundo
a = np.ones(FH); t0 = FH - 230; a[t0:] = np.linspace(1, 0, FH - t0) ** 1.6
f = f * a[:, None, None] + FUNDO * (1 - a[:, None, None])
img.paste(Image.fromarray(f.astype(np.uint8)), (0, 0))
d = ImageDraw.Draw(img)

# texto
y = 712
d.text((70, y), "TCC APROVADO", font=F(56), fill=LARANJA)
d.line((72, y + 66, 300, y + 66), fill=LARANJA, width=5)
d.text((70, y + 86), "Espacialização da MUSLE para identificação", font=F(36), fill=BRANCO)
d.text((70, y + 128), "de áreas críticas de erosão", font=F(36), fill=BRANCO)
d.text((70, y + 176), "Estudo de caso na bacia do rio Jundiaí", font=F(27, False), fill=CLARO)

# mapa sem fundo: branco e cinza neutro ficam transparentes; preto vira branco
m = np.array(Image.open(os.path.join(BASE, "TCC_Texto", "figuras", "slides", "mapa_medio_MC.png")).convert("RGB").crop((106, 122, 979, 480))).astype(int)
sat = m.max(axis=2) - m.min(axis=2); lum = m.mean(axis=2)
alpha = np.where((sat < 30) & (lum > 150), 0, 255)
escuro = (sat < 40) & (lum < 110)
m[escuro] = [235, 240, 248]
rgba = np.dstack([m, alpha]).astype(np.uint8)
mapa = Image.fromarray(rgba, "RGBA"); mw = 780; mh = int(mapa.height * mw / mapa.width)
mapa = mapa.resize((mw, mh), Image.LANCZOS)
my = 950
img.paste(mapa, ((W - mw) // 2 + 10, my), mapa)
d.text((70, H - 54), "Erosão média de 17 eventos de chuva, pixel a pixel", font=F(23, False), fill=CLARO)
d.text((W - 70, H - 54), "Engenharia Civil · Unicamp · 2026", font=F(23), fill=BRANCO, anchor="ra")
img.save(OUT, quality=95); print("ok", OUT, mh)
