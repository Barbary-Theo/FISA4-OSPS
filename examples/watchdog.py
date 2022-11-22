import socket
import time
import threading

from rich import console
import config

console = console.Console()

error_communication_text = "Impossible de se connecter au serveur "

def watchdog_server_one(ip, port):

    try:
        s_serv_one = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_serv_one.connect((ip, port))

        while True:

            try:
                s_serv_one.sendall("Hello, world".encode())
                data = s_serv_one.recv(1024)

                if data.decode().__str__() == "":
                    console.print(error_communication_text + "1", style="red")
                    break
                else:
                    print("Received data -> " + data.decode().__str__())

                time.sleep(2)

            except Exception:
                console.print(error_communication_text + "1", style="red")
                break
    except Exception:
        console.print("Impossible de se connecter au socket server 1", style="red")


def watchdog_server_two(ip, port):

    try:
        s_serv_two = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_serv_two.connect((ip, port))

        while True:

            try:
                s_serv_two.sendall("Hello, world".encode())
                data = s_serv_two.recv(1024)

                if data.decode().__str__() == "":
                    console.print(error_communication_text + "2", style="red")
                    break
                else:
                    print("Received data -> " + data.decode().__str__())

                time.sleep(2)

            except Exception:
                console.print(error_communication_text + "2", style="red")
                break
    except Exception:
        console.print("Impossible de se connecter au socket server 2", style="red")


def join(worker):
    while worker.is_alive():
        worker.join(0.5)


def launch_watchdog():

    time.sleep(1)

    worker_server_one = threading.Thread(target=watchdog_server_one, args=[config.SERVER_ONE_IP, config.SERVER_ONE_PORT])
    worker_server_one.daemon = True
    worker_server_one.start()

    worker_server_two = threading.Thread(target=watchdog_server_two, args=[config.SERVER_TWO_IP, config.SERVER_TWO_PORT])
    worker_server_two.daemon = True
    worker_server_two.start()

    join(worker_server_one)
    join(worker_server_two)


if __name__ == "__main__":
    launch_watchdog()
