import pygame, sys, os
from Source_files.Sub_class.button import Button
from Source_files.Assets.Board_handling.Create_region import *
from Source_files.Assets.Board_handling.Create_region import Create_region

class Menu:
    def __init__(self, root):
        self.screen = root
        pygame.display.set_caption("Menu")
        
        # Dimensions of the screen
        self.screen_width = 1280
        self.screen_height = 720

        background = pygame.image.load("Assets/Source_files/Images/menu/imgs/Background.png")
        self.BG = pygame.transform.smoothscale(background, (1280, 720))
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.GREEN = (50, 205, 50)

        self.current_page = "Katarenga"  # default page
        self.buttons = []
        self.icon_buttons = []  # Buttons for the bottom menu icons
        self.volume = 0.5  # Default volume
        self.is_dragging = False  # Drag and Drop
        
        # Init slider
        self.slider_width = 800
        self.slider_height = 20
        self.slider_x = 640 - self.slider_width // 2
        self.slider_y = 200
        button_radius = 25
        self.slider_rect = pygame.Rect(self.slider_x, self.slider_y - button_radius, 
                                  self.slider_width, self.slider_height + 2 * button_radius)
        
        self.setup_buttons()

        # Init audio
        pygame.mixer.init()
        
        # Load and play background music
        try:
            pygame.mixer.music.load(r"Assets\Source_files\Sounds\soundtrack.mp3")
            pygame.mixer.music.play(-1)  # Playing the music in a loop
            pygame.mixer.music.set_volume(self.volume)
        except Exception as e:
            print(f"Error loading music file: {e}")

    def get_font(self, size):
        return pygame.font.Font(r"Assets/Source_files/fonts/font.ttf", size)
    
    def get_font2(self, size):
        return pygame.font.Font(r"Assets/Source_files/fonts/font2.ttf", size)

    def setup_buttons(self):
        # main buttons
        path_test = "Assets/Source_files/Images/menu/imgs/button_asset.png"
        if self.current_page == "Katarenga":
            self.buttons = [
               Button(pos=(580, 250), image=None, text="Solo", base_color="black", font_size= int(self.screen_height/720 * 64)),
               Button(pos=(440, 350), image=None, text="Local Multiplayer", base_color="black", font_size= int(self.screen_height/720 * 64)),
               Button(pos=(430, 450), image=None, text="Online Multiplayer", base_color="black", font_size= int(self.screen_height/720 * 64))
            ]
        elif self.current_page == "Settings":
            self.buttons = [
                Button(pos=(540, 250),image=None, text="Options", base_color="black", font_size= int(self.screen_height/720 * 64)),
               Button(pos=(570, 350), image=None, text="Rules", base_color="black", font_size= int(self.screen_height/720 * 64)),
               Button(pos=(490, 450), image=None, text="Create tiles", base_color="black", font_size= int(self.screen_height/720 * 64))
            ]
        elif self.current_page == "Options":
            # No default buttons for Options page
            self.buttons = []
        elif self.current_page == "Rules":
            # Buttons for rules selection
            self.buttons = [
                Button(pos=(220, 300), image=None, text="Katarenga", base_color="black", font_size=int(self.screen_height/720 * 64)),
                Button(pos=(530, 300), image=None, text="Congress", base_color="black", font_size=int(self.screen_height/720 * 64)),
                Button(pos=(820, 300), image=None, text="Isolation", base_color="black", font_size=int(self.screen_height/720 * 64))
            ]
        else:
            self.buttons = [
                Button(pos=(580, 250),image=None, text="Solo", base_color="black", font_size= int(self.screen_height/720 * 64)),
               Button(pos=(440, 350), image=None, text="Local Multiplayer", base_color="black", font_size= int(self.screen_height/720 * 64)),
               Button(pos=(430, 450), image=None, text="Online Multiplayer", base_color="black", font_size= int(self.screen_height/720 * 64))
            ]

        # Path to the icon images
        icon_images = [
            "Assets/Source_files/Images/menu/icons/tour2.png",
            "Assets/Source_files/Images/menu/icons/plateau2.png",
            "Assets/Source_files/Images/menu/icons/I2.png",
            "Assets/Source_files/Images/menu/icons/settings2.png"
        ]

        # Create icon buttons
        icon_positions = [(350, 670), (550, 670), (750, 670), (950, 670)]
        self.icon_buttons = []  # Reset the list

        for index, (pos, image_path) in enumerate(zip(icon_positions, icon_images)):
            # Expend the button if it corresponds to the current page
            expanded = (
                (self.current_page == "Katarenga" and index == 0) or
                (self.current_page == "Congress" and index == 1) or
                (self.current_page == "Isolation" and index == 2) or
                (self.current_page == "Settings" and index == 3) or
                (self.current_page == "Options" and index == 3) or
                (self.current_page == "Rules" and index == 3)
            )
            icon_button = IconButton(
                pos,
                "",
                self.get_font(20),
                "#FFFFFF",
                "#888888",
                icon_image=image_path,
                expanded=expanded
            )
            self.icon_buttons.append(icon_button)

    def draw_title(self):
        # Display the title text
        title_text = self.get_font(120).render(self.current_page, True, "#514b4b")
        title_rect = title_text.get_rect(center=(640, 120))
        self.screen.blit(title_text, title_rect)

    def menu_buttons(self):
         # Background for the bottom menu with rounded corners
        s = pygame.Surface((800, 200), pygame.SRCALPHA)
        s.fill((0, 0, 0, 0))  # Clear with transparent background
        
        # Draw rounded rectangle on the surface
        rect = pygame.Rect(0, 0, 800, 200)  # You can adjust this value for more/less rounded corners
        pygame.draw.rect(s, (*self.BLACK, 180), rect, border_radius=15)
        
        # Blit the surface to the screen
        self.screen.blit(s, (240, 620))

        # Draw icons
        for button in self.icon_buttons:
            button.draw(self.screen)

    def draw_volume_slider(self):
        # "Volume"
        volume_text = self.get_font(60).render("Volume", True, "#514b4b")
        volume_rect = volume_text.get_rect(center=(640, 120))
        self.screen.blit(volume_text, volume_rect)

        # Volume bar (background)
        pygame.draw.rect(self.screen, self.GRAY, 
                        (self.slider_x, self.slider_y, self.slider_width, self.slider_height),
                        border_radius=10)
        
        # Volume bar (active)
        active_width = int(self.slider_width * self.volume)
        pygame.draw.rect(self.screen, self.GREEN, 
                        (self.slider_x, self.slider_y, active_width, self.slider_height),
                        border_radius=10)
        
        # Button for volume control
        button_radius = 25
        button_x = self.slider_x + active_width
        button_y = self.slider_y + self.slider_height // 2
        pygame.draw.circle(self.screen, self.GREEN, (button_x, button_y), button_radius)
    
    def draw_display_mode(self):
        # "Display Mode"
        display_text = self.get_font(60).render("Display Mode", True, "#514b4b")
        display_rect = display_text.get_rect(center=(640, 350))
        self.screen.blit(display_text, display_rect)
        
        # Buttons for display mode
        self.display_buttons = [
            Button(pos=(380, 450), image=None, text="Windowed", base_color="black", font_size= int(self.screen_height/720 * 64)),
            Button(pos=(680, 450), image=None, text="Fullscreen", base_color="black", font_size= int(self.screen_height/720 * 64))
        ]
        
        # Update and display the display mode buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.display_buttons:
            button.changeColor(mouse_pos, "grey")
            button.update(self.screen)

    def handle_volume_input(self, pos, is_click=False):
        if self.slider_rect.collidepoint(pos):
            if is_click:
                self.is_dragging = True
            
            if self.is_dragging:
                # Calculate the new volume based on the slider position
                rel_x = max(0, min(pos[0] - self.slider_x, self.slider_width))
                self.volume = rel_x / self.slider_width
                if self.volume < 0.01:
                    self.volume = 0.0
                # Update the volume
                pygame.mixer.music.set_volume(self.volume)

    def update(self):
        # Display the background
        
        self.screen.blit(self.BG, (0, 0))
        
        # If on the Options page, display the volume slider and display mode buttons
        if self.current_page == "Options":
            self.draw_volume_slider()
            self.draw_display_mode()
        else:
            # Display the title
            self.draw_title()
            
            # Claim the mouse position
            mouse_pos = pygame.mouse.get_pos()
            
            # Update and display the main buttons
            for button in self.buttons:
                button.changeColor(mouse_pos, "grey")
                button.update(self.screen)

        # Display bottom menu icons
        self.menu_buttons()

    def handle_icon_clicks(self, mouse_pos):
        """Handle clicks on the menu icon buttons"""
        for index, button in enumerate(self.icon_buttons):
            if button.checkInput(mouse_pos):
                # If we're in rules display mode, restore the original update method
                if hasattr(self, 'original_update') and self.current_page == "Rules_Display":
                    self.update = self.original_update
                
                if index == 0:
                    self.current_page = "Katarenga"
                elif index == 1:
                    self.current_page = "Congress"
                elif index == 2:
                    self.current_page = "Isolation"
                elif index == 3:
                    self.current_page = "Settings"
                self.setup_buttons()  # Update buttons to reflect the new page
                return True
        return False

    def handle_settings_buttons(self, mouse_pos):
        """Handle clicks on the settings page buttons"""
        for i, button in enumerate(self.buttons):
            if button.checkInput(mouse_pos):
                if i == 0:  # "Option" button
                    self.current_page = "Options"
                    self.setup_buttons()
                    return True
                elif i == 1:  # "Rules" button
                    self.current_page = "Rules"
                    self.setup_buttons()
                    return True
                elif i == 2:  # "Create Tiles" button
                    self.launch_create_region()
                    return True
        return False
    
    def rules_display_update(self):
        self.screen.blit(self.BG, (0, 0))
        
        # Display title
        title_text = self.get_font(80).render(self.rules_title, True, "#514b4b")
        title_rect = title_text.get_rect(center=(640, 80))
        self.screen.blit(title_text, title_rect)
        
        # Display rules text with line wrapping
        font = self.get_font2(30)
        y_offset = 150
        for line in self.rules_text.split('\n'):
            if line.strip():  # Skip empty lines
                text = font.render(line, True, (0, 0, 0))
                self.screen.blit(text, (100, y_offset))
            y_offset += 35
        
        # Add back button
        back_button = Button(pos=(50, 650), image=None, text="Retour", base_color="black", 
                            font_size=int(self.screen_height/720 * 50))
        
        # Check if mouse is hovering over back button
        mouse_pos = pygame.mouse.get_pos()
        back_button.changeColor(mouse_pos, "grey")
        back_button.update(self.screen)
        
        # Check if back button is clicked
        if pygame.mouse.get_pressed()[0]:
            if back_button.checkInput(mouse_pos):
                self.current_page = "Rules"
                self.setup_buttons()
                self.update = self.original_update
        
        # Display bottom menu icons
        self.menu_buttons()
    
    def handle_rules_buttons(self, mouse_pos):
        for i, button in enumerate(self.buttons):
            if button.checkInput(mouse_pos):
                if self.current_page == "Rules_Display":
                    # Return to rules selection page
                    self.current_page = "Rules"
                    self.setup_buttons()
                    self.update = self.original_update  # Restore original update method
                    return True
                    
                elif i == 0:  # "Katarenga Rules" button
                    # Load and display Katarenga rules
                    try:
                        with open("Assets/Source_files/Rules/katarenga_rules.txt", "r", encoding="utf-8") as file:
                            rules_content = file.read()
                        
                        self.current_page = "Rules_Display"
                        self.original_update = self.update  # Store original update method
                        self.update = self.rules_display_update  # Set custom update method
                        
                        # Store the rules content for display
                        self.rules_text = rules_content
                        self.rules_title = "Katarenga Rules"
                    except FileNotFoundError:
                        print("Rules file not found")
                    except Exception as e:
                        print(f"Error loading rules: {e}")
                    return True
                elif i == 1:  # "Congress Rules" button
                    try:
                        with open("Assets/Source_files/Rules/congress_rules.txt", "r", encoding="utf-8") as file:
                            rules_content = file.read()
                        
                        self.current_page = "Rules_Display"
                        self.original_update = self.update
                        self.update = self.rules_display_update
                        
                        # Store the rules content for display
                        self.rules_text = rules_content
                        self.rules_title = "Congress Rules"
                        
                    except FileNotFoundError:
                        print("Rules file not found")
                    except Exception as e:
                        print(f"Error loading rules: {e}")
                    return True
                elif i == 2:  # "Isolation Rules" button
                    try:
                        with open("Assets/Source_files/Rules/isolation_rules.txt", "r", encoding="utf-8") as file:
                            rules_content = file.read()
                        
                        self.current_page = "Rules_Display"
                        self.original_update = self.update
                        self.update = self.rules_display_update
                        
                        # Store the rules content for display
                        self.rules_text = rules_content
                        self.rules_title = "Isolation Rules"

                    except FileNotFoundError:
                        print("Rules file not found")
                    except Exception as e:
                        print(f"Error loading rules: {e}")
                    return True
        return False
        
    def launch_create_region(self):
        """Launch the Create_region module"""
        # Save volume state before quitting
        volume_level = self.volume
        pygame.mixer.music.stop()

        try:
            # Import the create_region function
            screen = pygame.display.set_mode((1280, 720))
            # Run the create_region function
            Create_region(screen)
            
            # After the create_region function returns, reinitialize the display for menu
            pygame.display.set_mode((1280, 720))
        except Exception as e:
            print(f"Error launching Create_region: {e}")
            # Ensure the display is reset if there's an error
            pygame.display.set_mode((1280, 720))
        
        # Restore music and volume after return
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(volume_level)
        
    def handle_display_options(self, mouse_pos):
        """Handle clicks on display mode buttons"""
        if hasattr(self, 'display_buttons'):
            for i, button in enumerate(self.display_buttons):
                if button.checkInput(mouse_pos):
                    if i == 0:  # Windowed mode
                        pygame.display.set_mode((1280, 720))
                        return True
                    elif i == 1:  # Fullscreen mode
                        pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
                        return True
        return False
    
    def get_usernames(self, mode):
        """Display a username input screen based on the selected mode."""
        num_fields = 1 if mode in ["Solo", "Online Multiplayer"] else 2
        prompt = "Enter Username" if mode in ["Solo", "Online Multiplayer"] else "Enter Usernames"
        username_input = UsernameInput(self.screen, prompt, num_fields)
        result = username_input.run()
        if result == "back":
            return None  # Return None to indicate going back to the main menu
        return username_input
        
    def handle_mouse_button_down(self, event):
        """Handle mouse button down events"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Check for clicks on the icons
        if self.handle_icon_clicks(mouse_pos):
            return
        
        # Check for clicks on the main buttons in Settings page
        if self.current_page == "Settings":
            if self.handle_settings_buttons(mouse_pos):
                return
                
        # Check for clicks on the rules buttons
        if self.current_page == "Rules":
            if self.handle_rules_buttons(mouse_pos):
                return
        
        # Handle clicks on the volume bar
        if self.current_page == "Options":
            self.handle_volume_input(mouse_pos, True)
            
            # Handle clicks on display mode buttons
            self.handle_display_options(mouse_pos)
        
        if self.current_page == "Katarenga":
            if self.buttons[0].checkInput(mouse_pos):  # Solo
                usernames = self.get_usernames("Solo")
                # truc des username pour le jeu
            elif self.buttons[1].checkInput(mouse_pos):  # Local Multiplayer
                usernames = self.get_usernames("Local Multiplayer")
                # truc des username pour le jeu
            elif self.buttons[2].checkInput(mouse_pos):  # Online Multiplayer
                usernames = self.get_usernames("Online Multiplayer")
                # truc des username pour le jeu
            
    def handle_mouse_motion(self, event):
        """Handle mouse motion events"""
        # Update volume if adjusting the volume bar
        if self.current_page == "Options" and self.is_dragging:
            self.handle_volume_input(pygame.mouse.get_pos())

    def run_menu(self):
        """Main function to run the menu"""

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_button_down(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.is_dragging = False
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event)
            
            self.update()
            pygame.display.update()
        
        pygame.quit()
        sys.exit()

class IconButton():
    def __init__(self, pos, text_input, font, base_color, hovering_color, icon_image=None, expanded=False):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.width = 120
        self.height = 70 if not expanded else 120  # Expend the button if expanded is true
        self.rect = pygame.Rect(self.x_pos - self.width//2, self.y_pos - self.height//2, self.width, self.height)
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.current_color = base_color
        self.icon_image = icon_image
        if self.icon_image:
            self.icon_image = pygame.image.load(icon_image)
            self.icon_image = pygame.transform.smoothscale(self.icon_image, (65, 65))  # resize icon

    def draw(self, screen):
        # Draw the button rectangle
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)

        # Draw image in the center of the button
        if self.icon_image:
            image_rect = self.icon_image.get_rect(center=self.rect.center)
            screen.blit(self.icon_image, image_rect)

    def checkInput(self, position):
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        if self.checkInput(position):
            self.current_color = self.hovering_color
        else:
            self.current_color = self.base_color



if __name__ == "__main__":
    pygame.init()
    Menu(pygame.display.set_mode((1280, 720))).run_menu()