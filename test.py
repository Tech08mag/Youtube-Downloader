import os, inspect
print(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))