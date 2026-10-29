import json,sys,re
def load(path):
    j=json.load(open(path,encoding="utf-8")); c=j["content"]; return c, c["tabs"][0]["documentTab"]
def paras(tab):
    out=[]
    def walk(content,intable=None):
        for el in content:
            if "paragraph" in el:
                p=el["paragraph"]; t="".join(r.get("textRun",{}).get("content","") for r in p["elements"])
                has_eq=any("equation" in r for r in p["elements"]); has_img=any("inlineObjectElement" in r for r in p["elements"])
                out.append(dict(s=el["startIndex"],e=el["endIndex"],style=p["paragraphStyle"].get("namedStyleType"),al=p["paragraphStyle"].get("alignment"),
                  fi=(p["paragraphStyle"].get("indentFirstLine") or {}).get("magnitude"),t=t,eq=has_eq,img=has_img,tbl=intable,bullet="bullet" in p))
            elif "table" in el:
                tb=el["table"]
                for ri,row in enumerate(tb["tableRows"]):
                    for ci,cell in enumerate(row["tableCells"]): walk(cell["content"],(el["startIndex"],ri,ci))
    walk(tab["body"]["content"]); return out
if __name__=="__main__":
    c,tab=load(sys.argv[1]); P=paras(tab)
    for k,p in enumerate(P):
        if p["tbl"] and p["tbl"][1]>0: continue   # so cabecalho/1a linha de tabelas
        flag=("EQ " if p["eq"] else "")+("IMG " if p["img"] else "")+("TBL%d "%p["tbl"][0] if p["tbl"] else "")
        print(k,p["s"],p["e"],p["style"],p["al"],p["fi"],flag+repr(p["t"][:75]))
