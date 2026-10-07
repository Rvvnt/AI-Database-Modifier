from pathlib import Path
from collections import Counter
import subprocess

IGNORED={".git",".venv","venv","node_modules","__pycache__",".idea",".pytest_cache","dist","build"}
EXTENSIONS={".py":"Python",".js":"JavaScript",".jsx":"React",".ts":"TypeScript",".tsx":"React/TypeScript",".java":"Java",".go":"Go",".rs":"Rust",".cpp":"C++",".c":"C",".html":"HTML",".css":"CSS",".json":"JSON",".yaml":"YAML",".yml":"YAML",".md":"Markdown"}

def safe_root(path):
    root=Path(path).expanduser().resolve()
    if not root.is_dir(): raise ValueError(f"Repository directory does not exist: {root}")
    return root

def iter_files(root):
    for p in root.rglob("*"):
        if p.is_file() and not any(x in IGNORED for x in p.parts): yield p

def language_for(p): return EXTENSIONS.get(p.suffix.lower(),"Other")

def is_test_file(p):
    n=p.name.lower(); s=str(p).replace("\\","/").lower()
    return n.startswith("test_") or n.endswith("_test.py") or ".test." in n or ".spec." in n or "/tests/" in s

def detect_test_command(root):
    if any(p.suffix==".py" for p in iter_files(root)) and ((root/"tests").exists() or (root/"pyproject.toml").exists() or (root/"pytest.ini").exists()):
        return "python -m pytest"
    if (root/"package.json").exists(): return "npm test"
    if (root/"go.mod").exists(): return "go test ./..."
    return None

def framework_signals(root):
    text=""
    for name in ["requirements.txt","pyproject.toml","package.json","go.mod"]:
        p=root/name
        if p.exists(): text+=p.read_text(encoding="utf-8",errors="ignore").lower()
    signals={"FastAPI":"fastapi","Flask":"flask","Django":"django","React":"react","Next.js":"next","Express":"express","pytest":"pytest","Jest":"jest"}
    return [k for k,v in signals.items() if v in text][:8]

def summarize(root):
    fs=list(iter_files(root)); langs=Counter(language_for(p) for p in fs); tests=[p for p in fs if is_test_file(p)]
    recent=sorted(fs,key=lambda p:p.stat().st_mtime,reverse=True)[:10]
    return {"name":root.name,"path":str(root),"files":len(fs),"tests":len(tests),"languages":dict(langs),"framework_signals":framework_signals(root),"test_command":detect_test_command(root),
            "recent_files":[{"path":str(p.relative_to(root)),"language":language_for(p),"lines":len(p.read_text(encoding="utf-8",errors="ignore").splitlines()),"is_test":is_test_file(p)} for p in recent]}

def git_diff(root):
    try:
        r=subprocess.run(["git","-C",str(root),"diff","--","."],capture_output=True,text=True,timeout=10); return r.stdout
    except (OSError,subprocess.SubprocessError): return ""
