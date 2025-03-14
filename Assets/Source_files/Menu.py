import pygame, sys, os
from Sub_class.button import Button
from Create_region import *

class Menu:
    def __init__(self, root):
        self.root = root
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Menu")
        
        # Dimensions de l'écran
        self.screen_width = 1280
        self.screen_height = 720

        self.BG = pygame.image.load("Assets/Source_files/Images/menu/imgs/Background.png")
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.GREEN = (50, 205, 50)

        self.current_page = "Katarenga"  # Page active par défaut
        self.buttons = []
        self.icon_buttons = []  # Liste pour les boutons d'icônes
        self.volume = 0.5  # Volume initial (50%)
        self.is_dragging = False  # Pour le drag and drop du slider
        
        # Initialiser slider ici
        self.slider_width = 800
        self.slider_height = 20
        self.slider_x = 640 - self.slider_width // 2
        self.slider_y = 200
        button_radius = 25
        self.slider_rect = pygame.Rect(self.slider_x, self.slider_y - button_radius, 
                                  self.slider_width, self.slider_height + 2 * button_radius)
        
        self.setup_buttons()

        # Initialiser le mixer pour le son
        pygame.mixer.init()
        
        # Charger et jouer la musique de fond
        try:
            pygame.mixer.music.load("Assets\Source_files\Sounds\medieval-adventure-154671.mp3")
            pygame.mixer.music.play(-1)  # Jouer en boucle
            pygame.mixer.music.set_volume(self.volume)
        except:
            print("Fichier audio non trouvé, le son sera désactivé")

    def get_font(self, size):
        return pygame.font.Font(r"Assets/Source_files/fonts/font.ttf", size)

    def setup_buttons(self):
        # Boutons principaux
        if self.current_page == "Katarenga":
            self.buttons = [
               Button((640, 300),None,  text_input="Solo", base_color="#514b4b", font_size= int(self.screen_height*0.03), hovering_color="#888888"),
               Button((640, 400),None,  text_input="Local Multiplayer", base_color="#514b4b", font_size= int(self.screen_height*0.03), hovering_color="#888888"),
               Button((640, 500),None,  text_input="Online Multiplayer", base_color="#514b4b", font_size= int(self.screen_height*0.03), hovering_color="#888888")
            ]
        elif self.current_page == "Settings":
            self.buttons = [
                Button((640, 300),None,  text_input="Option", base_color="#514b4b", font_size= int(self.screen_height*0.03), hovering_color="#888888"),
                Button((640, 400),None,  text_input="Rules", base_color="#514b4b", font_size= int(self.screen_height*0.03), hovering_color="#888888"),
                Button((640, 500),None,  text_input="Create Tiles", base_color="#514b4b", font_size= int(self.screen_height*0.03), hovering_color="#888888")
            ]
        elif self.current_page == "Options":
            # Pas de boutons standard sur la page des options
            self.buttons = []
        else:
            self.buttons = [
                Button((640, 300),None,  text_input="Solo", base_color="#514b4b", font_size= int(self.screen_height*0.03), hovering_color="#888888"),
                Button((640, 400),None,  text_input="Local Multiplayer", base_color="#514b4b", font_size= int(self.screen_height*0.03), hovering_color="#888888"),
                Button((640, 500),None,  text_input="Online Multiplayer", base_color="#514b4b", font_size= int(self.screen_height*0.03), hovering_color="#888888")
            ]

        # Chemins vers les images des icônes
        icon_images = [
            "Assets/Source_files/Images/menu/icons/tour.png",
            "Assets/Source_files/Images/menu/icons/plateau.png",
            "Assets/Source_files/Images/menu/icons/I.png",
            "Assets/Source_files/Images/menu/icons/settings.png"
        ]

        # Création des boutons d'icônes avec des images
        icon_positions = [(350, 670), (550, 670), (750, 670), (950, 670)]
        self.icon_buttons = []  # Réinitialiser les boutons d'icônes

        for index, (pos, image_path) in enumerate(zip(icon_positions, icon_images)):
            # Agrandir le rectangle du bouton actif
            expanded = (
                (self.current_page == "Katarenga" and index == 0) or
                (self.current_page == "Congress" and index == 1) or
                (self.current_page == "Isolation" and index == 2) or
                (self.current_page == "Settings" and index == 3) or
                (self.current_page == "Options" and index == 3)  # Garder le bouton Settings actif pour Options
            )
            icon_button = IconButton(
                pos,
                "",
                self.get_font(20),
                "#FFFFFF",
                "#888888",
                icon_image=image_path,
                expanded=expanded
            )
            self.icon_buttons.append(icon_button)

    def draw_title(self):
        # Afficher le titre basé sur la page active
        title_text = self.get_font(120).render(self.current_page, True, "#514b4b")
        title_rect = title_text.get_rect(center=(640, 120))
        self.screen.blit(title_text, title_rect)

    def menu_buttons(self):
        # Fond semi-transparent pour la barre de menu
        s = pygame.Surface((800, 100))
        s.set_alpha(180)
        s.fill(self.BLACK)
        self.screen.blit(s, (250, 620))

        # Dessiner les icônes
        for button in self.icon_buttons:
            button.draw(self.screen)

    def draw_volume_slider(self):
        # "Volume"
        volume_text = self.get_font(60).render("Volume", True, "#514b4b")
        volume_rect = volume_text.get_rect(center=(640, 120))
        self.screen.blit(volume_text, volume_rect)

        # Barre de volume (fond)
        pygame.draw.rect(self.screen, self.GRAY, 
                        (self.slider_x, self.slider_y, self.slider_width, self.slider_height),
                        border_radius=10)
        
        # Barre de volume (barre verte)
        active_width = int(self.slider_width * self.volume)
        pygame.draw.rect(self.screen, self.GREEN, 
                        (self.slider_x, self.slider_y, active_width, self.slider_height),
                        border_radius=10)
        
        # Bouton du slider (rond)
        button_radius = 25
        button_x = self.slider_x + active_width
        button_y = self.slider_y + self.slider_height // 2
        pygame.draw.circle(self.screen, self.GREEN, (button_x, button_y), button_radius)
    
    def draw_display_mode(self):
        # "Display Mode"
        display_text = self.get_font(60).render("Display Mode", True, "#514b4b")
        display_rect = display_text.get_rect(center=(640, 350))
        self.screen.blit(display_text, display_rect)
        
        # Boutons pour les modes d'affichage (plein écran, fenêtré)
        self.display_buttons = [
            Button((500, 450),None,  text_input="Windowed", base_color="#514b4b", font_size= int(self.screen_height*0.03), hovering_color="#888888"),
            Button((800, 450),None,  text_input="Fullscreen", base_color="#514b4b", font_size= int(self.screen_height*0.03), hovering_color="#888888"),
        ]
        
        # Mettre à jour et afficher les boutons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.display_buttons:
            button.changeColor(mouse_pos)
            button.update(self.screen)

    def handle_volume_input(self, pos, is_click=False):
        if self.slider_rect.collidepoint(pos):
            if is_click:
                self.is_dragging = True
            
            if self.is_dragging:
                # Calculer le nouveau volume basé sur la position horizontale du bouton de la barre de volume
                rel_x = max(0, min(pos[0] - self.slider_x, self.slider_width))
                self.volume = rel_x / self.slider_width
                
                # Mettre à jour le volume de la musique
                pygame.mixer.music.set_volume(self.volume)

    def update(self):
        # Afficher le fond
        self.screen.blit(self.BG, (0, 0))
        
        # Si nous sommes sur la page des options, afficher les contrôles spécifiques
        if self.current_page == "Options":
            self.draw_volume_slider()
            self.draw_display_mode()
        else:
            # Afficher le titre
            self.draw_title()
            
            # Récupérer la position de la souris
            mouse_pos = pygame.mouse.get_pos()
            
            # Mettre à jour et afficher chaque bouton principal
            for button in self.buttons:
                button.changeColor(mouse_pos)
                button.update(self.screen)

        # Afficher les boutons du menu (icônes)
        self.menu_buttons()

