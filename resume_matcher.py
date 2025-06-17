import os, docx, pdfplumber, requests

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
HEADERS = {"Authorization": f"Bearer {os.environ['HF_TOKEN']}"}

def extract_text(path):
    if path.lower().endswith(".pdf"):
        with pdfplumber.open(path) as pdf:
            return "\n".join(p.extract_text() or "" for p in pdf.pages)
    elif path.lower().endswith((".doc", ".docx")):
        return "\n".join(p.text for p in docx.Document(path).paragraphs)
    return ""

def get_similarity(jd, resume_text):
    response = requests.post(API_URL, headers=HEADERS, json={
        "inputs": {
            "source_sentence": jd,
            "sentences": [resume_text]
        }
    })
    if response.status_code == 200:
        return response.json()[0]
    else:
        return 0.0  # fallback if request fails

def match_resumes(folder, jd):
    results = []
    for f in os.listdir(folder):
        if f.lower().endswith((".pdf", ".doc", ".docx")):
            txt = extract_text(os.path.join(folder, f))
            sim = get_similarity(jd, txt)
            results.append({"file": f, "score": round(sim, 2)})
    return sorted(results, key=lambda x: x["score"], reverse=True)
