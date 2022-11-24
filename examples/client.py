import socket as socket
import config

from rich import console

console = console.Console()
style_error = config.COLOR_ERROR


to_serv_two = None


def client_serv_two(server):

    global to_serv_two

    try:
        if to_serv_two is None:
            to_serv_two = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            to_serv_two.connect((server[0], int(server[1])))

        while True:

            try:
                text_to_send = input("Qu'envoyer au server 2 (STOP pour quitter) -> ")

                if text_to_send.upper() == "STOP":
                    break

                to_serv_two.sendall(text_to_send.encode())
                data = to_serv_two.recv(1024)
                print(data.decode())

            except Exception:
                console.print("Impossible d'envoyer le message au server 2", style=style_error)

    except Exception:
        console.print("Impossible de se connecter au server 2")


def client_serv_one():
    try:

        to_serv_one = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        to_serv_one.connect((config.SERVER_ONE_CLIENT_IP, config.SERVER_ONE_CLIENT_PORT))

        while True:

            text_serv_one = input("Bienvenu sur le serveur 1, écrivez STOP pour quitter -> ")

            if text_serv_one.upper() == "STOP":
                break

            try:
                to_serv_one.send("Give me server address and port".encode())
                data = to_serv_one.recv(1024)

                server_informations = data.decode().split(" ")
                print(server_informations)

                client_serv_two(server_informations)

            except Exception:
                console.print("Impossible d'envoyer le message au server 1", style=style_error)

    except Exception:
        console.print("Impossible de se connecter au server 1", style=style_error)


if __name__ == "__main__":
    client_serv_one()
