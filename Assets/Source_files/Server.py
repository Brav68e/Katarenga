import socket
import threading
import json
import time


class Server:

    def __init__(self, ip: str, port: int, broadcast_port = 50000):
        self.ip = ip
        self.port = port
        self.broadcast_port = broadcast_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}                                                                   # Key : Socket / Value : Name
        self.running = False
        self.thread = None
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
        for client in list(self.clients.keys()):
            try:
                client.close()
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
                    # Gestion de l'information

                except:
                    break
                
        except Exception as e:
            print(f"Erreur client: {e}")
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

        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # Get the actual local IP and network interface
        try:
            # Create a dummy socket to determine the correct network interface
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))  # Connect to an external server
            local_ip = s.getsockname()[0]
            s.close()

            # Explicitly set broadcast address based on local IP
            broadcast_addr = '.'.join(local_ip.split('.')[:-1] + ['255'])
            
            message = json.dumps({"private_ip": local_ip, "port": self.port})

            # Bind to a specific interface if needed
            udp_socket.bind((local_ip, 0))

            while self.running:
                udp_socket.sendto(message.encode("utf-8"), (broadcast_addr, self.broadcast_port))
                time.sleep(5)  # Broadcast every 5 seconds

        except Exception as e:
            print(f"Broadcast error: {e}")
        finally:
            udp_socket.close()


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