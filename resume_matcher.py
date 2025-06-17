import os
import difflib
import docx
import pdfplumber

def extract_text(path):
    if path.lower().endswith(".pdf"):
        with pdfplumber.open(path) as pdf:
            return "\n".join(p.extract_text() or "" for p in pdf.pages)
    elif path.lower().endswith((".doc", ".docx")):
        doc = docx.Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    return ""

def match_resumes(folder, jd):
    results = []
    for filename in os.listdir(folder):
        if not filename.lower().endswith((".pdf", ".doc", ".docx")):
            continue
        text = extract_text(os.path.join(folder, filename))
        if not text.strip(): continue

        ratio = difflib.SequenceMatcher(None, jd, text).ratio()
        results.append({"file": filename, "score": round(ratio, 2)})

    return sorted(results, key=lambda x: x["score"], reverse=True)
