import cowsay
import re
import sys

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
    def __init__(self, x, y, phrase):
        self.x = x
        self.y = y
        self.phrase = phrase

    def say(self):
        print(cowsay.cowsay(self.phrase))

class Game:
    def __init__(self):
        self.size = 10
        self.monsters = {}

    def encounter(self, x, y):
        self.monsters[(x,y)].say()

    def play(self):
        player = Player()
        while s := sys.stdin.readline():
            s = s[:-1]
            match s:
                case ("up" | "down" | "left" | "right"):
                    player.move(s, self.size)
                    if (player.x, player.y) in self.monsters:
                        self.encounter(player.x, player.y)
                case x if x.split()[0] == "addmon":
                    if not re.match(r"addmon \d+ \d+ .*", s):
                        print("Invalid arguments")
                    _, x, y, phrase = s.split()
                    x, y = int(x), int(y)
                    if x < 0 or x >= self.size or y < 0 or y >= self.size:
                        print("Invalid arguments")
                    else:
                        print(f"Added monster to ({x}, {y}) saying {phrase}")
                        if (x,y) in self.monsters: 
                            print("Replaced the old monster")
                        self.monsters[(x, y)] = Monster(x, y, phrase)
                case _:
                    print("Invalid command")

g = Game()
g.play()
