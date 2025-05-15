from Source_files.Sub_class.button import *
from Source_files.Games import *
import pygame



class GamesUI():

    def __init__(self, screen, gamemode, usernames, grid = None, style = "solo", client = None):

        if style != "online":
            self.game = Games(grid, usernames[0], usernames[1], gamemode)
            self.game.init_pawns()

        self.style = style
        self.gamemode = gamemode
        self.client = client
        if client:
            # Make a relation between client and game_ui
            self.client.set_game_ui(self)
            self.grid = read_board(self.client.send_msg(("get_grid", None)))
            
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
            if (player := (self.game.katarenga_winner() if not self.client else self.client.send_msg(("katarenga_winner", None)))) != None:
                self.running = False
                self.show_winner(player)
                print(f"{player} wins !")
                if self.style != "online" and self.rematch():
                    self.game.reset()
                    self.running = True

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
            if (player := (self.game.congress_winner() if not self.client else self.client.send_msg(("congress_winner", None)))) != None:
                self.running = False
                self.show_winner(player)
                print(f"{player} wins !")
                if self.style != "online" and self.rematch():
                    self.game.reset()
                    self.running = True

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


    def run_isolation(self):
        '''Main loop of the game'''

        self.running = True
        
        while self.running:

            # Check for game over
            if (player := (self.game.isolation_winner() if not self.client else self.client.send_msg(("isolation_winner", None)))) != None:
                self.running = False
                self.show_winner(player)
                print(f"{player} wins !")
                if self.style != "online" and self.rematch():
                    self.game.reset()
                    self.running = True

            if self.style == "solo" :
                self.bot_move()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_placement()
                       
                        
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
        
        self.tiles_img = {"horse" : pygame.image.load("Source_files/Assets/Images/Board/horse.png").convert(),
                          "rook" : pygame.image.load("Source_files/Assets/Images/Board/rook.png").convert(),
                          "bishop": pygame.image.load("Source_files/Assets/Images/Board/bishop.png").convert(),
                          "king": pygame.image.load("Source_files/Assets/Images/Board/king.png").convert(),
                          "queen": pygame.image.load("Source_files/Assets/Images/Board/queen.png").convert(),
                          "possible_move": pygame.image.load("Source_files/Assets/Images/Game/possible_move.png").convert_alpha()
                          }
        
        self.pawns_img = {"white" : pygame.image.load("Source_files/Assets/Images/Game/white_pawn.png").convert_alpha(),
                          "black" : pygame.image.load("Source_files/Assets/Images/Game/black_pawn.png").convert_alpha(),
                          "ghost_white" : pygame.image.load("Source_files/Assets/Images/Game/white_pawn.png").convert_alpha(),
                          "ghost_black" : pygame.image.load("Source_files/Assets/Images/Game/black_pawn.png").convert_alpha()
                          }
        
        self.buttons_img = {"yes" : pygame.image.load("Source_files/Assets/Images/Utility/next.png").convert_alpha(),
                            "no" : pygame.image.load("Source_files/Assets/Images/Utility/next.png").convert_alpha()
                            }

        # Adjust needed images to be transparent
        self.pawns_img["ghost_white"].set_alpha(100)
        self.pawns_img["ghost_black"].set_alpha(100)
        
        self.background_img = pygame.image.load("Source_files/Assets/Images/Menu/Game_Background.png").convert()
        self.board_background_img = pygame.image.load("Source_files/Assets/Images/Game/board_background.png").convert()
        self.font = pygame.font.Font("Source_files/Assets/Fonts/font.ttf", int(self.screen_height * 0.1))


###################################################################################################


    def resize_assets(self):

        self.background_img = pygame.transform.smoothscale(self.background_img, (self.screen_width, self.screen_height))
        
        for tile in self.tiles_img.keys():
            self.tiles_size = int(self.screen_height * 0.093)              # int prevent float number which create space between tiles
            self.tiles_img[tile] = pygame.transform.smoothscale(self.tiles_img[tile], (self.tiles_size, self.tiles_size))

        for pawn in self.pawns_img.keys():
            self.pawns_img[pawn] = pygame.transform.smoothscale(self.pawns_img[pawn], (self.tiles_size, self.tiles_size))

        for button in self.buttons_img.keys():
            self.buttons_img[button] = pygame.transform.smoothscale(self.buttons_img[button], (self.screen_width * 200/1280, self.screen_height * 120/780))

        self.board_background_topleft = (self.screen_width * 125/1280, self.screen_height * 30/720)
        self.board_background_img = pygame.transform.smoothscale(self.board_background_img, (self.tiles_size * 10, self.tiles_size * 10))


