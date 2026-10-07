from pathlib import Path
import re, subprocess, tempfile
GITHUB_RE=re.compile(r"^https?://github\\.com/[^/]+/[^/]+/?(?:\\.git)?$")
def load_source(source):
    source=source.strip()
    if not source.startswith(("http://","https://")):
        p=Path(source).expanduser().resolve()
        if not p.is_dir(): raise ValueError(f"Local repository not found: {p}")
        return {"path":str(p),"source":"local"}
    if not GITHUB_RE.match(source): raise ValueError("Use a standard public GitHub repository URL.")
    name=source.rstrip("/").split("/")[-1].removesuffix(".git")
    target=Path(tempfile.mkdtemp(prefix="forgepilot_"))/name
    r=subprocess.run(["git","clone","--depth","1",source,str(target)],capture_output=True,text=True,timeout=120)
    if r.returncode: raise ValueError((r.stderr or r.stdout)[-2000:])
    return {"path":str(target),"source":source}