class IconButton():
    def __init__(self, pos, text_input, font, base_color, hovering_color, icon_image=None, expanded=False):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.width = 120
        self.height = 70 if not expanded else 120  # Agrandir la hauteur si "expanded" est activé
        self.rect = pygame.Rect(self.x_pos - self.width//2, self.y_pos - self.height//2, self.width, self.height)
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.current_color = base_color
        self.icon_image = icon_image
        if self.icon_image:
            self.icon_image = pygame.image.load(icon_image)
            self.icon_image = pygame.transform.scale(self.icon_image, (50, 50))  # Redimensionner l'image si nécessaire

    def draw(self, screen):
        # Dessiner le fond du bouton (rectangle avec coins arrondis)
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)

        # Dessiner l'image à l'intérieur du bouton (centrée)
        if self.icon_image:
            image_rect = self.icon_image.get_rect(center=self.rect.center)
            screen.blit(self.icon_image, image_rect)

    def checkInput(self, position):
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        if self.checkInput(position):
            self.current_color = self.hovering_color
        else:
            self.current_color = self.base_color

if __name__ == "__main__":
    pygame.init()
    menu = Menu(pygame.display.set_mode((1280, 720)))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Vérifier les clics sur les icônes
                for index, button in enumerate(menu.icon_buttons):
                    if button.checkInput(mouse_pos):
                        if index == 0:
                            menu.current_page = "Katarenga"
                        elif index == 1:
                            menu.current_page = "Congress"
                        elif index == 2:
                            menu.current_page = "Isolation"
                        elif index == 3:
                            menu.current_page = "Settings"
                        menu.setup_buttons()  # Mettre à jour les boutons pour refléter la nouvelle page
                
                # Vérifier les clics sur les boutons principaux
                if menu.current_page == "Settings":
                    for i, button in enumerate(menu.buttons):
                        if button.checkInput(mouse_pos):
                            if i == 0:  # Bouton "Option"
                                menu.current_page = "Options"
                                menu.setup_buttons()
                
                # Gérer les clics sur la barre de volume
                if menu.current_page == "Options":
                    menu.handle_volume_input(mouse_pos, True)
                    
                    # Gérer les clics sur les boutons de mode d'affichage
                    if hasattr(menu, 'display_buttons'):
                        for i, button in enumerate(menu.display_buttons):
                            if button.checkInput(mouse_pos):
                                if i == 0:  # Mode fenêtré
                                    pygame.display.set_mode((1280, 720))
                                elif i == 1:  # Mode plein écran
                                    pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                menu.is_dragging = False
            
            elif event.type == pygame.MOUSEMOTION:
                # Mettre à jour le volume si on est en train d'ajuster la barre de volume
                if menu.current_page == "Options" and menu.is_dragging:
                    menu.handle_volume_input(pygame.mouse.get_pos())
        
        menu.update()
        pygame.display.update()
    
    pygame.quit()
    sys.exit()