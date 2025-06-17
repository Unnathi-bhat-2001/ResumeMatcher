import os
import docx
import pdfplumber
import tensorflow_hub as hub
import tensorflow as tf

USE_MODEL = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

def extract_text(path):
    if path.endswith(".pdf"):
        with pdfplumber.open(path) as pdf:
            return "\n".join(p.extract_text() or '' for p in pdf.pages)
    elif path.endswith((".doc", ".docx")):
        doc = docx.Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    return ""

def match_resumes(folder, jd):
    jd_emb = USE_MODEL([jd])
    results = []
    for f in os.listdir(folder):
        if f.lower().endswith((".pdf", ".doc", ".docx")):
            text = extract_text(os.path.join(folder, f))
            if not text.strip(): continue
            emb = USE_MODEL([text])
            score = float(-tf.keras.losses.cosine_similarity(jd_emb, emb).numpy()[0])
            results.append({"file": f, "score": round(score, 2)})
    return results
