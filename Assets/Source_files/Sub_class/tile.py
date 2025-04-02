class Tile:
    def __init__(self, deplacement_pattern, pawn_on=None, collision=None):
        self.deplacement_pattern = deplacement_pattern 
        self.pawn_on = pawn_on
        self.collision = collision

    def __repr__(self):
        """
        Return a string representation of the tile.
        - If the tile has a pawn, show the pawn and the tile type separately.
        - If the tile is empty, show the tile type only.
        """
        pawn = self.pawn_on if self.pawn_on else "-"
        pattern = self.deplacement_pattern if self.deplacement_pattern else "-"
        return f"{pawn}({pattern})"

    def get_pawn(self):
        return self.pawn_on

    def place_pawn(self, pawn):
        self.pawn_on = pawn

    def get_deplacement(self):
        return self.deplacement_pattern

    def get_collision(self):
        return self.collision

    def to_dict(self):
        '''Return a transformed version of the current object in a dictionary (JSON handling)'''
        return {
            "deplacement_pattern": self.deplacement_pattern,
            "pawn_on": self.pawn_on,
            "collision": self.collision
        }

    @staticmethod
    def from_dict(data):
        '''Return a Tile object based on the dictionary version given (JSON handling)'''
        return Tile(data["deplacement_pattern"], data["pawn_on"], data["collision"])

    def get_possible_moves(self, x, y, board):
        """
        Determine possible moves for a pawn on this tile based on its type.
        :param x: Current x-coordinate of the tile.
        :param y: Current y-coordinate of the tile.
        :param board: The board (2D list of Tile objects).
        :return: List of valid moves [(new_x, new_y), ...].
        """
        print(f"Calculating possible moves for tile at ({x}, {y}) with pattern {self.deplacement_pattern} and pawn {self.pawn_on}")
        if not self.deplacement_pattern:
            print(f"No movement pattern defined for tile at ({x}, {y}).")
            return []

        moves = []
        if self.deplacement_pattern.lower() == "king":
            moves = self.king_moves(x, y, board)
        elif self.deplacement_pattern.lower() in ["knight", "horse"]:  # Handle both "knight" and "horse"
            moves = self.knight_moves(x, y, board)
        elif self.deplacement_pattern.lower() == "bishop":
            moves = self.bishop_moves(x, y, board)
        elif self.deplacement_pattern.lower() == "rook":
            moves = self.rook_moves(x, y, board)
        elif self.deplacement_pattern.lower() == "queen":
            moves = self.queen_moves(x, y, board)
        
        print(f"Possible moves for tile at ({x}, {y}): {moves}")
        return moves

    def king_moves(self, x, y, board):
        """Calculate King-like moves (8 adjacent tiles)."""
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        return self._get_moves_in_directions(x, y, board, directions, max_steps=1)

    def knight_moves(self, x, y, board):
        """Calculate Knight-like moves (L-shaped)."""
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        moves = []
        taille = len(board)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < taille and 0 <= ny < taille:
                if not board[nx][ny].pawn_on or board[nx][ny].pawn_on != self.pawn_on:
                    moves.append((nx, ny))

        return moves

    def bishop_moves(self, x, y, board):
        """Calculate Bishop-like moves (diagonal) with constraints."""
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self._get_moves_in_directions(x, y, board, directions, stop_on_pattern="bishop")

    def rook_moves(self, x, y, board):
        """Calculate Rook-like moves (straight lines) with constraints."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return self._get_moves_in_directions(x, y, board, directions, stop_on_pattern="rook")

    def queen_moves(self, x, y, board):
        """Calculate Queen-like moves (combination of Rook and Bishop)."""
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        return self._get_moves_in_directions(x, y, board, directions)

    def _get_moves_in_directions(self, x, y, board, directions, max_steps=None, stop_on_pattern=None):
        """
        Helper method to calculate moves in given directions.
        :param x: Current x-coordinate of the tile.
        :param y: Current y-coordinate of the tile.
        :param board: The board (2D list of Tile objects).
        :param directions: List of (dx, dy) tuples representing movement directions.
        :param max_steps: Maximum number of steps in a direction (None for unlimited).
        :param stop_on_pattern: Stop moving if a tile with this pattern is encountered.
        :return: List of valid moves [(new_x, new_y), ...].
        """
        moves = []
        taille = len(board)

        for dx, dy in directions:
            nx, ny = x, y
            steps = 0
            while True:
                nx, ny = nx + dx, ny + dy
                if not (0 <= nx < taille and 0 <= ny < taille):
                    break  # Out of bounds

                if board[nx][ny].pawn_on:
                    break  # Stop if a pawn is encountered

                moves.append((nx, ny))

                if stop_on_pattern and board[nx][ny].deplacement_pattern.lower() == stop_on_pattern:
                    break  # Stop if the specified pattern is encountered

                steps += 1
                if max_steps and steps >= max_steps:
                    break  # Stop if max steps are reached

        return moves
