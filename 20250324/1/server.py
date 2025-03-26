import sys
import asyncio
import cowsay
from io import StringIO
import shlex

COWS = cowsay.list_cows() + ['jgsbat']

JGSBAT = cowsay.read_dot_cow(StringIO(r"""
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\\\--//|.'-._  (
     )'   .'\/o\/o\/'.   `(
      ) .' . \====/ . '. (
       )  / <<    >> \  (
        '-._/``  ``\_.-'
  jgs    __\\\'--'//__
         (((""`  `"")))
"""))

class Error(BaseException):
    def __init__(self, code, name = ''):
        match code:
            case 1:
                self.text = "Invalid arguments"
            case 2:
                self.text = "Cannot add unknown monster"
            case 3:
                self.text = f"No {name} here"
            case 4:
                self.text = "Unknown weapon"


class Player:
    def __init__(self):
        self.x, self.y = 0, 0

    def move(self, d_x, d_y):
        self.x = (self.x + d_x) % 10
        self.y = (self.y + d_y) % 10
        return f"Moved to ({self.x}, {self.y})"


class Monster:
    def __init__(self, x, y, name, phrase, hitpoints):
        self.x = x
        self.y = y
        self.phrase = phrase
        self.cow = name
        self.hp = hitpoints

    def say(self):
        if self.cow == 'jgsbat':
            return cowsay.cowsay(self.phrase, cowfile=jgsbat)
        else:
            return cowsay.cowsay(self.phrase, cow=self.cow)

class Game:
    def __init__(self):
        self.size = 10
        self.monsters = {}

    def encounter(self, x, y):
        if self.monsters[(x, y)]:
            return self.monsters[(x, y)].say()
        return ''

    def moving(self, player, d_x, d_y):
        s = player.move(d_x, d_y)
        if (player.x, player.y) in self.monsters:
            s += self.encounter(player.x, player.y)
        return s

    def add_monster(self, x, y, hp, hello, name):
        ans = f"Added monster {name} to ({x}, {y}) saying {hello}\n"
        if (x,y) in self.monsters and not(self.monsters[(x,y)] is None):
            ans += "Replaced the old monster\n"
        self.monsters[(x, y)] = Monster(x, y, name, hello, hp)
        return ans

    def attack(self, x, y, weapon, name):
        if ((x, y) not in self.monsters or
            self.monsters[(x, y)] is None or
            self.monsters[(x, y)].cow != name):
            return 'no'
        damage = min(self.monsters[(x, y)].hp, weapon)
        self.monsters[(x, y)].hp = self.monsters[(x, y)].hp - damage
        ans = f"Attacked {self.monsters[(x, y)].cow}, damage {damage} hp"
        if self.monsters[(x, y)].hp == 0:
            self.monsters[(x, y)] = None
            ans += f"{self.monsters[(x, y)].cow} died"
        else:
            ans += f"{self.monsters[(x, y)].cow} now has {self.monsters[(x, y)].hp}"
        return ans


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
    if name not in COWS:
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
    if len(args) == 0 or splitted[0] not in COWS:
        raise Error(1)
    name = splitted[0]
    return weapon, name

async def echo(reader, writer):
    global game, players

    queue = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(queue.get())

    await asyncio.wait_for(send, timeout=None)
    login = send.result().decode()[:-1]
    if login in players:
        writer.write('0'.encode())
        writer.close()
        send.cancel()
        receive.cancel()
        await writer.wait_closed()
        return
    else:
        players[login] = Player()
        writer.write(f"1".encode())


    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(login, me)

    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for request in done:
            if request is send:
                send = asyncio.create_task(reader.readline())
                match request.result().decode().split(maxsplit=1):
                    case ['addmon', args]:
                        try:
                            x, y, hp, hello, name = add_monster_check(args)
                        except Error as e:
                            writer.write(e.text.encode())
                            continue
                        writer.write(game.add_monster(int(x), int(y), int(hp), hello, name).encode())
                    case ['attack', args]:
                        try:
                            weapon, name = attack_check(args)
                        except Error as e:
                            writer.write(e.text.enode())
                            continue
                        x, y = players[login].x, players[login].y
                        writer.write(game.attack(x, y, int(weapon), name).encode())
                    case ['move', args]:
                        d_x, d_y = [int(i) for i in args.split()]
                        writer.write(game.moving(players[login], d_x, d_y).encode())
            if request is receive:
                receive = asyncio.create_task(my_queue.get())

    send.cancel()
    receive.cancel()
    writer.close()
    print(login, "LEFT")
    del players[login]
    await writer.wait_closed()

async def main():
    global game, players
    game = Game()
    players = {}
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
