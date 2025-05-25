from pathlib import Path

DOIT_CONFIG = {"default_tasks": ['html']}


def task_pot():
    """Build pot"""
    return {
        'actions': ["pybabel extract -o mud.pot po"],
        'file_dep': [str(i) for i in Path("./mood/server").glob("*.py")],
        'targets': ["mud.pot"],
    }


def task_po():
    """Build po"""
    return {
        'actions': ["pybabel update -l ru --previous --init-missing --ignore-pot-creation-date -D mud -i mud.pot -d po"],
        'file_dep': ['mud.pot'],
        'targets': ["po/ru/LC_MESSAGES/mud.po"],
    }


def task_il8n():
    """Build il8n"""
    return {
            "file_dep": ['po/ru/LC_MESSAGES/mud.po'],
            "actions": ["pybabel compile -D mud -l ru -i po/ru/LC_MESSAGES/mud.po -d po"],
            "targets": ['po/ru/LC_MESSAGES/mud.mo']
    }


def task_html():
    """Build html"""
    return {
            "file_dep": [str(i) for i in Path("./source").glob("*.rst")],
            'task_dep': ['test'],
            "actions": ["sphinx-build -M html source _build"],
            'targets': ['_build/html/index.html'],
    }


def task_test():
    """Run tests"""
    return {
            'task_dep': ['il8n'],
            "actions": ["python3 -m unittest test_client_srv.py"],
    }


def task_erase():
    """Clean represitory"""
    return {
            'actions': ['git clean -xdf'],
    }
