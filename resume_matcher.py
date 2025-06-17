import os
import docx
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text(path):
    if path.lower().endswith(".pdf"):
        with pdfplumber.open(path) as pdf:
            return "\n".join(p.extract_text() or "" for p in pdf.pages)
    elif path.lower().endswith((".doc", ".docx")):
        doc = docx.Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    return ""

def match_resumes(folder, jd):
    texts = []
    files = []
    for f in os.listdir(folder):
        if f.lower().endswith((".pdf", ".doc", ".docx")):
            txt = extract_text(os.path.join(folder, f))
            if txt.strip():
                texts.append(txt)
                files.append(f)

    if not texts:
        return []

    tfidf = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform([jd] + texts)  # row0=JD, others=resumes
    sims = cosine_similarity(matrix[0:1], matrix[1:])[0]

    result = []
    for f, score in zip(files, sims):
        result.append({"file": f, "score": round(float(score), 2)})
    return sorted(result, key=lambda x: x["score"], reverse=True)
