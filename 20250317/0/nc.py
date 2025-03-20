import sys
import socket
import cmd

class client(cmd.Cmd):
    prompt = '>'
    host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
    port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])

    def __init__(self, *ap, socket=None, **kwargs):
        self.socket = socket
        super.__init__(*ap, **kwargs)
    
    def response(self):
        print(self.s.recv(1024).rstrip().decode())

    def do_print(self, args):
        self.socket.sendall(f"print {args}\n".encode())
        self.response()

    def do_info(self, args):
        self.socket.sendall(f"info {args}\n".encode()) 
        self.response()

    def complete_info(self, text, line, begidx, endidx):
        return [c for c in ['host', 'port'] if c.startswith(text)]


if __name__ == '__main__':
    cient().cmdloop()
