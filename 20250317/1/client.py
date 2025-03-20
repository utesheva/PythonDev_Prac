import cmd
from prog import Error
import shlex
import cowsay
import readline
import sys
import socket

cows = cowsay.list_cows() + ['jgsbat']

def parse_args(args, param):
    args_parsed = {}
    for i in param:
        if i not in args:
            return None
        args_parsed[i] = args[args.index(i) + 1: args.index(i) + 1 + param[i]]
    return args_parsed

def add_monster_check(args):
    preprocess = shlex.split(args)
    if len(preprocess) != 8:
        raise Error(1)
    name = preprocess[0]
    parsed_args = parse_args(preprocess[1:], {"hello": 1, "hp": 1, "coords": 2})
    if not parsed_args:
        raise Error(1)
    x, y = parsed_args['coords']
    hello = parsed_args['hello'][0]
    hp = parsed_args['hp'][0]
    if (not x.isdigit() or
        not y.isdigit() or
        not hp.isdigit()):
        raise Error(1)
    x, y, hp = map(int, [x, y, hp])
    if x < 0 or x >= 10 or y < 0 or y >= 10 or hp <= 0:
        raise Error(1)
    if name not in cows:
        raise Error(2)
    return x, y, hp, hello, name

def attack_check(self, x, y, args):
    splitted = shlex.split(args)
    parsed_args = parse_args(splitted, {'with': 1})
    if parsed_args:
        match parsed_args['with'][0]:
            case 'sword': weapon = 10
            case 'spear': weapon = 15
            case 'axe': weapon = 20
            case _:
                raise Error(4)
    else: weapon = 10
    if len(args) == 0 or splitted[0] not in cows:
        raise Error(1)
    name = splitted[0]
    return weapon, name

class Client_MUD(cmd.Cmd):
    prompt = 'MUD> '
    readline.set_completer_delims(readline.get_completer_delims().replace('-', ''))

    def do_addmon(self, args):
        try:
            x, y, hp, hello, name = add_monster_check(args)
        except Error as e:
            print(e.text)

    def do_attack(self, args):
        try:
            weapon, name = attack_check(args)
        except Error as e:
            print(e.text)
    
    def do_up(self, args):
        if len(args) != 0:
            print(Error(1).text)

    def do_down(self, args):
        if len(args) != 0:
            print(Error(1).text)

    def do_left(self, args):
        if len(args) != 0:
            print(Error(1).text)

    def do_right(self, args):
        if len(args) != 0:
            print(Error(1).text)

if __name__ == '__main__':
    host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
    port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        Client_MUD().cmdloop()
