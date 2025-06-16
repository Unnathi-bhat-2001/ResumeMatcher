from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from resume_matcher import match_resumes
import os, shutil, tempfile

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def health(): return {"status": "alive"}

@app.post("/match-folder")
async def match_folder(jd: str = Form(...), resumes: list[UploadFile] = File(...)):
    temp_dir = tempfile.mkdtemp()
    try:
        for resume in resumes:
            with open(os.path.join(temp_dir, resume.filename), "wb") as f:
                f.write(await resume.read())
        result = match_resumes(temp_dir, jd)
        return result
    finally:
        shutil.rmtree(temp_dir)
