import os, sys
from multiprocessing import shared_memory
from time import sleep

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
            shm_segment1 = shared_memory.SharedMemory("shm_osps")
            print(shm_segment1.name)
            # print('Overture du tube1 en écriture...')
            fifo1 = open(pathtube1, "w")

            # print('Overture du tube2 en lecture...')
            fifo2 = open(pathtube2, "r")

            # print('Processus principal prêt pour échanger des messages...')
            # print('Écriture dans le tube1...')
            shm_segment1.buf[:7] = bytearray([66, 111, 110, 106, 111, 117, 114])
            fifo1.write("PING\n")

            # print('Fermeture du tube1...')
            #fifo1.close()

            # print('Processus principal en attente de réception de messages...')
            for line in fifo2:
                print("Message recu : " + line)

            # print('Fermeture du tube2...')
            #fifo2.close()

            # print('Destruction des tubes...')
            #os.unlink(pathtube1)
            #os.unlink(pathtube2)
        else:
            shm_segment2 = shared_memory.SharedMemory("shm_osps")
            # print('Overture du tube1 en lecture...')
            fifo1 = open(pathtube1, "r")

            # print('Overture du tube2 en écriture...')
            fifo2 = open(pathtube2, "w")

            # print('Processus secondaire prêt pour échanger des messages...')

            # print('Processus secondaire en attente de réception de messages...')

            for line in fifo1:
                print("Message recu : " + line)

            # print('Fermeture du tube1...')
            #fifo1.close()

            # print('Écriture dans le tube2...')
            print("Contenue dans le server secondaire : ", bytes(shm_segment2.buf[:10]))
            fifo2.write("PONG\n")

            # print('Fermeture du tube2...')
            #fifo2.close()

    except Exception as e:
        print(to_red(e.__str__()))


if __name__ == "__main__":
    main()
