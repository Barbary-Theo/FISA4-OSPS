import os
import pairetubesnommesprocessalancerenpremier as first
import pairetubesnommesprocessalancerensecond as second


def mkfifo(path):
    # NE PAS FAIRE, C'EST DÉGEU, MAIS ON A PAS LE CHOIX DU COUP ON LE FAIT
    try:
        os.mkfifo(path, 0o0600)
    except:
        pass


def prog():
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
            print('Création des tubes...')

            # Ci-dessous "0o" instroduit un nombre en octal

            for i in range(3):
                print('Overture du tube1 en écriture...')

                # Ouverture en écriture est bloquante si pas de lecteur

                fifo1 = open(pathtube1, "w")

                print('Overture du tube2 en lecture...')

                # Ouverture en lecture est bloquante si pas de rédacteur

                fifo2 = open(pathtube2, "r")

                print('Processus principal prêt pour échanger des messages...')

                print('Écriture dans le tube1...')

                fifo1.write("Message 1 du processus principal !\n")
                fifo1.write("Message 2 du processus principal !\n")

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

            for i in range(3):
                print('Overture du tube1 en lecture...')

                # Ouverture en lecture est bloquante si pas de rédacteur

                fifo1 = open(pathtube1, "r")

                print('Overture du tube2 en écriture...')

                # Ouverture en écriture est bloquante si pas de lecteur

                fifo2 = open(pathtube2, "w")

                print('Processus secondaire prêt pour échanger des messages...')

                print('Processus secondaire en attente de réception de messages...')

                for line in fifo1:
                    print("Message recu : " + line)

                print('Fermeture du tube1...')

                fifo1.close()

                print('Écriture dans le tube2...')

                fifo2.write("Message 1 du processus secondaire !\n")
                fifo2.write("Message 2 du processus secondaire !\n")

                print('Fermeture du tube2...')

                fifo2.close()

    except Exception as e:
        print(to_red(e.__str__()))


if __name__ == "__main__":
    prog()
