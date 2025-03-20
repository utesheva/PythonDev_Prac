import cmd
from prog import Error
import shlex
import cowsay
import readline
import sys
import socket
from io import StringIO

cows = cowsay.list_cows() + ['jgsbat']

jgsbat = cowsay.read_dot_cow(StringIO(r"""
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\\\--//|.'-._  (
     )'   .'\/o\/o\/'.   `(
      ) .' . \====/ . '. (
       )  / <<    >> \  (
        '-._/``  ``\_.-'
  jgs     __\\\'--'//__
         (((""`  `"")))
"""))

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

def attack_check(args):
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

    def __init__(self, *args, socket, **kwargs):
        self.s = socket
        self.s.connect((self.host, self.port))
        return super().__init__(*args, **kwargs)
    
    def response_addmon(self, name, x, y, hello):
        response = self.s.recv(1024).rstrip().decode()
        print(f"Added monster {name} to ({x}, {y}) saying {hello}")
        if response == '1': print("Replaced the old monster")

    def response_attack(self, name):
        response = self.s.recv(1024).rstrip().decode()
        if response == 'no':
            print(f"No {name} here")
            return
        damage, hp = [int(i) for i in response.split()]
        print(f"Attacked {name}, damage {damage} hp")
        if hp == 0:
            print(f"{name} died")
        else:
            print(f"{name} now has {hp}")

    def response_move(self):
        response = self.s.recv(1024).rstrip().decode().split()
        print(f"Moved to ({int(response[0])}, {int(response[1])})")
        if len(response) > 2:
            hello = ' '.join(response[3:])
            if response[2] == 'jgsbat':
                print(cowsay.cowsay(hello, cowfile=jgsbat))
            else:
                print(cowsay.cowsay(hello, cow=response[2]))
    
    def do_addmon(self, args):
        try:
            x, y, hp, hello, name = add_monster_check(args)
            self.s.sendall(f"addmon {name} {x} {y} {hp} {hello}\n".encode())
            self.response_addmon(name, x, y, hello)
        except Error as e:
            print(e.text)

    def do_attack(self, args):
        try:
            weapon, name = attack_check(args)
            self.s.sendall(f"attack {weapon} {name}\n".encode())
            self.response_attack(name)
        except Error as e:
            print(e.text)
    
    def do_up(self, args):
        if len(args) != 0:
            print(Error(1).text)
        else:
            self.s.sendall(f"move 0 -1\n".encode())
            self.response_move()

    def do_down(self, args):
        if len(args) != 0:
            print(Error(1).text)
        else:
            self.s.sendall(f"move 0 1\n".encode())
            self.response_move()

    def do_left(self, args):
        if len(args) != 0:
            print(Error(1).text)
        else:
            self.s.sendall(f"move -1 0\n".encode())
            self.response_move()

    def do_right(self, args):
        if len(args) != 0:
            print(Error(1).text)
        else:
            self.s.sendall(f"move 1 0\n".encode())
            self.response_move()
    
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
            self.matches = [c for c in cows if c.startswith(text)]
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
    Client_MUD(socket=s).cmdloop()
