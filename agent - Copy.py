from pathlib import Path
import re
from .repository import iter_files,is_test_file
TERMS={"auth":["auth","login","password","token","session","user"],"api":["api","route","endpoint","controller","view"],"database":["db","database","model","schema","migration"],"frontend":["component","page","view","ui","client","frontend","src"],"payment":["payment","billing","checkout","invoice"]}

def score(p,task):
    hay=f"{p} {p.name}".lower(); words=re.findall(r"[a-zA-Z_]{3,}",task.lower())
    points=sum(2 for w in words if w in hay)
    for domain,terms in TERMS.items():
        if domain in task.lower(): points+=sum(2 for t in terms if t in hay)
    return points+(1 if is_test_file(p) else 0)

def build_plan(repo_path,task):
    root=Path(repo_path).resolve()
    ranked=sorted(((score(p,task),str(p.relative_to(root))) for p in iter_files(root)),reverse=True)
    relevant=[p for s,p in ranked if s>0][:10] or [p for _,p in ranked[:10]]
    area=next((d for d in TERMS if d in task.lower()),"application logic")
    return {"task":task,"relevant_files":relevant,"suspected_area":area,
            "investigation":["Map the repository and locate implementation files related to the task.","Inspect existing tests before changing behavior.","Trace the execution path and prefer existing project patterns.","Do not invent imports, APIs, helpers, or configuration."],
            "validation_contract":["Add/update a focused regression test.","Run the complete existing test suite.","Inspect the final Git diff for unrelated changes.","Only report VERIFIED when regression and existing tests pass."]}