###################################################################################################


    def draw_board(self):
        '''Draw the board and its tiles'''
        try:
            # Acquire the board itself
            if self.style == "online":
                grid = self.grid
                camps = self.client.send_msg(("get_camps", []))
            else:
                grid = self.game.get_grid()
                camps = self.game.get_camps()

            # Drawing the background
            self.screen.blit(self.background_img, (0, 0))
            self.screen.blit(self.board_background_img, (self.board_background_topleft[0], self.board_background_topleft[1]))

            # Drawing the tiles
            for row in range(8):
                for column in range(8):
                    type = grid[row][column].get_deplacement()
                    self.screen.blit(self.tiles_img[type], (self.board_background_topleft[0] + (column + 1) * self.tiles_size, self.board_background_topleft[1] + (row + 1) * self.tiles_size))

            # Draw the pawns on the camps
            for i in range(2):
                if camps["W"][i]:
                    self.screen.blit(self.pawns_img["white"], (self.board_background_topleft[0] + i * self.tiles_size*9, self.board_background_topleft[1]))
                if camps["B"][i]:
                    self.screen.blit(self.pawns_img["black"], (self.board_background_topleft[0] + i * self.tiles_size*9, self.board_background_topleft[1] + 9 * self.tiles_size))

        except Exception as e:
            print(f"Error in draw_board: {e}")
            import traceback
            traceback.print_exc()


#####################################################################################################


    def draw_pawns(self):
        '''Draw the pawns on the board'''

        if self.style == "online":
            grid = self.grid
            player0 = self.client.send_msg(("get_player", [0]))["username"]
        else:
            grid = self.game.get_grid()
            player0 = self.game.get_player(0).get_username()
        
        for row in range(8):
            for column in range(8):
                if (pawn := grid[row][column].get_pawn()) != None:
                    owner = pawn.get_owner().get_username()
                    if owner == player0:
                        self.screen.blit(self.pawns_img["white"], (self.board_background_topleft[0] + (column + 1) * self.tiles_size, self.board_background_topleft[1] + (row + 1) * self.tiles_size))
                    else:
                        self.screen.blit(self.pawns_img["black"], (self.board_background_topleft[0] + (column + 1) * self.tiles_size, self.board_background_topleft[1] + (row + 1) * self.tiles_size))


####################################################################################################


    def draw_current_player(self):
        '''Draw the current player on the board'''

        # Get the current player and create the formatted string
        if self.style == "online":
            current_player = self.client.send_msg(("current_player", None))["username"]
        else:
            current_player = self.game.get_current_player().get_username()
        lines = [f"Turn of {current_player}", "Choose Wisely !"]

        for i, line in enumerate(lines):
            self.title = self.font.render(line, True, "black")
            self.title_pos = self.title.get_rect(center=(self.screen.get_width() * 1025/1280, self.screen.get_height() * (300 + i*100) / 720))
            self.screen.blit(self.title, self.title_pos)


