from Server import Server
from Client import Client
from Sub_class.button import *
import pygame
import threading
import time



class Online_hub():

    def __init__(self, screen, controller = None):

        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.client = Client()
        self.server = None                  # Current hosting server
        self.servers = []                   # List all servers available
        self.servers_amount = 0
        self.page_amount = 1
        self.current_page = 0
        self.hosting = False

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True

        # Loading Images & Sound
        self.load_assets()
        self.resize_assets()

        # Button creation
        self.create_buttons()                                       

        # Creation of a thread to refresh the server's list
        threading.Thread(target = self.client.discover_server, daemon=True).start()
        threading.Thread(target = self.refresh_servers, daemon=True).start()                                          
    

###################################################################################################


    def run(self):

        while self.running:
            self.refresh_screen()
            self.handle_event()
            self.clock.tick(self.fps)

        self.client.stop()
        if self.server:
            self.server.stop()


###################################################################################################


    def refresh_screen(self):
        
        self.screen.blit(self.background_img, (0,0))
        for button in self.buttons.keys():
            self.buttons[button].update(self.screen)
        self.display_servers()
        pygame.display.flip()


###################################################################################################


    def handle_event(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_event()


###################################################################################################


    def handle_mouse_event(self):

        x,y = pygame.mouse.get_pos()
        
        if self.buttons["back"].checkInput((x,y)):
            self.running = False
        elif self.buttons["join"].checkInput((x,y)):
            pass
        elif self.buttons["host"].checkInput((x,y)) and not self.hosting:
            self.host_server()
        elif self.buttons["up"].checkInput((x,y)) and self.current_page > 0:
            self.current_page -= 1
        elif self.buttons["down"].checkInput((x,y)) and self.current_page < self.page_amount-1:
            self.current_page += 1


###################################################################################################


    def host_server(self):

        self.server = Server("0.0.0.0", 5555)

        # Start the server in a separate thread
        threading.Thread(target=self.server.start, daemon=True).start()

        self.client.connect("127.0.0.1", 5555)
        self.hosting = True


###################################################################################################


    def load_assets(self):
        '''Load once all the assets needed in this menu'''
             
        self.background_img = pygame.image.load("Assets/Source_files/Images/Create_region/background.png")
        self.buttons_img = {"back": pygame.image.load("Assets/Source_files/Images/Create_region/close_rules.png"),
                            "up": pygame.image.load("Assets/Source_files/Images/Create_region/close_rules.png"),
                            "down": pygame.image.load("Assets/Source_files/Images/Create_region/close_rules.png"),
                            "join": pygame.image.load("Assets/Source_files/Images/Create_region/close_rules.png"),
                            "host": pygame.image.load("Assets/Source_files/Images/Create_region/close_rules.png")}


###################################################################################################


    def resize_assets(self):

        self.background_img = pygame.transform.smoothscale(self.background_img, (self.screen_width, self.screen_height))
        
        for button in self.buttons_img.keys():
            self.buttons_img[button] = pygame.transform.smoothscale(self.buttons_img[button], (self.screen_width * 200/1280, self.screen_height * 120/780))


###################################################################################################


    def create_buttons(self):
        '''Initialize all buttons needed with their respective coordinates'''

        self.buttons = {"back" : Button((self.screen_width * 0.03, self.screen_height * 0.78), self.buttons_img["back"]),
                        "up" : Button((self.screen_width * 0.76 ,self.screen_height * 0.09), self.buttons_img["up"]),
                        "down" : Button((self.screen_width * 0.76, self.screen_height * 0.38), self.buttons_img["down"]),
                        "join" : Button((self.screen_width * 0.3, self.screen_height * 0.75), self.buttons_img["up"], text="Join", base_color="black", font_size= int(self.screen_height/720 * 64)),
                        "host" : Button((self.screen_width * 0.51, self.screen_height * 0.75), self.buttons_img["down"], text="Host", base_color="black", font_size= int(self.screen_height/720 * 64))
                        }


###################################################################################################

    
    def refresh_servers(self):
        '''Refresh the current list of server every 5s'''

        while self.running:
            self.servers = self.client.get_server()
            self.servers_amount = len(self.servers)
            self.page_amount = self.servers_amount//4 + 1
            time.sleep(5)
            print(self.servers)


###################################################################################################


    def display_servers(self):
        '''Used to blit at max 4 availables servers, based on current page'''

        x, y = self.screen_width * 0.17, self.screen_height * 0.10
        for i in range(self.current_page * 4, self.current_page*4+4):
            if i < self.servers_amount and self.servers[i]:
                font = pygame.font.Font("Assets/Source_files/fonts/font.ttf", int(self.screen_height/720 * 64))
                text_surface = font.render("Server", True, "red")
                text_rect = text_surface.get_rect()
                text_rect.topleft = (x, y)
                self.screen.blit(text_surface, text_rect)
            y += self.screen_height * 0.15


######################################################################################################################################################################################################


if __name__ == "__main__":
    #Using this command before because in real usage, it will be "setup"
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))                          # Another commune resolution is 1280 x 720
    Online_hub(screen).run()