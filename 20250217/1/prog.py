from zlib import decompress
from glob import iglob
from os.path import dirname, basename
import sys

path = sys.argv[1]
if len(sys.argv) == 2:
    for name in iglob(path + '/.git/refs/heads/*'):
        print(basename(name))
else:
    name = sys.argv[2]
    last_commit = open(path + '/.git/refs/heads/' + name).read()
    f = open(path + f'/.git/objects/{last_commit[:2]}/{last_commit[2:-1]}', 'rb')
    obj = decompress(f.read())
    header, _, body = obj.partition(b'\x00')
    out = body.decode().replace('\n', '\n' + "  ")
    print(f"  {out}")
