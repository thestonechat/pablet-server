import asyncio
import websockets
import pyautogui
import struct
import socket

pyautogui.FAILSAFE = False


def get_local_ip(interface="Wi-Fi"):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(("10.255.255.255", 1))
        IP = s.getsockname()[0]
    except:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP


IP = get_local_ip()
PORT = 3244


async def echo(websocket, path):
    async for message in websocket:
        if type(message) == str:
            if message == "1":
                pyautogui.click(_pause=False)
            elif message == "2":
                pyautogui.rightClick(_pause=False)

            continue

        ints = struct.unpack(
            "<2h", message
        )  # Unpack 2 signed 16-bit integers (4 bytes)

        # floating points are multiplied by 100 and turned into ints so we can keep the 2 decimal precision while lowering the sent data size for extra efficiency
        x = ints[0] / 100
        y = ints[1] / 100

        print(f"Cursor position: {x}, {y}")
        pyautogui.moveRel(x, y, _pause=False)


def main():
    start_server = websockets.serve(echo, IP, PORT)

    print(f"Server started at ws://{IP}:{PORT}")

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
