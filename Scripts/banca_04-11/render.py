import fitz,sys
d=fitz.open("tcc_b/TCC_Texto/TCC_versao_04-11.pdf")
print(len(d))
for p in [23,26,27,29,43,45,46,47,49,52,53,67,68]:
    pg=d[p-1]; pix=pg.get_pixmap(dpi=95); pix.save(f"figs/p{p}.png")
