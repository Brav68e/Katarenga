import sys
import pygame
from Sub_class.button import Button
from Sub_class.player import Player

class UsernameInput:
    def __init__(self, screen, prompt, num_fields=1):
        self.screen = screen
        self.prompt = prompt
        self.num_fields = num_fields
        self.font = pygame.font.Font("Assets/Source_files/fonts/font.ttf", 40)
        self.label_font = pygame.font.Font("Assets/Source_files/fonts/font.ttf", 30)
        self.input_boxes = [pygame.Rect(440, 300 + i * 100, 500, 70) for i in range(num_fields)]  # Adjusted for multiple fields
        self.labels = ["Player 1", "Player 2"][:num_fields]  # Labels for the input boxes
        self.max_text_width = 480  # Maximum width for text inside the input box
        self.usernames = [f"Player {i + 1}" for i in range(num_fields)]  # Default usernames
        self.active = [False] * num_fields
        self.back_arrow = Button(pos=(70, 600), image=pygame.image.load("Assets/Source_files/Images/Delete_region/left_arrow.png").convert_alpha(), text=None)
        self.next_button = Button(
            pos=(580, 500),  # Adjusted position for "Next" button
            image=pygame.transform.smoothscale(
                pygame.image.load("Assets/Source_files/Images/Create_region/next.png").convert_alpha(),
                (180, 60)
            ),
            text="Next",
            base_color="black",
            font_size=40
        )
        self.background = pygame.image.load("Assets/Source_files/Images/menu/imgs/Background.png").convert()
        self.background = pygame.transform.smoothscale(self.background, screen.get_size())

    def run(self):
        """Run the username input UI."""
        running = True
        while running:
            self.screen.blit(self.background, (0, 0))  
            title_text = self.font.render(self.prompt, True, (0, 0, 0))
            self.screen.blit(title_text, (440, 200))

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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_arrow.checkInput(event.pos):
                        return "back"  # Return "back" to indicate going back to the main menu
                    for i, box in enumerate(self.input_boxes):
                        self.active[i] = box.collidepoint(event.pos)
                    if self.next_button.checkInput(event.pos) and all(self.usernames):
                        running = False
                elif event.type == pygame.KEYDOWN:
                    for i, active in enumerate(self.active):
                        if active:
                            if event.key == pygame.K_BACKSPACE:
                                self.usernames[i] = self.usernames[i][:-1]
                            else:
                                # Check if the new text fits within the input box
                                new_text = self.usernames[i] + event.unicode
                                text_width = self.font.size(new_text)[0]
                                if text_width <= self.max_text_width:
                                    self.usernames[i] = new_text

            pygame.display.flip()

        return self.usernames  # Return the updated usernames