####################################################################################################


    def handle_selection(self):
        '''Handle pawn selection on the board'''
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if self.style == "online":
            grid = self.grid
            current_player = self.client.send_msg(("current_player", None))["username"]
            # Check if the current player is me
            if current_player != self.client.get_username():
                return
        else:
            grid = self.game.get_grid()
            current_player = self.game.get_current_player().get_username()

        # Calculate the tile clicked based on mouse position
        column = int((mouse_x - (self.board_background_topleft[0])) // (self.tiles_size) - 1)
        row = int((mouse_y - (self.board_background_topleft[1])) // (self.tiles_size) - 1)

        # Check if the click is within the board boundaries + got a pawn that belongs to the current player
        if 0 <= row < 8 and 0 <= column < 8 and grid[row][column].get_pawn() and grid[row][column].get_pawn().get_owner().get_username() == current_player:
            self.selected_tile = grid[row][column]


##############################################################################################################


    def handle_deplacement(self):
        '''Handle pawn deplacement on the board'''

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Get the current pawn's position and possible moves
        x, y = self.selected_tile.get_pawn().get_coordinates()
        moves = (self.game.get_possible_moves(x, y) if self.style != "online" else self.client.send_msg(("get_possible_moves", [x, y])))

        selected_column = int((mouse_x - (self.board_background_topleft[0])) // (self.tiles_size) - 1)
        selected_row = int((mouse_y - (self.board_background_topleft[1])) // (self.tiles_size) - 1)
        
        # Check if the clicked tile is a valid move
        if self.style == "online" and [selected_row, selected_column] in moves:

            self.game.move_pawn(x, y, selected_row, selected_column) if self.style != "online" else self.client.send_msg(("move_pawn", [x, y, selected_row, selected_column]))
            self.game.switch_player() if self.style != "online" else self.client.send_msg(("switch_player", None))
            self.selected_tile = None

        elif (selected_row, selected_column) in moves:

            self.move_animation(x, y, selected_row, selected_column)
            self.game.move_pawn(x, y, selected_row, selected_column) if self.style != "online" else self.client.send_msg(("move_pawn", [x, y, selected_row, selected_column]))
            self.game.switch_player() if self.style != "online" else self.client.send_msg(("switch_player", None))
            self.selected_tile = None

        else:
            self.selected_tile = None


###########################################################################################################


    def handle_placement(self):
        '''Handle tile placement on the board'''
        
        if self.style == "online" and self.client.send_msg(("current_player", None))["username"] != self.client.get_username():
            # If it's not the player's turn, do nothing
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid = self.game.get_grid() if self.style != "online" else self.grid
        available_tiles = self.game.get_available_tiles() if self.style != "online" else self.client.send_msg(("get_available_tiles", None))
        current_player = self.game.get_current_player() if self.style != "online" else self.client.send_msg(("current_player", None))


        # Calculate the tile clicked based on mouse position
        column = int((mouse_x - (self.board_background_topleft[0])) // (self.tiles_size) - 1)
        row = int((mouse_y - (self.board_background_topleft[1])) // (self.tiles_size) - 1)

        # Check if the click is within the board boundaries
        if 0 <= row < 8 and 0 <= column < 8 and not grid[row][column].get_pawn():
            # Now determine if the tile is available for placement
            if (row, column) in available_tiles: 
                self.game.place_pawn(row, column, current_player) if self.style != "online" else self.client.send_msg(("place_pawn", [row, column, current_player]))
                self.game.switch_player() if self.style != "online" else self.client.send_msg("switch_player, None")


###########################################################################################################


    def show_possible_moves(self):
        '''Show the possible moves for the selected tile'''

        if self.gamemode == "katarenga" or self.gamemode == "congress":
            current_player = self.game.get_current_player().get_username() if self.style != "online" else self.client.send_msg(("current_player", None))["username"]

            if self.selected_tile and self.selected_tile.get_pawn() != None and self.selected_tile.get_pawn().get_owner().get_username() == current_player:
                pawn_x, pawn_y = self.selected_tile.get_pawn().get_coordinates()
                possible_moves = self.game.get_possible_moves(pawn_x, pawn_y) if self.style != "online" else self.client.send_msg(("get_possible_moves", [pawn_x, pawn_y]))

                for row in range(8):
                    for column in range(8):
                        if (row, column) not in possible_moves:
                            self.screen.blit(self.tiles_img["possible_move"], (self.board_background_topleft[0] + (column + 1) * self.tiles_size, self.board_background_topleft[1] + (row + 1) * self.tiles_size))

        # Handle the case for isolation mode
        else:
            x, y = pygame.mouse.get_pos()
            column = int((x - (self.board_background_topleft[0])) // (self.tiles_size) - 1)
            row = int((y - (self.board_background_topleft[1])) // (self.tiles_size) - 1)

            # Make darker the tiles that are not available
            available_tiles = self.game.get_available_tiles() if self.style != "online" else self.client.send_msg(("get_available_tiles", None))
            for r in range(8):
                for c in range(8):
                    if (r, c) not in available_tiles:
                        self.screen.blit(self.tiles_img["possible_move"], (self.board_background_topleft[0] + (c + 1) * self.tiles_size, self.board_background_topleft[1] + (r + 1) * self.tiles_size))

            if 0 <= row < 8 and 0 <= column < 8:
                # Acquire useful information
                current_player = self.game.get_current_player() if self.style != "online" else self.client.send_msg(("current_player", None))
                grid = self.game.get_grid() if self.style != "online" else self.grid
                player0 = self.game.get_player(0) if self.style != "online" else self.client.send_msg(("get_player", [0]))

                if grid[row][column].get_pawn() == None and (row, column) in available_tiles:
                    # Since this is an empty tile, we can show the possible move
                    if current_player == player0:
                        self.screen.blit(self.pawns_img["ghost_white"], (self.board_background_topleft[0] + (column + 1) * self.tiles_size, self.board_background_topleft[1] + (row + 1) * self.tiles_size))
                    else:
                        self.screen.blit(self.pawns_img["ghost_black"], (self.board_background_topleft[0] + (column + 1) * self.tiles_size, self.board_background_topleft[1] + (row + 1) * self.tiles_size))
                    
                    # Display every tile covered by the pawn
                    possible_moves = self.game.get_possible_moves(row, column) if self.style != "online" else self.client.send_msg(("get_possible_moves", [row, column]))
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

        # Acquire information
        grid = self.game.get_grid()
        player0 = self.game.get_player(0)

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
                    if (pawn := grid[row][column].get_pawn()) != None and (row, column) != (x, y):
                        owner = pawn.get_owner()
                        if owner == player0:
                            self.screen.blit(self.pawns_img["white"], (self.board_background_topleft[0] + (column + 1) * self.tiles_size, self.board_background_topleft[1] + (row + 1) * self.tiles_size))
                        else:
                            self.screen.blit(self.pawns_img["black"], (self.board_background_topleft[0] + (column + 1) * self.tiles_size, self.board_background_topleft[1] + (row + 1) * self.tiles_size))

            # Draw the moving pawn
            if grid[x][y].get_pawn().get_owner() == player0:
                self.screen.blit(self.pawns_img["white"], (x_pos, y_pos))
            else:
                self.screen.blit(self.pawns_img["black"], (x_pos, y_pos))

            pygame.display.flip()
            self.clock.tick(self.fps)


###############################################################################################################


    def bot_move(self):
        '''Perform a random move for the bot.'''

        # Acquire the current player and the player 2 (bot)
        current_player = self.game.get_current_player() if self.style != "online" else self.client.send_msg(("current_player", None))
        bot = self.game.get_player(1) if self.style != "online" else self.client.send_msg(("get_player", [1]))

        if self.gamemode == "katarenga" or self.gamemode == "congress":
            if current_player == bot and self.running:                      # Player 2 (index 1) is the bot
                # Get the bot move
                new_x, new_y, x, y = self.game.bot_move() if self.style != "online" else self.client.send_msg(('bot_move', None))

                self.move_animation(x, y, new_x, new_y)
                self.game.move_pawn(x, y, new_x, new_y) if self.style != "online" else self.client.send_msg(("move_pawn", [x, y, new_x, new_y]))
                self.game.switch_player() if self.style != "online" else self.client.send_msg(('switch_player', None))

        else:
            if current_player == bot and self.running:                      # Player 2 (index 1) is the bot
                # Get the bot move
                x, y = self.game.bot_move() if self.style != "online" else self.client.send_msg('bot_move', None)
                self.game.place_pawn(x, y, current_player) if self.style != "online" else self.client.send_msg(("place_pawn", [x, y, current_player]))
                self.game.switch_player() if self.style != "online" else self.client.send_msg(('switch_player', None))
        

###############################################################################################################


    def show_winner(self, winner):
        '''Display the winner of the game'''
        
        # Creating a popup window
        popup = pygame.Surface((self.screen_width * 0.75, self.screen_height * 0.75))
        popup.fill((255, 255, 255))

        # Adding text to the popup
        self.title = self.font.render(f"{winner} won the game !", True, "black")
        self.title_pos = self.title.get_rect(center=(self.screen_width * 0.5, self.screen_height * 0.35))

        # Display the image on the screen
        self.screen.blit(popup, (self.screen_width * 0.125, self.screen_height * 0.125))
        self.screen.blit(self.title, self.title_pos)
        pygame.display.flip()

        # Wait for a few seconds before closing
        pygame.time.delay(3000)
        

###############################################################################################################


    def rematch(self):
        '''Display a popup asking for a rematch'''

        # Creating a popup window
        popup = pygame.Surface((self.screen_width * 0.75, self.screen_height * 0.75))
        popup.fill((255, 255, 255))

        # Adding text to the popup
        self.title = self.font.render("Do you want a rematch ?", True, "black")
        self.title_pos = self.title.get_rect(center=(self.screen_width * 0.5, self.screen_height * 0.35))

        # Adding buttons to the popup
        yes_button = Button((self.screen_width * 0.25, self.screen_height * 0.45), image=self.buttons_img["yes"], text="Yes", font_size= int(self.screen_height/720 * 64))
        no_button = Button((self.screen_width * 0.55, self.screen_height * 0.45), image=self.buttons_img["no"],text="No", font_size= int(self.screen_height/720 * 64))
        
        # Main loop for the popup
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if yes_button.checkInput(event.pos):
                        return True
                    elif no_button.checkInput(event.pos):
                        return False

            # Draw the popup and buttons
            self.screen.blit(popup, (self.screen_width * 0.125, self.screen_height * 0.125))
            self.screen.blit(self.title, self.title_pos)
            yes_button.update(self.screen)
            no_button.update(self.screen)
            pygame.display.flip()


###############################################################################################################


    def set_board(self, grid):
        '''Set the board to a new grid'''
        
        self.grid = grid