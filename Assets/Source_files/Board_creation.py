from pygame import *
from Sub_class.tile import *
from Sub_class.button import *
from Sub_class.region import *
import json
from math import ceil




class Delete_region():

    def __init__(self, screen, controller = None):
        
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.clock = pygame.time.Clock()
        self.fps = 60
        running = True

        self.region_amount = region_amount()
        self.current_region_index = 0
        self.current_region = load_region(0)
        self.selected_region = None                         # Store a Region object
        self.board = [None, None, None, None]               # Contain all 4 regions that make a board. 0 : Top_left, 1 : Top_right, 2 : Bottom_left, 3 : Bottom_right

        self.load_assets()
        self.resize_assets()

        # Creation of things that need to be display
        self.font = font.Font("Assets/Source_files/fonts/font.ttf", int(self.screen_height * 0.1))
        self.create_buttons()


        #Mainloop
        while running:
           
            x, y = pygame.mouse.get_pos()

            # Display background
            self.screen.blit(self.background_img, (0,0))
            self.display_title("Board Creation", self.font)

            # Display the aside_region and the board
            self.display_region()
            # self.display_board()

            # Refreshing all buttons
            self.button_up.update(self.screen)                                                        
            self.button_next.update(self.screen)
            self.button_down.update(self.screen)
            self.button_back.update(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Exit
                    if(self.button_back.checkInput((x,y))):
                        running = False
                    
                    # Check for Up/Down buttons
                    elif self.button_up.checkInput((x, y)) and self.current_region_index > 0:
                        self.current_region_index -= 1
                        self.current_region = load_region(self.current_region_index)

                    elif self.button_down.checkInput((x, y)) and self.current_region_index < self.region_amount - 1:
                        self.current_region_index += 1
                        self.current_region = load_region(self.current_region_index)


                                    

            # Limit framerate
            self.clock.tick(self.fps)




###################################################################################################




    def load_assets(self):
        '''Load once all the assets needed in this menu'''
        
        self.tiles_img = {"horse" : pygame.image.load("Assets/Source_files/Images/Create_region/horse.png").convert(),
                          "rook" : pygame.image.load("Assets/Source_files/Images/Create_region/rook.png").convert(),
                          "bishop": pygame.image.load("Assets/Source_files/Images/Create_region/bishop.png").convert(),
                          "king": pygame.image.load("Assets/Source_files/Images/Create_region/king.png").convert(),
                          "queen": pygame.image.load("Assets/Source_files/Images/Create_region/queen.png").convert()
                          }
        
        self.background_img = pygame.image.load("Assets/Source_files/Images/menu/imgs/Background.png").convert()
        self.button_img = pygame.image.load("Assets/Source_files/Images/Create_region/button.png").convert_alpha()
        self.back_img = pygame.image.load("Assets/Source_files/Images/Delete_region/left_arrow.png").convert_alpha()
        self.up_img = pygame.image.load("Assets/Source_files/Images/Delete_region/up_arrow.png").convert_alpha()
        self.down_img = pygame.image.load("Assets/Source_files/Images/Delete_region/down_arrow.png").convert_alpha()
        self.next_img = pygame.image.load("Assets/Source_files/Images/Create_region/next.png").convert_alpha()


###################################################################################################


    def resize_assets(self):
        '''Resize all assets used in this menu'''

        # Background rescale
        self.background_img = pygame.transform.smoothscale(self.background_img, (self.screen_width, self.screen_height))
        
        # Tiles rescale
        self.tiles_side = self.screen_width * 0.05
        self.region_side = self.tiles_side * 4

        for key in self.tiles_img:
            self.tiles_img[key] = pygame.transform.smoothscale(self.tiles_img[key], (self.tiles_side, self.tiles_side))

        # Buttons_icons rescale
        self.button_height = int(self.screen_height * 0.15)
        self.button_width = int(self.screen_width * 0.15625)
        self.button_img = pygame.transform.smoothscale(self.button_img, (self.button_width, self.button_height))
        self.up_img = pygame.transform.smoothscale(self.up_img, (self.button_width, self.button_height))
        self.down_img = pygame.transform.smoothscale(self.down_img, (self.button_width, self.button_height))
        self.next_img = pygame.transform.smoothscale(self.next_img, (self.button_width, self.button_height))

        # Back_icon rescale
        self.back_img = pygame.transform.smoothscale(self.back_img, (100/720 * self.screen_height, 100/720 * self.screen_height))


###################################################################################################


    def create_buttons(self):
        '''Initialize all buttons needed with their respective coordinates'''

        self.button_back = Button((self.screen_width * 0.03, self.screen_height * 0.78), self.back_img)
        self.button_up = Button((self.screen_width * 0.72, self.screen_height * 0.19), self.up_img)
        self.button_down = Button((self.screen_width * 0.72, self.screen_height * 0.67), self.down_img)
        self.button_next = Button((self.screen_width * 0.3, self.screen_height * 0.75), self.next_img, "Next", base_color="black", font_size= int(self.screen_height/720 * 64))


###################################################################################################


    def display_title(self, txt, font):
        '''Display the given text at the top of the screen'''

        self.title = font.render(txt, True, "black")
        self.title_pos = self.title.get_rect(midtop=(screen.get_width() // 2, 30))
        self.screen.blit(self.title, self.title_pos)


###################################################################################################


    def display_region(self):
        '''Used to blit the current_region aside, between the 2 buttons'''

        x = self.screen_width * 0.72
        y = self.screen_height * 0.33
        self.current_region.display(self.screen, self.tiles_img, (x,y), self.tiles_side)




######################################################################################################################################################################################################


if __name__ == "__main__":
    #Using this command before because in real usage, it will be "setup"
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    #screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    Delete_region(screen)