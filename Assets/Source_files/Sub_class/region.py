import json



class Region():

    total_region = 0

    def __init__(self, board):
        
        self.region = board

#######################################

    def get_region(self):
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

    def to_dict(region):
        '''Return a transformed version of the current object in a dictionnary (JSON handling)'''

        region_dict = {
            "region": [[tile.to_dict() for tile in row] for row in region.region]
        }

        return region_dict
    
#######################################

    def from_dict(dict):
        '''Return a Region object based on the given dictionnary (JSON handling)'''

        region = Region(dict["region"])

        return region
    

###################################################################################################
# JSON file handling about region


def save_region(region):
    '''Add a dictionnary version of a region to the JSON region file'''

    try:
        with open("Assets/Source_files/Data_files/region.json", 'r') as f:
            regions = json.load(f)          # Lecture du fichier

    # Problème de lecture si le fichier est vide
    except(FileNotFoundError, json.JSONDecodeError):
        regions = []

    regions.append(region)
    # Réécrire tout le fichier
    with open("Assets/Source_files/Data_files/region.json", 'w') as f:
        json.dump(regions, f, indent=4)


###################################################################################################


def search_region(target):
    '''Return a boolean that indicate if the specific region (MUST BE THE DICTIONNARY VERSION) is already in the JSON datafile'''

    exist = False
    # Read the file and recreate a list that contain all the regions inside
    with open("Assets/Source_files/Data_files/region.json", 'r') as f:
        regions_dicts = json.load(f)

    for reg in regions_dicts:
        if reg["region"] == target["region"]:
            exist = True

    return exist