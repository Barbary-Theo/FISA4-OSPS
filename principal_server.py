import os, sys
from multiprocessing import shared_memory
from time import sleep
from random import randint


def prog_server_principal():
    to_red = lambda text: "\033[382{}{}{}m{} \033[382255255255m".format(255, 0, 0, text)

    pathtube1 = "/tmp/tubenommeprincipalsecond"
    pathtube2 = "/tmp/tubenommesecondprincipal"

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