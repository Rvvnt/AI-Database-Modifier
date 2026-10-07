from app.agent import build_plan
def test_plan_finds_related_files(tmp_path):
    (tmp_path/"auth.py").write_text("def login(): pass")
    (tmp_path/"tests").mkdir()
    (tmp_path/"tests"/"test_auth.py").write_text("def test_login(): pass")
    r=build_plan(str(tmp_path),"Fix authentication login password")
    assert "auth.py" in r["relevant_files"]
    assert any("test_auth.py" in x for x in r["relevant_files"])
    assert r["validation_contract"]
