# client side chat
import socket, time, sys

# global constants
HEADER_LENGTH = 10
HOST = "127.0.0.1"
PORT = 7777

def client():
    print("\n*Welcome to the client-server chat room*\n")
    time.sleep(1)

    # code adapted from: https://www.biob.in/2018/04/simple-server-and-client-chat-using.html
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # set up connection with server, send client name
        client_name = input(str("\nEnter your name: "))
        print(f"\nAttempting to connect to {HOST} ({PORT})\n")
        time.sleep(1)
        s.connect((HOST, PORT))
        print("Connected...\n")
        s.send(client_name.encode())

        # get server name
        server_name = s.recv(1023)
        server_name = server_name.decode()
        print(f"{server_name} has entered the chat room\nEnter \q to exit the chat room\n")
        while True:

            # get msg header + length
            message_header = s.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            msg = s.recv(message_length)
            msg = msg.decode()
            print(f"{server_name}: {msg}")
            msg = input(str("Me: "))

            if msg == "\q":
                msg = "exiting chat room..."
                message_header = f"{len(msg):<{HEADER_LENGTH}}".encode('utf-8')
                s.send(message_header + msg.encode('utf-8'))
                print("\n")
                sys.exit()
                break

            # process and send msg header + msg length
            msg = msg.encode('utf-8')
            message_header = f"{len(msg):<{HEADER_LENGTH}}".encode('utf-8')
            s.send(message_header + msg)

if __name__ == '__main__':
    client()
