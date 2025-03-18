class Tile:
    def __init__(self, deplacement_pattern, pawn_on=None, collision=None):
        self.deplacement_pattern = deplacement_pattern 
        self.pawn_on = pawn_on
        self.collision = collision

    def __repr__(self):
        return f"{self.deplacement_pattern[0].upper() if self.deplacement_pattern else '-'}{self.pawn_on if self.pawn_on else ''}"

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
        moves = []
        taille = len(board)

        if self.deplacement_pattern == "King":
            # King-like movement: 8 adjacent tiles
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < taille and 0 <= ny < taille:
                    moves.append((nx, ny))

        elif self.deplacement_pattern == "Knight":
            # Knight-like movement: L-shaped moves
            directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < taille and 0 <= ny < taille:
                    moves.append((nx, ny))

        elif self.deplacement_pattern == "Bishop":
            # Bishop-like movement: Diagonal, stop at the first yellow tile
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dx, dy in directions:
                nx, ny = x, y
                while True:
                    nx, ny = nx + dx, ny + dy
                    if 0 <= nx < taille and 0 <= ny < taille:
                        moves.append((nx, ny))
                        if board[nx][ny].deplacement_pattern == "Bishop" or board[nx][ny].pawn_on:
                            break
                    else:
                        break

        elif self.deplacement_pattern == "Rook":
            # Rook-like movement: Straight lines, stop at the first red tile
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in directions:
                nx, ny = x, y
                while True:
                    nx, ny = nx + dx, ny + dy
                    if 0 <= nx < taille and 0 <= ny < taille:
                        moves.append((nx, ny))
                        if board[nx][ny].deplacement_pattern == "Rook" or board[nx][ny].pawn_on:
                            break
                    else:
                        break

        elif self.deplacement_pattern == "Queen":
            # Queen-like movement: Combine Rook and Bishop logic
            # Diagonal directions (Bishop)
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dx, dy in directions:
                nx, ny = x, y
                while True:
                    nx, ny = nx + dx, ny + dy
                    if 0 <= nx < taille and 0 <= ny < taille:
                        moves.append((nx, ny))
                        if board[nx][ny].deplacement_pattern in ("Bishop", "Queen") or board[nx][ny].pawn_on:
                            break
                    else:
                        break

            # Straight directions (Rook)
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in directions:
                nx, ny = x, y
                while True:
                    nx, ny = nx + dx, ny + dy
                    if 0 <= nx < taille and 0 <= ny < taille:
                        moves.append((nx, ny))
                        if board[nx][ny].deplacement_pattern in ("Rook", "Queen") or board[nx][ny].pawn_on:
                            break
                    else:
                        break

        return moves
