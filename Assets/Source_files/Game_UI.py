from Katarenga import *
import pygame



class GamesUI():

    def __init__(self, screen, grid, gamemode, usernames, style = "solo"):

        self.game = Games(grid, usernames[0], usernames[1], gamemode)
        self.game.init_pawns()
        self.style = style
        
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

            # Check for game over
            if (player := self.game.katarenga_winner()) != None:
                self.running = False
                print(f"{player} wins !")

            if self.style == "solo" :
                self.bot_move()

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
            self.draw_current_player()

            pygame.display.flip()
            self.clock.tick(self.fps)


###################################################################################################


    def run_congress(self):
        '''Main loop of the game'''

        self.running = True
        self.selected_tile = None
        
        while self.running:

            # Check for game over
            if (player := self.game.congress_winner()) != None:
                self.running = False
                print(f"{player} wins !")

            if self.style == "solo" :
                self.bot_move()

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
            self.draw_current_player()

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
        self.font = pygame.font.Font("Assets/Source_files/fonts/font.ttf", int(self.screen_height * 0.1))


###################################################################################################


    def resize_assets(self):

        self.background_img = pygame.transform.smoothscale(self.background_img, (self.screen_width, self.screen_height))
        
        for tile in self.tiles_img.keys():
            self.tiles_size = int(self.screen_height * 0.093)              # int prevent float number which create space between tiles
            self.tiles_img[tile] = pygame.transform.smoothscale(self.tiles_img[tile], (self.tiles_size, self.tiles_size))

        for pawn in self.pawns_img.keys():
            self.pawns_img[pawn] = pygame.transform.smoothscale(self.pawns_img[pawn], (self.tiles_size, self.tiles_size))

        self.board_background_topleft = (self.screen_width * 125/1280, self.screen_height * 30/720)
        self.board_background_img = pygame.transform.smoothscale(self.board_background_img, (self.tiles_size * 10, self.tiles_size * 10))


###################################################################################################


    def draw_board(self):       
            
        # Drawing the background
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.board_background_img, (self.board_background_topleft[0], self.board_background_topleft[1]))

        # Drawing the tiles
        for row in range(8):
            for column in range(8):
                type = self.game.get_grid()[row][column].get_deplacement()
                self.screen.blit(self.tiles_img[type], (self.board_background_topleft[0] + (column + 1) * self.tiles_size, self.board_background_topleft[1] + (row + 1) * self.tiles_size))

        # Draw the pawns on the camps
        for i in range(2):
            if self.game.get_camps()["W"][i]:
                self.screen.blit(self.pawns_img["white"], (self.board_background_topleft[0] + i * self.tiles_size, self.board_background_topleft[1]))
            if self.game.get_camps()["B"][i]:
                self.screen.blit(self.pawns_img["black"], (self.board_background_topleft[0] + i * self.tiles_size, self.board_background_topleft[1] + 9 * self.tiles_size))


#####################################################################################################


    def draw_pawns(self):
        '''Draw the pawns on the board'''
        
        for row in range(8):
            for column in range(8):
                if (pawn := self.game.get_grid()[row][column].get_pawn()) != None:
                    owner = pawn.get_owner()
                    if owner == self.game.get_player(0):
                        self.screen.blit(self.pawns_img["white"], (self.board_background_topleft[0] + (column + 1) * self.tiles_size, self.board_background_topleft[1] + (row + 1) * self.tiles_size))
                    else:
                        self.screen.blit(self.pawns_img["black"], (self.board_background_topleft[0] + (column + 1) * self.tiles_size, self.board_background_topleft[1] + (row + 1) * self.tiles_size))


####################################################################################################


    def draw_current_player(self):
        '''Draw the current player on the board'''

        # Get the current player and create the formatted string
        current_player = self.game.get_current_player().get_username()
        lines = [f"Turn of {current_player}", "Choose Wisely !"]

        for i, line in enumerate(lines):
            self.title = self.font.render(line, True, "black")
            self.title_pos = self.title.get_rect(center=(self.screen.get_width() * 1025/1280, self.screen.get_height() * (300 + i*100) / 720))
            self.screen.blit(self.title, self.title_pos)


