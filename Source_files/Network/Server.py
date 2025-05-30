import socket
import threading
import json
import time
from Source_files.Games import Games
from Source_files.Sub_class.tile import Tile


class Server:

    def __init__(self, ip: str, port: int, name: str, gamemode: str, broadcast_port = 50000):
        self.name = name
        self.gamemode = gamemode
        self.ip = ip
        self.port = port
        self.broadcast_port = broadcast_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = {}                                                                   # Key : Socket / Value : Client ID
        self.usernames = []                                                                 # List of usernames
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
        """Properly stop the server and clean up resources"""
        
        # Set flag to stop accepting new connections and processing client requests
        self.running = False
        
        # Send a final broadcast announcing the server is no longer available
        try:
            with self.lock:
                if hasattr(self, 'udp_socket') and self.udp_socket:
                    try:
                        message = json.dumps({
                            "hosting": 0, 
                            "private_ip": self.get_private_ip(), 
                            "port": self.port, 
                            "name": self.name,
                            "gamemode": self.gamemode
                        })
                        # Send to both broadcast addresses to ensure coverage
                        self.udp_socket.sendto(message.encode("utf-8"), ("255.255.255.255", self.broadcast_port))
                        
                        # Only try specific broadcast if we have a valid IP
                        if hasattr(self, 'broadcast_ip'):
                            self.udp_socket.sendto(message.encode("utf-8"), (self.broadcast_ip, self.broadcast_port))
                        
                        # Close the UDP socket
                        self.udp_socket.close()
                    except Exception as e:
                        print(f"Error sending final broadcast: {e}")
        except Exception as e:
            print(f"Error during broadcast shutdown: {e}")

        # Close all client connections gracefully
        client_sockets = list(self.clients.keys())  # Make a copy to avoid modification during iteration
        for client_socket in client_sockets:
            try:
                # Try to send a disconnect message
                try:
                    disconnect_message = json.dumps({"type": "server_shutdown"}) + "\n"
                    client_socket.send(disconnect_message.encode('utf-8'))
                    time.sleep(0.1)  # Give time for the message to be sent
                except:
                    pass  # Continue with closure even if sending fails
                
                # Close the socket
                client_socket.close()
            except Exception as e:
                print(f"Error closing client socket: {e}")

        # Finally close the server socket
        try:
            self.server_socket.close()
        except Exception as e:
            print(f"Error closing server socket: {e}")
        
        # Clear client tracking
        self.clients = {}
        self.client_amount = 0
        


    def accept_connections(self):
        while self.running and self.client_amount < 2:
            try:
                client_socket, ip_port = self.server_socket.accept()                            # Just need the socket itself       
                self.usernames.append(client_socket.recv(1024).decode('utf-8'))                 # Get the username from the client         
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()      # Weird notation cuz args needs tuple (and tuple need atleast a comma)                
            except:
                break


        
    def handle_client(self, client_socket: socket.socket):
        """Handle client connection and gracefully manage disconnections"""
        
        with self.lock:
            self.client_amount += 1
            self.clients[client_socket] = self.client_amount
            
        buffer = ""
        client_id = self.clients[client_socket]
        
        while self.running:
            try:
                
                message_data = client_socket.recv(1024).decode('utf-8')
                if not message_data:
                    break
                
                buffer += message_data

                while "\n" in buffer:
                    # Handle the request
                    message, buffer = buffer.split("\n", 1)  # Split the buffer into one message and the rest
                
                    data = json.loads(message)  # Parse the JSON message

                    if data["type"] in ["deplacement", "placement"]:
                        self.broadcast_board_update(data["type"], data["params"])

                    elif data["type"] == "stop_game":
                        self.broadcast_board_update("stop_game", None)
                    
            except (ConnectionResetError, ConnectionAbortedError):
                #print(f"Connection with client {client_id} was closed.")
                break
            except Exception as e:
                import traceback
                print(f"Unexpected server error with client {client_id}: {e}")
                traceback.print_exc()
                break
            


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

        for client_socket in self.clients.keys():
            start_message = {
                "start": "game",
                "gamemode": self.gamemode,
                "usernames": self.usernames,
                "board": [[tile.to_dict() for tile in row] for row in grid]
            }
        
            start_message = json.dumps(start_message) + '\n'

            try:
                client_socket.send(start_message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending start message: {e}")


    def broadcast_board_update(self, type, params):
        '''Broadcast the current game state to all clients'''

        for client_socket in self.clients.keys():
            try:
                message = {
                    "type": type,
                    "params": params
                }
                
                message = json.dumps(message) + '\n'
                client_socket.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending board message: {e}")