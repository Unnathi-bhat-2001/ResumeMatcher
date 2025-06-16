import os
from io import BytesIO
import pdfplumber
import docx
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

def extract_text_from_file(path):
    ext = path.lower().split(".")[-1]
    if ext == "pdf":
        with pdfplumber.open(path) as pdf:
            return " ".join(p.extract_text() for p in pdf.pages if p.extract_text())
    elif ext in ["doc", "docx"]:
        docf = docx.Document(path)
        return "\n".join(p.text for p in docf.paragraphs)
    return ""

def match_resumes(folder_path, jd_text, threshold=0.5):
    matches = []
    jd_embedding = model.encode(jd_text, convert_to_tensor=True)
    for file in os.listdir(folder_path):
        if file.endswith((".pdf", ".doc", ".docx")):
            full_path = os.path.join(folder_path, file)
            resume_text = extract_text_from_file(full_path)
            if resume_text.strip():
                sim = util.pytorch_cos_sim(
                    model.encode(resume_text, convert_to_tensor=True), jd_embedding
                ).item()
                if sim >= threshold:
                    matches.append({"file": file, "score": round(sim, 2)})
    return matches
