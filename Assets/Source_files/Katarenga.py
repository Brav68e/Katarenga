from Sub_class.tile import *
from Sub_class.pawn import *
from Sub_class.player import *
from Board_creation import Delete_region


class Games:
    
    def __init__(self, grille, username1: str, username2: str):
        """
        Initialize a board using an existing grid of Tile objects.
        """

        self.players = [Player(username1), Player(username2)]

        self.grille = grille
        self.taille = 8
        self.init_pawns(self.players[0], self.players[1])
        self.camps = {"W": [False, False], "B": [False, False]}  # Track if camps are occupied
    
#####################################################
    def afficher(self):
        """Display the board with row and column numbers for easier testing."""
        print("   " + " ".join(str(i) for i in range(self.taille)))  # Print column numbers
        for i, ligne in enumerate(self.grille):
            print(f"{i} " + " ".join(str(case) for case in ligne))  # Print row number and row content
#####################################################
    

    def init_pawns(self, player1: Player, player2: Player):
        """
        Initialize pawns on the board for both players.
        :param player1: Player 1 (White).
        :param player2: Player 2 (Black).
        """

        for i in range(self.taille):
            self.grille[0][i].place_pawn(Pawn(player2, (0, i)))
            self.grille[7][i].place_pawn(Pawn(player1, (7, i)))


    def get_possible_moves(self, x, y):
        """
        Determine possible moves for a pawn on this tile based on its type.
        :param x: Current x-coordinate of the tile.
        :param y: Current y-coordinate of the tile.
        :return: List of valid moves [(new_x, new_y), ...].
        """

        match self.board[x][y].get_deplacement():
            case "bishop":
                moves = self.bishop_moves(x, y)
            case "rook":
                moves = self.rook_moves(x, y)
            case "queen":
                moves = self.queen_moves(x, y)
            case "king":
                moves = self.king_moves(x, y)
            case "knight" | "horse":
                moves = self.knight_moves(x, y)
            case _:
                print(f"Unknown movement pattern: {self.deplacement_pattern}")
                return []

        return moves


    def king_moves(self, x, y):
        """Calculate King-like moves (8 adjacent tiles)."""
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        return self._get_moves_in_directions(x, y, directions, max_steps=1)


    def knight_moves(self, x, y):
        """Calculate Knight-like moves (L-shaped)."""
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        moves = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.taille and 0 <= ny < self.taille:
                # Check if the tile is empty or occupied by an opponent's pawn
                if not (pawn := self.board[nx][ny].get_pawn()) or pawn.get_owner().get_username() != self.current_player.get_username():
                    moves.append((nx, ny))

        return moves


    def bishop_moves(self, x, y):
        """Calculate Bishop-like moves (diagonal) with constraints."""
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self._get_moves_in_directions(x, y, directions, stop_on_pattern="bishop")


    def rook_moves(self, x, y):
        """Calculate Rook-like moves (straight lines) with constraints."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return self._get_moves_in_directions(x, y, directions, stop_on_pattern="rook")


    def queen_moves(self, x, y):
        """Calculate Queen-like moves (combination of Rook and Bishop)."""
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        return self._get_moves_in_directions(x, y, directions)


    def _get_moves_in_directions(self, x, y, directions, max_steps=None, stop_on_pattern=None, capture=True):
        """
        Helper method to calculate moves in given directions.
        :param x: Current x-coordinate of the tile.
        :param y: Current y-coordinate of the tile.
        :param board: The board (2D list of Tile objects).
        :param directions: List of (dx, dy) tuples representing movement directions.
        :param max_steps: Maximum number of steps in a direction (None for unlimited).
        :param stop_on_pattern: Stop moving if a tile with this pattern is encountered.
        :param capture: If True, allow capturing opponent's pawns.
        :return: List of valid moves [(new_x, new_y), ...].
        """
        moves = []

        for dx, dy in directions:
            nx, ny = x, y
            steps = 0
            while True:
                nx, ny = nx + dx, ny + dy
                if not (0 <= nx < self.taille and 0 <= ny < self.taille):
                    break  # Out of bounds

                if pawn := self.board[nx][ny].get_pawn():
                    # Check if the pawn is an opponent's pawn
                    if pawn.get_owner().get_username() != self.current_player.get_username() and self.capture:
                        # Capture the opponent's pawn
                        moves.append((nx, ny))
                        break
                    else:
                        break

                moves.append((nx, ny))

                if stop_on_pattern and self.board[nx][ny].get_deplacement() == stop_on_pattern:
                    break  # Stop if the specified pattern is encountered

                steps += 1
                if max_steps and steps >= max_steps:
                    break  # Stop if max steps are reached

        return moves
        
    


    def move_pawn(self, x: int, y: int, new_x: int, new_y: int):
        """
        Move a pawn from (x, y) to (new_x, new_y).
        :param x: Current x-coordinate of the pawn.
        :param y: Current y-coordinate of the pawn.
        :param new_x: New x-coordinate of the pawn.
        :param new_y: New y-coordinate of the pawn.
        """
        tile = self.grille[x][y]
        target_tile = self.grille[new_x][new_y]

        # If the target tile has a pawn, capture it
        if pawn:= target_tile.pawn_on:
            pawn.get_owner().set_pawns(pawn.get_owner().pawns_nbr() - 1)  # Decrease the pawn count of the owner
            target_tile.pawn_on = None

        # Move the pawn
        target_tile.pawn_on = tile.pawn_on
        tile.pawn_on = None


    def enter_camp(self, pion: str):
        """
        Handle a pawn entering the opponent's camp.
        :param pion: The pawn ('B' or 'W').
        """
        if pion in self.camps and not all(self.camps[pion]):
            for i in range(2):
                if not self.camps[pion][i]:
                    self.camps[pion][i] = True
                    break
        else:
            raise ValueError("Both camps are already occupied.")
        
        
    def katarenga_winner(self):
        """
        Check if there is a winner.
        :return: The winner ('B' or 'W') or None if there is no winner yet.
        """
        if all(self.camps['W']):  # If both camps of 'W' are occupied, 'B' wins
            return 'B'
        elif all(self.camps['B']):  # If both camps of 'B' are occupied, 'W' wins
            return 'W'
        return None
    

    def bot_move(self, bot_player: str):
        """
        Perform a random move for the bot.
        :param bot_player: The bot's player ('B' or 'W').
        """
        possible_moves = []

        # Collect all possible moves for the bot's pawns
        for x in range(self.taille):
            for y in range(self.taille):
                tile = self.grille[x][y]
                if tile.pawn_on == bot_player:
                    moves = self.get_possible_moves(x, y)
                    for move in moves:
                        possible_moves.append((x, y, move[0], move[1]))

        # If no moves are possible, the bot cannot play
        if not possible_moves:
            print(f"No possible moves for bot ({bot_player}).")
            return

        # Randomly select a move
        selected_move = random.choice(possible_moves)
        x, y, new_x, new_y = selected_move

        # Validate and execute the move
        try:
            self.validate_move(x, y, new_x, new_y, bot_player)
            self.move_pawn(x, y, new_x, new_y)
            print(f"Bot ({bot_player}) moved pawn from ({x}, {y}) to ({new_x}, {new_y}).")
        except Exception as e:
            print(f"Bot move failed: {e}")


if __name__ == "__main__":
    # Example usage
    import random
    import pygame

    def creer_grille_personnalisee():
        """
        Create a custom grid with specific tile types for each row and place pawns on their base lines.
        """
        taille = 8
        grille = []

        # Define specific tile types for each row
        tile_types = [
            ["Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook"],  # Top row
            ["Rook"] * taille,  # Second row
            ["Bishop"] * taille,  # Third row
            ["Knight"] * taille,  # Fourth row
            ["Knight"] * taille,  # Fifth row
            ["Bishop"] * taille,  # Sixth row
            ["Rook"] * taille,  # Seventh row
            ["Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook"],  # Bottom row
        ]

        # Create the grid with the specified tile types
        for i in range(taille):
            row = [Tile(deplacement_pattern=tile_types[i][j].lower()) for j in range(taille)]
            grille.append(row)

        # Place pawns for both players on their base lines
        for i in range(taille):
            grille[1][i].place_pawn('B')  # Player B's pawns on the second row
            grille[6][i].place_pawn('W')  # Player W's pawns on the second-to-last row

        # Debugging: Print the grid after initialization
        print("Grid after initialization:")
        for row in grille:
            print([str(tile) for tile in row])

        return grille

    def creer_plateau_depuis_board_creation():
        """
        Create a game board using the combined regions from Board_creation.py and initialize pawns.
        """
        print("Initializing board using Board_creation...")
        pygame.init()
        screen = pygame.display.set_mode((1280, 720))
        board_creator = Delete_region(screen)
        board_creator.run()

        # Combine regions to create the board
        combined_board = board_creator.combine_regions()

        # Initialize pawns for both players
        taille = len(combined_board)
        for i in range(taille):
            combined_board[0][i].place_pawn('B')  # Player B's pawns on the second row
            combined_board[7][i].place_pawn('W')  # Player W's pawns on the second-to-last row

        # Debugging: Print the combined board with pawns
        print("Combined board with pawns initialized:")
        for row in combined_board:
            print([str(tile) for tile in row])

        return combined_board

    def play_game():
        """
        Play the game in a functional mode without a graphical interface.
        """
        print("Welcome to Katarenga!")

        # Create the board using Board_creation
        grille = creer_plateau_depuis_board_creation()

        # Initialize the Plateau with the new board
        plateau = Plateau(grille=grille)
        plateau.afficher()

        current_player = 'W'
        while True:
            print(f"\nPlayer {current_player}'s turn.")
            print("Enter your move in the format: x y new_x new_y")
            print("Example: 1 0 2 0 to move the pawn at (1, 0) to (2, 0).")
            plateau.afficher()

            try:
                move = input("Your move: ").strip()
                print(f"Received input: {move}")
                if move.lower() == "quit":
                    print("Game ended.")
                    break

                x, y, new_x, new_y = map(int, move.split())
                plateau.validate_move(x, y, new_x, new_y, current_player)
                plateau.move_pawn(x, y, new_x, new_y)

                # Check for a winner
                winner = plateau.check_winner()
                if winner:
                    print(f"Player {winner} wins!")
                    break

                # Switch player
                current_player = 'B' if current_player == 'W' else 'W'

            except ValueError as e:
                print(f"Invalid input or move: {e}")
            except IndexError as e:
                print(f"Move out of bounds: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

    #Launch the game
    play_game()

