from Assets.Source_files.Sub_class.player import *
from Assets.Source_files.Sub_class.tile import *
import pygame
import cv2
import numpy as np


class Template():

    def __init__(self, root, board, username1, username2):

        #Game gestion
        self.board = board
        self.board_size = 8
        self.players = [Player(username1), Player(username2)]
        self.current_player = self.players[0]
        self.opponent = self.players[1]
        self.selected_pawn = None


        #GUI part
        self.root = root


##############################################################################
    

    def king_possibilities(self, pawn, capture):
        '''Return a list of coordinates based on the current pawn movement possibilities'''
        
        possibilities = []
        coord = pawn.get_coordinates()
        line, column = coord[0], coord[1]
        
        for i in range(-1, 0, 1):
            for j in range(-1, 0, 1):
                line_target = line + i
                column_target = column + j
                #Check if the targetted tile is inside the board
                if (0 < line_target < self.board_size) and (0 < column_target < self.board_size) :
                    pawn = self.board[line_target][column_target].get_pawn()
                    #Capture check
                    if (pawn==None or (pawn.get_owner()==self.opponent and capture)) :
                        possibilities.append((line_target, column_target))

        return possibilities


##############################################################################


    def knight_possibilities(self, pawn, capture):
        '''Return a list of coordinates based on the current pawn movement possibilities'''

        possibilities = []
        coord = pawn.get_coordinates()
        line, column = coord[0], coord[1]

        target_add = ((-2,-1), (-2,1), (-1,2), (1,2), (2,1), (2,-1), (1,-2), (-1,-2))       #Relatif knight possibilities
        for target in target_add:
            line_target = line + target[0]
            column_target = column + target[1]                            
            #Check if the targetted tile is inside the board
            if (0 < line_target < self.board_size) and (0 < column_target < self.board_size) :
                pawn = self.board[line_target][column_target].get_pawn()
                #Capture check
                if (pawn==None or (pawn.get_owner()==self.opponent and capture)) :
                    possibilities.append((line_target, column_target))

        return possibilities

##############################################################################


    def rook_possibilities(self, pawn, capture):
        '''Return a list of coordinates based on the current pawn movement possibilities'''

        possibilities = []
        coord = pawn.get_coordinates()
        line, column = coord[0], coord[1]

        directions = ((1,0), (-1,0), (0,1), (0,-1))
        for direction in directions:
            count = 1
            line_target = line + direction[0]
            column_target = column + direction[1]
            #Is a possibility if : Inside the board AND not a rook tile AND empty tile / take tile 
            while (0 < line_target < self.board_size) and (0 < column_target < self.board_size) and (self.board[line_target][column_target].get_deplacement()!="rook") and (((pawn := self.board[line_target][column_target].get_pawn()) == None) or (pawn.get_owner()==self.opponent and capture)):
                possibilities.append((line_target, column_target))
                count += 1
                line_target = line + direction[0] * count
                column_target = column + direction[1] * count

        return possibilities


##############################################################################


    def bishop_possibilities(self, pawn, capture):
        '''Return a list of coordinates based on the current pawn movement possibilities'''

        possibilities = []
        coord = pawn.get_coordinates()
        line, column = coord[0], coord[1]

        directions = ((1,1), (-1,1), (-1,1), (-1,-1))
        for direction in directions:
            count = 1
            line_target = line + direction[0]
            column_target = column + direction[1]
            #Is a possibility if : Inside the board AND not a bishop tile AND empty tile / take tile 
            while ((0 < line_target < self.board_size) and (0 < column_target < self.board_size)) and (self.board[line_target][column_target].get_deplacement()!="bishop") and (((pawn := self.board[line_target][column_target].get_pawn()) == None) or (pawn.get_owner()==self.opponent and capture)):
                possibilities.append((line_target, column_target))
                count += 1
                line_target = line + direction[0] * count
                column_target = column + direction[1] * count


##############################################################################


    def queen_possibilities(self, pawn, capture):
        '''Return a list of coordinates based on the current pawn movement possibilities'''

        possibilities = self.bishop_possibilities(pawn, capture)
        possibilities += self.rook_possibilities(pawn, capture)
        return possibilities







##########################################################################################################################################################################################################################################


if __name__ == "__main__":
    	
    # Initialisation de Pygame
    pygame.init()

    # Charger la vidéo avec OpenCV
    video_path = "Assets/Source_files/test.mp4"  # Remplacez par le chemin de votre vidéo
    cap = cv2.VideoCapture(video_path)

    # Obtenir les dimensions de la vidéo
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Configurer la fenêtre Pygame
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Lecture de la vidéo")


    # Lecture de la vidéo
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Lire une frame de la vidéo
        ret, frame = cap.read()
        if not ret:
            print("Fin de la vidéo.")
            running = False
            break

        # Convertir la frame d'OpenCV (BGR) en Pygame (RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (1920, 1080))
        frame_surface = pygame.surfarray.make_surface(np.transpose(frame, (1, 0, 2)))

        # Afficher la frame dans la fenêtre Pygame
        screen.blit(frame_surface, (0, 0))

        pygame.draw.rect(screen, "red", (500,500,800,800))

        pygame.display.flip()

        # Contrôler la vitesse de lecture
        clock.tick(fps)

    # Libérer les ressources
    cap.release()
    pygame.quit()
