from zlib import decompress
from glob import iglob
from os.path import dirname, basename
import sys

def get_branches(path):
    return '\n'.join([basename(i) for i in iglob(path + "/.git/refs/heads/*")])

def get_last_commit_id(path, branch):
    return open(path + '/.git/refs/heads/' + branch).read()

def get_obj_by_id(path, obj_id):
    f = open(path + f'/.git/objects/{obj_id[:2]}/{obj_id[2:-1]}', 'rb')
    obj = decompress(f.read())
    return obj.partition(b'\x00')


path = sys.argv[1]

if len(sys.argv) == 2:
    print(get_branches(path))
else:
    name = sys.argv[2]
    last_commit_id = get_last_commit_id(path, name)
    header, _, body = get_obj_by_id(path, last_commit_id)
    print(body.decode())

