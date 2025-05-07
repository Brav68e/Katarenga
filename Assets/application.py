from Source_files.Intro import Intro
import pygame



class Game():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Game")

        Intro(self.screen)






