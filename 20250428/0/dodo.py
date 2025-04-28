def task_docs():
    """Build docs"""
    return {
            "actions": ["sphinx-build -M html source build"],
    }

def task_erase():
    """Erase all generates and new files"""
    return {
            "actions": ["git reset --hard", "git clean -xdf"]
    }
