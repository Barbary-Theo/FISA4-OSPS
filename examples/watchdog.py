import socket
from rich import console
import config

console = console.Console()


def prog():

    HOST = config.SERVER_ONE_IP  # The server's hostname or IP address
    PORT = config.SERVER_ONE_PORT # The port used by the server

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((config.SERVER_ONE_IP, config.SERVER_ONE_PORT))

            while True:

                s.sendall(b"Hello, world")
                data = s.recv(1024)

                print(f"Received {data!r}")
    except Exception as e:
        print(e.__str__())
        console.print("Impossible de se connecter au socket", style="red")


if __name__ == "__main__":
    prog()
