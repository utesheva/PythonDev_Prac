from pathlib import Path

DOIT_CONFIG = {"default_tasks": ['html']}


def task_pot():
    """Build pot"""
    return {
        'actions': ["pybabel extract -o mood/mud.pot mood"],
        'file_dep': [str(i) for i in Path("./mood/server").glob("*.py")],
        'targets': ["mood/mud.pot"],
    }


def task_po():
    """Build po"""
    return {
        'actions': ["pybabel update -l ru --previous --init-missing --ignore-pot-creation-date -D mud -i mood/mud.pot -d mood/po"],
        'file_dep': ['mood/mud.pot'],
        'targets': ["mood/po/ru/LC_MESSAGES/mud.po"],
    }


def task_il8n():
    """Build il8n"""
    return {
            "file_dep": ['mood/po/ru/LC_MESSAGES/mud.po'],
            "actions": ["pybabel compile -D mud -l ru -i mood/po/ru/LC_MESSAGES/mud.po -d mood/po"],
            "targets": ['mood/po/ru/LC_MESSAGES/mud.mo']
    }


def task_html():
    """Build html"""
    return {
            "file_dep": [str(i) for i in Path("./source").glob("*.rst")],
            'task_dep': ['test'],
            "actions": ["sphinx-build -M html docs mood/_build"],
            'targets': ['mood/_build/html/index.html'],
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


def task_sdist():
    """Make sdist"""
    return {
            'task_dep': ['html', 'erase'],
            'actions': ['python3 -m build -s -n']
    }

def task_wheel():
    """Make wheel"""
    return {
            'task_dep': ['html'],
            'actions': ['python3 -m build -w']
    }
