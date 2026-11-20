"""Montagem para o Instagram (1080 x 1350): foto da defesa + mapa de erosão média do TCC."""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FOTO, NOME = sys.argv[1], sys.argv[2]
OUT = NOME  # caminho de saida (fora do repositorio: as fotos sao pessoais)
NAVY, AZUL, BRANCO, LARANJA = (27, 58, 107), (61, 133, 198), (255, 255, 255), (232, 160, 60)
F = lambda s, b=True: ImageFont.truetype(f"/usr/share/fonts/truetype/crosextra/Carlito-{'Bold' if b else 'Regular'}.ttf", s)

W, H = 1080, 1350
img = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(img)

# foto: recorte 4:3 ocupando o topo
f = Image.open(FOTO).convert("RGB"); fw, fh = f.size
alvo = 4 / 3
if fw / fh > alvo:
    nw = int(fh * alvo); f = f.crop(((fw - nw) // 2, 0, (fw - nw) // 2 + nw, fh))
else:
    nh = int(fw / alvo); f = f.crop((0, (fh - nh) // 2, fw, (fh - nh) // 2 + nh))
f = f.resize((W, 700), Image.LANCZOS); img.paste(f, (0, 0))

# faixa "TCC aprovado"
d.rounded_rectangle((40, 40, 420, 112), radius=16, fill=LARANJA)
d.text((230, 77), "TCC APROVADO", font=F(46), fill=NAVY, anchor="mm")

# texto
y = 726
d.text((W // 2, y), "Espacialização da MUSLE para identificação", font=F(38), fill=BRANCO, anchor="ma")
d.text((W // 2, y + 44), "de áreas críticas de erosão", font=F(38), fill=BRANCO, anchor="ma")
d.text((W // 2, y + 98), "Estudo de caso na bacia do rio Jundiaí", font=F(28, False), fill=(205, 222, 242), anchor="ma")

# mapa (area interna do grafico) em cartao branco
m = Image.open(os.path.join(BASE, "TCC_Texto", "figuras", "slides", "mapa_medio_MC.png")).convert("RGB").crop((106, 122, 979, 480))
mw = 820; mh = int(m.height * mw / m.width); m = m.resize((mw, mh), Image.LANCZOS)
cy = 870
d.rounded_rectangle(((W - mw) // 2 - 10, cy - 10, (W + mw) // 2 + 10, cy + mh + 10), radius=18, fill=BRANCO)
img.paste(m, ((W - mw) // 2, cy))
d.text((W // 2, cy + mh + 24), "Erosão média de 17 eventos de chuva, pixel a pixel (30 m)", font=F(24, False), fill=(205, 222, 242), anchor="ma")
d.text((W // 2, H - 38), "Engenharia Civil  ·  FECFAU / Unicamp  ·  2026", font=F(24), fill=BRANCO, anchor="mm")
img.save(OUT, quality=95); print("ok", OUT, mh)
