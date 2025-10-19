# Test, der die Syntax von Dateien prüft

def test_all_python_files_syntax():
    for file in pathlib.Path(".").rglob("*.py"):
        try:
            compile(file.read_text(encoding="utf-8"), str(file), "exec")
        except SyntaxError as e:
            pytest.fail(f"Syntaxfehler in {file}: {e}")