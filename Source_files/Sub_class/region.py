import json
from .tile import *


class Region():

    total_region = 0

    def __init__(self, board):
        
        self.region = board


#######################################

    def set(self, line, column, value):
        self.region[line][column] = value
    
#######################################

    def get(self):
        return self.region

#######################################

    def rotate(self):
        '''Simply rotate the region by 90° Clockwise'''

        new_region = [[None for i in range(4)] for j in range(4)]           # Create a new 4x4 empty board
        for i, row in enumerate(self.region):
            for j, tile in enumerate(row):
                new_region[i][j] = self.region[3-j][i]

        self.region = new_region

#######################################

    def flip(self):
        '''Flip the region'''

        new_region = [[None for i in range(4)] for j in range(4)]           # Create a new 4x4 empty board
        for i, row in enumerate(self.region):
            for j, tile in enumerate(row):
                new_region[i][j] = self.region[3-i][j]

        self.region = new_region

#######################################

    def display(self, screen, imgs, pos, tile_size):
        '''Display a region at the pos coordinates and need the main screen and a dict with all img associate to their movement'''

        # Blit all the currently placed tiles on the edit board
        for i in range(len(self.region)):
            for j in range(len(self.region)):
                if tile := self.region[i][j]:
                    x, y = pos
                    screen.blit(imgs[tile.get_deplacement()], (x+(j*tile_size), y+(i*tile_size)))
        
#######################################

    def fulfilled(self):
        '''Return a boolean that indicate if the current region is completly filled with Tile'''

        complete = True
        for row in self.region:
            for ele in row:
                complete = complete and isinstance(ele, Tile)

        return complete

#######################################


    def complete(self):
        '''Return a boolean that indicate if the current region match the rules conditions to be save'''

        result = True

        if self.fulfilled():
            # Let's count every type of tile
            amount = {"rook": 0, "bishop": 0, "horse": 0, "king": 0, "queen": 0}
            for row in self.region:
                for tile in row:
                    amount[tile.get_deplacement()] += 1
            
            # Check that each type is either 0 or 4
            for type in amount:
                if amount[type] == 0 or amount[type] == 4:
                    result = result and True
                else:
                    result = result and False

        else:
            result = False

        return result

#######################################

    def to_dict(region):
        '''Return a transformed version of the current object in a dictionnary (JSON handling)'''

        region_dict = {
            "region": [[tile.to_dict() for tile in row] for row in region.region]
        }

        return region_dict
    
#######################################

    def from_dict(dict):
        '''Return a Region object based on the given dictionnary (JSON handling)'''

        grid = dict["region"]
        region = Region([[Tile.from_dict(tile) for tile in row] for row in grid])
        return region
    






###################################################################################################
# JSON file handling about region


def save_region(region):
    '''Add a dictionnary version of a region to the JSON region file'''

    try:
        with open("Source_files/Assets/Data_files/region.json", 'r') as f:
            regions = json.load(f)          # Lecture du fichier

    # Problème de lecture si le fichier est vide
    except(FileNotFoundError, json.JSONDecodeError):
        regions = []

    regions.append(region)
    # Réécrire tout le fichier
    with open("Source_files/Assets/Data_files/region.json", 'w') as f:
        json.dump(regions, f, indent=4)


###################################################################################################


def search_region(target):
    '''Return a boolean that indicate if the specific region (MUST BE THE DICTIONNARY VERSION) is already in the JSON datafile'''

    exist = False
    # Read the file and recreate a list that contain all the regions inside
    with open("Source_files/Assets/Data_files/region.json", 'r') as f:
        regions_dicts = json.load(f)

    for reg in regions_dicts:
        if reg["region"] == target["region"]:
            exist = True

    return exist


###################################################################################################


def region_amount():
    '''Return a int that indicate how many regions are available in your own datas'''

    try:
        with open("Source_files/Assets/Data_files/region.json", 'r') as f:
            regions = json.load(f)          # Lecture du fichier

    # Problème de lecture si le fichier est vide
    except(FileNotFoundError, json.JSONDecodeError):
        regions = []

    return len(regions)


###################################################################################################


def delete_region(index):
    '''Delete a region based on his index'''

    try:
        with open("Source_files/Assets/Data_files/region.json", 'r') as f:
            regions = json.load(f)          # Lecture du fichier

    # Problème de lecture si le fichier est vide
    except(FileNotFoundError, json.JSONDecodeError):
        regions = []

    # Suppresion de la région
    regions.pop(index)

    # Réécrire tout le fichier
    with open("Source_files/Assets/Data_files/region.json", 'w') as f:
        json.dump(regions, f, indent=4)


###################################################################################################


def load_region(index):
    '''Return a Region object based on his index'''

    with open("Source_files/Assets/Data_files/region.json", 'r') as f:
        regions_list = json.load(f)

        # Load new regions
        return Region.from_dict(regions_list[index])