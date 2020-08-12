#!./venv/bin/python
import threading
import socket
import blessings # Module to style and control the terminal/console.

HEADER = 128 # Message length limit
FORMAT = "utf-8" # Format of sent messages.
DISCONNECT = "DISCONNECT" # Message to request disconnection from the server.

class Console():
    def __init__(self):
        self.terminal = blessings.Terminal()

    def print_starting(self):
        print(self.terminal.red("[STARTING SERVER]..."))

    def print_listening(self, addr):
        str_addr = str(addr)
        print(self.terminal.red("[SERVER]:") + f" Server listening on " + self.terminal.green(str_addr))

    def print_new_con(self, addr): # Print new connection alert.
        str_addr = str(addr)
        print(self.terminal.yellow("[NEW CONNECTION]: ") + self.terminal.green(str_addr) + " has connected.")

    def print_active_count(self, count): # Print current number of clients connected.
        print(self.terminal.yellow("[ACTIVE CONNECTIONS]:") + f" {count}")

    def print_new_msg(self, msg, user_name): # Print new client's message.
        print(self.terminal.green(f"({user_name}): ") +  f"{msg}")

    def print_discon(self, addr): # Print disconnection alert.
        str_addr = str(addr)
        print(self.terminal.yellow("[USER DISCONNECTED]: ") + self.terminal.green(str_addr) + " has disconnected.")
console = Console() # Initialize Console


class Client():
    default_user_name = "user"

    def __init__(self, CONN, ADDR, user_name = default_user_name):
        self.CONN = CONN # Socket object allowing communication with the client.
        self.ADDR = ADDR # Client's address.
        self.IS_CONNECTED = True
        self.user_name = user_name

    def set_user_name(self, name):
        self.user_name = name

    def listen_msg(self): # Listen to new incoming messages from the client
        msg = self.CONN.recv(HEADER).decode(FORMAT)

        if msg: # If message is not empty.
            if msg != DISCONNECT:
                return msg
            else: # If disconnection is requested.
                self.IS_CONNECTED = False



class Server():

    default_ip = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1] # Server's IPv4 address.
    default_port = 5050
    default_max_con = 5

    def __init__(self, IP = default_ip, PORT = default_port, MAX_CON = default_max_con):
        self.IP = IP
        self.PORT = PORT
        self.ADDR = (IP, PORT) # Tuple containing server's IP address and port
        self.MAX_CON = MAX_CON # Maximum number of connections to the server.
        self.SOCK = None # Server's socket object.
        self.conn_clients = [] # List containing current connected clients.
        self.active_con = 0 # Current number of clients connected to server.
        self.msg_hist = [] # Message history.

    def start(self):
        console.print_starting()
        self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Server's socket object.
        self.SOCK.bind(self.ADDR)
        console.print_listening(self.ADDR)

    def __handle_discon(self, conn, addr): # Handle disconnection of a client.
        self.conn_clients.remove(conn)
        console.print_discon(addr)

    def __receive_user_name(self, client):
        user_name = client.listen_msg() # Receive client's user name.
        client.set_user_name(user_name) # Change client's user name.

    def __handle_client(self, conn, addr):
        client = Client(conn, addr) # Initialize Client object.
        self.__receive_user_name()
        self.conn_clients.append(client.CONN)
        
        # Listen to messages from CLIENT
        while client.IS_CONNECTED:
            msg = client.listen_msg()
            if msg: # If message is not empty
                self.msg_hist.append((client, msg))
                console.print_new_msg(msg, client.user_name)

        self.__handle_discon(conn, addr) # When client disconnects.


    def listenConn(self): # Listen to new connections and assign a new thread to each one.
        self.SOCK.listen(self.MAX_CON)
        while True:
            conn, addr = self.SOCK.accept()
            client_thread = threading.Thread(target=self.__handle_client, args=(conn, addr))
            client_thread.start() # Start client thread.
            self.active_con = threading.activeCount() - 1 # Update active connections.
            console.print_new_con(addr)
            console.print_active_count(self.active_con)


def main():
    server = Server()
    server.start()
    server.listenConn()

if __name__ == "__main__":
    main()