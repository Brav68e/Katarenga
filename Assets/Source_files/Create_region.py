from Sub_class.tile import *
from Sub_class.button import *
from Sub_class.region import *
import pygame
from datetime import datetime
import json
import os



 

class Create_region():

    def __init__(self, screen, controller = None):

        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.region = [[0 for i in range(4)] for j in range(4)]
        self.selected_tile = None

        self.clock = pygame.time.Clock()
        self.fps = 60
        running = True

        #Loading Images & Sound
        self.load_assets()

        #GUI part
        self.load_region()                                  # Resize all the assets with new property
        self.load_tiles()
        self.load_buttons()
        self.load_backgrounds()
        self.initialize_aside_tiles()                       # Create all the tiles objects ONCE (performance issues)

        #Button creation
        self.create_buttons()                                                                                                                                                


        #Mainloop for this menu
        while running:

            self.screen.blit(self.background_img, (0,0))                                                # Display background
            self.screen.blit(self.region_img, (self.region_x, self.region_y))                           # Display region
            self.highlight_selected()                                                                   # Add a visual for the selected_tile
            self.blit_aside_tiles()                                                                     # Display Aside Tiles
            self.blit_tiles()                                                                           # OnBoard tiles
            self.button_save.update(self.screen)                                                        # Refreshing all buttons
            self.button_rules.update(self.screen)
            self.button_back_menu.update(self.screen)

            pygame.display.flip()
            x, y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.select_tile(x, y)
                    self.place_tile(x, y)

                    if self.button_back_menu.checkInput((x,y)):
                        pass

                    elif self.button_rules.checkInput((x,y)):
                        self.show_rules()

                    elif self.button_save.checkInput((x,y)):
                        # Check if the current region is fulfilled with Tile
                        if self.region_complete():
                            region = Region(self.region)
                            region = Region.to_dict(region)

                            # Check if the region isn't already register
                            if not search_region(region):
                                region["region_img"] = self.get_region_img()
                                save_region(region)
                


                # Handle hovering animation
                self.button_back_menu.changeColor((x,y))
                self.button_rules.changeColor((x,y))
                self.button_save.changeColor((x,y))
                

            # Limit framerate
            self.clock.tick(self.fps)
    

###################################################################################################


    def load_assets(self):
        '''Load once all the assets needed in this menu'''

        self.tiles_aside_img = {"horse" : pygame.image.load("Assets/Source_files/Images/Create_region/horse.png").convert(),
                                "rook" : pygame.image.load("Assets/Source_files/Images/Create_region/rook.png").convert(),
                                "bishop": pygame.image.load("Assets/Source_files/Images/Create_region/bishop.png").convert(),
                                "king": pygame.image.load("Assets/Source_files/Images/Create_region/king.png").convert(),
                                "queen": pygame.image.load("Assets/Source_files/Images/Create_region/queen.png").convert()
                                }
        
        self.tiles_img = {"horse" : pygame.image.load("Assets/Source_files/Images/Create_region/horse.png").convert(),
                          "rook" : pygame.image.load("Assets/Source_files/Images/Create_region/rook.png").convert(),
                          "bishop": pygame.image.load("Assets/Source_files/Images/Create_region/bishop.png").convert(),
                          "king": pygame.image.load("Assets/Source_files/Images/Create_region/king.png").convert(),
                          "queen": pygame.image.load("Assets/Source_files/Images/Create_region/queen.png").convert()
                          }
        
        self.region_img = pygame.image.load("Assets/Source_files/Images/Create_region/region.png")
        self.background_img = pygame.image.load("Assets/Source_files/Images/Create_region/background.png")
        self.rules_img = pygame.image.load("Assets/Source_files/Images/Create_region/rules.png")
        self.button_img = pygame.image.load("Assets/Source_files/Images/Create_region/button.png")
        self.button_back_edit_img = pygame.image.load("Assets/Source_files/Images/Create_region/close_rules.png")



