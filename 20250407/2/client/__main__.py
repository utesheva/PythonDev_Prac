import cmd
import readline
import sys
import socket
import threading
import cowsay
import shlex
import time

cows = cowsay.list_cows() + ['jgsbat']


class Client_MUD(cmd.Cmd):
    """Cmd string to work with user"""
    prompt = 'MUD> '
    readline.set_completer_delims(readline.get_completer_delims().replace('-', ''))

    def __init__(self, *args, socket, **kwargs):
        """
        Initialize connection

        socket:socket
        """
        self.s = socket
        return super().__init__(*args, **kwargs)

    def precmd(self, line):
        time.sleep(1)
        return super().precmd(line)

    def do_addmon(self, args):
        """
        Add monster

        Addmon {name} coords {x} {y} hp {hp} hello {hello}

        named parameters could be in any order
        x:int first coordinate
        y:int second coordinate
        hp:int number of hitpoints
        hello:str phrase to be said by monster
        name:str name of the monster
        """
        self.s.sendall(f"addmon {args}\n".encode())

    def do_attack(self, args):
        """
        Attack monster

        Attack {name} with {weapon}

        weapon: sword, spear or axe
        name: name of the monster to be attacked
        """
        self.s.sendall(f"attack {args}\n".encode())

    def do_up(self, args):
        """Move up"""
        self.s.sendall("move 0 -1\n".encode())

    def do_down(self, args):
        """Move down"""
        self.s.sendall("move 0 1\n".encode())

    def do_left(self, args):
        """Move left"""
        self.s.sendall("move -1 0\n".encode())

    def do_right(self, args):
        """Move right"""
        self.s.sendall("move 1 0\n".encode())

    def do_sendall(self, args):
        """
        Send message to all users

        args:str message
        """
        self.s.sendall(f"sendall {args}\n".encode())

    def do_EOF(self, args):
        return 1
    def emptyline(self):
        return 

    def default(self, args):
        """Process any other commands"""
        print("Invalid command")

    def complete_addmon(self, text, line, begidx, endidx):
        """Complete addmon command"""
        words = shlex.split(line[:endidx] + ".")
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
        """Complete attack command"""
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

    def from_srv(self, cmdline, s):
        """
        Print all messages from the server

        cmdline:Client_MUD
        s:socket
        """
        while response := s.recv(1024).rstrip().decode():
            print(f"\n{response}\n{cmdline.prompt}{readline.get_line_buffer()}", end="", flush=True)


if __name__ == '__main__':
    if sys.argv[2] == '--file' and len(sys.argv) > 3:
        file = open(sys.argv[3])
    else:
        file = None
    host = "localhost"
    port = 1337
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((host, port))
    s.sendall(f"{sys.argv[1]}\n".encode())
    if s.recv(1024).rstrip().decode() == '1':
        print("<<< Welcome to Python-MUD 0.1 >>>")
        print(f"Your login: {sys.argv[1]}")
        if file is None:
            cmdline = Client_MUD(socket=s)
        else:
            cmdline = Client_MUD(socket=s, stdin=file)
            cmdline.prompt = ''
            cmdline.use_rawinput = False
        mes = threading.Thread(target=cmdline.from_srv, args=(cmdline, s))
        mes.start()
        cmdline.cmdloop()
    else:
        print("ERROR: Choose another login")
    s.shutdown(socket.SHUT_RDWR)
    if file:
        file.close()
