import asyncio
import websockets
import pyautogui
import struct

pyautogui.FAILSAFE = False

IP = "192.168.100.4"
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
        )  # Unpack 2 signed 16-bit integers (little-endian)

        # Now you have the integers
        x = ints[0] / 100
        y = ints[1] / 100
        print(f"Cursor position: {x}, {y}")
        pyautogui.moveRel(x, y, _pause=False)


def main():
    start_server = websockets.serve(echo, IP, PORT)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
