import os, sys
import random
from multiprocessing import shared_memory
from time import sleep
from random import randint

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from shm import shm


def mkfifo(path):
    try:
        os.mkfifo(path, 0o0600)
    except:
        pass


def main_server(pathtube1, pathtube2):
    shm_segment1 = shared_memory.SharedMemory("shm_osps")
    rand = randint

    random_text = ["mot", "sus", "BEANSS", "Python", "cheval"]

    while True:

        try:
            fifo1 = open(pathtube1, "w")
            fifo2 = open(pathtube2, "r")

            text_to_write = input("Server 1 have to write -> ")

            shm_segment1.buf[:len(text_to_write)] = bytearray([ord(value) for value in text_to_write])

            print("Serveur 1 a écrit")
            fifo1.write(str(len(text_to_write)) + "\n")
            fifo1.flush()

            print("Serveur 1 à lu : ",  fifo2.readline().replace("\n", ""))

        except Exception as e:
            break


def secondary_server(pathtube1, pathtube2):

    shm_segment2 = shared_memory.SharedMemory("shm_osps")
    rand = randint

    last_message = ""

    while True:

        try:
            fifo1 = open(pathtube1, "r")
            fifo2 = open(pathtube2, "w")

            length = fifo1.readline().replace("\n", "")

            print("Serveur 2 à lu la taille : ", length)
            print('Contenu du segment mémoire partagée en octets via second accès :', bytes(shm_segment2.buf[:int(length)]))

            sleep(randint(0, 5))

            print("Serveur 2 a écrit")
            fifo2.write("I read\n")
            fifo2.flush()

        except Exception as e:
            break


def main():
    to_red = lambda text: "\033[382{}{}{}m{} \033[382255255255m".format(255, 0, 0, text)

    pathtube1 = "/tmp/tubenommeprincipalsecond"
    pathtube2 = "/tmp/tubenommesecondprincipal"

    mkfifo(pathtube1)
    mkfifo(pathtube2)

    try:
        print("Création du segment mémoire partagée")
        shm()
    except Exception as e:
        print(to_red(e.__str__()))

    try:
        pid = os.fork()
        if pid < 0:
            print("It's not possible to fork() !")

        elif pid == 0:
            main_server(pathtube1, pathtube2)

        else:
            secondary_server(pathtube1, pathtube2)

    except Exception as e:
        print(to_red(e.__str__()))


if __name__ == "__main__":
    main()
