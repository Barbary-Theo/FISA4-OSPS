import os, sys
from multiprocessing import shared_memory


def mkfifo(path):
    # NE PAS FAIRE, C'EST DÉGEU, MAIS ON A PAS LE CHOIX DU COUP ON LE FAIT
    try:
        os.mkfifo(path, 0o0600)
    except:
        pass


def shm():
    shm_segment1 = shared_memory.SharedMemory(name='012345', create=True, size=10)
    print('Nom du segment mémoire partagée :', shm_segment1.name)
    print('Taille du segment mémoire partagée en octets via premier accès :', len(shm_segment1.buf))
    shm_segment1.buf[:10] = bytearray([74, 73, 72, 71, 70, 69, 68, 67, 66, 65])

    shm_segment2 = shared_memory.SharedMemory(shm_segment1.name)
    print('Taille du segment mémoire partagée en octets via second accès :', len(shm_segment2.buf[:10]))
    print('Contenu du segment mémoire partagée en octets via second accès :', bytes(shm_segment2.buf[:10]))

    newpid = os.fork()
    if newpid < 0:
        print("fork() impossible")
        os.abort()
    if newpid == 0:
        os.execlp("ipcs", "ipcs", "-m")
    else:
        os.wait()

    shm_segment2.close()
    shm_segment1.close()
    shm_segment1.unlink()


def main():
    to_red = lambda text: "\033[382{}{}{}m{} \033[382255255255m".format(255, 0, 0, text)

    pathtube1 = "/tmp/tubenommeprincipalsecond"
    pathtube2 = "/tmp/tubenommesecondprincipal"

    mkfifo(pathtube1)
    mkfifo(pathtube2)

    try:
        pid = os.fork()
        if pid < 0:
            print("It's not possible to fork() !")
        elif pid == 0:
            print('Overture du tube1 en écriture...')
            fifo1 = open(pathtube1, "w")

            print('Overture du tube2 en lecture...')
            fifo2 = open(pathtube2, "r")

            print('Processus principal prêt pour échanger des messages...')
            print('Écriture dans le tube1...')

            fifo1.write("PING\n")

            print('Fermeture du tube1...')
            fifo1.close()

            print('Processus principal en attente de réception de messages...')
            for line in fifo2:
                print("Message recu : " + line)

            print('Fermeture du tube2...')
            fifo2.close()

            print('Destruction des tubes...')
            os.unlink(pathtube1)
            os.unlink(pathtube2)
        else:
            print('Overture du tube1 en lecture...')
            fifo1 = open(pathtube1, "r")

            print('Overture du tube2 en écriture...')
            fifo2 = open(pathtube2, "w")

            print('Processus secondaire prêt pour échanger des messages...')

            print('Processus secondaire en attente de réception de messages...')

            for line in fifo1:
                print("Message recu : " + line)

            print('Fermeture du tube1...')
            fifo1.close()

            print('Écriture dans le tube2...')
            fifo2.write("PONG\n")

            print('Fermeture du tube2...')
            fifo2.close()

    except Exception as e:
        print(to_red(e.__str__()))


if __name__ == "__main__":
    main()
