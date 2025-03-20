import sys
import asyncio

class Player:
    def __init__(self):
        self.x, self.y = 0, 0

    def move(self, d_x, d_y):
        self.x = (self.x + d_x) % 10
        self.y = (self.y + d_y) % 10
        return f"{self.x} {self.y}"

class Monster:
    def __init__(self, x, y, name, phrase, hitpoints):
        self.x = x
        self.y = y
        self.phrase = phrase
        self.cow = name
        self.hp = hitpoints

class Game:
    def __init__(self):
        self.size = 10
        self.monsters = {}

    def encounter(self, x, y):
        if self.monsters[(x, y)]:
            return f' {self.monsters[(x, y)].cow} {self.monsters[(x, y)].phrase}'
        return ''

    def moving(self, player, d_x, d_y):
        s = player.move(d_x, d_y)
        if (player.x, player.y) in self.monsters:
            s += self.encounter(player.x, player.y)
        print(s)
        return s

    def add_monster(self, x, y, hp, hello, name):
        replaced = "0"
        if (x,y) in self.monsters and not(self.monsters[(x,y)] is None):
            replaced = "1"
        self.monsters[(x, y)] = Monster(x, y, name, hello, hp)
        return replaced

    def attack(self, x, y, weapon, name):
        if ((x, y) not in self.monsters or
            self.monsters[(x, y)] is None or
            self.monsters[(x, y)].cow != name):
            return 'no'
        damage = min(self.monsters[(x, y)].hp, weapon)
        self.monsters[(x, y)].hp = self.monsters[(x, y)].hp - damage
        if self.monsters[(x, y)].hp == 0:
            self.monsters[(x, y)] = None
            return f'{damage} 0'
        return f'{damage} {self.monsters[(x, y)].hp}'

async def echo(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    game = Game()
    player = Player()

    queue = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(queue.get())

    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for request in done:
            if request is send:
                send = asyncio.create_task(reader.readline())
                match request.result().decode().split():
                    case ['addmon', *args]:
                        name, x, y, hp = args[:4]
                        hello = ' '.join(args[5:])
                        writer.write(game.add_monster(int(x), int(y), int(hp), hello, name).encode())
                    case ['attack', *args]:
                        x, y = player.x, player.y
                        weapon, name = args
                        writer.write(game.attack(x, y, int(weapon), name).encode())
                    case ['move', *args]:
                        d_x, d_y = [int(i) for i in args]
                        writer.write(game.moving(player, d_x, d_y).encode())
            if request is receive:
                receive = asyncio.create_task(my_queue.get())

    send.cancel()
    receive.cancel()
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
