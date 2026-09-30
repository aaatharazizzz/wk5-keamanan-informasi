from wk5_crypt import des_encrypt, des_decrypt, pad_pkcs5, unpad_pkcs5
import socket, sys, threading

key = 0x67ABCDEFABCDEF67

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5050

BUF_SIZE = 2048

clients : list[socket.socket] = []

def broadcast(data):
    for c in clients:
        try:
            c.sendall(data)
        except socket.error:
            c.close()
            clients.remove(c)

def handle_client(client_socket : socket.socket, addr):
    while True:
        try:
            data = client_socket.recv(BUF_SIZE)
            if not data:
                break
            print(unpad_pkcs5(des_decrypt(data, key.to_bytes(length=8))))
            broadcast(data)
        except ConnectionResetError:
            print("Client forcibly closed")
            break
    client_socket.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    print("Server is litsening...")
    server_socket.listen(5)
    server_socket.settimeout(1.0)

    try:
        while True:
            try:
                client_socket, addr = server_socket.accept()
                print("A client has connected")
                clients.append(client_socket)
                threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()
            except socket.timeout:
                continue
    except KeyboardInterrupt:
        print("Exiting by keyboard interrupt")
        sys.exit(0)
    finally:
        server_socket.close()
        



