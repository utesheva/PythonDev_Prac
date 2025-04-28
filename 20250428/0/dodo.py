from pathlib import Path
from zipfile import ZipFile

DOIT_CONFIG = {"default_tasks": ['docs']}

def task_docs():
    """Build docs"""
    return {
            "file_dep": list(Path("./source").glob("*.rst")),
            "actions": ["sphinx-build -M html source _build"],
    }

def task_create_docs():
    task = ['html', 'text']
    for i in range(2):
        yield {'name': f'create {task[i]}',
               "file_dep": list(Path("./source").glob("*.rst")),
               "actions": [f"sphinx-build -M {task[i]} source _build"],
        }

def task_zip():
    """Zip docs"""
    return {
            "task_dep": ["docs"],
            "targets": ["docs.zip"],
            "actions": ["zip -r docs.zip _build/html"]
    }

def task_stat():
    """List zip archive"""
    def zip_smth(zipfile, targets):
        with ZipFile(zipfile, "r") as zf:
            f = '\n'.join(zf.namelist())
            with open(targets[0], "w") as output:
                output.write(f)

    return {
            "actions": [(zip_smth, ["docs.zip"])],
            "file_dep": ["docs.zip"],
            "targets": ["docs.list"]
    }

def task_erase():
    """Erase all generates and new files"""
    return {
            "actions": ["git reset --hard", "git clean -xdf"]
    }

