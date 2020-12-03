# /home/neolight1010/anaconda3/bin/python /home/neolight1010/Documents/Coding/mini_chat/client/client.py
import socket
import blessings
import atexit
from time import sleep

HEADER = 128  # Message length limit
FORMAT = "utf-8"  # Format of sent messages.
DISCONNECT = "DISCONNECT"  # Message to request disconnection from the server.

default_port = 5050


class Console():
    def __init__(self):
        self.t = blessings.Terminal()

    def print_starting(self):
        print(self.t.red("[STARTING]..."))

    def print_failed_connection(self):
        print(self.t.red("[ERROR]: ") + "Connection to the server has failed. Please, try again.")

    def print_conn_success(self, addr):
        str_addr = str(addr)
        print(self.t.green("[CONNECTED]: ") + "You are now connected to " + self.t.green(str_addr))
console = Console()


class Server():
    default_server_ip = "192.168.0.189"

    def __init__(self, IP = default_server_ip, PORT = default_port):
        self.IP = IP
        self.PORT = PORT
        self.ADDR = (IP, PORT)

    def change_ADDR(self, ip = default_server_ip, port = default_port):
        self.IP = ip
        self.PORT = port


class Client():
    default_client_ip = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1] # Get client's ip

    def __init__(self, linker, user_name, IP = default_client_ip, PORT = default_port):
        self.IP = IP # Client's IP
        self.PORT = PORT 
        self.ADDR = (IP, PORT) # Tuple containing Client's IP and PORT
        self.SOCK = None # Socket object for Client
        self.IS_CONNECTED = True # True if client is connected to Server.
        self.user_name = user_name # User's name.
        self.linker = linker

    def start(self, addr): # addr = Server's addr
        self.linker.send_notif('Backend linker connected!')
        console.print_starting()
        self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.SOCK.connect(addr) # Connect to Server's addr.
        except OSError:
            self.linker.send_notif("CONNECT_ERROR")
            self.IS_CONNECTED = False

        if self.IS_CONNECTED:
            console.print_conn_success(addr)
            self.linker.send_notif('CONNECT_SUCCESS')
            self.IS_CONNECTED = True
            self.SOCK.send(self.user_name.encode(FORMAT))  # Send user's name to SERVER.
            self.linker.send_notif("Connection successful. Welcome.")

    def send_msg(self,msg):
        encoded = msg.encode(FORMAT)
        self.SOCK.send(encoded)

        if msg == DISCONNECT:
            self.IS_CONNECTED = False

    def disconnect(self):
        self.send_msg(DISCONNECT)    
        self.IS_CONNECTED = False    

    def terminal_input(self):
        while self.IS_CONNECTED:
            msg = input(": ")
            self.send_msg(msg)

    
def start(server, client):
    client.start(server.ADDR) # Connect to Server's ADDR.
    if client.IS_CONNECTED:
        atexit.register(client.disconnect)


# if __name__ == "__main__":
#     server = Server()
#     client = Client()
#     start(server, client)