####################################################################################################


    def handle_selection(self):
        '''Handle tile selection on the board'''
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate the tile clicked based on mouse position
        column = int((mouse_x - (self.board_background_topleft[0])) // (self.tiles_size) - 1)
        row = int((mouse_y - (self.board_background_topleft[1])) // (self.tiles_size) - 1)

        # Check if the click is within the board boundaries
        if 0 <= row < 8 and 0 <= column < 8:
            self.selected_tile = self.game.get_grid()[row][column]


##############################################################################################################


    def handle_deplacement(self):
        '''Handle tile selection on the board'''

        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        if self.selected_tile.get_pawn() == None:
            self.selected_tile = None

        elif self.selected_tile.get_pawn().get_owner() == self.game.get_current_player():
            # Get the current pawn's position and possible moves
            x, y = self.selected_tile.get_pawn().get_coordinates()
            moves = self.game.get_possible_moves(x, y)

            selected_column = int((mouse_x - (self.board_background_topleft[0])) // (self.tiles_size) - 1)
            selected_row = int((mouse_y - (self.board_background_topleft[1])) // (self.tiles_size) - 1)
            
            # Check if the clicked tile is a valid move
            if (selected_row, selected_column) in moves:
                self.move_animation(x, y, selected_row, selected_column)
                self.game.move_pawn(x, y, selected_row, selected_column)
                self.game.switch_player()
                self.selected_tile = None
            else:
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
                self.screen.blit(self.tiles_img["possible_move"], (self.board_background_topleft[0] + (column + 1) * self.tiles_size, self.board_background_topleft[1] + (row + 1) * self.tiles_size))


##############################################################################################################


    def move_animation(self, x, y, new_x, new_y):
        '''Animate the movement of the pawn'''
        
        # Get the starting and ending positions
        start_pos = (self.board_background_topleft[0] + (y + 1) * self.tiles_size, self.board_background_topleft[1] + (x + 1) * self.tiles_size)
        end_pos = (self.board_background_topleft[0] + (new_y + 1) * self.tiles_size, self.board_background_topleft[1] + (new_x + 1) * self.tiles_size)

        anim_duration = 750                                                 # Animation duration in milliseconds
        start_time = pygame.time.get_ticks()

        # Animate the movement
        while True:

            current_time = pygame.time.get_ticks() - start_time
            if current_time >= anim_duration:
                break

            progress = current_time / anim_duration                         # 0 to 1 (percentage of animation completed)
            eased_progress = 1 - pow(1 - progress, 3)                       # Ease-in cubic function   f(progress) = 1 - (1-progress)³

            x_pos = start_pos[0] + (end_pos[0] - start_pos[0]) * eased_progress
            y_pos = start_pos[1] + (end_pos[1] - start_pos[1]) * eased_progress

            self.draw_board()
            self.draw_current_player()
            # Draw pawns EXCEPT the one moving
            for row in range(8):
                for column in range(8):
                    if (pawn := self.game.get_grid()[row][column].get_pawn()) != None and (row, column) != (x, y):
                        owner = pawn.get_owner()
                        if owner == self.game.get_player(0):
                            self.screen.blit(self.pawns_img["white"], (self.board_background_topleft[0] + (column + 1) * self.tiles_size, self.board_background_topleft[1] + (row + 1) * self.tiles_size))
                        else:
                            self.screen.blit(self.pawns_img["black"], (self.board_background_topleft[0] + (column + 1) * self.tiles_size, self.board_background_topleft[1] + (row + 1) * self.tiles_size))

            # Draw the moving pawn
            if self.game.get_grid()[x][y].get_pawn().get_owner() == self.game.get_player(0):
                self.screen.blit(self.pawns_img["white"], (x_pos, y_pos))
            else:
                self.screen.blit(self.pawns_img["black"], (x_pos, y_pos))

            pygame.display.flip()
            self.clock.tick(self.fps)


###############################################################################################################


    def bot_move(self):
        '''Perform a random move for the bot.'''
        
        if self.game.get_current_player() == self.game.get_player(1) and self.running:                      # Player 2 (index 1) is the bot
            # Get the bot move
            new_x, new_y, x, y = self.game.bot_move()

            self.move_animation(x, y, new_x, new_y)
            self.game.move_pawn(x, y, new_x, new_y)
            self.game.switch_player()