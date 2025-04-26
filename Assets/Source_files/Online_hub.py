from Server import Server
from Client import Client
from Sub_class.button import *
from math import ceil
from Board_creation import *
import pygame
import threading
import time



class Online_hub():

    def __init__(self, screen, controller = None):

        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.client = Client(screen=screen)  # Create a client instance with the screen as an argument

        self.server = None                  # Current hosting server
        self.hosting = False

        self.servers = []                   # List all servers available
        self.servers_amount = 0
        self.page_amount = 1
        self.current_page = 0
        self.selected_server = None

        self.lock = threading.Lock()        # Create a Lock to handle critical data

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True
        self.waiting = False

        # Loading Images & Sound
        self.load_assets()
        self.resize_assets()
        self.font = pygame.font.Font("Assets/Source_files/fonts/font.ttf", int(self.screen_height/720 * 64))

        # Button creation & Server selection collision
        self.create_buttons()                         
        self.create_server_collision()              

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
        self.display_title()
        for button in ["back", "up", "down", "join", "host"]:
            self.buttons[button].update(self.screen)
        self.display_servers_background()
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
            if self.client.connect(self.servers[self.selected_server][0], self.servers[self.selected_server][1]):           # 0 is ip, 1 is port, 2 is name, 3 is gamemode
                self.waiting_menu2()
        elif self.buttons["host"].checkInput((x,y)) and not self.hosting:
            self.host_menu()
        elif self.buttons["up"].checkInput((x,y)) and self.current_page > 0:
            self.current_page -= 1
        elif self.buttons["down"].checkInput((x,y)) and self.current_page < self.page_amount-1:
            self.current_page += 1
        
        # Check for server selection
        index = self.check_server_selection((x,y))
        if index != -1:
            self.selected_server = self.current_page * 4 + index



###################################################################################################


    def host_server(self, host_name, gamemode):

        self.server = Server("0.0.0.0", 5555, host_name, gamemode)

        # Start the server in a separate thread
        threading.Thread(target=self.server.start, daemon=True).start()

        self.client.connect("127.0.0.1", 5555)
        self.hosting = True


