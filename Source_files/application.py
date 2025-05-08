from Source_files.Menu.Intro import Intro
from Source_files.Menu.Menu import Menu
import pygame



class Game():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Game")



    def run(self):

        Intro(self.screen)
        Menu(self.screen).run_menu()






Game().run()