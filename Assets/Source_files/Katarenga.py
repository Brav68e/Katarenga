from Sub_class.tile import *
from Sub_class.pawn import *
from Sub_class.player import *
from Board_creation import Delete_region
from random import choice, random


class Games:
    
    def __init__(self, grille, username1: str, username2: str):
        """
        Initialize a board using an existing grid of Tile objects.
        """

        self.players = [Player(username1), Player(username2)]
        self.current_player = self.players[0]  # Start with player 1

        self.board = grille
        self.taille = 8
        self.init_pawns()
        self.camps = {"W": [False, False], "B": [False, False]}  # Track if camps are occupied
    

    def init_pawns(self):
        """
        Initialize pawns on the board for both players.
        :param player1: Player 1 (White).
        :param player2: Player 2 (Black).
        """

        for i in range(self.taille):
            self.board[0][i].place_pawn(Pawn(self.players[1], (0, i)))
            self.board[7][i].place_pawn(Pawn(self.players[0], (7, i)))


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
                    if pawn.get_owner().get_username() != self.current_player.get_username() and capture:
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
        tile = self.board[x][y]
        target_tile = self.board[new_x][new_y]

        # If the target tile has a pawn, capture it
        if pawn:= target_tile.pawn_on:
            pawn.get_owner().set_pawns(pawn.get_owner().pawns_nbr() - 1)  # Decrease the pawn count of the owner
            target_tile.pawn_on = None

        # Move the pawn
        tile.pawn_on.set_coordinates((new_x, new_y))
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
    

    def bot_move(self):
        """
        Perform a random move for the bot.
        :param bot_player: The bot's player ('B' or 'W').
        """
        possible_moves = []

        # Collect all possible moves for the bot's pawns
        for x in range(self.taille):
            for y in range(self.taille):
                tile = self.board[x][y]
                if (pawn := tile.get_pawn()) and pawn.get_owner().get_username() == self.players[1].get_username():
                    moves = self.get_possible_moves(x, y)
                    for move in moves:
                        possible_moves.append((x, y, move[0], move[1]))

        # Randomly select a move
        selected_move = choice(possible_moves)
        x, y, new_x, new_y = selected_move

        return (new_x, new_y, x, y)


    def get_grid(self):
        """
        Return the grid of tiles.
        :return: 2D list of Tile objects.
        """
        return self.board
    

    def get_player(self, nbr: int):
        """
        Return the first player.
        :param nbr: Player number (0 or 1).
        :return: Player object representing player nbr.
        """
        return self.players[nbr]
    
    def get_current_player(self):
        """
        Return the current player.
        :return: Player object representing the current player.
        """
        return self.current_player
    
    def switch_player(self):
        """
        Switch to the next player.
        """
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]