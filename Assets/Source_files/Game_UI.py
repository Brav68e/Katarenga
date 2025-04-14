from Katarenga import *
import pygame



class GamesUI():

    def __init__(self, screen, grid, gamemode, usernames, type):

        self.game = Games(grid, usernames[0], usernames[1])
        self.game.init_pawns()
        
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()

        self.clock = pygame.time.Clock()
        self.fps = 60


        #Loading Images & Sound
        self.load_assets()
        self.resize_assets()

        if gamemode == "katarenga":
            self.run_katarenga()
        elif gamemode == "congress":
            self.run_congress()
        elif gamemode == "isolation":
            self.run_isolation()


###################################################################################################


    def run_katarenga(self):
        '''Main loop of the game'''

        self.running = True
        self.selected_tile = None
        
        while self.running:

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.selected_tile == None:
                        self.handle_selection()
                    else:   
                        self.handle_deplacement()
                       
                        
            # Refresh the screen
            self.draw_board()
            self.draw_pawns()
            self.show_possible_moves()
            

            # Refresh the screen
            pygame.display.flip()
            self.clock.tick(self.fps)



###################################################################################################


    def load_assets(self):
        '''Load once all the assets needed in this menu'''
        
        self.tiles_img = {"horse" : pygame.image.load("Assets/Source_files/Images/Create_region/horse.png").convert(),
                          "rook" : pygame.image.load("Assets/Source_files/Images/Create_region/rook.png").convert(),
                          "bishop": pygame.image.load("Assets/Source_files/Images/Create_region/bishop.png").convert(),
                          "king": pygame.image.load("Assets/Source_files/Images/Create_region/king.png").convert(),
                          "queen": pygame.image.load("Assets/Source_files/Images/Create_region/queen.png").convert(),
                          "possible_move": pygame.image.load("Assets/Source_files/Images/Create_region/possible_move.png").convert_alpha()
                          }
        
        self.pawns_img = {"white" : pygame.image.load("Assets/Source_files/Images/white_pawn.png").convert_alpha(),
                          "black" : pygame.image.load("Assets/Source_files/Images/black_pawn.png").convert_alpha()
                          }
        
        self.background_img = pygame.image.load("Assets/Source_files/Images/menu/imgs/Background.png").convert()
        self.board_background_img = pygame.image.load("Assets/Source_files/Images/board_background.png").convert()


###################################################################################################


    def resize_assets(self):

        self.background_img = pygame.transform.smoothscale(self.background_img, (self.screen_width, self.screen_height))
        self.board_background_img = pygame.transform.smoothscale(self.board_background_img, (self.screen_height * 667/720, self.screen_height * 667/720))
        
        for tile in self.tiles_img.keys():
            self.tiles_img[tile] = pygame.transform.smoothscale(self.tiles_img[tile], (self.screen_height * 67/720, self.screen_height * 67/720))

        for pawn in self.pawns_img.keys():
            self.pawns_img[pawn] = pygame.transform.smoothscale(self.pawns_img[pawn], (self.screen_height * 67/720, self.screen_height * 67/720))


###################################################################################################


    def draw_board(self):       
            
        # Drawing the background
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.board_background_img, (self.screen_width * 150/1280, self.screen_height * 30/720))

        # Drawing the tiles
        for row in range(8):
            for column in range(8):
                type = self.game.get_grid()[row][column].get_deplacement()
                self.screen.blit(self.tiles_img[type], (self.screen_width * 150/1280 + (column + 1) * self.screen_height * 67/720, self.screen_height * 30/720 + (row + 1) * self.screen_height * 67/720))


#####################################################################################################


    def draw_pawns(self):
        '''Draw the pawns on the board'''
        
        for row in range(8):
            for column in range(8):
                if (pawn := self.game.get_grid()[row][column].get_pawn()) != None:
                    owner = pawn.get_owner()
                    if owner == self.game.get_player(0):
                        self.screen.blit(self.pawns_img["white"], (self.screen_width * 150/1280 + (column + 1) * self.screen_height * 67/720, self.screen_height * 30/720 + (row + 1) * self.screen_height * 67/720))
                    else:
                        self.screen.blit(self.pawns_img["black"], (self.screen_width * 150/1280 + (column + 1) * self.screen_height * 67/720, self.screen_height * 30/720 + (row + 1) * self.screen_height * 67/720))


####################################################################################################


    def handle_selection(self):
        '''Handle tile selection on the board'''
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate the tile clicked based on mouse position
        column = int((mouse_x - (self.screen_width * 150/1280)) // (self.screen_height * 67/720) - 1)
        row = int((mouse_y - (self.screen_height * 30/720)) // (self.screen_height * 67/720) - 1)

        # Check if the click is within the board boundaries
        if 0 <= row < 8 and 0 <= column < 8:
            self.selected_tile = self.game.get_grid()[row][column]


##############################################################################################################


    def handle_deplacement(self):
        '''Handle tile selection on the board'''

        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        if self.selected_tile.get_pawn() == None:
            self.selected_tile = None

        else:
            x, y = self.selected_tile.get_pawn().get_coordinates()
            moves = self.game.get_possible_moves(x, y)

            selected_column = int((mouse_x - (self.screen_width * 150/1280)) // (self.screen_height * 67/720) - 1)
            selected_row = int((mouse_y - (self.screen_height * 30/720)) // (self.screen_height * 67/720) - 1)
            
            # Check if the clicked tile is a valid move
            if (selected_row, selected_column) in moves:
                self.game.move_pawn(x, y, selected_row, selected_column)
                self.selected_tile = None
            else:
                self.selected_tile = None


###########################################################################################################


    def show_possible_moves(self):
        '''Show the possible moves for the selected tile'''
        
        if self.selected_tile and self.selected_tile.get_pawn() != None and self.selected_tile.get_pawn().get_owner() == self.game.get_current_player():
            pawn_x, pawn_y = self.selected_tile.get_pawn().get_coordinates()
            possible_moves = self.game.get_possible_moves(pawn_x, pawn_y)
            for move in possible_moves:
                row, column = move
                self.screen.blit(self.tiles_img["possible_move"], (self.screen_width * 150/1280 + (column + 1) * self.screen_height * 67/720, self.screen_height * 30/720 + (row + 1) * self.screen_height * 67/720))



