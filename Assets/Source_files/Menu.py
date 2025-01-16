import pygame, sys

class Menu:
    def __init__(self, root):
        self.root = root
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Menu")

        self.BG = pygame.image.load("Assets/imgs/Background.png")
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        self.current_page = "Katarenga"  # Page active par défaut
        self.buttons = []
        self.icon_buttons = []  # Liste pour les boutons d'icônes
        self.setup_buttons()

    def get_font(self, size):
        return pygame.font.Font("Assets/fonts/font.ttf", size)

    def setup_buttons(self):
        # Boutons principaux
        if self.current_page != "Settings":  # Ne pas afficher ces boutons dans les Settings
            self.buttons = [
                Button(None, (640, 300), "Solo", self.get_font(65), "#FFFFFF", "#888888"),
                Button(None, (640, 400), "Local Multiplayer", self.get_font(65), "#FFFFFF", "#888888"),
                Button(None, (640, 500), "Online Multiplayer", self.get_font(65), "#FFFFFF", "#888888")
            ]
        else:
            self.buttons = [
                Button(None, (640, 300), "Option", self.get_font(65), "#FFFFFF", "#888888"),
                Button(None, (640, 400), "Create Tiles", self.get_font(65), "#FFFFFF", "#888888"),
            ]

        # Chemins vers les images des icônes
        icon_images = [
            "Assets/icons/tour.png",
            "Assets/icons/plateau.png",
            "Assets/icons/I.png",
            "Assets/icons/settings.png"
        ]

        # Création des boutons d'icônes avec des images
        icon_positions = [(290, 635), (490, 635), (690, 635), (890, 635)]
        self.icon_buttons = []  # Réinitialiser les boutons d'icônes

        for index, (pos, image_path) in enumerate(zip(icon_positions, icon_images)):
            # Agrandir le rectangle du bouton actif
            expanded = (
                (self.current_page == "Katarenga" and index == 0) or
                (self.current_page == "Congress" and index == 1) or
                (self.current_page == "Isolation" and index == 2) or
                (self.current_page == "Settings" and index == 3)
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
        title_text = self.get_font(120).render(self.current_page, True, "#FFFFFF")
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

    def update(self):
        # Afficher le fond
        self.screen.blit(self.BG, (0, 0))
        
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

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

class IconButton():
    def __init__(self, pos, text_input, font, base_color, hovering_color, icon_image=None, expanded=False):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.width = 120
        self.height = 70 if not expanded else 120  # Agrandir la hauteur si "expanded" est activé
        self.rect = pygame.Rect(self.x_pos, self.y_pos - (self.height - 70) // 2, self.width, self.height)
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

    def checkForInput(self, position):
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        if self.checkForInput(position):
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
                    if button.checkForInput(mouse_pos):
                        if index == 0:
                            menu.current_page = "Katarenga"
                        elif index == 1:
                            menu.current_page = "Congress"
                        elif index == 2:
                            menu.current_page = "Isolation"
                        elif index == 3:
                            menu.current_page = "Settings"
                        menu.setup_buttons()  # Mettre à jour les boutons pour refléter la nouvelle page
        
        menu.update()
        pygame.display.update()
    
    pygame.quit()
    sys.exit()
