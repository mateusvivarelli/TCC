import fitz, re, sys
sys.stdout.reconfigure(encoding="utf-8")
doc = fitz.open(r"C:\TCC\1-s2.0-S0022169425002793-main.pdf")
print("paginas", len(doc)); print(doc.metadata)
txt = "\n".join(f"\n=====PAG {i+1}=====\n" + p.get_text() for i, p in enumerate(doc))
open(r"C:\Users\sonek\AppData\Local\Temp\claude\checagens_27-10\brandao_texto.txt", "w", encoding="utf-8").write(txt)
for kw in ("Woodward", "1.33", "1\\.15", "0\\.05", "convert", "S0\\.05", "S_{0", "lambda", "λ"):
    ms = [m.start() for m in re.finditer(kw, txt)]
    print(kw, len(ms))
