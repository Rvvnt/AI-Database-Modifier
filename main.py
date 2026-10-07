from fastapi import FastAPI,HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .models import RepoRequest,TaskRequest,TestRequest
from .repository import safe_root,summarize,git_diff
from .repository_loader import load_source
from .agent import build_plan
from .runner import run_tests
app=FastAPI(title="ForgePilot — AI Software Engineering Agent")
app.mount("/static",StaticFiles(directory="app/static"),name="static")
@app.get("/")
def index(): return FileResponse("app/static/index.html")
@app.get("/api/health")
def health(): return {"status":"ok","agent":"forgepilot","version":"2.0"}
@app.post("/api/repository")
def repository(req:RepoRequest):
    try:
        x=load_source(req.source); d=summarize(safe_root(x["path"])); d["source"]=x["source"]; return d
    except (ValueError,OSError) as e: raise HTTPException(400,str(e))
@app.post("/api/plan")
def plan(req:TaskRequest):
    try: safe_root(req.repo_path); return build_plan(req.repo_path,req.task)
    except ValueError as e: raise HTTPException(400,str(e))
@app.post("/api/tests")
def tests(req:TestRequest):
    try:
        root=safe_root(req.repo_path); info=summarize(root); cmd=req.command or info["test_command"]
        if not cmd: raise ValueError("No supported test command detected.")
        return run_tests(req.repo_path,cmd)
    except ValueError as e: raise HTTPException(400,str(e))
@app.get("/api/diff")
def diff(path:str):
    try: return {"diff":git_diff(safe_root(path))}
    except ValueError as e: raise HTTPException(400,str(e))
