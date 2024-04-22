import asyncio
import websockets
import pyautogui
import struct
import socket
from threading import Thread
import gui

pyautogui.FAILSAFE = False


def get_local_ip():
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

server = None
serve = None

gui.local_ip = IP


async def echo(websocket, path):
    gui.has_connection = True

    try:
        async for message in websocket:
            if type(message) == str:
                if message == "1":
                    pyautogui.click(_pause=False)
                    gui.last_message = "left click"
                elif message == "2":
                    pyautogui.rightClick(_pause=False)
                    gui.last_message = "right click"

                continue

            ints = struct.unpack(
                "<2h", message
            )  # Unpack 2 signed 16-bit integers (4 bytes)

            # floating points are multiplied by 100 and turned into ints so we can keep the 2 decimal precision while lowering the sent data size for extra efficiency
            x = ints[0] / 100
            y = ints[1] / 100

            print(f"Cursor position: {x}, {y}")
            pyautogui.moveRel(x, y, _pause=False)

            gui.last_message = f"{x}, {y}"
    except:
        gui.has_connection = False
        print("Connection lost")

    gui.has_connection = False
    print("Connection closed")


def start_server():
    global server, serve
    serve = websockets.serve(echo, IP, PORT)
    server = asyncio.get_event_loop().run_until_complete(serve)

    print(f"Server started at ws://{IP}:{PORT}")

    return server


def close_server(loop=None):
    global server, serve
    # if server:
    #     server.close()
    #     asyncio.get_event_loop().run_until_complete(server.wait_closed())
    #     print("Server closed")

    if serve:
        # serve.close()
        # asyncio.get_event_loop().run_until_complete(serve.wait_closed())
        # print("Server closed")
        loop.stop()


def main():
    server = start_server()
    gui.is_running = True

    gui_thread = Thread(target=gui.gui, args=())
    gui_thread.start()

    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass

    close_server(asyncio.get_event_loop())


if __name__ == "__main__":
    main()
