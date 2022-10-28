import multiprocessing
import threading
import socket as f
import time


def function(args):

    param: f.socket = args

    while True:
        value = param.recv(1)
        if value != None:
            print(value)


def join (worker):
    while worker.is_alive():
        worker.join(0.5)


def prog():

    port1 = 9001
    ip1 = "127.0.0.1"

    port2 = 9002
    ip2 = "127.0.0.1"

    current_socket1 = f.socket(f.AF_INET, f.SOCK_STREAM)
    current_socket1.bind((ip1, port1))
    current_socket1.listen(9003)

    current_socket2 = f.socket(f.AF_INET, f.SOCK_STREAM)
    current_socket2.bind((ip2, port2))
    current_socket2.listen(1)

    worker1 = threading.Thread(target=function, args=[current_socket1])
    worker1.daemon = True

    worker2 = threading.Thread(target=function, args=[current_socket2])
    worker2.daemon = True

    worker1.start()
    worker2.start()

    join(worker1)
    join(worker2)


if __name__ == "__main__":
    prog()