###################################################################################################


    def load_backgrounds(self):
        '''Load all the backgrounds img with specific size'''

        self.background_img = pygame.transform.scale(self.background_img, (self.screen_width, self.screen_height))

        self.rules_y = int(self.screen_height * 0.075)
        self.rules_x = int(self.screen_width * 0.075)
        self.rules_img = pygame.transform.scale(self.rules_img, (self.screen_width * 0.85, self.screen_height * 0.85))



###################################################################################################


    def load_tiles(self):
        '''Load all the tiles img with specific size'''

        self.tile_aside_side = int(self.screen_height * 0.125)                      # 12.5% of screen height
        self.tiles_side = self.region_side/4

        for key in self.tiles_aside_img:
            self.tiles_aside_img[key] = pygame.transform.scale(self.tiles_aside_img[key], (self.tile_aside_side, self.tile_aside_side))

        for key in self.tiles_img:
            self.tiles_img[key] = pygame.transform.scale(self.tiles_img[key], (self.tiles_side, self.tiles_side))


###################################################################################################


    def load_region(self):
        '''Load the current region img with specific size'''

        # Set up the region dimensions relative to the screen size
        self.region_side = int(self.screen_height * 0.6)                # Sides are based on screen height
        self.region_x = (self.screen_width * 0.19)                      # Top-Left Corner   
        self.region_y = (self.screen_height * 0.1)
        self.region_img = pygame.transform.scale(self.region_img, (self.region_side, self.region_side))
 
        #Collision rectangle to detect click on the region
        self.region_collision = pygame.Rect(self.region_x, self.region_y, self.region_side, self.region_side)


###################################################################################################


    def load_buttons(self):
        '''Load all the buttons's img with proper dimension'''

        self.button_height = int(self.screen_height * 0.10)
        self.button_width = int(self.screen_width * 0.20)

        self.button_save_img = pygame.transform.scale(self.button_img, (self.button_width, self.button_height))
        self.button_back_edit_img =  pygame.transform.scale(self.button_back_edit_img, (self.button_height, self.button_height))


#########################################################################################################################################################################################################################################################################################################


    def initialize_aside_tiles(self):
        '''Used to create ONCE all the aside tiles used for selection'''

        self.tiles_aside = []
        patterns = ["horse", "rook", "bishop", "king", "queen"]
        tile_x = int(self.screen_width * 0.7)                          # Tiles first "column axe"
        tile_y = int(self.screen_height * 0.2)                        # Starting Y

        for i in range(3):
            collision_rect = pygame.Rect(tile_x, tile_y, self.tile_aside_side, self.tile_aside_side)                    # Create a collision surfaces -> detect click later on
            current = Tile(patterns[i], collision=collision_rect)                                                       # Create a tile object
            self.tiles_aside.append(current)

            # Determine the next Y
            tile_y += self.tile_aside_side + int(self.screen_height * 0.025)                                            # 2.5% screen height interval

        # Setting a new "column axe"
        tile_x = int(self.screen_width * 0.85)
        tile_y = int(self.screen_height * 0.2)

        for j in range(3,5):
            collision_rect = pygame.Rect(tile_x, tile_y, self.tile_aside_side, self.tile_aside_side)                    # Create a collision surfaces -> detect click later on
            current = Tile(patterns[j], collision=collision_rect)                                                       # Create a tile object
            self.tiles_aside.append(current)

            # Determine the next Y
            tile_y += self.tile_aside_side + int(self.screen_height * 0.025)                                            # 2.5% screen height interval


###################################################################################################


    def blit_aside_tiles(self):
        '''Blit on screen all the aside tiles used for selection'''

        for tile in self.tiles_aside:
            self.screen.blit(self.tiles_aside_img[tile.get_deplacement()], tile.get_collision().topleft)


