import os, difflib, docx, pdfplumber

def extract_text(path):
    if path.lower().endswith(".pdf"):
        with pdfplumber.open(path) as pdf:
            return "\n".join(p.extract_text() or "" for p in pdf.pages)
    elif path.lower().endswith((".doc", ".docx")):
        return "\n".join(p.text for p in docx.Document(path).paragraphs)
    return ""

def match_resumes(folder, jd):
    results = []
    for f in os.listdir(folder):
        if f.lower().endswith((".pdf", ".doc", ".docx")):
            txt = extract_text(os.path.join(folder, f))
            ratio = difflib.SequenceMatcher(None, jd, txt).ratio()
            results.append({"file": f, "score": round(ratio, 2)})
    return sorted(results, key=lambda x: x["score"], reverse=True)
