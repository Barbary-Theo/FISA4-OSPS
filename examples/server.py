import os
from multiprocessing import shared_memory
from time import sleep
from random import randint
from datetime import datetime

def mkfifo(path):
    try:
        os.mkfifo(path, 0o0600)
    except:
        pass


def get_prefix_log():
    return "[" + datetime.now().strftime("%X") + "] "

def main_server(pathtube1, pathtube2):
    shm_segment1 = shared_memory.SharedMemory("shm_osps")

    while True:

        try:
            fifo1 = open(pathtube1, "w")
            fifo2 = open(pathtube2, "r")

            text_to_write = input("Server 1 have to write -> ")

            shm_segment1.buf[:len(text_to_write)] = bytearray([ord(value) for value in text_to_write])

            print("Serveur 1 a écrit")
            fifo1.write(str(len(text_to_write)) + "\n")

            with open("servers.log", "a+") as log:
                log.write(get_prefix_log() + "Server 1 wrote in pipe and shared memory text '" + text_to_write + "' with length of " + str(len(text_to_write)) + "\n")

            fifo1.flush()

            text_read = fifo2.readline().replace("\n", "")

            with open("servers.log", "a+") as log:
                log.write(get_prefix_log() + "Server 1 read '" + text_read + "'\n")

            print("Serveur 1 à lu : ",  text_read)

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
            shared_memory_text = bytes(shm_segment2.buf[:int(length)])

            with open("servers.log", "a+") as log:
                log.write(get_prefix_log() + "Server 2 read '" + str(shared_memory_text) + "'\n")

            print('Contenu du segment mémoire partagée en octets via second accès :', shared_memory_text)

            sleep(randint(0, 5))

            print("Serveur 2 a écrit")
            fifo2.write("I read\n")

            with open("servers.log", "a+") as log:
                log.write(get_prefix_log() + "Server 2 wrote 'I read'\n")

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
        shared_memory.SharedMemory(name='shm_osps', create=True, size=10)
    except Exception as e:
        print(to_red(e.__str__()))

    with open("servers.log", "w") as log:
        log.write("")

    try:
        pid = os.fork()
        if pid < 0:
            print("⚠️ Error during fork ⚠️")

        elif pid == 0:
            main_server(pathtube1, pathtube2)

        else:
            secondary_server(pathtube1, pathtube2)

    except Exception as e:
        print(to_red(e.__str__()))


if __name__ == "__main__":
    main()
