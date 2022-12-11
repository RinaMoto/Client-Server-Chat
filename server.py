# server side chat
import socket, time, sys

# global constants
HEADER_LENGTH = 10
HOST = "127.0.0.1"
PORT = 7777

def server():
    print("\n*Welcome to the client-server chat room*\n")
    time.sleep(1)

    # code adapted from: https://www.biob.in/2018/04/simple-server-and-client-chat-using.html
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # set up connection with client, send server name
        s.bind((HOST, PORT))
        name = input(str("Enter your name: "))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            server_name = conn.recv(1024)
            server_name = server_name.decode()
            print(f"{server_name} has entered the chat room\nEnter \q to exit the chat room\n")
            conn.send(name.encode())

            while True:
                # process msg and send msg header + msg
                msg = input(str("Me: "))
                if msg == "\q":
                    msg = "exiting chat room..."
                    message_header = f"{len(msg):<{HEADER_LENGTH}}".encode('utf-8')
                    conn.send(message_header + msg.encode('utf-8'))
                    print("\n")
                    sys.exit()
                    break
                msg = msg.encode('utf-8')
                message_header = f"{len(msg):<{HEADER_LENGTH}}".encode('utf-8')
                conn.send(message_header + msg)

                # receive msg header + msg
                message_header = conn.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                msg = conn.recv(message_length)
                msg = msg.decode()
                print(f"{server_name}: {msg}")


if __name__ == '__main__':
    server()
