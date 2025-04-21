import asyncio
import square

async def echo(reader, writer):
    while data := await reader.readline():
        res = data.strip().decode()
        try:
            sol = square.sqroots(res)
            writer.write(f"{sol}\n".encode())
        except Exception:
            writer.write("\n".encode())
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
