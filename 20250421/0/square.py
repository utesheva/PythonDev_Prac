import sys
import math
import socket

def sqroots(coeffs:str) -> str:
    a, b, c = [float(i) for i in coeffs.split()]
    if a == 0:
        raise Exception
    d = b * b - 4 * a * c
    if d < 0:
        return ''
    if d == 0:
        x1 = (-b) / (2 * a)
        return str(x1)
    x1 = (-b + math.sqrt(d)) / (2 * a)
    x2 = (-b - math.sqrt(d)) / (2 * a)
    return f'{x1}, {x2}'

def sqrootnet(coeffs: str, s: socket.socket) -> str:
    s.sendall((coeffs + "\n").encode())
    return s.recv(128).decode().strip()

if  __name__ == "__main__":
    match sys.argv:
        case [prog, args]:
            print(sqroots(args))
        case [prog, args, host, port]:
             with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                 s.connect((host, int(port)))
                 print(sqrootnet(args, s))
