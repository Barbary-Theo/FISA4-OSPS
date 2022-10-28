import socket


def prog():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("www.python.org", 80))


if (__name__ == "__main__"):
    prog()
