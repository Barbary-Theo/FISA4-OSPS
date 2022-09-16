#! /usr/bin/env python3
# _*_ coding: utf8 _*_
#
# Test d'une paire de tubes nommés SANS controle d'erreur
#
# Processus "secondaire" a lancer en second,
# en parallele du processus "principal",
# dans une autre console (shell)
import os

pathtube1 = "/tmp/tubenommeprincipalsecond.fifo"
pathtube2 = "/tmp/tubenommesecondprincipal.fifo"

for i in range(3):
    print ('Overture du tube1 en lecture...');

    # Ouverture en lecture est bloquante si pas de rédacteur

    fifo1 = open(pathtube1, "r")

    print ('Overture du tube2 en écriture...');

    # Ouverture en écriture est bloquante si pas de lecteur

    fifo2 = open(pathtube2, "w")

    print ('Processus secondaire prêt pour échanger des messages...')

    print ('Processus secondaire en attente de réception de messages...')

    for line in fifo1:
        print ("Message recu : " + line)

    print ('Fermeture du tube1...');

    fifo1.close()

    print ('Écriture dans le tube2...');

    fifo2.write("Message 1 du processus secondaire !\n")
    fifo2.write("Message 2 du processus secondaire !\n")

    print ('Fermeture du tube2...');

    fifo2.close()
