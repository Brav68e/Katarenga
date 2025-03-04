import socket
import threading
import json
import server


class Client:

    def __init__(self, ip: None, port: None, username: None, broadcast_port = 50000):
        self.ip = ip
        self.port = port
        self.broadcast_port = broadcast_port
        self.username = username
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Socket de lien avec le server
        self.available_server = []
        self.connected = False
        self.listening = True
        self.messages = None
        self.thread = None
        print(f"Socket de communication : {ip},{port}")


    def connect(self) -> bool:
        try:
            self.client_socket.connect((self.ip, self.port))
            # Envoyer le nom d'utilisateur
            self.client_socket.send(json.dumps({"username": self.username}).encode('utf-8'))
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


    def disconnect(self):
        self.connected = False
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
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                message_data = json.loads(data)                 # Loads act as parsing
                # Gestion de l'information
            except:
                break
        
        self.connected = False


    def discover_server(self):
        '''Listens for server broadcasts and stores the first discovered server'''

        # Socket UDP to track servers
        self.listening = True
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.bind(("", self.broadcast_port))

        print("Listening for server broadcasts...")
        while self.listening:
            data, addr = udp_socket.recvfrom(1024)
            server_info = json.loads(data.decode("utf-8"))
            self.server_host, self.server_port = server_info["private_ip"], server_info["port"]
            print(f"Discovered server at {self.server_host}:{self.server_port}")

        udp_socket.close()