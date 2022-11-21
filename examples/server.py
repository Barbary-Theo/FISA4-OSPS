import os
import threading
import socket as soc
import config

from multiprocessing import shared_memory
from time import sleep
from random import randint
from datetime import datetime
from rich import console

console = console.Console()


def mkfifo(path):
    try:
        os.mkfifo(path, 0o0600)
    except Exception as e:
        console.print(e.__str__(), style="bold red")


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

            console.print("Serveur 1 doit écrire ->", style="blue")
            text_to_write = input()

            shm_segment1.buf[:len(text_to_write)] = bytearray([ord(value) for value in text_to_write])

            console.print("Serveur 1 a écrit " + text_to_write, style="blue")
            fifo1.write(str(len(text_to_write)) + "\n")

            write_in_file(config.LOG_FILENAME, "a+",
                          get_prefix_log() + "Server 1 wrote in pipe and shared memory text '" + text_to_write + "' with length of " + str(
                              len(text_to_write)) + "\n")

            fifo1.flush()

            text_read = fifo2.readline().replace("\n", "")

            write_in_file(config.LOG_FILENAME, "a+", get_prefix_log() + "Server 1 read '" + text_read + "'\n")

            console.print("Serveur 1 a lu : " + text_read, style="blue")

        except Exception as e:
            write_in_file(config.LOG_FILENAME, "a+", get_prefix_log() + "Server 1 looks like down")


def secondary_server(pathtube1, pathtube2):
    shm_segment2 = shared_memory.SharedMemory("shm_osps")
    rand = randint

    last_message = ""

    while True:

        try:
            fifo1 = open(pathtube1, "r")
            fifo2 = open(pathtube2, "w")

            length = fifo1.readline().replace("\n", "")

            console.print("Serveur 2 a lu la taille : " + length, style="green")
            shared_memory_text = bytes(shm_segment2.buf[:int(length)])

            write_in_file(config.LOG_FILENAME, "a+",
                          get_prefix_log() + "Server 2 read '" + str(shared_memory_text) + "'\n")

            console.print("Contenu du segment mémoire partagée en octets via second accès : " + shared_memory_text.__str__(), style="green")

            sleep(randint(0, config.SERVER_TWO_INTERVAL_CHECKING))

            console.print("Serveur 2 a écrit", style="green")
            fifo2.write("I read\n")

            write_in_file(config.LOG_FILENAME, "a+", get_prefix_log() + "Server 2 wrote 'I read'\n")

            fifo2.flush()

        except Exception:
            write_in_file(config.LOG_FILENAME, "a+", get_prefix_log() + "Server 2 looks like down")


def launch_socket(args):

    s: soc.socket = args

    while True:
        print("oui")

        s.listen()
        conn, addr = s.accept()
        with conn:
            console.print("Connected by " + addr, style="bold red")

            data = conn.recv(1024)
            if data:
                conn.sendall(data)


def join(worker):
    while worker.is_alive():
        worker.join(0.5)


def main():
    to_red = lambda text: "\033[382{}{}{}m{} \033[382255255255m".format(255, 0, 0, text)

    pathtube1 = "/tmp/tubenommeprincipalsecond"
    pathtube2 = "/tmp/tubenommesecondprincipal"

    mkfifo(pathtube1)
    mkfifo(pathtube2)

    try:
        console.print("Création du segment mémoire partagée", style="yellow")
        shared_memory.SharedMemory(name='shm_osps', create=True, size=10)
    except Exception as e:
        console.print(e.__str__(), style="bold red")

    with open("../files/servers.log", "w") as log:
        log.write("")

    try:
        pid = os.fork()
        if pid < 0:
            console.print("⚠️ Error during fork ⚠️", style="bold red")

        elif pid == 0:
            with soc.socket(soc.AF_INET, soc.SOCK_STREAM) as s:
                s.bind((config.SERVER_ONE_IP, config.SERVER_ONE_PORT))

                worker1 = threading.Thread(target=launch_socket, args=[s])
                worker1.daemon = False

                worker1.start()

                main_server(pathtube1, pathtube2)

        else:
            with soc.socket(soc.AF_INET, soc.SOCK_STREAM) as s:
                s.bind((config.SERVER_TWO_IP, config.SERVER_TWO_PORT))

                worker2 = threading.Thread(target=launch_socket, args=[s])
                worker2.daemon = False
                worker2.start()

                secondary_server(pathtube1, pathtube2)

    except Exception as e:
        console.print(e.__str__(), style="bold red")


if __name__ == "__main__":
    main()
