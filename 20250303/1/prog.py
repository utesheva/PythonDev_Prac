import cowsay
import re
import sys
from io import StringIO
import shlex

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

    def play(self):
        player = Player()
        while s := sys.stdin.readline():
            s = [int(i) if i.isdigit() else i for i in  shlex.split(s)]
            match s:
                case (["up"] | ["down"] | ["left"] | ["right"]):
                    player.move(s[0], self.size)
                    if (player.x, player.y) in self.monsters:
                        self.encounter(player.x, player.y)

                case (["addmon", str(name), 
                       "hello", str(hello_string), 
                       "hp", int(hitpoints), 
                       "coords", int(x), int(y)]):
                    if x < 0 or x >= self.size or y < 0 or y >= self.size or hitpoints <= 0:
                        print("Invalid arguments")
                    elif name not in cowsay.list_cows() and name != 'jgsbat':
                        print("Cannot add unknown monster")
                    else:
                        print(f"Added monster {name} to ({x}, {y}) saying {hello_string}")
                        if (x,y) in self.monsters:
                            print("Replaced the old monster")
                        self.monsters[(x, y)] = Monster(x, y, name, hello_string, hitpoints)
                case ["addmon", *args]:
                    print("Invalid arguments")
                case _:
                    print("Invalid command")

print("<<< Welcome to Python-MUD 0.1 >>>")
g = Game()
g.play()

