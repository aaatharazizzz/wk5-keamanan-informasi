from wk5_crypt import des_encrypt, des_decrypt, pad_pkcs5, unpad_pkcs5
import socket, sys, threading

key = 0x67ABCDEFABCDEF67

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5050

BUF_SIZE = 2048

def handle_client(client_socket : socket.socket, addr):
    while True:
        data = client_socket.recv(BUF_SIZE)
        if not data:
            break
        client_socket.sendall
    client_socket.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    print("Server is litsening...")
    server_socket.listen(5)
    try:
        while True:
            client_socket, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, addr)).start()
    except KeyboardInterrupt:
        print("Exiting by keyboard interrupt")
        sys.exit(0)
    
        