###################################################################################################


    def blit_tiles(self):
        '''Blit all the currently placed tiles on the edit board'''

        for i in range(len(self.region)):
            for j in range(len(self.region)):
                if tile := self.region[i][j]:
                    x, y = self.region_collision.topleft
                    self.screen.blit(self.tiles_img[tile.get_deplacement()], (x+(j*self.region_side/4), y+(i*self.region_side/4)))


###################################################################################################


    def select_tile(self, x, y):
        '''Update the "selected_tile" attribut'''

        # For every tiles aside
        for tile in self.tiles_aside:
            # Check if the click is inside the tile 'collision'
            if tile.get_collision().collidepoint(x,y):
                self.selected_tile = tile


###################################################################################################


    def highlight_selected(self):
        '''Add a visual background to the current selected tile'''

        if self.selected_tile:
            surface = self.selected_tile.get_collision()
            topleft = surface.topleft
            add = int(self.screen_height * 0.01)

            highlight = pygame.Rect(topleft[0]-add, topleft[1]-add, self.tile_aside_side+add*2, self.tile_aside_side+add*2)
            pygame.draw.rect(self.screen, "green", highlight)


###################################################################################################


    def place_tile(self, x, y):
        '''Handle placement of selected tile on the region editor'''

        if self.selected_tile and self.region_collision.collidepoint(x,y):
            top_left_corner = self.region_collision.topleft
            column = int((x - top_left_corner[0]) / (self.region_side / 4))
            line = int((y - top_left_corner[1]) / (self.region_side / 4))

            self.region[line][column] = Tile(self.selected_tile.get_deplacement())


###################################################################################################


    def create_buttons(self):
        '''Initialize all buttons needed with their respective coordinates'''

        # Starting topleft corner
        y = self.screen_height * 0.8
        x = self.screen_width * 0.15

        self.button_back_menu = Button((x,y), self.button_img, text_input="Back to Menu", base_color="white", font_size= int(self.screen_height*0.03), hovering_color="green")
        x += self.button_width
        self.button_rules = Button((x,y), self.button_img, text_input="Show Rules", base_color="white", font_size= int(self.screen_height*0.03), hovering_color="green")
        x += self.button_width
        self.button_save = Button((x,y), self.button_img, text_input="Save Region", base_color="white", font_size= int(self.screen_height*0.03), hovering_color="green")

        # Rules interface button
        x, y = (self.screen_width * 0.75, self.screen_height * 0.25)
        self.button_back_edit = Button((x,y), self.button_back_edit_img)


###################################################################################################


    def show_rules(self):
        '''Create a overlapping menu that handle a rules interface'''

        # Basically a secondary mainloop
        rules = True

        while rules:

            self.screen.blit(self.rules_img, (self.rules_x, self.rules_y))
            self.button_back_edit.update(self.screen)

            pygame.display.flip()
            x, y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    rules = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_back_edit.checkInput((x,y)):
                        rules = False
                
                # Handle hovering animation
                self.button_back_edit.changeColor((x,y))
                

            # Limit framerate
            self.clock.tick(self.fps)


######################################################################################################################################################################################################


    def get_region_img(self):
        '''Create a new img file based on the current region created and return the path of the file'''

        # Creating a new surface that represent the region
        region_img = pygame.Surface((self.region_side, self.region_side))

        for y, row in enumerate(self.region):
            for x, col in enumerate(row):
                tile_img = self.tiles_img[self.region[x][y].get_deplacement()]
                region_img.blit(tile_img, (x * self.tiles_side, y * self.tiles_side))


        # Then save it with a datetime id for unicity
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"Assets/Source_files/Images/Regions/region_{timestamp}.png"

        pygame.image.save(region_img, file_path)

        return file_path


###################################################################################################


    def region_complete(self):
        '''Return a boolean that indicate if the current region is completly filled with Tile'''

        complete = True
        for row in self.region:
            for ele in row:
                complete = complete and isinstance(ele, Tile)

        return complete


###################################################################################################


if __name__ == "__main__":
    #Using this command before because in real usage, it will be "setup"
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))                          # Another commune resolution is 1280 x 720
    Create_region(screen)