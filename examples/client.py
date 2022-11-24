import socket as socket
import config

from rich import console

console = console.Console()
style_error = config.COLOR_ERROR

to_serv_two = None


# Connexion au serveur 2 après interrogation du serveur 1
def client_serv_two(server):

    global to_serv_two

    try:
        # Connexion si elle n'a pas déjà été faite
        if to_serv_two is None:
            to_serv_two = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            to_serv_two.connect((server[0], int(server[1])))

        while True:

            try:
                # Texte à envoyer au serveur 2
                text_to_send = input("Qu'envoyer au server 2 (STOP pour quitter) -> ")

                # Arrêt en indiquant "STOP"
                if text_to_send.upper() == "STOP":
                    break

                # Envoie du message
                to_serv_two.sendall(text_to_send.encode())
                data = to_serv_two.recv(1024)
                print(data.decode())

            except Exception:
                console.print("Impossible d'envoyer le message au server 2", style=style_error)

    except Exception:
        console.print("Impossible de se connecter au server 2")


# Connexion au serveur 1
def client_serv_one():
    try:

        # Connexion au serveur 1
        to_serv_one = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        to_serv_one.connect((config.SERVER_ONE_CLIENT_IP, config.SERVER_ONE_CLIENT_PORT))

        while True:
            # Texte à envoyer au serveur 1
            text_serv_one = input("Bienvenu sur le serveur 1, écrivez STOP pour quitter -> ")

            # Arrêt en indiquant "STOP"
            if text_serv_one.upper() == "STOP":
                break

            try:
                # Envoie du message
                to_serv_one.send("Give me server address and port".encode())
                data = to_serv_one.recv(1024)

                # Récupération des informations de connexion au serveur 2
                server_informations = data.decode().split(" ")
                print(server_informations)

                # Connexion au serveur 2
                client_serv_two(server_informations)

            except Exception:
                console.print("Impossible d'envoyer le message au server 1", style=style_error)

    except Exception:
        console.print("Impossible de se connecter au server 1", style=style_error)


if __name__ == "__main__":
    client_serv_one()
