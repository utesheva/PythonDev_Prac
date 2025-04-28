from pathlib import Path

DOIT_CONFIG = {"default_tasks": ['docs']}

def task_docs():
    """Build docs"""
    return {
            "file_dep": list(Path("./source").glob("*.rst")),
            "actions": ["sphinx-build -M html source _build"],
    }

def task_erase():
    """Erase all generates and new files"""
    return {
            "actions": ["git reset --hard", "git clean -xdf"]
    }
