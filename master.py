from fastapi import FastAPI, UploadFile, File, Form
import tempfile, os, shutil
from resume_matcher import match_resumes

app = FastAPI()

@app.get("/")
def root(): return {"status": "OK"}

@app.post("/match")
async def match(jd: str = Form(...), resumes: list[UploadFile] = File(...)):
    temp_dir = tempfile.mkdtemp()
    try:
        for r in resumes:
            with open(os.path.join(temp_dir, r.filename), "wb") as f:
                f.write(await r.read())
        result = match_resumes(temp_dir, jd)
        return result
    finally:
        shutil.rmtree(temp_dir)
