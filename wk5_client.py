from wk5_crypt import des_encrypt, des_decrypt, pad_pkcs5, unpad_pkcs5
import socket, sys, threading


key = 0x67ABCDEFABCDEF67

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5050

BUF_SIZE = 2048

def receive(client_socket : socket.socket):
    try:
        while True:
            msg = client_socket.recv(BUF_SIZE)
            decrypted_msg = unpad_pkcs5(des_decrypt(msg, key.to_bytes(length=8))).decode('utf-8')
            print(decrypted_msg)
    except ConnectionResetError:
         pass



client_socket = socket.socket()
print("Connecting to server...")
client_socket.connect((SERVER_HOST, SERVER_PORT))
print("Connected")
receive_thread = threading.Thread(target=receive, args=[client_socket], daemon=True)
receive_thread.start()
try:
    while True:
            msg = input("> ")
            encrypted_msg = des_encrypt(pad_pkcs5(bytes(msg, 'utf-8')), key.to_bytes(length=8))
            client_socket.send(encrypted_msg)
except ConnectionResetError:
     print("Disconnected from server")
except KeyboardInterrupt:
    print("Exiting by keyboard interrupt...")
    sys.exit(0)