from Source_files.Sub_class.button import *
from Source_files.Games import *
from Source_files.Menu.ingame_menu import InGameMenu
import pygame
from Source_files.Assets.Sounds.button_sound import ButtonSound



class GamesUI():

    def __init__(self, screen, gamemode, usernames, grid = None, style = "solo", client = None):


        self.game = Games(grid, usernames[0], usernames[1], gamemode)
        self.game.init_pawns()

        self.style = style
        self.gamemode = gamemode
        self.usernames = usernames
        self.client = client
        self.move_pawn = False                      # Used to check if the pawn is moving in online mode

        if client:
            # Make a relation between client and game_ui
            self.client.set_game_ui(self)
            
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
                self.show_winner(player)

                if self.style != "online" and self.rematch():
                    self.game.reset()
                    self.running = True

            if self.style == "solo" :
                self.bot_move()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and self.style in ("solo", "multi","online"):
                    leave_game = self.pause_menu()
                    if leave_game and self.style != "online":
                        self.running = False
                    elif leave_game and self.style == "online":
                        # Stop the game and send a message to the server
                        self.client.send_move("stop_game", None)
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

            # Check for online animation
            if self.style == "online" and self.move_pawn:

                self.move_animation(self.x, self.y, self.new_x, self.new_y)
                self.game.move_pawn(self.x, self.y, self.new_x, self.new_y)
                self.game.switch_player()
                self.selected_tile = None
                self.move_pawn = False

            pygame.display.flip()
            self.clock.tick(self.fps)


###################################################################################################


    def run_congress(self):
        '''Main loop of the game'''

        self.running = True
        self.selected_tile = None
        
        while self.running:

            # Check for game over
            if player := self.game.congress_winner():
                self.running = False
                self.show_winner(player)

                if self.style != "online" and self.rematch():
                    self.game.reset()
                    self.running = True
                

            if self.style == "solo" :
                self.bot_move()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and self.style in ("solo", "multi","online"):
                    leave_game = self.pause_menu()
                    if leave_game and self.style != "online":
                        self.running = False
                    elif leave_game and self.style == "online":
                        # Stop the game and send a message to the server
                        self.client.send_move("stop_game", None)
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

            # Check for online animation
            if self.style == "online" and self.move_pawn:

                self.move_animation(self.x, self.y, self.new_x, self.new_y)
                self.game.move_pawn(self.x, self.y, self.new_x, self.new_y)
                self.game.switch_player()
                self.selected_tile = None
                self.move_pawn = False

            pygame.display.flip()
            self.clock.tick(self.fps)


###################################################################################################


    def run_isolation(self):
        '''Main loop of the game'''

        self.running = True
        
        while self.running:

            # Check for game over
            if player := self.game.isolation_winner():
                self.running = False
                self.show_winner(player)

                if self.style != "online" and self.rematch():
                    self.game.reset()
                    self.running = True


            if self.style == "solo" :
                self.bot_move()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and self.style in ("solo", "multi","online"):
                    leave_game = self.pause_menu()
                    if leave_game and self.style != "online":
                        self.running = False
                    elif leave_game and self.style == "online":
                        # Stop the game and send a message to the server
                        self.client.send_move("stop_game", None)
                        self.running = False
                        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_placement()
                       
                        
            # Refresh the screen
            self.draw_board()
            self.draw_pawns()
            self.show_possible_moves_isolation()
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
        self.popup_img = pygame.image.load("Source_files/Assets/Images/Menu/popup.png").convert_alpha()
        self.get_camps_img = pygame.image.load("Source_files/Assets/Images/Board/sun.png").convert_alpha()
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

        self.get_camps_img = pygame.transform.smoothscale(self.get_camps_img, (int(self.tiles_size), int(self.tiles_size)))
        self.board_background_topleft = (self.screen_width * 125/1280, self.screen_height * 30/720)
        self.board_background_img = pygame.transform.smoothscale(self.board_background_img, (self.tiles_size * 10, self.tiles_size * 10))
        self.popup_img = pygame.transform.smoothscale(self.popup_img, (self.screen_width * 0.75, self.screen_height * 0.75))


###################################################################################################


    def draw_board(self):
        '''Draw the board and its tiles'''
        try:
            # Acquire the board itself
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

        grid = self.game.get_grid()
        player0 = self.game.get_player(0)
        
        for row in range(8):
            for column in range(8):
                if (pawn := grid[row][column].get_pawn()) != None:
                    owner = pawn.get_owner()
                    if owner == player0:
                        self.screen.blit(self.pawns_img["white"], (self.board_background_topleft[0] + (column + 1) * self.tiles_size, self.board_background_topleft[1] + (row + 1) * self.tiles_size))
                    else:
                        self.screen.blit(self.pawns_img["black"], (self.board_background_topleft[0] + (column + 1) * self.tiles_size, self.board_background_topleft[1] + (row + 1) * self.tiles_size))


