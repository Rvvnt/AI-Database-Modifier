import subprocess,time
ALLOWED={"pytest":["pytest"],"python -m pytest":["python","-m","pytest"],"npm test":["npm","test"],"npm run test":["npm","run","test"],"go test ./...":["go","test","./..."]}
def run_tests(repo_path,command):
    from pathlib import Path
    if command not in ALLOWED: raise ValueError("Unsupported test command.")
    start=time.perf_counter()
    try:
        r=subprocess.run(ALLOWED[command],cwd=Path(repo_path),capture_output=True,text=True,timeout=120)
        out=((r.stdout or "")+"\n"+(r.stderr or "")).strip(); code=r.returncode
    except subprocess.TimeoutExpired:
        out="Test process exceeded the 120-second safety limit."; code=124
    except OSError as e: out=str(e); code=127
    return {"command":command,"return_code":code,"passed":code==0,"output":out[-16000:],"duration_ms":int((time.perf_counter()-start)*1000)}
