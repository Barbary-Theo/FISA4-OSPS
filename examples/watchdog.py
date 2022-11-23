import socket
import sys
import time
import threading

from rich import console
import config

console = console.Console()

error_communication_text = "Impossible de se connecter au serveur "
error_on_a_server = False
style_error = config.COLOR_ERROR


def stop_other_server_text(server_number):
    return "Mise à l'arrêt du serveur " + ("2" if server_number == "1" else "1")


def get_server_style(server_number):
    return "green" if server_number == "1" else "cyan"


def watchdog_server(ip, port, server_number):
    global error_on_a_server

    try:
        s_serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_serv.connect((ip, port))

        while True:

            try:
                s_serv.sendall(config.MESSAGE_PING_ERROR.encode() if error_on_a_server else "ARE U ALIVE".encode())

                if error_on_a_server:
                    sys.exit(1)

                data = s_serv.recv(1024)

                if data.decode().__str__() == "":
                    console.print(error_communication_text + server_number, style=style_error)
                    console.print(stop_other_server_text(server_number), style=style_error)
                    error_on_a_server = True
                    break
                else:
                    console.print("Received data -> " + data.decode().__str__(), style=get_server_style(server_number))

                time.sleep(2)

            except Exception:
                console.print(error_communication_text + server_number, style=style_error)
                console.print(stop_other_server_text(server_number), style=style_error)
                error_on_a_server = True
                break
    except Exception:
        console.print("Impossible de se connecter au socket server " + server_number, style=style_error)
        console.print(stop_other_server_text(server_number), style=style_error)
        error_on_a_server = True


def join(worker):
    while worker.is_alive():
        worker.join(0.5)


def launch_watchdog():

    time.sleep(1)

    worker_server_one = threading.Thread(target=watchdog_server, args=[config.SERVER_ONE_IP, config.SERVER_ONE_PORT, "1"])
    worker_server_one.daemon = True
    worker_server_one.start()

    worker_server_two = threading.Thread(target=watchdog_server, args=[config.SERVER_TWO_IP, config.SERVER_TWO_PORT, "2"])
    worker_server_two.daemon = True
    worker_server_two.start()

    join(worker_server_one)
    join(worker_server_two)


if __name__ == "__main__":
    launch_watchdog()
