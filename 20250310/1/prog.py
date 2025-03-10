import cowsay
import re
import sys
from io import StringIO
import shlex
import cmd

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

class Player:
    def __init__(self):
        self.x, self.y = 0, 0

    def move(self, direction, size):
        match direction:
            case "up":
                self.y = (self.y - 1) if self.y > 0 else (size - 1)
            case "down":
                self.y = (self.y + 1) if self.y < (size - 1) else 0
            case "left":
                self.x = (self.x - 1) if self.x > 0 else (size - 1)
            case "right":
                self.x = (self.x + 1) if self.x < (size - 1) else 0
        print(f"Moved to ({self.x}, {self.y})")

class Monster:
    def __init__(self, x, y, name, phrase, hitpoints):
        self.x = x
        self.y = y
        self.phrase = phrase
        self.cow = name
        self.hp = hitpoints

    def say(self):
        if self.cow == 'jgsbat':
            print(cowsay.cowsay(self.phrase, cowfile=jgsbat))
        else:
            print(cowsay.cowsay(self.phrase, cow=self.cow))

class Game:
    def __init__(self):
        self.size = 10
        self.monsters = {}

    def encounter(self, x, y):
        self.monsters[(x,y)].say()

    def parse_args(self, args, param):
        args_parsed = {}
        cur = ''
        for i in param:
            if i not in args:
                return None
            args_parsed[i] = args[args.index(i) + 1: args.index(i) + 1 + param[i]]
        return args_parsed

    def moving(self, player, direction):
        player.move(direction, self.size)
        if (player.x, player.y) in self.monsters:
            self.encounter(player.x, player.y)

    def play(self):
        player = Player()
        while s := sys.stdin.readline():
            s = [int(i) if i.isdigit() else i for i in  shlex.split(s)]
            match s:
                case (["up"] | ["down"] | ["left"] | ["right"]):
                    self.moving(player, s[0])
                case ["addmon", str(name), *args]:
                    parsed_args = self.parse_args(args, {"hello": 1, "hp": 1, "coords": 2})
                    if parsed_args:
                        x, y = parsed_args['coords']
                        hello_string = parsed_args['hello'][0]
                        hitpoints = parsed_args['hp'][0]
                        if x < 0 or x >= self.size or y < 0 or y >= self.size or hitpoints <= 0:
                            print("Invalid arguments")
                        elif name not in cowsay.list_cows() and name != 'jgsbat':
                            print("Cannot add unknown monster")
                        else:
                            print(f"Added monster {name} to ({x}, {y}) saying {hello_string}")
                            if (x,y) in self.monsters:
                                print("Replaced the old monster")
                            self.monsters[(x, y)] = Monster(x, y, name, hello_string, hitpoints)
                    else:
                        print('Invalid arguments')
                case ["addmon", *args]:
                    print("Invalid arguments")
                case _:
                    print("Invalid command")

print("<<< Welcome to Python-MUD 0.1 >>>")
g = Game()
g.play()
