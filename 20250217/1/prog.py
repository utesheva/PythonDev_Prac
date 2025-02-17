from glob import iglob
from os.path import basename
import sys

name = sys.argv[1]
if len(sys.argv) == 2:
    for name in iglob('/home/kate/PythonDev_Prac/.git/refs/heads/*'):
        print(basename(name))
