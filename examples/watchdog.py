import socket


def prog():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 9001))

    s.send("s".encode())


if __name__ == "__main__":
    prog()
