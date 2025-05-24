from Source_files.Sub_class.pawn import *

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
            "pawn_on": self.pawn_on.to_dict() if self.pawn_on else self.pawn_on,
            "collision": self.collision
        }

    def from_dict(data):
        '''Return a Tile object based on the dictionary version given (JSON handling)'''
        return Tile(data["deplacement_pattern"], Pawn.from_dict(data["pawn_on"]) if data["pawn_on"] else data["pawn_on"], data["collision"])

    

#################################################################
# Function that is useful for board formatting


def read_board(grid):
    '''Return a Board and Player using Object using a json-like formatted board
    param grid: list of list of Tile object (json-like format)
    return : tuple of (board, owner)
    board: list of list of Tile object
    owner: dictionary of Player object (key : username, value : Player object)
    '''


    try:
        board = []
        owner = {}  # Track players to prevent duplication

        for i, row in enumerate(grid):
            new_row = []
            for j, column in enumerate(row):
                tile = grid[i][j]

                # Check if the tile has a pawn and the owner already exists
                if tile["pawn_on"] and tile["pawn_on"]["owner"]["username"] not in owner:
                    owner[tile["pawn_on"]["owner"]["username"]] = Player.from_dict(tile["pawn_on"]["owner"])

                if tile["pawn_on"]:
                    tile["pawn_on"]["owner"] = owner[tile["pawn_on"]["owner"]["username"]]

                new_row.append(Tile.from_dict(tile))

            board.append(new_row)

        return (board, owner)
    except Exception as e:
        print(f"Error in read_board: {e}")
        import traceback
        traceback.print_exc()
        return None