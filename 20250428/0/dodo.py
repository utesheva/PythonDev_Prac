from pathlib import Path

def task_docs():
    """Build docs"""
    return {
            "file_dep": list(Path(".").glob("*.{py, rst}")),
            "actions": ["sphinx-build -M html source _build"],
    }

def task_erase():
    """Erase all generates and new files"""
    return {
            "actions": ["git reset --hard", "git clean -xdf"]
    }
