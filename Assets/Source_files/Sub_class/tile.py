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
        moves = []
        taille = len(board)

        if not self.deplacement_pattern:
            print(f"No movement pattern defined for tile at ({x}, {y}).")
            return moves

        if self.deplacement_pattern.lower() == "king":
            # King-like movement: 8 adjacent tiles
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < taille and 0 <= ny < taille:
                    if not board[nx][ny].pawn_on or board[nx][ny].pawn_on != self.pawn_on:
                        moves.append((nx, ny))

        elif self.deplacement_pattern.lower() == "pawn":
            # Pawn-like movement: Forward one step
            direction = -1 if self.pawn_on == 'B' else 1  # Player B moves up, Player N moves down
            nx, ny = x + direction, y
            if 0 <= nx < taille and not board[nx][ny].pawn_on:
                moves.append((nx, ny))

        elif self.deplacement_pattern.lower() == "knight":
            # Knight-like movement: L-shaped moves
            directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < taille and 0 <= ny < taille:
                    if not board[nx][ny].pawn_on or board[nx][ny].pawn_on != self.pawn_on:
                        moves.append((nx, ny))

        elif self.deplacement_pattern.lower() == "bishop":
            # Bishop-like movement: Diagonal
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dx, dy in directions:
                nx, ny = x, y
                while True:
                    nx, ny = nx + dx, ny + dy
                    if 0 <= nx < taille and 0 <= ny < taille:
                        if not board[nx][ny].pawn_on or board[nx][ny].pawn_on != self.pawn_on:
                            moves.append((nx, ny))
                        if board[nx][ny].pawn_on:
                            break
                    else:
                        break

        elif self.deplacement_pattern.lower() == "rook":
            # Rook-like movement: Straight lines
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in directions:
                nx, ny = x, y
                while True:
                    nx, ny = nx + dx, ny + dy
                    if 0 <= nx < taille and 0 <= ny < taille:
                        if not board[nx][ny].pawn_on or board[nx][ny].pawn_on != self.pawn_on:
                            moves.append((nx, ny))
                        if board[nx][ny].pawn_on:
                            break
                    else:
                        break

        elif self.deplacement_pattern.lower() == "queen":
            # Queen-like movement: Combine Rook and Bishop logic
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in directions:
                nx, ny = x, y
                while True:
                    nx, ny = nx + dx, ny + dy
                    if 0 <= nx < taille and 0 <= ny < taille:
                        if not board[nx][ny].pawn_on or board[nx][ny].pawn_on != self.pawn_on:
                            moves.append((nx, ny))
                        if board[nx][ny].pawn_on:
                            break
                    else:
                        break

        print(f"Possible moves for tile at ({x}, {y}): {moves}")
        return moves
