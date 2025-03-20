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
    host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
    port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])

    def __init__(self, socket):
        self.s = socket
        self.s.connect((self.host, self.port))
        return super().__init__()

    def response(self):
        print(self.s.recv(1024).rstrip().decode())
    
    def do_addmon(self, args):
        try:
            x, y, hp, hello, name = add_monster_check(args)
            self.s.sendall(f"addmon {name} {x} {y} {hp} {hello}".encode())
            self.response()
        except Error as e:
            print(e.text)

    def do_attack(self, args):
        try:
            weapon, name = attack_check(args)
            self.s.sendall(f"attack {weapon} {name}".encode())
            self.response()
        except Error as e:
            print(e.text)
    
    def do_up(self, args):
        if len(args) != 0:
            print(Error(1).text)
        else:
            self.s.sendall(f"move 0 -1".encode())
            self.response()

    def do_down(self, args):
        if len(args) != 0:
            print(Error(1).text)
        else:
            self.s.sendall(f"move 0 1".encode())
            self.response()

    def do_left(self, args):
        if len(args) != 0:
            print(Error(1).text)
        else:
            self.s.sendall(f"move -1 0".encode())
            self.response()

    def do_right(self, args):
        if len(args) != 0:
            print(Error(1).text)
        else:
            self.s.sendall(f"move 1 0".encode())
            self.response()
    
    def default(self, args):
        print("Invalid command")

    def complete_addmon(self, text, line, begidx, endidx):
        words = (line[:endidx] + ".").split()
        DICT = list({'hello', 'hp', 'coords'} - set(line[:endidx].split()))
        if 'coords' in words and words[-2] != 'coords':
            condition = (len(words) % 2 == 0)
        else:
            condition = (len(words) % 2 == 1)
        if len(words) == 2:
            DICT = cows
        elif not condition:
            DICT = []
        return [c for c in DICT if c.startswith(text)]

    def complete_attack(self, text, line, begidx, endidx):
        words = (line[:endidx] + ".").split()
        if (len(words) == 2 and
            (not hasattr(self, 'ind') or
             hasattr(self, 'ind') and self.matches[self.ind] != text)):
            self.matches = [c for c in self.game.cows if c.startswith(text)]
            self.ind = -1
        elif len(words) == 3:
            self.matches = ['with']
            self.ind = -1
        elif len(words) == 4 and words[-2] == 'with' and (self.matches[self.ind] != text or text == ''):
            self.matches = ['sword', 'spear', 'axe']
            self.ind = -1
        self.ind = (self.ind + 1) % len(self.matches)
        return [self.matches[self.ind]]

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    Client_MUD(socket=s).cmdloop()