###################################################################################################


    def host_menu(self):
        '''Mainloop that allow the player to decide a server's name and display a button to continue'''

        running = True
        host_name = ""
        active = False
        input_box = pygame.Rect(0, 0, self.screen_width * 0.53, self.screen_height * 0.14)
        input_box.center = (self.screen_width // 2, int(self.screen_height * 0.45))
        color_active = (200, 200, 200)
        color_inactive = (175, 175, 175)
        color = color_inactive
        max_chars = 20

        while running:
            
            # Display Background + Button
            self.screen.blit(self.background_img, (0,0))
            self.buttons["back"].update(self.screen)
            self.buttons["next"].update(self.screen)

            # Handle Event
            x,y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check for text selection
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive

                    # Check for button selection
                    if self.buttons["back"].checkInput((x,y)):
                        running = False
                    elif self.buttons["next"].checkInput((x,y)):      
                        # Go on the next interface to choose gamemode
                        running = self.gamemode_menu(host_name)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Act as create button (Enter key)
                        running = self.gamemode_menu(host_name)
                    elif event.key == pygame.K_BACKSPACE:
                        host_name = host_name[:-1]
                    elif len(host_name) < max_chars and active:
                        host_name += event.unicode

            # Check for hovering animation
            if self.buttons["create"].checkInput((x,y)) and host_name:
                self.buttons_img["create"].set_alpha(250)
            else:
                self.buttons_img["create"].set_alpha(150)

            # Draw input box
            pygame.draw.rect(self.screen, color, input_box, border_radius=5)

            # Render text + blitting
            text_surface = self.font.render(host_name, True, (255, 0, 0))
            input_width, input_height = text_surface.get_size()
            self.screen.blit(text_surface, (input_box.x + (input_box.width - input_width) // 2, input_box.y + (input_box.height - input_height) // 2))

            pygame.display.flip()


###################################################################################################


    def gamemode_menu(self, host_name):
            '''Mainloop that allow the player to decide a server's gamemode between the 3 availables'''

            running = True
            gamemode = None
            rect = pygame.Rect(0, 0, self.screen_width * 0.42, self.screen_height * 0.14)

            while running:
                
                # Display Background + Button
                self.screen.blit(self.background_img, (0,0))
                self.buttons["back"].update(self.screen)
                self.buttons["create"].update(self.screen)
                self.buttons["katarenga"].update(self.screen)
                self.buttons["congress"].update(self.screen)
                self.buttons["isolation"].update(self.screen)

                # Display a selection rectangle around the selected gamemode
                if gamemode:
                    rect.center = self.buttons[gamemode].rect.center
                    pygame.draw.rect(self.screen, (0, 0, 0), rect, 5, border_radius=10)
                    self.buttons_img["create"].set_alpha(250)
                else:
                    self.buttons_img["create"].set_alpha(150)

                # Handle Event
                x,y = pygame.mouse.get_pos()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Check for button selection
                        if self.buttons["back"].checkInput((x,y)):
                            running = False
                        elif self.buttons["create"].checkInput((x,y)) and gamemode:      
                            # Create a server and switch interface
                            self.host_server(host_name, gamemode)
                            running = self.waiting_menu(host_name)
                        elif self.buttons["katarenga"].checkInput((x,y)):
                            gamemode = "katarenga"
                        elif self.buttons["congress"].checkInput((x,y)):
                            gamemode = "congress"
                        elif self.buttons["isolation"].checkInput((x,y)):
                            gamemode = "isolation"
                        else:
                            gamemode = None




                pygame.display.flip()


###################################################################################################


    def waiting_menu(self, party_name):
        '''Lock the current hosting user in a loading screen waiting for other user'''

        waiting = True

        text_surface = self.font.render(f"{party_name}, waiting for player", True, (255, 0, 0))
        text_width= text_surface.get_size()[0]
        text_x, text_y= (self.screen_width - text_width) // 2, int(self.screen_height * 0.35)
        
        # Dot animation setup
        dots = [".", "..", "..."]
        dot_index = 0
        last_update_time = pygame.time.get_ticks()
        dot_surface = self.font.render(dots[0], True, (255, 0, 0))
        dot_width = dot_surface.get_size()[0]
        dot_x = text_x + (text_width - dot_width) // 2
        dot_y = int(self.screen_height * 0.45)
        

        while waiting:

            # Update dot animation every 500ms
            if pygame.time.get_ticks() - last_update_time > 500:
                dot_index = (dot_index + 1) % len(dots)
                last_update_time = pygame.time.get_ticks()
                dot_surface = self.font.render(dots[dot_index], True, (255, 0, 0))
                dot_width = dot_surface.get_size()[0]
                dot_x = text_x + (text_width - dot_width) // 2
                dot_y = int(self.screen_height * 0.45)

            # Display Background + Button
            self.screen.blit(self.background_img, (0,0))
            self.buttons["back"].update(self.screen)

            # Display the Party's name
            self.screen.blit(text_surface, (text_x, text_y))
            # Display dot animation
            self.screen.blit(dot_surface, (dot_x, dot_y))

            
            # Handle Event
            x,y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttons["back"].checkInput((x,y)):
                        self.server.stop()
                        self.client.reset()
                        self.server = None
                        self.hosting = False
                        waiting = False

            # Check if the server is full
            with self.lock:                                 # Lock before reading shared data
                if self.server and self.server.get_client_amount() >= 2:
                    waiting = False
                    board = Board_creation(self.screen).run()
                    self.server.start_game(board)

                    

            pygame.display.flip()

        return False


###################################################################################################


    def waiting_menu2(self):
        '''Lock the user that joined a server in a loading screen waiting for the host'''

        self.waiting = True

        text_surface = self.font.render("Loading", True, (255, 0, 0))
        text_width= text_surface.get_size()[0]
        text_x, text_y= (self.screen_width - text_width) // 2, int(self.screen_height * 0.35)
        
        # Dot animation setup
        dots = [".", "..", "..."]
        dot_index = 0
        last_update_time = pygame.time.get_ticks()
        dot_surface = self.font.render(dots[0], True, (255, 0, 0))
        dot_width = dot_surface.get_size()[0]
        dot_x = text_x + (text_width - dot_width) // 2
        dot_y = int(self.screen_height * 0.45)
        

        while self.waiting:

            # Update dot animation every 500ms
            if pygame.time.get_ticks() - last_update_time > 500:
                dot_index = (dot_index + 1) % len(dots)
                last_update_time = pygame.time.get_ticks()
                dot_surface = self.font.render(dots[dot_index], True, (255, 0, 0))
                dot_width = dot_surface.get_size()[0]
                dot_x = text_x + (text_width - dot_width) // 2
                dot_y = int(self.screen_height * 0.45)

            # Display Background + Button
            self.screen.blit(self.background_img, (0,0))

            # Display the Party's name
            self.screen.blit(text_surface, (text_x, text_y))
            # Display dot animation
            self.screen.blit(dot_surface, (dot_x, dot_y))

            
            # Handle Event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.waiting = False
                    

            pygame.display.flip()

        return False
    

###################################################################################################


    def load_assets(self):
        '''Load once all the assets needed in this menu'''
             
        self.background_img = pygame.image.load("Assets/Source_files/Images/menu/imgs/Background.png")
        self.buttons_img = {"back": pygame.image.load("Assets/Source_files/Images/Delete_region/left_arrow.png"),
                            "up": pygame.image.load("Assets/Source_files/Images/Delete_region/up_arrow.png"),
                            "down": pygame.image.load("Assets/Source_files/Images/Delete_region/down_arrow.png"),
                            "join": pygame.image.load("Assets/Source_files/Images/Create_region/next.png"),
                            "host": pygame.image.load("Assets/Source_files/Images/Create_region/next.png"),
                            "create": pygame.image.load("Assets/Source_files/Images/Create_region/next.png"),
                            "next": pygame.image.load("Assets/Source_files/Images/Create_region/next.png"),
                            }


###################################################################################################


    def resize_assets(self):

        self.background_img = pygame.transform.smoothscale(self.background_img, (self.screen_width, self.screen_height))
        
        for button in self.buttons_img.keys():
            self.buttons_img[button] = pygame.transform.smoothscale(self.buttons_img[button], (self.screen_width * 200/1280, self.screen_height * 120/780))

        self.buttons_img["back"] = pygame.transform.smoothscale(self.buttons_img["back"], (self.screen_height * 100/780, self.screen_height * 100/780))

###################################################################################################


    def create_buttons(self):
        '''Initialize all buttons needed with their respective coordinates'''

        self.buttons = {"back" : Button((self.screen_width * 0.03, self.screen_height * 650/780), self.buttons_img["back"]),
                        "up" : Button((self.screen_width * 0.76 ,self.screen_height * 216/780), self.buttons_img["up"]),
                        "down" : Button((self.screen_width * 0.76, self.screen_height * 386/780), self.buttons_img["down"]),
                        "join" : Button((self.screen_width * 0.3, self.screen_height * 625/780), self.buttons_img["join"], text="Join", base_color="black", font_size= int(self.screen_height/720 * 64)),
                        "host" : Button((self.screen_width * 0.51, self.screen_height * 625/780), self.buttons_img["host"], text="Host", base_color="black", font_size= int(self.screen_height/720 * 64)),
                        "next" : Button((self.screen_width * 0.42125, self.screen_height * 0.69), self.buttons_img["next"], text="Next", base_color="black", font_size= int(self.screen_height/720 * 64)),
                        "create" : Button((self.screen_width * 0.42125, self.screen_height * 0.79), self.buttons_img["create"], text="Create", base_color="black", font_size= int(self.screen_height/720 * 64)),
                        "katarenga" : Button((self.screen_width * 0.4125, self.screen_height * 0.25), text="Katarenga", base_color="black", font_size= int(self.screen_height/720 * 64)),
                        "congress" : Button((self.screen_width * 0.42, self.screen_height * 0.40), text="Congress", base_color="black", font_size= int(self.screen_height/720 * 64)),
                        "isolation" : Button((self.screen_width * 0.42, self.screen_height * 0.55), text="Isolation", base_color="black", font_size= int(self.screen_height/720 * 64))
                        }


###################################################################################################


    def create_server_collision(self):
        '''Store in a list Rect item that correspond to server's selection'''      

        self.servers_collision = []

        # Get background rect dimensions
        bg_x, bg_y = self.screen_width * 0.11, self.screen_height * 0.17
        bg_width, bg_height = self.screen_width * 0.6, self.screen_height * 0.57

        slot_height = bg_height / 4
        slot_y_start = bg_y

        for i in range(4):
            adjusted_width = bg_width * 0.9
            adjusted_height = slot_height * 0.8
            adjusted_x = bg_x + (bg_width - adjusted_width) / 2              # Center horizontally
            adjusted_y = slot_y_start + (slot_height - adjusted_height) / 2  # Center vertically
            self.servers_collision.append(pygame.Rect(adjusted_x, adjusted_y, adjusted_width, adjusted_height))
            slot_y_start += slot_height


###################################################################################################


    def check_server_selection(self, pos):
        '''Return the a integer depending on which server was selected (1,2,3 or 4. It's not index based)'''

        for i, collision in enumerate(self.servers_collision):
            if collision.collidepoint(pos):
                return i
            
        return -1        # No server was selected


###################################################################################################


    def display_servers_background(self):
        '''Used to display the gray rectangle acting as the area for server display'''

        if not hasattr(self, "servers_background"):
            # Using a surface trick because Rect object doesn't handle alpha channel
            self.servers_background = pygame.Surface((self.screen_width * 0.6, self.screen_height * 0.57), pygame.SRCALPHA)
            pygame.draw.rect(self.servers_background, (114, 114, 114, 125), self.servers_background.get_rect(), border_radius=20)

        self.screen.blit(self.servers_background, (self.screen_width * 0.11, self.screen_height * 0.17))


###################################################################################################


    def display_title(self):
        '''Simply blit the "Available Games" on top of the screen'''

        if not hasattr(self, "title"):
            self.title = self.font.render("Available Games", True, (0, 0, 0))
            self.title_surface = self.title.get_rect(center = (self.screen_width//2, self.screen_height * 0.1))

        self.screen.blit(self.title, self.title_surface)


###################################################################################################

    
    def refresh_servers(self):
        '''Refresh the current list of server every 5s'''

        while self.running:

            with self.lock:                             # Lock before modifying shared resources (Same as self.lock.acquire() + self.lock.release())
                self.servers = self.client.get_server()
                self.servers_amount = len(self.servers)
                self.page_amount = ceil(self.servers_amount/4)

            time.sleep(5)
            print(self.servers)


###################################################################################################


    def display_servers(self):
        '''Used to blit at max 4 availables servers, based on current page'''

        font = pygame.font.Font("Assets/Source_files/fonts/font.ttf", int(self.screen_height/720 * 32))

        with self.lock:                                 # Lock before reading shared data
            servers_to_display = self.servers[self.current_page * 4: self.current_page * 4 + 4]
        
        for i, (server, collision) in enumerate(zip(servers_to_display, self.servers_collision)):
            # Draw the seperation line between the servers
            if i < len(servers_to_display) - 1:
                pygame.draw.line(self.screen, (0, 0, 0), (collision.x, collision.y + collision.height), (collision.x + collision.width, collision.y + collision.height), 2)

            # Draw the selection area
            if self.selected_server == self.current_page * 4 + i:
                smaller_rect = collision.scale_by(0.8)
                pygame.draw.rect(self.screen, (217, 217, 217), smaller_rect, border_radius=10)

            text_surface = font.render(f"{server[2]}    Gamemode : {server[3]}", True, "black")
            text_rect = text_surface.get_rect(center=collision.center)  # Center text inside the collision box
            self.screen.blit(text_surface, text_rect)


###################################################################################################


    def set_waiting(self, waiting):
        '''Set the current state of the client to waiting or not'''

        self.waiting = waiting

######################################################################################################################################################################################################


if __name__ == "__main__":
    #Using this command before because in real usage, it will be "setup"
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))                          # Another commune resolution is 1280 x 720
    Online_hub(screen).run()