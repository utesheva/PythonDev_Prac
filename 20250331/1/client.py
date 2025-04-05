import cmd
import readline
import sys
import socket
import threading
import cowsay
import shlex

cows = cowsay.list_cows() + ['jgsbat']

class Client_MUD(cmd.Cmd):
    prompt = 'MUD> '
    readline.set_completer_delims(readline.get_completer_delims().replace('-', ''))

    def __init__(self, *args, socket, **kwargs):
        self.s = socket
        return super().__init__(*args, **kwargs)
       
    def do_addmon(self, args):
        self.s.sendall(f"addmon {args}\n".encode())

    def do_attack(self, args):
        self.s.sendall(f"attack {args}\n".encode())
    
    def do_up(self, args):
        self.s.sendall(f"move 0 -1\n".encode())

    def do_down(self, args):
        self.s.sendall(f"move 0 1\n".encode())

    def do_left(self, args):
        self.s.sendall(f"move -1 0\n".encode())

    def do_right(self, args):
        self.s.sendall(f"move 1 0\n".encode())

    def default(self, args):
        print("Invalid command")

    def complete_addmon(self, text, line, begidx, endidx):
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
        while response := s.recv(1024).rstrip().decode():
            print(f"\n{response}\n{cmdline.prompt}{readline.get_line_buffer()}", end="", flush=True)

if __name__ == '__main__':
    host = "localhost" if len(sys.argv) < 3 else sys.argv[2]
    port = 1337 if len(sys.argv) < 4 else int(sys.argv[3])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((host, port))
    s.sendall(f"{sys.argv[1]}\n".encode())
    if s.recv(1024).rstrip().decode() == '1':
        print("<<< Welcome to Python-MUD 0.1 >>>")
        print(f"Your login: {sys.argv[1]}")
        cmdline = Client_MUD(socket=s)
        mes = threading.Thread(target=cmdline.from_srv, args=(cmdline, s))
        mes.start()
        cmdline.cmdloop()
    else:
        print("ERROR: Choose another login")
    s.shutdown(socket.SHUT_RDWR)
