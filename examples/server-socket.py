import socket


def prog():

    HOST = "127.0.0.1"
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        while True:

            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")

                data = conn.recv(1024)
                if data:
                    conn.sendall(data)


if __name__ == "__main__":
    prog()
