import socket
import time

from rich import console
import config

console = console.Console()


def prog():

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((config.SERVER_ONE_IP, config.SERVER_ONE_PORT))

            while True:

                s.sendall("Hello, world".encode())
                data = s.recv(1024)

                print("Received data -> " + data.decode().__str__())

                time.sleep(2)

    except Exception as e:
        if e.__str__().__contains__("Connection refused"):
            console.print("Impossible de se connecter au socket", style="red")
        else:
            print(e.__str__())
            console.print("socket error", style="red")


if __name__ == "__main__":
    prog()
