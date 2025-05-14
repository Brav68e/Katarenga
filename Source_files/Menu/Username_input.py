import sys
import pygame
from Source_files.Sub_class.button import Button
from Source_files.Sub_class.player import Player

class UsernameInput:
    def __init__(self, screen, prompt, num_fields=1):
        self.screen = screen
        self.prompt = prompt
        self.num_fields = num_fields
        self.font = pygame.font.Font("Source_files/Assets/fonts/font.ttf", 40)
        self.label_font = pygame.font.Font("Source_files/Assets/fonts/font.ttf", 30)
        self.input_boxes = [pygame.Rect(440, 300 + i * 100, 500, 70) for i in range(num_fields)]  # Adjusted for multiple fields
        self.labels = ["Player 1", "Player 2"][:num_fields]  # Labels for the input boxes
        self.max_characters = 20  # Maximum number of characters allowed for usernames
        self.usernames = [f"Player {i + 1}" for i in range(num_fields)]  # Default usernames
        self.active = [False] * num_fields
        self.back_arrow = Button(pos=(70, 600), image=pygame.image.load("Source_files/Assets/Images/Utility/left_arrow.png").convert_alpha(), text="")
        self.next_button = Button(
            pos=(self.screen.get_width() // 2 - 90, 500),  
            image=pygame.transform.smoothscale(
                pygame.image.load("Source_files/Assets/Images/Utility/next.png").convert_alpha(),
                (180, 60)
            ),
            text="Next",
            base_color="black",
            font_size=40
        )
        self.background = pygame.image.load("Source_files/Assets/Images/Menu/Background.png").convert()
        self.background = pygame.transform.smoothscale(self.background, screen.get_size())

    def run(self):
        """Run the username input UI."""
        running = True
        while running:
            self.screen.blit(self.background, (0, 0))  
            title_text = self.font.render(self.prompt, True, (0, 0, 0))
            self.screen.blit(title_text, (self.screen.get_width() // 2 - 120, 200))  # Align "Enter Username" with "Next" button

            for i, box in enumerate(self.input_boxes):
                # Draw labels
                label_text = self.label_font.render(self.labels[i], True, (0, 0, 0))
                self.screen.blit(label_text, (box.x - 120, box.y + 20))  

                # Draw input boxes
                color = (200, 200, 200) if not self.active[i] else (220, 220, 220)  # Use lighter gray when active
                pygame.draw.rect(self.screen, color, box, border_radius=15)  
                text_surface = self.font.render(self.usernames[i], True, (0, 0, 0))  
                self.screen.blit(text_surface, (box.x + 10, box.y + 20))  

            # Update buttons
            self.back_arrow.update(self.screen)
            self.next_button.update(self.screen)

            # Apply a rounded gray overlay if not all usernames are filled
            if not all(self.usernames):
                overlay = pygame.Surface(self.next_button.image.get_size(), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 0))  # Transparent background
                pygame.draw.rect(overlay, (150, 150, 150, 100), overlay.get_rect(), border_radius=15)  # Semi-transparent gray
                self.screen.blit(overlay, self.next_button.rect.topleft)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_arrow.checkInput(event.pos):
                        return "back"  # Return "back" to indicate going back to the main menu
                    if self.next_button.checkInput(event.pos) and all(self.usernames):
                        running = False
                    for i, box in enumerate(self.input_boxes):
                        self.active[i] = box.collidepoint(event.pos)
                elif event.type == pygame.KEYDOWN:
                    for i, active in enumerate(self.active):
                        if active:
                            if event.key == pygame.K_BACKSPACE:
                                self.usernames[i] = self.usernames[i][:-1]
                            elif len(self.usernames[i]) < self.max_characters:  # Limit by character count
                                self.usernames[i] += event.unicode

            pygame.display.flip()

        return self.usernames