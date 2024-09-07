import os, inspect

def resource_path():
    cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    return cwd