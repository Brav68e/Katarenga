from Sub_class.tile import *
from Sub_class.button import *
from Sub_class.region import *
import pygame
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
            self.button_database.update(self.screen)
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
                        print("back")

                    elif self.button_database.checkInput((x,y)):
                        print("data")

                    elif self.button_save.checkInput((x,y)):
                        print("save")
                        # Check if the current region is fulfilled with Tile
                        if self.region_complete():
                            region = Region(self.region)
                            region = Region.to_dict(region)

                            # Check if the region isn't already register
                            if not search_region(region):
                                save_region(region)
                


                # Handle hovering animation
                self.button_database.changeColor((x,y))
                self.button_save.changeColor((x,y))
                

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
        
        self.region_img = pygame.image.load("Assets/Source_files/Images/Create_region/region.png").convert()
        self.background_img = pygame.image.load("Assets/Source_files/Images/menu/imgs/Background.png").convert()
        self.button_img = pygame.image.load("Assets/Source_files/Images/Create_region/button.png").convert_alpha()
        self.back_img = pygame.image.load("Assets/Source_files/Images/Create_region/left_arrow.png").convert_alpha()



###################################################################################################


    def load_backgrounds(self):
        '''Load all the backgrounds img with specific size'''

        self.background_img = pygame.transform.smoothscale(self.background_img, (self.screen_width, self.screen_height))



###################################################################################################


    def load_tiles(self):
        '''Load all the tiles img with specific size'''

        self.tiles_side = self.region_side/4

        for key in self.tiles_img:
            self.tiles_img[key] = pygame.transform.smoothscale(self.tiles_img[key], (self.tiles_side, self.tiles_side))


###################################################################################################


    def load_region(self):
        '''Load the current region img with specific size'''

        # Set up the region dimensions relative to the screen size
        self.region_side = int(self.screen_width * 0.40)
        self.region_x = (self.screen_width * 0.0625)                      # Top-Left Corner   
        self.region_y = (self.screen_height * 0.083)
        self.region_img = pygame.transform.smoothscale(self.region_img, (self.region_side, self.region_side))
 
        #Collision rectangle to detect click on the region
        self.region_collision = pygame.Rect(self.region_x, self.region_y, self.region_side, self.region_side)


###################################################################################################


    def load_buttons(self):
        '''Load all the buttons's img with proper dimension'''

        self.button_height = int(self.screen_height * 0.22)
        self.button_width = int(self.screen_width * 0.1875)

        self.button_img = pygame.transform.smoothscale(self.button_img, (self.button_width, self.button_height))
        self.back_img =  pygame.transform.smoothscale(self.back_img, (100/720 * self.screen_height, 100/720 * self.screen_height))


#########################################################################################################################################################################################################################################################################################################


    def initialize_aside_tiles(self):
        '''Used to create ONCE all the aside tiles used for selection'''

        self.tiles_aside = []
        patterns = ["horse", "rook", "bishop", "king", "queen"]
        tile_x = int(self.screen_width * 0.55)                          # Tiles first "row axe"
        tile_y = int(self.screen_height * 0.083)                        # Starting Y

        for i in range(3):
            collision_rect = pygame.Rect(tile_x, tile_y, self.tiles_side, self.tiles_side)                    # Create a collision surfaces -> detect click later on
            current = Tile(patterns[i], collision=collision_rect)                                                       # Create a tile object
            self.tiles_aside.append(current)

            # Determine the next X
            tile_x += self.tiles_side + int(self.screen_width * 0.06)                                            # 6% screen width interval

        # Setting a new "row axe"
        tile_x = int(self.screen_width * 0.61)
        tile_y = int(self.screen_height * 0.36)

        for j in range(3,5):
            collision_rect = pygame.Rect(tile_x, tile_y, self.tiles_side, self.tiles_side)                    # Create a collision surfaces -> detect click later on
            current = Tile(patterns[j], collision=collision_rect)                                                       # Create a tile object
            self.tiles_aside.append(current)

            # Determine the next X
            tile_x += self.tiles_side + int(self.screen_width * 0.06)                                            # 6% screen height interval


###################################################################################################


    def blit_aside_tiles(self):
        '''Blit on screen all the aside tiles used for selection'''

        for tile in self.tiles_aside:
            self.screen.blit(self.tiles_img[tile.get_deplacement()], tile.get_collision().topleft)


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

            highlight = pygame.Rect(topleft[0]-add, topleft[1]-add, self.tiles_side+add*2, self.tiles_side+add*2)
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

        self.button_back_menu = Button((self.screen_width * 0.03, self.screen_height * 0.82), self.back_img)

        # Starting topleft corner
        y = self.screen_height * 0.65
        x = self.screen_width * 0.52
          
        self.button_save = Button((x,y), self.button_img, text="Save\nCurrent", base_color="white", font_size= int(self.screen_height/720 * 64), hovering_color="green")
        x += self.screen_width * 0.06 + self.button_width
        self.button_database = Button((x,y), self.button_img, text="Your\nRegions", base_color="white", font_size= int(self.screen_height/720 * 64), hovering_color="green")


###################################################################################################


    def region_fulfilled(self):
        '''Return a boolean that indicate if the current region is completly filled with Tile'''

        complete = True
        for row in self.region:
            for ele in row:
                complete = complete and isinstance(ele, Tile)

        return complete


###################################################################################################


    def region_complete(self):
        '''Return a boolean that indicate if the current region match the rules conditions to be save'''

        result = True

        if self.region_fulfilled():
            # Let's count every type of tile
            amount = {"rook": 0, "bishop": 0, "horse": 0, "king": 0, "queen": 0}
            for row in self.region:
                for tile in row:
                    amount[tile.get_deplacement()] += 1
            
            # Check that each type is either 0 or 4
            for type in amount:
                if amount[type] == 0 or amount[type] == 4:
                    result = result and True
                else:
                    result = result and False

        else:
            result = False

        return result


###################################################################################################


if __name__ == "__main__":
    #Using this command before because in real usage, it will be "setup"
    pygame.init()
    # screen = pygame.display.set_mode((1280, 720))
    screen = pygame.display.set_mode((1720, 1080))
    Create_region(screen)