import os, sys
from multiprocessing import shared_memory
from time import sleep
from random import randint


def prog_secondary_server():
    to_red = lambda text: "\033[382{}{}{}m{} \033[382255255255m".format(255, 0, 0, text)

    pathtube1 = "/tmp/tubenommeprincipalsecond"
    pathtube2 = "/tmp/tubenommesecondprincipal"

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