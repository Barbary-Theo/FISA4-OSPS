import os
import sys
import threading
import socket as soc
import config

import random
import string

from multiprocessing import shared_memory
from time import sleep
from random import randint
from datetime import datetime
from rich import console

console = console.Console()
style_error = config.COLOR_ERROR
color_server_one = config.COLOR_SERVER_ONE
color_server_two = config.COLOR_SERVER_TWO

error_on_server_one = False
error_on_server_two = False


def mkfifo(path):
    try:
        os.mkfifo(path, 0o0600)
    except Exception as e:
        console.print(e.__str__(), style=style_error)


def get_prefix_log():
    return "[" + datetime.now().strftime("%X") + "] "


def main_server(pathtube1, pathtube2):
    shm_segment1 = shared_memory.SharedMemory("shm_osps")

    fifo1 = None
    fifo2 = None

    while True:

        try:
            fifo1 = open(pathtube1, "w")
            fifo2 = open(pathtube2, "r")

            sleep(randint(0, config.SERVER_ONE_INTERVAL_CHECKING))

            text_to_write = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

            shm_segment1.buf[:len(text_to_write)] = bytearray(text_to_write.encode('utf-8'))

            console.print("Serveur 1 a écrit", style=color_server_one)
            fifo1.write(str(len(text_to_write)) + "\n")

            fifo1.flush()

            text_read = fifo2.readline().replace("\n", "")

            console.print("Serveur 1 à lu : " + text_read, style=color_server_one)

        except Exception:
            fifo1.close()
            fifo2.close()
            shm_segment1.unlink()
            shm_segment1.close()
            break


def secondary_server(pathtube1, pathtube2):
    shm_segment2 = shared_memory.SharedMemory("shm_osps")

    fifo1 = None
    fifo2 = None

    while True:

        try:
            fifo1 = open(pathtube1, "r")
            fifo2 = open(pathtube2, "w")

            length = fifo1.readline().replace("\n", "")

            console.print("Serveur 2 à lu la taille : " + str(length), style=color_server_two)
            shared_memory_text = bytes(shm_segment2.buf[:int(length)])

            console.print('Contenu du segment mémoire partagée en octets via second accès : ' + shared_memory_text.decode(), style=color_server_two)

            sleep(randint(0, config.SERVER_TWO_INTERVAL_CHECKING))

            console.print("Serveur 2 a écrit", style=color_server_two)
            fifo2.write(''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + "\n")

            fifo2.flush()

        except Exception:
            fifo1.close()
            fifo2.close()
            shm_segment2.unlink()
            shm_segment2.close()
            break


def there_is_error_on_server(server_number, error_server_one, error_server_two, data):
    return (server_number == "1" and error_server_one) \
           or (server_number == "2" and error_server_two) \
           or (bytes(data).decode() == config.MESSAGE_PING_ERROR)


def launch_socket_for_watchdog(ip, port, server_number):
    global error_on_server_one
    global error_on_server_two

    try:
        with soc.socket(soc.AF_INET, soc.SOCK_STREAM) as s:
            s.bind((ip, port))
            s.listen()
            conn, addr = s.accept()
            console.print("\n Watchdog server " + server_number + " connected by " + addr.__str__(), style="yellow")

            while True:
                try:
                    data = conn.recv(1024)
                    if data:

                        if there_is_error_on_server(server_number, error_on_server_one, error_on_server_two, data):
                            shared_memory.ShareableList.shm.unlink()
                            shared_memory.ShareableList.shm.close()
                            sys.exit(1)

                        conn.sendall(str("Server " + server_number + " up").encode())

                except Exception as e:
                    console.print(e.__str__(), style=style_error)
                    conn.close()
                    s.detach()
                    s.close()
                    break
    except Exception as e:
        console.print(e.__str__(), style=style_error)


def socket_with_client():
    try:
        with soc.socket(soc.AF_INET, soc.SOCK_STREAM) as s:
            s.bind((config.SERVER_ONE_CLIENT_IP, config.SERVER_ONE_CLIENT_PORT))
            s.listen()
            conn, addr = s.accept()
            console.print("\n Client connected on server 1 by " + addr.__str__(), style="yellow")

            while True:
                try:
                    data = conn.recv(1024)
                    if data:
                        conn.sendall((str(config.SERVER_TWO_CLIENT_IP) + " " + str(config.SERVER_TWO_CLIENT_PORT)).encode())

                except Exception as e:
                    console.print(e.__str__(), style=style_error)
                    conn.close()
                    s.detach()
                    s.close()
                    break
    except Exception as e:
        console .print(e.__str__(), style=style_error)


def socket_server_2_with_client():
    try:
        with soc.socket(soc.AF_INET, soc.SOCK_STREAM) as s:
            s.bind((config.SERVER_TWO_CLIENT_IP, config.SERVER_TWO_CLIENT_PORT))
            s.listen()
            conn, addr = s.accept()
            console.print("\n Client connected on server 2 by " + addr.__str__(), style="yellow")

            while True:
                try:
                    data = conn.recv(1024)
                    if data:
                        conn.sendall("J'ai rien à te dire ...".encode())

                except Exception as e:
                    console.print(e.__str__(), style=style_error)
                    conn.close()
                    s.detach()
                    s.close()

    except Exception as e:
        console .print(e.__str__(), style=style_error)


def main():
    global error_on_server_one
    global error_on_server_two

    pathtube1 = "/tmp/tubenommeprincipalsecond"
    pathtube2 = "/tmp/tubenommesecondprincipal"

    mkfifo(pathtube1)
    mkfifo(pathtube2)

    try:
        console.print("Création du segment mémoire partagée", style="yellow")
        shared_memory.SharedMemory(name='shm_osps', create=True, size=10)
    except Exception as e:
        console.print(e.__str__(), style=style_error)

    try:
        pid = os.fork()
        if pid < 0:
            console.print("⚠️ Error during fork ⚠️", style=style_error)

        elif pid == 0:
            worker_watchdog = threading.Thread(target=launch_socket_for_watchdog, args=[config.SERVER_ONE_IP, config.SERVER_ONE_PORT, "1"])
            worker_watchdog.daemon = False
            worker_watchdog.start()

            worker_client = threading.Thread(target=socket_with_client, args=[])
            worker_client.daemon = False
            worker_client.start()

            main_server(pathtube1, pathtube2)

            # Si on passe ici ça veut dire qu'il y a eu un problème dans le traitement serveur
            error_on_server_one = True

        else:
            worker2 = threading.Thread(target=launch_socket_for_watchdog, args=[config.SERVER_TWO_IP, config.SERVER_TWO_PORT, "2"])
            worker2.daemon = False
            worker2.start()

            worker_client = threading.Thread(target=socket_server_2_with_client, args=[])
            worker_client.daemon = False
            worker_client.start()

            secondary_server(pathtube1, pathtube2)

            # Si on passe ici ça veut dire qu'il y a eu un problème dans le traitement serveur
            error_on_server_two = True

    except Exception as e:
        console.print(e.__str__(), style=style_error)


if __name__ == "__main__":
    main()
