import os, sys
from multiprocessing import shared_memory
from time import sleep
from random import randint

from shm import shm


def mkfifo(path):
    # NE PAS FAIRE, C'EST DÉGEU, MAIS ON A PAS LE CHOIX DU COUP ON LE FAIT
    try:
        os.mkfifo(path, 0o0600)
    except:
        pass


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
            # SERVER PRINCIPALE
            shm_segment1 = shared_memory.SharedMemory("shm_osps")
            rand = randint

            while True:

                try:
                    fifo1 = open(pathtube1, "w")
                    fifo2 = open(pathtube2, "r")

                    shm_segment1.buf[:7] = bytearray([71, 70, 69, 68, 67, 66, 65])

                    fifo1.write("Bonjour\n")
                    sleep(randint(0, 5))
                    fifo1.flush()

                    print(to_red("Principale -> msg : ") + fifo2.readline().replace("\n", " "))
                except Exception as e:
                    break

        else:
            # SERVER SECONDAIRE
            shm_segment2 = shared_memory.SharedMemory("shm_osps")
            rand = randint

            while True:

                try:
                    fifo1 = open(pathtube1, "r")
                    fifo2 = open(pathtube2, "w")

                    shm_segment2.buf[:7] = bytearray([71, 70, 69, 68, 67, 66, 65])

                    fifo2.write("Au revoir\n")
                    sleep(randint(0, 5))
                    fifo2.flush()

                    print(to_red("Secondaire -> msg : ") + fifo1.readline().replace("\n", " "))

                except Exception as e:
                    break

    except Exception as e:
        print(to_red(e.__str__()))


if __name__ == "__main__":
    main()
