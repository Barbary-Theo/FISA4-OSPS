#! /usr/bin/env python3
# _*_ coding: utf8 _*_
#
# Test d'une paire de tubes nommés SANS controle d'erreur
#
# Processus "principal" a lancer en premier
import os

print ('Création des tubes...');

# Ci-dessous "0o" instroduit un nombre en octal

pathtube1 = "/tmp/tubenommeprincipalsecond.fifo"
pathtube2 = "/tmp/tubenommesecondprincipal.fifo"
os.mkfifo(pathtube1, 0o0600)
os.mkfifo(pathtube2, 0o0600)

for i in range(3):
    print ('Overture du tube1 en écriture...');

    # Ouverture en écriture est bloquante si pas de lecteur

    fifo1 = open(pathtube1, "w")

    print ('Overture du tube2 en lecture...');

    # Ouverture en lecture est bloquante si pas de rédacteur

    fifo2 = open(pathtube2, "r")

    print ('Processus principal prêt pour échanger des messages...')

    print ('Écriture dans le tube1...');

    fifo1.write("Message 1 du processus principal !\n")
    fifo1.write("Message 2 du processus principal !\n")

    print ('Fermeture du tube1...');

    fifo1.close()

    print ('Processus principal en attente de réception de messages...')

    for line in fifo2:
        print ("Message recu : " + line)

    print ('Fermeture du tube2...');

    fifo2.close()

print ('Destruction des tubes...');

os.unlink(pathtube1)
os.unlink(pathtube2)
