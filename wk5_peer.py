from wk5_crypt import des_encrypt, des_decrypt, pad_pkcs5, unpad_pkcs5
import socket, sys, threading


key = 0xFAFAFAFA67676767

class P2PNode:

    def __init__(self):
        pass


def main():
    if len(sys.argv) < 2:
        print("Usage: python wk5_main.py [LISTEN_PORT]")
        exit(0);
    try:
        listen_host = '127.0.0.1'
        listen_port = int(sys.argv)
        if(listen_port < 0 or listen_port > 65535):
            raise Exception("Port number too low or too high")
    except TypeError:
        print("Error: Cannot parse [LISTEN_PORT], please enter a valid number")
        exit(-1)
    except Exception as e:
        print(f"Error: {e}")
        exit(-1)
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    

if __name__ == "__main__":
    main()