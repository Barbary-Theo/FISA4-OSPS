#! /usr/bin/env python3
# _*_ coding: utf8 _*_
#
# Exemple de création d'un segment mémoire partagé + écriture d'information "à l'intérieur"
#
# Version 27/09/2022
#
import os, sys
from multiprocessing import shared_memory


# Création du segment mémoire partagée + accès à son "nom" (utilisé pour générer une clef)
# (le nom peut être généré automatiquement, mais l'avantage de le fixer est que les n processus
# qui accèdent au même segment ont "juste besoin de connaitre ce nom pour y accéder")
#
# PROBLÈMES : Qui gère les droits ? Pourquoi ipcs ne "voit" pas le segment ?
def shm():
    shared_memory.SharedMemory(name='shm_osps', create=True, size=10)
    '''shm_segment1 = shared_memory.SharedMemory(name='shm_osps', create=True, size=10)
    #print('Nom du segment mémoire partagée :', shm_segment1.name)

    # Accès + écriture de données via le premier accès au segment mémoire partagée
    print('Taille du segment mémoire partagée en octets via premier accès :', len(shm_segment1.buf))
    shm_segment1.buf[:10] = bytearray([74, 73, 72, 71, 70, 69, 68, 67, 66, 65])

    # Simuler l'attachement d'un second processus au même segment mémoire partagée
    # en utilisant le même nom que précédemment :
    shm_segment2 = shared_memory.SharedMemory(shm_segment1.name)

    # Accès + écriture de données via le second accès au MÊME segment mémoire partagée
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
    shm_segment1.unlink()'''
