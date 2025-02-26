from pygame import *
from Sub_class.tile import *
from Sub_class.button import *
from Sub_class.region import *
import json
from math import ceil, pow, cos, pi, sin
import copy



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
        self.region_collision = None
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
            self.display_board()

            # Refreshing all buttons
            self.button_up.update(self.screen)                                                        
            self.button_next.update(self.screen)
            self.button_down.update(self.screen)
            self.button_back.update(self.screen)

            # Display the selected region following the mouse
            self.display_selected_region((x, y))

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

                    # Check for Region selection
                    elif self.region_collision.collidepoint((x, y)):
                        self.selected_region = copy.deepcopy(self.current_region)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.selected_region:
                        self.animate_rotation()
                    elif event.key == pygame.K_t and self.selected_region:
                        self.animate_flip()             

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
        self.board_background_img = pygame.image.load("Assets/Source_files/Images/Create_region/region.png").convert()
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
        self.tiles_side = int(self.screen_width * 0.039)              # int prevent float number which create space between tiles
        self.region_side = self.tiles_side * 4

        for key in self.tiles_img:
            self.tiles_img[key] = pygame.transform.smoothscale(self.tiles_img[key], (self.tiles_side, self.tiles_side))

        # Board background
        self.board_background_img = pygame.transform.smoothscale(self.board_background_img, (self.region_side * 2, self.region_side * 2))

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

        self.button_back = Button((self.screen_width * 0.03, self.screen_height * 0.80), self.back_img)
        self.button_up = Button((self.screen_width * 0.72, self.screen_height * 0.19), self.up_img)
        self.button_down = Button((self.screen_width * 0.72, self.screen_height * 0.67), self.down_img)
        self.button_next = Button((self.screen_width * 0.3, self.screen_height * 0.80), self.next_img, "Next", base_color="black", font_size= int(self.screen_height/720 * 64))


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
        y = self.screen_height * 0.365
        self.current_region.display(self.screen, self.tiles_img, (x,y), self.tiles_side)
        if self.region_collision is None:
            self.region_collision = pygame.Rect(x, y, self.region_side, self.region_side)


###################################################################################################


    def display_board(self):
        '''Display the board itself and regions placed on him'''

        # Topleft corner
        x = self.screen_width * 0.21875
        y = self.screen_height * 0.21

        self.screen.blit(self.board_background_img, (x,y))


###################################################################################################


    def display_selected_region(self, mouse_pos):
        '''Display the selected region at the mouse position with transparency.'''

        if self.selected_region:
            x, y = mouse_pos
            transparent_surface = pygame.Surface((self.region_side, self.region_side), pygame.SRCALPHA)
            self.selected_region.display(transparent_surface, self.tiles_img, (0, 0), self.tiles_side)
            transparent_surface.set_alpha(150)                 
            self.screen.blit(transparent_surface, (x - self.region_side // 2, y - self.region_side // 2))


###################################################################################################


    def animate_rotation(self):
        '''Animation rotating the selected region smoothly.'''
           
        anim_duration = 500                                 # Animation duration in milliseconds
        start_time = pygame.time.get_ticks()

        original_image = pygame.Surface((self.region_side, self.region_side), pygame.SRCALPHA)
        self.selected_region.display(original_image, self.tiles_img, (0, 0), self.tiles_side)
        original_image.set_alpha(150)

        while True:
            pygame.event.pump()                             # Needed since there is no pygame.event.get()
            x, y = pygame.mouse.get_pos()
            current_time = pygame.time.get_ticks() - start_time
            if current_time >= anim_duration:
                break

            progress = current_time / anim_duration                         # 0 to 1 (percentage of animation completed)
            eased_progress = 1 - pow(1 - progress, 3)                       # Ease-in cubic function   f(progress) = 1 - (1-progress)³
            angle = -eased_progress * 90

            rotated_image = pygame.transform.rotate(original_image, angle)
            rect = rotated_image.get_rect(center=(x, y))

            # Refresh static elements and blit the region
            self.redraw_static_elements()
            self.screen.blit(rotated_image, rect.topleft)

            pygame.display.flip()
            self.clock.tick(self.fps)  # Maintain frame rate

        # Apply the actual rotation after animation
        self.selected_region.rotate()



###################################################################################################


    def animate_flip(self):
        '''Animation that shrinks the selected region to zero height, flips it, then expands it back.'''
        
        anim_duration = 800                                         # Animation duration in milliseconds
        start_time = pygame.time.get_ticks()

        # Create a surface with the original image
        original_image = pygame.Surface((self.region_side, self.region_side), pygame.SRCALPHA)
        self.selected_region.display(original_image, self.tiles_img, (0, 0), self.tiles_side)
        original_image.set_alpha(150) 
        
        # First phase: Shrink to zero height
        while True:
            pygame.event.pump()                                     # Needed since there is no pygame.event.get()
            x, y = pygame.mouse.get_pos()
            
            current_time = pygame.time.get_ticks() - start_time
            if current_time >= anim_duration / 2:
                break
                
            progress = current_time / (anim_duration / 2)
            
            # Smooth easing function (ease-in)
            eased_progress = 1 - cos(progress * pi / 2)             # 0 to 1, starts slow, ends fast
            scale_factor = 1 - eased_progress
            
            # Scale the image vertically
            if scale_factor > 0:                                    # Prevent zero height which would cause errors
                scaled_image = pygame.transform.smoothscale(
                    original_image, (self.region_side, int(self.region_side * scale_factor))
                )
                rect = scaled_image.get_rect(center=(x, y))
                
                self.redraw_static_elements()
                
                # Overlay the scaled image
                self.screen.blit(scaled_image, rect.topleft)
                
            pygame.display.flip()
            self.clock.tick(self.fps)
        
        # Apply the flip at the invisible point
        self.selected_region.flip()
        
        # Create a new surface with the flipped image
        flipped_image = pygame.Surface((self.region_side, self.region_side), pygame.SRCALPHA)
        self.selected_region.display(flipped_image, self.tiles_img, (0, 0), self.tiles_side)
        flipped_image.set_alpha(150)
        
        # Second phase: Expand from zero back to full height
        start_time = pygame.time.get_ticks()
        while True:
            pygame.event.pump()
            x, y = pygame.mouse.get_pos()
            
            current_time = pygame.time.get_ticks() - start_time
            if current_time >= anim_duration / 2:
                break
                
            progress = current_time / (anim_duration / 2)
            
            # Smooth easing function (ease-out)
            eased_progress = sin(progress * pi / 2)
            scale_factor = eased_progress
            
            # Scale the image vertically
            if scale_factor > 0:                                    # Prevent zero height which would cause errors
                scaled_image = pygame.transform.smoothscale(
                    flipped_image, (self.region_side, int(self.region_side * scale_factor))
                )
                rect = scaled_image.get_rect(center=(x, y))
                
                self.redraw_static_elements()
                
                # Overlay the scaled image
                self.screen.blit(scaled_image, rect.topleft)
                
            pygame.display.flip()
            self.clock.tick(self.fps)



###################################################################################################


    def redraw_static_elements(self):
        '''Often used to refresh in animation function'''
        
        self.screen.blit(self.background_img, (0, 0))
        self.display_title("Board Creation", self.font)
        self.display_region()
        self.display_board()
        self.button_up.update(self.screen)
        self.button_next.update(self.screen)
        self.button_down.update(self.screen)
        self.button_back.update(self.screen)


######################################################################################################################################################################################################


if __name__ == "__main__":
    #Using this command before because in real usage, it will be "setup"
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    #screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    Delete_region(screen)