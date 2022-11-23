import os
import sys
import threading
import socket as soc
import config

from multiprocessing import shared_memory
from time import sleep
from random import randint
from datetime import datetime
from rich import console

console = console.Console()
style_error = "bold red"

error_on_server_one = False
error_on_server_two = False


def mkfifo(path):
    try:
        os.mkfifo(path, 0o0600)
    except Exception as e:
        console.print(e.__str__(), style=style_error)


def get_prefix_log():
    return "[" + datetime.now().strftime("%X") + "] "


def write_in_file(file_name, mode, text):
    with open(file_name, mode) as state_file:
        state_file.write(text)


def main_server(pathtube1, pathtube2):
    shm_segment1 = shared_memory.SharedMemory("shm_osps")

    while True:

        try:
            fifo1 = open(pathtube1, "w")
            fifo2 = open(pathtube2, "r")

            text_to_write = input("Serveur 1 doit écrire -> ")

            shm_segment1.buf[:len(text_to_write)] = bytearray(text_to_write.encode())

            console.print("Serveur 1 a écrit " + text_to_write, style="blue")
            fifo1.write(str(len(text_to_write)) + "\n")

            fifo1.flush()

            text_read = bytes(fifo2.readline()).decode().replace("\n", "")

            console.print("Serveur 1 a lu : " + text_read, style="blue")

        except Exception:
            break


def secondary_server(pathtube1, pathtube2):
    shm_segment2 = shared_memory.SharedMemory("shm_osps")

    while True:

        try:
            fifo1 = open(pathtube1, "r")
            fifo2 = open(pathtube2, "w")

            length = fifo1.readline().replace("\n", "")

            console.print("Serveur 2 a lu la taille : " + length, style="green")
            shared_memory_text = bytes(shm_segment2.buf[:int(length)])

            console.print(
                "Contenu du segment mémoire partagée en octets via second accès : " + bytes(shared_memory_text).decode(),
                style="green")

            sleep(randint(0, config.SERVER_TWO_INTERVAL_CHECKING))

            console.print("Serveur 2 a écrit", style="green")
            fifo2.write("I read\n")

            fifo2.flush()

        except Exception:
            break


def there_is_error_on_server(server_number, error_on_server_one, error_on_server_two, data):
    return (server_number == "1" and error_on_server_one) \
           or (server_number == "2" and error_on_server_two) \
           or (bytes(data).decode() == config.MESSAGE_PING_ERROR)


def launch_socket(ip, port, server_number):
    global error_on_server_one
    global error_on_server_two

    try:
        with soc.socket(soc.AF_INET, soc.SOCK_STREAM) as s:
            s.bind((ip, port))
            s.listen()
            conn, addr = s.accept()
            console.print("\n Watchdog server " + server_number + " connected by " + addr.__str__(), style=style_error)

            while True:
                try:
                    data = conn.recv(1024)
                    if data:

                        if there_is_error_on_server(server_number, error_on_server_one, error_on_server_two, data):
                           os._exit(0)

                        conn.sendall(str("Server " + server_number + " up").encode())

                except Exception as e:
                    console.print(e.__str__(), style=style_error)
                    conn.close()
                    s.detach()
                    s.close()
                    break
    except Exception as e:
        console.print(e.__str__(), style=style_error)


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
        os.remove(config.LOG_FILENAME)
    except Exception as e:
        console.print(e.__str__(), style=style_error)

    try:
        pid = os.fork()
        if pid < 0:
            console.print("⚠️ Error during fork ⚠️", style=style_error)

        elif pid == 0:
            worker1 = threading.Thread(target=launch_socket, args=[config.SERVER_ONE_IP, config.SERVER_ONE_PORT, "1"])
            worker1.daemon = True
            worker1.start()

            main_server(pathtube1, pathtube2)

            # Si on passe ici ça veut dire qu'il y a eu un problème dans le traitement serveur
            error_on_server_one = True

        else:
            worker2 = threading.Thread(target=launch_socket, args=[config.SERVER_TWO_IP, config.SERVER_TWO_PORT, "2"])
            worker2.daemon = True
            worker2.start()

            secondary_server(pathtube1, pathtube2)

            # Si on passe ici ça veut dire qu'il y a eu un problème dans le traitement serveur
            error_on_server_two = True

    except Exception as e:
        console.print(e.__str__(), style=style_error)


if __name__ == "__main__":
    main()
