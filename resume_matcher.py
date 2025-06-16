import os
import docx
import pdfplumber
from sentence_transformers import SentenceTransformer, util

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            return "\n".join(p.extract_text() or '' for p in pdf.pages)
    elif file_path.endswith((".doc", ".docx")):
        doc = docx.Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)
    return ""

def match_resumes(folder_path, jd):
    model = SentenceTransformer("all-MiniLM-L6-v2")  # Light model
    jd_emb = model.encode(jd, convert_to_tensor=True)

    result = []
    for f in os.listdir(folder_path):
        if f.endswith((".pdf", ".doc", ".docx")):
            full_path = os.path.join(folder_path, f)
            text = extract_text(full_path)
            if not text.strip(): continue
            emb = model.encode(text, convert_to_tensor=True)
            score = float(util.pytorch_cos_sim(jd_emb, emb))
            result.append({"file": f, "score": round(score, 2)})
    return result
