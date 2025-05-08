import pygame
import math


class Intro():

    def __init__(self, screen):
        
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.load_assets()
        self.run()
        


    
    def load_assets(self):

        self.background = pygame.image.load("Assets/Source_files/Images/menu/imgs/Background.png").convert()
        self.logo = pygame.image.load("Assets/Source_files/Images/Other/smart.png").convert_alpha()


        self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))
        self.logo = pygame.transform.scale(self.logo, (self.screen.get_width() * 740/1280, self.screen.get_height() * 560/720))




    def run(self):

        anim_duration = 5000                                                 # Animation duration in milliseconds
        start_time = pygame.time.get_ticks()

        # Animation
        while True:

            current_time = pygame.time.get_ticks() - start_time
            if current_time >= anim_duration:
                break

            progress = current_time / anim_duration                         # 0 to 1 (percentage of animation completed)
            eased_progress = -(math.cos(math.pi * progress) - 1) / 2;                       

            transparency = int(255 * (eased_progress))                        # 0 to 255 (0 = fully transparent, 255 = fully opaque)

            self.screen.blit(self.background, (0, 0))
            self.logo.set_alpha(transparency)
            rect = self.logo.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
            self.screen.blit(self.logo, rect.topleft)

            pygame.display.flip()
            self.clock.tick(self.fps)
        

############################################

if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Game")
    Intro(screen)