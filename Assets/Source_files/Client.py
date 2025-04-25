import socket
import threading
import json
import time
import Server as Server
from Game_UI import *


class Client:

    def __init__(self, ip = None, port = None, username = None, broadcast_port = 50000, screen = None):
        self.ip = ip
        self.port = port
        self.broadcast_port = broadcast_port
        self.username = username

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Socket de lien avec le server
        self.available_server = []

        self.connected = False
        self.listening = True
        self.messages = None
        self.screen = screen

        self.timeout = 2.0      # Timeout of 2s for server request
        self.response_data = None
        self.thread = None
        self.lock = threading.Lock()


    def connect(self, ip, port) -> bool:
        self.port = port
        self.ip = ip
        try:
            self.client_socket.connect((self.ip, self.port))
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


    def send_message(self, message: str) -> bool:
        if not self.connected:
            return False
        
        try:
            data = {"message": message}
            self.client_socket.send(json.dumps(data).encode('utf-8'))
            return True
        except:
            self.connected = False
            return False


    def receive_messages(self):
        while self.connected:
            try:
                data = self.client_socket.recv(8192).decode('utf-8')
                if not data:
                    break

                message_data = json.loads(data)                 # Loads act as parsing
                # Informations handling
                # Game initialization
                if "message" in message_data and message_data["message"] == "start":
                    grid = self.read_board(message_data["board"])
                    gamemode = message_data["gamemode"]
                    usernames = message_data["usernames"]
                    
                    # Start the GameUI in online mode
                    self.game_ui = GamesUI(self.screen, grid, gamemode, usernames, style="online", client=self)
                
                # Game updates
                elif "response" in message_data:
                    self.response_data = message_data["response"]

                    

            except Exception as e:
                print(f"Error receiving message: {e}")
        
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
    
    
    def send_msg(self, msg):
        '''Send a msg to the server that basically returns the request's response
        param: msg is a tuple with a string and a list of parameters
        '''

        self.response_data = None
        request = {"request": msg[0],
                   "params": msg[1] if msg[1] else None}
        self.client_socket.send(json.dumps(request).encode('utf-8'))

        start_time = time.time()
        while self.response_data is None and (time.time() - start_time) < self.timeout:
            time.sleep(0.05)

        return self.response_data
    

    def read_board(self, grid):
        '''Return a board with Object using a json like formatted board'''

        try:
            # Debug print to check the input grid
            print(f"Input grid: {grid}")

            # Process the grid (assuming this method transforms the board data)
            processed_grid = [[Tile.from_dict(tile) for tile in row] for row in grid]

            # Debug print to check the processed grid
            print(f"Processed grid: {processed_grid}")
            return processed_grid
        except Exception as e:
            print(f"Error processing board: {e}")
            return None