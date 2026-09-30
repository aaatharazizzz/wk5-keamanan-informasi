from wk5_crypt import des_encrypt, des_decrypt, pad_pkcs5, unpad_pkcs5
import socket, sys, threading


key = 0x67ABCDEFABCDEF67

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5050

client_socket = socket.socket()
client_socket.connect((SERVER_HOST, SERVER_PORT))

