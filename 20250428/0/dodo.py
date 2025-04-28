def task_docs():
    """Build docs"""
    return {
            "actions": ["sphinx-build -M html source build"],
    }
