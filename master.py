from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import pdfplumber
import docx
from io import BytesIO
from functools import lru_cache
from sentence_transformers import SentenceTransformer, util

app = FastAPI()

@lru_cache()
def get_model():
    return SentenceTransformer("paraphrase-MiniLM-L3-v2")

def extract_text(file: UploadFile) -> str:
    ext = file.filename.split('.')[-1].lower()
    content = file.file.read()
    if ext == "pdf":
        with pdfplumber.open(BytesIO(content)) as pdf:
            return " ".join(p.extract_text() for p in pdf.pages if p.extract_text())
    elif ext in ["doc", "docx"]:
        doc = docx.Document(BytesIO(content))
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        raise ValueError("Unsupported file type")

def get_similarity(resume_text, jd_text):
    model = get_model()
    emb1 = model.encode(resume_text, convert_to_tensor=True)
    emb2 = model.encode(jd_text, convert_to_tensor=True)
    return float(util.pytorch_cos_sim(emb1, emb2))

@app.post("/match")
async def match_resume(resume: UploadFile = File(...), jd: str = Form(...)):
    try:
        resume_text = extract_text(resume)
        score = get_similarity(resume_text, jd)
        return {
            "match_score": round(score, 2),
            "match_level": (
                "Strong" if score > 0.75 else
                "Moderate" if score > 0.5 else
                "Weak"
            )
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    