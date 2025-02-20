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
        self.current_page = 0
        self.selected_region = None                         # Store an integer that correspond to the region_index in the currently loaded regions
        self.max_page = ceil(self.region_amount / 4)        # Displaying 4 by 4, if region_amount % 4 != 0 we got an extra page for up to 3 regions

        self.load_regions(0)                                # Load first regions
        self.load_assets()
        self.resize_assets()

        self.create_buttons()
        self.initialize_regions_pos()

        #Mainloop
        while running:
           
            x, y = pygame.mouse.get_pos()

            # Handle hovering animation
            if self.selected_region:
                self.button_delete.changeColor((x,y), "green")
            else:
                self.button_delete.changeColor((x,y), "red")

            # Display background
            self.screen.blit(self.background_img, (0,0))

            # Refreshing all current regions and display potential overlay
            self.region_overlay()
            self.refresh_regions()

            # Refreshing all buttons
            self.button_up.update(self.screen)                                                        
            self.button_delete.update(self.screen)
            self.button_down.update(self.screen)
            self.button_back.update(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if(self.button_back.checkInput((x,y))):
                        running = False
                    # Check if a region was clicked
                    self.select_region((x,y))
                

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


###################################################################################################


    def resize_assets(self):
        '''Resize all assets used in this menu'''

        # Background rescale
        self.background = pygame.transform.smoothscale(self.background_img, (self.screen_width, self.screen_height))
        
        # Tiles rescale
        self.tiles_side = self.screen_width * 0.05
        self.region_side = self.tiles_side * 4

        for key in self.tiles_img:
            self.tiles_img[key] = pygame.transform.smoothscale(self.tiles_img[key], (self.tiles_side, self.tiles_side))

        # Buttons_icons rescale
        self.button_height = int(self.screen_height * 0.22)
        self.button_width = int(self.screen_width * 0.1875)
        self.button_img = pygame.transform.smoothscale(self.button_img, (self.button_width, self.button_height))
        self.up_img = pygame.transform.smoothscale(self.up_img, (self.button_width, self.button_height))
        self.down_img = pygame.transform.smoothscale(self.down_img, (self.button_width, self.button_height))

        # Back_icon rescale
        self.back_img =  pygame.transform.smoothscale(self.back_img, (100/720 * self.screen_height, 100/720 * self.screen_height))


###################################################################################################


    def create_buttons(self):
        '''Initialize all buttons needed with their respective coordinates'''

        self.button_back = Button((self.screen_width * 0.03, self.screen_height * 0.78), self.back_img)

        # Starting topleft corner
        y = self.screen_height * 0.09
        x = self.screen_width * 0.76
          
        self.button_up = Button((x,y), self.up_img)
        y += self.screen_height * 0.065 + self.button_height
        self.button_delete = Button((x,y), self.button_img, text="Delete\nRegion", base_color="white", font_size= int(self.screen_height/720 * 64))
        y += self.screen_height * 0.065 + self.button_height
        self.button_down = Button((x,y), self.down_img)


###################################################################################################


    def refresh_regions(self):
        '''Display on the screen all the current regions'''

        i = 0
        for region in self.current_regions:
            region.display(self.screen, self.tiles_img, self.regions_pos[i], self.tiles_side)
            i += 1
        

###################################################################################################


    def load_regions(self, page):
        '''Store in a list, all the currently displayed regions depending on the "page" to load (the page°n group of 4 regions)'''

        self.current_regions = []

        with open("Assets/Source_files/Data_files/region.json", 'r') as f:
            regions_list = json.load(f)

            # Check if we can read 4 regions
            maxi = self.current_page * 4 + 4
            maxi = maxi if maxi < self.region_amount else self.region_amount
            
            for i in range(self.current_page * 4, maxi):
                self.current_regions.append(Region.from_dict(regions_list[i]))


###################################################################################################


    def initialize_regions_pos(self):
        '''Generate all the value that will indicates the top-left corner of the '''

        self.regions_pos = [0, 0, 0, 0]
        self.regions_pos[0] = (self.screen_width * 0.2, self.screen_height * 0.11)
        self.regions_pos[1] = (self.screen_width * 0.46, self.screen_height * 0.11)
        self.regions_pos[2] = (self.screen_width * 0.2, self.screen_height * 0.53)
        self.regions_pos[3] = (self.screen_width * 0.46, self.screen_height * 0.53)

        #Collision rectangle to detect click on the region (using Topleft-corner)
        self.region_collision = []
        self.region_collision.append(pygame.Rect(self.screen_width * 0.2, self.screen_height * 0.11, self.region_side, self.region_side))
        self.region_collision.append(pygame.Rect(self.screen_width * 0.46, self.screen_height * 0.11, self.region_side, self.region_side))
        self.region_collision.append(pygame.Rect(self.screen_width * 0.2, self.screen_height * 0.53, self.region_side, self.region_side))
        self.region_collision.append(pygame.Rect(self.screen_width * 0.46, self.screen_height * 0.53, self.region_side, self.region_side))


###################################################################################################


    def select_region(self, pos):
        '''Check if you are in a region and update the selected_region'''

        self.selected_region = None  # Reset selection first

        for i in range(len(self.current_regions)):              # Iterate over existing regions (prevent issues when fewer are loaded)
            if self.region_collision[i].collidepoint(pos):
                self.selected_region = i
            

###################################################################################################


    def region_overlay(self):
        '''Add a visual outline to the selected_region'''

        if self.selected_region is not None:
            topleft = self.region_collision[self.selected_region].topleft
            new_topleft = (topleft[0] - 10, topleft[1] - 10)
            pygame.draw.rect(self.screen, (178, 158, 135), pygame.Rect(new_topleft[0], new_topleft[1], self.region_side + 20, self.region_side + 20))
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(new_topleft[0], new_topleft[1], self.region_side + 20, self.region_side + 20), 2)


######################################################################################################################################################################################################


if __name__ == "__main__":
    #Using this command before because in real usage, it will be "setup"
    pygame.init()
    # screen = pygame.display.set_mode((1280, 720))
    screen = pygame.display.set_mode((1720, 1080))
    Delete_region(screen)