####################################################################################################


    def draw_current_player(self):
        '''Draw the current player on the board, always well placed'''

        # Get the current player and create the formatted string
        current_player = self.game.get_current_player().get_username()
        
        # Prepare lines
        lines = ["Turn of", f"{current_player}", "Choose Wisely !"]
        font_sizes = [48, 56, 40]  # Different font sizes for hierarchy
        fonts = [pygame.font.Font("Source_files/Assets/Fonts/font.ttf", size) for size in font_sizes]
        
        # Define the area for the text (right panel)
        panel_x = int(self.screen.get_width() * 0.64)
        panel_y = int(self.screen.get_height() * 0.10)
        panel_w = int(self.screen.get_width() * 0.32)
        panel_h = int(self.screen.get_height() * 0.80)
    
        # Calculate total height of all lines
        rendered_lines = [fonts[i].render(line, True, "black") for i, line in enumerate(lines)]
        total_height = sum(text.get_height() for text in rendered_lines) + 20 * (len(lines) - 1)
        start_y = panel_y + (panel_h - total_height) // 2
        
        # Blit each line centered in the panel
        y = start_y
        for i, text in enumerate(rendered_lines):
            text_rect = text.get_rect(center=(panel_x + panel_w // 2, y + text.get_height() // 2))
            self.screen.blit(text, text_rect)
            y += text.get_height() + 20


####################################################################################################


    def handle_selection(self):
        '''Handle pawn selection on the board'''
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        grid = self.game.get_grid()
        current_player = self.game.get_current_player().get_username()

        # Check if it's the player's turn
        if self.style == "online" and current_player != self.client.get_username():
            return

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
        moves = self.game.get_possible_moves(x, y)

        selected_column = int((mouse_x - (self.board_background_topleft[0])) // (self.tiles_size) - 1)
        selected_row = int((mouse_y - (self.board_background_topleft[1])) // (self.tiles_size) - 1)
        
        # Check if the clicked tile is a valid move
        if (selected_row, selected_column) in moves:

            self.move_animation(x, y, selected_row, selected_column)
            self.game.move_pawn(x, y, selected_row, selected_column)

            if self.style == "online":
                # Send a message to update game state
                self.client.send_move("deplacement", [x, y, selected_row, selected_column, self.game.get_current_player().get_username()])

            self.game.switch_player()
            self.selected_tile = None

        else:
            self.selected_tile = None


###########################################################################################################


    def online_deplacement(self, x, y, new_x, new_y, current_player):
        '''Handle pawn deplacement on the board in online mode'''

        # Check if the clicked tile is a valid move
        if current_player == self.game.get_current_player().get_username():

            self.x = x
            self.y = y
            self.new_x = new_x
            self.new_y = new_y
            self.move_pawn = True


###########################################################################################################


    def handle_placement(self):
        '''Handle tile placement on the board'''
        
        if self.style == "online" and self.game.get_current_player().get_username() != self.client.get_username():
            # If it's not the player's turn, do nothing
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()
        available_tiles = self.game.get_available_tiles()
        available_tiles = [tuple(tile) for tile in available_tiles]
        current_player = self.game.get_current_player()


        # Calculate the tile clicked based on mouse position
        column = int((mouse_x - (self.board_background_topleft[0])) // (self.tiles_size) - 1)
        row = int((mouse_y - (self.board_background_topleft[1])) // (self.tiles_size) - 1)

        # Check if the click is within the board boundaries
        if 0 <= row < 8 and 0 <= column < 8 and (row, column) in available_tiles :

            self.game.place_pawn(row, column, current_player)

            if self.style == "online":
                # Send a message to update game state
                self.client.send_move("placement", [row, column, current_player.get_username()])

            self.game.switch_player()


###########################################################################################################


    def online_placement(self, x, y, current_player):
        '''Handle pawn deplacement on the board in online mode'''

        if current_player == self.game.get_current_player().get_username():

            current_player = self.game.get_current_player()
            self.game.place_pawn(x, y, current_player)
            self.game.switch_player()


###########################################################################################################


    def show_possible_moves(self):
        '''Show the possible moves for the selected tile, used for congress and katarenga'''

        current_player = self.game.get_current_player().get_username()

        if self.selected_tile and self.selected_tile.get_pawn() != None and self.selected_tile.get_pawn().get_owner().get_username() == current_player:
            pawn_x, pawn_y = self.selected_tile.get_pawn().get_coordinates()
            possible_moves = self.game.get_possible_moves(pawn_x, pawn_y)
            possible_moves = [tuple(move) for move in possible_moves]

            for row in range(8):
                for column in range(8):
                    if (row, column) not in possible_moves:
                        self.screen.blit(self.tiles_img["possible_move"], (self.board_background_topleft[0] + (column + 1) * self.tiles_size, self.board_background_topleft[1] + (row + 1) * self.tiles_size))

            for move in possible_moves:
                row, column = move
                if (row == -1 or row == 8):
                    self.screen.blit(self.get_camps_img, (self.board_background_topleft[0] + (column + 1) * self.tiles_size, self.board_background_topleft[1] + (row + 1) * self.tiles_size))



##############################################################################################################


    def show_possible_moves_isolation(self):
        '''Show the possible moves for the selected tile, used for isolation'''

        # Acquire useful information
        current_player = self.game.get_current_player()
        player0 = self.game.get_player(0)
        x, y = pygame.mouse.get_pos()
        column = int((x - (self.board_background_topleft[0])) // (self.tiles_size) - 1)
        row = int((y - (self.board_background_topleft[1])) // (self.tiles_size) - 1)

        # Make darker the tiles that are not available
        available_tiles = self.game.get_available_tiles()
        available_tiles = [tuple(tile) for tile in available_tiles]
        for r in range(8):
            for c in range(8):
                if (r, c) not in available_tiles:
                    self.screen.blit(self.tiles_img["possible_move"], (self.board_background_topleft[0] + (c + 1) * self.tiles_size, self.board_background_topleft[1] + (r + 1) * self.tiles_size))

        # If this is online, check if the player is the current player
        if self.style == "online" and current_player.get_username() != self.client.get_username():
            return

        if 0 <= row < 8 and 0 <= column < 8:
            if (row, column) in available_tiles:
                # Since this is an empty tile, we can show the possible move
                if current_player == player0:
                    self.screen.blit(self.pawns_img["ghost_white"], (self.board_background_topleft[0] + (column + 1) * self.tiles_size, self.board_background_topleft[1] + (row + 1) * self.tiles_size))
                else:
                    self.screen.blit(self.pawns_img["ghost_black"], (self.board_background_topleft[0] + (column + 1) * self.tiles_size, self.board_background_topleft[1] + (row + 1) * self.tiles_size))
                
                # Display every tile covered by the pawn
                possible_moves = self.game.get_possible_moves(row, column)
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

        if current_player == bot and self.running:
            pygame.time.delay(1700)

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
        
        # Play the win sound
        win_sound = pygame.mixer.Sound("Source_files/Assets/Sounds/win.mp3")
        win_sound.play()

        # Adding text to the popup
        self.title = self.font.render(f"{winner} won the game !", True, "black")
        self.title_pos = self.title.get_rect(center=(self.screen_width * 0.5, self.screen_height * 0.35))

        # Display the image on the screen
        self.screen.blit(self.popup_img, (self.screen_width * 0.125, self.screen_height * 0.125))
        self.screen.blit(self.title, self.title_pos)
        pygame.display.flip()

        # Wait for a few seconds before closing
        pygame.time.delay(3000)
        

###############################################################################################################


    def rematch(self):
        '''Display a popup asking for a rematch'''

        # Adding text to the popup
        self.title = self.font.render("Do you want a rematch ?", True, "black")
        self.title_pos = self.title.get_rect(center=(self.screen_width * 0.5, self.screen_height * 0.35))

        # Adding buttons to the popup
        yes_button = Button((self.screen_width * 0.25, self.screen_height * 0.45), self.buttons_img["yes"], text="Yes", font_size= int(self.screen_height/720 * 64))
        no_button = Button((self.screen_width * 0.55, self.screen_height * 0.45), self.buttons_img["no"],text="No", font_size= int(self.screen_height/720 * 64))
        
        # Main loop for the popup
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if yes_button.checkInput(event.pos):
                        ButtonSound.play()
                        return True
                    if no_button.checkInput(event.pos):
                        ButtonSound.play()
                        return False

            # Draw the popup and buttons
            self.screen.blit(self.popup_img, (self.screen_width * 0.125, self.screen_height * 0.125))
            self.screen.blit(self.title, self.title_pos)
            yes_button.update(self.screen)
            no_button.update(self.screen)
            pygame.display.flip()


###############################################################################################################


    def set_board(self, grid):
        '''Set the board to a new grid'''
        
        self.grid = grid
        
        
###############################################################################################################


    def pause_menu(self):
        """Affiche le menu pause via InGameMenu"""
        menu = InGameMenu(self.screen, self.screen_width, self.screen_height, self.clock, self.fps)
        return menu.show()


###############################################################################################################


    def stop(self):
        '''Stop the game, usefull when leaving the game or closing the window in online mode'''
        
        self.running = False
