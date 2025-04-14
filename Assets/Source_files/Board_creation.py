from pygame import *
from Sub_class.tile import *
from Sub_class.button import *
from Sub_class.region import *
from Game_UI import *
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
        self.selected_region = None                         # Store a Region object

        # Contain all regions that the board contain
        self.board = {
            "top_left": None,
            "top_right": None,
            "bottom_left": None,
            "bottom_right": None
        }

        self.region_collision = None
        self.board_positions = None

        self.load_assets()
        self.resize_assets()

        # Creation of things that need to be display
        self.font = font.Font("Assets/Source_files/fonts/font.ttf", int(self.screen_height * 0.1))
        self.create_buttons()


###################################################################################################


    def run(self):
        '''"Mainloop for this class'''

        self.running = True

        while self.running:
            self.handle_events()
            self.render_screen()
            pygame.display.flip()
            self.clock.tick(self.fps)


###################################################################################################


    def render_screen(self):
        '''Renders all UI elements on the screen.'''

        self.screen.blit(self.background_img, (0,0))
        self.display_title("Board Creation", self.font)
        self.display_region()
        self.display_board()
        self.display_selected_region(pygame.mouse.get_pos())

        # Update buttons
        for button in self.buttons.values():
            button.update(self.screen)


###################################################################################################


    def handle_events(self):
        '''Handles all pygame events.'''

        self.handle_hovering()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click()
            elif event.type == pygame.KEYDOWN:
                self.handle_key_press(event)


###################################################################################################


    def handle_hovering(self):
        '''Allow the next button to change style'''

        if self.buttons["next"].checkInput(pygame.mouse.get_pos()) and self.board_full():
            self.next_img.set_alpha(400)
        else:
            self.next_img.set_alpha(200)


###################################################################################################


    def board_full(self):
        '''Return a boolean that indicate if every board's region is fulfilled'''

        full = True
        for region in self.board.values():
            full = full and region
        return full


###################################################################################################


    def handle_mouse_click(self):
        '''Handles mouse click events.'''
        x, y = pygame.mouse.get_pos()

        if self.buttons["back"].checkInput((x,y)):
            self.running = False

        elif self.buttons["up"].checkInput((x, y)) and self.current_region_index > 0:
            self.switch_region(-1)

        elif self.buttons["down"].checkInput((x, y)) and self.current_region_index < self.region_amount - 1:
            self.switch_region(1)

        elif self.region_collision.collidepoint((x, y)):
            self.selected_region = copy.deepcopy(self.current_region)

        elif index := self.board_region((x,y)):
            self.board[index] = self.selected_region
            self.selected_region = None

        elif self.buttons["next"].checkInput(pygame.mouse.get_pos()) and self.board_full():
            # USE THE COMBINATION METHOD HERE, RETURN THE LIST WITH ALL TILES (NO MORE REGIONS)
            self.running = GamesUI(self.screen, self.combine_regions(), "katarenga", ["francis", "patrick"], "solo")

        else:
            self.selected_region = None


###################################################################################################


    def handle_key_press(self, event):
        '''Handles keypress events.'''
        if event.key == pygame.K_r and self.selected_region:
            self.animate_rotation()
        elif event.key == pygame.K_t and self.selected_region:
            self.animate_flip()


###################################################################################################


    def switch_region(self, direction):
        '''Switches the currently displayed region.'''

        self.selected_region = None
        old_region = self.current_region
        self.current_region_index += direction
        self.current_region = load_region(self.current_region_index)
        self.animate_slide(old_region, direction)


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
        self.next_img.set_alpha(200)


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

        self.buttons = {
            "back": Button((self.screen_width * 0.03, self.screen_height * 0.80), self.back_img),
            "up": Button((self.screen_width * 0.72, self.screen_height * 0.19), self.up_img),
            "down": Button((self.screen_width * 0.72, self.screen_height * 0.67), self.down_img),
            "next": Button((self.screen_width * 0.3, self.screen_height * 0.80), self.next_img, "Next", base_color="black", font_size=int(self.screen_height/720 * 64)),
        }



