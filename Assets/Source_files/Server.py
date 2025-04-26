import socket
import threading
import json
import time
from Games import *


class Server:

    def __init__(self, ip: str, port: int, name: str, gamemode: str, broadcast_port = 50000):
        self.name = name
        self.gamemode = gamemode
        self.ip = ip
        self.port = port
        self.broadcast_port = broadcast_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = {}                                                                   # Key : Socket / Value : Name
        self.running = False
        self.thread = None
        self.lock = threading.Lock()
        self.client_amount = 0

    def start(self):
        try:
            self.server_socket.bind((self.ip, self.port))
            self.server_socket.listen(2)
            self.running = True

            # Seperate thread to show presence
            self.thread = threading.Thread(target=self.broadcast_presence)
            self.thread.daemon = True
            self.thread.start()

            # Seperate thread to handle connection
            self.thread = threading.Thread(target=self.accept_connections)
            self.thread.daemon = True
            self.thread.start()
            return True
        except Exception as e:
            print(f"Erreur de démarrage du serveur: {e}")
            return False


    def stop(self):
        self.running = False
        
        with self.lock:  # Lock before modifying or closing the socket
            if self.udp_socket:
                try:
                    message = json.dumps({"hosting": 0, "private_ip": self.get_private_ip(), "port": self.port, "name": self.name})
                    self.udp_socket.sendto(message.encode("utf-8"), ("<broadcast>", self.broadcast_port))
                    self.udp_socket.sendto(message.encode("utf-8"), (self.broadcast_ip, self.broadcast_port))
                    self.udp_socket.close()
                    self.udp_socket = None
                except Exception as e:
                    print(f"Error closing UDP socket: {e}")

        for client in list(self.clients.keys()):
            try:
                client.close()
                print("client close")
            except:
                pass
        try:
            self.server_socket.close()
        except:
            pass


    def accept_connections(self):
        while self.running:
            try:
                client_socket, ip_port = self.server_socket.accept()                            # Just need the socket itself                             
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()      # Weird notation cuz args needs tuple (and tuple need atleast a comma)                
            except:
                break


    def handle_client(self, client_socket: socket.socket):
        try: 
            self.client_amount += 1
            self.clients[client_socket] = self.client_amount
            
            while self.running:
                try:
                    message_data = client_socket.recv(1024).decode('utf-8')
                    if not message_data:
                        break
                    
                    data = json.loads(message_data)
                    print(f"Request received from client: {data}")

                    # Handle the request
                    response = None
                    match data["request"]:
                        case "get_grid":
                            response = [[tile.to_dict() for tile in row] for row in self.game.get_grid()]
                            print(f"Grid sent to client: {response}")

                        case "get_camps":
                            response = self.game.get_camps()
                            print(f"Camps sent to client: {response}")

                        # Add other cases as needed...

                    # Send the response
                    if response is not None:
                        message = {"response": response}
                        client_socket.send(json.dumps(message).encode('utf-8'))
                        print(f"Response sent to client: {message}")

                except Exception as e:
                    print(f"Error handling client request: {e}")
                    import traceback
                    traceback.print_exc()
                    break
                    
        except Exception as e:
            print(f"Error in handle_client: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if client_socket in self.clients:
                del self.clients[client_socket]
                client_socket.close()
    

    def broadcast(self, data):
        '''Send a specific message to all clients connected to the server'''

        message = json.dumps(data)
        for client in list(self.clients.keys()):
            try:
                client.send(message.encode('utf-8'))
            except:
                # Si l'envoi échoue, on considère que le client est déconnecté
                if client in self.clients:
                    del self.clients[client]


    def broadcast_presence(self):
        '''Periodically broadcasts server presence via UDP.'''

        with self.lock:
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # Try broadcasting to specific broadcast address instead of <broadcast>
        local_ip = self.get_private_ip()
        if local_ip:
            # Calculate broadcast address based on local IP (ASSUMING WE GOT A 24bits Mask)
            ip_parts = local_ip.split('.')
            self.broadcast_ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.255"
            message = json.dumps({"hosting": 1, "private_ip": local_ip, "port": self.port, "name": self.name, "gamemode": self.gamemode})
            
            while self.running and self.client_amount < 2:
                try:
                    with self.lock:  # Lock before using the UDP socket
                        if self.udp_socket:
                            self.udp_socket.sendto(message.encode("utf-8"), (self.broadcast_ip, self.broadcast_port))
                            self.udp_socket.sendto(message.encode("utf-8"), ("255.255.255.255", self.broadcast_port))
                        else:
                            break
                except Exception as e:
                    print(f"Broadcast error: {e}")
                time.sleep(5)
                

    def get_private_ip(self):
        try:
            # Create a dummy socket to find the real local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))                          # Connect to an external server (Google DNS)
            local_ip = s.getsockname()[0]                       # Get the assigned local IP
            s.close()
            return local_ip
        except Exception as e:
            print(f"Error getting private IP: {e}")
            return None
        

        
    def get_client_amount(self):
        return self.client_amount
    

    def start_game(self, grid):
        '''Start the game on the server and communicates it to client'''

        self.game = Games(grid, "host", "guess", self.gamemode)
        self.game.init_pawns()
        self.game_started = True

        # Formatting the board object notation into json
        board = [[tile.to_dict() for tile in row] for row in self.game.get_grid()]

        for client_socket in self.clients.keys():
            start_message = {
                "message": "start",
                "board": board,
                "gamemode": self.gamemode,
                "usernames": ["host", "guest"],
                "current_player": 0
            }

            try:
                client_socket.send(json.dumps(start_message).encode('utf-8'))
            except Exception as e:
                print(f"Error sending start message: {e}")
