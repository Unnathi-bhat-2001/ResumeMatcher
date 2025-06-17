from fastapi import FastAPI, UploadFile, File, Form
import tempfile, shutil, os
from resume_matcher import match_resumes

app = FastAPI()

@app.get("/")
def root():
    return {"status": "OK"}

@app.post("/match")
async def match(jd: str = Form(...), resumes: list[UploadFile] = File(...)):
    tmp = tempfile.mkdtemp()
    try:
        for file in resumes:
            path = os.path.join(tmp, file.filename)
            with open(path, "wb") as f:
                f.write(await file.read())
        return match_resumes(tmp, jd)
    finally:
        shutil.rmtree(tmp)