###################################################################################################


    def display_title(self, txt, font):
        '''Display the given text at the top of the screen'''

        self.title = font.render(txt, True, "black")
        self.title_pos = self.title.get_rect(midtop=(self.screen.get_width() // 2, 30))
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

        # Topleft corner of the board
        x = self.screen_width * 0.21875
        y = self.screen_height * 0.21

        # Place board collision if they don't exist
        if self.board_positions is None:
            self.board_positions = {
                "top_left": pygame.Rect(x, y, self.region_side, self.region_side),
                "top_right": pygame.Rect(x + self.region_side, y, self.region_side, self.region_side),
                "bottom_left": pygame.Rect(x, y + self.region_side, self.region_side, self.region_side),
                "bottom_right": pygame.Rect(x + self.region_side, y + self.region_side, self.region_side, self.region_side)
            }

        self.screen.blit(self.board_background_img, (x, y))

        for position, region in self.board.items():
            if region:
                region.display(self.screen, self.tiles_img, self.board_positions[position].topleft, self.tiles_side)



###################################################################################################


    def board_region(self, pos):
        '''Return the name of the board region where the mouse is currently at'''

        for (key, value) in self.board_positions.items():
            if value.collidepoint(pos):
                return key
        return 0


###################################################################################################


    def display_selected_region(self, mouse_pos):
        '''Display the selected region at the mouse position with transparency.'''

        if self.selected_region:
            # First check for placeholder
            placeholder = False

            if index := self.board_region(mouse_pos):
                    placeholder = True
                    transparent_surface = pygame.Surface((self.region_side, self.region_side), pygame.SRCALPHA)
                    self.selected_region.display(transparent_surface, self.tiles_img, (0, 0), self.tiles_side)
                    transparent_surface.set_alpha(150)                 
                    self.screen.blit(transparent_surface, self.board_positions[index].topleft)

            # Else, check for default mouse pos
            if not placeholder:
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
            self.display_region()
            self.screen.blit(rotated_image, rect.topleft)

            pygame.display.flip()
            self.clock.tick(self.fps)  # Maintain frame rate

        # Apply the actual rotation after animation
        self.selected_region.rotate()
        pygame.event.clear()



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
            scale_factor = cos(progress * pi / 2)
            
            # Scale the image vertically
            if scale_factor > 0:                                    # Prevent zero height which would cause errors
                scaled_image = pygame.transform.smoothscale(
                    original_image, (self.region_side, int(self.region_side * scale_factor))
                )
                rect = scaled_image.get_rect(center=(x, y))
                
                self.redraw_static_elements()
                self.display_region()
                
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
            scale_factor = sin(progress * pi / 2)
            
            # Scale the image vertically
            if scale_factor > 0:                                    # Prevent zero height which would cause errors
                scaled_image = pygame.transform.smoothscale(
                    flipped_image, (self.region_side, int(self.region_side * scale_factor))
                )
                rect = scaled_image.get_rect(center=(x, y))
                
                self.redraw_static_elements()
                self.display_region()
                
                # Overlay the scaled image
                self.screen.blit(scaled_image, rect.topleft)
                
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.event.clear()



###################################################################################################


    def animate_slide(self, old_region, direction):
        '''Animation that slides the old region up/down while shrinking and the new region slides in while growing.'''

        anim_duration = 500  # Animation duration in milliseconds
        start_time = pygame.time.get_ticks()

        # Load the old and new region images
        old_image = pygame.Surface((self.region_side, self.region_side), pygame.SRCALPHA)
        old_region.display(old_image, self.tiles_img, (0, 0), self.tiles_side)

        new_image = pygame.Surface((self.region_side, self.region_side), pygame.SRCALPHA)
        self.current_region.display(new_image, self.tiles_img, (0, 0), self.tiles_side)

        x_center = self.screen_width * 0.72 + self.region_side // 2
        y_start = self.screen_height * 0.365 if direction == 1 else self.screen_height * 0.365 + self.region_side
        y_center = self.screen_height * 0.365 + self.region_side // 2
        y_movement = self.region_side // 2 * direction

        while True:
            current_time = pygame.time.get_ticks() - start_time
            if current_time >= anim_duration:
                break
            
            progress = current_time / anim_duration  # Progress (0 to 1)
            eased_progress = 1 - pow(1 - progress, 3)  # Smooth ease-in
            self.redraw_static_elements()

            # Shrinking old region while moving it
            old_scale = 1 - eased_progress
            if old_scale > 0:
                old_scaled = pygame.transform.smoothscale(
                    old_image, (int(self.region_side * old_scale), int(self.region_side * old_scale))
                )
                old_rect = old_scaled.get_rect(center=(x_center, y_center + y_movement * eased_progress))
                self.screen.blit(old_scaled, old_rect.topleft)

            # Growing new region while moving it
            new_scaled = pygame.transform.smoothscale(
                new_image, (int(self.region_side * eased_progress), int(self.region_side * eased_progress))
            )
            new_rect = new_scaled.get_rect(center=(x_center, y_start + y_movement * eased_progress))
            self.screen.blit(new_scaled, new_rect.topleft)

            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.event.clear()



###################################################################################################


    def redraw_static_elements(self):
        '''Often used to refresh in animation function'''
        
        self.screen.blit(self.background_img, (0, 0))
        self.display_title("Board Creation", self.font)
        self.display_board()
        for button in self.buttons.values():
            button.update(self.screen)


###################################################################################################


    def combine_regions(self):
        '''Return the board itself (bidimensional list), combining all Regions specified in the current board dictionary.'''

        # Ensure all regions are filled
        if not all(self.board.values()):
            raise ValueError("All regions must be filled before combining.")

        # First, combine top_left and top_right
        top = [self.board["top_left"].get()[i] + self.board["top_right"].get()[i] for i in range(4)]

        # Same for bottom
        bot = [self.board["bottom_left"].get()[i] + self.board["bottom_right"].get()[i] for i in range(4)]

        # Finally, combine top and bottom parts
        combined = top + bot

        # Convert raw data into Tile objects
        return [[Tile(cell.get_deplacement(), cell.get_pawn(), cell.get_collision()) for cell in row] for row in combined]


######################################################################################################################################################################################################


if __name__ == "__main__":
    #Using this command before because in real usage, it will be "setup"
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    #screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    Delete_region(screen).run()
