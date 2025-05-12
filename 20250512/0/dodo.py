from pathlib import Path

DOIT_CONFIG = {"default_tasks": ['html']}

def task_i8n():
    """Build i8n"""
    return {
            "file_dep": list(Path("./source").glob("*.rst")),
            "actions": ["pybabel compile -D mud -l ru -i po/ru/LC_MESSAGES/mud.po -d po",
    }

def task_html():
    """Build html"""
    return {
            "file_dep": list(Path("./source").glob("*.rst")),
            "actions": ["sphinx-build -M html source _build"],
    }

def task_test():
    """Run tests"""
    return {
            "file_dep": ['po/ru/LC_MESSAGES/mud.mo'],
            "actions": ["python3 -m unittest test_client_srv.py"],
    }

def task_wheel():
    return {
            "actions": ['python -m build --sdist'],
    }
