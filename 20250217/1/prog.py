from zlib import decompress
from glob import iglob
from os.path import dirname, basename
import sys

def get_branches(path):
    return '\n'.join([basename(i) for i in iglob(path + "/.git/refs/heads/*")])

def get_last_commit_id(path, branch):
    return open(path + '/.git/refs/heads/' + branch).read()[:-1]


def get_obj_by_id(path, obj_id):
    f = open(path + f'/.git/objects/{obj_id[:2]}/{obj_id[2:]}', 'rb')
    obj = decompress(f.read())
    return obj.partition(b'\x00')

def parse_tree(path, body):
    tree = []
    tail = body
    while tail:
        treeobj, _, tail = tail.partition(b'\x00')
        tmode, tname = treeobj.split()
        num, tail = tail[:20], tail[20:]
        obj_id = num.hex()
        obj_name = get_obj_by_id(path, obj_id)[0].decode().split()[0]
        tree.append([obj_name, obj_id, tname.decode()])
    return tree

def commits_to_dict(path, branch):
    f = open(path+'/.git/logs/refs/heads/' + branch).read()
    commits = dict()
    for i in f.split('\n'):
        if len(i) == 0: continue
        cur = i.split()[1]
        if cur not in commits:
            commits[cur] = i.split()[0]
    return commits

path = sys.argv[1]

if len(sys.argv) == 2:
    print(get_branches(path))
else:
    name = sys.argv[2]
    last_commit_id = get_last_commit_id(path, name)
    header, _, body = get_obj_by_id(path, last_commit_id)
    print(body.decode())
    
    print("TREE FOR THE LAST COMMIT")
    tree_id = body.decode().split('\n')[0].split()[1]
    header, _, body = get_obj_by_id(path, tree_id)
    print('\n'.join([' '.join(i) for i in parse_tree(path, body)]))
    print()
    commits = commits_to_dict(path, name)
    cur = last_commit_id

    while cur != '0000000000000000000000000000000000000000':
        print(f'TREE for commit {cur}')
        cur = commits[cur]
        header, _, body = get_obj_by_id(path, last_commit_id)
        tree_id = body.decode().split('\n')[0].split()[1]
        header, _, body = get_obj_by_id(path, tree_id)
        print('\n'.join([' '.join(i) for i in parse_tree(path, body)]))

