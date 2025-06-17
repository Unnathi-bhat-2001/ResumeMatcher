from fastapi import FastAPI, UploadFile, File, Form
import tempfile, os, shutil
from resume_matcher import match_resumes

app = FastAPI()

@app.get("/")
def root(): return {"status": "OK"}

@app.post("/match")
async def match(jd: str = Form(...), resumes: list[UploadFile] = File(...)):
    tmp = tempfile.mkdtemp()
    try:
        for r in resumes:
            out = os.path.join(tmp, r.filename)
            with open(out, "wb") as f:
                f.write(await r.read())
        return match_resumes(tmp, jd)
    finally:
        shutil.rmtree(tmp)
