import pygame
from Source_files.Sub_class.button import Button
from Source_files.Assets.Sounds.button_sound import ButtonSound

class InGameMenu:
    def __init__(self, screen, screen_width, screen_height, clock, fps):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.clock = clock
        self.fps = fps
        self.font = pygame.font.Font("Source_files/Assets/Fonts/font.ttf", int(self.screen_height * 0.07))
        self.popup = pygame.image.load("Source_files/Assets/Images/Menu/popup.png").convert_alpha()
        self.popup = pygame.transform.scale(self.popup, (int(self.screen_width * 0.8), int(self.screen_height * 0.6)))

    def show(self):
        """Affiche le menu pause et retourne True si quitter, False si reprendre"""
        rect = self.popup.get_rect(center=(self.screen_width // 2, self.screen_height // 2))

        title = self.font.render("Pause", False, (0, 0, 0))
        title_rect = title.get_rect(center=(self.popup.get_width() // 2, int(self.popup.get_height() * 0.22)))

        btn_w = int(self.popup.get_width() * 0.7)
        btn_h = int(self.popup.get_height() * 0.18)
        btn_quit = Button((rect.x + self.popup.get_width() // 2 - btn_w // 2, rect.y + int(self.popup.get_height() * 0.45)), None, text="Quitter la partie", base_color="black", font_size=int(self.screen_height/720*48))
        btn_resume = Button((rect.x + self.popup.get_width() // 2 - btn_w // 2, rect.y + int(self.popup.get_height() * 0.7)), None, text="Reprendre", base_color="black", font_size=int(self.screen_height/720*48))
        btn_quit.rect.width = btn_w
        btn_quit.rect.height = btn_h
        btn_resume.rect.width = btn_w
        btn_resume.rect.height = btn_h

        while True:

            mouse_pos = pygame.mouse.get_pos()
            # Highlight the buttons if the mouse is over them
            if btn_quit.checkInput(mouse_pos):
                btn_quit.base_color = (220, 60, 60)
            else:
                btn_quit.base_color = (0, 0, 0)

            if btn_resume.checkInput(mouse_pos):
                btn_resume.base_color = (60, 220, 60)
            else:
                btn_resume.base_color = (0, 0, 0)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_quit.checkInput(event.pos):
                        ButtonSound.play()
                        return True
                    if btn_resume.checkInput(event.pos):
                        ButtonSound.play()
                        return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
            self.screen.blit(self.popup, rect.topleft)
            self.popup.blit(title, title_rect)
            btn_quit.update(self.screen)
            btn_resume.update(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)
