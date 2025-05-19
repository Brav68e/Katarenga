import socket
import threading
import json
import time
import Source_files.Network.Server as Server
from Source_files.Game_UI import *


class Client:

    def __init__(self, ip = None, port = None, username = None, broadcast_port = 50000, screen = None, online_hub = None):
        self.ip = ip
        self.port = port
        self.broadcast_port = broadcast_port
        self.username = username

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Socket de lien avec le server
        self.online_hub = online_hub        # Keep track of the Online_hub object to update the waiting variable
        self.available_server = []

        self.connected = False
        self.listening = True
        self.messages = None
        self.screen = screen

        self.timeout = 5      # Timeout of 5s for server request
        self.thread = None
        self.lock = threading.Lock()


    def connect(self, ip, port) -> bool:
        self.port = port
        self.ip = ip
        try:
            self.client_socket.connect((self.ip, self.port))
            self.client_socket.send(self.username.encode('utf-8'))  # Send the username to the server
            self.connected = True
            self.listening = False

            # Seperate Thread to handle communication
            self.thread = threading.Thread(target=self.receive_messages)
            self.thread.daemon = True
            self.thread.start()

            return True
        except Exception as e:
            print(f"Erreur de connexion: {e}")
            return False


    def stop(self):

        self.listening = False
        self.connected = False
        with self.lock:
            self.available_server = []
        try:
            self.client_socket.close()
        except:
            pass


    def receive_messages(self):
        buffer = ""
        while self.connected:
            try:
                # Read data from the socket
                data = self.client_socket.recv(8192).decode('utf-8')

                # Accumulate data in the buffer
                buffer += data

                # Process complete messages (delimited by '\n')
                while "\n" in buffer:
                    message, buffer = buffer.split("\n", 1)  # Split the buffer into one message and the rest
                    try:
                        message_data = json.loads(message)  # Parse the JSON message

                        # Handle responses
                        if message_data["type"] == "deplacement":
                            self.online_hub.online_deplacement(message_data["params"][0], message_data["params"][1], message_data["params"][2], message_data["params"][3], message_data["params"][4])

                        elif message_data["type"] == "placement":
                            self.online_hub.online_placement(message_data["params"][0], message_data["params"][1], message_data["params"][2])

                        elif "start" in message_data:
                            self.online_hub.start_game(read_board(message_data["board"])[0], message_data["usernames"], message_data["gamemode"])
                            self.online_hub.set_waiting(False)

                    except json.JSONDecodeError as e:
                        print(f"JSON decoding error: {e}")
                        continue

            except Exception as e:
                print(f"Error receiving message: {e}")
                import traceback
                traceback.print_exc()

        self.connected = False


    def discover_server(self):
        '''Listens for server broadcasts and stores the first discovered server'''

        # Socket UDP to track servers
        self.available_server = []
        self.listening = True
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow to reuse a port if alr used
        udp_socket.bind(("0.0.0.0", self.broadcast_port))

        print("Listening for server broadcasts...")
        while self.listening:
            data, addr = udp_socket.recvfrom(1024)
            server_info = json.loads(data.decode("utf-8"))
            server_host, server_port, server_name, hosting, gamemode= server_info["private_ip"], server_info["port"], server_info["name"], server_info["hosting"], server_info["gamemode"]
            
            with self.lock:
                if (server_host, server_port, server_name, gamemode) not in self.available_server and hosting:
                    self.available_server.append((server_host, server_port, server_name, gamemode))
                    print(f"Discovered server at {server_host}:{server_port}")

                elif not hosting:
                    # Delete the specific server info
                    for i, info in enumerate(self.available_server):
                        if info[0]==str(server_host) and info[1]==server_port:
                            self.available_server.pop(i)    

        with self.lock:
            self.available_server = []
        udp_socket.close()


    def get_server(self):
        '''Return the current list of available server'''

        with self.lock:
            return self.available_server
        

    def reset(self):
        '''Reset all important information about the current Client, useful we leaving a server'''

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Socket de lien avec le server
        self.connected = False
        self.listening = True

    
    def set_game_ui(self, game_ui):
        '''Set the game UI to the current client'''

        self.game_ui = game_ui

        
    def send_move(self, type, params):
        '''Send a msg to the server that basically spread the game state to all the players
        param type: a string to qualify the type of move (placement / deplacement)
        param params: a list of parameters to send to the server
        '''

        request = {"type": type, params: params}
        self.client_socket.send((json.dumps(request) + '\n').encode('utf-8'))


    def get_username(self):
        '''Return the current username of the client'''

        return self.username
    
    def set_username(self, username):
        '''Set the current username of the client'''

        self.username = username